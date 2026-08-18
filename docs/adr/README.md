# Architecture Decision Records

Every significant decision is recorded here: the problem, the constraints, the alternatives
genuinely considered, the decision, and its consequences. This is where the project's *judgment*
is visible — source code shows what was built, not what was rejected and why.

## Rules

- **Numbered, zero-padded, never renumbered.** The number is a permanent identifier, cited from
  code, commits, and other docs.
- **Immutable once Accepted.** A change of mind is a *new* ADR that supersedes the old one; the
  old one is marked `Superseded by NNNN`, never edited or deleted.
- **Status:** `Proposed` → `Accepted` → optionally `Superseded` / `Deprecated`.
- Format: [`template.md`](template.md).

## Index

| ADR | Title | Status | Date |
| --- | --- | --- | --- |
| [0001](0001-python-as-primary-language.md) | Python as primary language | Proposed | 2026-08-18 |
| [0002](0002-hexagonal-architecture.md) | Hexagonal architecture with a CI-enforced dependency rule | Proposed | 2026-08-18 |
| [0003](0003-build-runtime-not-adopt-temporal.md) | Build the execution runtime rather than adopt Temporal | Proposed | 2026-08-18 |
| [0004](0004-postgres-pgvector-primary-store.md) | PostgreSQL + pgvector as the primary store | Proposed | 2026-08-18 |
| [0005](0005-aws-with-hard-cost-ceiling.md) | AWS as cloud, under a hard cost ceiling | Proposed | 2026-08-18 |
| [0006](0006-ecs-fargate-over-eks.md) | ECS Fargate for production; local Kubernetes for learning | Proposed | 2026-08-18 |

> Later ADRs are added as decisions are made — e.g. lease-vs-Redlock (Ph 3), tool isolation level
> (Ph 4), model routing policy (Ph 7), Redis Streams vs Kafka (Ph 12), isolation levels (Ph 12),
> OIDC vs static keys (Ph 16), and the four managed-service build-vs-buy decisions (Ph 16).
