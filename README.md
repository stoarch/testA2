# Valetax Support Ticket Co-Pilot

An agent-assist prototype for classifying retail Forex/CFD support tickets, retrieving allowlisted evidence, producing cited drafts or explicit abstentions, and routing safety-sensitive cases to human review.

The governing specification is [`doc/master-prompt.md`](doc/master-prompt.md). Current delivery status is tracked in [`DASHBOARD/PROGRESS.md`](DASHBOARD/PROGRESS.md). The numerical business case for 10,000 tickets/month is in [`reports/business-case.md`](reports/business-case.md).

---

## Architecture & Implementation Overview

- **Deterministic Offline Processing**: Built using Python 3.12+ and Pydantic v2. Operates completely offline without external LLM API dependencies or paid cloud requirements during Phase 1.
- **Synthetic Knowledge Base**: Uses checked-in synthetic JSON snapshots (`tests/fixtures/kb/synthetic_snapshot.json`) enforcing cryptographic content hashes and URL allowlisting. Ingestion of live Valetax documentation and vector search remain planned for Phase 2.
- **Fail-Closed Safety Routing**: Automatically detects and refuses/routes trading advice, personalized leverage queries, trading signals, price targets, KYC/AML decisions, and customer complaints directly to human reviewers.
- **BDD Roadmap Alignment**: 19 core scenarios (`SCN-001` through `SCN-019`) are fully implemented with executable tests. The remaining 9 roadmap scenarios (`SCN-020` through `SCN-028`) are documented architectural specifications reserved for Phase 2 scaling.

---

## Implemented BDD Scenarios (19/28 Passing)

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

*Planned Phase 2 Scenarios (`SCN-020`–`SCN-028`): Business case generator, live retrieval failure recovery, mixed trading/support routing, prompt injection resistance, provider outage handling, unsupported language routing, and input validation bounds.*

---

## CLI Demonstration Commands

All commands run offline, require no API credentials, and output schema-valid JSON.

### 1. Grounded Deposit Answer with Citation
```bash
support-copilot --ticket-id DEMO-001 --text "How do I make a deposit?" --kb-snapshot tests/fixtures/kb/synthetic_snapshot.json
```

### 2. Abstention for Unsupported Policy (Deposit Cancellation / Unknown Policy)
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

---

## Developer Quickstart

```bash
# Install development dependencies using uv
uv sync --extra dev

# Run unit and integration pytest suite
uv run pytest -q

# Run implemented BDD feature scenarios
uv run behave bdd/features --tags=@must

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
- [Architecture Decision Records (ADRs)](doc/adr/README.md)
- [PlantUML Architecture Views](doc/uml/README.md)
- [Functional & Non-Functional Requirements](doc/requirements/README.md)
- [BDD Scenarios & Feature Specs](bdd/README.md)
- [Phase 2 Scaling & Generative Strategy](doc/phase-2-scaling.md)
- [Known Limitations](doc/known-limitations.md)
- [Technical Walkthrough](doc/walkthrough.md)
