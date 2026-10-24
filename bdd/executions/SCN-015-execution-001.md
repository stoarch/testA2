# SCN-015 Execution 001

- Date: 2026-10-24
- Requirement: [REQ-009](../../doc/requirements/functional-requirements.md#req-009-route-required-cases-to-a-human)
- Scenario: [SCN-015](../scenarios/SCN-015.md)
- Result: Passed
- Scope: Route classification or grounding results strictly below an explicit configured confidence threshold

## Red

Unit, serialized integration-contract, and Behave expectations were added before the routing contract existed.

- Pytest collection errored for both new test modules with `ModuleNotFoundError: support_copilot.routing`.
- SCN-015 errored at its first Given step for the same missing module.

## Green

Added validated immutable confidence-assessment and low-confidence route-result contracts, the canonical `low_confidence` review reason, and deterministic routing for values strictly below the configured threshold.

- Focused pytest result: `4 passed`
- BDD result: `1 scenario passed`, `4 steps passed`

## Refactor

Reused the shared frozen `ContractModel` and named the threshold comparison as `is_below_threshold()` so the inclusive/exclusive boundary is explicit in the domain model.

- Pytest regression: `38 passed`
- BDD regression: SCN-001 through SCN-015 passed; `59 steps passed`
- Ruff: all checks passed
- Gherkin validation: `5 feature files`, `28 unique scenarios`, Markdown parity confirmed
- Architecture documentation validation: passed

## Limits of this increment

- Confidence values are supplied by a caller; provider calibration and evaluation-set threshold tuning are not implemented.
- The threshold is recorded in the typed route result but is not yet part of a named configuration object.
- The route remains an in-process typed result; no queue, persistence adapter, or CLI review journey exists yet.
