# Phase 0 · Write-up

**Foundations & Decisions** · 2026-08-18 → 2026-08-19 · Tag `v0.1.0-phase-00-foundations`

> What was built, what was proven, and what changed from [`design.md`](design.md).

## What was built

**Documentation spine (0.1–0.4)** — the operating manual and ignore rules; a reader-routing index;
the 18-phase roadmap with sub-phases, file paths, concepts, study sources, exit criteria, and proof
artifacts per phase; the repository-structure document that decides where every future file lives;
the C4 Level-1 context diagram; the OS↔agent-runtime mapping diagram; and the phase status board.

**Decision record (0.3, 0.11)** — ADR practice established with a template and index, and the six
decisions genuinely made so far written up with their alternatives and consequences. All six moved
Proposed → Accepted on 2026-08-19 and are now immutable.

**Foundations (0.4)** — `os-to-agent-runtime.md`, the project's most distinctive early artifact:
the run as a process, the event log as a write-ahead log, the determinism boundary, scheduling,
memory hierarchy with demand versus anticipatory paging, the tool boundary as a system call,
leases and fencing, and an explicit account of where the analogy breaks down.

**Collaboration (0.5)** — contribution policy stated honestly (issues and critique welcome;
core-runtime PRs declined until Phase 8 because building them is the point), MIT licence, PR and
issue templates.

**Environment (0.6–0.9)** — dependency groups declaring the dev/prod split; a cross-platform
`Makefile` as the single command entry point; a hermetic conda environment at `./myvenv`; a
dependency-free verification script; and pre-commit hooks including a secret guard.

## What was proven

| Exit criterion | Evidence |
| --- | --- |
| Documentation legible with zero code | `docs/` reads end to end; a reader reaches the roadmap in two clicks from the README |
| Decisions recorded with alternatives | Six ADRs, each naming what lost and why; all Accepted |
| Every file has a defined home | `repository-structure.md`; every `(Ph N)` marker maps to an assigned sub-phase |
| Environment is hermetic | `site.ENABLE_USER_SITE == False`; `pip check` clean after removing leaked user-site packages |
| Assumptions are verified, not assumed | `make verify` — 19 checks, 0 failures |
| Private files cannot leak | `git check-ignore` confirms `CLAUDE.md`, `private/`, `.env` — re-checked on every `make verify` |
| Quality gates work | `make check` clean; `pre-commit run --all-files` clean |

## What changed from the design

Four deviations, all deliberate and recorded:

1. **AWS setup deferred** (0.13). The design put cost guardrails first. On review, nothing is
   provisioned until Phase 16, so creating an account now would start a clock and add a
   verification dependency for no benefit. The rule is unchanged: *the budget alarm exists before
   the first resource does.*
2. **`private/` backup deferred** to end of Phase 2 (0.10). At Phase 0 the content is thin and
   reconstructable; a whole-disk backup covers it when revisited.
3. **Phase 0 grew from 8 sub-phases to 13.** The original plan treated "environment readiness" as
   one item. Splitting it into declaration → creation → verification → quality gates exposed real
   defects that a single step would have hidden.
4. **Dependabot and extra issue templates deferred** to Phase 1 — they would currently watch four
   dev tools and no software.

## What the environment work actually caught

The verification step (0.8) existed to turn assumptions into facts, and it earned its place
immediately:

- **User site-packages were leaking into `./myvenv`** — three unrelated, broken packages
  (`dataset`, `datasets`, `alembic`) were visible inside a supposedly fresh environment. Fixed
  with `PYTHONNOUSERSITE=1`. Undetected, this would have produced irreproducible builds.
- **`make` is absent on Windows** — installed via conda-forge, and the `Makefile` rewritten to
  avoid `grep`/`awk`/`command -v` so the same targets work on Windows, Git Bash, and CI.
- **Standalone `.mmd` files do not render on GitHub** — diagrams moved to `.md` with fenced
  `mermaid` blocks, and a format policy recorded in `diagrams/README.md`.
- **A verification script must never prompt** — `psql` blocked on a password prompt; fixed with
  `-w`.
- **Line endings were unmanaged** — `.gitattributes` added to normalise LF, with `.ps1`/`.bat`
  kept as CRLF.

## Deferred, with triggers

| Item | Trigger |
| --- | --- |
| AWS account + hard budget alarm | Immediately before Phase 16 |
| `private/` backup | End of Phase 2, or ~10 session-log entries |
| Dependabot, extra issue templates | Phase 1, when there are real dependencies |
| pgvector confirmation | **Before Phase 2** — `verify_env` reports SKIP pending auth setup |

## Metrics

Not applicable — Phase 0 has no runtime. Later phases report measurements here against targets
declared in advance.

## Links

[Exit criteria](README.md) · [Design](design.md) · [Evidence](evidence/) ·
[ADRs 0001–0006](../../adr/README.md) · [Roadmap § Phase 0](../../roadmap.md)
