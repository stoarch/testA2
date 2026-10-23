# Domain Class Model

- Authoritative source: [domain-class.puml](domain-class.puml)
- Related decisions: [ADR-0004](../adr/0004-mvp-architecture-and-cli.md), [ADR-0005](../adr/0005-kb-snapshot-and-lexical-retrieval.md), [ADR-0007](../adr/0007-provider-abstraction-and-offline-fallback.md)
- Related requirements: `REQ-001`, `REQ-010`, `REQ-020`, `REQ-104`, `REQ-107`

The model distinguishes the implemented Pydantic `SupportTicket` and partial `ProcessingResult` classification contract from planned evidence, snapshot, and provider contracts. Identity plus category, urgency, language, and sentiment are implemented; draft, citation, safety, review, configuration, latency, and usage fields remain planned. Labels prevent planned fields from being mistaken for working code.
