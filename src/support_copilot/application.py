from datetime import UTC, datetime
from pathlib import Path
from time import perf_counter
from typing import NamedTuple

from support_copilot.abstention import AbstentionResult, ReviewReason
from support_copilot.audit import (
    AnswerStatus,
    AuditableProcessingResult,
    build_auditable_result,
)
from support_copilot.contracts import SupportTicket
from support_copilot.drafting import Citation, InsufficientEvidenceError, draft_deposit_answer
from support_copilot.knowledge_base import load_snapshot, retrieve_passages
from support_copilot.safety import SafetyFlag, SafetyResult, apply_safety_policy
from support_copilot.ticket_processing import process_ticket

DEFAULT_CONFIGURATION_ID = "deterministic-offline-v1"
_UNSUPPORTED_ANSWER = (
    "The available knowledge base does not establish a supported answer. "
    "A human reviewer must confirm it."
)


class _OfflineDecision(NamedTuple):
    answer_status: AnswerStatus
    answer_text: str
    citations: tuple[Citation, ...]
    safety_flags: tuple[SafetyFlag, ...]
    human_review_required: bool
    review_reasons: tuple[ReviewReason, ...]


def _unsupported_abstention() -> AbstentionResult:
    return AbstentionResult(
        text=_UNSUPPORTED_ANSWER,
        review_reasons=(ReviewReason.INSUFFICIENT_KNOWLEDGE,),
    )


def _decision_from_safety(result: SafetyResult) -> _OfflineDecision:
    return _OfflineDecision(
        answer_status=AnswerStatus(result.status),
        answer_text=result.text,
        citations=result.citations,
        safety_flags=result.safety_flags,
        human_review_required=result.human_review_required,
        review_reasons=result.review_reasons,
    )


def _decision_from_knowledge(text: str, snapshot_path: Path) -> _OfflineDecision:
    snapshot = load_snapshot(snapshot_path)
    passages = retrieve_passages(
        snapshot,
        query=text,
        retrieved_at=datetime.now(UTC),
    )
    # Do not answer fee/limit/timeline questions by returning an unrelated procedural paragraph.
    normalized = text.casefold()
    high_risk_details = (
        "fee",
        "charge",
        "cost",
        "how long",
        "when",
        "time",
        "limit",
        "minimum",
        "maximum",
    )
    category = process_ticket(ticket_id="classification-only", text=text).category
    from support_copilot.contracts import TicketCategory

    if category != TicketCategory.DEPOSIT or any(
        term in normalized for term in high_risk_details
    ):
        abstention = _unsupported_abstention()
        return _OfflineDecision(
            answer_status=AnswerStatus.ABSTAINED,
            answer_text=abstention.text,
            citations=(),
            safety_flags=(),
            human_review_required=True,
            review_reasons=abstention.review_reasons,
        )
    try:
        draft_result = draft_deposit_answer(passages, query=text)
    except InsufficientEvidenceError:
        abstention = _unsupported_abstention()
        return _OfflineDecision(
            answer_status=AnswerStatus.ABSTAINED,
            answer_text=abstention.text,
            citations=abstention.citations,
            safety_flags=(),
            human_review_required=abstention.human_review_required,
            review_reasons=abstention.review_reasons,
        )

    return _OfflineDecision(
        answer_status=AnswerStatus.DRAFTED,
        answer_text=draft_result.text,
        citations=draft_result.citations,
        safety_flags=(),
        human_review_required=False,
        review_reasons=(),
    )


def process_offline_ticket(
    *,
    ticket_id: str,
    text: str,
    snapshot_path: Path,
    configuration_id: str = DEFAULT_CONFIGURATION_ID,
) -> AuditableProcessingResult:
    started_at = perf_counter()
    classification = process_ticket(ticket_id=ticket_id, text=text)
    ticket = SupportTicket(ticket_id=ticket_id, text=text)
    safety_result = apply_safety_policy(ticket)
    decision = (
        _decision_from_safety(safety_result)
        if safety_result is not None
        else _decision_from_knowledge(text, snapshot_path)
    )

    return build_auditable_result(
        classification=classification,
        answer_status=decision.answer_status,
        answer_text=decision.answer_text,
        citations=decision.citations,
        safety_flags=decision.safety_flags,
        human_review_required=decision.human_review_required,
        review_reasons=decision.review_reasons,
        configuration_id=configuration_id,
        latency_ms=(perf_counter() - started_at) * 1000,
    )
