# Assumptions, Risks, and Open Questions

## Assumptions

| ID | Assumption | Basis |
|---|---|---|
| ASM-001 | Phase 1 is an agent-assist tool, not autonomous customer messaging. | Human-review requirement and minimal demo scope |
| ASM-002 | The four English Valetax URLs are the only approved KB sources for the prototype. | Source brief |
| ASM-003 | The challenge evaluates architecture reasoning and measurable tradeoffs more than production completeness. | Timebox, mocks/stubs, technical walkthrough |
| ASM-004 | The 10,000 tickets/month figure is average volume, not peak throughput. | Wording in source; peak is unspecified |

## Risks

| ID | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| RISK-001 | LLM drafts unsupported policy or timelines | Medium | Critical | Claim/citation validation, abstention, human route |
| RISK-002 | Trading advice bypasses simple keyword detection | Medium | Critical | Diverse adversarial set, defense in depth, output filter |
| RISK-003 | Complaint/KYC/AML language is ambiguous | Medium | Critical | Conservative routing and explicit reason codes |
| RISK-004 | Live KB changes make evaluations irreproducible | High | High | Snapshot/version sources with retrieval timestamp |
| RISK-005 | KB wording is conflicting or misleading | High | High | Surface conflicts and abstain rather than reconcile silently |
| RISK-006 | Business case overstates savings | Medium | High | Use measured acceptance/review rates and sensitivity ranges |
| RISK-007 | Customer ticket data reaches a provider under unclear controls | Medium | Critical | Redaction/minimization and production provider review |
| RISK-008 | Average monthly volume hides peaks | Medium | Medium | Make peak factor/headroom explicit in Phase 2 design |
| RISK-009 | Ticket or retrieved content attempts prompt injection | High | Critical | Treat content as data; deterministic pre/post gates; adversarial evaluation |
| RISK-010 | Synthetic fixtures are mistaken for live evidence or measured provider quality | Medium | High | Mandatory execution-mode and synthetic provenance labels |
| RISK-011 | Logs retain raw customer text or PII | Medium | Critical | Redacted structured telemetry and artifact scanning |

## Open questions

| ID | Priority | Question | Blocks |
|---|---|---|---|
| OQ-001 | P1 | Which urgency and sentiment label sets are expected? | Final evaluation schema |
| OQ-002 | P1 | Must all Phase 1 outputs be human-reviewed, or only routed cases? | Workflow and business case |
| OQ-003 | P1 | What confidence thresholds trigger review, and how are they calibrated? | Routing policy |
| OQ-004 | P1 | What labeled evaluation tickets are available, and may synthetic cases supplement them? | Evaluation validity |
| OQ-005 | P1 | What are baseline handling time, loaded labor cost, and draft acceptance assumptions? | Monetary business case |
| OQ-006 | P1 | What peak factor, SLA, concurrency, and headroom are required for Phase 2? | Scale architecture |
| OQ-007 | P0 before production | What customer-data retention, redaction, access, residency, and provider-use rules apply? | Production release |
| OQ-008 | P0 before production | Who owns KB authority and resolves conflicts between pages/SOPs? | Production grounding policy |

These questions do not block the 3–5 hour prototype if they remain explicit and mocked/configurable. OQ-007 and OQ-008 block production deployment.

