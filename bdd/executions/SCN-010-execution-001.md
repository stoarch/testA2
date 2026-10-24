# SCN-010 Execution 001

- Date: 2026-10-24
- Requirement: [REQ-007](../../doc/requirements/functional-requirements.md#req-007-refuse-trading-advice)
- Scenario: [SCN-010](../scenarios/SCN-010.md)
- Result: Passed
- Scope: Refuse a direct currency-pair buy recommendation before retrieval or provider use

## Red

Unit, ticket-contract integration, and Behave expectations were added before the safety policy module existed.

- Unit and integration collection both failed with `ModuleNotFoundError: support_copilot.safety`.
- SCN-010 completed its Given step, then errored in When because the policy gate was absent.

## Green

Added a deterministic direct currency-pair recommendation detector, frozen Pydantic refusal result, `trading_advice` safety flag/review reason, and a fixed polite refusal containing no asset recommendation, signal, or target.

- Safety unit result: `2 passed`
- Ticket-to-policy integration result: `1 passed`
- BDD result: `1 scenario passed`, `5 steps passed`

## Refactor

Consolidated the detector's mandatory recommendation-language and currency-pair checks into an explicit required-pattern predicate. The operational `buy a replacement security key` negative control remains green.

- Pytest regression: `23 passed`
- BDD regression: SCN-001 through SCN-010 passed; `37 steps passed`
- Ruff: all checks passed
- Gherkin validation: `5 feature files`, `28 unique scenarios`, Markdown parity confirmed
- Architecture documentation validation: passed

## Limits of this increment

- Detection is deliberately bounded to direct `should I` or `recommend ... buy/sell` language paired with a three-letter currency pair such as `EUR/USD`.
- Indirect phrasing, currency names without pair notation, signals, price targets, and obfuscated advice requests remain later safety coverage.
- Leverage recommendation handling remains SCN-011.
- The policy result is not yet connected to the CLI or a general application orchestrator.
