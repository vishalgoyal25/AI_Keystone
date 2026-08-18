# Repository Structure

**The authority for file placement in AI_Keystone.**

> Every file has exactly one correct home, and it is defined here. If something has no home, its
> home is decided **and recorded in this document** before the file is created.
>
> This describes the **complete future tree**. Directories marked `(Ph N)` do not exist yet —
> they are created when the first real file needs them. **There is no empty scaffolding**: a
> directory containing only a placeholder is a promise, not a structure, and reviewers can tell
> the difference.

---

## 1 · Placement principles

| Principle | Consequence |
| --- | --- |
| **One concern, one home** | A file type appears in exactly one place. No "utils" scattered across layers |
| **Dependency direction is inward** | `domain ← application ← infrastructure/interfaces`, enforced by CI |
| **Ports are centralised** | Every interface the system plugs into lives in `application/ports/` |
| **Wiring is centralised** | All dependency binding in one composition root |
| **Different lifecycle → different tree** | ML training code and runtime code are separate top-level trees |
| **Correctness ≠ quality** | `tests/` asserts correctness; `evals/` measures quality. Never merged |
| **Create on first use** | Directories appear when a real file needs them |
| **Public by default, private by exception** | `private/` and `CLAUDE.md` are the only exceptions, and they are gitignored |

### The architectural shape

**A modular monolith with service-ready seams.** Strict module boundaries give the discipline of
microservices without the operational cost of running them solo. Multiple *deployable units*
(API, worker, ingest Lambda, CLI) already share one codebase through `interfaces/`, so extraction
later is mechanical rather than archaeological.

---

## 2 · Top level

```
AI_Keystone/
├── .github/          CI/CD workflows, PR & issue templates
├── docs/             ALL public documentation
├── src/keystone/     backend — hexagonal architecture
├── web/              thin Next.js interface                      (Ph 2)
├── ml/               ML training & registry — separate lifecycle  (Ph 9)
├── evals/            quality measurement (≠ tests)                (Ph 10)
├── tests/            correctness assertion
├── notebooks/        benchmarks & analysis — charts are evidence
├── infra/            terraform, docker, kubernetes, observability
├── scripts/          development, data, and operational scripts
├── data/             local corpora — gitignored except samples    (Ph 2)
├── private/          GITIGNORED — strategy, drafts, planning
├── trash/            GITIGNORED — nothing is ever hard-deleted
├── CLAUDE.md         GITIGNORED — operating manual
├── README.md
├── CONTRIBUTING.md   (Ph 0)
├── LICENSE           (Ph 0)
├── CHANGELOG.md      (Ph 1)
├── pyproject.toml    dependency groups: core / dev / test / ml / docs
├── docker-compose.yml                                            (Ph 2)
├── Makefile          the single entry point for every command
├── .env.example      every variable documented, no real values
├── .importlinter     the dependency rule                          (Ph 1)
├── .pre-commit-config.yaml                                        (Ph 1)
└── .gitignore
```

---

## 3 · `docs/` — public documentation

```
docs/
├── README.md                      reader router — routes by audience, not a ToC
├── roadmap.md                     ★ 18-phase plan; authority for what gets built
│
├── adr/                           Architecture Decision Records
│   ├── README.md                  index: number · title · status · date
│   ├── template.md                Context → Decision → Status → Consequences
│   └── NNNN-kebab-case-title.md   zero-padded, never renumbered, never edited once Accepted
│
├── architecture/
│   ├── repository-structure.md    ★ this file — authority for file placement
│   ├── capacity-model.md                                          (Ph 16)
│   ├── c4/
│   │   ├── context.md             L1 — system in its environment
│   │   ├── container.md           L2 — processes & datastores      (Ph 2)
│   │   └── component-*.md         L3 — internals, one per subsystem (Ph 3+)
│   ├── diagrams/
│   │   ├── *.mmd                  Mermaid sources — diffable, GitHub-rendered
│   │   └── *.svg                  Excalidraw exports for shareable diagrams
│   └── concepts/                  ← PERMANENT topical reference, kept current
│       ├── determinism-boundary.md                                (Ph 3)
│       ├── lease-and-fencing.md                                   (Ph 3)
│       ├── tool-capability-model.md                               (Ph 4)
│       ├── memory-tiers.md                                        (Ph 5)
│       ├── context-budgeting.md                                   (Ph 5)
│       ├── token-aware-rate-limiting.md                           (Ph 7)
│       ├── zero-downtime-reindex.md                               (Ph 8)
│       └── trajectory-evaluation.md                               (Ph 10)
│
├── phases/                        ← CHRONOLOGICAL record, frozen once written
│   ├── README.md                  live status board across all phases
│   └── phase-NN-slug/
│       ├── README.md              goal, scope, exit-criteria checklist
│       ├── design.md              worked out BEFORE building
│       ├── writeup.md             what was built, what was proven
│       └── evidence/              charts, screenshots, recordings
│
├── foundations/                   CS fundamentals → AI systems mapping
│   ├── README.md
│   ├── os-to-agent-runtime.md                                     (Ph 0)
│   ├── dbms-to-state-management.md                                (Ph 3)
│   ├── compilers-to-orchestration.md                              (Ph 6)
│   ├── networks-to-model-plane.md                                 (Ph 7)
│   └── algorithms-to-retrieval.md                                 (Ph 8)
│
├── operations/                                                    (Ph 11+)
│   ├── slos.md
│   ├── runbooks/                  one per alert — an alert without one is noise
│   ├── postmortems/               YYYY-MM-DD-slug.md — negative results published
│   ├── red-team-report.md                                         (Ph 14)
│   ├── chaos-results.md                                           (Ph 16)
│   └── cost-review.md                                             (Ph 16)
│
├── api/                           generated OpenAPI + usage guides (Ph 2)
└── writing/                       published essays (drafts in private/)
```

### The two documentation axes — do not merge them

| Axis | Location | Answers | Lifetime |
| --- | --- | --- | --- |
| **Chronological** | `phases/` | *"What was done, when, and what did it prove?"* | **Frozen** once written |
| **Topical** | `architecture/concepts/`, `adr/` | *"How does subsystem X work?"* | **Living** — updated as the system evolves |

Merging them is why most repositories' documentation rots: the historical record gets rewritten
every time the system changes, and the reference becomes archaeology.

---

## 4 · `src/keystone/` — the backend

```
src/keystone/
│
├── domain/                        PURE. Imports nothing internal. No I/O, no framework.
│   ├── run/                       Run, RunEvent, RunState, state_machine, errors   (Ph 3)
│   ├── agent/                     Agent, CapabilitySet                             (Ph 3)
│   ├── tool/                      ToolDescriptor, SideEffectClass                  (Ph 4)
│   ├── memory/                    MemoryRecord, MemoryType, Tier                   (Ph 5)
│   ├── orchestration/             graph, node, edge — the IR types                 (Ph 6)
│   ├── retrieval/                 Document, Chunk, Citation, lineage               (Ph 8)
│   └── shared/                    value objects, base errors, structures/
│       └── structures/            priority queue+aging, LRU/LFU, token bucket,
│                                  consistent hash ring, bloom filter               (Ph 1)
│
├── application/                   Use cases + PORTS. Imports domain only.
│   ├── ports/                     ← EVERY interface the system plugs into
│   │   ├── run_store.py  model.py  tool_registry.py  memory_store.py
│   │   ├── retrieval.py  source.py  event_bus.py
│   │   └── clock.py  random.py    ← time & randomness are ports (determinism)
│   ├── runtime/                   executor, scheduler, effects, replay_cursor,
│   │                              lease, budgets, cancellation, retry             (Ph 3)
│   ├── tools/                     registry, validation, permissions,
│   │                              credential_broker, idempotency, compensation,
│   │                              saga, errors, limits, external_limits,
│   │                              reconciliation, drift                        (Ph 4, 13)
│   ├── memory/                    tiering, write_policy, consolidation, decay,
│   │                              context_budget, compaction, assembly,
│   │                              isolation                                       (Ph 5)
│   ├── orchestration/             ir, validation, topologies/, loop_guard,
│   │                              handoff, hitl, messaging                        (Ph 6)
│   ├── model/                     router, circuit_breaker, fallback,
│   │                              semantic_cache, token_estimator, rate_limiter,
│   │                              admission, accounting, structured, streaming,
│   │                              prompts/                                        (Ph 7)
│   ├── ingest/                    sync, upsert, quality, dlq                      (Ph 8)
│   ├── retrieval/                 chunking/, embedding, hybrid orchestration,
│   │                              graph                                           (Ph 8)
│   ├── evaluation/                online sampling, drift                         (Ph 10)
│   ├── messaging/                 consumer, backpressure, dlq                    (Ph 12)
│   ├── events/                    the ingest→embed→index→notify cascade          (Ph 12)
│   ├── auth/                      rbac, policy evaluation                        (Ph 14)
│   ├── tenancy/                   quotas, fairness                               (Ph 14)
│   ├── security/                  injection defence, filtering                   (Ph 14)
│   ├── experiments/               A/B assignment & metrics                        (Ph 9)
│   └── use_cases/                 start_run, resume_run, cancel_run, approve_run
│
├── infrastructure/                ADAPTERS. Imports application + domain.
│   ├── persistence/
│   │   ├── postgres/              event_store, lease_store, memory_store, outbox,
│   │   │                          audit, rls, concurrency
│   │   ├── redis/                 L1 cache adapters
│   │   ├── objectstore/           MinIO / S3 — L3 tier, one code path
│   │   └── migrations/            Alembic — NEVER edit an applied migration
│   ├── models/                    anthropic, groq, cerebras, bedrock, openai_compat
│   ├── tools/                     concrete tools, sandbox, secrets, oauth,
│   │                              integrations/
│   ├── retrieval/                 pgvector, bm25, hybrid, reranker, opensearch
│   ├── ingest/                    source adapters (arXiv, OpenAlex)
│   ├── messaging/                 redis_streams, redis_scripts/ (Lua)
│   ├── ml/                        feature client, ranker inference (SageMaker)
│   ├── observability/             tracing, metrics, logging, context
│   ├── clock.py  random.py        the non-deterministic adapters
│   └── config/
│       ├── settings.py            env-driven, validated at startup
│       └── container.py           ★ composition root — ALL wiring, one file
│
└── interfaces/                    ← DEPLOYABLE UNITS
    ├── http/                      FastAPI app, routers/, schemas/, dependencies
    ├── worker/                    run executor, pool, lifecycle
    ├── ingest/                    Lambda handler                                 (Ph 16)
    ├── mcp/                       MCP server                                      (Ph 6)
    └── cli/                       admin CLI, replay
```

**The dependency rule** — arrows point inward; violations fail CI:

```
domain  ←  application  ←  infrastructure / interfaces
```

**Watch for drift:** `domain/shared/` and any `utils` module become dumping grounds if unguarded.
A thing belongs in `shared/` only if **two or more** modules genuinely need it **and** it has no
dependencies. Otherwise it belongs to the module that uses it.

---

## 5 · `tests/` — correctness

```
tests/
├── unit/            mirrors src/ — no I/O, fast (<5s total)
├── integration/     real Postgres + Redis via docker-compose
├── contract/        ← every adapter must satisfy its port's contract suite
├── architecture/    fitness functions: import rules, naming conventions
├── e2e/             full stack through the HTTP API
├── load/            k6 scenarios shaped for agent workloads          (Ph 16)
├── security/        injection/ — the self-run red team               (Ph 14)
├── fixtures/
└── conftest.py
```

**Contract tests are the mechanism that makes ports safe.** One suite defines what *any*
`ModelPort` adapter must do; every adapter runs against it. Adding Bedrock in Phase 16 is then
verifiable immediately rather than in production.

---

## 6 · `evals/` — quality (deliberately not in `tests/`)

```
evals/
├── datasets/        retrieval/ generation/ trajectory/ — labelled, versioned, TRACKED
├── suites/          retrieval_quality, generation_quality, trajectory, performance
├── judges/          judge prompts + human calibration data
├── results/         historical scores — TRACKED, this is the regression record
├── reports/         notebooks rendering results
└── run_evals.py
```

| | `tests/` | `evals/` |
| --- | --- | --- |
| Asserts | Correctness | Quality |
| Output | Pass / fail | A score |
| Nature | Deterministic | Statistical |
| Failure means | Code is broken | Quality regressed |

Merging them means a noisy quality metric blocks a legitimate bug fix.

---

## 7 · `ml/` — machine learning (Ph 9)

Separate from `src/` because it has a different lifecycle and different dependencies. Only the
*inference client* lives in `infrastructure/ml/`.

```
ml/
├── features/        definitions shared by training AND serving — prevents train/serve skew
├── training/        pipelines, config/ (seeds, data-snapshot hashes)
├── evaluation/      splits (temporal, no leakage), metrics, ablations
├── registry/        model cards + metadata — WEIGHTS ARE GITIGNORED
├── serving/         packaging for the SageMaker endpoint, cold_start
└── artifacts/       gitignored
```

---

## 8 · `infra/` — infrastructure

```
infra/
├── terraform/                                                       (Ph 16)
│   ├── bootstrap/       S3 state bucket + DynamoDB lock table — run once
│   ├── modules/         network, ecs-service, rds, redis, s3, iam, lambda,
│   │                    github-oidc, observability
│   ├── environments/    dev/ staging/ prod/ — THIN: module calls + variables only
│   └── backend/         remote state configuration
├── k8s/                                                             (Ph 15)
│   ├── kind-cluster.yaml
│   └── base/            Deployment, Service, ConfigMap, HPA, StatefulSet, probes
├── docker/              api, worker, web, sandbox Dockerfiles
├── observability/
│   ├── grafana/dashboards/    JSON — version controlled
│   ├── prometheus/rules/      alerts as code
│   └── otel/                  collector configuration
└── local/               docker-compose stacks for development       (Ph 2)
```

Environments stay thin and modules hold the logic — otherwise dev, staging, and prod drift, and
drift is how "it worked in staging" happens.

---

## 9 · Remaining trees

```
web/            app/ components/ lib/ public/ — thin; a window, never the deliverable
notebooks/      exploration/ benchmarks/ analysis/ — outputs COMMITTED (they are evidence)
scripts/        dev/ (setup, seed, reset)  data/ (load, embed, reindex, backfill)
                ops/ (migrate, rotate-secrets, replay-run, replay-dlq, chaos/)  release/
data/           README.md + samples/ TRACKED; raw/ interim/ processed/ cache/ GITIGNORED
private/        planning/ (session-log, phase prep) · strategy/ · research-notes/
                drafts/ · scratch/                                    ALL GITIGNORED
trash/          YYYY-MM-DD/ + WHY.md one-liner                        GITIGNORED
```

**`trash/`** — nothing meaningful is ever hard-deleted. Git preserves *tracked* files; `trash/`
covers untracked scratch work and removes the friction of discarding hours of effort. The
one-line `WHY.md` prevents resurrecting a bad idea six weeks later.

---

## 10 · Where does X go? — lookup

| I have… | It goes… |
| --- | --- |
| A business rule with no I/O | `domain/<module>/` |
| An interface to something external | `application/ports/` |
| A concrete DB / provider / API implementation | `infrastructure/<category>/` |
| Orchestration logic across domain objects | `application/<module>/` |
| A new HTTP endpoint | `interfaces/http/routers/` |
| A new deployable process | `interfaces/<name>/` |
| Dependency wiring | `infrastructure/config/container.py` — **only** here |
| A decision with alternatives considered | `docs/adr/NNNN-*.md` |
| An explanation of how a subsystem works | `docs/architecture/concepts/` |
| A record of what a phase achieved | `docs/phases/phase-NN-*/writeup.md` |
| A chart, screenshot, or recording | `docs/phases/phase-NN-*/evidence/` |
| A benchmark with analysis | `notebooks/benchmarks/` |
| A theory→practice mapping | `docs/foundations/` |
| An alert response procedure | `docs/operations/runbooks/` |
| A test asserting correctness | `tests/<category>/` |
| A measurement of output quality | `evals/suites/` |
| Labelled evaluation data | `evals/datasets/` |
| Feature engineering code | `ml/features/` |
| Model weights | **Nowhere** — gitignored; registry holds cards and metadata |
| A one-off operational command | `scripts/ops/` |
| A secret | `.env` only — **never** a tracked file |
| Career or strategy notes | `private/strategy/` |
| Something being replaced | `trash/YYYY-MM-DD/` with `WHY.md` |
| Something with no obvious home | **Stop.** Decide its home, record it here, then create it |

---

## 11 · Naming conventions

| Thing | Convention | Example |
| --- | --- | --- |
| ADR | `NNNN-kebab-case.md`, zero-padded, **never renumbered** | `0003-build-runtime-not-adopt-temporal.md` |
| Phase directory | `phase-NN-slug/` | `phase-03-agent-runtime/` |
| Concept doc | `kebab-case.md`, one concept per file | `determinism-boundary.md` |
| Postmortem | `YYYY-MM-DD-slug.md` | `2026-11-14-worker-lease-storm.md` |
| Python module | `snake_case.py` | `circuit_breaker.py` |
| Migration | Alembic revision — **never edit once applied** | |
| Terraform module | `kebab-case/` | `ecs-service/` |
| Branch | `phase-NN/desc`, `fix/`, `docs/`, `chore/`, `spike/` | `phase-03/lease-and-fencing` |
| Commit | Conventional Commits | `feat(runtime): add fencing tokens` |
| Tag | `vX.Y.Z-phase-NN-slug` | `v0.3.0-phase-03-runtime` |

ADR numbers are **permanent identifiers** — cited in code comments, commit messages, and other
documents. Renumbering breaks references.

---

## 12 · Public / private map

| Public | Private (gitignored) |
| --- | --- |
| `docs/` — ADRs, architecture, phases, foundations, operations | `private/strategy/` — career, positioning |
| All source, tests, evals, ml, infra | `private/planning/` — session log, prep |
| `notebooks/` with outputs | `private/research-notes/` — raw reading notes |
| `data/samples/` only | `private/drafts/` — pre-publication essays |
| Sanitised postmortems | `CLAUDE.md` — operating manual |
| Published essays in `docs/writing/` | `trash/`, `data/` (except samples), `.env` |

**Pre-commit checklist:** no secrets, keys, tokens, account IDs · no personal contact details ·
no references to other projects or employers · screenshots scrubbed of URLs and tokens ·
`git diff --staged` actually read, not skimmed.

---

## 13 · Growth rules

1. **Create on first use.** A directory appears when a real file needs it.
2. **Every non-obvious directory gets a `README.md`** stating what belongs there and what does not.
3. **Index files carry status** — `docs/adr/README.md` and `docs/phases/README.md` are live tables.
4. **ADRs are immutable once Accepted.** Change = a new ADR marked as superseding the old one.
5. **Evidence lives with its phase**, never scattered at root.
6. **One concept, one file.** Everything else links to it; nothing re-explains it.
7. **This document is updated in the same commit** as any structural change. A tree that has
   drifted from this file is a defect, not a detail.
