# Technical Walkthrough

## Current five-minute walkthrough

1. Read [the master prompt](master-prompt.md) and [traceability matrix](master-prompt-traceability.md).
2. Review the five required architecture decisions through the [ADR index](adr/README.md).
3. Open the [component](uml/component-overview.puml) and [processing sequence](uml/processing-sequence.puml) sources to inspect trust boundaries and safe branches.
4. Inspect [SCN-001](../bdd/scenarios/SCN-001.md) and [SCN-002](../bdd/scenarios/SCN-002.md), including their red-green-refactor execution evidence.
5. Run the current tests from the repository [README](../README.md).

## Planned MVP demo

The completion demo must invoke the real CLI in deterministic offline mode and show four distinct outcomes:

1. A grounded operational answer with resolvable citation.
2. Abstention for missing or contradictory evidence.
3. Refusal of trading advice with no recommendation content.
4. Human escalation for complaint/KYC, injection, unsafe output, or dependency failure.

Each result must identify execution mode, configuration, route reasons, evidence provenance, latency, and usage when available. Synthetic evidence must be visibly labeled.
