# Work Breakdown Structure

This WBS implements the governing [master prompt](master-prompt.md), with the original [support-ticket brief](task-desc.md) retained as product context. The delivery constraint is a 3-5 hour MVP followed by a scale-up design for approximately 10,000 tickets per month.

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
| WBS-003 | Resolve architecture decisions | Five master-prompt decision areas are accepted and traced ([execution](tasks/WBS-003-execution-001.md)) | WBS-002 | Done |
| WBS-004 | Refine system models | PlantUML component, class, sequence, activity, context, and deployment views identify trust boundaries and implementation state ([execution](tasks/WBS-004-execution-001.md)) | WBS-002, WBS-003 | Done |
| WBS-005 | Plan implementation | Implementation tasks have owners, estimates, dependencies, and testable completion criteria ([execution](tasks/WBS-005-execution-001.md)) | WBS-002, WBS-003 | Done |
| WBS-006 | Prepare engineering foundation | Repository layout, build, configuration, quality checks, and local developer workflow are documented and reproducible ([execution](tasks/WBS-006-execution-001.md)) | WBS-005 | Done |
| WBS-007 | Implement domain increments | Each prioritized requirement is delivered in a small, independently verifiable increment | WBS-005, WBS-006 | In progress |
| WBS-008 | Verify quality attributes | Functional tests and applicable security, performance, reliability, accessibility, and recovery checks pass | WBS-007 | In progress |
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

## Ticket intake and classification increments

- [x] **WBS-007.001 / SCN-001** - preserve ticket identity; unit and tagged BDD tests pass ([execution evidence](../bdd/executions/SCN-001-execution-001.md))
- [x] **WBS-007.002 / SCN-002** - classify a supported withdrawal topic; unit and tagged BDD tests pass ([execution evidence](../bdd/executions/SCN-002-execution-001.md))
- [x] **WBS-007.003 / SCN-003** - preserve an unsupported topic; unit and tagged BDD tests pass ([execution evidence](../bdd/executions/SCN-003-execution-001.md))
- [x] **WBS-007.004 / SCN-004** - return every required classification field through Pydantic and CLI boundaries ([execution evidence](../bdd/executions/SCN-004-execution-001.md))

## Grounded retrieval and drafting increments

- [x] **WBS-007.005 / SCN-005** - persist a synthetic KB snapshot and retrieve only allowlisted passages with provenance ([execution evidence](../bdd/executions/SCN-005-execution-001.md))
- [x] **WBS-007.006 / SCN-006** - draft an extractive answer supported by retrieved deposit evidence ([execution evidence](../bdd/executions/SCN-006-execution-001.md))
- [ ] **WBS-007.007 / SCN-007** - validate that timeline claims have exact cited support

WBS-007 remains in progress until the prioritized domain increments are complete. WBS-008 is also in progress because functional verification has begun, while E2E and non-functional checks remain outstanding.

## Master-prompt delivery checklist

- [x] Five required architecture decision areas documented
- [x] Authoritative PlantUML component, class, sequence, and activity views
- [x] Trust boundaries and implemented/planned distinctions documented
- [x] Missing master-prompt BDD cases specified (28 total scenarios)
- [x] Pydantic classification contracts and real CLI
- [x] Persisted synthetic KB snapshot loading, hashing, retrieval, and provenance
- [ ] Live KB snapshot fetching and refresh
- [ ] Deterministic compliance gates and human routing
- [ ] Provider abstraction and deterministic offline adapter
- [ ] Integration and subprocess E2E tests
- [ ] At least 30 synthetic evaluation tickets and metrics
- [ ] Measured one-page business case and four-outcome demo
- [x] CI lint/test/document-validation gate
- [ ] PlantUML rendering in CI

## Definition of ready for implementation

An implementation item is ready when it has an owner, related requirement IDs, bounded scope, explicit dependencies, BDD acceptance scenarios, a TDD unit/component test plan, identified E2E coverage, and no unresolved blocking decision.

## Definition of done

A work item is done when its BDD scenarios are satisfied, TDD-created unit/component tests pass, applicable E2E journeys pass, non-functional limits are verified, documentation and diagrams reflect the delivered behavior, and remaining risks or follow-ups are recorded in the dashboard.

