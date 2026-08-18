# AI_Keystone — Development Roadmap

**18 phases (0–17) · ~35 weeks · solo · CPU-only**

> **Living document.** The phase *structure* is fixed; contents and ordering are revised only
> through a new ADR, so that deviation is recorded as engineering evolution rather than hidden.
> Each phase ends with exit criteria that must be **fully** met before the next begins.

---

## How to read this

Every phase declares:

| Field | Meaning |
| --- | --- |
| **Goal** | The single capability the phase delivers |
| **Why here** | What it unlocks, and what it depends on |
| **Sub-phases** | Ordered units of work, each with the files it touches |
| **Concepts** | Named industry/research terms landed |
| **Anchor** | The CS fundamental it maps onto |
| **Study** | Primary sources — official docs, papers, source code |
| **Exit criteria** | Checklist; all must be true to proceed |
| **Proof** | The artifact that demonstrates it worked |

⭐ marks the runtime core — the deepest treatment.

---

## Standing deliverables — every phase, without exception

Sub-phase file lists below name only what is **specific** to that phase. The following are
produced by **every** phase and are not repeated each time. A phase is not complete until all
eight exist.

| # | Deliverable | Location |
| --- | --- | --- |
| 1 | **Phase README** with exit criteria, written *before* the phase starts | `docs/phases/phase-NN-slug/README.md` |
| 2 | **Design doc** — worked out before building | `docs/phases/phase-NN-slug/design.md` |
| 3 | **Write-up** — what was built, what was proven, with measurements | `docs/phases/phase-NN-slug/writeup.md` |
| 4 | **Evidence** — charts, screenshots, recordings referenced by the write-up | `docs/phases/phase-NN-slug/evidence/` |
| 5 | **ADRs** for every significant decision made during the phase | `docs/adr/NNNN-*.md` + index row |
| 6 | **One diagram** — the phase's most explanatory visual, Mermaid source + SVG export | `docs/architecture/diagrams/` |
| 7 | **Status updates** — phase board, ADR index, roadmap status | `docs/phases/README.md`, `docs/adr/README.md` |
| 8 | **Session log entries** throughout; final entry closes the phase | `private/planning/session-log.md` |

**Documentation timing:** produced in one concentrated pass at phase end, not interleaved
continuously. Interleaving destroys build flow and produces worse writing.

**The per-phase diagram** (deliverable 6) is the highest-reach artifact the project produces —
a good architecture diagram is shared far more widely than a good ADR is read. Planned subjects:

| Phase | Diagram |
| --- | --- |
| 0 | OS concepts ↔ agent runtime mapping |
| 1 | Hexagonal layers with the dependency rule |
| 2 | C4 container view of the walking skeleton |
| 3 | Run state machine · record-vs-replay across the determinism boundary |
| 4 | Tool call lifecycle with compensation on failure |
| 5 | Memory type × storage tier matrix, with paging flow |
| 6 | The five topologies, side by side |
| 7 | Gateway with circuit-breaker states and the token bucket |
| 8 | Ingestion pipeline and retrieval path |
| 9 | Candidate generation → feature store → ranker |
| 10 | Eval pyramid: component → trajectory → gates |
| 11 | Trace hierarchy and the replay mechanism |
| 12 | Event cascade with backpressure points |
| 13 | Cross-system saga with real external services |
| 14 | Tenant isolation boundaries |
| 15 | Kubernetes topology with probes and resource limits |
| 16 | AWS deployment topology |

---

## Track map

```
T1 FOUNDATION        Ph 0–1     architecture, patterns, CI
T2 SKELETON          Ph 2       thin end-to-end slice + pain log
T3 RUNTIME CORE ⭐    Ph 3–6     agent infrastructure proper
T4 SUPPORTING        Ph 7–9     model plane, data plane, ML
T5 QUALITY & OPS     Ph 10–12   evals, observability, event backbone
T6 PLATFORM & CLOUD  Ph 13–16   integration, tenancy, containers, AWS
T7 OPERATE           Ph 17      run it, write about it
```

**Dependency chains** — hard: `1→2`, `3→4→5→6`, `3→11`, `4→13`, `8→9`, `12→14`, `15→16`.
Reorderable: 7, 9, 12.

**Depth weighting**

```
Agent runtime          ████████████████   Ph 3
Tools & memory         ████████████       Ph 4–5
Orchestration          ██████████         Ph 6
Platform & cloud       █████████          Ph 15–16
Model plane            ███████            Ph 7
Eval & observability   ███████            Ph 10–11
ML / MLOps             ██████             Ph 9
Data plane             ████               Ph 8
```

---
---

# T1 — FOUNDATION

## Phase 0 · Foundations & Decisions

**Goal** — Establish that no decision in this project goes unrecorded, and that the environment
is reproducible, before any application code exists.

**Why here** — Documentation discipline cannot be retrofitted honestly; backfilled ADRs read as
backfilled. Cost guardrails must exist before any cloud resource can be created.

**Duration** — ~1 week

### 0.1 Repo foundation & rulebook
- Private operating manual; ignore rules covering environments, secrets, IaC state, data,
  models, observability volumes, and private work.
- Files: `CLAUDE.md` *(private)*, `.gitignore`, `README.md`

### 0.2 Documentation spine
- Reader-routing index (routes by audience, not a table of contents); this roadmap; the complete
  future repository tree annotated with what belongs where, marked `(Phase N)` for directories
  that do not yet exist; the C4 Level-1 context diagram (system, users, external dependencies);
  and the live phase status board.
- Files: `docs/README.md`, `docs/roadmap.md`, `docs/architecture/repository-structure.md`,
  `docs/architecture/c4/context.md`, `docs/architecture/diagrams/os-to-runtime-mapping.mmd`,
  `docs/phases/README.md`, `docs/phases/phase-00-foundations/README.md`

### 0.3 Decision practice
- ADR template (Context → Decision → Status → Consequences), index table with status column,
  and the six decisions genuinely already made.
- Files: `docs/adr/README.md`, `docs/adr/template.md`,
  `docs/adr/0001-python-as-primary-language.md`,
  `docs/adr/0002-hexagonal-architecture.md`,
  `docs/adr/0003-build-runtime-not-adopt-temporal.md`,
  `docs/adr/0004-postgres-pgvector-primary-store.md`,
  `docs/adr/0005-aws-with-hard-cost-ceiling.md`,
  `docs/adr/0006-ecs-fargate-over-eks.md`

### 0.4 Foundations mapping
- The operating-systems → agent-runtime concept mapping, written as a teaching document.
  This is the project's most distinctive early artifact.
- Files: `docs/foundations/README.md`, `docs/foundations/os-to-agent-runtime.md`

### 0.5 Collaboration setup
- Contribution policy stated honestly (issues and critique welcome; core-runtime PRs declined
  until Phase 8, because building them is the point). PR and issue templates.
- Files: `CONTRIBUTING.md`, `LICENSE`, `.github/PULL_REQUEST_TEMPLATE.md`,
  `.github/ISSUE_TEMPLATE/task.md`

### 0.6 Environment readiness
- Dependency groups (core/dev/test/ml/docs), the single command entry point, CI skeleton,
  and every environment variable documented with obviously-fake placeholders.
- Files: `pyproject.toml`, `Makefile`, `.env.example`, `.github/workflows/ci.yml`

### 0.7 Cloud guardrails
- AWS account, IAM user for daily work, **hard budget cap and billing alarms configured before
  any resource is created**. Commands pasted for manual execution.
- Files: none tracked (account configuration)

### 0.8 Private planning
- Session log (did / next / blocked) and career strategy, kept out of the public record.
- Files: `private/planning/session-log.md`, `private/planning/strategy.md`

**Concepts** — ADR practice, C4 modelling, documentation-as-deliverable, cost guardrails,
public/private separation.

**Study** — Nygard on ADRs; Simon Brown's C4 model; arc42.

**Exit criteria**
- [ ] A stranger reading `docs/` understands what is being built and why, with zero code present
- [ ] Six ADRs written, each naming alternatives considered and why they lost
- [ ] `docs/architecture/repository-structure.md` defines the home of every future file type,
      and every `(Ph N)` marker in it maps to an assigned sub-phase in this roadmap
- [ ] C4 context diagram renders, and the OS↔runtime mapping diagram is exported
- [ ] `docs/phases/README.md` status board exists and reflects reality
- [ ] AWS budget alarm confirmed active (screenshot in evidence/)
- [ ] CI runs green on lint, formatting, and markdown/link checks (no package exists yet)
- [ ] `.gitignore` verified to exclude `CLAUDE.md` and `private/` (`git check-ignore -v`)
- [ ] `.env.example` documents every variable with obviously-fake placeholders

**Proof** — The repository is legible and disciplined before it is functional.

---

## Phase 1 · Architecture Skeleton

**Goal** — A codebase whose *shape* is the first thing a reviewer notices, with the dependency
rule enforced mechanically.

**Why here** — Every later phase drops components into this structure. Correct boundaries now
mean Phases 3–16 have an obvious home; incorrect ones mean a painful refactor at Phase 8.

**Duration** — ~1.5 weeks

### 1.1 Package layout
- Four layers created with real (not placeholder) contents; `src` layout so tests exercise the
  installed package.
- Files: `src/keystone/{domain,application,infrastructure,interfaces}/`, `pyproject.toml`

### 1.2 Dependency rule in CI
- `import-linter` contract: `domain` imports nothing internal; `application` imports `domain`
  only; reverse imports fail the build.
- Files: `.importlinter`, `tests/architecture/test_import_rules.py`, `.github/workflows/ci.yml`

### 1.3 Domain primitives
- Pure entities and value objects with invariants enforced in constructors. No I/O, no framework.
- Files: `src/keystone/domain/shared/`, `src/keystone/domain/run/entities.py`

### 1.4 Ports
- The interface set the application layer depends on — including `ClockPort` and `RandomPort`,
  because Phase 3's determinism boundary requires time and randomness to be injectable.
- Files: `src/keystone/application/ports/{run_store,model,tool_registry,memory_store,retrieval,event_bus,clock}.py`

### 1.5 SOLID demonstrations
- Each principle shown as a real violation and its fix, each with an ADR:
  SRP (orchestration vs persistence), OCP (adding a provider without editing the router),
  LSP (a provider that cannot stream), ISP (a fat `Tool` interface split by capability),
  DIP (application depends on `ModelPort`, never a concrete client).
- Files: `docs/adr/0007-…` through `0011-…`, plus the affected source modules

### 1.6 Design patterns where warranted
- Strategy (routing), Adapter (providers), Repository (persistence), Factory (agent
  construction), Decorator (middleware chain), Observer (event bus). Applied only where they are
  the honest solution.
- Files: across `application/` and `infrastructure/`

### 1.7 Data-structure primitives
- Built here, consumed later: priority queue with aging (→ Phase 3 scheduler), LRU and LFU
  caches benchmarked against each other (→ Phase 5, 7), token bucket and leaky bucket
  (→ Phase 7, 14), consistent hash ring (→ Phase 14), Bloom filter (→ Phase 8 dedup).
- Files: `src/keystone/domain/shared/structures/`, `tests/unit/domain/structures/`

### 1.8 Test harness
- Unit (no I/O), contract (every adapter must satisfy its port), architecture (fitness
  functions), property-based tests on the primitives.
- Files: `tests/{unit,contract,architecture}/`, `tests/conftest.py`

### 1.9 Quality gates & release hygiene
- ruff, mypy strict, pre-commit, coverage; CI green from the first commit. Changelog started now
  so it is generated from Conventional Commits rather than reconstructed later.
- Files: `.pre-commit-config.yaml`, `pyproject.toml`, `.github/workflows/ci.yml`, `CHANGELOG.md`

**Concepts** — Hexagonal architecture, dependency inversion, SOLID, GoF patterns, fitness
functions, property-based testing, contract testing.

**Anchor** — Data structures and algorithms made load-bearing rather than interview trivia.

**Study** — *Cosmic Python* (cosmicpython.com); `import-linter` docs; Hypothesis.

**Exit criteria**
- [ ] A PR that makes `domain` import `infrastructure` **fails CI**
- [ ] All five SOLID principles demonstrated in code with an ADR each
- [ ] Five data-structure primitives implemented, property-tested, benchmarked
- [ ] Contract-test harness exists and at least one port has a contract suite
- [ ] mypy strict passes with no ignores in `domain/` or `application/`
- [ ] CI green

**Proof** — Screenshot of CI rejecting a dependency-rule violation.

---
---

# T2 — SKELETON

## Phase 2 · Walking Skeleton

**Goal** — One thin, ugly, working path through every layer, and a written record of everything
that hurt.

**Why here** — This is the pivot of the plan. The whole system shape must be visible early so
that every later deepening is motivated by observed pain rather than a checklist.

**Duration** — ~2 weeks

### 2.1 Local infrastructure
- Postgres 17 + pgvector, Redis, MinIO (local S3-compatible object store, so the L3 code path is
  identical to AWS later).
- Files: `docker-compose.yml`, `infra/local/`, `scripts/dev/setup.ps1`, `data/README.md`
  (what belongs in each data directory and how to fetch it — the directory itself is gitignored)

### 2.2 Minimal persistence
- Schema and migrations for runs and documents. Simplest workable model — mutable state, to be
  replaced by the event log in Phase 3.
- Files: `src/keystone/infrastructure/persistence/postgres/`, `.../migrations/`

### 2.3 Minimal model access
- One provider adapter behind `ModelPort`. Direct calls, no routing, no caching.
- Files: `src/keystone/infrastructure/models/`, `src/keystone/application/ports/model.py`

### 2.4 Minimal retrieval
- ~1,000 documents loaded by a script, fixed-size chunking, one embedding model, pgvector with
  default settings.
- Files: `scripts/data/load_sample.py`, `src/keystone/infrastructure/retrieval/pgvector.py`

### 2.5 Minimal agent loop
- A plain `while` loop, one tool (search), no durability, no memory.
- Files: `src/keystone/application/runtime/executor.py`, `src/keystone/infrastructure/tools/search.py`

### 2.6 HTTP interface
- One endpoint, SSE token streaming, request/response schemas. OpenAPI spec generated from the
  code — never hand-written, so it cannot go stale.
- Files: `src/keystone/interfaces/http/`, `tests/e2e/`, `docs/api/`, `scripts/dev/export_openapi.py`

### 2.7 Thin UI
- Input box, streamed output, nothing else.
- Files: `web/app/`, `web/components/`, `web/package.json`

### 2.8 Pain log ← **the real deliverable**
- A written list of everything that broke or frustrated: lost state on interrupt, infinite loops,
  no visibility into tool choice, context overflow, one bad provider response killing a request.
- Files: `docs/phases/phase-02-walking-skeleton/pain-log.md`

**Concepts** — Walking skeleton / tracer bullet, integration-first design, vertical slicing.

**Exit criteria**
- [ ] A question typed in the UI returns a streamed, retrieval-grounded answer end to end
- [ ] Entire stack starts from one command
- [ ] Pain log contains at least ten specific, dated observations
- [ ] Each pain item is mapped to the phase that will close it

**Proof** — A recorded end-to-end demo, and the pain log. Every phase from here closes a line
item on it, which is what keeps later work non-speculative.

---
---

# T3 — RUNTIME CORE ⭐

## Phase 3 · Agent Execution Runtime ⭐

**Goal** — An agent run becomes a durable, replayable, schedulable unit of work that survives
the death of the process executing it.

**Why here** — The hardest and highest-value component in the system. Everything above depends
on its guarantees, and Phases 6 and 11 become nearly free because of it.

**Duration** — ~3 weeks

### 3.1 Run as a persisted entity
- `Run` with identity, tenant, status, current step, consumed budgets, lease fields. State
  transitions defined as an explicit finite state machine with enumerable, validated edges.
- Files: `src/keystone/domain/run/{entities,state_machine,errors}.py`,
  `src/keystone/application/ports/run_store.py`

### 3.2 Event-sourced execution log
- Append-only `RunEvent` ordered by sequence; current state is a fold over events; periodic
  snapshots to bound fold cost. Append is one transaction — no half-written state.
- Files: `src/keystone/domain/run/events.py`,
  `src/keystone/infrastructure/persistence/postgres/event_store.py`, `.../migrations/`,
  `docs/foundations/dbms-to-state-management.md` (WAL, atomic commit, recovery-by-replay →
  event sourcing)

### 3.3 Determinism boundary ← **the central idea**
- Split orchestration (deterministic, replayable) from effects (model calls, tool calls, clock,
  randomness). Effects execute once and are recorded; on replay they are served from the log
  rather than re-executed. Orchestration must therefore never call `datetime.now()`,
  `random()`, or the network directly.
- Files: `src/keystone/application/runtime/effects.py`, `.../replay_cursor.py`,
  `src/keystone/infrastructure/{clock,random}.py`,
  `docs/architecture/concepts/determinism-boundary.md`

### 3.4 Checkpoint & crash-resume
- Atomic checkpoint after every step; a new worker rebuilds state by replaying the log and
  continues live from the last recorded event.
- Files: `src/keystone/application/runtime/executor.py`,
  `src/keystone/application/use_cases/resume_run.py`

### 3.5 Lease, heartbeat, fencing
- Workers claim runs with an expiring lease and heartbeat to extend it. A missed heartbeat makes
  the run reclaimable. **Monotonic fencing tokens** cause the store to reject writes from a
  worker whose lease has expired — the failure mode that TTL-only locking cannot handle.
- Files: `src/keystone/application/runtime/lease.py`,
  `src/keystone/infrastructure/persistence/postgres/lease_store.py`,
  `docs/architecture/concepts/lease-and-fencing.md`, `docs/adr/00xx-lease-fencing-over-redlock.md`

### 3.6 Scheduler
- Priority queue with aging (the Phase 1 primitive, now in use), per-tenant concurrency caps,
  global caps protecting downstream services.
- Files: `src/keystone/application/runtime/scheduler.py`

### 3.7 Budgets & deadline propagation
- Wall-clock, token, and cost ceilings at both step and run level; remaining deadline propagates
  down the call tree rather than resetting per step.
- Files: `src/keystone/application/runtime/budgets.py`

### 3.8 Cancellation
- Cooperative cancellation checked at safe points between steps, with cleanup hooks — a worker
  cannot be safely killed mid-tool-call because it may already have written externally.
- Files: `src/keystone/application/runtime/cancellation.py`

### 3.9 Failure handling
- Error taxonomy (`retryable` / `terminal` / `needs-human`), exponential backoff **with jitter**
  to prevent thundering herd, max attempts, poison-run quarantine to a dead-letter path.
- Files: `src/keystone/application/runtime/retry.py`, `src/keystone/domain/run/errors.py`

### 3.10 Worker entrypoint
- The deployable worker process, with graceful shutdown draining in-flight runs.
- Files: `src/keystone/interfaces/worker/`

**Concepts** — Durable execution, event sourcing, deterministic replay, lease-based failure
detection, fencing tokens, cooperative cancellation, deadline propagation, poison-message
handling, jittered backoff.

**Anchor** — OS: process control block, scheduler, preemption, fault handling.
DBMS: write-ahead logging, atomic commit. TOC: the run is an explicit finite state machine.

**Study** — Temporal's durable-execution and workflow-determinism documentation; AWS Step
Functions execution semantics; Kleppmann, *How to do distributed locking*; Fowler on Event
Sourcing; Kubernetes `Lease`; Mozilla `rr`.

**Exit criteria**
- [ ] `kill -9` on a worker mid-run; the run resumes on another worker and completes correctly
- [ ] A completed run replays to a **byte-identical** trajectory
- [ ] An expired lease is reclaimed within the configured window
- [ ] A stale fencing token is rejected by the store
- [ ] Cancellation completes cleanly with cleanup hooks executed
- [ ] Budget exhaustion terminates a run and records the reason
- [ ] Scheduler demonstrates no starvation under mixed priority load
- [ ] Concept doc + three ADRs written

**Proof** — Two recordings: crash-and-resume, and identical replay of a historical run.

---

## Phase 4 · Tool Platform ⭐

**Goal** — Give a non-deterministic process controlled, revocable, auditable access to the real
world.

**Why here** — Steps are now durable; a step with external side effects is where agentic systems
actually break. This is the syscall boundary.

**Duration** — ~2.5 weeks

### 4.1 Tool descriptor & registry
- Name, version, JSON Schema for input and output, **side-effect class**
  (`read` / `write` / `destructive`), cost estimate, timeout, required capabilities.
- Files: `src/keystone/domain/tool/`, `src/keystone/application/tools/registry.py`,
  `src/keystone/application/ports/tool_registry.py`

### 4.2 Schema contracts & validation
- Validate both directions; malformed model output enters a bounded repair loop, then hard-fails
  rather than passing garbage downstream.
- Files: `src/keystone/application/tools/validation.py`

### 4.3 Capability & permission model
- Agents carry a capability set; every call is checked before dispatch. Denials are logged, not
  silently dropped — repeated denied attempts are a signal.
- Files: `src/keystone/domain/agent/capabilities.py`, `src/keystone/application/tools/permissions.py`

### 4.4 Credential brokering
- The agent holds a reference, never a secret. The broker resolves it at call time, scoped to
  the tenant, short-lived. Credentials never enter model context, logs, or traces.
- Files: `src/keystone/application/tools/credential_broker.py`,
  `src/keystone/infrastructure/tools/secrets.py`,
  `docs/architecture/concepts/tool-capability-model.md`

### 4.5 Sandboxing & the isolation spectrum
- Ephemeral container per code-execution call, destroyed after; network egress denied by
  default; CPU, memory, and wall-clock ceilings. An ADR documents the full spectrum
  (in-process → subprocess → **ephemeral container** → gVisor → MicroVM) and why the chosen
  tier is right for this system and what would change that.
- Files: `src/keystone/infrastructure/tools/sandbox.py`, `infra/docker/sandbox.Dockerfile`,
  `docs/adr/00xx-tool-isolation-level.md`

### 4.6 Idempotency
- Idempotency keys on all write tools so retries are safe.
- Files: `src/keystone/application/tools/idempotency.py`

### 4.7 Compensation & saga coordination
- Every write tool declares its undo operation; on downstream failure the coordinator executes
  compensations in reverse order.
- Files: `src/keystone/application/tools/compensation.py`, `.../saga.py`

### 4.8 Error taxonomy & rate limits
- Tool-level classification feeding the Phase 3 retry policy; per-tool, per-tenant limits using
  the Phase 1 token bucket.
- Files: `src/keystone/application/tools/errors.py`, `.../limits.py`

**Concepts** — Capability-based security, syscall boundary design, credential brokering, saga
pattern, compensating transactions, idempotency, sandboxing, error taxonomy.

**Anchor** — OS: system calls, protection rings, privilege separation, resource limits.
DBMS: compensation where true ACID is unavailable.

**Study** — MCP specification; Anthropic tool-use documentation; Garcia-Molina & Salem, *Sagas*;
capability-security literature.

**Exit criteria**
- [ ] An agent updates system A, B fails, and compensation cleanly unwinds A
- [ ] The audit log shows attempt → failure → compensation → final state
- [ ] A tool called outside the agent's capability set is denied and the denial is traced
- [ ] Sandboxed code cannot reach the network or exceed its resource ceiling
- [ ] Retrying a write tool with the same idempotency key produces no duplicate effect
- [ ] Isolation-level ADR written with the spectrum and the decision

**Proof** — Recording of a partial failure being compensated, with the audit trail.

---

## Phase 5 · Memory & Context Architecture ⭐

**Goal** — Memory that outlives the context window, and a context window managed as a scarce,
budgeted resource.

**Why here** — Runs are durable and tools are safe; now runs get long. Everything here is a
memory-hierarchy problem.

**Duration** — ~2.5 weeks

### 5.1 Memory types
- Working (current run), episodic (past runs and interactions), semantic (distilled facts),
  procedural (tool-usage patterns that worked).
- Files: `src/keystone/domain/memory/`, `src/keystone/application/ports/memory_store.py`

### 5.2 Storage tiers
- Orthogonal to type: **L1 Redis** (hot, microseconds) → **L2 Postgres/pgvector** (warm,
  milliseconds) → **L3 MinIO/S3** (cold, archived). MinIO locally means the S3 code path is
  identical in AWS.
- Files: `src/keystone/infrastructure/persistence/{redis,postgres,objectstore}/`,
  `docs/architecture/concepts/memory-tiers.md`

### 5.3 Promotion & demotion
- Access-frequency and recency driven movement between tiers.
- Files: `src/keystone/application/memory/tiering.py`

### 5.4 Write policy
- What is worth remembering, and when it is written (immediately vs on run completion).
- Files: `src/keystone/application/memory/write_policy.py`

### 5.5 Consolidation
- Background distillation of episodic → semantic. This is where memory quality is won.
- Files: `src/keystone/application/memory/consolidation.py`

### 5.6 Decay & eviction
- Relevance × recency scoring; eviction when a tier exceeds budget.
- Files: `src/keystone/application/memory/decay.py`

### 5.7 Context budgeter
- Token accounting across system prompt, tools, memory, retrieved documents, and history, with
  an explicit priority order for what gets dropped first.
- Files: `src/keystone/application/memory/context_budget.py`,
  `docs/architecture/concepts/context-budgeting.md`

### 5.8 Asynchronous compaction
- A watermark (~75% of budget) triggers **background** summarization; the run continues on
  current context and the compacted version is swapped in at the next step boundary. Blocking
  the execution thread to summarize would stall every agent.
- Files: `src/keystone/application/memory/compaction.py`, `src/keystone/interfaces/worker/`

### 5.9 Position-aware assembly
- Ordering and deduplication of injected context, accounting for uneven attention across long
  contexts.
- Files: `src/keystone/application/memory/assembly.py`

### 5.10 Concurrent-write conflict resolution
- Optimistic concurrency with version columns; conflict policy when two runs write the same
  memory record.
- Files: `src/keystone/infrastructure/persistence/postgres/memory_store.py`

### 5.11 Tenant isolation
- Memory partitioned per tenant at the storage layer, enforced rather than assumed.
- Files: `src/keystone/application/memory/isolation.py`

**Concepts** — Memory hierarchy, eviction policy, working set, compaction, consolidation,
relevance scoring, optimistic concurrency control, context engineering.

**Anchor** — OS: paging, page replacement, working-set model, prefetching.
Computer architecture: cache tiering. DBMS: lost-update anomaly, MVCC.

**Study** — MemGPT (context as virtual memory); *Lost in the Middle*; Anthropic context
engineering guidance.

**Exit criteria**
- [ ] A 200-turn conversation never exceeds the context limit and still recalls a turn-3 fact
- [ ] Recall accuracy, token cost, and latency **measured** against naive truncation
- [ ] Compaction demonstrably does not block the execution thread
- [ ] Records demonstrably move L1 → L2 → L3 under the tiering policy
- [ ] Two concurrent writes to one memory record resolve without lost updates
- [ ] Cross-tenant memory access is impossible by construction

**Proof** — Benchmark notebook: recall and cost curves, tiered vs truncation.

---

## Phase 6 · Orchestration & Protocols ⭐

**Goal** — Many agents coordinating, with no lost state and no runaway loops.

**Why here** — Single runs are durable, safe, and memory-managed. Multi-agent is the composition
layer — a graph and compiler problem, not a prompting problem.

**Duration** — ~2.5 weeks

### 6.1 Workflow graph as data
- Nodes, edges, and conditional transitions as an intermediate representation that can be
  validated, versioned, diffed, and visualized — not as imperative code.
- Files: `src/keystone/domain/orchestration/graph.py`,
  `src/keystone/application/orchestration/ir.py`,
  `docs/foundations/compilers-to-orchestration.md` (AST/IR, static analysis, graph validation →
  the workflow engine)

### 6.2 Static validation
- Cycle detection, unreachable-node detection, type compatibility across edges — before
  execution, not during.
- Files: `src/keystone/application/orchestration/validation.py`

### 6.3 Topologies
- Sequential; supervisor/router; parallel fan-out with join and a partial-failure policy;
  critic/reflection loop with bounded iterations; hierarchical delegation with depth limits.
- Files: `src/keystone/application/orchestration/topologies/`

### 6.4 Loop safety
- Maximum depth, maximum steps, **loop budgets** in tokens and cost, and progress detection that
  terminates a non-converging loop.
- Files: `src/keystone/application/orchestration/loop_guard.py`

### 6.5 Handoff protocol
- Explicit state transfer with **context filtering** — a sub-agent receives what it needs, not
  the parent's entire history. This is both a cost control and a security boundary.
- Files: `src/keystone/application/orchestration/handoff.py`

### 6.6 Human-in-the-loop
- A pause node suspending the run durably, awaiting external approval, with a timeout policy.
  Cheap only because Phase 3 made runs durable.
- Files: `src/keystone/application/orchestration/hitl.py`,
  `src/keystone/application/use_cases/approve_run.py`

### 6.7 MCP server
- Expose the tool platform to external clients over the Model Context Protocol.
- Files: `src/keystone/interfaces/mcp/`

### 6.8 Agent-to-agent messaging
- Typed envelopes over the message layer rather than direct in-process calls.
- Files: `src/keystone/application/orchestration/messaging.py`

### 6.9 Trajectory visualization
- Execution graph rendered with per-node latency and cost.
- Files: `src/keystone/interfaces/http/routers/trajectory.py`, `web/components/`

**Concepts** — Graph execution engines, IR design, static analysis, cycle detection, fan-out/join,
bounded recursion, context isolation on handoff, protocol design, MCP.

**Anchor** — Compiler design: the workflow graph is an AST/IR and validation is static analysis.
Algorithms: traversal, cycle detection, topological ordering. OS: process trees, IPC, fork/join.

**Study** — LangGraph source; MCP specification; Anthropic multi-agent engineering writing.

**Exit criteria**
- [ ] All five topologies execute correctly, including partial failure in fan-out
- [ ] An invalid graph is rejected by static validation before execution
- [ ] A deliberately recursive agent is terminated by the loop budget, not by a bill
- [ ] A run pauses for human approval, survives a worker restart, and resumes on approval
- [ ] An external MCP client can list and call tools
- [ ] Handoff demonstrably filters parent context

**Proof** — Trajectory graph of a supervisor with four parallel sub-agents and one critic pass,
annotated with timing and cost.

---
---

# T4 — SUPPORTING PLANES

## Phase 7 · Model Plane

**Goal** — Never call a provider SDK from business logic, and never be taken down by a provider.

**Why here** — The runtime has used a crude model port since Phase 2. It now becomes real, and
it is fast to build because the port already exists.

**Duration** — ~2.5 weeks

### 7.1 Provider adapters
- Anthropic, Groq, Cerebras, Bedrock, OpenAI-compatible — all behind one port, all passing one
  contract suite.
- Files: `src/keystone/infrastructure/models/`, `tests/contract/test_model_port_contract.py`,
  `docs/foundations/networks-to-model-plane.md` (load balancing, health checks, failover,
  backpressure → the gateway)

### 7.2 Unified streaming
- One streaming abstraction across providers with differing stream semantics.
- Files: `src/keystone/application/model/streaming.py`

### 7.3 Routing
- Written, defensible policy: small model for classification and routing, strong model for
  synthesis; cost, latency, and quality inputs.
- Files: `src/keystone/application/model/router.py`, `docs/adr/00xx-model-routing-policy.md`

### 7.4 Circuit breaker
- Per-provider closed → open → half-open, driven by observed error rates.
- Files: `src/keystone/application/model/circuit_breaker.py`

### 7.5 Fallback chains
- Ordered degradation across providers and models, invisible to the caller.
- Files: `src/keystone/application/model/fallback.py`

### 7.6 Semantic cache
- Embedding-similarity cache above a tuned threshold, with negative caching for known-bad
  queries.
- Files: `src/keystone/application/model/semantic_cache.py`

### 7.7 Token-weight estimation
- Estimate input tokens exactly and output tokens predictively **before dispatch**, because the
  limiter must know the cost before incurring it.
- Files: `src/keystone/application/model/token_estimator.py`

### 7.8 Token-aware rate limiting ← **distinct from request limiting**
- Providers limit on **tokens per minute**, not requests per second. The limiter is denominated
  in tokens, per provider and model, distributed via Redis with Lua for atomicity. When budget
  is exhausted, low-priority runs queue while interactive requests pass; backpressure signals
  upward so the Phase 3 scheduler slows admission rather than piling up. Observed 429s and
  provider rate-limit headers adjust the budget adaptively.
- Files: `src/keystone/application/model/rate_limiter.py`, `.../admission.py`,
  `src/keystone/infrastructure/messaging/redis_scripts/`,
  `docs/architecture/concepts/token-aware-rate-limiting.md`

### 7.9 Cost accounting
- Per-run, per-tenant, per-feature token and cost attribution with hard budget enforcement.
- Files: `src/keystone/application/model/accounting.py`

### 7.10 Structured output
- Schema-constrained generation with a bounded validate-and-repair loop.
- Files: `src/keystone/application/model/structured.py`

**Concepts** — Strategy/Adapter, circuit breaker, bulkhead isolation, semantic caching,
admission control with non-uniform cost, weighted fair queueing, backpressure, cost governance.

**Anchor** — CN: load balancing, health checking, failover. Queueing theory: Little's Law.
Computer architecture: cache hit economics.

**Study** — Fowler on Circuit Breaker; LiteLLM's provider abstraction; Bedrock Converse API.

**Exit criteria**
- [ ] Primary provider forced to fail; failover is invisible to the user
- [ ] Sustained load stays under the provider's TPM limit with **zero 429s**
- [ ] Low-priority work demonstrably queues while interactive work passes
- [ ] Semantic cache hit rate measured and charted
- [ ] Cost per query measured before and after routing
- [ ] All provider adapters pass one contract suite

**Proof** — Chaos recording of provider failover; cache-hit and cost-reduction charts.

---

## Phase 8 · Data Plane & Retrieval

**Goal** — Retrieval that is measured rather than assumed, on a pipeline architected to scale
later.

**Why here** — Retrieval quality dominates answer quality. Sized to what the AI layer needs
(~150k documents, one primary plus one supplementary source) with the seams for growth built in.

**Duration** — ~3 weeks

### 8.1 Source adapters
- Behind a port, so a distributed implementation is later a swap rather than a rewrite.
- Files: `src/keystone/infrastructure/ingest/`, `src/keystone/application/ports/source.py`

### 8.2 Incremental sync
- High-watermark cursors, resumable, never a full re-pull.
- Files: `src/keystone/application/ingest/sync.py`

### 8.3 Idempotent upsert
- Content-hash keyed; running twice produces zero duplicates.
- Files: `src/keystone/application/ingest/upsert.py`

### 8.4 Quality gates & DLQ
- Completeness, freshness, schema, distribution checks; failures to a dead-letter queue rather
  than into the index.
- Files: `src/keystone/application/ingest/quality.py`, `.../dlq.py`

### 8.5 Lineage
- Every record traceable to source, fetch time, and transform version.
- Files: `src/keystone/domain/retrieval/lineage.py`

### 8.6 Partitioning
- Decided at schema design; retrofitting a partition strategy on a live table is a migration
  nightmare.
- Files: `.../migrations/`, `docs/adr/00xx-partitioning-strategy.md`

### 8.7 Chunking comparison
- Fixed, recursive, semantic, and structural/section-aware, measured against a labelled set.
- Files: `src/keystone/application/retrieval/chunking/`, `evals/datasets/retrieval/`,
  `docs/foundations/algorithms-to-retrieval.md` (HNSW as a navigable small-world graph, BM25 as
  information theory, graph algorithms on the citation network)

### 8.8 Embedding pipeline
- Batched, checkpointed, resumable, queue-driven workers — scaling means adding workers.
- Files: `src/keystone/application/retrieval/embedding.py`, `scripts/data/embed.py`

### 8.9 Index selection
- HNSW vs IVFFlat measured on build time, memory, and recall — plus **quantization**
  (scalar and product quantization) as the memory/recall tradeoff axis.
- Files: `notebooks/benchmarks/index_comparison.ipynb`, `docs/adr/00xx-ann-index-selection.md`

### 8.10 Hybrid search
- BM25 + dense vectors + reciprocal rank fusion.
- Files: `src/keystone/infrastructure/retrieval/{bm25,hybrid}.py`

### 8.11 Reranking
- Cross-encoder reranking of the fused candidate set.
- Files: `src/keystone/infrastructure/retrieval/reranker.py`

### 8.12 Retrieval evaluation
- A labelled set of 300+ query→document pairs; Recall@k, NDCG@k, MRR across every configuration.
- Files: `evals/suites/retrieval_quality.py`, `evals/datasets/retrieval/`

### 8.13 Zero-downtime re-embedding
- Dual-write → shadow index → validate → cutover, for embedding-model upgrades.
- Files: `scripts/data/reindex.py`, `docs/architecture/concepts/zero-downtime-reindex.md`

### 8.14 Citation graph
- Co-citation, bibliographic coupling, PageRank for influence — the substrate for Phase 9.
- Files: `src/keystone/application/retrieval/graph.py`

**Concepts** — Incremental/CDC ingestion, idempotency, data quality gates, DLQ, lineage, ANN
indexing, quantization, hybrid retrieval, reranking, IR evaluation, blue-green data migration.

**Anchor** — DBMS: indexing, partitioning, query planning. Algorithms: HNSW as a navigable
small-world graph; BM25 as information theory; graph algorithms on the citation network.

**Study** — pgvector documentation; the HNSW paper; BM25 and Reciprocal Rank Fusion; RAGAS.

**Exit criteria**
- [ ] Pipeline run twice produces zero duplicates
- [ ] Killed mid-run, it resumes cleanly from the watermark
- [ ] A corrupted source record is caught by a quality gate and lands in the DLQ
- [ ] Retrieval quality chart across ≥4 chunking strategies × ≥3 index configurations
- [ ] Hybrid + rerank measurably beats dense-only on the labelled set
- [ ] Re-embedding completes with no read downtime
- [ ] Citation graph queries return within target latency

**Proof** — The retrieval-quality benchmark notebook. This chart alone outranks most AI
portfolios.

---

## Phase 9 · ML & MLOps

**Goal** — A real machine-learning system with honest offline evaluation, with no LLM involved.

**Why here** — The applied-science component, and what distinguishes an AI engineer from an
engineer who calls AI APIs. Requires the Phase 8 citation graph.

**Duration** — ~2.5 weeks

### 9.1 Candidate generation
- Embedding kNN plus graph signals (co-citation, bibliographic coupling).
- Files: `ml/features/candidates.py`

### 9.2 Feature engineering
- Content similarity, graph features (PageRank, co-citation strength, path distance), recency,
  popularity, user-history interactions.
- Files: `ml/features/`

### 9.3 Feature store pattern
- One feature definition serving both training and inference — the mechanism that prevents
  train/serve skew.
- Files: `ml/features/store.py`, `src/keystone/infrastructure/ml/features.py`

### 9.4 Ranker
- LightGBM LambdaMART; CPU-trainable, no GPU.
- Files: `ml/training/train_ranker.py`

### 9.5 Evaluation methodology
- **Temporal** train/test split to avoid leakage — the most common silent bug in recommender
  evaluation.
- Files: `ml/evaluation/splits.py`

### 9.6 Metrics
- NDCG@10, Recall@50, MRR, plus **coverage, intra-list diversity, novelty**, because a
  recommender optimizing accuracy alone degenerates.
- Files: `ml/evaluation/metrics.py`, `evals/reports/recsys_eval.ipynb`

### 9.7 Cold start
- Content-only fallback for new users and new documents.
- Files: `ml/serving/cold_start.py`

### 9.8 Registry & reproducibility
- Model versioning, model cards, fixed seeds, data-snapshot hashes.
- Files: `ml/registry/`, `ml/training/config/`

### 9.9 A/B framework
- Assignment, metric collection, and the statistics needed to read a result honestly.
- Files: `src/keystone/application/experiments/`

### 9.10 Ablation report
- Popularity baseline → content-only → +graph features → +learned ranker.
- Files: `evals/reports/recsys_ablation.ipynb`, `docs/phases/phase-09-ml/writeup.md`

**Concepts** — Learning-to-rank, candidate generation vs ranking, offline evaluation methodology,
temporal validation, train/serve skew, cold start, diversity/novelty tradeoffs, model registry.

**Anchor** — Probability and statistics; graph algorithms as ranking signal.

**Study** — Eugene Yan's recommender-systems writing; LightGBM ranking documentation.

**Exit criteria**
- [ ] Ablation table showing NDCG@10 lift at each stage
- [ ] No temporal leakage — verified explicitly
- [ ] Identical features served offline and online (skew test passes)
- [ ] Cold-start path measured separately
- [ ] Training reproducible from a config and a data snapshot hash
- [ ] Diversity/accuracy tradeoff curve produced

**Proof** — The evaluation report. This is the artifact that reads as *applied scientist*.

---
---

# T5 — QUALITY & OPERATIONS

## Phase 10 · Evaluation Harness

**Goal** — Prove that quality and performance do not regress — automatically, on every PR.

**Why here** — The system is now large enough that "did I break something?" is a real question,
and non-determinism means tests alone cannot answer it.

**Duration** — ~2 weeks

### 10.1 Golden datasets
- 300+ human-labelled examples across query types, versioned and hash-addressed.
- Files: `evals/datasets/{retrieval,generation,trajectory}/`

### 10.2 Generation evaluation
- Faithfulness, answer relevance, and **citation accuracy** — does the cited source actually
  support the claim.
- Files: `evals/suites/generation_quality.py`

### 10.3 Trajectory evaluation ← **the distinctive part**
- Score the path, not only the answer: tool-choice accuracy, ordering, step count versus optimal,
  and recovery from an injected tool failure.
- Files: `evals/suites/trajectory.py`,
  `docs/architecture/concepts/trajectory-evaluation.md`

### 10.4 Judge calibration
- Agreement with human labels measured (Cohen's κ), and documented biases: length preference,
  position bias, self-preference.
- Files: `evals/judges/`, `evals/reports/judge_calibration.ipynb`

### 10.5 Prompt registry
- Versioned, hash-addressed prompts, each linked to the eval scores it produced.
- Files: `src/keystone/application/model/prompts/`, `evals/results/`

### 10.6 Eval-gated CI
- A PR degrading any quality metric beyond threshold cannot merge.
- Files: `.github/workflows/evals.yml`, `evals/run_evals.py`

### 10.7 Performance regression gates
- Separate from quality: fail the build if tokens-per-task or p95 latency degrade beyond
  threshold. A change making the agent 30% more expensive should fail as loudly as a broken test.
- Files: `.github/workflows/evals.yml`, `evals/suites/performance.py`

### 10.8 Online monitoring
- Production run sampling and drift detection against the offline baseline.
- Files: `src/keystone/application/evaluation/online.py`

**Concepts** — Eval-driven development, component vs end-to-end evaluation, trajectory scoring,
LLM-as-judge and its failure modes, regression gating, drift detection.

**Anchor** — Statistics: sampling, inter-rater agreement, significance at small n.

**Study** — RAGAS; DeepEval; *Judging LLM-as-a-Judge*; Anthropic evaluation guidance.

**Exit criteria**
- [ ] A PR with a deliberately degraded prompt is **blocked by CI**
- [ ] A PR increasing token cost beyond threshold is **blocked by CI**
- [ ] Judge agreement with human labels reported with κ
- [ ] Trajectory evals distinguish a good path from a wasteful one on the same final answer
- [ ] Every prompt in production is registry-versioned

**Proof** — Screenshot of CI blocking a quality regression; the judge-calibration report.

---

## Phase 11 · Observability & Run Debugging

**Goal** — Understand a non-deterministic, multi-step process well enough to debug it after
the fact.

**Why here** — Print-statement debugging has stopped working, and Phase 3's event log makes
something far better possible.

**Duration** — ~2 weeks

### 11.1 Distributed tracing
- Spans following the natural hierarchy `run → step → tool call → model call`, using GenAI
  semantic conventions.
- Files: `src/keystone/infrastructure/observability/tracing.py`, `infra/observability/otel/`

### 11.2 Correlation
- One identifier threaded from HTTP request through queue through worker through model call.
- Files: `src/keystone/infrastructure/observability/context.py`

### 11.3 Run replay & time-travel debugging ← **the payoff for Phase 3**
- Reconstruct any historical run from its event log and step through it. Possible only because
  of the determinism boundary.
- Files: `src/keystone/application/runtime/replay.py`, `src/keystone/interfaces/cli/replay.py`,
  `scripts/ops/replay_run.py`

### 11.4 Trajectory inspection
- Execution graph with per-node latency, tokens, and cost.
- Files: `src/keystone/interfaces/http/routers/trajectory.py`, `web/components/`

### 11.5 Metrics
- **RED** (rate, errors, duration) + **USE** (utilization, saturation, errors) + AI-specific:
  tokens/sec, cache hit rate, provider fallback rate, eval score, cost per run, queue depth.
- Files: `src/keystone/infrastructure/observability/metrics.py`, `infra/observability/prometheus/`

### 11.6 Dashboards
- System, business, and cost dashboards, version-controlled as JSON.
- Files: `infra/observability/grafana/dashboards/`

### 11.7 SLOs & error budgets
- Defined targets with error budgets, published.
- Files: `docs/operations/slos.md`

### 11.8 Alerting & runbooks
- Alert rules as code, and one runbook per alert — an alert without a runbook is noise.
- Files: `infra/observability/prometheus/rules/`, `docs/operations/runbooks/`

### 11.9 Logging hygiene
- Structured logging (`structlog`, never `print`), with automatic PII and secret redaction in
  logs and traces.
- Files: `src/keystone/infrastructure/observability/logging.py`

**Concepts** — Distributed tracing, semantic conventions, deterministic replay debugging,
RED/USE, SLOs and error budgets, actionable alerting.

**Anchor** — OS: `strace`, debuggers, breakpoints. CN: request tracing across boundaries.

**Study** — OpenTelemetry GenAI semantic conventions; the Google SRE book; Langfuse.

**Exit criteria**
- [ ] One trace spans HTTP → queue → worker → tool → model with no gaps
- [ ] Any historical run can be replayed and stepped through
- [ ] Dashboards show system, business, and cost views
- [ ] Every alert has a runbook
- [ ] No secret or PII appears in any log or trace (verified by test)

**Proof** — A recorded debugging session: production run failed → replayed → stepped to the
failing node → cause identified. Plus a public read-only dashboard.

---

## Phase 12 · Event Backbone & Concurrency

**Goal** — Decouple the system, and make concurrency explicit, fair, and safe.

**Why here** — Multiple workloads now compete for workers; direct enqueueing is the bottleneck
and fairness is a real problem.

**Duration** — ~2 weeks

### 12.1 Streams & consumer groups
- Redis Streams with consumer groups, plus an ADR comparing Kafka/Redpanda and justifying the
  choice for a solo-operated system.
- Files: `src/keystone/infrastructure/messaging/redis_streams.py`,
  `docs/adr/00xx-redis-streams-over-kafka.md`

### 12.2 Delivery semantics
- At-least-once with dedup on message identity and idempotent consumers.
- Files: `src/keystone/application/messaging/consumer.py`

### 12.3 Outbox pattern
- Database write and event publish made atomic.
- Files: `src/keystone/infrastructure/persistence/postgres/outbox.py`

### 12.4 Backpressure
- Bounded queues, consumer-lag monitoring, admission control that sheds load rather than
  collapsing.
- Files: `src/keystone/application/messaging/backpressure.py`

### 12.5 DLQ & replay
- Dead-lettering with operator replay.
- Files: `src/keystone/application/messaging/dlq.py`, `scripts/ops/replay_dlq.py`

### 12.6 Worker pool
- Concurrency caps, **fair scheduling across tenants** so one tenant cannot starve others,
  graceful shutdown with in-flight drain.
- Files: `src/keystone/interfaces/worker/pool.py`

### 12.7 Shared-resource concurrency
- Distinct from run ownership: optimistic concurrency with version columns, Postgres advisory
  locks where pessimistic locking is genuinely needed, and an explicit **isolation level** choice
  per operation with the reasoning recorded.
- Files: `src/keystone/infrastructure/persistence/postgres/concurrency.py`,
  `docs/adr/00xx-isolation-levels.md`

### 12.8 Event cascade
- Document ingested → embedded → indexed → subscribers notified, entirely event-driven.
- Files: `src/keystone/application/events/`

**Concepts** — Event-driven architecture, delivery semantics, consumer groups, backpressure and
load shedding, outbox pattern, fair queueing, optimistic concurrency control, isolation levels.

**Anchor** — OS: producer/consumer, semaphores, bounded buffers, starvation.
DBMS: isolation levels, lost update, write skew, MVCC. Queueing theory: Little's Law.

**Study** — Redis Streams documentation; the transactional outbox pattern; Kafka delivery
semantics for comparison; Postgres isolation-level documentation.

**Exit criteria**
- [ ] Consumer stopped 10 minutes under load; on restart the backlog drains with zero loss and
      zero duplicates
- [ ] Consumer-lag graph shows the spike and recovery
- [ ] One tenant flooding the system does not starve others (measured)
- [ ] Concurrent writes to a shared record resolve without lost updates
- [ ] Graceful shutdown drains in-flight work with no orphaned runs

**Proof** — Lag and recovery chart; fairness measurement under adversarial tenant load.

---
---

# T6 — PLATFORM & CLOUD

## Phase 13 · Action Workload

**Goal** — Agents that *do things* in real external systems, where failure is partial and
irreversible.

**Why here** — The tool platform was built against your own tools. Real third-party APIs break it
in ways you cannot anticipate, and this is where enterprise agentic AI actually lives.

**Duration** — ~2 weeks

### 13.1 Integrations
- Two or three real SaaS APIs with free developer tiers. The specific choice matters less than
  that they are genuinely external and genuinely unreliable.
- Files: `src/keystone/infrastructure/tools/integrations/`

### 13.2 OAuth & credentials
- Authorization flows, token refresh, per-tenant encrypted storage. The agent acts **as** the
  tenant, never with platform keys.
- Files: `src/keystone/infrastructure/tools/oauth.py`,
  `src/keystone/application/tools/credential_broker.py`

### 13.3 Webhook ingestion
- Signature verification, replay-attack protection, dedup, out-of-order handling.
- Files: `src/keystone/interfaces/http/routers/webhooks.py`

### 13.4 External rate limits
- Third-party quota exhaustion handled **inside an agent loop** — a different problem from
  handling it in a request handler.
- Files: `src/keystone/application/tools/external_limits.py`

### 13.5 Partial-failure reconciliation
- The Phase 4 compensation machinery meeting real, non-transactional external services.
- Files: `src/keystone/application/tools/reconciliation.py`

### 13.6 Schema drift
- Detection and alerting when a vendor changes their API underneath you.
- Files: `src/keystone/application/tools/drift.py`, `tests/contract/test_external_schemas.py`

**Concepts** — OAuth and delegated authorization, webhook security, external rate-limit handling,
distributed partial failure, real-world compensation, vendor schema drift.

**Anchor** — CN: authentication protocols, idempotent request design.
Distributed systems: the impossibility of atomic multi-system writes.

**Exit criteria**
- [ ] An agent completes a multi-system workflow across ≥2 external services
- [ ] When step 3 fails, steps 1–2 are cleanly unwound and the audit trail proves consistency
- [ ] Tokens refresh without interrupting an in-flight run
- [ ] A replayed webhook is rejected
- [ ] Vendor schema change is detected by contract test, not by production failure

**Proof** — Recording of a real cross-system partial failure being compensated.

---

## Phase 14 · Multi-tenancy & Security

**Goal** — Safe for strangers, and safe from the model itself.

**Why here** — Real external credentials now flow through the system. Isolation stops being
theoretical.

**Duration** — ~2 weeks

### 14.1 Tenant isolation
- Postgres row-level security **and** per-tenant vector namespaces — defence in depth, because a
  single mechanism is not isolation.
- Files: `.../migrations/`, `src/keystone/infrastructure/persistence/postgres/rls.py`

### 14.2 RBAC
- Roles, permissions, policy evaluation at the boundary.
- Files: `src/keystone/application/auth/rbac.py`, `src/keystone/interfaces/http/dependencies.py`

### 14.3 Quotas & distributed rate limiting
- Runs, tokens, and tool calls per tenant; Redis token bucket with Lua for atomicity.
- Files: `src/keystone/application/tenancy/quotas.py`,
  `src/keystone/infrastructure/messaging/redis_scripts/`

### 14.4 Noisy-neighbour control
- Per-tenant concurrency caps and fair queueing (built in Phase 12) enforced here.
- Files: `src/keystone/application/tenancy/fairness.py`

### 14.5 Prompt-injection red team ← **you attack your own system**
- 50+ adversarial cases across attack classes: direct injection, **indirect injection via
  retrieved documents** (the realistic enterprise attack), tool-output injection, credential and
  data exfiltration, capability escalation.
- Files: `tests/security/injection/`, `docs/operations/red-team-report.md`

### 14.6 Defence & enforcement
- Tool-permission enforcement verified under adversarial pressure; input and output filtering.
- Files: `src/keystone/application/security/`

### 14.7 Audit trail
- Immutable record: who, what, when, which credentials, which tenant.
- Files: `src/keystone/infrastructure/persistence/postgres/audit.py`

### 14.8 Secret hygiene
- Rotation procedure; verified absence of secrets in logs, traces, and error messages.
- Files: `scripts/ops/rotate_secrets.py`, `docs/operations/runbooks/secret-rotation.md`

**Concepts** — Multi-tenancy patterns, defence in depth, RBAC, distributed rate limiting,
AI-specific attack surface, audit integrity, least privilege.

**Anchor** — DBMS: row-level security, isolation. OS: privilege separation, access control models.

**Study** — OWASP LLM Top 10; Simon Willison on prompt injection; Postgres RLS documentation.

**Exit criteria**
- [ ] Cross-tenant data access is impossible via API, vector search, or memory
- [ ] Quota exhaustion degrades one tenant only, with no global impact
- [ ] Red-team report published: attack class → outcome → mitigation → residual risk
- [ ] Indirect injection via a retrieved document cannot escalate tool capability
- [ ] Audit log is append-only and covers every tool invocation
- [ ] Automated test proves no secret reaches logs or traces

**Proof** — The red-team report on your own system.

---

## Phase 15 · Containerization & Orchestration ⭐

**Goal** — Production-grade container topology and Kubernetes fluency, without paying for a
managed control plane.

**Why here** — Container and orchestration semantics must be understood before cloud deployment
translates them.

**Duration** — ~2 weeks

### 15.1 Image hardening
- Multi-stage builds, minimal base images, non-root users, pinned digests, layer caching.
- Files: `infra/docker/{api,worker,web,sandbox}.Dockerfile`, `.dockerignore`

### 15.2 Local Kubernetes
- `kind` or `k3s` cluster on the laptop — free, and the concepts and YAML are identical to
  managed Kubernetes.
- Files: `infra/k8s/kind-cluster.yaml`, `Makefile`

### 15.3 Workload manifests
- Deployment, Service, ConfigMap, Secret, Namespace for API, worker, and web.
- Files: `infra/k8s/base/`

### 15.4 Resource governance
- Requests and limits, QoS classes, and the resulting eviction behaviour under pressure.
- Files: `infra/k8s/base/`

### 15.5 Health & lifecycle
- Liveness, readiness, and startup probes; `preStop` hooks and graceful shutdown so a terminating
  pod drains in-flight runs rather than abandoning them.
- Files: `infra/k8s/base/`, `src/keystone/interfaces/worker/lifecycle.py`

### 15.6 Autoscaling
- Horizontal Pod Autoscaler driven by a **custom metric** (run-queue depth), because CPU is the
  wrong signal for an agent workload.
- Files: `infra/k8s/base/hpa.yaml`

### 15.7 Stateful dependencies
- StatefulSet with persistent volumes for local Postgres/Redis, and the reasoning for why
  managed services replace them in cloud.
- Files: `infra/k8s/base/`

### 15.8 Deployment target decision
- ADR: local Kubernetes for learning; **ECS Fargate for production**, because an EKS control
  plane alone (~$73/month) exceeds the entire infrastructure budget. Knowing Kubernetes and
  choosing ECS deliberately is a stronger signal than silently using either.
- Files: `docs/adr/0006-ecs-fargate-over-eks.md` *(expanded)*

**Concepts** — Container hardening, declarative orchestration, resource requests/limits, QoS,
probes, graceful termination, custom-metric autoscaling, StatefulSets.

**Anchor** — OS: cgroups, namespaces, process supervision, signal handling.

**Exit criteria**
- [ ] Full stack runs on local Kubernetes from manifests
- [ ] Killing a pod mid-run causes no run loss (Phase 3 durability proven under orchestration)
- [ ] Rolling update completes with zero dropped requests
- [ ] HPA scales on queue depth under synthetic load
- [ ] A container exceeding its memory limit is terminated without affecting neighbours
- [ ] ECS-vs-EKS ADR written with the cost analysis

**Proof** — Recording of a rolling update and a pod kill with zero run loss.

---

## Phase 16 · Cloud, IaC & Scale

**Goal** — Reproducible infrastructure, safe releases, and a defensible capacity and cost story.

**Why here** — Last, deliberately: infrastructure-as-code for a system whose shape is still
changing is wasted work, and capacity modelling requires a system that already does real work.

**Duration** — ~3 weeks

### 16.1 Terraform bootstrap
- Remote state in S3 with **DynamoDB state locking**, so concurrent applies cannot corrupt
  infrastructure.
- Files: `infra/terraform/bootstrap/`, `infra/terraform/backend/`

### 16.2 CI authentication via OIDC
- GitHub Actions assumes a short-lived IAM role through OpenID Connect. **No long-lived access
  keys in repository secrets** — that pattern is a known anti-pattern.
- Files: `infra/terraform/modules/github-oidc/`, `.github/workflows/deploy-*.yml`,
  `docs/adr/00xx-oidc-over-static-keys.md`

### 16.3 Network
- VPC, public and private subnets, security groups, NAT strategy chosen for cost.
- Files: `infra/terraform/modules/network/`

### 16.4 Data services
- RDS Postgres with pgvector, ElastiCache Redis, S3 buckets with lifecycle policies (the L3
  memory tier, same code path as local MinIO).
- Files: `infra/terraform/modules/{rds,redis,s3}/`

### 16.5 Compute
- ECS Fargate services for API and worker, Application Load Balancer, service discovery.
- Files: `infra/terraform/modules/ecs-service/`

### 16.6 Identity
- Least-privilege IAM roles per service, each with written justification rather than a wildcard.
- Files: `infra/terraform/modules/iam/`

### 16.7 Environments
- `dev`, `staging`, `prod` as thin module invocations, so environments cannot drift.
- Files: `infra/terraform/environments/{dev,staging,prod}/`

### 16.8 Delivery pipeline
- test → **eval gate** → build → deploy staging → smoke → **canary to prod** → automatic
  rollback on metric regression.
- Files: `.github/workflows/deploy-staging.yml`, `.github/workflows/deploy-prod.yml`

### 16.9 Serverless path
- Lambda + API Gateway for the event-driven ingestion trigger.
- Files: `src/keystone/interfaces/ingest/`, `infra/terraform/modules/lambda/`

### 16.10 Managed AI services — each with a build-vs-buy ADR
- **Bedrock** behind the existing gateway, with Bedrock Guardrails compared against our own
  defences; **OpenSearch Serverless** benchmarked against pgvector on cost, latency, and
  operational burden; **SageMaker** endpoint hosting the Phase 9 ranker with autoscaling (CPU);
  **Step Functions** compared against our own orchestration engine.
- Files: `src/keystone/infrastructure/models/bedrock.py`,
  `src/keystone/infrastructure/retrieval/opensearch.py`, `ml/serving/sagemaker/`,
  `docs/adr/00xx-*.md` (four ADRs)

### 16.11 Load testing
- k6 scenarios shaped for **agent workloads** — long-lived, stateful, expensive runs behave
  nothing like CRUD traffic.
- Files: `tests/load/`, `notebooks/benchmarks/load_test_analysis.ipynb`

### 16.12 Capacity model
- MAU → concurrent sessions → runs/sec → tool calls/sec → tokens/min → $/month, with the
  saturating tier identified at each level and the extrapolation stated honestly.
- Files: `docs/architecture/capacity-model.md`

### 16.13 Cost engineering
- Attribution per tenant, feature, and run; a documented optimization campaign with before/after.
- Files: `infra/observability/grafana/dashboards/cost.json`, `docs/operations/cost-review.md`

### 16.14 Chaos exercises
- Kill Redis, kill a provider, kill a worker, exhaust a quota — prove graceful degradation at
  each and record what survived.
- Files: `scripts/ops/chaos/`, `docs/operations/chaos-results.md`

**Concepts** — Infrastructure as code, remote state locking, OIDC federation, immutable
infrastructure, least-privilege IAM, progressive delivery, managed-service evaluation, capacity
planning, FinOps, chaos engineering.

**Anchor** — CN: VPC design, subnets, routing, security groups.
Computer architecture: profiling, bottleneck analysis, Amdahl's law.

**Exit criteria**
- [ ] `terraform destroy` followed by `terraform apply` rebuilds the entire platform from nothing
- [ ] No long-lived AWS credentials exist anywhere in CI
- [ ] A deliberately bad deploy triggers automatic canary rollback
- [ ] Load test identifies the first saturating tier, with evidence
- [ ] Capacity model published with measured versus extrapolated clearly separated
- [ ] Cost per 1,000 runs measured before and after optimization
- [ ] Four build-vs-buy ADRs written with real benchmark numbers
- [ ] Chaos results documented per dependency
- [ ] Monthly spend within the budget cap

**Proof** — Recording of full infrastructure rebuild from zero; canary auto-rollback; the
capacity model; before/after cost and latency charts.

---
---

# T7 — OPERATE

## Phase 17 · Operate & Publish

**Goal** — Convert the build into a compounding asset.

**Why here** — Building and *operating* teach different things, and only the second is rare.

**Duration** — ongoing

### 17.1 Live operation
- Keep it running. Accrue real incidents.
- Files: `docs/operations/`

### 17.2 Postmortems
- Blameless: timeline, root cause, what changed. Negative results are published, which is what
  separates a research record from a portfolio.
- Files: `docs/operations/postmortems/`

### 17.3 Writing series
- 12–18 deep dives, each grounded in a phase and its measurements.
- Files: `docs/writing/`, drafts in `private/drafts/`

### 17.4 Visual artifacts
- Complete C4 set; the shareable diagrams (OS↔runtime mapping, determinism boundary, run state
  machine, topologies, deployment topology).
- Files: `docs/architecture/c4/`, `docs/architecture/diagrams/`

### 17.5 Demo
- A five-minute recorded walkthrough.
- Files: `docs/README.md` (link)

### 17.6 Optional extraction
- The model gateway or the runtime published as a standalone open-source package.

**Exit criteria**
- [ ] ≥3 months continuous operation
- [ ] ≥3 postmortems from real incidents
- [ ] ≥12 published deep dives
- [ ] Complete C4 set
- [ ] Demo video published
- [ ] Public SLO dashboard live

**Proof** — Months of uptime, a body of writing, and a system explicable at any depth.

---
---

# Summary

| Phase | Name | Weeks |
| --- | --- | --- |
| 0 | Foundations & Decisions | 1 |
| 1 | Architecture Skeleton | 1.5 |
| 2 | Walking Skeleton | 2 |
| 3 ⭐ | Agent Execution Runtime | 3 |
| 4 ⭐ | Tool Platform | 2.5 |
| 5 ⭐ | Memory & Context | 2.5 |
| 6 ⭐ | Orchestration & Protocols | 2.5 |
| 7 | Model Plane | 2.5 |
| 8 | Data Plane & Retrieval | 3 |
| 9 | ML & MLOps | 2.5 |
| 10 | Evaluation Harness | 2 |
| 11 | Observability & Debugging | 2 |
| 12 | Event Backbone & Concurrency | 2 |
| 13 | Action Workload | 2 |
| 14 | Multi-tenancy & Security | 2 |
| 15 ⭐ | Containerization & Orchestration | 2 |
| 16 | Cloud, IaC & Scale | 3 |
| 17 | Operate & Publish | ongoing |
| | **Total** | **~35 weeks** |

**Milestones**

| When | State |
| --- | --- |
| Week 4 | Working end-to-end system, locally |
| Month 3.5 | Runtime core complete — the differentiating capability exists |
| Month 5.5 | Full quality and operations story |
| Month 8 | Deployed, scaled, operated, documented |

**Constraints held throughout** — solo · CPU only, no GPU at any point · local development until
Phase 16 · AWS spend under a hard cap, free and local wherever possible · every significant
decision recorded as an ADR · no phase begins until the previous phase's exit criteria are
fully met.
