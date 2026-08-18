%% AI_Keystone — the governing analogy, as a diagram.
%% "If the LLM is the CPU, AI_Keystone is the operating system."
%% Each operating-system concept maps to an agent-runtime component; the right column
%% names the phase where that component is built.

graph LR
    subgraph OS["Operating System"]
        os1[Process scheduler]
        os2[Process control block]
        os3[Write-ahead log]
        os4[System call interface]
        os5[Memory management]
        os6[Virtual memory / paging]
        os7[Protection rings]
        os8[Interrupt / fault handling]
        os9[cgroups / resource limits]
        os10[Debugger / strace]
        os11[IPC]
    end

    subgraph RT["AI_Keystone Agent Runtime"]
        rt1[Run scheduling · priority · aging<br/>Ph 3]
        rt2[Run state · checkpointed<br/>Ph 3]
        rt3[Event log · state = fold events<br/>Ph 3]
        rt4[Tool boundary · capabilities<br/>Ph 4]
        rt5[Context budgeting · memory tiers<br/>Ph 5]
        rt6[Context compaction · paging<br/>Ph 5]
        rt7[Credential brokering · sandboxing<br/>Ph 4]
        rt8[Timeouts · cancellation · compensation<br/>Ph 3-4]
        rt9[Per-tenant quotas · token budgets<br/>Ph 7-14]
        rt10[Trajectory replay · time-travel debug<br/>Ph 11]
        rt11[Agent-to-agent messaging · handoff<br/>Ph 6]
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
