# Project Documentation

This directory is the project planning and architecture source of truth. The governing specification is [the master prompt](master-prompt.md); `task-desc.md` is the original product brief.

## Contents

- [Task description](task-desc.md) — product and delivery requirements.
- [Master-prompt traceability](master-prompt-traceability.md) — deliverable coverage and honest implementation state.
- [Requirements baseline](requirements/README.md) — source-backed scope, requirements, BDD scenarios, KB assessment, verification, and business-case rules.
- [Work breakdown structure](WBS.md) — scoped work packages, dependencies, and acceptance criteria.
- [Task specifications](tasks/README.md) — execution prompts, boundaries, and verification strategy for individual WBS items.
- [Architecture decisions](adr/README.md) — durable technical decisions and their consequences.
- [UML models](uml/README.md) — system context, components, runtime flow, and deployment views.
- [Progress dashboard](../DASHBOARD/PROGRESS.md) — current delivery state, risks, decisions, and next actions.
- [Phase 2 scaling plan](phase-2-scaling.md) — queueing, retries, versioning, approval, observability, security, and scale triggers.
- [Known limitations](known-limitations.md) and [technical walkthrough](walkthrough.md).

## Working agreement

1. Update `task-desc.md` before committing to domain-specific design.
2. Assign each requirement a stable ID (`REQ-###`) and reference it from WBS items, ADRs, and diagrams.
3. Record consequential or difficult-to-reverse decisions as ADRs.
4. Update the dashboard when a work item changes state or a blocker appears.
5. Keep PlantUML sources authoritative and their Markdown companion pages synchronized under ADR-0008.
6. Specify behavior with BDD, implement units with TDD, and verify critical journeys with E2E tests.

