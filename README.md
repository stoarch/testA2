# Valetax Support Ticket Co-Pilot

An agent-assist prototype for classifying retail Forex/CFD support tickets, retrieving allowlisted evidence, producing cited drafts or explicit abstentions, and routing safety-sensitive cases to human review.

The governing specification is [`doc/master-prompt.md`](doc/master-prompt.md). Current delivery status is tracked in [`DASHBOARD/PROGRESS.md`](DASHBOARD/PROGRESS.md).

## Current implemented slice

- Preserve the input ticket identifier (`SCN-001`).
- Classify a withdrawal question as `withdrawal` (`SCN-002`).
- Preserve unsupported topics as `other` (`SCN-003`).
- Return category, urgency, language, and sentiment through Pydantic contracts (`SCN-004`).
- Provide a credential-free CLI that emits schema-valid JSON for agent review.

Retrieval, drafting, compliance routing, evaluation, and business-case runtime behavior remains planned unless the dashboard says otherwise.

## Developer quickstart

Prerequisite: Python 3.12+.

```text
python -m pip install -e ".[dev]"
python -m pytest -q
python -m behave bdd/features --name=SCN-001 --name=SCN-002 --name=SCN-003 --name=SCN-004
python bdd/validate_gherkin.py
python scripts/validate_architecture_docs.py
ruff check src tests bdd/features/steps
```

Run the current offline classifier:

```text
support-copilot --ticket-id TICKET-004 --text "I am frustrated because my withdrawal is still pending."
```

The command returns JSON to the support-agent interface; it has no customer-send operation.

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
