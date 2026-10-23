# Known Limitations

- Only SCN-001 through SCN-006 have executable step definitions and passing production behavior.
- Category recognition identifies only the case-insensitive marker `withdraw`; other text becomes `other`. Urgency, English-language, and negative-sentiment recognition use narrow deterministic markers and are not yet evaluated.
- Pydantic classification contracts, the classification CLI, a persisted synthetic KB snapshot, allowlisted section retrieval, a snapshot integration test, and a classification subprocess E2E test are implemented.
- One extractive synthetic deposit draft and its structured provenance citation are implemented. General citation/claim validation, live KB fetching/refresh, generative drafting, abstention, policy gates, routing, provider adapters, and grounded-answer E2E paths are not implemented.
- The 30-ticket evaluation dataset and metrics report do not yet exist.
- The business case contains formulas and placeholders, not measured savings or a justified deployment recommendation.
- PlantUML sources are present, but automated rendering is not yet a CI gate.
- No Git repository/commit evidence or repository link is currently available.
- The synthetic snapshot and rules-only classification paths are executable separately; the complete offline demo and optional live-provider mode are not yet executable.
