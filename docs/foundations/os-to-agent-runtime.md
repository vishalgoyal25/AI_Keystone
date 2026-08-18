# Operating Systems → The Agent Runtime

> The governing analogy of AI_Keystone: **if the LLM is the CPU, the runtime is the operating
> system.** This document is written alongside the runtime core (Phases 3–6); this stub records
> the mapping and the sections to be filled as each component is built.

## The claim

An LLM can reason but cannot schedule its own work, survive a crash, hold state across minutes,
call the outside world safely, or explain what it did. Those are the exact responsibilities an OS
took on for programs. The runtime is that OS, one layer up.

## The mapping

| Operating system | Agent runtime | Built in |
| --- | --- | --- |
| Process scheduler | Run scheduling — priority, aging, fairness | Ph 3 |
| Process control block | Run state — externalised, checkpointed | Ph 3 |
| Write-ahead log & recovery | Event log; state = fold(events); replay recovery | Ph 3 |
| Context switch | Checkpoint out, resume on another worker | Ph 3 |
| System call interface | Tool boundary — the controlled path outward | Ph 4 |
| Protection rings / privilege | Capability model, credential brokering, sandboxing | Ph 4 |
| Memory hierarchy | Working/episodic/semantic memory across L1–L3 tiers | Ph 5 |
| Virtual memory / paging | Context compaction — summarise out, page relevant history in | Ph 5 |
| Inter-process communication | Agent-to-agent messaging, handoff, delegation | Ph 6 |
| Interrupt / fault handling | Timeouts, cancellation, tool failure, compensation | Ph 3–4 |
| cgroups / resource limits | Per-tenant quotas, token budgets, concurrency caps | Ph 7, 14 |
| Debugger / `strace` | Trajectory tracing, deterministic replay, time-travel debug | Ph 11 |

Diagram source: [`../architecture/diagrams/os-to-runtime-mapping.mmd`](../architecture/diagrams/os-to-runtime-mapping.mmd).

## Sections to be written (with their phases)

- **Scheduling** — priority, aging, starvation, preemption vs cooperative yielding *(Ph 3)*
- **The process control block** — what run state must contain to be resumable *(Ph 3)*
- **Write-ahead logging** — why event sourcing is the WAL, applied to agents *(Ph 3)*
- **System calls & protection** — the tool boundary as a privilege boundary *(Ph 4)*
- **Memory hierarchy & paging** — context budgeting as page replacement *(Ph 5)*
- **IPC** — handoff and messaging as inter-process communication *(Ph 6)*
- **Fault handling** — leases/fencing as failure detection; the split-brain problem *(Ph 3)*

> Each section is filled when its component is built, so the explanation is grounded in real code
> rather than written ahead of it.
