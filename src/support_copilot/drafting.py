import re
from collections.abc import Sequence
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from support_copilot.knowledge_base import RetrievedPassage

DEPOSIT_SOURCE_URL = "https://valetax.com/how-to-deposit/"
SYNTHETIC_FIXTURE_PREFIX = "Synthetic fixture for testing: "

_UNSUPPORTED_DEPOSIT_PATTERNS = (
    re.compile(r"\b(cancel|cancelling|cancellation|undo|revert|void|refund)\b", re.IGNORECASE),
    re.compile(r"\b(fee|fees|cost|costs|charge|charges|commission|pricing)\b", re.IGNORECASE),
    re.compile(
        r"\b(limit|limits|minimum|maximum|min|max|time|timeline|timelines|duration|processing|pending|delay|status|fast|speed)\b",
        re.IGNORECASE,
    ),
    re.compile(r"\bhow\s+long\b", re.IGNORECASE),
)

_SUPPORTED_DEPOSIT_HOW_TO_PATTERNS = (
    re.compile(r"\b(how|where)\b.{0,40}\bdeposit", re.IGNORECASE),
    re.compile(r"\bdeposit\b.{0,40}\b(how|where)\b", re.IGNORECASE),
)


def is_supported_deposit_query(query: str) -> bool:
    if not query:
        return True
    for pattern in _UNSUPPORTED_DEPOSIT_PATTERNS:
        if pattern.search(query):
            return False
    return any(pattern.search(query) for pattern in _SUPPORTED_DEPOSIT_HOW_TO_PATTERNS)


class DraftingModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)


class Citation(DraftingModel):
    source_id: str
    title: str
    url: str
    heading: str
    passage: str
    retrieved_at: datetime
    content_hash: str
    snapshot_id: str
    synthetic: bool

    @classmethod
    def from_passage(cls, passage: RetrievedPassage) -> "Citation":
        return cls.model_validate(passage.model_dump())


class DraftResult(DraftingModel):
    text: str = Field(min_length=1)
    citations: tuple[Citation, ...] = Field(min_length=1)


class InsufficientEvidenceError(ValueError):
    pass


def _extract_supported_text(passage: RetrievedPassage) -> str:
    supported_text = passage.passage.removeprefix(SYNTHETIC_FIXTURE_PREFIX)
    return supported_text[0].upper() + supported_text[1:]


def draft_deposit_answer(
    passages: Sequence[RetrievedPassage],
    query: str = "",
) -> DraftResult:
    if query and not is_supported_deposit_query(query):
        raise InsufficientEvidenceError(
            "Query operation or attribute is not supported by available deposit evidence"
        )

    deposit_evidence = next(
        (passage for passage in passages if passage.url == DEPOSIT_SOURCE_URL),
        None,
    )
    if deposit_evidence is None:
        raise InsufficientEvidenceError("Cannot draft without approved deposit evidence")

    return DraftResult(
        text=_extract_supported_text(deposit_evidence),
        citations=(Citation.from_passage(deposit_evidence),),
    )
