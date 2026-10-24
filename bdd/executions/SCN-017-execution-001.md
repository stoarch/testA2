# SCN-017 Execution 001

- Date: 2026-10-24
- Requirement: [REQ-011](../../doc/requirements/functional-requirements.md#req-011-preserve-source-gaps-and-conflicts)
- Scenario: [SCN-017](../scenarios/SCN-017.md)
- Result: Passed
- Scope: Detect explicit conflicting duration claims for one requested detail, abstain, expose both sources, and require review

## Red

Unit, persisted retrieval-integration, and Behave expectations were added before the conflict detector existed.

- Pytest collection errored for both new test modules with `ModuleNotFoundError: support_copilot.conflicts`.
- SCN-017 completed its Given step, then errored at the When step for the same missing module.

## Green

Added deterministic same-detail duration comparison, the canonical `source_conflict` review reason, and a builder that reuses the typed abstention contract while converting every relevant retrieved passage into a complete citation.

- Focused pytest result: `4 passed`
- BDD result: `1 scenario passed`, `5 steps passed`

## Refactor

Extracted relevant claim collection so each matching passage is normalized and parsed once before conflict comparison.

- Pytest regression: `47 passed`
- BDD regression: SCN-001 through SCN-017 passed; `67 steps passed`
- Ruff: all checks passed
- Gherkin validation: `5 feature files`, `28 unique scenarios`, Markdown parity confirmed
- Architecture documentation validation: passed

## Limits of this increment

- Detection is intentionally limited to explicit numeric minute/hour/day/week duration claims containing the requested-detail phrase.
- General semantic contradictions, misleading nonnumeric wording, and source-authority ranking are not implemented.
- The conflict path is not yet exposed through the CLI orchestration journey.
