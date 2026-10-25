import json
from datetime import datetime
from pathlib import Path

import pytest

from support_copilot.abstention import ReviewReason
from support_copilot.application import process_offline_ticket
from support_copilot.audit import AnswerStatus, AuditableProcessingResult
from support_copilot.knowledge_base import KBSnapshot, RetrievedPassage

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SNAPSHOT_PATH = PROJECT_ROOT / "tests" / "fixtures" / "kb" / "synthetic_snapshot.json"


def _assert_retrieval_failure(result: AuditableProcessingResult, *, ticket_id: str) -> None:
    assert result.ticket_id == ticket_id
    assert result.category == "deposit"
    assert result.answer_status is AnswerStatus.ABSTAINED
    assert result.answer_text
    assert "temporarily unable to verify" in result.answer_text.casefold()
    assert result.citations == ()
    assert result.safety_flags == ()
    assert result.human_review_required is True
    assert result.review_reasons == (ReviewReason.RETRIEVAL_FAILURE,)
    assert result.configuration_id == "test-retrieval-failure"
    assert result.latency_ms >= 0


def _process(snapshot_path: Path, *, ticket_id: str) -> AuditableProcessingResult:
    return process_offline_ticket(
        ticket_id=ticket_id,
        text="How do I make a deposit?",
        snapshot_path=snapshot_path,
        configuration_id="test-retrieval-failure",
    )


def test_missing_snapshot_returns_typed_fail_closed_result(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing-snapshot.json"

    result = _process(missing_path, ticket_id="TICKET-KB-MISSING")

    _assert_retrieval_failure(result, ticket_id="TICKET-KB-MISSING")
    assert str(missing_path) not in result.answer_text


def test_unreadable_snapshot_returns_typed_fail_closed_result(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def unreadable_snapshot(
        path: Path,
        encoding: str | None = None,
        errors: str | None = None,
    ) -> str:
        del path, encoding, errors
        raise PermissionError("internal filesystem detail")

    monkeypatch.setattr(Path, "read_text", unreadable_snapshot)

    result = _process(SNAPSHOT_PATH, ticket_id="TICKET-KB-UNREADABLE")

    _assert_retrieval_failure(result, ticket_id="TICKET-KB-UNREADABLE")
    assert "filesystem" not in result.answer_text.casefold()


def test_malformed_snapshot_returns_typed_fail_closed_result(tmp_path: Path) -> None:
    malformed_path = tmp_path / "malformed-snapshot.json"
    malformed_path.write_text("{not valid json", encoding="utf-8")

    result = _process(malformed_path, ticket_id="TICKET-KB-MALFORMED")

    _assert_retrieval_failure(result, ticket_id="TICKET-KB-MALFORMED")
    assert "json" not in result.answer_text.casefold()


def test_schema_invalid_snapshot_returns_typed_fail_closed_result(tmp_path: Path) -> None:
    invalid_path = tmp_path / "schema-invalid-snapshot.json"
    invalid_path.write_text("{}", encoding="utf-8")

    result = _process(invalid_path, ticket_id="TICKET-KB-SCHEMA")

    _assert_retrieval_failure(result, ticket_id="TICKET-KB-SCHEMA")
    assert "schema" not in result.answer_text.casefold()


def test_hash_mismatch_returns_typed_fail_closed_result(tmp_path: Path) -> None:
    payload = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
    payload["documents"][0]["content_hash"] = "0" * 64
    corrupt_path = tmp_path / "corrupt-snapshot.json"
    corrupt_path.write_text(json.dumps(payload), encoding="utf-8")

    result = _process(corrupt_path, ticket_id="TICKET-KB-HASH")

    _assert_retrieval_failure(result, ticket_id="TICKET-KB-HASH")
    assert "hash" not in result.answer_text.casefold()


def test_injected_retrieval_failure_returns_typed_fail_closed_result() -> None:
    from support_copilot.knowledge_base import RetrievalUnavailableError

    def failing_retriever(
        snapshot: KBSnapshot,
        query: str,
        retrieved_at: datetime,
    ) -> list[RetrievedPassage]:
        del snapshot, query, retrieved_at
        raise RetrievalUnavailableError("internal retrieval connection detail")

    result = process_offline_ticket(
        ticket_id="TICKET-KB-INJECTED",
        text="How do I make a deposit?",
        snapshot_path=SNAPSHOT_PATH,
        configuration_id="test-retrieval-failure",
        retriever=failing_retriever,
    )

    _assert_retrieval_failure(result, ticket_id="TICKET-KB-INJECTED")
    assert "connection" not in result.answer_text.casefold()


def test_unrelated_retriever_error_is_not_silently_converted() -> None:
    def broken_retriever(
        snapshot: KBSnapshot,
        query: str,
        retrieved_at: datetime,
    ) -> list[RetrievedPassage]:
        del snapshot, query, retrieved_at
        raise AssertionError("programming defect")

    with pytest.raises(AssertionError, match="programming defect"):
        process_offline_ticket(
            ticket_id="TICKET-KB-PROGRAMMING-ERROR",
            text="How do I make a deposit?",
            snapshot_path=SNAPSHOT_PATH,
            retriever=broken_retriever,
        )


def test_valid_snapshot_still_returns_grounded_deposit_draft() -> None:
    result = _process(SNAPSHOT_PATH, ticket_id="TICKET-KB-VALID")

    assert result.answer_status is AnswerStatus.DRAFTED
    assert len(result.citations) == 1
    assert result.citations[0].source_id == "KB-001"
    assert result.human_review_required is False


@pytest.mark.parametrize(
    ("ticket_id", "text", "expected_status", "expected_reason"),
    [
        (
            "TICKET-KB-SAFETY-TRADING",
            "Should I buy EUR/USD?",
            AnswerStatus.REFUSED,
            ReviewReason.TRADING_ADVICE,
        ),
        (
            "TICKET-KB-SAFETY-KYC",
            "Please approve my KYC verification.",
            AnswerStatus.ROUTED,
            ReviewReason.KYC,
        ),
        (
            "TICKET-KB-SAFETY-AML",
            "Should we release this AML-flagged transaction?",
            AnswerStatus.ROUTED,
            ReviewReason.AML,
        ),
    ],
)
def test_safety_policy_precedes_unavailable_snapshot(
    tmp_path: Path,
    ticket_id: str,
    text: str,
    expected_status: AnswerStatus,
    expected_reason: ReviewReason,
) -> None:
    result = process_offline_ticket(
        ticket_id=ticket_id,
        text=text,
        snapshot_path=tmp_path / "missing-snapshot.json",
    )

    assert result.answer_status is expected_status
    assert result.human_review_required is True
    assert result.review_reasons == (expected_reason,)
    assert ReviewReason.RETRIEVAL_FAILURE not in result.review_reasons
