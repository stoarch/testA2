from datetime import UTC, datetime
from pathlib import Path

from support_copilot.drafting import draft_deposit_answer
from support_copilot.knowledge_base import load_snapshot, retrieve_passages

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FIXTURE_PATH = PROJECT_ROOT / "tests" / "fixtures" / "kb" / "synthetic_snapshot.json"


def test_retrieved_deposit_evidence_produces_a_grounded_draft() -> None:
    snapshot = load_snapshot(FIXTURE_PATH)
    passages = retrieve_passages(
        snapshot,
        query="How can I deposit funds?",
        retrieved_at=datetime(2026, 10, 24, 1, tzinfo=UTC),
    )

    result = draft_deposit_answer(passages)

    assert result.text.casefold() in passages[0].passage.casefold()
    assert result.citations[0].passage == passages[0].passage
    assert result.citations[0].snapshot_id == snapshot.snapshot_id
