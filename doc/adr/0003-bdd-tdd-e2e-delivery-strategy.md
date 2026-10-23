# ADR-0003: BDD, TDD, and E2E delivery strategy

- Status: Accepted
- Date: 2026-10-23
- Owners: Project team
- Related requirements: To be assigned by WBS-002
- Related work: `WBS-002`, `WBS-005`, `WBS-007`, `WBS-008`
- Supersedes: None

## Context

The project needs a verification strategy that connects stakeholder intent to implementation feedback and integrated outcome validation. Relying on only unit tests or only E2E tests would leave either behavior alignment or fast diagnostic feedback weak.

## Options considered

### Option A: Layered BDD, TDD, and focused E2E verification

- Benefits: stakeholder-readable acceptance, fast implementation feedback, and confidence in critical integrated journeys.
- Costs and risks: requires traceability and discipline to avoid duplicated tests across layers.

### Option B: E2E-first verification only

- Benefits: tests resemble user behavior.
- Costs and risks: slower, more fragile, and harder to diagnose; business rules receive late feedback.

### Option C: Unit-test-first verification only

- Benefits: fast and precise developer feedback.
- Costs and risks: does not prove stakeholder intent or integration across real boundaries.

## Decision

Use BDD scenarios to define observable acceptance behavior, TDD to implement business rules and components through red-green-refactor, contract tests at owned interfaces, and a deliberately small E2E suite for critical user and operational journeys.

## Consequences

### Positive

- Requirements, tests, and delivery increments share stable identifiers.
- Most failures are caught by fast, focused tests.
- E2E coverage remains focused on high-value cross-boundary risks.

### Negative

- The team must decide the correct verification layer for each behavior.
- Poorly maintained BDD scenarios can become redundant prose.
- Production-like E2E environments require explicit ownership.

### Follow-up work

- [ ] Complete the WBS-002 verification matrix.
- [ ] Define test tooling and CI gates during WBS-006.
- [ ] Define production-like E2E data and environment ownership before WBS-008.

## Validation

The strategy is effective when every Must requirement has readable acceptance behavior, implementation work is covered by deterministic unit/component tests, interface risks have contract coverage, and critical journeys pass E2E without duplicating the entire lower-level suite.

