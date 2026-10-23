import sys
from datetime import UTC, datetime
from pathlib import Path

from behave import given, then, when

PROJECT_ROOT = Path(__file__).resolve().parents[3]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))


@given("the configured knowledge base contains the four approved Valetax pages")
def step_configured_kb_contains_approved_pages(context) -> None:
    from support_copilot.knowledge_base import load_snapshot

    fixture_path = PROJECT_ROOT / "tests" / "fixtures" / "kb" / "synthetic_snapshot.json"
    context.snapshot = load_snapshot(fixture_path)
    assert len(context.snapshot.documents) == 4
    assert context.snapshot.synthetic is True


@when("passages are retrieved for a deposit question")
def step_retrieve_deposit_passages(context) -> None:
    from support_copilot.knowledge_base import retrieve_passages

    context.passages = retrieve_passages(
        context.snapshot,
        query="How can I deposit funds?",
        retrieved_at=datetime(2026, 10, 24, 1, tzinfo=UTC),
    )


@then("every candidate passage identifies one of those approved source pages")
def step_every_passage_is_approved(context) -> None:
    from support_copilot.knowledge_base import APPROVED_SOURCE_URLS

    assert context.passages
    assert {passage.url for passage in context.passages} <= APPROVED_SOURCE_URLS
