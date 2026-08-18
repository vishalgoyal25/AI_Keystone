# ADR-0002 · Hexagonal architecture with a CI-enforced dependency rule

- **Status:** Proposed
- **Date:** 2026-08-18
- **Phase:** 0

## Context

The system will grow to ~18 phases of components that must remain swappable (model providers,
vector stores, message brokers) and testable in isolation. Business logic must not be coupled to
any specific database, framework, or provider. The Phase 3 determinism boundary further requires
that even time and randomness be injectable.

## Decision

Adopt hexagonal architecture (ports & adapters). Layers: `domain` (pure) ← `application`
(use cases + ports) ← `infrastructure` / `interfaces` (adapters). The dependency direction is
inward and **enforced in CI by import-linter** — a reverse import fails the build. All wiring
lives in one composition root. Time/rng/clock are ports.

## Alternatives considered

| Option | Why not chosen |
| --- | --- |
| Layered-by-technical-type (controllers/services/models) | Leaks framework and DB concerns into logic; hard to swap adapters |
| Enforce boundaries by convention | Conventions rot silently; only a build gate holds over 8 months |
| Microservices from the start | Operational suicide for a solo dev; premature distribution |

## Consequences

**Positive** — swappable adapters, isolated tests, a legible structure, and the determinism
boundary becomes natural. Modular monolith with service-ready seams.

**Negative / accepted** — more indirection and boilerplate (ports + adapters + wiring) than a
flat app; accepted as the cost of long-term maintainability.

**Revisit if** — never for the rule itself; specific port shapes evolve via their own ADRs.
