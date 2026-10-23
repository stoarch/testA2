# Primary Use-Case Sequence

This sequence covers the primary agent-assist path, including abstention and mandatory human review.

```mermaid
sequenceDiagram
    actor Agent as Support agent
    participant UI as CLI / Web UI
    participant App as Orchestrator
    participant Classifier as Classifier
    participant Guard as Safety and routing
    participant KB as Approved KB retriever
    participant LLM as LLM provider
    participant Validator as Citation validator

    Agent->>UI: Submit ticket (REQ-001)
    UI->>App: Process ticket
    App->>Classifier: Classify category, urgency, language, sentiment
    Classifier->>LLM: Constrained classification
    LLM-->>Classifier: Structured labels
    Classifier-->>App: Labels
    App->>Guard: Detect protected intents

    alt Trading advice, complaint, KYC, or AML
        Guard-->>App: Mandatory human route
        App-->>UI: Safe decline/acknowledgement + reason
    else Eligible knowledge question
        App->>KB: Retrieve approved passages
        KB-->>App: Passages + source provenance
        App->>LLM: Draft only from evidence
        LLM-->>App: Draft + claim citations
        App->>Validator: Validate claims and citations
        alt Supported and non-conflicting
            Validator-->>App: Validated draft
            App-->>UI: Cited draft + review decision
        else Gap, conflict, or failure
            Validator-->>App: Abstain + reason
            App-->>UI: Abstention + mandatory human route
        end
    end
    UI-->>Agent: Structured result (REQ-010)
```

The human reviewer remains accountable for routed outcomes and customer-facing use.

