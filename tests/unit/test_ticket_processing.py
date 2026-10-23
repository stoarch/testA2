from support_copilot.ticket_processing import process_ticket


def test_process_ticket_preserves_ticket_identifier() -> None:
    result = process_ticket(ticket_id="TICKET-001", text="How do I withdraw funds?")

    assert result.ticket_id == "TICKET-001"


def test_process_ticket_classifies_withdrawal_request() -> None:
    result = process_ticket(ticket_id="TICKET-002", text="How do I withdraw funds?")

    assert result.category == "withdrawal"


def test_process_ticket_preserves_unsupported_topic_as_other() -> None:
    result = process_ticket(
        ticket_id="TICKET-003",
        text="Can I receive a paper account statement?",
    )

    assert result.category == "other"
    assert result.category not in {
        "deposit",
        "withdrawal",
        "account_opening",
        "verification",
    }
