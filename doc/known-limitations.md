# Known Limitations

The repository is a submission-ready, human-reviewed prototype, not a production system.

## Implemented boundary

- `SCN-001` through `SCN-020` are executable and passing: 20 of 28 roadmap scenarios (71.4%). The remaining eight are intentional future work, not submission blockers.
- Classification has five outcomes: `deposit`, `withdrawal`, `account_opening`, `verification`, and `other`. No match or multiple category matches explicitly fall back to `other`.
- The working offline path validates deposit intent, produces an extractive deposit how-to draft when approved evidence supports it, and otherwise abstains. Citations include structured source and snapshot provenance.
- Deterministic safety rules refuse buy/sell recommendations, trading signals, price targets, and personalized leverage choices. KYC, AML, and complaint outcome requests route to human review.
- The CLI supports classification, offline ticket processing, a four-case synthetic evaluation, and evidence-gated business-case generation. Automated pytest, Behave, Ruff, Gherkin-parity, architecture-document, and GitHub CI checks are present.
- The business case compares three configurations and can project positive value under modeled assumptions, but currently returns **no-go for deployment** because quality evidence is insufficient.

## Intentional limitations

- The KB is a checked-in synthetic offline fixture, not live Valetax page ingestion, search, or synchronization.
- The end-to-end drafting path is extractive and deposit-only; other supported classifications do not imply general answer generation.
- No generative LLM or external model-provider integration is implemented.
- Classification and safety detection use bounded, English-oriented deterministic patterns. They are not reliable multilingual or adversarial semantic classifiers.
- Evaluation contains four synthetic cases, which is insufficient for statistical performance or universal safety claims; the separate 30+ case target remains future validation work.
- Semantic grounding is limited. Timeline conflict detection depends on requested-detail phrases and distinct numeric duration claims; broader semantic and nonnumeric contradiction detection is absent.
- Confidence thresholds are recorded but not statistically calibrated. Verification coverage and safety routing remain pattern-bound and can miss obfuscated intent.
- Audit metadata is returned in each response but is not persisted. There is no production review queue, database, live KB, customer system, or other external integration.
- There is no production deployment or customer auto-send path. Security, privacy, capacity, monitoring, and operational ownership require separate Phase 2 work.
- PlantUML sources are maintained, but rendered-diagram validation is not a CI gate.
