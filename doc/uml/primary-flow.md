# Processing Sequence

- Authoritative source: [processing-sequence.puml](processing-sequence.puml)
- Related decisions: [ADR-0004](../adr/0004-mvp-architecture-and-cli.md), [ADR-0006](../adr/0006-deterministic-compliance-and-human-review.md)
- Related requirements: `REQ-001`-`REQ-012`, `REQ-016`-`REQ-021`

The sequence includes normal grounded drafting, validation failure, knowledge gaps, source contradictions, protected intents, prompt injection, unsupported input, and provider/retrieval failure. Every branch ends in validated JSON for a support agent; no branch automatically transmits content to a customer.
