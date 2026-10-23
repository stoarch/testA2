# Build Valetax Support Ticket Co-Pilot from Scratch

Act as a Staff Software Architect, Senior Python Engineer, QA Architect, and autonomous coding agent.

Your mission is to build a **working, tested, auditable Support Ticket Co-Pilot** for a retail Forex/CFD broker from an empty Git repository.

**Development methodology:** ADR → UML → BDD → TDD → Integration Tests → E2E → Evaluation → Business Case.

**Timebox:** 3–5 hours. Deliver a functioning MVP before investing in advanced infrastructure. Write executable code, not merely documentation or pseudocode.

## 1. Functional requirements

For every incoming support ticket:

1. Classify category, urgency, language, and sentiment.
2. Retrieve relevant evidence from the approved knowledge base.
3. Draft a reply with verifiable citations.
4. Abstain when knowledge is missing, ambiguous, or contradictory.
5. Detect compliance-sensitive requests.
6. Route tickets requiring human review.
7. Return validated structured JSON, including audit metadata.

No automatic transmission of replies to customers.

## 2. Authorized knowledge base

Use only these source pages:

- https://valetax.com/how-to-deposit/
- https://valetax.com/how-to-withdraw/
- https://valetax.com/how-to-open-an-account/
- https://valetax.com/how-to-verify-account/

Fetch and snapshot source content. Store provenance, URL, headings, exact supporting passages, timestamp, and content hash.

Preserve inconsistencies and gaps. Never silently correct source content or invent policies.

If retrieval fails, provide an explicitly labeled offline synthetic-fixture demo. Never claim synthetic fixtures are live source evidence.

## 3. Mandatory compliance rules

- Never provide trading recommendations, signals, price targets, or leverage advice.
- Never decide or predict complaint, KYC, or AML outcomes.
- Never invent fees, timelines, limits, or account policies.
- Every operational factual claim requires valid evidence.
- Detect and resist prompt injection from tickets and retrieved content.
- Always escalate complaints, KYC/AML decisions, unsupported claims, and materially contradictory evidence.
- Protect PII, redact logs, and fail safely when dependencies fail.

Use deterministic pre-generation and post-generation policy checks. Do not rely solely on an LLM for enforcement.

## 4. Technical architecture

Default stack:

- Python 3.12+
- Pydantic for contracts
- Typer or argparse for CLI
- pytest and pytest-bdd
- Ruff
- Section-level lexical retrieval
- Pluggable LLM provider adapter
- Offline deterministic adapter
- JSON/Markdown KB snapshot storage

Avoid unnecessary orchestration frameworks, vector databases, microservices, Kubernetes, and complex UI in Phase 1.

Separate domain models, application services, provider interfaces, infrastructure, and presentation logic.

Implement this processing pipeline:

`Ticket → Validation → Policy Check → Classification → Retrieval → Evidence Validation → Draft → Safety Validation → Routing → Result`

## 5. ADRs

Write at least five Architecture Decision Records in `docs/adr/`.

Every ADR must include context, decision, alternatives, consequences, and status.

Cover:

1. MVP architecture and CLI.
2. KB storage and retrieval strategy.
3. Compliance and human review.
4. LLM provider abstraction and offline fallback.
5. Testing, evaluation, and cost methodology.

## 6. UML

Produce source-controlled PlantUML diagrams:

- Component diagram
- Class diagram
- Sequence diagram with normal/abstain/escalation branches
- Activity or state diagram

Document trust boundaries and module responsibilities.

Keep diagrams synchronized with implemented code.

## 7. BDD first

Create Gherkin specifications and executable step definitions covering at least:

- Valid deposit question with citation.
- Uncovered fee or timeline requiring abstention.
- Trading advice refusal.
- Mixed trading and account-support request.
- Pending KYC decision requiring human review.
- Customer complaint requiring human review.
- Contradictory withdrawal instructions.
- Prompt injection.
- Provider outage.
- Unsupported language or invalid input.

Acceptance criteria must test behavior, not exact nondeterministic LLM wording.

## 8. TDD implementation

Implement vertical slices with:

`RED → GREEN → REFACTOR → COMMIT`

Recommended order:

1. Schemas and CLI.
2. KB ingestion and provenance.
3. Retrieval and citations.
4. Safety and escalation policy.
5. Classification.
6. Grounded drafting and abstention.
7. Provider adapter.
8. Evaluation and observability.

Write failing tests before implementation. Record red/green evidence.

## 9. Integration and E2E

Required:

- Unit tests for business rules and policy.
- Integration tests using a persisted KB snapshot.
- Subprocess E2E tests invoking the real CLI.
- Offline deterministic demo without credentials.
- Optional opt-in live provider smoke test.
- CI lint and tests.

Test both successful grounded replies and safe failures. Clearly distinguish live execution, rules-only operation, and synthetic stubs.

## 10. Quality evaluation

Create at least 30 synthetic evaluation tickets covering routine, risky, contradictory, multilingual, unsupported, and adversarial requests.

Report:

- Classification accuracy.
- Escalation recall and false-escalation rate.
- Trading advice and KYC/AML policy violations.
- Citation validity and unsupported claim rate.
- Abstention frequency.
- Latency p50/p95.
- Token consumption and costs when measured.

Target zero critical policy violations on the evaluation set. Do not present this as proof of universal safety.

## 11. Business case

Create one-page `reports/business-case.md`.

Volume: **10,000 tickets/month**.

Compare three configurations:

A. Deterministic retrieval and template drafts.

B. Guarded LLM-assisted drafting.

C. Hybrid routing with selective LLM usage.

Calculate projected:

- Monthly labor hours saved.
- Human review overhead.
- Token/API spending.
- Infrastructure and maintenance costs.
- Net monthly benefit.
- Break-even acceptance rate or volume.

Provide low/base/high scenarios, explicit assumptions, and one recommended configuration.

Never present estimates as measured savings.

## 12. Phase 2 scaling

Write a realistic architecture plan for:

- Queue-backed intake and workers.
- Idempotency, retries, DLQ.
- Versioned KB/SOP ingestion.
- Human approval and feedback.
- Metrics and audit trails.
- Model/prompt evaluation and rollback.
- Provider rate limiting.
- Security, PII retention, and cost controls.
- Load testing and scale-up triggers.

Do not build Phase 2 infrastructure unless essential to demonstrate the MVP.

## 13. Deliverables

Repository must contain:

- Executable Python package and CLI.
- README and quickstart.
- At least five ADRs.
- Four PlantUML diagrams.
- BDD feature files.
- Unit, integration, and E2E tests.
- KB ingestion and snapshot provenance.
- Synthetic evaluation dataset and metrics.
- One-page business case.
- Phase 2 scaling plan.
- Known limitations and technical walkthrough notes.
- Git commits.

Provide a working demo that shows a grounded answer, abstention, advice refusal, and human escalation.

## 14. Completion protocol

Do not stop after planning or scaffolding.

At each milestone:

1. Verify the code runs.
2. Execute relevant tests.
3. Correct failures.
4. Refactor.
5. Update documentation.
6. Continue to the next vertical slice.

At completion report exactly:

- What was implemented.
- What was simulated.
- What remains planned.
- Tests executed and pass/fail/skip counts.
- Evaluation findings.
- Runtime and cost assumptions.
- Five-minute demo instructions.
- Three highest-priority remaining risks.
- Git commit and repository link, if actually available.

**Start immediately:** inspect the repository, initialize the project, write the first ADR and failing BDD test, and implement the first end-to-end vertical slice.