from datetime import UTC, datetime

import pytest

from support_copilot.drafting import Citation, DraftResult
from support_copilot.evidence_validation import (
    UnsupportedTimelineClaimError,
    validate_timeline_claims,
)


def _citation(passage: str) -> Citation:
    return Citation(
        source_id="KB-003",
        title="How to Open an Account",
        url="https://valetax.com/how-to-open-an-account/",
        heading="Account opening overview",
        passage=passage,
        retrieved_at=datetime(2026, 10, 24, 1, tzinfo=UTC),
        content_hash="a" * 64,
        snapshot_id="snapshot-synthetic-unit",
        synthetic=True,
    )


def test_validate_timeline_claims_accepts_exact_cited_duration() -> None:
    result = DraftResult(
        text="Account opening is completed within 48 hours.",
        citations=(
            _citation(
                "Synthetic fixture for testing: account opening is completed within 48 hours."
            ),
        ),
    )

    assert validate_timeline_claims(result) == ("48 hours",)


def test_validate_timeline_claims_rejects_duration_absent_from_citations() -> None:
    result = DraftResult(
        text="Account opening is completed within 24 hours.",
        citations=(
            _citation(
                "Synthetic fixture for testing: account opening is completed within 48 hours."
            ),
        ),
    )

    with pytest.raises(UnsupportedTimelineClaimError, match="24 hours"):
        validate_timeline_claims(result)
