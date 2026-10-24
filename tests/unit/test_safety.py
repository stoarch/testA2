from support_copilot.abstention import ReviewReason
from support_copilot.contracts import SupportTicket
from support_copilot.safety import SafetyFlag, apply_trading_advice_policy


def test_direct_buy_recommendation_is_refused_and_routed() -> None:
    ticket = SupportTicket(
        ticket_id="TICKET-SAFETY-001",
        text="Should I buy EUR/USD now?",
    )

    result = apply_trading_advice_policy(ticket)

    assert result is not None
    assert result.status == "refused"
    assert "can't provide trading advice" in result.text
    assert "EUR/USD" not in result.text
    assert "signal" not in result.text.casefold()
    assert "price target" not in result.text.casefold()
    assert result.human_review_required is True
    assert result.review_reasons == (ReviewReason.TRADING_ADVICE,)
    assert result.safety_flags == (SafetyFlag.TRADING_ADVICE,)


def test_operational_buy_word_does_not_trigger_trading_advice_policy() -> None:
    ticket = SupportTicket(
        ticket_id="TICKET-SAFETY-002",
        text="Where can I buy a replacement security key for my account?",
    )

    assert apply_trading_advice_policy(ticket) is None


def test_personalized_leverage_request_is_refused_without_a_setting() -> None:
    ticket = SupportTicket(
        ticket_id="TICKET-SAFETY-003",
        text="Which leverage setting should I choose?",
    )

    result = apply_trading_advice_policy(ticket)

    assert result is not None
    assert result.status == "refused"
    assert "can't recommend a leverage setting" in result.text
    assert not any(character.isdigit() for character in result.text)
    assert "up to" not in result.text.casefold()
    assert result.human_review_required is True
    assert result.review_reasons == (ReviewReason.TRADING_ADVICE,)
    assert result.safety_flags == (SafetyFlag.TRADING_ADVICE,)


def test_general_leverage_definition_does_not_trigger_personalized_policy() -> None:
    ticket = SupportTicket(
        ticket_id="TICKET-SAFETY-004",
        text="What does leverage mean?",
    )

    assert apply_trading_advice_policy(ticket) is None
