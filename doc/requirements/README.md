# Support Co-pilot Requirements Baseline

This baseline derives from [`task-desc.md`](../task-desc.md). It defines a support-ticket co-pilot for a retail forex/CFD broker: ship a demonstrable prototype quickly, then define how it scales to roughly 10,000 tickets per month.

## Documents

| Document | Purpose |
|---|---|
| [Scope and actors](scope-and-actors.md) | Product boundary, users, phases, and exclusions |
| [Functional requirements](functional-requirements.md) | Classification, grounded drafting, citations, abstention, routing, evaluation, and business case |
| [Non-functional requirements](non-functional-requirements.md) | Safety, grounding, auditability, scale, maintainability, and prototype constraints |
| [BDD scenarios](../../bdd/README.md) | Acceptance examples for normal and safety-critical behavior |
| [Knowledge-base assessment](knowledge-base.md) | Required pages, known gaps, overlap, and inconsistencies |
| [Business case](business-case.md) | One-page decision model and required configuration comparison |
| [Verification matrix](verification-matrix.md) | BDD/TDD/contract/E2E/quality allocation |
| [Risks and open questions](risks-and-open-questions.md) | Assumptions, risks, decisions still needed |
| [Approval](approval.md) | Baseline status and review evidence |

## Priority convention

- Must: required by the source brief or a direct safety consequence.
- Should: valuable for a credible prototype or scale plan, but not explicitly mandatory.
- Could: optional within the 3–5 hour timebox.
- Won't now: explicitly outside WBS-002 or Phase 1.

