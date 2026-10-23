# Project Progress Dashboard

- Last updated: 2026-10-23
- Overall state: In progress — WBS-001 and WBS-002 complete
- Current phase: Architecture decisions and implementation planning
- Current task: `WBS-003` — Resolve architecture decisions
- Completed task specs: [`WBS-001`](../doc/tasks/WBS-001.md), [`WBS-002`](../doc/tasks/WBS-002.md)
- Latest execution: [`WBS-002 execution 002`](../doc/tasks/WBS-002-execution-002.md)
- Source of truth: [`doc/task-desc.md`](../doc/task-desc.md)
- Work plan: [`doc/WBS.md`](../doc/WBS.md)
- Architecture decisions: [`doc/adr/README.md`](../doc/adr/README.md)
- System models: [`doc/uml/README.md`](../doc/uml/README.md)
- Requirements: [`doc/requirements/README.md`](../doc/requirements/README.md)

## Snapshot

| Category | State | Evidence / next action |
|---|---|---|
| Documentation baseline | Done | WBS-001 execution passed |
| Requirements | Done | WBS-002 execution 002 passed with REQ-001–016 and REQ-101–110 |
| Architecture decisions | In progress | Choose Phase 1 boundaries, provider adapter, retrieval, safety, and evaluation design |
| UML models | Done for baseline | Context, components, primary flow, and two-phase deployment aligned |
| Delivery plan | In progress | WBS-003 onward remains to be detailed |
| Implementation | Not started | Begins after definition-of-ready is met |
| Verification | Ready | BDD scenarios and verification matrix are defined |

## Immediate next actions

| Priority | Action | Owner | Target | Related item |
|---|---|---|---|---|
| P0 | Decide Phase 1 architecture and deterministic safety boundaries | TBD | TBD | WBS-003 |
| P0 | Select the smallest 3–5 hour implementation slice | TBD | TBD | WBS-005 |
| P0 | Build a labeled normal/gap/conflict/safety fixture set | TBD | TBD | WBS-005 / WBS-008 |
| P1 | Decide LLM/provider configuration and KB snapshot approach | TBD | TBD | WBS-003 |
| P1 | Populate business-case labor and pricing assumptions | TBD | TBD | REQ-014 / OQ-005 |

## Blockers

| ID | Blocker | Impact | Resolution | Owner | State |
|---|---|---|---|---|---|
| BLK-001 | Earlier source brief was empty | WBS-002 execution 001 stopped | Source brief populated; execution 002 passed | Project requester | Closed |

## Risks

| ID | Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|---|
| RISK-001 | Unsupported policy/timeline drafting | Medium | Critical | Claim/citation validation, abstention, human review | Technical lead |
| RISK-002 | Safety intent bypass | Medium | Critical | Adversarial BDD/evaluation set and deterministic routing | Compliance / technical lead |
| RISK-003 | Live KB drift and contradictions | High | High | Version snapshots and explicit conflict behavior | KB owner |
| RISK-004 | Business case overstates savings | Medium | High | Measured review/acceptance rates and sensitivity ranges | Support operations |

## Decision backlog

Create an ADR only when the corresponding decision is ready for explicit comparison and approval.

| Topic | Trigger | State |
|---|---|---|
| Phase 1 orchestration and provider boundary | Requirements approved | Ready |
| Retrieval, snapshot, and citation validation | KB assessment complete | Ready |
| Safety enforcement and human routing | Safety BDD scenarios complete | Ready |
| Evaluation configuration and metrics | Verification matrix complete | Ready |
| Phase 2 data/privacy/operations | Production constraints resolved | Waiting |

## Recent updates

| Date | Update |
|---|---|
| 2026-10-23 | Created ADR framework, PlantUML views, WBS, and progress dashboard. |
| 2026-10-23 | Converted UML views to Mermaid-in-Markdown and detailed TASK-001 requirements discovery. |
| 2026-10-23 | Added the WBS-002 execution prompt, functional/non-functional limits, and BDD/TDD/E2E strategy. |
| 2026-10-23 | Executed WBS-002; stopped under mandatory conditions because all required domain inputs are missing. |
| 2026-10-23 | Source brief populated with the retail forex/CFD support co-pilot definition. |
| 2026-10-23 | Fixed and executed WBS-001 and WBS-002; requirements, KB assessment, BDD, verification, business case, and Mermaid views now align. |

## Reporting rules

- Update this file whenever a blocker, top risk, milestone, or work-package status changes.
- Keep detailed task decomposition in `doc/WBS.md`; keep this page concise and current.
- Close blockers and risks with an outcome note instead of deleting their history.

