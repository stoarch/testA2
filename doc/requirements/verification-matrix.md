# Verification Matrix

| Requirement | BDD | Unit/component TDD | Contract/integration | E2E | Quality evidence |
|---|---|---|---|---|---|
| REQ-001 | [SCN-001](../../bdd/scenarios/SCN-001.md) ([passing execution](../../bdd/executions/SCN-001-execution-001.md)) | [Ticket identity unit test](../../tests/unit/test_ticket_processing.py) | UI/CLI adapter | Submit ticket | REQ-104 |
| REQ-002 | [SCN-002](../../bdd/scenarios/SCN-002.md), [SCN-003](../../bdd/scenarios/SCN-003.md) | Category classifier/parser | Model response schema | Classification journey | Labeled confusion matrix |
| REQ-003 | [SCN-004](../../bdd/scenarios/SCN-004.md) | Field validation | Model response schema | Classification journey | Per-field metrics |
| REQ-004 | [SCN-005](../../bdd/scenarios/SCN-005.md) | Approved-source filter | Retriever/index | Grounded-answer journey | Source allowlist audit |
| REQ-005 | [SCN-006](../../bdd/scenarios/SCN-006.md), [SCN-007](../../bdd/scenarios/SCN-007.md) | Claim/citation validator | Retriever + model | Grounded-answer journey | REQ-102/103 |
| REQ-006 | [SCN-008](../../bdd/scenarios/SCN-008.md), [SCN-009](../../bdd/scenarios/SCN-009.md) | Coverage/abstention gate | Retriever | Gap journey | Abstention precision/recall |
| REQ-007 | [SCN-010](../../bdd/scenarios/SCN-010.md), [SCN-011](../../bdd/scenarios/SCN-011.md) | Safety detector and output filter | Model guardrail | Trading-advice journey | REQ-101 |
| REQ-008 | [SCN-012](../../bdd/scenarios/SCN-012.md), [SCN-013](../../bdd/scenarios/SCN-013.md) | Sensitive-intent routing | Model guardrail | KYC/complaint journey | REQ-101 |
| REQ-009 | [SCN-014](../../bdd/scenarios/SCN-014.md), [SCN-015](../../bdd/scenarios/SCN-015.md) | Routing rules/reasons | Queue stub/adapter | Review-routing journey | Review-rate report |
| REQ-010 | [SCN-016](../../bdd/scenarios/SCN-016.md) | Result schema and metrics | Provider usage metadata | Agent-view journey | REQ-104/108 |
| REQ-011 | [SCN-017](../../bdd/scenarios/SCN-017.md) | Conflict detector | Retriever | Conflict journey | Conflict-case review |
| REQ-012 | [SCN-018](../../bdd/scenarios/SCN-018.md) | Interface presenter | Application service | CLI/web smoke test | Manual demo |
| REQ-013 | [SCN-019](../../bdd/scenarios/SCN-019.md) | Metric calculations | Provider/pricing inputs | Evaluation command | Reproducible report |
| REQ-014 | [SCN-020](../../bdd/scenarios/SCN-020.md) | Cost-model formulas | Pricing/config source | Report generation | Scenario/sensitivity review |
| REQ-015 | Design review | Ingestion/versioning units | Source fetch/index | KB update rehearsal | Maintainability review |
| REQ-016 | [SCN-021](../../bdd/scenarios/SCN-021.md) | Failure-path tests | Forced dependency failures | Safe-failure journey | Zero unsupported fallback drafts |

## Test order

1. Write BDD examples for observable behavior.
2. Implement each rule through red → green → refactor unit/component TDD.
3. Add provider/retrieval contract tests at external boundaries.
4. Keep E2E coverage focused on grounded answer, abstention, trading advice, complaint/KYC, conflict, safe failure, and business-case generation.

