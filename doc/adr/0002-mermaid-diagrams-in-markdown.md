# ADR-0002: Mermaid diagrams in Markdown

- Status: Accepted
- Date: 2026-10-23
- Owners: Project team
- Related requirements: Project documentation baseline
- Related work: `WBS-001`, `WBS-004`
- Supersedes: ADR-0001 modeling-format decision

## Context

The initial documentation baseline stored UML-style models as PlantUML source files. The project now requires diagrams to live in Markdown and use Mermaid so each view can be read together with its purpose, assumptions, and update rules.

## Options considered

### Option A: Mermaid fenced blocks in Markdown

- Benefits: diagrams and explanation stay together; many repository viewers render Mermaid directly; text remains reviewable.
- Costs and risks: Mermaid support and UML notation vary between renderers.

### Option B: Standalone PlantUML files

- Benefits: broad UML feature set and mature rendering tools.
- Costs and risks: requires separate rendering and separates model context from the diagram.

## Decision

Store architecture diagrams as Markdown files under `doc/uml/`, with one Mermaid fenced block per primary view. Use flowcharts for context, component, and deployment views, and a Mermaid sequence diagram for runtime interaction.

## Consequences

### Positive

- Diagrams render alongside their descriptions in compatible Markdown viewers.
- Diagram changes and their rationale can be reviewed in one file.
- No project-specific diagram-rendering command is required for ordinary review.

### Negative

- Renderer differences may require conservative Mermaid syntax.
- Strict UML semantics are secondary to clear communication.

### Follow-up work

- [ ] Replace placeholder nodes when TASK-001 is approved (`WBS-004`).

## Validation

All diagram Markdown files must contain a Mermaid block, use consistent element names, and link to relevant requirements or decisions when domain content is added.
