# ADR-0003 · Build the execution runtime rather than adopt Temporal

- **Status:** Proposed
- **Date:** 2026-08-18
- **Phase:** 0

## Context

Durable agent execution (checkpointing, crash-resume, deterministic replay, leases) is the core
learning objective of this project. Temporal, Restate, and AWS Step Functions provide these
guarantees off the shelf. The goal here is **demonstrated understanding of the mechanism**, not
the fastest path to a durable workflow.

## Decision

Build the execution runtime in-house — event-sourced state, the determinism boundary, leases with
fencing tokens, the scheduler — treating Temporal's published model as the reference design to
study and match, not a dependency to import.

## Alternatives considered

| Option | Why not chosen |
| --- | --- |
| Adopt Temporal | Hides exactly the mechanism the project exists to demonstrate; adds an operational dependency |
| Step Functions | Managed, AWS-locked, opaque; no learning of the internals |
| No durability (naive loop) | Fails the entire premise — the pain log (Ph 2) will demand it |

## Consequences

**Positive** — deep, defensible understanding of durable execution; the event log unlocks Phase
11 replay debugging almost for free; no external workflow dependency.

**Negative / accepted** — significant build effort (Phase 3 is the deepest phase) and the burden
of correctness (fencing, determinism discipline) falls on us. This is the point, not a drawback.

**Revisit if** — the goal shifts from learning to shipping a product at speed; then a managed
engine behind the same ports becomes reasonable.
