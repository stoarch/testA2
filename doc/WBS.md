# Work Breakdown Structure

This WBS implements the [support-ticket co-pilot definition](task-desc.md). The delivery constraint is a 3–5 hour prototype followed by a scale-up design for approximately 10,000 tickets per month.

## Status values

- `Not started`
- `In progress`
- `Blocked`
- `Done`
- `Deferred`

## Work packages

| ID | Work package | Deliverable / acceptance criterion | Depends on | Status |
|---|---|---|---|---|
| WBS-001 | Establish project and documentation baseline | Execute [WBS-001](tasks/WBS-001.md): source brief, ADR, Mermaid, WBS, dashboard, and task structures exist and cross-link correctly | — | Done |
| WBS-002 | Define and approve co-pilot requirements | Execute [WBS-002](tasks/WBS-002.md): actors, behavior, hard safety rules, KB limits, BDD scenarios, quality limits, business-case requirements, and verification mapping | WBS-001 | Done |
| WBS-003 | Resolve architecture decisions | Options and consequences are recorded for consequential technical choices; accepted ADRs reference relevant requirements | WBS-002 | Not started |
| WBS-004 | Refine system models | Context, component, sequence, and deployment diagrams contain approved elements and trace to requirements/ADRs | WBS-002, WBS-003 | Not started |
| WBS-005 | Plan implementation | Implementation tasks have owners, estimates, dependencies, and testable completion criteria | WBS-002, WBS-003 | Not started |
| WBS-006 | Prepare engineering foundation | Repository layout, build, configuration, quality checks, and local developer workflow are documented and reproducible | WBS-005 | Not started |
| WBS-007 | Implement domain increments | Each prioritized requirement is delivered in a small, independently verifiable increment | WBS-005, WBS-006 | Not started |
| WBS-008 | Verify quality attributes | Functional tests and applicable security, performance, reliability, accessibility, and recovery checks pass | WBS-007 | Not started |
| WBS-009 | Prepare release and operations | Deployment, rollback, monitoring, support, data migration, and runbook needs are satisfied | WBS-006, WBS-008 | Not started |
| WBS-010 | Release and validate outcomes | Release is completed, acceptance criteria pass, and follow-up work is recorded | WBS-009 | Not started |

## WBS-002 requirements checklist

Latest execution: [`WBS-002 execution 002`](tasks/WBS-002-execution-002.md). The [first execution](tasks/WBS-002-execution-001.md) is retained as historical evidence from before the source brief was populated.

- [x] Problem statement and measurable outcome
- [x] Stakeholders and system actors
- [x] In-scope and out-of-scope behavior
- [x] Functional requirements with BDD acceptance examples
- [x] Hard safety rules and mandatory human-review behavior
- [x] Knowledge-base sources, gaps, overlaps, and inconsistencies
- [x] Data inputs, outputs, and audit fields
- [x] Quality attributes and sourced measurable limits
- [x] Phase 1 prototype and Phase 2 scale constraints
- [x] Business-case calculation requirements
- [x] Assumptions, dependencies, risks, and open questions

## Definition of ready for implementation

An implementation item is ready when it has an owner, related requirement IDs, bounded scope, explicit dependencies, BDD acceptance scenarios, a TDD unit/component test plan, identified E2E coverage, and no unresolved blocking decision.

## Definition of done

A work item is done when its BDD scenarios are satisfied, TDD-created unit/component tests pass, applicable E2E journeys pass, non-functional limits are verified, documentation and diagrams reflect the delivered behavior, and remaining risks or follow-ups are recorded in the dashboard.

