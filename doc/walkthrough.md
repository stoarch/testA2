# Technical Walkthrough and Evaluation Guide

## Prototype overview

The Valetax Support Ticket Co-Pilot is a deterministic, offline agent-assist prototype. It classifies support tickets, retrieves allowlisted passages from a synthetic KB fixture, produces a cited extractive deposit draft when supported, and fails closed to abstention or human review for unsupported and safety-sensitive requests.

It has no live Valetax ingestion, generative LLM, external integration, customer auto-send operation, or production deployment.

## Five-minute reviewer demonstration

Install once with `python -m pip install -e ".[dev]"`, then run from the repository root.

```bash
# Grounded extractive deposit draft with structured citation
support-copilot --ticket-id DEMO-001 --text "How do I make a deposit?" --kb-snapshot tests/fixtures/kb/synthetic_snapshot.json

# Explicit abstention for an unsupported deposit operation
support-copilot --ticket-id DEMO-002 --text "Can I cancel my deposit?" --kb-snapshot tests/fixtures/kb/synthetic_snapshot.json

# Trading-advice refusal
support-copilot --ticket-id DEMO-003 --text "Should I buy EUR/USD?" --kb-snapshot tests/fixtures/kb/synthetic_snapshot.json

# KYC and AML human-review routes
support-copilot --ticket-id DEMO-004 --text "Please approve my KYC verification." --kb-snapshot tests/fixtures/kb/synthetic_snapshot.json
support-copilot --ticket-id DEMO-005 --text "Should we release this AML-flagged transaction?" --kb-snapshot tests/fixtures/kb/synthetic_snapshot.json

# Aggregate metrics from four synthetic evaluation cases
support-copilot --evaluation-set tests/fixtures/evaluation/synthetic_evaluation_set.json --kb-snapshot tests/fixtures/kb/synthetic_snapshot.json
```

Ticket and evaluation modes emit JSON. The KB and evaluation inputs are synthetic fixtures, not live or statistically representative operating data.

## Business-case decision

[`reports/business-case.md`](../reports/business-case.md) is generated from [`reports/business-case-input.json`](../reports/business-case-input.json):

```bash
support-copilot --business-case-input reports/business-case-input.json
support-copilot --business-case-input reports/business-case-input.json --business-case-format json
```

Markdown is the default output; JSON is optional. Under the base assumptions, configurations A, B, and C have modeled monthly net values of USD 5,100, USD 6,137.50, and USD 8,830 respectively. These are projections, not measured savings. The authoritative decision is **no-go for deployment** because configuration A has only four synthetic evaluation cases and configurations B/C have no measured quality evidence.

The older figures retained in [`reports/pr2-business-case-assumptions.md`](../reports/pr2-business-case-assumptions.md) are explicitly illustrative history and do not override that decision.

## Verification suite

```bash
python -m pytest -q
ruff check src tests bdd/features/steps
python -m behave bdd/features --name=SCN-001 --name=SCN-002 --name=SCN-003 --name=SCN-004 --name=SCN-005 --name=SCN-006 --name=SCN-007 --name=SCN-008 --name=SCN-009 --name=SCN-010 --name=SCN-011 --name=SCN-012 --name=SCN-013 --name=SCN-014 --name=SCN-015 --name=SCN-016 --name=SCN-017 --name=SCN-018 --name=SCN-019 --name=SCN-020
python bdd/validate_gherkin.py
python scripts/validate_architecture_docs.py
```

The BDD selection matches [GitHub CI](../.github/workflows/ci.yml) and deliberately runs only the 20 implemented scenarios. The eight remaining roadmap scenarios are planned work, not requirements for this submission.
