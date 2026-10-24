from enum import StrEnum
from typing import Literal

from pydantic import Field

from support_copilot.abstention import ReviewReason
from support_copilot.contracts import ContractModel


class ConfidenceKind(StrEnum):
    CLASSIFICATION = "classification"
    GROUNDING = "grounding"


class ConfidenceAssessment(ContractModel):
    confidence_kind: ConfidenceKind
    confidence: float = Field(ge=0.0, le=1.0)
    configured_threshold: float = Field(ge=0.0, le=1.0)

    def is_below_threshold(self) -> bool:
        return self.confidence < self.configured_threshold


class LowConfidenceRouteResult(ContractModel):
    status: Literal["routed"] = "routed"
    human_review_required: Literal[True] = True
    review_reasons: tuple[ReviewReason, ...] = (ReviewReason.LOW_CONFIDENCE,)
    confidence_kind: ConfidenceKind
    confidence: float = Field(ge=0.0, le=1.0)
    configured_threshold: float = Field(ge=0.0, le=1.0)


def route_low_confidence(
    assessment: ConfidenceAssessment,
) -> LowConfidenceRouteResult | None:
    if not assessment.is_below_threshold():
        return None

    return LowConfidenceRouteResult(
        confidence_kind=assessment.confidence_kind,
        confidence=assessment.confidence,
        configured_threshold=assessment.configured_threshold,
    )
