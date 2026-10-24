# Valetax Support Co-Pilot Business Case

- Status: no-go
- Planning volume: 10,000 tickets/month
- Evidence rule: financial outputs are modeled estimates, not measured savings

## Recommendation

**No configuration is justified for deployment yet.**

- Configuration A: measured set has 4 cases; at least 30 are required.
- Configuration B: quality and safety results are not measured.
- Configuration C: quality and safety results are not measured.

## Base-case comparison

| Configuration | Evidence | Accepted drafts | Review hours | Labor value | Run cost | Net value | Cost/ticket | Break-even acceptance |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| A - Deterministic retrieval and template drafts | measured offline fixture | 2,600 | 375.0 | USD 6,500.00 | USD 1,400.00 | USD 5,100.00 | USD 0.14 | 14.0% |
| B - Guarded LLM-assisted drafting | not measured | 3,575 | 300.0 | USD 8,937.50 | USD 2,800.00 | USD 6,137.50 | USD 0.28 | 20.4% |
| C - Hybrid routing with selective LLM usage | not measured | 3,960 | 275.0 | USD 10,890.00 | USD 2,060.00 | USD 8,830.00 | USD 0.21 | 13.6% |

## Low/base/high sensitivity

| Config | Case | Eligible | Acceptance | Review rate | Hours saved | Monthly cost | Monthly net value |
|---|---|---:|---:|---:|---:|---:|---:|
| A | low | 25% | 50% | 85% | 83.3 | USD 1,100.00 | USD 1,400.00 |
| A | base | 40% | 65% | 75% | 216.7 | USD 1,400.00 | USD 5,100.00 |
| A | high | 55% | 75% | 65% | 446.9 | USD 1,700.00 | USD 11,706.25 |
| B | low | 35% | 45% | 80% | 105.0 | USD 3,100.00 | USD 50.00 |
| B | base | 55% | 65% | 60% | 297.9 | USD 2,800.00 | USD 6,137.50 |
| B | high | 70% | 78% | 45% | 591.5 | USD 2,600.00 | USD 15,145.00 |
| C | low | 35% | 55% | 75% | 144.4 | USD 2,190.00 | USD 2,141.25 |
| C | base | 55% | 72% | 55% | 363.0 | USD 2,060.00 | USD 8,830.00 |
| C | high | 70% | 82% | 40% | 650.5 | USD 1,990.00 | USD 17,526.00 |

## Evidence and assumptions

Loaded labor cost is assumed at USD 30.00/hour. Configuration A has only a four-case offline synthetic measurement; B and C are unmeasured. Eligibility, acceptance, handling time, provider cost, infrastructure, and maintenance values are explicit sensitivity assumptions. Review workload is disclosed separately and the handling-time delta already reflects review effort, so it is not double-counted as another run cost.

Phase 2 requires the 30+ case evaluation, measured operating handling times, provider pricing/usage, security and privacy approval, live KB ownership, and peak-capacity validation before deployment.
