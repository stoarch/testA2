# Functional Requirements

## REQ-001: Accept a support ticket

- Type: Functional
- Priority: Must
- Source: Scenario — each incoming ticket
- Statement: The co-pilot shall accept ticket text plus an identifier and shall return a structured result tied to that identifier.
- Acceptance evidence: [SCN-001](../../bdd/scenarios/SCN-001.md)

## REQ-002: Classify ticket category

- Type: Functional
- Priority: Must
- Source: “Classify it: category”
- Statement: The co-pilot shall classify the ticket as deposit, withdrawal, account opening, account verification, or other/unknown.
- Acceptance evidence: [SCN-002](../../bdd/scenarios/SCN-002.md), [SCN-003](../../bdd/scenarios/SCN-003.md)

## REQ-003: Classify urgency, language, and sentiment

- Type: Functional
- Priority: Must
- Source: “urgency, language, sentiment”
- Statement: The co-pilot shall return explicit urgency, detected language, and sentiment fields for every processed ticket.
- Acceptance evidence: [SCN-004](../../bdd/scenarios/SCN-004.md)

## REQ-004: Retrieve from the approved knowledge base

- Type: Functional
- Priority: Must
- Source: Four public Valetax help pages
- Statement: The co-pilot shall retrieve supporting passages only from the configured approved knowledge-base documents and preserve their source URL/title.
- Acceptance evidence: [SCN-005](../../bdd/scenarios/SCN-005.md)

## REQ-005: Draft a grounded reply with citations

- Type: Functional
- Priority: Must
- Source: “Draft a reply grounded in the knowledge base, with citations”
- Statement: When the approved sources support an answer, the co-pilot shall draft a reply whose policy, fee, timeline, process, and eligibility claims are supported by cited source passages.
- Acceptance evidence: [SCN-006](../../bdd/scenarios/SCN-006.md), [SCN-007](../../bdd/scenarios/SCN-007.md)

## REQ-006: Abstain when coverage is insufficient

- Type: Functional
- Priority: Must
- Source: “or abstain when the knowledge base does not cover it”
- Statement: When sources do not support a complete safe answer, the co-pilot shall state that the answer is unknown or insufficiently covered and shall not fill the gap from model knowledge.
- Acceptance evidence: [SCN-008](../../bdd/scenarios/SCN-008.md), [SCN-009](../../bdd/scenarios/SCN-009.md)

## REQ-007: Refuse trading advice

- Type: Functional
- Priority: Must
- Source: Hard rule — never give trading advice
- Statement: The co-pilot shall detect requests for buy/sell recommendations, signals, price targets, leverage suggestions, or equivalent personalized trading guidance; it shall decline politely and route for human review without providing the requested advice.
- Acceptance evidence: [SCN-010](../../bdd/scenarios/SCN-010.md), [SCN-011](../../bdd/scenarios/SCN-011.md)

## REQ-008: Avoid complaint, KYC, and AML decisions

- Type: Functional
- Priority: Must
- Source: Hard rule — never decide complaint, KYC, or AML outcomes
- Statement: The co-pilot shall not approve, reject, uphold, deny, or otherwise decide a complaint, KYC review, or AML review; it may draft an acknowledgement and shall route the ticket to a person.
- Acceptance evidence: [SCN-012](../../bdd/scenarios/SCN-012.md), [SCN-013](../../bdd/scenarios/SCN-013.md)

## REQ-009: Route required cases to a human

- Type: Functional
- Priority: Must
- Source: “Route to a human reviewer whenever required” plus hard rules
- Statement: The co-pilot shall set `human_review_required=true` with reason codes for trading-advice requests, complaints, KYC/AML cases, abstentions, source conflicts, processing errors, and any configured low-confidence case.
- Acceptance evidence: [SCN-014](../../bdd/scenarios/SCN-014.md), [SCN-015](../../bdd/scenarios/SCN-015.md)

## REQ-010: Expose evidence and decision metadata

- Type: Functional
- Priority: Must
- Source: Citation, measurement, and human-review needs
- Statement: Each result shall include ticket ID, classifications, draft/abstention, citations, safety flags, human-review decision/reasons, model/configuration ID, and processing measurements.
- Acceptance evidence: [SCN-016](../../bdd/scenarios/SCN-016.md)

## REQ-011: Preserve source gaps and conflicts

- Type: Functional
- Priority: Must
- Source: “Use them as they are, including gaps, overlaps and inconsistencies”
- Statement: The system shall not silently reconcile conflicting knowledge-base claims; it shall surface the conflicting sources, abstain from the disputed claim, and route to review.
- Acceptance evidence: [SCN-017](../../bdd/scenarios/SCN-017.md)

## REQ-012: Provide a minimal agent interface

- Type: Functional
- Priority: Must
- Source: Minimal CLI or simple web page is enough
- Statement: Phase 1 shall provide a CLI or simple web interface that accepts a ticket and displays the complete structured result.
- Acceptance evidence: [SCN-018](../../bdd/scenarios/SCN-018.md)

## REQ-013: Evaluate configurations

- Type: Functional
- Priority: Must
- Source: “measure it” and business-case configuration question
- Statement: The prototype shall run a labeled evaluation set against at least one configuration and report classification quality, safety-rule outcomes, grounding/citation outcomes, abstention/review rate, latency, and estimated cost.
- Acceptance evidence: [SCN-019](../../bdd/scenarios/SCN-019.md)

## REQ-014: Produce the one-page business case

- Type: Functional
- Priority: Must
- Source: Business case in numbers
- Statement: The project shall produce a one-page comparison that answers whether the co-pilot is worth running at 10,000 tickets per month and identifies the recommended measured configuration.
- Acceptance evidence: [SCN-020](../../bdd/scenarios/SCN-020.md)

## REQ-015: Support knowledge-base growth

- Type: Functional
- Priority: Should
- Source: Phase 2 — KB and SOPs expand
- Statement: The scale design shall separate ingestion/indexing from ticket processing and shall support adding/versioning documents without rewriting core classification or safety logic.
- Acceptance evidence: Architecture and design review

## REQ-016: Handle dependency failure safely

- Type: Functional
- Priority: Must
- Source: Direct safety consequence of required LLM/KB processing
- Statement: On model, retrieval, parsing, or citation-validation failure, the co-pilot shall return a safe error result, draft no unsupported answer, and require human review.
- Acceptance evidence: [SCN-021](../../bdd/scenarios/SCN-021.md)

