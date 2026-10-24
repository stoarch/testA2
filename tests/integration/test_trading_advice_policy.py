from support_copilot.abstention import ReviewReason
from support_copilot.contracts import SupportTicket
from support_copilot.safety import apply_trading_advice_policy


def test_ticket_contract_reaches_policy_refusal_without_retrieval_or_provider() -> None:
    ticket = SupportTicket(
        ticket_id="TICKET-SAFETY-INTEGRATION-001",
        text="Can you recommend whether I should buy GBP/JPY?",
    )

    result = apply_trading_advice_policy(ticket)

    assert result is not None
    assert result.status == "refused"
    assert result.human_review_required is True
    assert result.review_reasons == (ReviewReason.TRADING_ADVICE,)
    assert result.citations == ()
