# Component Overview

This logical view shows requirement-driven responsibilities. Technology and provider choices remain WBS-003 decisions.

```mermaid
flowchart LR
    subgraph copilot[Support-ticket Co-pilot]
        interface["CLI / Simple Web UI<br/>REQ-012"]
        orchestrator["Ticket Orchestrator<br/>REQ-001/010/016"]
        classifier["Classifier<br/>REQ-002/003"]
        retrieval["KB Retrieval + Provenance<br/>REQ-004/011"]
        drafting["Grounded Draft / Abstention<br/>REQ-005/006"]
        safety["Safety and Routing Rules<br/>REQ-007–009"]
        validation["Claim / Citation Validator<br/>REQ-005/010"]
        evaluation["Evaluation + Cost Model<br/>REQ-013/014"]
    end

    kb[("Versioned KB Snapshot")]
    llm["LLM Provider"]
    reviewer["Human Reviewer"]

    interface --> orchestrator
    orchestrator --> classifier
    orchestrator --> retrieval
    retrieval --> kb
    classifier --> llm
    retrieval --> drafting
    drafting --> llm
    drafting --> validation
    classifier --> safety
    validation --> safety
    safety --> orchestrator
    orchestrator --> reviewer
    orchestrator --> evaluation
```

Safety and deterministic validation remain separate from provider inference so hard rules are not prompt-only controls.

