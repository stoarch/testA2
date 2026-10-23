# One-Page Business-Case Requirements

The final one-page artifact must answer: **Is the co-pilot worth running at approximately 10,000 tickets per month, and with which measured configuration?**

## Configurations to compare

At minimum, report the implemented Phase 1 configuration. Prefer comparison with one meaningful alternative when time permits, such as a different model, retrieval depth, or human-review threshold. Do not invent results for an untested configuration.

## Required measured inputs

| Input | Unit |
|---|---|
| Monthly ticket volume | tickets/month; baseline 10,000 |
| Eligible/repetitive share | percentage of tickets |
| Automation/draft acceptance rate | percentage |
| Abstention and human-review rate | percentage |
| Average handling time before co-pilot | minutes/ticket |
| Average review handling time with co-pilot | minutes/ticket |
| Loaded support labor cost | currency/hour |
| Model input/output usage | tokens or provider units/ticket |
| Model/retrieval/infrastructure price | currency/unit |
| Observed quality and safety metrics | percentage/count |
| Observed p50/p95 latency | seconds |

Unknown business inputs must appear as explicit assumptions or ranges.

## Required calculations

```text
eligible_tickets = monthly_volume × eligible_share
accepted_drafts = eligible_tickets × draft_acceptance_rate
hours_saved = accepted_drafts × (baseline_AHT - review_AHT) / 60
labor_value = hours_saved × loaded_hourly_cost
model_cost = monthly_volume × measured_model_cost_per_ticket
monthly_run_cost = model_cost + retrieval_cost + infrastructure_cost + operating_overhead
monthly_net_value = labor_value - monthly_run_cost
cost_per_ticket = monthly_run_cost / monthly_volume
break_even_accepted_drafts = monthly_run_cost / value_saved_per_accepted_draft
```

## Decision rule

Recommend a configuration only if:

1. all hard safety acceptance tests pass;
2. grounding/citation quality meets the defined acceptance set;
3. the human-review workload is operationally credible;
4. assumptions and sensitivity ranges are visible; and
5. monthly net value is positive or a documented strategic benefit justifies the cost.

## One-page output layout

- Recommendation and confidence
- Configuration comparison table
- Quality/safety/review-rate summary
- Monthly cost, value, net value, and cost per ticket
- Top assumptions and sensitivity range
- Phase 2 scale/operational investments
- Go / conditional go / no-go conclusion

