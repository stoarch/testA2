# ADR-0001: Documentation and modeling conventions

- Status: Superseded by ADR-0002
- Date: 2026-10-23
- Owners: Project team
- Related requirements: Project documentation baseline
- Related work: `WBS-001`
- Supersedes: None

## Context

The project needs architecture decisions, system models, a work breakdown, and a compact progress view before implementation begins. The task description is currently empty, so the baseline must be useful without asserting domain behavior that has not been approved.

## Options considered

### Option A: Markdown and PlantUML stored with the project

- Benefits: reviewable diffs, stable links, low tooling lock-in, and diagrams generated from text.
- Costs and risks: rendering requires PlantUML-compatible tooling and diagrams can drift without review discipline.

### Option B: External documentation and diagram tools

- Benefits: rich visual editing and collaboration features.
- Costs and risks: access dependencies, weaker version traceability, and links may become stale.

## Decision

Store ADRs, planning documents, and PlantUML sources under `doc/`. Keep the delivery summary in `DASHBOARD/PROGRESS.md`. Use stable `REQ-###` and `WBS-###` identifiers to trace requirements through decisions, models, and implementation work.

## Consequences

### Positive

- Documentation changes can be reviewed alongside implementation changes.
- Architecture views can be regenerated consistently.
- Unknown requirements remain visible as `TBD` instead of becoming implicit assumptions.

### Negative

- Contributors need a PlantUML renderer for diagram previews.
- The team must update cross-references when scope changes.

### Follow-up work

- [ ] Populate `doc/task-desc.md` and assign requirement IDs (`WBS-002`).
- [ ] Replace diagram placeholders with approved system elements (`WBS-004`).

## Validation

The baseline is effective when every approved requirement maps to at least one WBS item and relevant architecture decisions and diagrams can be located from the documentation index.

