# Phase 0 · Design

> Worked out **before** building. Records the intended approach and the reasoning, so the
> write-up can later report what actually happened against it.

## Problem

A long-lived, solo, build-in-public infrastructure project needs its judgment to be **visible**
and its state to be **recoverable** after gaps. Both are impossible to retrofit honestly. Phase 0
puts the record-keeping and reproducibility machinery in place before there is code to document.

## Approach

1. **Decisions as ADRs** — every significant choice captured with alternatives and consequences,
   immutable once accepted.
2. **Two-axis documentation** — chronological (`phases/`) separated from topical
   (`adr/`, `concepts/`) so neither corrupts the other.
3. **A single placement authority** — `repository-structure.md` decides where every file lives,
   so the tree cannot drift into chaos as it grows.
4. **Foundations mapping** — the CS theory the developer already owns, mapped explicitly onto the
   system's components, to make later phases learnable rather than mysterious.
5. **Cost guardrails first** — a hard AWS budget alarm before any resource can be created,
   because uncontrolled cloud spend is how solo projects die.
6. **Resumability machinery** — session log, phase status board, exit-criteria checklists.

## Key decisions (detailed in ADRs)

- 0001 Python as primary language · 0002 Hexagonal architecture · 0003 Build the runtime rather
  than adopt Temporal · 0004 Postgres + pgvector · 0005 AWS with a hard cost ceiling ·
  0006 ECS Fargate over EKS.

## Out of scope for Phase 0

Any application code, dependency installation beyond tooling, and any cloud resource other than
the account and its budget alarm.
