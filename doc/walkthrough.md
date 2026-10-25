# Technical Walkthrough & Evaluation Guide

## 1. Quick Technical Overview

The **Valetax Support Co-Pilot** is an agent-assist prototype designed to assist retail Forex/CFD customer support teams. It classifies support tickets, retrieves verified evidence from allowlisted knowledge sources, generates cited response drafts, and enforces safety boundaries by escalating sensitive or unsupported queries to human reviewers.

Key Architectural Guarantees:
- **Fail-Closed Safety**: Requests involving trading advice, price targets, trading signals, personalized leverage, KYC outcomes, or complaints are routed to human review with explicit review reasons.
- **Strict Evidence Grounding**: Answers are generated only when supported by approved knowledge base passages. Unsupported operations (such as deposit cancellation or unknown fees/limits) trigger an explicit abstention.
- **Deterministic Offline Processing**: Built with Python 3.12+ and Pydantic v2, operating credential-free and offline without external LLM dependencies.

---

## 2. Five-Minute Reviewer Demonstration

Run the five CLI demonstration commands to verify all core ticket processing outcomes:

### Outcome 1: Grounded Operational Answer with Citation
```bash
support-copilot --ticket-id DEMO-001 --text "How do I make a deposit?" --kb-snapshot tests/fixtures/kb/synthetic_snapshot.json
```
*Expected Result*: Returns `answer_status: "drafted"`, extractive deposit instructions, and a structured citation pointing to `https://valetax.com/how-to-deposit/`.

### Outcome 2: Abstention for Unsupported Policy (Deposit Cancellation)
```bash
support-copilot --ticket-id DEMO-002 --text "Can I cancel my deposit?" --kb-snapshot tests/fixtures/kb/synthetic_snapshot.json
```
*Expected Result*: Returns `answer_status: "abstained"`, `human_review_required: true`, and `review_reasons: ["insufficient_knowledge"]`.

### Outcome 3: Refusal of Prohibited Trading Advice
```bash
support-copilot --ticket-id DEMO-003 --text "Should I buy EUR/USD?" --kb-snapshot tests/fixtures/kb/synthetic_snapshot.json
```
*Expected Result*: Returns `answer_status: "refused"`, polite refusal message without financial advice, `safety_flags: ["trading_advice"]`, and `human_review_required: true`.

### Outcome 4: Human Escalation for KYC Outcome Request
```bash
support-copilot --ticket-id DEMO-004 --text "Please approve my KYC verification." --kb-snapshot tests/fixtures/kb/synthetic_snapshot.json
```
*Expected Result*: Returns `answer_status: "routed"`, neutral acknowledgement, `safety_flags: ["kyc_decision"]`, and `review_reasons: ["KYC"]`.

### Outcome 5: Aggregate Offline Evaluation Report
```bash
support-copilot --evaluation-set tests/fixtures/evaluation/synthetic_evaluation_set.json --kb-snapshot tests/fixtures/kb/synthetic_snapshot.json
```
*Expected Result*: Emits aggregate metrics covering classification accuracy, safety accuracy, grounding accuracy, review rate, latency, and cost availability.

---

## 3. Business Case Summary

The complete economic analysis for 10,000 tickets/month is located in [`reports/business-case.md`](../reports/business-case.md).

Key Findings:
- **Baseline (Human-Only)**: $40,000 / month ($4.00 / ticket at 8 min AHT).
- **Configuration A (Deterministic Prototype - Phase 1)**: $31,550 / month ($3.16 / ticket) -> **$8,450 / month net savings ($101.4k/year)**.
- **Configuration C (Hybrid - Phase 2 Recommended)**: $16,735 / month ($1.67 / ticket) -> **$23,265 / month net savings ($279.2k/year)**.

---

## 4. Test Verification Suite

Execute the full verification suite:

```bash
# 1. Run all Pytest unit, integration, and E2E tests
uv run pytest -q

# 2. Run implemented Behave BDD feature scenarios
uv run behave bdd/features --tags=@must

# 3. Validate Gherkin specification parity
uv run python bdd/validate_gherkin.py

# 4. Validate Architecture Decisions and PlantUML models
uv run python scripts/validate_architecture_docs.py

# 5. Code quality and formatting checks
uv run ruff check src tests bdd/features/steps
```
