from pathlib import Path

from support_copilot.abstention import ReviewReason
from support_copilot.application import process_offline_ticket
from support_copilot.audit import AnswerStatus

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SNAPSHOT_PATH = PROJECT_ROOT / "tests" / "fixtures" / "kb" / "synthetic_snapshot.json"


def test_offline_application_returns_a_cited_deposit_draft() -> None:
    result = process_offline_ticket(
        ticket_id="TICKET-INTERFACE-001",
        text="How do I make a deposit?",
        snapshot_path=SNAPSHOT_PATH,
    )

    assert result.ticket_id == "TICKET-INTERFACE-001"
    assert result.answer_status is AnswerStatus.DRAFTED
    assert "deposit" in result.answer_text.casefold()
    assert len(result.citations) == 1
    assert result.citations[0].source_id == "KB-001"
    assert result.human_review_required is False
    assert result.review_reasons == ()
    assert result.latency_ms >= 0


def test_offline_application_abstains_when_no_supported_draft_exists() -> None:
    result = process_offline_ticket(
        ticket_id="TICKET-INTERFACE-002",
        text="Can I receive a paper statement?",
        snapshot_path=SNAPSHOT_PATH,
    )

    assert result.answer_status is AnswerStatus.ABSTAINED
    assert "does not establish" in result.answer_text
    assert result.citations == ()
    assert result.human_review_required is True
    assert result.review_reasons == (ReviewReason.INSUFFICIENT_KNOWLEDGE,)
