import sys
from datetime import UTC, datetime
from pathlib import Path

from behave import given, then, when

PROJECT_ROOT = Path(__file__).resolve().parents[3]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))


@given("a customer asks for a fee not stated in the approved pages")
def step_customer_asks_for_uncovered_fee(context) -> None:
    from support_copilot.knowledge_base import load_snapshot, retrieve_passages

    fixture_path = PROJECT_ROOT / "tests" / "fixtures" / "kb" / "synthetic_snapshot.json"
    snapshot = load_snapshot(fixture_path)
    context.fee_passages = retrieve_passages(
        snapshot,
        query="What is the withdrawal fee?",
        retrieved_at=datetime(2026, 10, 24, 1, tzinfo=UTC),
    )
    assert context.fee_passages


@when("the ticket is processed")
def step_uncovered_fee_ticket_is_processed(context) -> None:
    from support_copilot.abstention import build_uncovered_fee_abstention

    context.abstention_result = build_uncovered_fee_abstention(context.fee_passages)


@then("the co-pilot states that the available knowledge base does not establish the fee")
def step_result_states_fee_is_not_established(context) -> None:
    assert "does not establish the requested fee" in context.abstention_result.text


@then("it does not invent an amount")
def step_result_does_not_invent_amount(context) -> None:
    assert not any(character.isdigit() for character in context.abstention_result.text)


@then("human review is required")
def step_human_review_is_required(context) -> None:
    from support_copilot.abstention import ReviewReason

    assert context.abstention_result.human_review_required is True
    assert context.abstention_result.review_reasons == (
        ReviewReason.INSUFFICIENT_KB_COVERAGE,
    )
