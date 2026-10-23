# Deployment View

- Authoritative source: [deployment.puml](deployment.puml)
- Related decisions: [ADR-0004](../adr/0004-mvp-architecture-and-cli.md), [ADR-0005](../adr/0005-kb-snapshot-and-lexical-retrieval.md), [ADR-0007](../adr/0007-provider-abstraction-and-offline-fallback.md)

Phase 1 is a local Python package and CLI using persisted snapshots and deterministic fixtures. Live-provider use is optional and opt-in. Phase 2 is a plan—not implemented infrastructure—and introduces authenticated intake, queues, idempotent workers, retry/DLQ handling, versioned knowledge, human approval, redacted audit storage, and provider rate limiting.
