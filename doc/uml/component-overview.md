# Component Overview

- Authoritative source: [component-overview.puml](component-overview.puml)
- Related decisions: [ADR-0004](../adr/0004-mvp-architecture-and-cli.md), [ADR-0005](../adr/0005-kb-snapshot-and-lexical-retrieval.md), [ADR-0006](../adr/0006-deterministic-compliance-and-human-review.md), [ADR-0007](../adr/0007-provider-abstraction-and-offline-fallback.md)
- Related requirements: `REQ-001`-`REQ-021`, `REQ-101`-`REQ-115`

The component model separates the CLI, application orchestration, domain policy, provider protocols, infrastructure adapters, and validated result presentation. Ticket and retrieved content enter from untrusted boundaries. Deterministic pre-generation and post-generation gates remain independent of any LLM provider.

The CLI, Pydantic input/classification and auditable-result contracts, deterministic classifier, synthetic JSON snapshot repository, allowlist, hash validation, section retriever, extractive deposit drafting, exact numeric-duration citation validation, explicit duration-conflict abstention with source exposure, typed fee/verification abstentions, direct currency-pair and personalized-leverage refusals, explicit KYC/complaint decision routing, configured low-confidence routing, and in-process audit-result composition are implemented. Live snapshot fetching, orchestration, confidence production/calibration, general semantic evidence/conflict validation, broader safety routing, providers, full-result CLI output, and audit storage remain architectural commitments or planned MVP work and are labeled accordingly in the PlantUML source.
