from datetime import UTC, datetime
from pathlib import Path

from support_copilot.knowledge_base import (
    APPROVED_SOURCE_URLS,
    load_snapshot,
    retrieve_passages,
    save_snapshot,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FIXTURE_PATH = PROJECT_ROOT / "tests" / "fixtures" / "kb" / "synthetic_snapshot.json"


def test_persisted_snapshot_round_trip_and_approved_retrieval(tmp_path: Path) -> None:
    snapshot = load_snapshot(FIXTURE_PATH)
    persisted_path = tmp_path / "snapshot.json"

    save_snapshot(snapshot, persisted_path)
    reloaded = load_snapshot(persisted_path)
    passages = retrieve_passages(
        reloaded,
        query="How can I deposit funds?",
        retrieved_at=datetime(2026, 10, 24, 1, tzinfo=UTC),
    )

    assert reloaded == snapshot
    assert len(reloaded.documents) == 4
    assert reloaded.synthetic is True
    assert passages
    assert {passage.url for passage in passages} <= APPROVED_SOURCE_URLS
    assert all(passage.synthetic is True for passage in passages)
