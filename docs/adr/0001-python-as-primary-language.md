# ADR-0001 · Python as primary language

- **Status:** Accepted
- **Date:** 2026-08-18 · **Accepted:** 2026-08-19
- **Phase:** 0

## Context

The platform is async-heavy (streaming, concurrent agent runs, I/O-bound model and tool calls)
and sits in an ecosystem where the agent, ML, and data libraries are Python-first (LangGraph,
pydantic, pgvector clients, LightGBM, the provider SDKs). The developer is strongest in Python.
The complexity budget must go into the *execution model*, not into juggling languages.

## Decision

Python (async-first) is the primary language for all backend logic. TypeScript is used only for
the thin web interface; HCL only for Terraform. No other language is introduced without an ADR.

## Alternatives considered

| Option | Why not chosen |
| --- | --- |
| Go | Excellent concurrency, but the agent/ML ecosystem is thin; would fight the tooling |
| Rust | Best-in-class safety/performance, but slows solo iteration and the libraries aren't here |
| Java/Kotlin | Mature, but heavier and off-ecosystem for GenAI work |

## Consequences

**Positive** — one language for runtime, data, and ML; the richest agent ecosystem; fast iteration.

**Negative / accepted** — GIL and raw-CPU limits vs Go/Rust; mitigated by async I/O, worker
processes, and the fact that no GPU/compute-bound path lives in-process.

**Revisit if** — a hot path proves CPU-bound in a way async and worker scaling cannot address.
