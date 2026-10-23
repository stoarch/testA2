# Task Specifications

Task specifications turn WBS work packages into bounded, executable assignments. Each specification includes its prompt, inputs, outputs, scope limits, acceptance scenarios, and verification approach.

## Index

| WBS item | Task | Status |
|---|---|---|
| [WBS-001](WBS-001.md) | Establish project and documentation baseline | Done |
| [WBS-002](WBS-002.md) | Define and approve co-pilot requirements | Done |
| WBS-003 | Resolve architecture decisions | Done - [execution](WBS-003-execution-001.md) |
| WBS-004 | Refine system models | Done for baseline - [execution](WBS-004-execution-001.md) |
| [WBS-005](WBS-005.md) | Plan MVP implementation | Done - [execution](WBS-005-execution-001.md) |
| [WBS-006](WBS-006.md) | Prepare engineering foundation | In progress |

Latest execution records: [WBS-004 execution 001](WBS-004-execution-001.md), [WBS-005 execution 001](WBS-005-execution-001.md), and [SCN-003 execution 001](../../bdd/executions/SCN-003-execution-001.md). WBS-006 is the active foundation task.

## Delivery approach

- **BDD:** Define observable behavior and acceptance before implementation.
- **TDD:** For implementation tasks, write a failing unit or component test, add the smallest behavior that passes, then refactor.
- **E2E:** Verify a small set of critical user journeys across real system boundaries in a production-like environment.

BDD scenarios are requirements evidence, TDD is the implementation loop, and E2E tests protect integrated outcomes. One does not replace the others.

