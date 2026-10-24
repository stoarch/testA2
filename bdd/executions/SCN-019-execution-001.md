# SCN-019 Execution 001

- Date: 2026-10-24
- Requirement: [REQ-013](../../doc/requirements/functional-requirements.md#req-013-evaluate-configurations)
- Scenario: [SCN-019](../scenarios/SCN-019.md)
- Result: Passed
- Scope: Evaluate one deterministic offline configuration against a bounded labeled set and emit aggregate quality, review, latency, and cost measurements as validated JSON

## Red

Typed metric, integration, subprocess E2E, and Behave expectations were added before the evaluation domain or CLI mode existed.

- Pytest collection failed with `ModuleNotFoundError: support_copilot.evaluation`.
- SCN-019 reached the real CLI, which required ticket arguments and rejected evaluation mode.

## Green

Added typed evaluation cases, expected outcomes, ratio/latency/cost measurements, a four-kind synthetic fixture, an aggregate report builder, and `--evaluation-set` CLI execution. Every ratio exposes its numerator and denominator; cost remains explicitly unavailable unless both usage and pricing exist.

- Focused pytest result: `6 passed`
- BDD result: `1 scenario passed`, `3 steps passed`

## Refactor

Centralized ratio and percentile calculation, enforced ratio/latency/cost invariants in the contracts, and kept raw ticket text out of the report.

- Pytest regression: `54 passed`
- BDD regression: SCN-001 through SCN-019 passed; `73 steps passed`
- Ruff: all checks passed
- Gherkin validation: `5 feature files`, `28 unique scenarios`, Markdown parity confirmed
- Architecture documentation validation: passed

## Observed bounded-set findings

The four-case offline fixture reported:

- Classification, safety, grounding, and citation outcome accuracy: `4/4` each.
- Review rate: `3/4`; review recall: `3/3`; false-review rate: `0/1`.
- Review-reason accuracy: `3/4`. The conflict-labeled case safely abstains and routes, but the bounded application path currently reports `insufficient_knowledge` rather than `source_conflict`.
- Abstention frequency: `2/4`; unsupported-claim rate: `0/1` drafted results.
- Critical policy violations: `0/1` safety cases. This is not evidence of universal safety.
- Latency p50/p95 are measured for each local run and therefore environment-dependent.
- Cost status: `unavailable` because the offline path provides neither measured token usage nor supplied pricing.

## Limits of this increment

- The executable fixture has four representative cases, not the separate required 30+ routine/risky/contradictory/multilingual/unsupported/adversarial set.
- Citation validity is a case-level comparison against labeled source IDs; general semantic support validation remains planned.
- The report evaluates one deterministic offline configuration; provider comparison and business-case projections remain SCN-020 work.
