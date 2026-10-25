# PR #2 Business-Case Assumptions Appendix

This appendix preserves PR #2's earlier illustrative token and labor calculations. The reproducible, evidence-gated deployment decision remains [`business-case.md`](business-case.md), generated from [`business-case-input.json`](business-case-input.json).

All figures below are non-measured modeling assumptions for prototype evaluation.

| Configuration | Illustrative mechanism | Token calculation | Monthly API cost | Illustrative total monthly cost |
|---|---|---:|---:|---:|
| A | Deterministic offline rules, exact citations, synthetic KB | No API tokens | USD 0.00 | USD 31,550.00 |
| B | Guarded generative drafting | 10,000 × 1,500 = 15,000,000 tokens at USD 0.002/1,000 | USD 30.00 | USD 21,230.00 |
| C | Deterministic routing plus 4,500 selective LLM calls | 4,500 × 1,500 = 6,750,000 tokens at USD 0.002/1,000 | USD 13.50 | USD 16,613.50 |

The earlier projection assumed an 8-minute baseline at USD 30/hour, with illustrative monthly savings of USD 8,450 for A, USD 18,770 for B, and USD 23,386.50 for C. These values are not measured operating results and do not override the current no-go evidence gate.

The conservative pilot model retained from `main` uses a 6-minute baseline at USD 15/hour, mandatory human approval, and break-even accepted-ticket fractions of 10.4% for A, 22.7% for B, and 14.7% for C. Deployment requires measured acceptance, review-time, safety, token, and provider-cost data.
