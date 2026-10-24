# SCN-020 Execution 001

- Date: 2026-10-25
- Requirement: [REQ-014](../../doc/requirements/functional-requirements.md#req-014-produce-the-one-page-business-case)
- Scenario: [SCN-020](../scenarios/SCN-020.md)
- Result: Passed
- Scope: Compare deterministic, guarded-LLM, and hybrid configurations under low/base/high assumptions at 10,000 tickets per month and enforce the evidence-based recommendation gate

## Red

Formula, integration, subprocess E2E, and Behave expectations were added before the business-case domain or CLI mode existed.

- Pytest collection failed with `ModuleNotFoundError: support_copilot.business_case`.
- SCN-020 reached the real CLI, which rejected `--business-case-input` and `--business-case-format`.

## Green

Added typed staffing/cost assumptions, three-configuration low/base/high projections, labor-value and run-cost formulas, review-workload disclosure, break-even calculations, an evidence gate, JSON/Markdown CLI output, and the generated one-page report.

- Focused pytest result: `7 passed`
- BDD result: `1 scenario passed`, `4 steps passed`

## Refactor

Separated projection calculation, evidence qualification, decision selection, and Markdown rendering. Schema literals prevent projections from being relabeled as measured results.

- Pytest regression: `58 passed`
- BDD regression: SCN-001 through SCN-020 passed; `77 steps passed`
- Ruff: all checks passed
- Gherkin validation: `5 feature files`, `28 unique scenarios`, Markdown parity confirmed
- Architecture documentation validation: passed

## Findings

At 10,000 tickets/month, the modeled base cases produce:

- Configuration A: USD 1,400 monthly run cost, USD 5,100 net value, 14.0% break-even acceptance.
- Configuration B: USD 2,800 monthly run cost, USD 6,137.50 net value, 20.4% break-even acceptance.
- Configuration C: USD 2,060 monthly run cost, USD 8,830 net value, 13.6% break-even acceptance.

The decision is **no-go** despite positive modeled net values. Configuration A has only four offline synthetic evaluation cases, below the 30-case gate; configurations B and C have no measured quality or safety results.

## Limits of this increment

- Eligibility, acceptance, handling time, labor rate, provider cost, infrastructure, and maintenance values are explicit estimates, not measured operating results.
- Configuration A quality evidence comes from the bounded offline fixture; configurations B and C are modeled only.
- The report does not justify production deployment and leaves OQ-005 open pending real operating inputs.
