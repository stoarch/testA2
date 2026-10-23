# Step Definitions

Step definitions are added one scenario at a time through red-green-refactor.

| Scenario | Step module | State |
|---|---|---|
| SCN-001 | [`ticket_identity_steps.py`](ticket_identity_steps.py) | Passing |
| SCN-002 | [`ticket_classification_steps.py`](ticket_classification_steps.py) | Passing |
| SCN-003 | [`ticket_classification_steps.py`](ticket_classification_steps.py) | Passing |
| SCN-004 | [`ticket_classification_steps.py`](ticket_classification_steps.py) | Passing |
| SCN-005 | [`knowledge_base_steps.py`](knowledge_base_steps.py) | Passing |
| SCN-006 | [`drafting_steps.py`](drafting_steps.py) | Passing |
| SCN-007 | [`evidence_validation_steps.py`](evidence_validation_steps.py) | Passing |

Run the implemented first scenario with:

```text
behave bdd/features --name=SCN-001 --name=SCN-002 --name=SCN-003 --name=SCN-004 --name=SCN-005 --name=SCN-006 --name=SCN-007
```

The remaining scenarios intentionally have undefined steps until their implementation increments begin.

