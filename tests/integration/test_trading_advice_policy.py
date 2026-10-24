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


def test_leverage_request_is_refused_without_copying_source_marketing() -> None:
    ticket = SupportTicket(
        ticket_id="TICKET-SAFETY-INTEGRATION-002",
        text="What leverage should I choose for my account?",
    )
    source_marketing = "leverage up to 1:2000"

    result = apply_trading_advice_policy(ticket)

    assert result is not None
    assert result.status == "refused"
    assert source_marketing not in result.text.casefold()
    assert "1:2000" not in result.text
    assert result.human_review_required is True
    assert result.review_reasons == (ReviewReason.TRADING_ADVICE,)
