# ADR-0004: Layered Python MVP with CLI

- Status: Accepted
- Date: 2026-10-23
- Owners: Project team
- Related requirements: `REQ-001`-`REQ-012`, `REQ-016`-`REQ-021`, `REQ-105`
- Related work: `WBS-003`, `WBS-004`, `WBS-006`, `WBS-007`
- Supersedes: None

## Context

The master prompt requires a functioning MVP within 3-5 hours, a real command-line entry point, auditable JSON output, and clear separation between domain rules, application orchestration, external providers, infrastructure, and presentation. Phase 1 must avoid infrastructure that does not directly demonstrate the required behavior.

## Options considered

### Option A: Layered Python package with a synchronous CLI

- Benefits: fast delivery, deterministic local tests, explicit dependency boundaries, and direct subprocess E2E testing.
- Costs and risks: the single-process prototype is not the Phase 2 scaling topology.

### Option B: Web service and browser UI first

- Benefits: richer interaction and a production-like interface.
- Costs and risks: consumes the timebox on transport and UI concerns instead of grounding and safety.

### Option C: Workflow framework or microservices

- Benefits: built-in orchestration primitives.
- Costs and risks: unnecessary operational complexity and weaker visibility into core rules.

## Decision

Build a Python 3.12+ package with domain models, application services, provider protocols, infrastructure adapters, and an argparse or Typer CLI. The synchronous pipeline is:

`Ticket -> Validation -> Policy Check -> Classification -> Retrieval -> Evidence Validation -> Draft -> Safety Validation -> Routing -> Result`

The CLI returns validated structured JSON for agent review and never transmits a reply to a customer.

## Consequences

### Positive

- The MVP remains small enough for red-green-refactor delivery.
- External dependencies are replaceable behind interfaces.
- The real CLI can be exercised through subprocess E2E tests.

### Negative

- Queueing, horizontal workers, and durable audit storage remain Phase 2 work.
- A later service adapter must preserve the same application contracts.

### Follow-up work

- [x] Add Pydantic input/output contracts and the CLI entry point for the implemented classification slice.
- [ ] Add subprocess E2E tests for grounded, abstain, refuse, and escalate paths.

## Validation

The decision is validated when the offline CLI runs without credentials, returns schema-valid JSON, and critical journeys pass subprocess E2E tests.
