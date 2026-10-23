# System Context

This view identifies the Phase 1 co-pilot boundary and its external actors and data sources.

```mermaid
flowchart LR
    customer["Customer"]
    agent["Support Agent /<br/>Human Reviewer"]
    ops["Support Operations /<br/>Compliance"]
    copilot["Support-ticket Co-pilot"]
    kb["Approved Valetax<br/>Knowledge Pages"]
    llm["LLM Provider"]
    metrics["Evaluation and<br/>Business-case Outputs"]

    customer -->|"Incoming ticket"| agent
    agent -->|"Submit ticket · REQ-001"| copilot
    copilot -->|"Classification, cited draft or abstention,<br/>review reasons · REQ-002–010"| agent
    copilot -->|"Retrieve approved passages · REQ-004"| kb
    copilot -->|"Constrained inference"| llm
    ops -->|"Safety and routing policy"| copilot
    copilot -->|"Measured results · REQ-013/014"| metrics
```

The co-pilot assists agents; it does not execute transactions, decide complaints/KYC/AML outcomes, or provide trading advice.

