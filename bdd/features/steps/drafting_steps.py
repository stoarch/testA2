import sys
from datetime import UTC, datetime
from pathlib import Path

from behave import given, then, when

PROJECT_ROOT = Path(__file__).resolve().parents[3]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))


@given("the deposit page supports the steps needed to make a deposit")
def step_deposit_page_supports_steps(context) -> None:
    from support_copilot.knowledge_base import load_snapshot, retrieve_passages

    fixture_path = PROJECT_ROOT / "tests" / "fixtures" / "kb" / "synthetic_snapshot.json"
    snapshot = load_snapshot(fixture_path)
    context.deposit_passages = retrieve_passages(
        snapshot,
        query="How can I deposit funds?",
        retrieved_at=datetime(2026, 10, 24, 1, tzinfo=UTC),
    )
    assert context.deposit_passages


@when("a customer asks how to deposit")
def step_customer_asks_how_to_deposit(context) -> None:
    from support_copilot.drafting import draft_deposit_answer

    context.draft_result = draft_deposit_answer(context.deposit_passages)


@then("the draft summarizes only supported steps")
def step_draft_summarizes_supported_steps(context) -> None:
    assert context.draft_result.text.casefold() in context.deposit_passages[0].passage.casefold()


@then("it cites the deposit page")
def step_draft_cites_deposit_page(context) -> None:
    assert context.draft_result.citations
    assert context.draft_result.citations[0].url == "https://valetax.com/how-to-deposit/"
