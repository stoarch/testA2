# Step Definitions

Step definitions are added one scenario at a time through red-green-refactor.

| Scenario | Step module | State |
|---|---|---|
| SCN-001 | [`ticket_identity_steps.py`](ticket_identity_steps.py) | Passing |

Run the implemented first scenario with:

```text
behave bdd/features --tags=@REQ-001
```

The remaining scenarios intentionally have undefined steps until their implementation increments begin.

