from datetime import UTC, datetime

import pytest

from support_copilot.abstention import ReviewReason
from support_copilot.conflicts import (
    NoSourceConflictError,
    build_source_conflict_abstention,
)
from support_copilot.knowledge_base import RetrievedPassage


def _passage(source_id: str, url: str, text: str) -> RetrievedPassage:
    return RetrievedPassage(
        source_id=source_id,
        title=f"Approved source {source_id}",
        url=url,
        heading="Withdrawal processing time",
        passage=text,
        retrieved_at=datetime(2026, 10, 24, 1, tzinfo=UTC),
        content_hash=source_id.casefold().replace("-", "a").ljust(64, "a")[:64],
        snapshot_id="snapshot-synthetic-conflict",
        synthetic=True,
    )


def test_conflicting_duration_claims_abstain_and_expose_both_sources() -> None:
    passages = [
        _passage(
            "KB-001",
            "https://valetax.com/how-to-withdraw/",
            "Withdrawal processing time is 1 business day.",
        ),
        _passage(
            "KB-002",
            "https://valetax.com/how-to-open-an-account/",
            "Withdrawal processing time is 3 business days.",
        ),
    ]

    result = build_source_conflict_abstention(
        passages,
        requested_detail="withdrawal processing time",
    )

    assert result.status == "abstained"
    assert "1 business day" not in result.text
    assert "3 business days" not in result.text
    assert tuple(citation.source_id for citation in result.citations) == ("KB-001", "KB-002")
    assert result.human_review_required is True
    assert result.review_reasons == (ReviewReason.SOURCE_CONFLICT,)


def test_matching_duration_claims_do_not_create_a_conflict_abstention() -> None:
    passages = [
        _passage(
            "KB-001",
            "https://valetax.com/how-to-withdraw/",
            "Withdrawal processing time is 1 business day.",
        ),
        _passage(
            "KB-002",
            "https://valetax.com/how-to-open-an-account/",
            "Withdrawal processing time is 1 business day.",
        ),
    ]

    with pytest.raises(NoSourceConflictError, match="No conflicting"):
        build_source_conflict_abstention(
            passages,
            requested_detail="withdrawal processing time",
        )


def test_conflict_detection_rejects_an_empty_requested_detail() -> None:
    with pytest.raises(ValueError, match="requested detail"):
        build_source_conflict_abstention([], requested_detail=" ")
