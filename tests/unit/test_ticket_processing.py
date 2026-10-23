from support_copilot.ticket_processing import process_ticket


def test_process_ticket_preserves_ticket_identifier() -> None:
    result = process_ticket(ticket_id="TICKET-001", text="How do I withdraw funds?")

    assert result.ticket_id == "TICKET-001"
