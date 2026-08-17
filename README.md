# AI_Keystone

**An agent runtime platform — the infrastructure layer that agentic AI applications execute on.**

Not an agent. Not an AI application. The substrate beneath them.

---

## Purpose

AI_Keystone is a deliberate, long-form study of **AI infrastructure**, built as a real system
rather than a set of exercises.

The application layer of AI — calling a model, wiring up retrieval, shipping a chat interface —
is well documented and increasingly commoditised. The layer beneath it is not. How does a
request become a durable agent run? Where does agent state live, and what happens when a worker
dies at step seven of twelve? How do you give a non-deterministic process access to real
systems without handing it real credentials? How do you observe, debug, and regression-test
something that never produces the same output twice?

Those questions have answers, and the answers are engineering — schedulers, state machines,
isolation boundaries, failure semantics, and evaluation harnesses. This repository is an
attempt to work through them properly, in the open, by building the system rather than reading
about it.

The goal is depth: a platform that is designed, deployed, and **operated** long enough to
encounter real failure, real cost, and real scale — with the reasoning behind every significant
decision written down.

## The core idea

> **If the LLM is the CPU, AI_Keystone is the operating system.**

A language model can reason. It cannot schedule its own work, survive a process crash, hold
state across minutes, call tools safely, isolate one tenant from another, or explain what it
did and why. Those are infrastructure concerns — and they closely mirror problems operating
systems solved decades ago.

| Operating system | Agent runtime |
| --- | --- |
| Process scheduler | Agent run scheduling, priority, fairness |
| Process control block | Agent state, checkpointed for crash-resume |
| System call interface | Tool interface — the controlled boundary to the outside world |
| Memory management | Context-window budgeting; short- and long-term memory tiers |
| Virtual memory / paging | Context compaction — summarise out, page relevant history back in |
| Inter-process communication | Agent-to-agent messaging, handoff, and delegation |
| Protection rings | Tool permissioning, credential isolation, sandboxing |
| Interrupt and fault handling | Timeouts, cancellation, tool failure, compensating actions |
| Resource limits (cgroups) | Per-tenant quotas, token budgets, concurrency caps |
| Debugger / `strace` | Trajectory tracing, run replay, time-travel debugging |

The analogy is not decorative. Each row corresponds to a component that has to be designed,
and the operating-systems literature is a genuinely useful guide to designing it.

## What the platform provides

| Layer | Responsibility |
| --- | --- |
| **Execution runtime** | Durable agent execution: checkpointing, crash-resume, cancellation, timeout budgets, retries |
| **Tool platform** | Tool registry, schema contracts, permission model, sandboxing, credential brokering, compensation for partial failure |
| **Memory architecture** | Working, episodic, and semantic memory; write and consolidation policies; retrieval into context |
| **Orchestration** | Multi-agent topologies — supervisor, handoff, parallel fan-out, critic and reflection loops; agent-to-agent protocols; MCP |
| **Model plane** | Provider-agnostic gateway with routing, fallback chains, circuit breaking, semantic caching, and cost attribution |
| **Data plane** | Incremental ingestion, hybrid retrieval, reranking, and measured retrieval quality |
| **Evaluation** | Trajectory-level evaluation — scoring the path taken, not only the final answer — gating deployment |
| **Observability** | Distributed tracing across non-deterministic multi-step runs, run replay, SLOs, cost and quality metrics |
| **Platform** | Multi-tenancy, isolation, quotas, rate limiting, authentication and authorisation |

## Two workloads

The platform carries two deliberately opposite workloads. This is what makes it a platform
rather than an application: one system, two very different stress profiles.

**Knowledge-heavy** — research intelligence over scientific literature. Retrieval with grounded
citations, multi-step literature review, and a learned recommender. Stresses memory, context
management, retrieval quality, and long reasoning chains.

**Action-heavy** — agents operating against real third-party APIs, where steps have side
effects and failures are partial. Stresses the tool boundary, credential isolation, idempotency,
and compensating transactions.

## Development philosophy

**Build the walking skeleton first, then deepen.**
A thin vertical slice through every layer — minimal, unpolished, working end to end — comes
before any layer is built properly. Every subsequent deepening is then motivated by observed
pain rather than a checklist, and the system is demonstrable throughout.

**Everything built must be load-bearing.**
No scaffolding for its own sake, no components that exist to demonstrate a concept and are then
discarded. If it would not survive into the final system, it is not built.

**Design the seams for scale; build the scale later.**
Idempotency, watermarking, partitioning strategy, and storage abstractions are established from
the first commit because retrofitting them is prohibitively expensive. Distributed compute and
horizontal capacity are added when there is load to justify them, not before.

**Boring technology by default.**
Novelty must be argued for in an ADR. The complexity budget belongs in the execution model —
concurrency, failure handling, state — not in the number of technologies involved.

**Architecture enforced by tooling, not intention.**
The codebase follows a ports-and-adapters structure, and the dependency rule is checked in CI.
A domain layer that imports infrastructure fails the build.

**Decisions are recorded, including the ones that turned out badly.**
Every significant choice is an ADR: the problem, the constraints, the alternatives considered,
the decision, and its consequences. Reversals are recorded as new ADRs rather than edits.

**Operated, not merely deployed.**
Building a system and running a system teach different things. This one stays live, accrues
incidents, and the postmortems are published.

## Stack

Technology choices are recorded as ADRs; this table reflects current direction.

| Concern | Choice |
| --- | --- |
| Primary language | Python (async-first) |
| API layer | FastAPI, Pydantic |
| Agent orchestration | LangGraph, MCP |
| Datastore | PostgreSQL, pgvector |
| Cache, queues, streams | Redis |
| Interface | Next.js, React, TypeScript (deliberately thin) |
| Model providers | Provider-agnostic gateway across multiple frontier and inference APIs |
| Evaluation | Offline eval harness with trajectory scoring; regression gates in CI |
| Observability | OpenTelemetry, Prometheus, Grafana, LLM-level tracing |
| Machine learning | Gradient-boosted ranking for recommendation; offline evaluation with standard IR metrics |
| Cloud | AWS |
| Infrastructure as code | Terraform |
| Containerisation | Docker |
| CI/CD | GitHub Actions, with tests and evaluation gates before promotion |

## Scope boundaries

Stated explicitly, because scope discipline is part of the design:

- **Not model training or research.** This layer sits above the model, not inside it.
- **Not GPU or large-scale training infrastructure.** Different discipline, different problem.
- **Not a low-code product or a commercial platform clone.** The runtime is exposed as code,
  not hidden behind a builder interface.
- **Not a data engineering project.** The data plane exists to serve the AI layer, sized to
  what that requires and architected so it can be scaled later.
- **Not a UI project.** The interface is a window into the platform, never the deliverable.

## Why this is public

Architecture is judgment exercised under constraints, and judgment is only visible when the
reasoning is written down. Source code shows what was built; it rarely shows what was
considered and rejected, or why.

This repository is therefore as much a written record as a codebase: architecture decision
records, design documents, phase write-ups with measurements, and postmortems from running the
system in production. The commit history is left intact deliberately — the evolution is part of
the record.

---

**Status:** Phase 0 — foundations. Documentation and architectural discipline are being
established before application code exists. That ordering is intentional.
