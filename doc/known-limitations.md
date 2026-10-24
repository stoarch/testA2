# Known Limitations

- Only SCN-001 through SCN-011 have executable step definitions and passing production behavior.
- Category recognition identifies only the case-insensitive marker `withdraw`; other text becomes `other`. Urgency, English-language, and negative-sentiment recognition use narrow deterministic markers and are not yet evaluated.
- Pydantic classification contracts, the classification CLI, a persisted synthetic KB snapshot, allowlisted section retrieval, a snapshot integration test, and a classification subprocess E2E test are implemented.
- One extractive synthetic deposit draft, its structured provenance citation, exact numeric-duration validation, typed fee/verification coverage abstentions, and narrow direct currency-pair and personalized-leverage refusals are implemented. Verification coverage is exact-phrase only; trading detection uses bounded patterns, and leverage detection recognizes only explicit `leverage ... should I choose/use/set` wording. General semantic claim validation, broader or obfuscated safety intents, live KB fetching/refresh, generative drafting, provider adapters, and grounded-answer E2E paths are not implemented.
- The 30-ticket evaluation dataset and metrics report do not yet exist.
- The business case contains formulas and placeholders, not measured savings or a justified deployment recommendation.
- PlantUML sources are present, but automated rendering is not yet a CI gate.
- No Git repository/commit evidence or repository link is currently available.
- The synthetic snapshot and rules-only classification paths are executable separately; the complete offline demo and optional live-provider mode are not yet executable.
