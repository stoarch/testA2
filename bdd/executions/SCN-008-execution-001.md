# SCN-008 Execution 001

- Date: 2026-10-24
- Requirement: [REQ-006](../../doc/requirements/functional-requirements.md#req-006-abstain-when-coverage-is-insufficient)
- Scenario: [SCN-008](../scenarios/SCN-008.md)
- Result: Passed
- Scope: Produce a typed, human-reviewed abstention when approved evidence does not state a requested fee

## Red

Unit, persisted-snapshot integration, and Behave expectations were added before the abstention module existed.

- Unit and integration collection both failed with `ModuleNotFoundError: support_copilot.abstention`.
- SCN-008 completed its Given step, then errored in When because the abstention boundary was absent.

## Green

Added a frozen Pydantic abstention contract, stable `insufficient_kb_coverage` review reason, conservative fee-amount detection, and a typed error that prevents an uncovered-fee result when evidence explicitly contains an amount.

- Abstention unit result: `2 passed`
- Snapshot integration result: `1 passed`
- BDD result: `1 scenario passed`, `5 steps passed`

## Refactor

Extracted explicit fee-amount detection into a named private predicate while preserving the public safe-result boundary.

- Pytest regression: `17 passed`
- BDD regression: SCN-001 through SCN-008 passed; `28 steps passed`
- Ruff: all checks passed
- Gherkin validation: `5 feature files`, `28 unique scenarios`, Markdown parity confirmed
- Architecture documentation validation: passed

## Limits of this increment

- Fee support detection covers currency-prefixed numeric amounts and percentages near the word `fee`.
- Currency codes, spelled-out amounts, ranges, and semantically equivalent charge language are not covered.
- A supported-fee drafting path is not implemented; the guard only prevents a false uncovered-fee abstention.
- The result is not yet integrated into the CLI or a general application orchestrator.
- Missing verification detail and uncovered timeline handling remain SCN-009 and SCN-028 work.
