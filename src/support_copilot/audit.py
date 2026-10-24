from collections.abc import Sequence
from enum import StrEnum

from pydantic import Field

from support_copilot.abstention import ReviewReason
from support_copilot.contracts import (
    ContractModel,
    ProcessingResult,
    TicketCategory,
    TicketLanguage,
    TicketSentiment,
    TicketUrgency,
)
from support_copilot.drafting import Citation
from support_copilot.safety import SafetyFlag


class AnswerStatus(StrEnum):
    DRAFTED = "drafted"
    ABSTAINED = "abstained"
    REFUSED = "refused"
    ROUTED = "routed"


class UsageData(ContractModel):
    input_tokens: int = Field(ge=0)
    output_tokens: int = Field(ge=0)


class AuditableProcessingResult(ContractModel):
    ticket_id: str = Field(min_length=1)
    category: TicketCategory
    urgency: TicketUrgency
    language: TicketLanguage
    sentiment: TicketSentiment
    answer_status: AnswerStatus
    citations: tuple[Citation, ...] = ()
    safety_flags: tuple[SafetyFlag, ...] = ()
    human_review_required: bool
    review_reasons: tuple[ReviewReason, ...] = ()
    configuration_id: str = Field(min_length=1)
    latency_ms: float = Field(ge=0.0)
    usage: UsageData | None = None


def build_auditable_result(
    *,
    classification: ProcessingResult,
    answer_status: AnswerStatus,
    citations: Sequence[Citation],
    safety_flags: Sequence[SafetyFlag],
    human_review_required: bool,
    review_reasons: Sequence[ReviewReason],
    configuration_id: str,
    latency_ms: float,
    usage: UsageData | None = None,
) -> AuditableProcessingResult:
    return AuditableProcessingResult.model_validate(
        {
            **classification.model_dump(),
            "answer_status": answer_status,
            "citations": tuple(citations),
            "safety_flags": tuple(safety_flags),
            "human_review_required": human_review_required,
            "review_reasons": tuple(review_reasons),
            "configuration_id": configuration_id,
            "latency_ms": latency_ms,
            "usage": usage,
        }
    )
