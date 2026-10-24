from support_copilot.audit import AnswerStatus, build_auditable_result
from support_copilot.routing import (
    ConfidenceAssessment,
    ConfidenceKind,
    route_low_confidence,
)
from support_copilot.ticket_processing import process_ticket


def test_classification_and_low_confidence_route_compose_into_auditable_result() -> None:
    classification = process_ticket(
        ticket_id="TICKET-AUDIT-INTEGRATION-001",
        text="Why is my withdrawal delayed?",
    )
    route = route_low_confidence(
        ConfidenceAssessment(
            confidence_kind=ConfidenceKind.CLASSIFICATION,
            confidence=0.49,
            configured_threshold=0.50,
        )
    )
    assert route is not None

    result = build_auditable_result(
        classification=classification,
        answer_status=AnswerStatus.ROUTED,
        answer_text="A human reviewer must confirm this result.",
        citations=(),
        safety_flags=(),
        human_review_required=route.human_review_required,
        review_reasons=route.review_reasons,
        configuration_id="offline-v1",
        latency_ms=3.5,
    )
    payload = result.model_dump(mode="json")

    assert payload["ticket_id"] == "TICKET-AUDIT-INTEGRATION-001"
    assert payload["category"] == "withdrawal"
    assert payload["answer_status"] == "routed"
    assert payload["answer_text"] == "A human reviewer must confirm this result."
    assert payload["human_review_required"] is True
    assert payload["review_reasons"] == ["low_confidence"]
    assert payload["configuration_id"] == "offline-v1"
    assert payload["latency_ms"] == 3.5
    assert payload["usage"] is None
