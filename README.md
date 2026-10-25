# Valetax Support Ticket Co-Pilot

An agent-assist prototype for classifying retail Forex/CFD support tickets, retrieving allowlisted evidence, producing cited drafts or explicit abstentions, and routing safety-sensitive cases to human review.

The governing specification is [`doc/master-prompt.md`](doc/master-prompt.md). Current delivery status is tracked in [`DASHBOARD/PROGRESS.md`](DASHBOARD/PROGRESS.md). The numerical business case for 10,000 tickets/month is in [`reports/business-case.md`](reports/business-case.md).

---
## Demo scope and decision support

## Current implemented slice

- Preserve the input ticket identifier (`SCN-001`).
- Classify a withdrawal question as `withdrawal` (`SCN-002`).
- Preserve unsupported topics as `other` (`SCN-003`).
- Return category, urgency, language, and sentiment through Pydantic contracts (`SCN-004`).
- Load a persisted synthetic KB snapshot and retrieve only from the four approved source URLs (`SCN-005`).
- Produce an extractive deposit draft with full-provenance structured citation (`SCN-006`).
- Validate explicit numeric timeline claims against exact durations in cited passages (`SCN-007`).
- Return a typed, human-reviewed abstention when approved evidence does not establish a requested fee (`SCN-008`).
- Abstain without inference when approved verification evidence lacks a requested detail (`SCN-009`).
- Refuse direct currency-pair buy recommendations and require human review (`SCN-010`).
- Refuse personalized leverage-setting recommendations without repeating marketing claims (`SCN-011`).
- Route explicit KYC verification-outcome requests with a neutral acknowledgement and human review (`SCN-012`).
- Route explicit complaint-outcome requests with a neutral acknowledgement and human review (`SCN-013`).
- Route coverage abstentions to human review with canonical reason `insufficient_knowledge` (`SCN-014`).
- Route configured low-confidence classification or grounding results and retain the threshold (`SCN-015`).
- Return a frozen auditable result with classifications, decision metadata, evidence, configuration, latency, and optional token usage (`SCN-016`).
- Abstain from explicit conflicting approved-source duration claims, expose both sources, and require review with `source_conflict` (`SCN-017`).
- Process an offline ticket through the CLI and return validated classification, answer, citations, and review metadata (`SCN-018`).
- Evaluate a bounded synthetic normal/gap/conflict/safety set and return aggregate quality, review, latency, and cost-availability measurements (`SCN-019`).
- Generate an evidence-gated one-page comparison of deterministic, guarded-LLM, and hybrid configurations at 10,000 tickets/month (`SCN-020`).
- Provide a credential-free CLI that emits schema-valid JSON for agent review.

Live retrieval, general semantic claim validation, generative drafting, broad safety-intent coverage/routing, the 30+ case evaluation corpus, and measured operating inputs remain planned unless the dashboard says otherwise.
## Prototype boundary

This is an **agent-assist test-task prototype**, not a production deployment. The CLI
runs against an explicitly **synthetic offline snapshot**; it never contacts customers.
Four common category intents are classified by bounded keyword rules; ambiguity falls
back to `other`. Procedural deposit answers can be extracted with a synthetic citation.
Other topics and fee/timeline/limit questions safely abstain until verified live KB
sources or further domain-specific answer rules are incorporated. Human review is mandatory
for abstentions and sensitive outcomes including AML. No production KB ingestion, model
provider, calibration or general multilingual NLP is claimed.

See [`reports/business-case.md`](reports/business-case.md) for the numerical three-configuration
business case (all assumptions explicitly illustrative), and
[`doc/phase-2-scaling.md`](doc/phase-2-scaling.md) for scale-up design.

### Five-minute technical demo

#### Full developer verification and business-case generation

Prerequisite: Python 3.12+.

```text
python -m pip install -e ".[dev]"
python -m pytest -q
python -m behave bdd/features --name=SCN-001 --name=SCN-002 --name=SCN-003 --name=SCN-004 --name=SCN-005 --name=SCN-006 --name=SCN-007 --name=SCN-008 --name=SCN-009 --name=SCN-010 --name=SCN-011 --name=SCN-012 --name=SCN-013 --name=SCN-014 --name=SCN-015 --name=SCN-016 --name=SCN-017 --name=SCN-018 --name=SCN-019 --name=SCN-020
python bdd/validate_gherkin.py
python scripts/validate_architecture_docs.py
ruff check src tests bdd/features/steps
```

Run the current offline classifier:

```text
support-copilot --ticket-id TICKET-004 --text "I am frustrated because my withdrawal is still pending."
```

Run the bounded full-result journey against the synthetic snapshot:

```text
support-copilot --ticket-id TICKET-018 --text "How do I make a deposit?" --kb-snapshot tests/fixtures/kb/synthetic_snapshot.json
```

Run the bounded offline evaluation:

```text
support-copilot --evaluation-set tests/fixtures/evaluation/synthetic_evaluation_set.json --kb-snapshot tests/fixtures/kb/synthetic_snapshot.json
```

Generate the one-page business case as Markdown:

```text
support-copilot --business-case-input reports/business-case-input.json --business-case-format markdown
```

Ticket and evaluation commands return JSON; business-case mode supports JSON or Markdown. None has a customer-send operation. The evaluation report contains aggregate metrics only, labels its execution mode, and reports cost as unavailable because offline token usage and pricing are not measured. Business-case financial outputs are explicitly labeled estimates and the current evidence gate returns no-go.
#### Quick demo commands

```shell
support-copilot --ticket-id DEMO-1 --text "How do I make a deposit?" --kb-snapshot tests/fixtures/kb/synthetic_snapshot.json
support-copilot --ticket-id DEMO-2 --text "What is the deposit fee?" --kb-snapshot tests/fixtures/kb/synthetic_snapshot.json
support-copilot --ticket-id DEMO-3 --text "Should I buy EUR/USD?" --kb-snapshot tests/fixtures/kb/synthetic_snapshot.json
support-copilot --ticket-id DEMO-4 --text "Should we release this AML-flagged transaction?" --kb-snapshot tests/fixtures/kb/synthetic_snapshot.json
support-copilot --evaluation-set tests/fixtures/evaluation/synthetic_evaluation_set.json --kb-snapshot tests/fixtures/kb/synthetic_snapshot.json
```

## Architecture & Implementation Overview

- **Deterministic Offline Processing**: Built using Python 3.12+ and Pydantic v2. Operates completely offline without external LLM API dependencies or paid cloud requirements during Phase 1.
- **Synthetic Knowledge Base**: Uses checked-in synthetic JSON snapshots (`tests/fixtures/kb/synthetic_snapshot.json`) enforcing cryptographic content hashes and URL allowlisting. Ingestion of live Valetax documentation and vector search remain planned for Phase 2.
- **Fail-Closed Safety Routing**: Automatically detects and refuses/routes trading advice (buy/sell recommendations, signals, price targets, leverage choices), KYC decisions, AML flags, and customer complaints directly to human review.
- **BDD Roadmap Alignment**: 20 core scenarios (`SCN-001` through `SCN-020`) are fully implemented with executable tests. The remaining 8 roadmap scenarios (`SCN-021` through `SCN-028`) are reserved for subsequent increments.

---

## Implemented BDD Scenarios (20/28 Passing)

1. `SCN-001`: Preserve ticket identity across classification pipeline.
2. `SCN-002`: Classify supported withdrawal queries accurately.
3. `SCN-003`: Map unsupported/unknown categories strictly to `other`.
4. `SCN-004`: Return validated Pydantic contracts for category, urgency, language, and sentiment.
5. `SCN-005`: Enforce snapshot content integrity hashes and approved source URL allowlists.
6. `SCN-006`: Produce extractive deposit answers with full-provenance citations.
7. `SCN-007`: Enforce exact numeric timeline claim matching against cited passages.
8. `SCN-008`: Abstain with human review when requested fees are uncovered in knowledge base.
9. `SCN-009`: Abstain without inference when requested verification details are missing.
10. `SCN-010`: Refuse direct currency-pair buy/sell recommendations and route to human review.
11. `SCN-011`: Refuse personalized leverage recommendations without repeating marketing claims.
12. `SCN-012`: Neutral acknowledgement and human routing for explicit KYC outcome requests.
13. `SCN-013`: Neutral acknowledgement and human routing for complaint outcome decisions.
14. `SCN-014`: Route coverage abstentions with canonical review reason `insufficient_knowledge`.
15. `SCN-015`: Route low-confidence grounding or classification below configured threshold.
16. `SCN-016`: Build immutable JSON-ready audit records with latency and decision metadata.
17. `SCN-017`: Abstain on conflicting approved-source timeline claims with dual citations and `source_conflict`.
18. `SCN-018`: Execute CLI offline ticket processing returning validated classification, draft/abstention, and audit metadata.
19. `SCN-019`: Run offline evaluation suite emitting aggregate accuracy, review rate, latency, and cost availability metrics.
20. `SCN-020`: Generate an evidence-gated business-case comparison for deterministic, guarded-LLM, and hybrid configurations.

*Planned scenarios (`SCN-021`–`SCN-028`): live retrieval failure recovery, mixed trading/support routing, prompt injection resistance, provider outage handling, unsupported language routing, and input validation bounds.*

---

## CLI Demonstration Commands

All commands run offline, require no API credentials, and output schema-valid JSON.

### 1. Grounded Deposit Answer with Citation
```bash
support-copilot --ticket-id DEMO-001 --text "How do I make a deposit?" --kb-snapshot tests/fixtures/kb/synthetic_snapshot.json
```

### 2. Abstention for Unsupported Deposit Policy (Deposit Cancellation / Fee / Limit)
```bash
support-copilot --ticket-id DEMO-002 --text "Can I cancel my deposit?" --kb-snapshot tests/fixtures/kb/synthetic_snapshot.json
```

### 3. Trading-Advice Safety Refusal
```bash
support-copilot --ticket-id DEMO-003 --text "Should I buy EUR/USD?" --kb-snapshot tests/fixtures/kb/synthetic_snapshot.json
```

### 4. AML / KYC Escalation to Human Review
```bash
support-copilot --ticket-id DEMO-004 --text "Please approve my KYC verification." --kb-snapshot tests/fixtures/kb/synthetic_snapshot.json
```

### 5. Aggregate Offline Evaluation Output
```bash
support-copilot --evaluation-set tests/fixtures/evaluation/synthetic_evaluation_set.json --kb-snapshot tests/fixtures/kb/synthetic_snapshot.json
```

### 6. Mixed-Category Request Abstention
```bash
support-copilot --ticket-id DEMO-005 --text "How do I withdraw and deposit?" --kb-snapshot tests/fixtures/kb/synthetic_snapshot.json
```

---

## Developer Quickstart

```bash
# Install development dependencies using uv
uv sync --extra dev

# Run unit and integration pytest suite
uv run pytest -q

# Run implemented BDD feature scenarios
uv run behave bdd/features --name=SCN-001 --name=SCN-002 --name=SCN-003 --name=SCN-004 --name=SCN-005 --name=SCN-006 --name=SCN-007 --name=SCN-008 --name=SCN-009 --name=SCN-010 --name=SCN-011 --name=SCN-012 --name=SCN-013 --name=SCN-014 --name=SCN-015 --name=SCN-016 --name=SCN-017 --name=SCN-018 --name=SCN-019

# Validate Gherkin specification parity
uv run python bdd/validate_gherkin.py

# Validate architecture documentation & ADR links
uv run python scripts/validate_architecture_docs.py

# Run code style & lint checks
uv run ruff check src tests bdd/features/steps
```

---

## Documentation Index

- [Business Case & Economic Evaluation (10k tickets/month)](reports/business-case.md)
- [PR #2 Business-Case Assumptions Appendix](reports/pr2-business-case-assumptions.md)
- [Architecture Decision Records (ADRs)](doc/adr/README.md)
- [PlantUML Architecture Views](doc/uml/README.md)
- [Functional & Non-Functional Requirements](doc/requirements/README.md)
- [BDD Scenarios & Feature Specs](bdd/README.md)
- [Phase 2 Scaling & Generative Strategy](doc/phase-2-scaling.md)
- [Known Limitations](doc/known-limitations.md)
- [Technical Walkthrough](doc/walkthrough.md)
