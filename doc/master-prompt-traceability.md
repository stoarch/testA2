# Master Prompt Traceability

This matrix maps the governing [master prompt](master-prompt.md) to repository evidence. `Planned` means the design or acceptance specification exists but executable delivery is incomplete.

| Master section | Evidence | State |
|---|---|---|
| Functional requirements | [Functional requirements](requirements/functional-requirements.md), [BDD](../bdd/README.md) | Partial: SCN-001/002 implemented |
| Authorized knowledge base | [KB assessment](requirements/knowledge-base.md), [ADR-0005](adr/0005-kb-snapshot-and-lexical-retrieval.md) | Planned |
| Compliance rules | [ADR-0006](adr/0006-deterministic-compliance-and-human-review.md), safety scenarios | Planned |
| Technical architecture | [ADR-0004](adr/0004-mvp-architecture-and-cli.md), [component model](uml/component-overview.puml) | Accepted; implementation partial |
| Five ADR topics | [ADR index](adr/README.md) | Done |
| PlantUML views | [UML index](uml/README.md) | Baseline done |
| BDD first | [Feature files](../bdd/README.md), 28 scenario files | Defined; 2 implemented |
| TDD red-green-refactor | [Execution evidence](../bdd/executions/README.md) | Active |
| Integration and E2E | [Verification matrix](requirements/verification-matrix.md) | Planned |
| 30+ ticket evaluation | REQ-114, ADR-0003 | Planned |
| One-page business case | [Business case](../reports/business-case.md) | Draft; measured inputs missing |
| Phase 2 scaling | [Scaling plan](phase-2-scaling.md), [deployment view](uml/deployment.puml) | Planned |
| README/quickstart | [Repository README](../README.md) | Current-state quickstart done |
| Known limitations/walkthrough | [Limitations](known-limitations.md), [walkthrough](walkthrough.md) | Done for current state |
| Git commits/link | No Git repository detected during prior work | Not available |

## Repository path convention

The master prompt names `docs/adr/`; this repository established `doc/adr/` before the master prompt was added. ADR-0001 keeps the singular `doc/` tree as the canonical documentation root to avoid duplicate sources and broken links.
