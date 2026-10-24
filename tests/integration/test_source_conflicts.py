from datetime import UTC, datetime

from support_copilot.abstention import ReviewReason
from support_copilot.conflicts import build_source_conflict_abstention
from support_copilot.knowledge_base import (
    KBSnapshot,
    SourceDocument,
    SourceSection,
    compute_document_hash,
    load_snapshot,
    retrieve_passages,
    save_snapshot,
)


def _document(source_id: str, title: str, url: str, duration: str) -> SourceDocument:
    document = SourceDocument(
        source_id=source_id,
        title=title,
        url=url,
        content_hash="0" * 64,
        sections=(
            SourceSection(
                heading="Withdrawal processing time",
                text=f"Withdrawal processing time is {duration}.",
            ),
        ),
    )
    return document.model_copy(update={"content_hash": compute_document_hash(document)})


def test_retrieved_approved_conflicts_reach_typed_abstention(tmp_path) -> None:
    captured_at = datetime(2026, 10, 24, 1, tzinfo=UTC)
    snapshot = KBSnapshot(
        snapshot_id="snapshot-synthetic-conflict",
        captured_at=captured_at,
        synthetic=True,
        documents=(
            _document(
                "KB-001",
                "How to Withdraw",
                "https://valetax.com/how-to-withdraw/",
                "1 business day",
            ),
            _document(
                "KB-002",
                "How to Open an Account",
                "https://valetax.com/how-to-open-an-account/",
                "3 business days",
            ),
        ),
    )
    snapshot_path = tmp_path / "conflicting-snapshot.json"
    save_snapshot(snapshot, snapshot_path)
    persisted = load_snapshot(snapshot_path)
    passages = retrieve_passages(
        persisted,
        query="withdrawal processing time",
        retrieved_at=captured_at,
    )

    result = build_source_conflict_abstention(
        passages,
        requested_detail="withdrawal processing time",
    )
    payload = result.model_dump(mode="json")

    assert len(payload["citations"]) == 2
    assert {citation["url"] for citation in payload["citations"]} == {
        "https://valetax.com/how-to-withdraw/",
        "https://valetax.com/how-to-open-an-account/",
    }
    assert payload["review_reasons"] == [ReviewReason.SOURCE_CONFLICT.value]
