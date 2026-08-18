# Contributing to AI_Keystone

Thank you for looking. First, an honest framing of what this project is.

AI_Keystone is a **solo learning project** — a deliberate, long-form study of AI infrastructure,
built in public. Building the core components *myself* is the entire point; it is how the
understanding is earned. That shapes what contributions make sense here.

## Very welcome

- **Issues** — bugs, correctness problems, "you got X wrong", "this claim doesn't hold"
- **Design critique** — better approaches, missed failure modes, sharper tradeoffs
- **Questions** — about the architecture, the decisions, or the reasoning
- **Discussion** — pointers to papers, prior art, or systems worth studying

These cost nothing and make the work better. Open an issue or a discussion.

## Likely to be declined (for now)

- **Pull requests implementing core runtime components** (execution engine, tool platform, memory,
  orchestration — Phases 3–6). Building these is the learning objective; accepting an
  implementation would defeat the purpose.

This is not about the quality of your work — it's about whose hands need to build it.

## Opening up later

From **Phase 8 onward**, peripheral contributions become welcome — additional model-provider
adapters, extra tool integrations, and documentation fixes — where they extend the platform
without replacing its core. This file will be updated when that opens.

## Workflow

The repository runs an organisation-grade workflow even though it is solo: one issue per unit of
work, a branch per issue, a PR per branch with a real description, CI green before merge, and a
protected `main`. Commits follow [Conventional Commits](https://www.conventionalcommits.org).

## Ground rules

- Be accurate and be kind. Disagreement about engineering is welcome; name the tradeoff.
- No secrets in issues or PRs — this is a public repository.
