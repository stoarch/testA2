# UML Models

PlantUML is the authoritative diagram format under [ADR-0008](../adr/0008-plantuml-as-authoritative-model-source.md). Markdown companion pages describe purpose, traceability, and synchronization rules without duplicating diagram source.

## Required views

| View | PlantUML source | Purpose | State |
|---|---|---|---|
| Component | [component-overview.puml](component-overview.puml) | Modules, dependencies, trust boundaries, and implemented/planned status | Baseline complete |
| Class | [domain-class.puml](domain-class.puml) | Domain contracts and provider ports | Baseline complete |
| Sequence | [processing-sequence.puml](processing-sequence.puml) | Normal, abstention, refusal, escalation, and failure branches | Baseline complete |
| Activity | [processing-activity.puml](processing-activity.puml) | Deterministic processing and safe-stop decisions | Baseline complete |

## Supporting views

| View | PlantUML source | Purpose |
|---|---|---|
| System context | [system-context.puml](system-context.puml) | Actors, external systems, and agent-assist boundary |
| Deployment | [deployment.puml](deployment.puml) | Phase 1 runtime and planned Phase 2 topology |

## Companion documentation

- [System context](system-context.md)
- [Component overview](component-overview.md)
- [Domain class model](domain-class.md)
- [Processing sequence](primary-flow.md)
- [Processing activity](processing-activity.md)
- [Deployment](deployment.md)

## Synchronization rules

- Mark elements `implemented`, `partially implemented`, `planned`, or `optional planned` when the distinction matters.
- Treat ticket text, retrieved pages, and live providers as untrusted/external trust boundaries.
- Keep the processing order aligned with ADR-0004 and executable application code.
- Update the class view whenever Pydantic/domain contracts change.
- Render all `.puml` files during CI once PlantUML tooling is added under WBS-006.
