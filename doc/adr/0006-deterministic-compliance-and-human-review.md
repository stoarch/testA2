# ADR-0006: Deterministic compliance gates and human review

- Status: Accepted
- Date: 2026-10-23
- Owners: Project team
- Related requirements: `REQ-006`-`REQ-011`, `REQ-016`-`REQ-019`, `REQ-021`, `REQ-101`, `REQ-102`, `REQ-109`, `REQ-111`, `REQ-112`
- Related work: `WBS-003`, `WBS-004`, `WBS-007`, `WBS-008`
- Supersedes: None

## Context

The co-pilot operates in a regulated support setting. Trading advice, complaint/KYC/AML decisions, unsupported operational claims, prompt injection, source conflicts, and dependency failure cannot be controlled solely through model instructions.

## Options considered

### Option A: Deterministic pre-generation and post-generation gates

- Benefits: defense in depth, testable reason codes, conservative failure behavior, and independence from provider behavior.
- Costs and risks: rules require maintenance and cannot detect every semantic variation.

### Option B: Prompt-only guardrails

- Benefits: minimal implementation effort.
- Costs and risks: vulnerable to prompt injection, model drift, and nondeterministic misses.

### Option C: Route every ticket without drafting

- Benefits: lowest automation risk.
- Costs and risks: provides little agent-assist value and cannot support the business-case evaluation.

## Decision

Apply deterministic input validation and policy detection before retrieval or generation. Treat ticket text and retrieved content as untrusted data. After drafting, validate prohibited content, evidence coverage, citations, and structured output. Any complaint, KYC/AML decision request, trading advice request, unsupported claim, material conflict, injection signal, invalid input, or dependency failure produces a typed safe result and human-review reason. No path automatically sends customer-facing content.

## Consequences

### Positive

- Critical policy behavior is directly unit-testable.
- Human routing is auditable through stable reason codes.
- Provider outages and unsafe drafts fail closed.

### Negative

- Conservative rules may increase false escalations.
- The evaluation set must evolve as bypass patterns are discovered.

### Follow-up work

- [ ] Define policy reason codes and adversarial fixtures.
- [ ] Verify zero critical violations on the labeled evaluation set.

## Validation

All labeled critical cases must refuse or escalate with no prohibited output, and the evaluation report must disclose both recall and false-escalation rate.
