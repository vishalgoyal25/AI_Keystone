# The OS ↔ Agent Runtime Mapping

The governing analogy of AI_Keystone, as a diagram.

> **If the LLM is the CPU, AI_Keystone is the operating system.**

Each operating-system concept on the left maps to an agent-runtime component on the right, tagged
with the phase that builds it. The analogy is a design guide, not decoration — the
operating-systems literature is genuinely the theory behind each component.

```mermaid
graph LR
    subgraph OS["Operating System"]
        direction TB
        os1["Process scheduler"]
        os2["Process control block"]
        os3["Write-ahead log"]
        os4["System call interface"]
        os5["Memory management"]
        os6["Virtual memory / paging"]
        os7["Protection rings"]
        os8["Interrupt / fault handling"]
        os9["cgroups / resource limits"]
        os10["Debugger / strace"]
        os11["IPC"]
    end

    subgraph RT["AI_Keystone Agent Runtime"]
        direction TB
        rt1["Run scheduling<br/>priority · aging · fairness<br/><b>Ph 3</b>"]
        rt2["Run state<br/>externalised · checkpointed<br/><b>Ph 3</b>"]
        rt3["Event log<br/>state = fold(events)<br/><b>Ph 3</b>"]
        rt4["Tool boundary<br/>schema contracts · capabilities<br/><b>Ph 4</b>"]
        rt5["Context budgeting<br/>memory tiers L1/L2/L3<br/><b>Ph 5</b>"]
        rt6["Context compaction<br/>semantic page fault<br/><b>Ph 5</b>"]
        rt7["Credential brokering<br/>sandboxed execution<br/><b>Ph 4</b>"]
        rt8["Timeouts · cancellation<br/>compensation · saga<br/><b>Ph 3-4</b>"]
        rt9["Per-tenant quotas<br/>token budgets<br/><b>Ph 7 · 14</b>"]
        rt10["Trajectory replay<br/>time-travel debugging<br/><b>Ph 11</b>"]
        rt11["Agent-to-agent messaging<br/>handoff · delegation<br/><b>Ph 6</b>"]
    end

    os1 --> rt1
    os2 --> rt2
    os3 --> rt3
    os4 --> rt4
    os5 --> rt5
    os6 --> rt6
    os7 --> rt7
    os8 --> rt8
    os9 --> rt9
    os10 --> rt10
    os11 --> rt11
```

## Where the analogy breaks

Worth stating, because the differences are where the engineering actually lives:

| | Operating system | Agent runtime |
| --- | --- | --- |
| **Addressing** | Exact — the MMU knows which page is absent | **Semantic** — absence must be inferred; retrieval is similarity-based, not equality |
| **Hardware support** | MMU, TLB, page tables in silicon | **None** — fault detection, handling, and the page table are all application code |
| **Miss cost** | Microseconds to milliseconds; latency only | 100ms–seconds, **plus money** (vector search + tokens) |
| **Failure mode** | Transparent — the program cannot tell | **Not transparent** — the wrong page produces a confidently wrong answer |

That last row is the significant one: OS paging is correctness-preserving, agent paging is
quality-affecting. There is no equivalent of "the page simply loaded correctly."

**Related:** [`../../foundations/os-to-agent-runtime.md`](../../foundations/os-to-agent-runtime.md)
