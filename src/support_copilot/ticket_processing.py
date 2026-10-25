from support_copilot.contracts import (
    ProcessingResult,
    SupportTicket,
    TicketCategory,
    TicketLanguage,
    TicketSentiment,
    TicketUrgency,
)


def classify_category(text: str) -> TicketCategory:
    normalized_text = text.casefold()
    markers = {
        TicketCategory.WITHDRAWAL: ("withdraw", "payout"),
        TicketCategory.DEPOSIT: ("deposit", "fund my account", "add funds"),
        TicketCategory.ACCOUNT_OPENING: (
            "open an account",
            "create an account",
            "sign up",
            "registration",
        ),
        TicketCategory.VERIFICATION: ("verify", "verification", "kyc", "upload documents"),
    }
    matches = [
        category for category, keywords in markers.items()
        if any(keyword in normalized_text for keyword in keywords)
    ]
    return matches[0] if len(matches) == 1 else TicketCategory.OTHER


def classify_urgency(text: str) -> TicketUrgency:
    normalized_text = text.casefold()
    high_urgency_markers = ("urgent", "immediately", "asap")
    if any(marker in normalized_text for marker in high_urgency_markers):
        return TicketUrgency.HIGH
    return TicketUrgency.NORMAL


def classify_language(text: str) -> TicketLanguage:
    if any("a" <= character.casefold() <= "z" for character in text):
        return TicketLanguage.ENGLISH
    return TicketLanguage.UNKNOWN


def classify_sentiment(text: str) -> TicketSentiment:
    normalized_text = text.casefold()
    negative_markers = ("frustrated", "frustrating", "angry")
    if any(marker in normalized_text for marker in negative_markers):
        return TicketSentiment.NEGATIVE
    return TicketSentiment.NEUTRAL


def process_ticket(ticket_id: str, text: str) -> ProcessingResult:
    ticket = SupportTicket(ticket_id=ticket_id, text=text)
    return ProcessingResult(
        ticket_id=ticket.ticket_id,
        category=classify_category(ticket.text),
        urgency=classify_urgency(ticket.text),
        language=classify_language(ticket.text),
        sentiment=classify_sentiment(ticket.text),
    )
