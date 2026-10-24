# SCN-018 Execution 001

- Date: 2026-10-24
- Requirement: [REQ-012](../../doc/requirements/functional-requirements.md#req-012-provide-a-minimal-agent-interface)
- Scenario: [SCN-018](../scenarios/SCN-018.md)
- Result: Passed
- Scope: Process a deterministic offline ticket through the CLI and return classifications, answer text/status, citations, and review metadata as validated JSON

## Red

Application-service, subprocess E2E, and Behave expectations were added before the offline orchestrator and CLI option existed.

- Pytest collection errored with `ModuleNotFoundError: support_copilot.application`.
- SCN-018 reached the real CLI, which rejected the unknown `--kb-snapshot` argument.

## Green

Added a bounded offline application service, required answer text on the audit result, and optional `--kb-snapshot`/`--configuration-id` CLI arguments. Deposit evidence produces a cited draft; unsupported requests produce a typed insufficient-knowledge abstention. The original classification-only invocation remains compatible.

- Focused pytest result: `9 passed`
- BDD result: `1 scenario passed`, `3 steps passed`

## Refactor

Separated safety and knowledge resolution behind one typed internal offline decision before composing the public auditable result.

- Pytest regression: `50 passed`
- BDD regression: SCN-001 through SCN-018 passed; `70 steps passed`
- Ruff: all checks passed
- Gherkin validation: `5 feature files`, `28 unique scenarios`, Markdown parity confirmed
- Architecture documentation validation: passed

## Limits of this increment

- Full-result CLI mode requires an explicit local snapshot path and supports the implemented deposit-draft, deterministic safety, and generic abstention paths.
- The classifier remains narrow, so the deposit journey currently retains category `other` while returning a supported deposit draft.
- No web UI, live provider, persistent audit store, or automatic customer transmission is included.
