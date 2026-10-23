# Component Overview

- Authoritative source: [component-overview.puml](component-overview.puml)
- Related decisions: [ADR-0004](../adr/0004-mvp-architecture-and-cli.md), [ADR-0005](../adr/0005-kb-snapshot-and-lexical-retrieval.md), [ADR-0006](../adr/0006-deterministic-compliance-and-human-review.md), [ADR-0007](../adr/0007-provider-abstraction-and-offline-fallback.md)
- Related requirements: `REQ-001`-`REQ-021`, `REQ-101`-`REQ-115`

The component model separates the CLI, application orchestration, domain policy, provider protocols, infrastructure adapters, and validated result presentation. Ticket and retrieved content enter from untrusted boundaries. Deterministic pre-generation and post-generation gates remain independent of any LLM provider.

Only ticket identity and initial withdrawal classification are currently implemented. Other components are architectural commitments or planned MVP work and are labeled accordingly in the PlantUML source.
