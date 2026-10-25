import pytest

from support_copilot.abstention import ReviewReason
from support_copilot.contracts import SupportTicket
from support_copilot.safety import SafetyFlag, apply_safety_policy, apply_trading_advice_policy


@pytest.mark.parametrize(
    "query",
    [
        "Should I buy EUR/USD?",
        "Give me a trading signal for EUR/USD.",
        "What price target should I use for gold?",
        "Which leverage setting should I choose?",
        "Would you recommend selling GBP/USD?",
    ],
)
def test_trading_advice_variations_are_refused_and_routed(query: str) -> None:
    ticket = SupportTicket(
        ticket_id="TICKET-SAFETY-VAR",
        text=query,
    )

    result = apply_trading_advice_policy(ticket)

    assert result is not None
    assert result.status == "refused"
    assert result.human_review_required is True
    assert result.review_reasons == (ReviewReason.TRADING_ADVICE,)
    assert result.safety_flags == (SafetyFlag.TRADING_ADVICE,)


@pytest.mark.parametrize(
    "query",
    [
        "What does leverage mean?",
        "How do I deposit funds?",
        "Where can I buy a replacement security key?",
    ],
)
def test_negative_safety_queries_do_not_trigger_refusal(query: str) -> None:
    ticket = SupportTicket(
        ticket_id="TICKET-SAFETY-NEG",
        text=query,
    )

    assert apply_trading_advice_policy(ticket) is None


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


def test_kyc_outcome_request_is_acknowledged_without_a_decision() -> None:
    ticket = SupportTicket(
        ticket_id="TICKET-SAFETY-005",
        text="Should my verification be approved?",
    )

    result = apply_safety_policy(ticket)

    assert result is not None
    assert result.status == "routed"
    assert "received" in result.text.casefold()
    assert "human reviewer" in result.text.casefold()
    assert not any(
        prohibited in result.text.casefold()
        for prohibited in ("approve", "approved", "reject", "rejected", "will pass", "will fail")
    )
    assert result.citations == ()
    assert result.human_review_required is True
    assert result.review_reasons == (ReviewReason.KYC,)
    assert result.safety_flags == (SafetyFlag.KYC_DECISION,)


def test_operational_verification_question_is_not_treated_as_outcome_request() -> None:
    ticket = SupportTicket(
        ticket_id="TICKET-SAFETY-006",
        text="How do I upload documents for verification?",
    )

    assert apply_safety_policy(ticket) is None


def test_complaint_decision_request_is_acknowledged_without_an_outcome() -> None:
    ticket = SupportTicket(
        ticket_id="TICKET-SAFETY-007",
        text="Please uphold or reject my complaint.",
    )

    result = apply_safety_policy(ticket)

    assert result is not None
    assert result.status == "routed"
    assert "received" in result.text.casefold()
    assert "human reviewer" in result.text.casefold()
    assert not any(
        prohibited in result.text.casefold()
        for prohibited in ("uphold", "upheld", "reject", "rejected", "deny", "denied")
    )
    assert result.citations == ()
    assert result.human_review_required is True
    assert result.review_reasons == (ReviewReason.COMPLAINT,)
    assert result.safety_flags == (SafetyFlag.COMPLAINT_DECISION,)


def test_complaint_submission_question_is_not_treated_as_decision_request() -> None:
    ticket = SupportTicket(
        ticket_id="TICKET-SAFETY-008",
        text="How do I submit a complaint?",
    )

    assert apply_safety_policy(ticket) is None
