import re
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from support_copilot.abstention import ReviewReason
from support_copilot.contracts import SupportTicket
from support_copilot.drafting import Citation

_RECOMMENDATION_REQUEST_PATTERN = re.compile(
    r"(?:\bshould\s+i\b.{0,40}\b(?:buy|sell)\b)"
    r"|(?:\brecommend\b.{0,60}\b(?:buy|sell)\b)",
    flags=re.IGNORECASE,
)
_CURRENCY_PAIR_PATTERN = re.compile(r"\b[A-Z]{3}/[A-Z]{3}\b", flags=re.IGNORECASE)
_TRADING_ADVICE_REFUSAL = (
    "I'm sorry, but I can't provide trading advice on whether to buy or sell. "
    "A human reviewer must review this request."
)


class SafetyFlag(StrEnum):
    TRADING_ADVICE = "trading_advice"


class SafetyResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    status: Literal["refused"] = "refused"
    text: str = Field(min_length=1)
    citations: tuple[Citation, ...] = ()
    safety_flags: tuple[SafetyFlag, ...] = Field(min_length=1)
    human_review_required: Literal[True] = True
    review_reasons: tuple[ReviewReason, ...] = Field(min_length=1)


def _is_direct_currency_pair_recommendation(text: str) -> bool:
    required_patterns = (
        _CURRENCY_PAIR_PATTERN,
        _RECOMMENDATION_REQUEST_PATTERN,
    )
    return all(pattern.search(text) for pattern in required_patterns)


def apply_trading_advice_policy(ticket: SupportTicket) -> SafetyResult | None:
    if not _is_direct_currency_pair_recommendation(ticket.text):
        return None

    return SafetyResult(
        text=_TRADING_ADVICE_REFUSAL,
        safety_flags=(SafetyFlag.TRADING_ADVICE,),
        review_reasons=(ReviewReason.TRADING_ADVICE,),
    )
