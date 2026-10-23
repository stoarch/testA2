from datetime import UTC, datetime
from pathlib import Path

import pytest

from support_copilot.drafting import Citation, DraftResult
from support_copilot.evidence_validation import (
    UnsupportedTimelineClaimError,
    validate_timeline_claims,
)
from support_copilot.knowledge_base import load_snapshot, retrieve_passages

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FIXTURE_PATH = PROJECT_ROOT / "tests" / "fixtures" / "kb" / "synthetic_snapshot.json"


def test_persisted_timeline_evidence_accepts_only_its_exact_duration() -> None:
    snapshot = load_snapshot(FIXTURE_PATH)
    passages = retrieve_passages(
        snapshot,
        query="How long does account opening take?",
        retrieved_at=datetime(2026, 10, 24, 1, tzinfo=UTC),
    )
    citation = Citation.from_passage(passages[0])

    supported = DraftResult(
        text="Account opening is completed within 48 hours.",
        citations=(citation,),
    )
    unsupported = DraftResult(
        text="Account opening is completed within 24 hours.",
        citations=(citation,),
    )

    assert validate_timeline_claims(supported) == ("48 hours",)
    with pytest.raises(UnsupportedTimelineClaimError, match="24 hours"):
        validate_timeline_claims(unsupported)
