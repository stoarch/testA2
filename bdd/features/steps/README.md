# Step Definitions

Step definitions are added one scenario at a time through red-green-refactor.

| Scenario | Step module | State |
|---|---|---|
| SCN-001 | [`ticket_identity_steps.py`](ticket_identity_steps.py) | Passing |
| SCN-002 | [`ticket_classification_steps.py`](ticket_classification_steps.py) | Passing |
| SCN-003 | [`ticket_classification_steps.py`](ticket_classification_steps.py) | Passing |
| SCN-004 | [`ticket_classification_steps.py`](ticket_classification_steps.py) | Passing |

Run the implemented first scenario with:

```text
behave bdd/features --name=SCN-001 --name=SCN-002 --name=SCN-003 --name=SCN-004
```

The remaining scenarios intentionally have undefined steps until their implementation increments begin.

