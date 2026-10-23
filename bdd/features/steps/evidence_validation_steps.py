import sys
from datetime import UTC, datetime
from pathlib import Path

from behave import given, then, when

PROJECT_ROOT = Path(__file__).resolve().parents[3]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))


@given("a draft mentions a processing or completion time")
def step_draft_mentions_timeline(context) -> None:
    from support_copilot.drafting import Citation, DraftResult
    from support_copilot.knowledge_base import load_snapshot, retrieve_passages

    fixture_path = PROJECT_ROOT / "tests" / "fixtures" / "kb" / "synthetic_snapshot.json"
    snapshot = load_snapshot(fixture_path)
    passages = retrieve_passages(
        snapshot,
        query="How long does account opening take?",
        retrieved_at=datetime(2026, 10, 24, 1, tzinfo=UTC),
    )
    context.timeline_draft = DraftResult(
        text="Account opening is completed within 48 hours.",
        citations=(Citation.from_passage(passages[0]),),
    )


@when("the result is validated")
def step_result_is_validated(context) -> None:
    from support_copilot.evidence_validation import validate_timeline_claims

    context.validated_timeline_claims = validate_timeline_claims(context.timeline_draft)


@then("the exact timeline claim is supported by a cited passage")
def step_exact_timeline_is_supported(context) -> None:
    assert context.validated_timeline_claims == ("48 hours",)
    assert "48 hours" in context.timeline_draft.citations[0].passage.casefold()
