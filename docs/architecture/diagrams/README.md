# Diagrams

One diagram per phase — the phase's most explanatory visual. These are the highest-reach
artifacts the project produces: a good architecture diagram is shared far more widely than a good
ADR is read.

## Format policy

**Canonical format is `.md` containing a fenced ` ```mermaid ` block**, not standalone `.mmd`.

| Format | Renders on GitHub | Renders in VS Code | Use |
| --- | --- | --- | --- |
| **`.md` + ```mermaid block** | ✅ natively | ✅ with a preview extension | **Canonical — always** |
| standalone `.mmd` | ❌ shows as plain text | ⚠️ only with an extension | Avoid |
| `.svg` export | ✅ | ✅ | Optional, for essays and external posts |

A `.md` diagram file carries the diagram **plus** a caption explaining what it shows and, where
useful, where the model breaks down. A diagram without that context is decoration.

## Viewing locally

- **VS Code** — install *Markdown Preview Mermaid Support*, then `Ctrl+Shift+V`
- **JetBrains** — Mermaid support is built into the Markdown plugin
- **Exporting to SVG/PNG** (only when needed for an essay):
  `npx @mermaid-js/mermaid-cli -i <file>.md -o <file>.svg`

## Index

| Diagram | Phase | Subject |
| --- | --- | --- |
| [`os-to-runtime-mapping.md`](os-to-runtime-mapping.md) | 0 | OS concepts ↔ agent runtime components |

Planned subjects per phase are listed in [`../../roadmap.md`](../../roadmap.md) under
*Standing deliverables*.
