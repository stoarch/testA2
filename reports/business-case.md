# Valetax support co-pilot — one-page business case (illustrative)

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
