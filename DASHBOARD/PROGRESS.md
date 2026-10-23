# Project Progress Dashboard

- Last updated: 2026-10-23
- Overall state: In progress - first two implementation scenarios are green
- Current phase: MVP implementation planning and incremental implementation
- Current task: [`WBS-005`](../doc/tasks/WBS-005.md) - Plan MVP implementation; next code slice is `WBS-007.003 / SCN-003`
- Completed work packages: WBS-001, WBS-002, WBS-003, WBS-004
- Latest architecture execution: [`WBS-004 execution 001`](../doc/tasks/WBS-004-execution-001.md)
- Latest code execution: [`SCN-002 execution 001`](../bdd/executions/SCN-002-execution-001.md)
- Source of truth: [`doc/master-prompt.md`](../doc/master-prompt.md)
- Work plan: [`doc/WBS.md`](../doc/WBS.md)
- Architecture decisions: [`doc/adr/README.md`](../doc/adr/README.md)
- System models: [`doc/uml/README.md`](../doc/uml/README.md)
- Requirements: [`doc/requirements/README.md`](../doc/requirements/README.md)

## Snapshot

| Category | State | Evidence / next action |
|---|---|---|
| Documentation baseline | Done | WBS-001 execution passed |
| Requirements | Updated | REQ-001-021 and REQ-101-115 now cover the master prompt; approval refresh remains |
| Architecture decisions | Done | WBS-003 passed; ADR-0003 through ADR-0008 cover all required decision areas |
| UML models | Done for baseline | WBS-004 passed; six authoritative PlantUML views include trust boundaries and implementation state |
| Delivery plan | In progress | WBS-005 opened with ten ordered MVP increments |
| Implementation | In progress | [x] SCN-001 identity; [x] SCN-002 withdrawal classification; SCN-003 is next |
| Verification | In progress | Unit: 2 passed; selected BDD: 2 scenarios / 6 steps passed; Gherkin parity target: 28 scenarios |

## Immediate next actions

| Priority | Action | Owner | Target | Related item |
|---|---|---|---|---|
| P0 | Complete WBS-005 estimates, ownership, and slice-level verification details | TBD | TBD | WBS-005 |
| P0 | Implement SCN-003 unsupported-topic fallback through red-green-refactor | TBD | TBD | WBS-007.003 |
| P0 | Build at least 30 labeled routine/risky/conflict/multilingual/adversarial fixtures | TBD | TBD | WBS-005 / WBS-008 / REQ-114 |
| P1 | Implement Pydantic contracts and the real CLI | TBD | TBD | WBS-006 / ADR-0004 |
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
| RISK-005 | Prompt injection from tickets or retrieved content | High | Critical | Untrusted-content boundaries, deterministic gates, adversarial evaluation | Compliance / technical lead |
| RISK-006 | Synthetic fixtures are confused with live evidence | Medium | High | Mandatory execution-mode and provenance labels | Technical lead |

## Decision backlog

Create an ADR only when the corresponding decision is ready for explicit comparison and approval.

| Topic | Trigger | State |
|---|---|---|
| Phase 1 orchestration and provider boundary | ADR-0004 / ADR-0007 | Decided |
| Retrieval, snapshot, and citation validation | ADR-0005 | Decided |
| Safety enforcement and human routing | ADR-0006 | Decided |
| Evaluation configuration and metrics | ADR-0003 | Decided |
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
| 2026-10-23 | Completed WBS-007.001 / SCN-001 through red-green-refactor; unit and tagged Behave execution pass, and Gherkin parity remains valid. |
| 2026-10-23 | Completed WBS-007.002 / SCN-002 through red-green-refactor; withdrawal classification and the SCN-001 regression both pass. |
| 2026-10-23 | Reconciled architecture with the master prompt; completed WBS-003 and WBS-004, added required ADRs and PlantUML views, expanded safety requirements/BDD, and opened WBS-005. |

## Reporting rules

- Update this file whenever a blocker, top risk, milestone, or work-package status changes.
- Keep detailed task decomposition in `doc/WBS.md`; keep this page concise and current.
- Close blockers and risks with an outcome note instead of deleting their history.

