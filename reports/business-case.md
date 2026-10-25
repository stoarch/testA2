# Valetax Support Co-Pilot Business Case

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
- **Total Operating Cost**: $31,550 / month ($3.16 / ticket).
- **Net Monthly Savings**: **$8,450 / month** ($101,400 / year).

### Configuration B: Guarded Generative LLM Engine (Phase 2 Production Strategy)
- **Mechanism**: Vector RAG retrieval, generative LLM drafting with guardrails, automated safety filtering.
- **Draft Acceptance Rate**: 60% (6,000 tickets auto-drafted; 1.5 min review time).
- **Human Escalation Rate**: 40% (4,000 tickets escalated to 8 min human handling).
- **Assisted Labor Hours**: (6,000 × 1.5 min / 60) + (4,000 × 8 min / 60) = **683.3 hours/month** ($20,500 labor).
- **API Token Expense**: 10,000 tickets × 1,500 tokens @ $0.002 / 1,000 tokens = $300 / month.
- **Platform Maintenance & Infra**: $700 / month.
- **Total Operating Cost**: $21,500 / month ($2.15 / ticket).
- **Net Monthly Savings**: **$18,500 / month** ($222,000 / year).

### Configuration C: Hybrid Selective System (Phase 2 Recommended Strategy)
- **Mechanism**: Deterministic rules handle routine deposit/withdrawal (30% tickets, 1 min check); Guarded LLM handles general queries (45% tickets, 2 min check); Unsafe/complex cases escalated directly (25% tickets, 8 min handling).
- **Assisted Labor Hours**: (3,000 × 1 min / 60) + (4,500 × 2 min / 60) + (2,500 × 8 min / 60) = **533.3 hours/month** ($16,000 labor).
- **API Token Expense**: 4,500 LLM calls × 1,500 tokens @ $0.002 / 1,000 tokens = $135 / month.
- **Platform Maintenance & Infra**: $600 / month.
- **Total Operating Cost**: $16,735 / month ($1.67 / ticket).
- **Net Monthly Savings**: **$23,265 / month** ($279,180 / year).

---

## 3. Financial Summary & Decision Recommendation

| Metric | Baseline | Config A (Phase 1) | Config B (LLM) | Config C (Hybrid) |
|---|---|---|---|---|
| Monthly Labor Hours | 1,333.3 h | 1,041.7 h | 683.3 h | 533.3 h |
| Monthly Labor Cost | $40,000 | $31,250 | $20,500 | $16,000 |
| Monthly API & Infra Cost | $0 | $300 | $1,000 | $735 |
| **Total Monthly Cost** | **$40,000** | **$31,550** | **$21,500** | **$16,735** |
| **Cost per Ticket** | **$4.00** | **$3.16** | **$2.15** | **$1.67** |
| **Net Monthly Savings** | **$0** | **+$8,450** | **+$18,500** | **+$23,265** |
| **Annualized ROI** | **N/A** | **$101,400** | **$222,000** | **$279,180** |

### Justified Recommendation
Running the system at 10,000 tickets/month is **economically justified**:
1. **Immediate Phase 1 Deployment (Config A)** yields **$8,450/month net savings** with zero LLM API dependency and strict zero-hallucination guarantees.
2. **Phase 2 Expansion (Config C - Hybrid)** delivers maximum projected savings of **$23,265/month (58% cost reduction)** while retaining fail-closed deterministic safety routing for regulated Forex/CFD requests.
