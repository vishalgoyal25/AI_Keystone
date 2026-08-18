# Documentation

The written record is a first-class part of AI_Keystone — as much as the code. This directory
holds all of it. Start where your question points.

## Start here

| If you want to… | Read |
| --- | --- |
| Understand what this project is | [`../README.md`](../README.md) |
| Follow the build, phase by phase | [`roadmap.md`](roadmap.md) → [`phases/README.md`](phases/README.md) |
| See the engineering decisions and why | [`adr/README.md`](adr/README.md) |
| Understand how a subsystem works | [`architecture/concepts/`](architecture/concepts/) *(grows from Phase 3)* |
| Know where a file belongs | [`architecture/repository-structure.md`](architecture/repository-structure.md) |
| See the system's shape | [`architecture/c4/context.md`](architecture/c4/context.md) |
| See the CS theory behind the design | [`foundations/README.md`](foundations/README.md) |
| Operate the system | [`operations/`](operations/) *(from Phase 11)* |
| Read the essays | [`writing/`](writing/) *(from Phase 17)* |

## How this is organised

Documentation runs on **two axes that are never merged**:

- **Chronological** — [`phases/`](phases/): what was done, when, and what it proved. **Frozen**
  once written; a historical record.
- **Topical** — [`adr/`](adr/) and [`architecture/concepts/`](architecture/): how the system
  works and why it is built this way. **Living**; updated as the system evolves.

Merging them is why most documentation rots — the record gets rewritten every time the system
changes. Here it does not.

## Conventions

- ADRs are numbered, zero-padded, and **immutable once Accepted** — a change of mind is a new ADR.
- One concept lives in exactly one file; everything else links to it.
- Directories are created when a real file needs them — no empty scaffolding.
