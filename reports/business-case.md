# Valetax support co-pilot — one-page business case (illustrative)

## PR #2 comparative projection

The following three-configuration projection uses explicit, non-measured assumptions to preserve the prototype's token and labor calculations. It is not a claim of measured savings.

- **Status**: Completed Take-Home Economic Evaluation
- **Target Volume**: 10,000 support tickets / month
- **Baseline Cost**: $40,000 / month ($4.00 / ticket)
- **Evidence Label**: *All labor rates, handling times, auto-resolution rates, and token costs are non-measured modeling assumptions for prototype evaluation.*

---

## 1. Baseline Human Support Operations (No AI Assistance)

| Parameter | Modeling Assumption | Monthly Total |
|---|---|---|
| Monthly Ticket Volume | 10,000 tickets | 10,000 tickets |
| Average Handling Time (AHT) | 8 minutes / ticket | 1,333.3 hours |
| Fully Loaded Support Labor Rate | $30.00 / hour | $40,000 / month |
| **Baseline Cost per Ticket** | **$4.00 / ticket** | **$40,000 / month** |

---

## 2. Operating Configurations Compared (10,000 Tickets/Month)

### Configuration A: Deterministic Offline Engine (Phase 1 Implemented Prototype)
- **Mechanism**: Rule-based classification, exact citation matching, deterministic safety routing, offline synthetic KB.
- **Draft Acceptance Rate**: 25% (2,500 tickets auto-drafted; review time reduced from 8 min to 1 min).
- **Human Escalation Rate**: 75% (7,500 tickets routed to full 8 min human handling).
- **Assisted Labor Hours**: (2,500 × 1 min / 60) + (7,500 × 8 min / 60) = **1,041.7 hours/month** ($31,250 labor).
- **API Token Expense**: $0.00 (offline local processing).
- **Platform Maintenance & Infra**: $300 / month.
- **Total Operating Cost**: **$31,550 / month** ($3.16 / ticket).
- **Net Monthly Savings**: **$8,450 / month** ($101,400 / year).

### Configuration B: Guarded Generative LLM Engine (Phase 2 Production Strategy)
- **Mechanism**: Vector RAG retrieval, generative LLM drafting with guardrails, automated safety filtering.
- **Draft Acceptance Rate**: 60% (6,000 tickets auto-drafted; 1.5 min review time).
- **Human Escalation Rate**: 40% (4,000 tickets escalated to 8 min human handling).
- **Assisted Labor Hours**: (6,000 × 1.5 min / 60) + (4,000 × 8 min / 60) = **683.3 hours/month** ($20,500 labor).
- **API Token Expense**: 10,000 tickets × 1,500 tokens = 15,000,000 tokens @ $0.002 / 1,000 tokens = $30.00 / month.
- **Platform Maintenance & Infra**: $700 / month.
- **Total Operating Cost**: **$21,230 / month** ($2.12 / ticket).
- **Net Monthly Savings**: **$18,770 / month** ($225,240 / year).

### Configuration C: Hybrid Selective System (Phase 2 Recommended Strategy)
- **Mechanism**: Deterministic rules handle routine deposit/withdrawal (30% tickets, 1 min check); Guarded LLM handles general queries (45% tickets, 2 min check); Unsafe/complex cases escalated directly (25% tickets, 8 min handling).
- **Assisted Labor Hours**: (3,000 × 1 min / 60) + (4,500 × 2 min / 60) + (2,500 × 8 min / 60) = **533.3 hours/month** ($16,000 labor).
- **API Token Expense**: 4,500 LLM calls × 1,500 tokens = 6,750,000 tokens @ $0.002 / 1,000 tokens = $13.50 / month.
- **Platform Maintenance & Infra**: $600 / month.
- **Total Operating Cost**: **$16,613.50 / month** ($1.66 / ticket).
- **Net Monthly Savings**: **$23,386.50 / month** ($280,638 / year).

---

## 3. Financial Summary & Decision Recommendation

| Metric | Baseline | Config A (Phase 1) | Config B (LLM) | Config C (Hybrid) |
|---|---|---|---|---|
| Monthly Labor Hours | 1,333.3 h | 1,041.7 h | 683.3 h | 533.3 h |
| Monthly Labor Cost | $40,000 | $31,250 | $20,500 | $16,000 |
| Monthly API & Infra Cost | $0 | $300 | $730 | $613.50 |
| **Total Monthly Cost** | **$40,000** | **$31,550** | **$21,230** | **$16,613.50** |
| **Cost per Ticket** | **$4.00** | **$3.16** | **$2.12** | **$1.66** |
| **Net Monthly Savings** | **$0** | **+$8,450** | **+$18,770** | **+$23,386.50** |
| **Annualized Net Savings** | **N/A** | **$101,400** | **$225,240** | **$280,638** |

### Justified Recommendation
Running the co-pilot system at 10,000 tickets/month is **economically justified**:
1. **Immediate Phase 1 Deployment (Config A)** yields **$8,450/month net savings** with zero LLM API dependency and strict zero-hallucination guarantees.
2. **Phase 2 Expansion (Config C - Hybrid)** delivers maximum projected savings of **$23,386.50/month (58% cost reduction)** while retaining fail-closed deterministic safety routing for regulated Forex/CFD requests.

## Conservative pilot-gate model from `main`

This second model intentionally uses more conservative assumptions as a decision gate. It complements, rather than replaces, the comparative projection above.

**Decision:** At 10,000 tickets/month, pilot **A: deterministic/extractive assist with mandatory human approval** first. Evaluate **C: hybrid** as the scale-up candidate only after measured quality, acceptance, and review-time data. Do not infer savings from synthetic tests.

## Inputs and assumptions (not measured Valetax data)

- Monthly tickets: **10,000**; baseline handling time: **6 min/ticket**; fully loaded support cost: **$15/hour**.
- Assumed share of tickets eligible for useful drafts: **60%**; no staffing reduction is assumed. Savings represent recoverable staff capacity, not guaranteed cash savings.
- The configurations below assume no automated sending and humans retain KYC/AML/complaint decisions.
- Cost estimates for provider/infrastructure/maintenance are **scenario assumptions**, not vendor quotes or measured tokens.

| Configuration | Accepted useful drafts as % of all tickets | Net minutes saved per accepted draft (including review/edit) | Monthly saved hours | Labor capacity value | Monthly run + maintenance cost | Net monthly value |
|---|---:|---:|---:|---:|---:|---:|
| A: Deterministic templates/extractive (Phase 1) | 30% | 2.5 | 125 | $1,875 | $650 | **+$1,225** |
| B: Guarded LLM drafts on eligible tickets | 42% | 3.0 | 210 | $3,150 | $1,700 | **+$1,450** |
| C: Hybrid deterministic + selective LLM (Phase 2 candidate) | 40% | 3.0 | 200 | $3,000 | $1,100 | **+$1,900** |

**Formula:** `net/month = 10,000 × accepted_fraction × net_minutes_saved / 60 × $15 − monthly_run_cost`. These are alternative scenarios, not additive benefits. Baseline labor time is `10,000 × 6 / 60 = 1,000 hours/month` ($15,000/month). The 60% eligible-share assumption caps the accepted fractions above.

**Break-even accepted-ticket fraction:** A **10.4%**, B **22.7%**, C **14.7%**, at each configuration's net saved minutes and cost. If the acceptance rate or handling-time benefit falls short, the configuration may not pay for itself.

**A sensitivity at 10,000 tickets/month:** pessimistic `15% × 1.5 min` => $562.50 capacity value − $650 = **−$87.50/month**; base **+$1,225/month**; optimistic `45% × 3 min` => $3,375 − $650 = **+$2,725/month**. The estimates intentionally exclude one-off development costs and safety-error losses, which should be tracked separately in pilot evaluation.

## Operational gate

Run an agent-in-the-loop pilot, **never customer-autosend**. Label ≥30 representative cases, including unsupported policy, conflict, injection, multilingual, and prohibited financial advice. Measure grounded citation validity, critical safety violations, classification, abstention/route precision-recall, agent acceptance/edit time, p50/p95 latency, actual tokens and provider prices. **Do not launch without zero observed critical violations on the pilot set, an explicit human override, and compliance approval**; zero in a small set is not proof of safety. Choose C over A only if measured extra value exceeds its extra costs while maintaining safety. At 10,000/month (~333/day), start with a simple worker; add queue, idempotency, retries, audit store and KB versioning only when peaks/SLA require them.
