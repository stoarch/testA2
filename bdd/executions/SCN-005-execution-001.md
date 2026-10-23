# SCN-005 Execution 001

- Date: 2026-10-24
- Requirements: [REQ-004 and REQ-020](../../doc/requirements/functional-requirements.md)
- Scenario: [SCN-005](../scenarios/SCN-005.md)
- Result: Passed
- Scope: Persist a synthetic snapshot and retrieve only allowlisted section passages with provenance

## Red

Unit, persisted-snapshot integration, and Behave expectations were added before the knowledge-base module existed.

- Unit collection failed with `ModuleNotFoundError: support_copilot.knowledge_base`.
- Integration collection failed with the same missing module.
- SCN-005 errored in its Given step before any retrieval occurred.

## Green

Added Pydantic snapshot/source/passage contracts, JSON load/save functions, an exact four-URL allowlist, and deterministic section-level lexical scoring.

- Allowlist/provenance unit result: `1 passed`
- Persisted snapshot integration result: `1 passed`
- BDD result: `1 scenario passed`, `3 steps passed`

## Refactor

Extracted canonical token normalization and SHA-256 document hashing, validated hashes on snapshot load/save, and added a corrupt-hash rejection test.

- Pytest regression: `8 passed`
- BDD regression: SCN-001 through SCN-005 passed; `16 steps passed`
- Ruff: all checks passed
- Gherkin validation: `5 feature files`, `28 unique scenarios`, Markdown parity confirmed

## Limits of this increment

- The checked-in content is explicitly synthetic and must not be represented as live Valetax evidence.
- Live page fetching and snapshot refresh are not implemented.
- Lexical scoring is deliberately small and has not been evaluated for paraphrase or multilingual recall.
- Citation validation, drafting, abstention, contradiction handling, and customer-facing behavior remain unimplemented.
