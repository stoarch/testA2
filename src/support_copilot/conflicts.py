import re
from collections.abc import Sequence

from support_copilot.abstention import AbstentionResult, ReviewReason
from support_copilot.drafting import Citation
from support_copilot.knowledge_base import RetrievedPassage

_DURATION_PATTERN = re.compile(
    r"\b\d+(?:\.\d+)?\s+(?:business\s+)?(?:minute|hour|day|week)s?\b",
    flags=re.IGNORECASE,
)
_SOURCE_CONFLICT_MESSAGE = (
    "The approved sources conflict about the requested detail. "
    "A human reviewer must confirm it."
)


class NoSourceConflictError(ValueError):
    pass


def _normalize_text(text: str) -> str:
    return " ".join(text.casefold().split())


def _duration_claims(text: str) -> frozenset[str]:
    return frozenset(match.group(0).casefold() for match in _DURATION_PATTERN.finditer(text))


def _claim_passages_for_detail(
    passages: Sequence[RetrievedPassage],
    normalized_detail: str,
) -> list[tuple[RetrievedPassage, frozenset[str]]]:
    claim_passages: list[tuple[RetrievedPassage, frozenset[str]]] = []
    for passage in passages:
        if normalized_detail not in _normalize_text(passage.passage):
            continue
        claims = _duration_claims(passage.passage)
        if claims:
            claim_passages.append((passage, claims))
    return claim_passages


def build_source_conflict_abstention(
    passages: Sequence[RetrievedPassage],
    *,
    requested_detail: str,
) -> AbstentionResult:
    normalized_detail = _normalize_text(requested_detail)
    if not normalized_detail:
        raise ValueError("The requested detail cannot be empty")

    claim_passages = _claim_passages_for_detail(passages, normalized_detail)
    distinct_claims = {claim for _, claims in claim_passages for claim in claims}
    if len(claim_passages) < 2 or len(distinct_claims) < 2:
        raise NoSourceConflictError("No conflicting duration claims found for requested detail")

    return AbstentionResult(
        text=_SOURCE_CONFLICT_MESSAGE,
        citations=tuple(Citation.from_passage(passage) for passage, _ in claim_passages),
        review_reasons=(ReviewReason.SOURCE_CONFLICT,),
    )
