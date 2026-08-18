# AI_Keystone

**An agent runtime platform — the infrastructure layer that agentic AI applications execute on.**

Not an agent. Not an AI application. The substrate beneath them.

---

## Purpose

AI_Keystone is a deliberate, long-form study of **AI infrastructure**, built as a real system
rather than a set of exercises.

The application layer of AI — calling a model, wiring up retrieval, shipping a chat interface —
is well documented and increasingly commoditised. The layer beneath it is not. How does a request
become a durable agent run? Where does that run's state live, and what happens when a worker dies
at step seven of twelve? How do you give a non-deterministic process access to real systems
without handing it real credentials? How do you debug, observe, and regression-test something
that never produces the same output twice?

Those questions have answers, and the answers are engineering — schedulers, state machines,
isolation boundaries, failure semantics, memory hierarchies, and evaluation harnesses. This
repository works through them by building the system rather than reading about it.

The goal is depth: a platform designed, deployed, and **operated** long enough to meet real
failure, real cost, and real load — with the reasoning behind every significant decision written
down as it happens.

## The core idea

> **If the LLM is the CPU, AI_Keystone is the operating system.**

A language model can reason. It cannot schedule its own work, survive a process crash, hold state
across minutes, call tools safely, isolate one tenant from another, or explain what it did and
why. Those are infrastructure concerns — and they map closely onto problems operating systems
solved decades ago.

| Operating system | Agent runtime |
| --- | --- |
| Process scheduler | Agent run scheduling, priority, aging, fairness |
| Process control block | Run state, checkpointed for crash-resume |
| Write-ahead log | Append-only event log; state is a fold over events |
| System call interface | Tool boundary — the controlled path to the outside world |
| Memory management | Context-window budgeting; working / episodic / semantic tiers |
| Virtual memory & paging | Context compaction — summarise out, page relevant history back in |
| Cache hierarchy | L1 Redis → L2 Postgres → L3 object storage |
| Inter-process communication | Agent-to-agent messaging, handoff, delegation |
| Protection rings | Capability model, credential brokering, sandboxing |
| Interrupt & fault handling | Timeouts, cancellation, tool failure, compensating actions |
| Resource limits (cgroups) | Per-tenant quotas, token budgets, concurrency caps |
| Debugger / `strace` | Trajectory tracing, deterministic replay, time-travel debugging |

The analogy is not decorative. Each row is a component that has to be designed, and the
operating-systems literature is a genuinely useful guide to designing it.

## What the platform provides

| Layer | Responsibility |
| --- | --- |
| **Execution runtime** | Durable agent execution: event-sourced state, checkpointing, crash-resume, deterministic replay, leases with fencing tokens, scheduling, budgets, cancellation |
| **Tool platform** | Registry with schema contracts, capability-based permissions, credential brokering, sandboxed execution, idempotency, compensating transactions |
| **Memory architecture** | Working / episodic / semantic / procedural memory across L1–L3 storage tiers, with consolidation, decay, and asynchronous context compaction |
| **Orchestration** | Workflow graph as a validated IR; supervisor, handoff, parallel fan-out, critic loops, hierarchical delegation; loop budgets; MCP; agent-to-agent protocols |
| **Model plane** | Provider-agnostic gateway with routing, fallback chains, circuit breaking, semantic caching, and token-aware rate limiting |
| **Data plane** | Incremental ingestion, hybrid retrieval, reranking, and measured retrieval quality |
| **Evaluation** | Trajectory-level evaluation — scoring the path taken, not only the answer — gating deployment |
| **Observability** | Distributed tracing across non-deterministic multi-step runs, run replay, SLOs, cost and quality metrics |
| **Platform** | Multi-tenancy, isolation, quotas, distributed rate limiting, audit trail |

## Two workloads

The platform carries two deliberately opposite workloads. This is what makes it a platform rather
than an application: one system, two very different stress profiles.

**Knowledge-heavy** — research intelligence over scientific literature. Retrieval with grounded
citations, multi-step literature review, and a learned recommender. Stresses memory, context
management, retrieval quality, and long reasoning chains.

**Action-heavy** — agents operating against real third-party APIs, where steps have side effects
and failures are partial. Stresses the tool boundary, credential isolation, idempotency, and
compensating transactions.

## Development philosophy

**Build the walking skeleton first, then deepen.**
A thin vertical slice through every layer — minimal, unpolished, working end to end — comes before
any layer is built properly. The slice produces a *pain log*, and every subsequent phase closes an
item on it. Deepening is therefore driven by observed failure, never by a checklist.

**Depth allocation, not build order, is where the difficulty goes.**
The agent runtime, tool platform, memory architecture, and orchestration layer receive the deepest
treatment, because that is where the scarce engineering lives.

**Everything built must be load-bearing.**
No scaffolding for its own sake, no component that exists to demonstrate a concept and is then
discarded. If it would not survive into the final system, it is not built.

**Design the seams for scale; build the scale later.**
Idempotency, watermarking, partitioning strategy, and storage abstractions are established from
the first commit because retrofitting them is prohibitively expensive. Horizontal capacity is
added when there is load to justify it.

**Boring technology by default.**
Novelty must be argued for in an ADR. The complexity budget belongs in the execution model —
concurrency, failure handling, state — not in the number of technologies involved.

**Architecture enforced by tooling, not intention.**
The codebase follows a ports-and-adapters structure and the dependency rule is checked in CI. A
domain layer that imports infrastructure fails the build.

**Decisions are recorded, including the ones that turned out badly.**
Every significant choice is an ADR: problem, constraints, alternatives considered, decision,
consequences. ADRs are immutable once accepted; a change of mind is a new ADR that supersedes the
old one, so the record shows what was believed and when.

**Operated, not merely deployed.**
Building a system and running a system teach different things. This one stays live, accrues
incidents, and the postmortems are published alongside the successes.

## Roadmap

Eighteen phases across seven tracks, roughly 35 weeks, solo, CPU-only throughout.

```
T1 FOUNDATION        Ph 0–1     architecture skeleton, patterns, CI
T2 SKELETON          Ph 2       thin end-to-end slice + pain log
T3 RUNTIME CORE ⭐    Ph 3–6     execution, tools, memory, orchestration
T4 SUPPORTING        Ph 7–9     model plane, data plane, ML
T5 QUALITY & OPS     Ph 10–12   evals, observability, event backbone
T6 PLATFORM & CLOUD  Ph 13–16   integration, tenancy, containers, AWS
T7 OPERATE           Ph 17      run it, write about it
```

Each phase declares its exit criteria **before** it starts, and no phase begins until the previous
one's criteria are fully met.

**Full detail — sub-phases, files touched, concepts, study sources, exit criteria, and proof
artifacts: [`docs/roadmap.md`](docs/roadmap.md).**

## Stack

Technology choices are recorded as ADRs; this reflects current direction.

| Concern | Choice |
| --- | --- |
| Language | Python (async-first); TypeScript for the interface; HCL for infrastructure |
| API | FastAPI, Pydantic |
| Orchestration | LangGraph, MCP |
| Datastore | PostgreSQL 17 + pgvector |
| Cache, streams, rate limiting | Redis 7 |
| Object storage | MinIO locally, S3 in cloud — one code path |
| Interface | Next.js, React, TypeScript (deliberately thin) |
| Model providers | Provider-agnostic gateway across multiple frontier and inference APIs |
| Evaluation | Offline harness with trajectory scoring; regression gates in CI |
| Observability | OpenTelemetry, Prometheus, Grafana |
| Machine learning | Gradient-boosted ranking (LambdaMART); offline IR evaluation; no GPU |
| Containers | Docker; local Kubernetes (kind/k3s) for orchestration work |
| Cloud | AWS — ECS Fargate, RDS, ElastiCache, S3, Bedrock |
| Infrastructure as code | Terraform, with remote state and locking |
| CI/CD | GitHub Actions, with test and evaluation gates before promotion |

## Scope boundaries

Stated explicitly, because scope discipline is part of the design. "AI infrastructure" names at
least five distinct disciplines; this is one of them, chosen deliberately.

- **Not model training or research.** This layer sits above the model, not inside it.
- **Not GPU or large-scale training infrastructure.** No distributed training, no CUDA or Triton
  kernels, no tensor or pipeline parallelism. Different discipline, different problem.
- **Not inference-serving internals.** No PagedAttention or continuous-batching implementation —
  hosted inference is consumed, not served.
- **Not a low-code product or a commercial platform clone.** The runtime is exposed as code, not
  hidden behind a builder interface.
- **Not a data engineering project.** The data plane exists to serve the AI layer, sized to what
  that requires and architected so it can be scaled later.
- **Not a UI project.** The interface is a window into the platform, never the deliverable.

## Repository layout

```
docs/          architecture, ADRs, phase records, foundations, operations
src/keystone/  domain · application (+ports) · infrastructure (adapters) · interfaces
web/           thin Next.js interface
ml/            features, training, evaluation, registry (Phase 9)
evals/         datasets, suites, judges, results (Phase 10)
tests/         unit · integration · contract · architecture · e2e · load
infra/         terraform, docker, kubernetes, observability config
notebooks/     benchmarks and analysis — charts are evidence
scripts/       development, data, and operational scripts
```

Directories are created when a real file needs them — there is no empty scaffolding. The full
future tree, with the home of every file type, is defined in
[`docs/architecture/repository-structure.md`](docs/architecture/repository-structure.md).

## Why this is public

Architecture is judgment exercised under constraints, and judgment is only visible when the
reasoning is written down. Source code shows what was built; it rarely shows what was considered
and rejected, or why.

This repository is therefore as much a written record as a codebase: architecture decision
records, design documents, phase write-ups with measurements, benchmark notebooks, and
postmortems from operating the system. The commit history is left intact deliberately — the
evolution is part of the record.

---

**Status:** Phase 0 — foundations. Documentation and architectural discipline are being
established before application code exists. That ordering is intentional.
