# ADR-0005 · AWS as cloud, under a hard cost ceiling

- **Status:** Accepted
- **Date:** 2026-08-18 · **Accepted:** 2026-08-19
- **Phase:** 0

## Context

The project must demonstrate real cloud and IaC competence, and AWS is the most widely recognised
target for AI-infrastructure roles (Bedrock, SageMaker, OpenSearch, ECS). It is also solo-funded,
so uncontrolled spend is an existential risk — the most common way solo cloud projects die.

## Decision

AWS is the cloud provider. A **hard budget cap with billing alarms is configured in Phase 0,
before any resource is created**. Development stays local until Phase 16; free/local tooling is
preferred everywhere; money is spent only at AWS, only where a concept genuinely requires it.

## Alternatives considered

| Option | Why not chosen |
| --- | --- |
| GCP / Azure | Fine technically, but AWS has the broadest role recognition and the managed AI services targeted |
| Stay fully local | Forgoes the IaC, managed-service, and scale learning that is a core objective |
| No budget cap | Unacceptable financial risk for a solo, months-long project |

## Consequences

**Positive** — recognised cloud experience; access to Bedrock/SageMaker/OpenSearch for real
build-vs-buy ADRs; spend stays bounded and visible.

**Negative / accepted** — some managed services cost more than self-hosting; each is entered only
with a cost justification, and cheaper equivalents (e.g. ECS over EKS, ADR-0006) are preferred.

**Revisit if** — the budget proves insufficient for a required Phase 16 demonstration; then scope,
not the cap, is adjusted.
