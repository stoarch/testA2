import sys
from datetime import UTC, datetime
from pathlib import Path

from behave import given, then, when

PROJECT_ROOT = Path(__file__).resolve().parents[3]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))


@given("the co-pilot cannot support a complete answer from approved sources")
def step_approved_sources_cannot_support_complete_answer(context) -> None:
    from support_copilot.knowledge_base import load_snapshot, retrieve_passages

    fixture_path = PROJECT_ROOT / "tests" / "fixtures" / "kb" / "synthetic_snapshot.json"
    snapshot = load_snapshot(fixture_path)
    context.routing_passages = retrieve_passages(
        snapshot,
        query="What is the withdrawal fee?",
        retrieved_at=datetime(2026, 10, 24, 1, tzinfo=UTC),
    )
    assert context.routing_passages


@when("it abstains")
def step_result_abstains(context) -> None:
    from support_copilot.abstention import build_uncovered_fee_abstention

    context.routing_result = build_uncovered_fee_abstention(context.routing_passages)
    assert context.routing_result.status == "abstained"


@then("human_review_required is true")
def step_human_review_required_is_true(context) -> None:
    assert context.routing_result.human_review_required is True


@then('the route reason includes "insufficient_knowledge"')
def step_route_reason_includes_insufficient_knowledge(context) -> None:
    payload = context.routing_result.model_dump(mode="json")
    assert "insufficient_knowledge" in payload["review_reasons"]
