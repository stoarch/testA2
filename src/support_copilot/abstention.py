import re
from collections.abc import Sequence
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from support_copilot.drafting import Citation
from support_copilot.knowledge_base import RetrievedPassage

_FEE_AMOUNT_PATTERN = re.compile(
    r"(?:\bfee\b.{0,40}(?:[$€£]\s*\d+(?:\.\d+)?|\d+(?:\.\d+)?\s*%))"
    r"|(?:(?:[$€£]\s*\d+(?:\.\d+)?|\d+(?:\.\d+)?\s*%).{0,40}\bfee\b)",
    flags=re.IGNORECASE,
)
_UNCOVERED_FEE_MESSAGE = (
    "The available knowledge base does not establish the requested fee. "
    "A human reviewer must confirm it."
)
_MISSING_VERIFICATION_DETAIL_MESSAGE = (
    "The available knowledge base does not establish the requested verification requirement. "
    "A human reviewer must confirm it."
)


class ReviewReason(StrEnum):
    INSUFFICIENT_KB_COVERAGE = "insufficient_kb_coverage"
    TRADING_ADVICE = "trading_advice"
    KYC = "KYC"
    COMPLAINT = "complaint"


class AbstentionResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    status: Literal["abstained"] = "abstained"
    text: str = Field(min_length=1)
    citations: tuple[Citation, ...] = ()
    human_review_required: Literal[True] = True
    review_reasons: tuple[ReviewReason, ...] = Field(min_length=1)


class FeeEvidencePresentError(ValueError):
    pass


class VerificationEvidencePresentError(ValueError):
    pass


def _contains_explicit_fee_amount(passages: Sequence[RetrievedPassage]) -> bool:
    return any(_FEE_AMOUNT_PATTERN.search(passage.passage) for passage in passages)


def _normalize_phrase(text: str) -> str:
    return " ".join(text.casefold().split())


def build_uncovered_fee_abstention(
    passages: Sequence[RetrievedPassage],
) -> AbstentionResult:
    if _contains_explicit_fee_amount(passages):
        raise FeeEvidencePresentError(
            "Cannot produce an uncovered-fee abstention when evidence contains a fee amount"
        )

    return AbstentionResult(
        text=_UNCOVERED_FEE_MESSAGE,
        review_reasons=(ReviewReason.INSUFFICIENT_KB_COVERAGE,),
    )


def build_missing_verification_detail_abstention(
    passages: Sequence[RetrievedPassage],
    requested_detail: str,
) -> AbstentionResult:
    normalized_detail = _normalize_phrase(requested_detail)
    if not normalized_detail:
        raise ValueError("Requested verification detail cannot be empty")

    if any(normalized_detail in _normalize_phrase(passage.passage) for passage in passages):
        raise VerificationEvidencePresentError(
            "Cannot abstain when evidence contains the requested verification detail"
        )

    return AbstentionResult(
        text=_MISSING_VERIFICATION_DETAIL_MESSAGE,
        review_reasons=(ReviewReason.INSUFFICIENT_KB_COVERAGE,),
    )
