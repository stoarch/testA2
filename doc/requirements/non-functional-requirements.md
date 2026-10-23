# Non-Functional Requirements

## REQ-101: Safety-rule recall

- Type: Quality — Safety
- Priority: Must
- Limit: 100% of labeled trading-advice, complaint-decision, KYC-decision, and AML-decision test cases trigger the required refusal or human route; zero cases contain a prohibited decision/advice statement.
- Verification: Deterministic safety test suite plus manual review.
- Basis: The source uses “Never,” making misses unacceptable in the acceptance set.

## REQ-102: Grounding integrity

- Type: Quality — Correctness
- Priority: Must
- Limit: 100% of policy, fee, timeline, process, and eligibility claims in the acceptance set are supported by cited approved-source passages; unsupported cases abstain.
- Verification: Claim-to-citation review and adversarial gap cases.

## REQ-103: Citation integrity

- Type: Quality — Auditability
- Priority: Must
- Limit: Every non-abstaining draft has at least one resolvable citation; every citation identifies the source page and supporting passage/chunk.
- Verification: Citation validator and manual spot check.

## REQ-104: Required-output completeness

- Type: Quality — Reliability
- Priority: Must
- Limit: 100% of successful processing results contain all fields required by REQ-010; failures return a typed safe-error result.
- Verification: Output-schema tests.

## REQ-105: Prototype timebox

- Type: Constraint — Delivery
- Priority: Must
- Limit: Phase 1 scope must be achievable within 3–5 hours; mocks and stubs must explicitly state production replacements.
- Verification: Repository review and walkthrough.

## REQ-106: Volume model

- Type: Quality — Scalability
- Priority: Must for Phase 2 design
- Limit: Capacity and cost calculations use at least 10,000 tickets/month; peak factor and headroom remain explicit configurable assumptions rather than hidden constants.
- Verification: Load/cost model review; later load test.

## REQ-107: Provider configurability

- Type: Quality — Maintainability
- Priority: Should
- Limit: Business logic and evaluation records identify model/provider/configuration explicitly; replacing the provider does not change safety-rule definitions or output schema.
- Verification: Component tests and configuration review.

## REQ-108: Observability

- Type: Quality — Operability
- Priority: Must
- Limit: Each processed ticket records latency, token/usage data when available, configuration ID, route/abstention reason, and error type without logging unnecessary customer content.
- Verification: Structured-output/log tests.

## REQ-109: Privacy and data minimization

- Type: Quality — Privacy
- Priority: Must for production design
- Limit: The design sends and stores only fields needed for support processing/evaluation; retention, redaction, access, and provider data-use controls must be decided before production.
- Verification: Data-flow and production-readiness review.

## REQ-110: Measured latency and quality

- Type: Quality — Performance
- Priority: Must
- Limit: Phase 1 reports observed end-to-end p50/p95 latency and quality metrics rather than inventing an SLA; the Phase 2 SLA is an open operational decision.
- Verification: Evaluation report.

