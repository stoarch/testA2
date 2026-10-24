# Domain Class Model

- Authoritative source: [domain-class.puml](domain-class.puml)
- Related decisions: [ADR-0004](../adr/0004-mvp-architecture-and-cli.md), [ADR-0005](../adr/0005-kb-snapshot-and-lexical-retrieval.md), [ADR-0007](../adr/0007-provider-abstraction-and-offline-fallback.md)
- Related requirements: `REQ-001`, `REQ-010`, `REQ-020`, `REQ-104`, `REQ-107`

The model distinguishes implemented Pydantic ticket/classification, synthetic snapshot/retrieved-passage, extractive draft/citation, abstention, safety-routing, and configured confidence-routing contracts from planned provider and full-result contracts. Snapshot loading, hashing, allowlist filtering, persistence, section retrieval, evidence-derived deposit drafting, exact timeline validation, fee/verification abstention with canonical insufficient-knowledge routing, direct-buy/leverage refusal, explicit KYC/complaint outcome routing, and strict below-threshold confidence routing are implemented. Live fetching plus general citation validation, confidence calibration, broader safety/review routing, complete configuration, latency, usage, and CLI draft integration remain planned.
