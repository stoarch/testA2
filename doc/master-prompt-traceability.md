# Master Prompt Traceability

This matrix maps the governing [master prompt](master-prompt.md) to repository evidence. `Planned` means the design or acceptance specification exists but executable delivery is incomplete.

| Master section | Evidence | State |
|---|---|---|
| Functional requirements | [Functional requirements](requirements/functional-requirements.md), [BDD](../bdd/README.md) | Prototype slice implemented through SCN-021 |
| Authorized knowledge base | [KB assessment](requirements/knowledge-base.md), [ADR-0005](adr/0005-kb-snapshot-and-lexical-retrieval.md) | Synthetic offline snapshot implemented; live ingestion planned |
| Compliance rules | [ADR-0006](adr/0006-deterministic-compliance-and-human-review.md), safety scenarios | Deterministic prototype rules implemented; broader production controls planned |
| Technical architecture | [ADR-0004](adr/0004-mvp-architecture-and-cli.md), [component model](uml/component-overview.puml) | Accepted; Phase 1 prototype implemented |
| Five ADR topics | [ADR index](adr/README.md) | Done |
| PlantUML views | [UML index](uml/README.md) | Baseline done |
| BDD first | [Feature files](../bdd/README.md), 28 scenario files | 21 implemented; 7 intentionally planned |
| TDD red-green-refactor | [Execution evidence](../bdd/executions/README.md) | Complete for SCN-001 through SCN-021 |
| Integration and E2E | [Verification matrix](requirements/verification-matrix.md) | Implemented for the Phase 1 prototype slice |
| 30+ ticket evaluation | REQ-114, ADR-0003 | Planned |
| One-page business case | [Business case](../reports/business-case.md) | Generated low/base/high comparison; no-go because evidence and operating inputs remain insufficient |
| Phase 2 scaling | [Scaling plan](phase-2-scaling.md), [deployment view](uml/deployment.puml) | Planned |
| README/quickstart | [Repository README](../README.md) | Current-state quickstart done |
| Known limitations/walkthrough | [Limitations](known-limitations.md), [walkthrough](walkthrough.md) | Done for current state |
| Git commits/link | Repository history on `main`; submission commit recorded in Git | Available |

## Repository path convention

The master prompt names `docs/adr/`; this repository established `doc/adr/` before the master prompt was added. ADR-0001 keeps the singular `doc/` tree as the canonical documentation root to avoid duplicate sources and broken links.
