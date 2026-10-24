from support_copilot.abstention import ReviewReason
from support_copilot.routing import (
    ConfidenceAssessment,
    ConfidenceKind,
    route_low_confidence,
)


def test_grounding_confidence_reaches_serialized_human_route_contract() -> None:
    assessment = ConfidenceAssessment(
        confidence_kind=ConfidenceKind.GROUNDING,
        confidence=0.39,
        configured_threshold=0.40,
    )

    result = route_low_confidence(assessment)

    assert result is not None
    assert result.model_dump(mode="json") == {
        "status": "routed",
        "human_review_required": True,
        "review_reasons": [ReviewReason.LOW_CONFIDENCE.value],
        "confidence_kind": ConfidenceKind.GROUNDING.value,
        "confidence": 0.39,
        "configured_threshold": 0.40,
    }
