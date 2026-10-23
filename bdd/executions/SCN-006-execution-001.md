# SCN-006 Execution 001

- Date: 2026-10-24
- Requirement: [REQ-005](../../doc/requirements/functional-requirements.md#req-005-draft-a-grounded-reply-with-citations)
- Scenario: [SCN-006](../scenarios/SCN-006.md)
- Result: Passed
- Scope: Produce an extractive deposit draft from approved evidence with a structured citation

## Red

Unit, retrieval-to-draft integration, and Behave expectations were added before the drafting module existed.

- Unit collection failed with `ModuleNotFoundError: support_copilot.drafting`.
- Integration collection failed with the same missing module.
- SCN-006 passed its evidence Given step, then errored in When because the drafting module was absent.

## Green

Added a frozen Pydantic draft/citation contract, deterministic deposit-evidence selection, extractive drafting, and a typed insufficient-evidence failure.

- Drafting unit result: `2 passed`
- Retrieval-to-draft integration result: `1 passed`
- BDD result: `1 scenario passed`, `4 steps passed`

## Refactor

Extracted passage-to-citation conversion and supported-text extraction into explicit boundaries for later citation validation.

- Pytest regression: `11 passed`
- BDD regression: SCN-001 through SCN-006 passed; `20 steps passed`
- Ruff: all checks passed
- Gherkin validation: `5 feature files`, `28 unique scenarios`, Markdown parity confirmed

## Limits of this increment

- Drafting is extractive and supports only the synthetic deposit passage.
- The structured citation preserves provenance, but claim/citation validation—especially timeline validation—remains SCN-007 work.
- Insufficient evidence raises a typed error; user-facing abstention and human routing remain SCN-008/009 work.
- The draft is not yet integrated into the CLI result contract and cannot be sent to a customer.
