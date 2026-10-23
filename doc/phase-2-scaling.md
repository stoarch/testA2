# Phase 2 Scaling Plan

Phase 2 begins only after the local MVP demonstrates safe behavior and measured value. The target planning volume is 10,000 tickets per month; peak factor, concurrency, SLA, and headroom remain configurable assumptions.

## Target flow

1. Authenticated intake validates schema and assigns an idempotency key.
2. A durable queue decouples intake from stateless processing workers.
3. Workers apply bounded retries with jitter for transient failures.
4. Exhausted or non-retryable failures enter a dead-letter queue and require review.
5. Workers read a pinned, versioned KB/SOP snapshot and configuration ID.
6. Human approval records edits, disposition, reason codes, and feedback.
7. Redacted metrics and audit events support evaluation, rollback, capacity, and cost controls.

## Required production capabilities

| Area | Plan / release gate |
|---|---|
| Queue and workers | Idempotent processing, retry classification, DLQ replay, concurrency limits |
| Knowledge lifecycle | Versioned ingestion, allowlists, hashes, conflict review, snapshot rollback |
| Human approval | Authenticated queue, least privilege, immutable decision history |
| Observability | Latency, errors, route reasons, acceptance/edit rate, tokens/cost; no raw PII in ordinary logs |
| Model/prompt lifecycle | Versioned configuration, evaluation before promotion, canary and rollback |
| Provider controls | Rate limiting, timeout/circuit breaker, regional/data-use review, cost budgets |
| Security/privacy | Encryption, secrets management, retention/deletion, residency, access audit, incident response |
| Load testing | Measured peak factor, p50/p95 latency, saturation, backlog recovery, provider throttling |

## Scale-up triggers

- Queueing is required when synchronous peak demand causes missed latency or provider limits.
- Additional workers are justified by measured backlog and utilization, not average monthly volume alone.
- Semantic/vector retrieval is reconsidered only when corpus growth causes measured lexical-recall failures.
- A production release is blocked until OQ-006 through OQ-008 and privacy/provider controls are resolved.
