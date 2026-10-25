# Valetax Support Ticket Co-Pilot

An offline, deterministic agent-assist prototype for the Valetax AI Engineer take-home assignment. It classifies retail Forex/CFD support tickets, retrieves allowlisted evidence from a checked-in synthetic knowledge-base snapshot, produces cited drafts or explicit abstentions, and routes safety-sensitive requests to human review.

This is a timeboxed prototype for reviewer evaluation, not a production deployment or customer auto-send system. The governing specification is [`doc/master-prompt.md`](doc/master-prompt.md), and current delivery status is in [`DASHBOARD/PROGRESS.md`](DASHBOARD/PROGRESS.md).

## What the Phase 1 prototype demonstrates

- Five classification outcomes: `deposit`, `withdrawal`, `account_opening`, `verification`, and `other`; zero or multiple category matches fall back to `other`.
- Pydantic contracts for classification, answer status, citations, review metadata, configuration, latency, and optional token usage.
- Retrieval from a persisted **synthetic offline KB fixture** with URL allowlisting and content-hash validation.
- An extractive deposit how-to draft with structured provenance; unsupported, ambiguous, or uncovered deposit requests abstain.
- Refusal of buy/sell advice, trading signals, price targets, and personalized leverage recommendations.
- Human-review routing for KYC, AML, complaint outcomes, low confidence, insufficient knowledge, and explicit source conflicts.
- Fail-closed, schema-valid abstention when the synthetic KB cannot be loaded, validated, or queried.
- A four-case synthetic evaluation and an evidence-gated comparison of three operating configurations.

The implemented acceptance slice is `SCN-001` through `SCN-021`: 21 of 28 roadmap scenarios (75%). The remaining seven scenarios are intentional future work and are not required for this submission.

## Quickstart

Requires Python 3.12 or later.

```bash
python -m pip install -e ".[dev]"
```

Run a classification-only request:

```bash
support-copilot --ticket-id DEMO-CLASSIFY --text "I am frustrated because my withdrawal is still pending."
```

Ticket and evaluation modes return JSON. Business-case mode returns Markdown by default and supports JSON with `--business-case-format json`.

## Five-minute CLI demonstration

All ticket-processing examples below use [`tests/fixtures/kb/synthetic_snapshot.json`](tests/fixtures/kb/synthetic_snapshot.json), a synthetic fixture rather than live Valetax page ingestion.

Grounded deposit draft with a structured citation:

```bash
support-copilot --ticket-id DEMO-001 --text "How do I make a deposit?" --kb-snapshot tests/fixtures/kb/synthetic_snapshot.json
```

Explicit abstention for an unsupported deposit operation:

```bash
support-copilot --ticket-id DEMO-002 --text "Can I cancel my deposit?" --kb-snapshot tests/fixtures/kb/synthetic_snapshot.json
```

Fail-closed abstention when the KB snapshot is unavailable:

```bash
support-copilot --ticket-id DEMO-KB-FAILURE --text "How do I make a deposit?" --kb-snapshot tests/fixtures/kb/does-not-exist.json
```

Trading-advice refusal:

```bash
support-copilot --ticket-id DEMO-003 --text "Should I buy EUR/USD?" --kb-snapshot tests/fixtures/kb/synthetic_snapshot.json
```

KYC and AML escalation to human review:

```bash
support-copilot --ticket-id DEMO-004 --text "Please approve my KYC verification." --kb-snapshot tests/fixtures/kb/synthetic_snapshot.json
support-copilot --ticket-id DEMO-005 --text "Should we release this AML-flagged transaction?" --kb-snapshot tests/fixtures/kb/synthetic_snapshot.json
```

Bounded offline evaluation:

```bash
support-copilot --evaluation-set tests/fixtures/evaluation/synthetic_evaluation_set.json --kb-snapshot tests/fixtures/kb/synthetic_snapshot.json
```

The evaluation fixture contains four synthetic cases (normal, knowledge gap, source conflict, and safety). It is useful for demonstrating the metrics contract, not for statistical safety claims.

## Testing and CI

Run the same implemented BDD selection used by [CI](.github/workflows/ci.yml):

```bash
python -m pytest -q
ruff check src tests bdd/features/steps
python -m behave bdd/features --name=SCN-001 --name=SCN-002 --name=SCN-003 --name=SCN-004 --name=SCN-005 --name=SCN-006 --name=SCN-007 --name=SCN-008 --name=SCN-009 --name=SCN-010 --name=SCN-011 --name=SCN-012 --name=SCN-013 --name=SCN-014 --name=SCN-015 --name=SCN-016 --name=SCN-017 --name=SCN-018 --name=SCN-019 --name=SCN-020 --name=SCN-021
python bdd/validate_gherkin.py
python scripts/validate_architecture_docs.py
```

The explicit `--name` selection matters: some planned scenarios also carry the `@must` tag but intentionally do not have executable steps yet.

## Quantitative business case

Generate the authoritative one-page report from its source input:

```bash
support-copilot --business-case-input reports/business-case-input.json
```

Optional JSON output:

```bash
support-copilot --business-case-input reports/business-case-input.json --business-case-format json
```

The model projects positive economic value under stated assumptions, but the evidence gate returns **no-go for deployment**: configuration A has only four synthetic evaluation cases, while configurations B and C have no measured quality evidence. Earlier figures in [`reports/pr2-business-case-assumptions.md`](reports/pr2-business-case-assumptions.md) are illustrative history, not measured savings or the authoritative decision.

## Phase 2 architecture and limitations

The repository documents a possible path to live retrieval, guarded generative drafting, broader evaluation, external integrations, and production operations. None is claimed as implemented. Current boundaries include deterministic English-oriented heuristics, deposit-only extractive drafting in the end-to-end path, limited semantic conflict detection, no live KB ingestion or generative LLM, no persistent audit store or review queue, and no production deployment.

See [`doc/phase-2-scaling.md`](doc/phase-2-scaling.md) and [`doc/known-limitations.md`](doc/known-limitations.md) for detail.

## Documentation

- [Technical walkthrough](doc/walkthrough.md)
- [Progress dashboard](DASHBOARD/PROGRESS.md)
- [Known limitations](doc/known-limitations.md)
- [Generated business case](reports/business-case.md)
- [Business-case source input](reports/business-case-input.json)
- [Requirements and verification](doc/requirements/README.md)
- [Architecture decisions](doc/adr/README.md)
- [Architecture views](doc/uml/README.md)
- [BDD scenarios and execution evidence](bdd/README.md)
