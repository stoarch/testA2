from support_copilot.abstention import ReviewReason
from support_copilot.audit import AnswerStatus, UsageData, build_auditable_result
from support_copilot.contracts import (
    ProcessingResult,
    TicketCategory,
    TicketLanguage,
    TicketSentiment,
    TicketUrgency,
)
from support_copilot.evaluation import (
    EvaluationCase,
    EvaluationCaseKind,
    EvaluationDataset,
    ExpectedEvaluationOutcome,
    TokenPricing,
    build_evaluation_report,
)
from support_copilot.safety import SafetyFlag


def _case(
    case_id: str,
    kind: EvaluationCaseKind,
    *,
    category: TicketCategory = TicketCategory.OTHER,
    answer_status: AnswerStatus = AnswerStatus.ABSTAINED,
    safety_flags: tuple[SafetyFlag, ...] = (),
    review: bool = True,
    review_reasons: tuple[ReviewReason, ...] = (ReviewReason.INSUFFICIENT_KNOWLEDGE,),
) -> EvaluationCase:
    return EvaluationCase(
        case_id=case_id,
        kind=kind,
        ticket_id=f"TICKET-{case_id}",
        text=f"Synthetic evaluation text for {case_id}",
        expected=ExpectedEvaluationOutcome(
            category=category,
            urgency=TicketUrgency.NORMAL,
            language=TicketLanguage.ENGLISH,
            sentiment=TicketSentiment.NEUTRAL,
            answer_status=answer_status,
            safety_flags=safety_flags,
            human_review_required=review,
            review_reasons=review_reasons,
        ),
    )


def _result(
    case: EvaluationCase,
    *,
    category: TicketCategory | None = None,
    answer_status: AnswerStatus | None = None,
    safety_flags: tuple[SafetyFlag, ...] | None = None,
    review: bool | None = None,
    review_reasons: tuple[ReviewReason, ...] | None = None,
    latency_ms: float,
    usage: UsageData | None = None,
):
    expected = case.expected
    return build_auditable_result(
        classification=ProcessingResult(
            ticket_id=case.ticket_id,
            category=category or expected.category,
            urgency=expected.urgency,
            language=expected.language,
            sentiment=expected.sentiment,
        ),
        answer_status=answer_status or expected.answer_status,
        answer_text="A safe aggregate-test result.",
        citations=(),
        safety_flags=expected.safety_flags if safety_flags is None else safety_flags,
        human_review_required=expected.human_review_required if review is None else review,
        review_reasons=expected.review_reasons if review_reasons is None else review_reasons,
        configuration_id="test-configuration",
        latency_ms=latency_ms,
        usage=usage,
    )


def _dataset() -> EvaluationDataset:
    return EvaluationDataset(
        dataset_id="metric-test-set",
        synthetic=True,
        cases=(
            _case(
                "NORMAL",
                EvaluationCaseKind.NORMAL,
                answer_status=AnswerStatus.DRAFTED,
                review=False,
                review_reasons=(),
            ),
            _case("GAP", EvaluationCaseKind.GAP),
            _case(
                "CONFLICT",
                EvaluationCaseKind.CONFLICT,
                category=TicketCategory.WITHDRAWAL,
            ),
            _case(
                "SAFETY",
                EvaluationCaseKind.SAFETY,
                answer_status=AnswerStatus.REFUSED,
                safety_flags=(SafetyFlag.TRADING_ADVICE,),
                review_reasons=(ReviewReason.TRADING_ADVICE,),
            ),
        ),
    )


def test_evaluation_report_calculates_explicit_metric_denominators_and_percentiles() -> None:
    dataset = _dataset()
    results = (
        _result(dataset.cases[0], latency_ms=10, review=True),
        _result(dataset.cases[1], latency_ms=20),
        _result(
            dataset.cases[2],
            category=TicketCategory.OTHER,
            answer_status=AnswerStatus.DRAFTED,
            review=False,
            review_reasons=(),
            latency_ms=30,
        ),
        _result(dataset.cases[3], latency_ms=40),
    )

    report = build_evaluation_report(dataset, results, execution_mode="offline_fixture")

    assert report.classification_accuracy.model_dump() == {
        "numerator": 3,
        "denominator": 4,
        "rate": 0.75,
    }
    assert report.safety_accuracy.rate == 1.0
    assert report.grounding_accuracy.rate == 0.75
    assert report.citation_validity.denominator == 4
    assert report.review_rate.rate == 0.75
    assert report.review_recall.rate == 2 / 3
    assert report.false_review_rate.rate == 1.0
    assert report.latency.sample_count == 4
    assert report.latency.p50_ms == 25.0
    assert report.latency.p95_ms == 38.5
    assert report.cost.status == "unavailable"
    assert report.cost.amount_usd is None


def test_evaluation_report_measures_cost_only_with_usage_and_pricing() -> None:
    dataset = _dataset()
    usage = UsageData(input_tokens=100, output_tokens=50)
    results = tuple(
        _result(case, latency_ms=index, usage=usage)
        for index, case in enumerate(dataset.cases, start=1)
    )

    report = build_evaluation_report(
        dataset,
        results,
        execution_mode="offline_fixture",
        pricing=TokenPricing(input_usd_per_million=2.0, output_usd_per_million=4.0),
    )

    assert report.cost.status == "measured"
    assert report.cost.input_tokens == 400
    assert report.cost.output_tokens == 200
    assert report.cost.amount_usd == 0.0016

