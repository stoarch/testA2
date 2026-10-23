# ADR-0005: Versioned KB snapshots and section-level lexical retrieval

- Status: Accepted
- Date: 2026-10-23
- Owners: Project team
- Related requirements: `REQ-004`-`REQ-006`, `REQ-011`, `REQ-015`, `REQ-020`, `REQ-102`, `REQ-103`
- Related work: `WBS-003`, `WBS-006`, `WBS-007`, `WBS-008`
- Supersedes: None

## Context

The MVP has four approved public pages. Every operational claim must be traceable to exact evidence, source gaps and contradictions must remain visible, and live retrieval must not be confused with synthetic demonstrations.

## Options considered

### Option A: JSON/Markdown snapshots with section-level lexical retrieval

- Benefits: deterministic, inspectable, inexpensive, easy to persist in tests, and sufficient for four documents.
- Costs and risks: lexical matching has weaker paraphrase recall than semantic retrieval.

### Option B: Vector database and embedding retrieval

- Benefits: stronger semantic matching at larger corpus sizes.
- Costs and risks: extra infrastructure, cost, nondeterminism, and provenance complexity for little Phase 1 benefit.

### Option C: Give complete pages directly to the model

- Benefits: minimal retrieval code.
- Costs and risks: weak claim-level traceability and poor scaling behavior.

## Decision

Fetch the four allowlisted pages into versioned JSON/Markdown snapshots. Preserve URL, title, headings, exact section text, retrieval timestamp, content hash, and snapshot identifier. Retrieve at section level using deterministic lexical scoring. Evidence records keep exact passages and stable source identifiers. Missing or contradictory evidence causes abstention and human review.

If live fetching is unavailable, the demo may use explicitly labeled synthetic fixtures; those fixtures must never be presented as live Valetax evidence.

## Consequences

### Positive

- Evaluation and integration tests are reproducible.
- Citations can resolve to exact stored passages.
- The design avoids a premature vector database.

### Negative

- Synonym and multilingual recall require evaluation and may initially be limited.
- Snapshot refresh and conflict review need explicit ownership.

### Follow-up work

- [x] Implement allowlisted synthetic snapshot loading, hashing, provenance storage, and section retrieval.
- [x] Add a persisted-snapshot integration test.
- [ ] Add live fetching/refresh and conflict fixtures.

## Validation

All cited claims must resolve to stored allowlisted passages, and offline fixtures must carry an unmistakable synthetic-evidence label.
