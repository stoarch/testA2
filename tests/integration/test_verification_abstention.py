from datetime import UTC, datetime
from pathlib import Path

from support_copilot.abstention import (
    ReviewReason,
    build_missing_verification_detail_abstention,
)
from support_copilot.knowledge_base import load_snapshot, retrieve_passages

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FIXTURE_PATH = PROJECT_ROOT / "tests" / "fixtures" / "kb" / "synthetic_snapshot.json"


def test_persisted_snapshot_missing_verification_detail_routes_to_review() -> None:
    snapshot = load_snapshot(FIXTURE_PATH)
    passages = retrieve_passages(
        snapshot,
        query="Does verification require a notarized utility bill?",
        retrieved_at=datetime(2026, 10, 24, 1, tzinfo=UTC),
    )

    result = build_missing_verification_detail_abstention(
        passages,
        requested_detail="notarized utility bill",
    )

    assert passages
    assert result.status == "abstained"
    assert result.human_review_required is True
    assert result.review_reasons == (ReviewReason.INSUFFICIENT_KNOWLEDGE,)
    assert result.citations == ()
