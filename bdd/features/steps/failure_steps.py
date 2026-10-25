import sys
from datetime import datetime
from pathlib import Path

from behave import given, then, when

PROJECT_ROOT = Path(__file__).resolve().parents[3]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))


@given("the retrieval dependency fails")
def step_retrieval_dependency_fails(context) -> None:
    from support_copilot.knowledge_base import (
        KBSnapshot,
        RetrievalUnavailableError,
        RetrievedPassage,
    )

    def failing_retriever(
        snapshot: KBSnapshot,
        query: str,
        retrieved_at: datetime,
    ) -> list[RetrievedPassage]:
        del snapshot, query, retrieved_at
        raise RetrievalUnavailableError("simulated retrieval dependency failure")

    context.retrieval_failure_retriever = failing_retriever


@when("a ticket is processed")
def step_ticket_is_processed_during_retrieval_failure(context) -> None:
    from support_copilot.application import process_offline_ticket

    fixture_path = (
        PROJECT_ROOT / "tests" / "fixtures" / "kb" / "synthetic_snapshot.json"
    )
    context.retrieval_failure_result = process_offline_ticket(
        ticket_id="TICKET-SCN-021",
        text="How do I make a deposit?",
        snapshot_path=fixture_path,
        retriever=context.retrieval_failure_retriever,
    )


@then("no customer answer is drafted from model memory")
def step_no_answer_is_drafted_from_model_memory(context) -> None:
    assert context.retrieval_failure_result.answer_status == "abstained"
    assert context.retrieval_failure_result.citations == ()
    assert "temporarily unable to verify" in (
        context.retrieval_failure_result.answer_text.casefold()
    )


@then("a typed error result requires human review")
def step_typed_error_result_requires_human_review(context) -> None:
    from support_copilot.abstention import ReviewReason
    from support_copilot.audit import AuditableProcessingResult

    assert isinstance(context.retrieval_failure_result, AuditableProcessingResult)
    assert context.retrieval_failure_result.human_review_required is True
    assert context.retrieval_failure_result.review_reasons == (
        ReviewReason.RETRIEVAL_FAILURE,
    )
