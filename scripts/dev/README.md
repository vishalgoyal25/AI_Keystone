# scripts/dev

Developer-environment scripts. These set up or verify a working machine; they never touch
application state or remote infrastructure.

| Script | Purpose |
| --- | --- |
| [`verify_env.py`](verify_env.py) | Go/no-go check on the local environment — `make verify` |

## `verify_env.py`

Turns assumptions into facts. Every check corresponds to something a later phase depends on;
finding a missing one mid-build in Phase 2 is far more expensive than finding it now.

Standard library only, deliberately — it must run before project dependencies exist.

**Status vocabulary**

| Status | Meaning |
| --- | --- |
| `PASS` | Verified working |
| `FAIL` | Hard requirement broken — **blocks**, exit code 1 |
| `WARN` | Needed by a later phase, not yet |
| `SKIP` | Cannot be determined here; verify manually |

**What it checks:** Python ≥ 3.11 · the active interpreter is `./myvenv` · the environment is
hermetic (`PYTHONNOUSERSITE`) · required tools on PATH · git branch and remote · that
`CLAUDE.md`, `private/`, and `.env` are genuinely gitignored (public-repo leak guard) ·
Docker daemon · PostgreSQL reachable · **pgvector actually available** · Redis · `.env` present.

The pgvector check matters more than it looks: having PostgreSQL 17 installed does **not** mean
the extension is present, and the data plane (Phase 8) cannot work without it.

## Where this fits in the daily workflow

Three checks with three different scopes — not duplication:

| When | Command | Answers |
| --- | --- | --- |
| Session start after a gap, or when something is odd | `make verify` | Is the **machine** correct? |
| Every `git commit` (automatic) | pre-commit hooks | Is this **change** clean? |
| Before pushing | `make check` | Does the **codebase** pass what CI runs? |
| On push / PR | GitHub Actions | Enforced, on a clean machine |

`make verify` is deliberately **not** wired into pre-commit or CI. It inspects local machine state
— Docker daemon, PostgreSQL, pgvector — none of which exists on a CI runner. Running it per-commit
would be slow and meaningless; running it in CI would fail for the wrong reason.

## What belongs here

Environment setup, verification, and local bootstrap helpers.

**Not here:** data pipeline scripts (`scripts/data/`), operational runbook commands
(`scripts/ops/`), or anything that writes to a remote system.
