from datetime import UTC, datetime

import pytest

from support_copilot.knowledge_base import (
    APPROVED_SOURCE_URLS,
    KBSnapshot,
    SourceDocument,
    SourceSection,
    retrieve_passages,
    validate_snapshot_integrity,
)


def test_retrieval_excludes_non_allowlisted_sources_and_preserves_provenance() -> None:
    captured_at = datetime(2026, 10, 24, tzinfo=UTC)
    approved_document = SourceDocument(
        source_id="KB-001",
        title="How to Deposit",
        url="https://valetax.com/how-to-deposit/",
        content_hash="a" * 64,
        sections=[
            SourceSection(
                heading="Deposit overview",
                text="Synthetic fixture: make a deposit from the deposit area.",
            )
        ],
    )
    unapproved_document = SourceDocument(
        source_id="UNAPPROVED-001",
        title="Unapproved deposit advice",
        url="https://example.test/deposit-advice",
        content_hash="b" * 64,
        sections=[
            SourceSection(
                heading="Deposit overview",
                text="Synthetic fixture: make a deposit from an unapproved page.",
            )
        ],
    )
    snapshot = KBSnapshot(
        snapshot_id="snapshot-synthetic-unit",
        captured_at=captured_at,
        synthetic=True,
        documents=[approved_document, unapproved_document],
    )

    passages = retrieve_passages(
        snapshot,
        query="How do I make a deposit?",
        retrieved_at=captured_at,
    )

    assert len(passages) == 1
    assert passages[0].url in APPROVED_SOURCE_URLS
    assert passages[0].snapshot_id == snapshot.snapshot_id
    assert passages[0].content_hash == approved_document.content_hash
    assert passages[0].heading == "Deposit overview"
    assert passages[0].passage == approved_document.sections[0].text
    assert passages[0].retrieved_at == captured_at
    assert passages[0].synthetic is True


def test_snapshot_integrity_rejects_a_mismatched_document_hash() -> None:
    snapshot = KBSnapshot(
        snapshot_id="snapshot-synthetic-corrupt",
        captured_at=datetime(2026, 10, 24, tzinfo=UTC),
        synthetic=True,
        documents=[
            SourceDocument(
                source_id="KB-001",
                title="How to Deposit",
                url="https://valetax.com/how-to-deposit/",
                content_hash="0" * 64,
                sections=[
                    SourceSection(
                        heading="Deposit overview",
                        text="Synthetic fixture: deposit instructions.",
                    )
                ],
            )
        ],
    )

    with pytest.raises(ValueError, match="Content hash mismatch for source KB-001"):
        validate_snapshot_integrity(snapshot)
