# Project Documentation

This directory is the project planning and architecture source of truth.

## Contents

- [Task description](task-desc.md) — product and delivery requirements.
- [Work breakdown structure](WBS.md) — scoped work packages, dependencies, and acceptance criteria.
- [Architecture decisions](adr/README.md) — durable technical decisions and their consequences.
- [UML models](uml/README.md) — system context, components, runtime flow, and deployment views.
- [Progress dashboard](../DASHBOARD/PROGRESS.md) — current delivery state, risks, decisions, and next actions.

## Working agreement

1. Update `task-desc.md` before committing to domain-specific design.
2. Assign each requirement a stable ID (`REQ-###`) and reference it from WBS items, ADRs, and diagrams.
3. Record consequential or difficult-to-reverse decisions as ADRs.
4. Update the dashboard when a work item changes state or a blocker appears.
5. Keep Mermaid diagrams in Markdown so they render with the surrounding explanation and remain reviewable in version control.

