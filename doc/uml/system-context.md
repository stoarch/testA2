# System Context

This view identifies external actors, the target-system boundary, and external dependencies. Names remain placeholders until TASK-001 is approved.

```mermaid
flowchart LR
    user["Primary User<br/>(TBD)"]
    system["Target System<br/>(TBD from task-desc.md)"]
    external["External Service<br/>(TBD)"]

    user -->|"Primary interaction<br/>TBD · REQ-###"| system
    system -->|"Integration<br/>TBD · REQ-###"| external
```

Boundary rule: replace placeholders only with approved actors, responsibilities, and dependencies from TASK-001.

