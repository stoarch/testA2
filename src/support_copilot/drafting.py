from collections.abc import Sequence
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from support_copilot.knowledge_base import RetrievedPassage

DEPOSIT_SOURCE_URL = "https://valetax.com/how-to-deposit/"
SYNTHETIC_FIXTURE_PREFIX = "Synthetic fixture for testing: "


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


def draft_deposit_answer(passages: Sequence[RetrievedPassage]) -> DraftResult:
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
