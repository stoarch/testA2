import sys
from datetime import UTC, datetime
from pathlib import Path

from behave import given, then, when

PROJECT_ROOT = Path(__file__).resolve().parents[3]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))


@given("approved pages provide conflicting or misleading wording for the requested detail")
def step_approved_pages_conflict(context) -> None:
    from support_copilot.knowledge_base import RetrievedPassage

    common = {
        "heading": "Withdrawal processing time",
        "retrieved_at": datetime(2026, 10, 24, 1, tzinfo=UTC),
        "snapshot_id": "snapshot-synthetic-bdd-conflict",
        "synthetic": True,
    }
    context.conflict_passages = (
        RetrievedPassage(
            source_id="KB-001",
            title="How to Withdraw",
            url="https://valetax.com/how-to-withdraw/",
            passage="Withdrawal processing time is 1 business day.",
            content_hash="a" * 64,
            **common,
        ),
        RetrievedPassage(
            source_id="KB-002",
            title="How to Open an Account",
            url="https://valetax.com/how-to-open-an-account/",
            passage="Withdrawal processing time is 3 business days.",
            content_hash="b" * 64,
            **common,
        ),
    )
    context.conflict_detail = "withdrawal processing time"


@when("that detail is needed in a draft")
def step_conflicting_detail_is_needed(context) -> None:
    from support_copilot.conflicts import build_source_conflict_abstention

    context.conflict_result = build_source_conflict_abstention(
        context.conflict_passages,
        requested_detail=context.conflict_detail,
    )


@then("the co-pilot abstains from the disputed claim")
def step_abstains_from_disputed_claim(context) -> None:
    assert context.conflict_result.status == "abstained"
    assert "1 business day" not in context.conflict_result.text
    assert "3 business days" not in context.conflict_result.text


@then("it exposes the relevant sources")
def step_exposes_relevant_sources(context) -> None:
    assert tuple(citation.source_id for citation in context.conflict_result.citations) == (
        "KB-001",
        "KB-002",
    )


@then('human review is required with reason "source_conflict"')
def step_source_conflict_requires_review(context) -> None:
    payload = context.conflict_result.model_dump(mode="json")
    assert payload["human_review_required"] is True
    assert payload["review_reasons"] == ["source_conflict"]
