import hashlib
import re
from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

APPROVED_SOURCE_URLS = frozenset(
    {
        "https://valetax.com/how-to-deposit/",
        "https://valetax.com/how-to-withdraw/",
        "https://valetax.com/how-to-open-an-account/",
        "https://valetax.com/how-to-verify-account/",
    }
)


class KnowledgeBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)


class SourceSection(KnowledgeBaseModel):
    heading: str = Field(min_length=1)
    text: str = Field(min_length=1)


class SourceDocument(KnowledgeBaseModel):
    source_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    url: str = Field(min_length=1)
    content_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    sections: tuple[SourceSection, ...] = Field(min_length=1)


class KBSnapshot(KnowledgeBaseModel):
    snapshot_id: str = Field(min_length=1)
    captured_at: datetime
    synthetic: bool
    documents: tuple[SourceDocument, ...] = Field(min_length=1)


class RetrievedPassage(KnowledgeBaseModel):
    source_id: str
    title: str
    url: str
    heading: str
    passage: str
    retrieved_at: datetime
    content_hash: str
    snapshot_id: str
    synthetic: bool


def compute_document_hash(document: SourceDocument) -> str:
    section_content = "\n".join(
        f"{section.heading}\n{section.text}" for section in document.sections
    )
    canonical_content = f"{document.title}\n{section_content}"
    return hashlib.sha256(canonical_content.encode("utf-8")).hexdigest()


def validate_snapshot_integrity(snapshot: KBSnapshot) -> None:
    for document in snapshot.documents:
        actual_hash = compute_document_hash(document)
        if actual_hash != document.content_hash:
            raise ValueError(f"Content hash mismatch for source {document.source_id}")


def load_snapshot(path: Path) -> KBSnapshot:
    snapshot = KBSnapshot.model_validate_json(path.read_text(encoding="utf-8"))
    validate_snapshot_integrity(snapshot)
    return snapshot


def save_snapshot(snapshot: KBSnapshot, path: Path) -> None:
    validate_snapshot_integrity(snapshot)
    path.write_text(snapshot.model_dump_json(indent=2), encoding="utf-8")


def _lexical_tokens(text: str) -> set[str]:
    tokens = re.findall(r"[a-z0-9]+", text.casefold())
    return {token[:-1] if len(token) > 3 and token.endswith("s") else token for token in tokens}


def retrieve_passages(
    snapshot: KBSnapshot,
    query: str,
    retrieved_at: datetime,
) -> list[RetrievedPassage]:
    query_tokens = _lexical_tokens(query)
    scored_passages: list[tuple[int, RetrievedPassage]] = []

    for document in snapshot.documents:
        if document.url not in APPROVED_SOURCE_URLS:
            continue
        for section in document.sections:
            section_tokens = _lexical_tokens(f"{section.heading} {section.text}")
            score = len(query_tokens & section_tokens)
            if score == 0:
                continue
            scored_passages.append(
                (
                    score,
                    RetrievedPassage(
                        source_id=document.source_id,
                        title=document.title,
                        url=document.url,
                        heading=section.heading,
                        passage=section.text,
                        retrieved_at=retrieved_at,
                        content_hash=document.content_hash,
                        snapshot_id=snapshot.snapshot_id,
                        synthetic=snapshot.synthetic,
                    ),
                )
            )

    scored_passages.sort(key=lambda item: (-item[0], item[1].source_id, item[1].heading))
    return [passage for _, passage in scored_passages]
