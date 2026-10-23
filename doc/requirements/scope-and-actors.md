# Scope and Actors

## Problem

Support agents repeatedly answer questions about deposits, withdrawals, account opening, and account verification. Answers must remain grounded in a small, imperfect knowledge base and must not cross regulated or safety-sensitive boundaries.

## Product outcome

For each incoming ticket, produce structured classification, a cited knowledge-grounded draft or explicit abstention, and a human-review decision. Measure quality, safety, latency, and cost, then state whether operation is worthwhile at approximately 10,000 tickets per month and under which configuration.

## Actors

| Actor | Goal / responsibility |
|---|---|
| Support agent / human reviewer | Review classification, citations, abstentions, and drafts; edit or approve before customer use where required |
| Support operations lead | Own routing policy, quality thresholds, staffing assumptions, and rollout decision |
| Customer | Submits a support ticket and ultimately receives a human-approved or policy-safe response |
| Compliance / risk reviewer | Defines and reviews complaint, KYC, AML, and trading-advice boundaries |
| Product/engineering team | Builds, evaluates, operates, and improves the co-pilot |
| Knowledge-base owner | Maintains approved source pages and resolves gaps or conflicts |

## Phase 1: ship ASAP

- Minimal CLI or simple web page
- Python preferred; provider-agnostic LLM integration
- Four specified public Valetax pages as the knowledge base
- Mocks/stubs allowed when production behavior is explained
- Ticket classification, grounded cited draft or abstention, and human routing
- Evaluation evidence and a one-page business case
- Work completed within the 3–5 hour challenge timebox

## Phase 2: scale up

- Sustain around 10,000 tickets per month with headroom defined during design
- Expand knowledge sources and SOPs without prompt-only rewrites
- Add robust ingestion/versioning, queues, observability, audit retention, security, and failure recovery
- Tune configuration using measured quality, latency, cost, and review-rate evidence

## Out of scope

- Autonomous customer sending unless explicitly approved later
- Trading recommendations, signals, price targets, or leverage suggestions
- Complaint, KYC, or AML decisions
- Policy, fee, or timeline claims absent from the approved knowledge base
- Trading execution, deposits, withdrawals, account opening, or KYC processing
- A production-scale implementation inside the 3–5 hour Phase 1 timebox

