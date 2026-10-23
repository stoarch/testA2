# ADR-0007: Pluggable provider abstraction with offline fallback

- Status: Accepted
- Date: 2026-10-23
- Owners: Project team
- Related requirements: `REQ-003`, `REQ-005`, `REQ-013`, `REQ-016`, `REQ-107`, `REQ-108`, `REQ-110`, `REQ-113`
- Related work: `WBS-003`, `WBS-006`, `WBS-007`, `WBS-008`
- Supersedes: None

## Context

The MVP must work without credentials, may optionally demonstrate a live model, and must preserve safety and output contracts when providers change or fail.

## Options considered

### Option A: Provider protocol plus deterministic offline adapter

- Benefits: credential-free demo, repeatable tests, explicit provider metadata, and replaceable live integrations.
- Costs and risks: the offline adapter does not demonstrate live-model quality.

### Option B: Direct calls to one hosted provider

- Benefits: fewer abstractions initially.
- Costs and risks: credentials become mandatory and business logic couples to one SDK.

### Option C: Full orchestration framework

- Benefits: many prebuilt provider integrations.
- Costs and risks: unnecessary dependency surface and reduced transparency.

## Decision

Define narrow classification and drafting provider interfaces. Ship a deterministic offline adapter used by tests and the default demo. Live providers are optional, configuration-selected adapters and must return the same validated contracts plus provider/model/configuration and usage metadata. Provider failures pass through typed errors to safe routing; they never trigger drafting from implicit model memory.

## Consequences

### Positive

- The project is runnable without secrets or network access.
- Tests remain deterministic and cheap.
- Live-provider comparisons use a common evaluation harness.

### Negative

- Adapter contracts require maintenance as provider APIs evolve.
- Offline results cannot be represented as measured live-provider quality.

### Follow-up work

- [ ] Implement the provider protocol and deterministic adapter.
- [ ] Add an opt-in live smoke test that skips without credentials.

## Validation

The offline CLI must complete critical demo journeys without credentials, and a forced provider outage must return a safe, typed, human-routed result.
