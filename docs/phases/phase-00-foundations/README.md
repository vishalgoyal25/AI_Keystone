# Phase 0 · Foundations & Decisions

**Status:** 🟡 in progress · **Duration:** ~1 week · **Track:** T1 Foundation

> Full sub-phase detail: [`../../roadmap.md`](../../roadmap.md) § Phase 0.

## Goal

Establish that no decision in this project goes unrecorded, and that the environment is
reproducible, **before any application code exists**. Documentation discipline cannot be
retrofitted honestly.

## Scope

Documentation spine, decision practice (ADRs), the CS-foundations mapping, collaboration setup,
environment readiness, cloud cost guardrails, and private planning. **No application code.**

## Sub-phases

| # | Sub-phase | Key files |
| --- | --- | --- |
| 0.1 | Repo foundation & rulebook | `CLAUDE.md`, `.gitignore`, `README.md` |
| 0.2 | Documentation spine | `docs/README.md`, `roadmap.md`, `repository-structure.md`, `c4/context.md`, `phases/README.md` |
| 0.3 | Decision practice | `adr/README.md`, `adr/template.md`, `adr/0001`–`0006` |
| 0.4 | Foundations mapping | `foundations/README.md`, `foundations/os-to-agent-runtime.md` |
| 0.5 | Collaboration setup | `CONTRIBUTING.md`, `LICENSE`, PR & issue templates |
| 0.6 | Environment readiness | `pyproject.toml`, `Makefile`, `.env.example`, `ci.yml` |
| 0.7 | Cloud guardrails | AWS account + hard budget alarm (no tracked files) |
| 0.8 | Private planning | `private/planning/session-log.md`, `strategy.md` |

## Exit criteria

*All must be genuinely true before Phase 1 begins.*

**Documentation**
- [x] A stranger reading `docs/` understands what is being built and why, with zero code present
- [x] Six ADRs written, each naming alternatives considered and why they lost, and all moved
      **Proposed → Accepted**
- [x] `repository-structure.md` defines the home of every future file type, and every `(Ph N)`
      marker in it maps to an assigned sub-phase in the roadmap
- [ ] C4 context and OS↔runtime diagrams **render correctly on GitHub** (verify after push)
- [x] `docs/phases/README.md` status board exists and reflects reality

**Environment**
- [x] `./myvenv` created, Python ≥ 3.11, `.[dev,test]` installed and active
- [x] `make verify` runs with **0 failures** (19 checks). Docker, Redis, and `.env` report WARN —
      correct, they are Phase 2 requirements
- [x] `make check` passes locally
- [x] Pre-commit hooks installed and clean across all files
- [x] `.env.example` documents every variable with obviously-fake placeholders
- [x] `.gitattributes` normalises line endings (LF in repo; `.ps1`/`.bat` CRLF)

**Safety & workflow**
- [x] `.gitignore` verified to exclude `CLAUDE.md`, `private/`, `.env` (`git check-ignore -v`)
- [x] ~~`private/` backed up~~ — ⏸ deferred to end of Phase 2 (see roadmap 0.10)
- [ ] CI runs green on lint and formatting (verify after push)
- [ ] Branch protection active on `main`
- [x] `writeup.md` completed against these criteria
- [ ] Tag `v0.1.0-phase-00-foundations` applied

**Deferred by decision — not blocking**
- ⏸ AWS account + hard budget alarm → before Phase 16 (roadmap 0.13)
- ⏸ Dependabot + extra issue templates → Phase 1 (roadmap 0.5)
- ⚠️ **pgvector confirmation → required before Phase 2.** `verify_env` reports SKIP pending
      PostgreSQL auth setup. Having PostgreSQL 17 installed does *not* mean the extension is
      present, and the data plane cannot work without it.

## Proof

The repository is legible and disciplined **before** it is functional.

## Standing deliverables

Design ([`design.md`](design.md)) · Write-up ([`writeup.md`](writeup.md)) · Evidence
([`evidence/`](evidence/)) · ADRs 0001–0006 · Diagram (OS↔runtime mapping) · status-board update ·
session-log entries.
