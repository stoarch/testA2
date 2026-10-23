# Deployment View

This view captures the categories of runtime nodes that may be needed. It does not select a hosting platform or protocol.

```mermaid
flowchart LR
    subgraph userEnv["User Environment (TBD)"]
        client["Client<br/>(TBD)"]
    end

    subgraph appEnv["Application Environment (TBD)"]
        app["Application Artifact<br/>(TBD)"]
    end

    subgraph dataEnv["Data Environment (TBD)"]
        database[("Primary Data Store<br/>(TBD)")]
    end

    external["External Platform<br/>(TBD)"]

    client -->|"Secure protocol TBD"| app
    app -->|"Data protocol TBD"| database
    app -->|"Integration protocol TBD"| external
```

Refinement trigger: TASK-001 defines availability, scale, security, data, environment, observability, backup, and recovery constraints.

