# ADR-0006 · ECS Fargate for production; local Kubernetes for learning

- **Status:** Proposed
- **Date:** 2026-08-18
- **Phase:** 0 (implemented across Ph 15–16)

## Context

Kubernetes is the standard vocabulary of infrastructure engineering and an infra role expects it.
But a managed EKS control plane costs ~$73/month — alone exceeding the entire infrastructure
budget (ADR-0005) — and adds operational burden that is disproportionate for a solo operator.
The learning value of Kubernetes and the cost of running it in production are separable.

## Decision

Split the two: **learn Kubernetes on local `kind`/`k3s`** (real manifests, probes, resource
limits, HPA, StatefulSets — Phase 15), and **deploy production on ECS Fargate** (Phase 16). The
tradeoff itself is documented as the artifact — knowing K8s and deliberately choosing ECS on cost
and operational grounds is a stronger signal than silently using either.

## Alternatives considered

| Option | Why not chosen |
| --- | --- |
| EKS in production | ~$73/mo control plane blows the budget; heavy ops for one operator |
| ECS only, skip K8s entirely | Leaves a gap in expected infra vocabulary; no manifest experience |
| Local K8s only, never deploy | No real cloud deployment; forgoes the production story |

## Consequences

**Positive** — Kubernetes fluency and manifests in the repo, real cloud deployment, budget intact,
and an explicit architectural-judgment artifact.

**Negative / accepted** — two orchestration targets to understand (K8s locally, ECS in cloud);
accepted as deliberate breadth, with the mapping between them documented.

**Revisit if** — a future need (multi-cluster, portability) justifies managed Kubernetes despite
the cost.
