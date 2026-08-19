# Phase 0 · Design

> Worked out **before** building. Records the intended approach and its reasoning, so the write-up
> can later report what actually happened against it.

## Problem

A long-lived, solo, build-in-public infrastructure project has two failure modes that cannot be
fixed retroactively:

1. **Invisible judgment** — decisions made silently and rationalised later. Backfilled reasoning
   reads as backfilled, and it is the reasoning, not the code, that demonstrates architecture.
2. **Unrecoverable state** — returning after a two-week gap and having to reconstruct what you were
   doing and why.

A third, quieter one: **assumed environment**. Discovering in Phase 2 that `pgvector` was never
installed, or that user site-packages are leaking into the venv, costs far more mid-build than it
does now.

Phase 0 puts the record-keeping, reproducibility, and verification machinery in place before there
is any code depending on it.

## Approach

**Documentation**

1. **Decisions as ADRs** — every significant choice with alternatives and consequences, immutable
   once accepted; a change of mind becomes a new superseding record.
2. **Two documentation axes, never merged** — chronological (`phases/`) separated from topical
   (`adr/`, `concepts/`), so the historical record isn't rewritten every time the system changes.
3. **A single placement authority** — `repository-structure.md` decides where every file lives, so
   the tree cannot drift as it grows to hundreds of files.
4. **Foundations mapping** — the CS theory already owned (OS, DBMS, compilers, networks,
   algorithms) mapped explicitly onto system components, so later phases are learnable rather than
   mysterious. This is also the project's most distinctive early artifact.

**Environment**

5. **Hermetic by construction** — a repo-local conda env at `./myvenv` with `PYTHONNOUSERSITE=1`,
   because pip otherwise pulls the machine's user site-packages into the environment and quietly
   destroys reproducibility.
6. **Install only what is used now** — Phase 0 has no application code, so runtime dependencies are
   zero. Pre-installing Phase 2's stack would mean unused packages, versions stale before first
   use, and conflicts resolved blind.
7. **Verification over assumption** — a dependency-free go/no-go script (`make verify`) that turns
   every assumption later phases rely on into a checked fact.

**Safety**

8. **Public/private separation enforced mechanically** — `CLAUDE.md` and `private/` gitignored, and
   `verify_env` re-checks that on every run rather than trusting it once.
9. **Three-layer quality gates** — pre-commit (per commit, automatic), `make check` (before push),
   CI (enforced on a clean machine). Same standard, three scopes.

## Key decisions

All six accepted 2026-08-19: [0001](../../adr/0001-python-as-primary-language.md) Python ·
[0002](../../adr/0002-hexagonal-architecture.md) Hexagonal architecture ·
[0003](../../adr/0003-build-runtime-not-adopt-temporal.md) **Build the runtime rather than adopt
Temporal** · [0004](../../adr/0004-postgres-pgvector-primary-store.md) Postgres + pgvector ·
[0005](../../adr/0005-aws-with-hard-cost-ceiling.md) AWS under a hard cost ceiling ·
[0006](../../adr/0006-ecs-fargate-over-eks.md) ECS Fargate over EKS.

0003 is the consequential one — it defines the project. Adopting Temporal would hide precisely the
mechanism this system exists to demonstrate.

## Deferred by decision (not skipped)

| Item | Deferred to | Why |
| --- | --- | --- |
| AWS account + budget alarm | Before Phase 16 | Nothing is provisioned until then; creating it now starts a clock and adds a verification dependency for zero benefit. The rule stands: **the alarm exists before the first resource does** |
| `private/` backup | End of Phase 2, or ~10 session-log entries | Content is thin and reconstructable now; a whole-disk backup covers it when revisited |

## Out of scope

Any application code, any dependency beyond the dev/test toolchain, and any cloud resource.
