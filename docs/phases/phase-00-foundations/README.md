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

- [ ] A stranger reading `docs/` understands what is being built and why, with zero code present
- [ ] Six ADRs written, each naming alternatives considered and why they lost
- [ ] `repository-structure.md` defines the home of every future file type, and every `(Ph N)`
      marker in it maps to an assigned sub-phase in the roadmap
- [ ] C4 context diagram renders, and the OS↔runtime mapping diagram is exported
- [ ] `docs/phases/README.md` status board exists and reflects reality
- [ ] AWS budget alarm confirmed active (screenshot in `evidence/`)
- [ ] CI runs green on lint, formatting, and markdown/link checks (no package exists yet)
- [ ] `.gitignore` verified to exclude `CLAUDE.md` and `private/` (`git check-ignore -v`)
- [ ] `.env.example` documents every variable with obviously-fake placeholders

## Proof

The repository is legible and disciplined **before** it is functional.

## Standing deliverables

Design ([`design.md`](design.md)) · Write-up ([`writeup.md`](writeup.md)) · Evidence
([`evidence/`](evidence/)) · ADRs 0001–0006 · Diagram (OS↔runtime mapping) · status-board update ·
session-log entries.
