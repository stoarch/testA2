import pytest
from pydantic import ValidationError

from support_copilot.abstention import ReviewReason
from support_copilot.routing import (
    ConfidenceAssessment,
    ConfidenceKind,
    route_low_confidence,
)


def test_classification_confidence_below_threshold_routes_to_human() -> None:
    assessment = ConfidenceAssessment(
        confidence_kind=ConfidenceKind.CLASSIFICATION,
        confidence=0.49,
        configured_threshold=0.50,
    )

    result = route_low_confidence(assessment)

    assert result is not None
    assert result.status == "routed"
    assert result.human_review_required is True
    assert result.review_reasons == (ReviewReason.LOW_CONFIDENCE,)
    assert result.confidence_kind is ConfidenceKind.CLASSIFICATION
    assert result.confidence == 0.49
    assert result.configured_threshold == 0.50


def test_confidence_at_or_above_threshold_does_not_route() -> None:
    at_threshold = ConfidenceAssessment(
        confidence_kind=ConfidenceKind.GROUNDING,
        confidence=0.50,
        configured_threshold=0.50,
    )
    above_threshold = ConfidenceAssessment(
        confidence_kind=ConfidenceKind.GROUNDING,
        confidence=0.51,
        configured_threshold=0.50,
    )

    assert route_low_confidence(at_threshold) is None
    assert route_low_confidence(above_threshold) is None


def test_confidence_threshold_must_be_a_probability() -> None:
    with pytest.raises(ValidationError, match="configured_threshold"):
        ConfidenceAssessment(
            confidence_kind=ConfidenceKind.CLASSIFICATION,
            confidence=0.49,
            configured_threshold=1.01,
        )
