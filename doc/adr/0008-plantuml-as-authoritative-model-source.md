# ADR-0008: PlantUML as the authoritative model source

- Status: Accepted
- Date: 2026-10-23
- Owners: Project team
- Related requirements: Architecture documentation baseline
- Related work: `WBS-003`, `WBS-004`
- Supersedes: ADR-0002

## Context

ADR-0002 selected Mermaid-in-Markdown, but the governing master prompt now explicitly requires source-controlled PlantUML component, class, sequence, and activity/state diagrams with trust boundaries and module responsibilities.

## Options considered

### Option A: PlantUML source plus Markdown companion pages

- Benefits: satisfies the required UML notation while preserving readable context, links, and update rules.
- Costs and risks: previewing diagrams requires a PlantUML renderer.

### Option B: Continue Mermaid only

- Benefits: convenient rendering in many repository viewers.
- Costs and risks: contradicts the current governing specification.

### Option C: Maintain equivalent Mermaid and PlantUML diagrams

- Benefits: broad preview support.
- Costs and risks: duplicate sources inevitably drift.

## Decision

Store authoritative `.puml` sources in `doc/uml/`. Keep Markdown companion pages for purpose, assumptions, traceability, and links to the source. PlantUML names and responsibilities must match implemented modules; diagrams showing planned elements label them as planned.

## Consequences

### Positive

- The required UML views are explicit and source controlled.
- Trust boundaries and branch behavior can be modeled precisely.
- Markdown remains the navigation layer.

### Negative

- Diagram rendering becomes an explicit tooling step.
- Existing Mermaid diagrams must be retired or converted.

### Follow-up work

- [x] Add component, class, sequence, and activity PlantUML sources.
- [ ] Add automated PlantUML syntax rendering to CI.

## Validation

Each required view has a `.puml` file linked from the UML index, and planned elements are distinguishable from implemented code.
