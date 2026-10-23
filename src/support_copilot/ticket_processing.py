from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SupportTicket:
    ticket_id: str
    text: str


@dataclass(frozen=True, slots=True)
class ProcessingResult:
    ticket_id: str
    category: str | None


def classify_category(text: str) -> str | None:
    normalized_text = text.casefold()
    withdrawal_markers = ("withdraw",)

    if any(marker in normalized_text for marker in withdrawal_markers):
        return "withdrawal"
    return None


def process_ticket(ticket_id: str, text: str) -> ProcessingResult:
    ticket = SupportTicket(ticket_id=ticket_id, text=text)
    return ProcessingResult(
        ticket_id=ticket.ticket_id,
        category=classify_category(ticket.text),
    )
