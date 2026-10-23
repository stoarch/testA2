from datetime import UTC, datetime

import pytest

from support_copilot.drafting import InsufficientEvidenceError, draft_deposit_answer
from support_copilot.knowledge_base import RetrievedPassage


def test_draft_deposit_answer_uses_only_supported_passage_and_cites_it() -> None:
    passage = RetrievedPassage(
        source_id="KB-001",
        title="How to Deposit",
        url="https://valetax.com/how-to-deposit/",
        heading="Deposit overview",
        passage=(
            "Synthetic fixture for testing: deposits are initiated from the account deposit area."
        ),
        retrieved_at=datetime(2026, 10, 24, 1, tzinfo=UTC),
        content_hash="a" * 64,
        snapshot_id="snapshot-synthetic-unit",
        synthetic=True,
    )

    result = draft_deposit_answer([passage])

    assert result.text == "Deposits are initiated from the account deposit area."
    assert "fee" not in result.text.casefold()
    assert "instant" not in result.text.casefold()
    assert result.citations[0].url == passage.url
    assert result.citations[0].passage == passage.passage
    assert result.citations[0].synthetic is True


def test_draft_deposit_answer_fails_closed_without_deposit_evidence() -> None:
    with pytest.raises(InsufficientEvidenceError, match="deposit evidence"):
        draft_deposit_answer([])
