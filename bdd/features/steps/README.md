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
| SCN-008 | [`abstention_steps.py`](abstention_steps.py) | Passing |
| SCN-009 | [`abstention_steps.py`](abstention_steps.py) | Passing |
| SCN-010 | [`safety_steps.py`](safety_steps.py) | Passing |
| SCN-011 | [`safety_steps.py`](safety_steps.py) | Passing |
| SCN-012 | [`safety_steps.py`](safety_steps.py) | Passing |
| SCN-013 | [`safety_steps.py`](safety_steps.py) | Passing |
| SCN-014 | [`routing_steps.py`](routing_steps.py) | Passing |

Run the implemented first scenario with:

```text
behave bdd/features --name=SCN-001 --name=SCN-002 --name=SCN-003 --name=SCN-004 --name=SCN-005 --name=SCN-006 --name=SCN-007 --name=SCN-008 --name=SCN-009 --name=SCN-010 --name=SCN-011 --name=SCN-012 --name=SCN-013 --name=SCN-014
```

The remaining scenarios intentionally have undefined steps until their implementation increments begin.

