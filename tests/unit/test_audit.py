from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from support_copilot.abstention import ReviewReason
from support_copilot.audit import (
    AnswerStatus,
    AuditableProcessingResult,
    UsageData,
)
from support_copilot.contracts import (
    TicketCategory,
    TicketLanguage,
    TicketSentiment,
    TicketUrgency,
)
from support_copilot.drafting import Citation
from support_copilot.safety import SafetyFlag


def _citation() -> Citation:
    return Citation(
        source_id="KB-001",
        title="How to Deposit",
        url="https://valetax.com/how-to-deposit/",
        heading="Deposit steps",
        passage="Open the deposit area and choose a supported method.",
        retrieved_at=datetime(2026, 10, 24, 1, tzinfo=UTC),
        content_hash="a" * 64,
        snapshot_id="snapshot-synthetic-unit",
        synthetic=True,
    )


def _result(**overrides: object) -> AuditableProcessingResult:
    values: dict[str, object] = {
        "ticket_id": "TICKET-AUDIT-001",
        "category": TicketCategory.WITHDRAWAL,
        "urgency": TicketUrgency.NORMAL,
        "language": TicketLanguage.ENGLISH,
        "sentiment": TicketSentiment.NEUTRAL,
        "answer_status": AnswerStatus.DRAFTED,
        "citations": (_citation(),),
        "safety_flags": (),
        "human_review_required": False,
        "review_reasons": (),
        "configuration_id": "offline-v1",
        "latency_ms": 12.5,
        "usage": UsageData(input_tokens=10, output_tokens=20),
    }
    values.update(overrides)
    return AuditableProcessingResult(**values)


def test_auditable_result_serializes_required_fields_and_available_usage() -> None:
    payload = _result().model_dump(mode="json")

    assert payload["ticket_id"] == "TICKET-AUDIT-001"
    assert payload["category"] == "withdrawal"
    assert payload["answer_status"] == "drafted"
    assert payload["citations"][0]["source_id"] == "KB-001"
    assert payload["safety_flags"] == []
    assert payload["review_reasons"] == []
    assert payload["configuration_id"] == "offline-v1"
    assert payload["latency_ms"] == 12.5
    assert payload["usage"] == {"input_tokens": 10, "output_tokens": 20}


def test_auditable_result_records_unavailable_usage_as_null() -> None:
    payload = _result(usage=None).model_dump(mode="json")

    assert "usage" in payload
    assert payload["usage"] is None


def test_auditable_result_rejects_invalid_audit_measurements() -> None:
    with pytest.raises(ValidationError, match="latency_ms"):
        _result(latency_ms=-0.1)

    with pytest.raises(ValidationError, match="configuration_id"):
        _result(configuration_id=" ")

    with pytest.raises(ValidationError, match="input_tokens"):
        UsageData(input_tokens=-1, output_tokens=0)


def test_auditable_result_is_immutable() -> None:
    result = _result(
        answer_status=AnswerStatus.ROUTED,
        citations=(),
        safety_flags=(SafetyFlag.KYC_DECISION,),
        human_review_required=True,
        review_reasons=(ReviewReason.KYC,),
    )

    with pytest.raises(ValidationError, match="frozen"):
        result.latency_ms = 13.0
