import re
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from support_copilot.abstention import ReviewReason
from support_copilot.contracts import SupportTicket
from support_copilot.drafting import Citation

_BUY_SELL_RECOMMENDATION_PATTERN = re.compile(
    r"(?:\bshould\s+i\b.{0,40}\b(?:buy|sell|trade|short|long)\b)"
    r"|(?:\b(?:would|do)\s+you\s+recommend\b.{0,40}\b(?:buy|selling|buying|sell|trade|trading|short|long)\b)"
    r"|(?:\brecommend\b.{0,60}\b(?:buy|selling|buying|sell|trade|trading)\b)"
    r"|(?:\b(?:buy|sell|trade)\b.{0,40}\b(?:recommendation|advice)\b)"
    r"|(?:\bis\s+it\s+a\s+good\s+time\s+to\b.{0,30}\b(?:buy|sell|trade)\b)",
    flags=re.IGNORECASE,
)
_TRADING_SIGNAL_PATTERN = re.compile(
    r"\b(?:trading\s+signal|trade\s+signal|forex\s+signal|crypto\s+signal|buy\s+signal|sell\s+signal|signals?)\b",
    flags=re.IGNORECASE,
)
_PRICE_TARGET_PATTERN = re.compile(
    r"\b(?:price\s+target|target\s+price|price\s+forecast)\b",
    flags=re.IGNORECASE,
)
_LEVERAGE_RECOMMENDATION_PATTERN = re.compile(
    r"(?:\bleverage\b.{0,60}\b(?:should\s+i|would\s+you|which|what)\b.{0,40}\b(?:choose|use|select|set|pick|go\s+with)\b)"
    r"|(?:\b(?:which|what)\s+leverage\b.{0,60}\b(?:setting\s+)?(?:should\s+i|would\s+you|choose|use|set|select|pick)\b)"
    r"|(?:\b(?:recommend|suggest)\b.{0,40}\bleverage\b)",
    flags=re.IGNORECASE,
)
_KYC_CONTEXT_PATTERN = re.compile(r"\b(?:KYC|verification)\b", flags=re.IGNORECASE)
_OUTCOME_DECISION_PATTERN = re.compile(
    r"(?:\bshould\b.{0,80}\b(?:be\s+)?(?:approved|rejected)\b)"
    r"|(?:\b(?:approve|reject)\b.{0,80})",
    flags=re.IGNORECASE,
)
_AML_CONTEXT_PATTERN = re.compile(
    r"\b(?:AML|anti.money.laundering|suspicious transaction)\b", flags=re.IGNORECASE
)
_AML_DECISION_PATTERN = re.compile(
    r"\b(?:approve|reject|clear|flag|freeze|unfreeze|release|pass|fail)\b",
    flags=re.IGNORECASE,
)
_COMPLAINT_CONTEXT_PATTERN = re.compile(r"\bcomplaint\b", flags=re.IGNORECASE)
_COMPLAINT_DECISION_PATTERN = re.compile(
    r"\b(?:uphold|upheld|reject|rejected|deny|denied)\b",
    flags=re.IGNORECASE,
)
_TRADING_ADVICE_REFUSAL = (
    "I'm sorry, but I can't provide trading advice on whether to buy or sell. "
    "A human reviewer must review this request."
)
_LEVERAGE_ADVICE_REFUSAL = (
    "I'm sorry, but I can't recommend a leverage setting. "
    "A human reviewer must review this request."
)
_KYC_ACKNOWLEDGEMENT = (
    "Your verification request has been received and requires review by a human reviewer."
)
_COMPLAINT_ACKNOWLEDGEMENT = (
    "Your complaint has been received and requires review by a human reviewer."
)


class SafetyFlag(StrEnum):
    TRADING_ADVICE = "trading_advice"
    KYC_DECISION = "kyc_decision"
    COMPLAINT_DECISION = "complaint_decision"
    AML_DECISION = "aml_decision"


class SafetyResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    status: Literal["refused", "routed"]
    text: str = Field(min_length=1)
    citations: tuple[Citation, ...] = ()
    safety_flags: tuple[SafetyFlag, ...] = Field(min_length=1)
    human_review_required: Literal[True] = True
    review_reasons: tuple[ReviewReason, ...] = Field(min_length=1)


def _refusal_message(text: str) -> str | None:
    if _LEVERAGE_RECOMMENDATION_PATTERN.search(text):
        return _LEVERAGE_ADVICE_REFUSAL
    if (
        _BUY_SELL_RECOMMENDATION_PATTERN.search(text)
        or _TRADING_SIGNAL_PATTERN.search(text)
        or _PRICE_TARGET_PATTERN.search(text)
    ):
        return _TRADING_ADVICE_REFUSAL
    return None


def _build_safety_result(
    *,
    status: Literal["refused", "routed"],
    text: str,
    safety_flag: SafetyFlag,
    review_reason: ReviewReason,
) -> SafetyResult:
    return SafetyResult(
        status=status,
        text=text,
        safety_flags=(safety_flag,),
        review_reasons=(review_reason,),
    )


def apply_trading_advice_policy(ticket: SupportTicket) -> SafetyResult | None:
    refusal_message = _refusal_message(ticket.text)
    if refusal_message is None:
        return None

    return _build_safety_result(
        status="refused",
        text=refusal_message,
        safety_flag=SafetyFlag.TRADING_ADVICE,
        review_reason=ReviewReason.TRADING_ADVICE,
    )


def _is_kyc_outcome_request(text: str) -> bool:
    return bool(_KYC_CONTEXT_PATTERN.search(text) and _OUTCOME_DECISION_PATTERN.search(text))


def _is_complaint_decision_request(text: str) -> bool:
    return bool(
        _COMPLAINT_CONTEXT_PATTERN.search(text) and _COMPLAINT_DECISION_PATTERN.search(text)
    )


def _sensitive_outcome_route(
    text: str,
) -> tuple[str, SafetyFlag, ReviewReason] | None:
    if _AML_CONTEXT_PATTERN.search(text) and _AML_DECISION_PATTERN.search(text):
        return (
            "Your request requires a human compliance review.",
            SafetyFlag.AML_DECISION,
            ReviewReason.AML,
        )
    if _is_kyc_outcome_request(text):
        return _KYC_ACKNOWLEDGEMENT, SafetyFlag.KYC_DECISION, ReviewReason.KYC
    if _is_complaint_decision_request(text):
        return (
            _COMPLAINT_ACKNOWLEDGEMENT,
            SafetyFlag.COMPLAINT_DECISION,
            ReviewReason.COMPLAINT,
        )
    return None


def apply_safety_policy(ticket: SupportTicket) -> SafetyResult | None:
    trading_result = apply_trading_advice_policy(ticket)
    if trading_result is not None:
        return trading_result

    route = _sensitive_outcome_route(ticket.text)
    if route is None:
        return None

    acknowledgement, safety_flag, review_reason = route
    return _build_safety_result(
        status="routed",
        text=acknowledgement,
        safety_flag=safety_flag,
        review_reason=review_reason,
    )
