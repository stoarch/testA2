from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SupportTicket:
    ticket_id: str
    text: str


@dataclass(frozen=True, slots=True)
class ProcessingResult:
    ticket_id: str


def process_ticket(ticket_id: str, text: str) -> ProcessingResult:
    ticket = SupportTicket(ticket_id=ticket_id, text=text)
    return ProcessingResult(ticket_id=ticket.ticket_id)
