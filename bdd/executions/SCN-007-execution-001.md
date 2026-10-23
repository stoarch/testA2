# SCN-007 Execution 001

- Date: 2026-10-24
- Requirement: [REQ-005](../../doc/requirements/functional-requirements.md#req-005-draft-a-grounded-reply-with-citations)
- Scenario: [SCN-007](../scenarios/SCN-007.md)
- Result: Passed
- Scope: Require each numeric processing/completion duration in a draft to occur in a cited passage

## Red

Unit, persisted-snapshot integration, and Behave expectations were added before the evidence validator existed.

- Unit and integration collection both failed with `ModuleNotFoundError: support_copilot.evidence_validation`.
- SCN-007 completed its Given step, then errored in When because the validator was absent.

## Green

Added deterministic duration extraction, exact claim-to-cited-passage comparison, and a typed failure for unsupported timeline claims. The synthetic account-opening passage now contains a directly cited `48 hours` duration and has a recomputed SHA-256 content hash.

- Timeline-validation unit result: `2 passed`
- Snapshot integration result: `1 passed`
- BDD result: `1 scenario passed`, `3 steps passed`

## Refactor

Kept duration extraction private and deduplicated normalized claims in first-seen order, leaving the public boundary as one validation function.

- Pytest regression: `14 passed`
- BDD regression: SCN-001 through SCN-007 passed; `23 steps passed`
- Ruff: all checks passed
- Gherkin validation: `5 feature files`, `28 unique scenarios`, Markdown parity confirmed
- Architecture documentation validation: passed

## Limits of this increment

- Validation covers explicit numeric durations expressed in minutes, hours, days, weeks, or months.
- It verifies exact duration presence, not full semantic equivalence between a draft sentence and evidence.
- Relative or qualitative phrases such as `instant`, `soon`, dates, ranges, and spelled-out numbers are not timeline claims in this slice.
- Unsupported-claim routing and user-facing abstention remain SCN-008, SCN-009, and SCN-028 work.
- Timeline validation is not yet wired into the CLI result contract.
