# Valetax Support Co-Pilot Business Case

- Status: Draft - awaiting measured evaluation and operating inputs
- Planning volume: 10,000 tickets/month
- Evidence rule: projections are estimates, not measured savings

## Configurations

| Configuration | Description | Expected tradeoff |
|---|---|---|
| A | Deterministic retrieval and template drafts | Lowest variable cost and risk; narrower coverage |
| B | Guarded LLM-assisted drafting | Broader language flexibility; higher cost and validation burden |
| C | Hybrid routing with selective LLM usage | Uses deterministic paths where possible and reserves LLM calls for eligible tickets |

## Required inputs

Baseline handling minutes, loaded labor cost, eligible-ticket share, acceptance/edit/review rates, provider token prices, measured tokens, infrastructure cost, maintenance cost, and evaluation-derived error rates remain `TBD` until measured or supplied.

## Calculations

- Baseline hours = `10,000 * baseline_minutes / 60`
- Assisted hours = review, edit, exception, and escalation hours under each configuration
- Labor benefit = `(baseline_hours - assisted_hours) * loaded_hourly_cost`
- Monthly cost = provider + infrastructure + maintenance + review overhead
- Net monthly benefit = labor benefit - monthly cost
- Break-even acceptance rate or volume is solved where net monthly benefit equals zero

## Sensitivity cases

Each configuration must show low/base/high assumptions for acceptance rate, review time, token usage, provider price, maintenance, and error-driven rework.

## Current recommendation

No deployment configuration is justified yet because the repository lacks measured end-to-end quality, handling-time, review-rate, latency, and cost evidence. The next decision point follows the 30+ ticket evaluation and subprocess CLI E2E run.
