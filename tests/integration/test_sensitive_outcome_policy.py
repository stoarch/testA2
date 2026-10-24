from support_copilot.abstention import ReviewReason
from support_copilot.contracts import SupportTicket
from support_copilot.safety import apply_safety_policy


def test_kyc_ticket_reaches_human_route_without_retrieval_or_provider() -> None:
    ticket = SupportTicket(
        ticket_id="TICKET-SENSITIVE-INTEGRATION-001",
        text="Can you tell me whether my verification should be approved?",
    )

    result = apply_safety_policy(ticket)

    assert result is not None
    assert result.status == "routed"
    assert result.citations == ()
    assert result.human_review_required is True
    assert result.review_reasons == (ReviewReason.KYC,)
    assert "approve" not in result.text.casefold()
    assert "reject" not in result.text.casefold()


def test_complaint_ticket_reaches_human_route_without_retrieval_or_provider() -> None:
    ticket = SupportTicket(
        ticket_id="TICKET-SENSITIVE-INTEGRATION-002",
        text="Should the broker uphold or reject my complaint?",
    )

    result = apply_safety_policy(ticket)

    assert result is not None
    assert result.status == "routed"
    assert result.citations == ()
    assert result.human_review_required is True
    assert result.review_reasons == (ReviewReason.COMPLAINT,)
    assert "uphold" not in result.text.casefold()
    assert "reject" not in result.text.casefold()
