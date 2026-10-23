import re

from support_copilot.drafting import DraftResult

_TIMELINE_DURATION_PATTERN = re.compile(
    r"\b\d+\s+(?:minutes?|hours?|days?|weeks?|months?)\b",
    flags=re.IGNORECASE,
)


class UnsupportedTimelineClaimError(ValueError):
    pass


def _timeline_durations(text: str) -> tuple[str, ...]:
    matches = _TIMELINE_DURATION_PATTERN.finditer(text)
    return tuple(
        dict.fromkeys(match.group(0).casefold() for match in matches)
    )


def validate_timeline_claims(result: DraftResult) -> tuple[str, ...]:
    claimed_durations = _timeline_durations(result.text)
    cited_durations = {
        duration
        for citation in result.citations
        for duration in _timeline_durations(citation.passage)
    }
    unsupported = tuple(
        duration for duration in claimed_durations if duration not in cited_durations
    )
    if unsupported:
        joined_claims = ", ".join(unsupported)
        raise UnsupportedTimelineClaimError(
            f"Timeline claim is absent from cited passages: {joined_claims}"
        )
    return claimed_durations
