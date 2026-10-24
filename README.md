# Valetax Support Ticket Co-Pilot

An agent-assist prototype for classifying retail Forex/CFD support tickets, retrieving allowlisted evidence, producing cited drafts or explicit abstentions, and routing safety-sensitive cases to human review.

The governing specification is [`doc/master-prompt.md`](doc/master-prompt.md). Current delivery status is tracked in [`DASHBOARD/PROGRESS.md`](DASHBOARD/PROGRESS.md).

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

## Developer quickstart

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

The checked-in KB fixture is explicitly synthetic. It supports deterministic tests and is not live Valetax evidence.

The unfiltered Behave suite is not expected to pass yet because planned scenarios intentionally have no step definitions.

## Documentation

- [Architecture decisions](doc/adr/README.md)
- [PlantUML models](doc/uml/README.md)
- [Requirements](doc/requirements/README.md)
- [BDD scenarios](bdd/README.md)
- [Work breakdown](doc/WBS.md)
- [Master-prompt traceability](doc/master-prompt-traceability.md)
- [Phase 2 scaling plan](doc/phase-2-scaling.md)
- [Known limitations](doc/known-limitations.md)
- [Technical walkthrough](doc/walkthrough.md)
