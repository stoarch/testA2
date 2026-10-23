# Deployment View

This view separates the timeboxed local prototype from the Phase 2 production shape. It does not select a cloud or LLM vendor.

```mermaid
flowchart LR
    subgraph phase1["Phase 1 · Local Prototype"]
        ui["CLI or Simple Web UI"]
        app["Python Co-pilot Process"]
        snapshot[("Four-page KB Snapshot")]
        eval[("Fixtures and Evaluation Results")]
        ui --> app
        app --> snapshot
        app --> eval
    end

    provider["Configured LLM Provider"]
    pages["Public Valetax Pages"]
    app --> provider
    pages --> snapshot

    subgraph phase2["Phase 2 · Scale Design"]
        gateway["Authenticated Agent Interface"]
        queue["Work Queue"]
        workers["Stateless Processing Workers"]
        index[("Versioned Search Index")]
        audit[("Metrics / Audit Store")]
        review["Human Review Queue"]
        gateway --> queue --> workers
        workers --> index
        workers --> audit
        workers --> review
    end

    pages --> index
    workers --> provider
```

Production data controls, SLA, peak factor, retention, and provider terms remain explicit pre-production decisions.

