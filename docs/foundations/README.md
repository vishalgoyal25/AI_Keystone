# Foundations — CS Theory → AI Systems

The premise of this project: **the CS fundamentals are the theory behind AI infrastructure, not a
separate subject.** A durable agent runtime is an operating system problem; state management is a
database problem; workflow orchestration is a compiler problem; the model gateway is a networking
problem; retrieval is an algorithms problem.

These documents make each mapping explicit — naming the real component, then anchoring it to the
fundamental that explains it. They exist so the build is *learnable at depth* rather than taken on
faith, and so the vocabulary transfers to interviews and to conversations with senior engineers.

## The mappings

| Fundamental | Maps onto | Doc | Phase |
| --- | --- | --- | --- |
| Operating systems | The agent execution runtime | [`os-to-agent-runtime.md`](os-to-agent-runtime.md) | 0 |
| Databases | Event-sourced state & recovery | `dbms-to-state-management.md` | 3 |
| Compiler design | Workflow-graph orchestration | `compilers-to-orchestration.md` | 6 |
| Computer networks | The model plane & gateway | `networks-to-model-plane.md` | 7 |
| Algorithms & data structures | Retrieval & ranking | `algorithms-to-retrieval.md` | 8 |

Each is written in the phase where its subject is built, so the theory lands next to the practice.
The OS mapping comes first because the runtime core is the deepest part of the system and the OS
analogy governs the whole design.
