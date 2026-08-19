# Operating Systems → The Agent Runtime

> **If the LLM is the CPU, AI_Keystone is the operating system.**

This is the governing analogy of the project. It is not decoration: each mapping below names a
component that has to be designed, and the operating-systems literature is a genuinely useful
guide to designing it.

---

## 1 · The claim

A language model can reason. It cannot:

- schedule its own work, or decide what runs next when a hundred requests arrive
- survive the process that hosts it dying mid-task
- hold state across minutes or days
- reach the outside world safely
- stop one tenant from consuming everything
- explain what it did, or let you re-examine it afterwards

Those are precisely the responsibilities an operating system assumed on behalf of programs.
Programs did not *become* able to multitask, page memory, or survive faults — the OS provided
those properties from the outside. The agent runtime is that layer, one level up.

---

## 2 · The mapping

| Operating system | Agent runtime | Built in |
| --- | --- | --- |
| Process scheduler | Run scheduling — priority, aging, fairness | Ph 3 |
| Process control block | Run state — externalised, checkpointed | Ph 3 |
| Write-ahead log & recovery | Event log; state = `fold(events)`; recovery by replay | Ph 3 |
| Context switch | Checkpoint out; resume on a different worker | Ph 3 |
| System call interface | Tool boundary — the controlled path outward | Ph 4 |
| Protection rings / privilege | Capability model, credential brokering, sandboxing | Ph 4 |
| Memory hierarchy | Working / episodic / semantic memory across L1–L3 tiers | Ph 5 |
| Demand paging & page faults | Semantic page fault — retrieve evicted context on miss | Ph 5 |
| Prefetching | Anticipatory tier promotion by access frequency | Ph 5 |
| Inter-process communication | Agent-to-agent messaging, handoff, delegation | Ph 6 |
| Interrupt / fault handling | Timeouts, cancellation, tool failure, compensation | Ph 3–4 |
| cgroups / resource limits | Per-tenant quotas, token budgets, concurrency caps | Ph 7, 14 |
| Debugger / `strace` | Trajectory tracing, deterministic replay, time-travel debug | Ph 11 |

Diagram: [`../architecture/diagrams/os-to-runtime-mapping.md`](../architecture/diagrams/os-to-runtime-mapping.md)

---

## 3 · A run is a process

The naive agent loop keeps everything in local variables:

```python
messages = [system_prompt, user_input]
while True:
    response = llm(messages)
    if response.tool_calls:
        messages.append(execute_tool(response.tool_calls))
    else:
        return response.text
```

The agent's entire existence lives inside one process. Kill the process and the agent ceases to
have ever existed — no history, no partial result, no way to resume, no way to inspect.

An OS solves this by **externalising process state**. The Process Control Block lives in kernel
memory, not in the program's registers: program counter, stack pointer, open file descriptors,
memory map. Because the state is *outside* the running thing, the kernel can suspend it, migrate
it, inspect it, and resume it.

The runtime does the same. A `Run` record in PostgreSQL holds identity, status, current step,
consumed budgets, and lease. **Workers become interchangeable** — the run isn't *in* a worker; it's
in the database, and any worker can pick it up.

| PCB field | Run field |
| --- | --- |
| Program counter | Current step index |
| Registers / stack | Accumulated messages and intermediate values |
| Open file descriptors | Active tool handles, credential references |
| Process state (ready/running/blocked) | `pending` / `running` / `paused` / `failed` / `completed` |
| Priority, nice value | Scheduling priority with aging |

---

## 4 · The event log is a write-ahead log

There are two ways to persist run state.

**Mutable state** — keep one row, overwrite it each step. Simple, and it throws away history. You
know *where* the run is; you have no idea how it got there.

**Event sourcing** — append immutable events; current state is a fold over them:

```
state = fold(apply_event, initial_state, events)
```

This is the **write-ahead log**, unchanged. A database doesn't mutate a page and hope; it appends
a change record first, and crash recovery means replaying the log. Same mechanism, same reason:
*an append is atomic, and history is the source of truth.*

What follows for free:

- **Complete history** — every decision, tool result, and model response
- **Audit trail** — inherent, not a separate system
- **Atomicity** — one event, one transaction; no half-written state
- **Time travel** — state at step *n* is `fold(events[:n])`
- **Replay** — which enables everything in §5

The costs are the same ones a DBMS pays: reads require a fold (mitigated by snapshots) and the log
grows (mitigated by compaction).

---

## 5 · The determinism boundary — where the analogy runs out

Here the agent runtime needs something an OS does not.

Replaying a run to debug it fails naively: the LLM returns something different this time, so you
follow a different path. You haven't reproduced the failure; you've created a new run.

The fix is to split the code in two:

| Category | Examples | Property |
| --- | --- | --- |
| **Deterministic orchestration** | Branching, loop conditions, which tool to call next | Same inputs → same behaviour |
| **Non-deterministic effects** | Model calls, tool calls, `now()`, `random()`, network I/O | Same inputs → possibly different results |

**The rule:** an effect executes **once** and its result is recorded in the event log. On replay,
the effect is *not re-executed* — the recorded result is served from history. Orchestration
therefore follows the identical path, and replay is byte-identical.

The constraint this imposes is real: orchestration code may never call `datetime.now()`,
`random()`, or the network directly. Time and randomness are **ports**, injected and recorded.
This is why `application/ports/clock.py` exists.

The nearest OS relatives are record-replay debuggers (`rr`) and deterministic simulation testing
(FoundationDB) — not the kernel itself. This is the one place where agent infrastructure needs a
mechanism the classical OS never required, because a CPU instruction is deterministic and a model
call is not.

---

## 6 · Scheduling

Finite workers, many runs. The tradeoff space is unchanged from a kernel scheduler:

| Policy | Failure mode |
| --- | --- |
| FIFO | A ten-minute run blocks a five-second run behind it |
| Strict priority | **Starvation** — low-priority runs may never execute |
| Priority + **aging** | Priority rises with waiting time — the classical fix |
| Weighted fair queueing per tenant | One tenant cannot monopolise the pool |

One difference in the constants: an OS time-slices in milliseconds and preempts freely. Agent runs
are seconds to minutes and **cannot be preempted mid-tool-call** — a tool may already have written
to an external system. So scheduling is *cooperative at step boundaries*, closer to early
cooperative multitasking than to modern preemption.

---

## 7 · Memory hierarchy and paging

The context window is RAM: fast, scarce, and far smaller than the data you'd like resident.

```
L1  Redis          hot     microseconds
L2  Postgres       warm    milliseconds
L3  Object store   cold    100ms+
```

Two movement mechanisms, and both exist in an OS:

- **Anticipatory (prefetch)** — promote records by access frequency and recency, *before* they're
  needed. This is tier promotion policy.
- **Demand (page fault)** — a run needs context that isn't resident, so the miss raises a fault: a
  handler searches L2/L3, retrieves the page, reinjects it, and execution continues.

**Compaction is page-out**: summarise old turns, keep a pointer to the full history. And it runs
on a *background worker* at a watermark, not on the execution thread — the same reason an OS
writes dirty pages out proactively instead of stalling on every fault.

Eviction policy is eviction policy: relevance × recency, an LRU/LFU descendant.

---

## 8 · The tool boundary is a system call

A system call is the controlled path from unprivileged code to privileged operations. The kernel
validates arguments, checks permissions, and performs the operation on the caller's behalf —
the caller never touches the hardware directly.

The tool boundary is identical:

| System call | Tool call |
| --- | --- |
| Call number + arguments | Tool name + JSON-Schema-validated arguments |
| Argument validation | Schema validation both directions |
| Permission check (uid, capabilities) | Capability set, checked before dispatch |
| Kernel performs the operation | Runtime performs it; the agent never holds credentials |
| Return value or `errno` | Result or a classified error (`retryable` / `terminal` / `needs-human`) |

**Protection rings** map onto isolation tiers: in-process → subprocess → ephemeral container →
gVisor → MicroVM. And **capabilities are bearer tokens with a TTL**, not static ACL entries —
closer to capability-based security systems than to Unix permission bits.

The genuinely harder problem: an OS can trust that the *program* meant to make that syscall. The
runtime cannot — a prompt-injected agent may be acting on an attacker's instruction. That is why
Phase 14 exists.

---

## 9 · Failure detection: leases and fencing

A worker claims a run and then loses power. Nothing is written. The status says `running` forever,
because the thing that would update it is the thing that died.

The answer is a **lease**: a claim with an expiry, extended by heartbeats. A missed heartbeat makes
the run reclaimable. You've seen this in DHCP leases and Kubernetes `Lease` objects.

The subtle failure: worker-7 wasn't dead, only paused by a long GC. Its lease expires, worker-9
claims the run, then worker-7 wakes still believing it owns it — **split brain**.

The fix is a **fencing token**: each lease acquisition increments a monotonic counter, every write
carries the token, and the store rejects any write bearing a stale one. This is why a TTL-based
distributed lock alone is unsafe, and it's the reason ADR-0003's design uses leases with fencing
rather than Redlock.

---

## 10 · Where the analogy breaks

Intellectual honesty matters more than a tidy metaphor. Four real differences:

| | Operating system | Agent runtime |
| --- | --- | --- |
| **Addressing** | Exact — the MMU knows page `0x4A2` is absent | **Semantic** — absence must be inferred; retrieval is similarity-based |
| **Hardware support** | MMU, TLB, page tables in silicon | **None** — fault detection, handling, and the page table are application code |
| **Miss cost** | Microseconds to milliseconds; latency only | 100ms–seconds, **and money** (vector search + tokens) |
| **Failure mode** | Transparent — the program cannot tell it was paged | **Not transparent** — the wrong page yields a confidently wrong answer |

The last row is the significant one. **OS paging is correctness-preserving; agent paging is
quality-affecting.** There is no equivalent of "the page simply loaded correctly" — a retrieval
that returns plausible-but-wrong context produces a plausible-but-wrong answer, silently.

Determinism is the other break: a CPU instruction is deterministic, so an OS never needed a
determinism boundary. The runtime does.

---

## 11 · How this document grows

The sections above are the conceptual mapping, and they are complete. What arrives later is the
**implementation-grounded detail** — written when the corresponding component exists, so the
explanation is anchored to real code rather than to intention:

| Addition | Phase |
| --- | --- |
| Scheduler measurements: starvation under mixed load, aging parameters | 3 |
| Event schema, snapshot cadence, replay determinism rules in practice | 3 |
| Lease timing: heartbeat interval vs TTL, observed reclaim latency | 3 |
| Isolation-tier benchmark: container spin-up cost per tool call | 4 |
| Page-fault rate and cost, measured against the tiering policy | 5 |
| Handoff context-filtering: what a sub-agent actually receives | 6 |

**Related:** [`../architecture/concepts/`](../architecture/) holds the per-mechanism deep dives;
this document is the map that connects them to what you already know.
