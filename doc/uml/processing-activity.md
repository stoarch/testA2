# Processing Activity

- Authoritative source: [processing-activity.puml](processing-activity.puml)
- Related decisions: [ADR-0004](../adr/0004-mvp-architecture-and-cli.md), [ADR-0006](../adr/0006-deterministic-compliance-and-human-review.md)
- Related requirements: `REQ-006`-`REQ-011`, `REQ-016`-`REQ-021`, `REQ-101`, `REQ-111`

This activity view makes fail-closed behavior explicit. Invalid input, unsupported language, injection signals, regulated requests, retrieval failure, evidence gaps, contradictions, and unsafe drafts all stop customer-draft progression and create a human-review outcome.
