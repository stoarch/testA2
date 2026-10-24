import sys
from pathlib import Path

from behave import given, then, when

PROJECT_ROOT = Path(__file__).resolve().parents[3]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))


@given("a ticket completes processing")
def step_ticket_completes_processing(context) -> None:
    from support_copilot.routing import (
        ConfidenceAssessment,
        ConfidenceKind,
        route_low_confidence,
    )
    from support_copilot.ticket_processing import process_ticket

    context.audit_classification = process_ticket(
        ticket_id="TICKET-BDD-016",
        text="Why is my withdrawal delayed?",
    )
    context.audit_route = route_low_confidence(
        ConfidenceAssessment(
            confidence_kind=ConfidenceKind.CLASSIFICATION,
            confidence=0.49,
            configured_threshold=0.50,
        )
    )
    assert context.audit_route is not None


@when("the structured result is returned")
def step_structured_result_is_returned(context) -> None:
    from support_copilot.audit import AnswerStatus, UsageData, build_auditable_result

    context.audit_result = build_auditable_result(
        classification=context.audit_classification,
        answer_status=AnswerStatus.ROUTED,
        citations=(),
        safety_flags=(),
        human_review_required=context.audit_route.human_review_required,
        review_reasons=context.audit_route.review_reasons,
        configuration_id="bdd-offline-v1",
        latency_ms=4.0,
        usage=UsageData(input_tokens=0, output_tokens=0),
    )


@then(
    "it includes classifications, answer status, citations, safety flags, review reasons, "
    "configuration ID, latency, and usage data when available"
)
def step_audit_fields_are_present(context) -> None:
    payload = context.audit_result.model_dump(mode="json")
    expected_fields = {
        "category",
        "urgency",
        "language",
        "sentiment",
        "answer_status",
        "citations",
        "safety_flags",
        "review_reasons",
        "configuration_id",
        "latency_ms",
        "usage",
    }

    assert expected_fields <= payload.keys()
    assert payload["usage"] == {"input_tokens": 0, "output_tokens": 0}
