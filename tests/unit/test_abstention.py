from datetime import UTC, datetime

import pytest

from support_copilot.abstention import (
    FeeEvidencePresentError,
    ReviewReason,
    VerificationEvidencePresentError,
    build_missing_verification_detail_abstention,
    build_uncovered_fee_abstention,
)
from support_copilot.knowledge_base import RetrievedPassage


def _passage(text: str) -> RetrievedPassage:
    return RetrievedPassage(
        source_id="KB-002",
        title="How to Withdraw",
        url="https://valetax.com/how-to-withdraw/",
        heading="Withdrawal overview",
        passage=text,
        retrieved_at=datetime(2026, 10, 24, 1, tzinfo=UTC),
        content_hash="a" * 64,
        snapshot_id="snapshot-synthetic-unit",
        synthetic=True,
    )


def test_uncovered_fee_returns_safe_abstention_and_requires_review() -> None:
    result = build_uncovered_fee_abstention(
        [_passage("Withdrawal requests are initiated from the withdrawal area.")]
    )

    assert result.status == "abstained"
    assert "does not establish the requested fee" in result.text
    assert result.citations == ()
    assert result.human_review_required is True
    assert result.review_reasons == (ReviewReason.INSUFFICIENT_KB_COVERAGE,)
    assert not any(character.isdigit() for character in result.text)


def test_uncovered_fee_abstention_rejects_evidence_with_a_fee_amount() -> None:
    with pytest.raises(FeeEvidencePresentError, match="fee amount"):
        build_uncovered_fee_abstention([_passage("The withdrawal fee is 2%.")])


def test_missing_verification_detail_abstains_without_inferring_requirement() -> None:
    result = build_missing_verification_detail_abstention(
        [_passage("Verification includes profile fields and document upload.")],
        requested_detail="notarized utility bill",
    )

    assert result.status == "abstained"
    assert "does not establish the requested verification requirement" in result.text
    assert "notarized" not in result.text.casefold()
    assert "utility bill" not in result.text.casefold()
    assert result.human_review_required is True
    assert result.review_reasons == (ReviewReason.INSUFFICIENT_KB_COVERAGE,)


def test_missing_verification_detail_rejects_directly_supported_evidence() -> None:
    with pytest.raises(VerificationEvidencePresentError, match="verification detail"):
        build_missing_verification_detail_abstention(
            [_passage("Verification requires a notarized utility bill.")],
            requested_detail="notarized utility bill",
        )
