# BDD Acceptance Scenarios

Each scenario lives in its own Markdown file so it can be reviewed, implemented, and updated independently. Executable Gherkin files are generated under `features/` and validated with the Gherkin parser and Behave.

## Executable feature files

- [`ticket_intake_and_classification.feature`](features/ticket_intake_and_classification.feature)
- [`grounded_response_drafting.feature`](features/grounded_response_drafting.feature)
- [`regulated_content_boundaries.feature`](features/regulated_content_boundaries.feature)
- [`human_review_conflicts_and_failures.feature`](features/human_review_conflicts_and_failures.feature)
- [`prototype_evaluation_and_decision_support.feature`](features/prototype_evaluation_and_decision_support.feature)

## Validation

Validate Gherkin syntax, unique scenario IDs, and Markdown/feature parity:

```text
python bdd/validate_gherkin.py
```

Run the implemented increments by scenario name:

```text
behave bdd/features --name=SCN-001 --name=SCN-002 --name=SCN-003 --name=SCN-004 --name=SCN-005 --name=SCN-006 --name=SCN-007 --name=SCN-008 --name=SCN-009 --name=SCN-010 --name=SCN-011 --name=SCN-012 --name=SCN-013 --name=SCN-014
```

SCN-001 through SCN-014 are implemented and passing. Other scenarios retain undefined steps until their own red-green-refactor increments begin, so an unfiltered full-suite run is not yet expected to pass. Execution evidence is stored under [`executions/`](executions/README.md).

## Ticket intake and classification

| Scenario | Requirement | Behavior |
|---|---|---|
| [SCN-001](scenarios/SCN-001.md) | REQ-001 | Preserve ticket identity |
| [SCN-002](scenarios/SCN-002.md) | REQ-002 | Classify a supported topic |
| [SCN-003](scenarios/SCN-003.md) | REQ-002 | Preserve an unsupported topic |
| [SCN-004](scenarios/SCN-004.md) | REQ-003 | Return all required classifications |
| [SCN-026](scenarios/SCN-026.md) | REQ-018 | Route an unsupported language |
| [SCN-027](scenarios/SCN-027.md) | REQ-018 | Reject invalid ticket input |

## Grounded response drafting

| Scenario | Requirement | Behavior |
|---|---|---|
| [SCN-005](scenarios/SCN-005.md) | REQ-004 | Retrieve only approved sources |
| [SCN-006](scenarios/SCN-006.md) | REQ-005 | Draft a supported answer |
| [SCN-007](scenarios/SCN-007.md) | REQ-005 | Cite a timeline claim |
| [SCN-008](scenarios/SCN-008.md) | REQ-006 | Abstain on an uncovered fee |
| [SCN-009](scenarios/SCN-009.md) | REQ-006 | Abstain on missing verification detail |
| [SCN-024](scenarios/SCN-024.md) | REQ-019 | Resist retrieved-content prompt injection |
| [SCN-028](scenarios/SCN-028.md) | REQ-006 | Abstain on an uncovered timeline |

## Regulated-content boundaries

| Scenario | Requirement | Behavior |
|---|---|---|
| [SCN-010](scenarios/SCN-010.md) | REQ-007 | Decline a buy recommendation |
| [SCN-011](scenarios/SCN-011.md) | REQ-007 | Do not recommend leverage |
| [SCN-012](scenarios/SCN-012.md) | REQ-008 | Route a KYC outcome request |
| [SCN-013](scenarios/SCN-013.md) | REQ-008 | Route a complaint decision |
| [SCN-022](scenarios/SCN-022.md) | REQ-007/021 | Route a mixed trading and support request |
| [SCN-023](scenarios/SCN-023.md) | REQ-019 | Resist ticket prompt injection |

## Human review, conflicts, and failures

| Scenario | Requirement | Behavior |
|---|---|---|
| [SCN-014](scenarios/SCN-014.md) | REQ-009 | Route an abstention |
| [SCN-015](scenarios/SCN-015.md) | REQ-009 | Route a configured low-confidence result |
| [SCN-016](scenarios/SCN-016.md) | REQ-010 | Produce auditable output |
| [SCN-017](scenarios/SCN-017.md) | REQ-011 | Do not silently reconcile source conflicts |
| [SCN-021](scenarios/SCN-021.md) | REQ-016 | Fail safely when retrieval is unavailable |
| [SCN-025](scenarios/SCN-025.md) | REQ-016 | Fail safely on provider outage |

## Prototype evaluation and decision support

| Scenario | Requirement | Behavior |
|---|---|---|
| [SCN-018](scenarios/SCN-018.md) | REQ-012 | Process a ticket through the minimal interface |
| [SCN-019](scenarios/SCN-019.md) | REQ-013 | Report evaluation results |
| [SCN-020](scenarios/SCN-020.md) | REQ-014 | Compare configurations at target volume |

