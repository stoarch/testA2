from collections.abc import Sequence
from enum import StrEnum
from pathlib import Path
from typing import Literal

from pydantic import Field, model_validator

from support_copilot.abstention import ReviewReason
from support_copilot.application import DEFAULT_CONFIGURATION_ID, process_offline_ticket
from support_copilot.audit import AnswerStatus, AuditableProcessingResult
from support_copilot.contracts import (
    ContractModel,
    TicketCategory,
    TicketLanguage,
    TicketSentiment,
    TicketUrgency,
)
from support_copilot.safety import SafetyFlag


class EvaluationCaseKind(StrEnum):
    NORMAL = "normal"
    GAP = "gap"
    CONFLICT = "conflict"
    SAFETY = "safety"


class ExecutionMode(StrEnum):
    OFFLINE_FIXTURE = "offline_fixture"
    RULES_ONLY = "rules_only"
    LIVE_PROVIDER = "live_provider"


class ExpectedEvaluationOutcome(ContractModel):
    category: TicketCategory
    urgency: TicketUrgency
    language: TicketLanguage
    sentiment: TicketSentiment
    answer_status: AnswerStatus
    citation_source_ids: tuple[str, ...] = ()
    safety_flags: tuple[SafetyFlag, ...] = ()
    human_review_required: bool
    review_reasons: tuple[ReviewReason, ...] = ()


class EvaluationCase(ContractModel):
    case_id: str = Field(min_length=1)
    kind: EvaluationCaseKind
    ticket_id: str = Field(min_length=1)
    text: str = Field(min_length=1)
    expected: ExpectedEvaluationOutcome


class EvaluationDataset(ContractModel):
    dataset_id: str = Field(min_length=1)
    synthetic: bool
    cases: tuple[EvaluationCase, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_case_coverage(self) -> "EvaluationDataset":
        case_ids = [case.case_id for case in self.cases]
        if len(case_ids) != len(set(case_ids)):
            raise ValueError("Evaluation case IDs must be unique")

        missing_kinds = set(EvaluationCaseKind) - {case.kind for case in self.cases}
        if missing_kinds:
            missing = ", ".join(sorted(kind.value for kind in missing_kinds))
            raise ValueError(f"Evaluation dataset is missing required case kinds: {missing}")
        return self


class RatioMeasurement(ContractModel):
    numerator: int = Field(ge=0)
    denominator: int = Field(ge=0)
    rate: float | None = Field(default=None, ge=0.0, le=1.0)

    @model_validator(mode="after")
    def validate_ratio(self) -> "RatioMeasurement":
        if self.numerator > self.denominator:
            raise ValueError("Metric numerator cannot exceed its denominator")
        expected_rate = self.numerator / self.denominator if self.denominator else None
        if self.rate != expected_rate:
            raise ValueError("Metric rate must equal numerator divided by denominator")
        return self


class LatencyMeasurement(ContractModel):
    sample_count: int = Field(ge=1)
    p50_ms: float = Field(ge=0.0)
    p95_ms: float = Field(ge=0.0)

    @model_validator(mode="after")
    def validate_percentile_order(self) -> "LatencyMeasurement":
        if self.p95_ms < self.p50_ms:
            raise ValueError("Latency p95 cannot be lower than p50")
        return self


class TokenPricing(ContractModel):
    input_usd_per_million: float = Field(ge=0.0)
    output_usd_per_million: float = Field(ge=0.0)


class CostMeasurement(ContractModel):
    status: Literal["measured", "unavailable"]
    input_tokens: int | None = Field(default=None, ge=0)
    output_tokens: int | None = Field(default=None, ge=0)
    amount_usd: float | None = Field(default=None, ge=0.0)
    reason: str | None = None

    @model_validator(mode="after")
    def validate_availability(self) -> "CostMeasurement":
        measured_values = (self.input_tokens, self.output_tokens, self.amount_usd)
        if self.status == "measured":
            if any(value is None for value in measured_values) or self.reason is not None:
                raise ValueError("Measured cost requires usage and amount without a reason")
        elif any(value is not None for value in measured_values) or not self.reason:
            raise ValueError("Unavailable cost requires a reason and no measured values")
        return self


class EvaluationReport(ContractModel):
    dataset_id: str
    configuration_id: str
    execution_mode: ExecutionMode
    synthetic: bool
    case_count: int = Field(ge=1)
    case_kinds: tuple[EvaluationCaseKind, ...]
    classification_accuracy: RatioMeasurement
    safety_accuracy: RatioMeasurement
    grounding_accuracy: RatioMeasurement
    citation_validity: RatioMeasurement
    review_rate: RatioMeasurement
    review_recall: RatioMeasurement
    false_review_rate: RatioMeasurement
    review_reason_accuracy: RatioMeasurement
    abstention_frequency: RatioMeasurement
    unsupported_claim_rate: RatioMeasurement
    critical_policy_violations: RatioMeasurement
    latency: LatencyMeasurement
    cost: CostMeasurement


def load_evaluation_dataset(path: Path) -> EvaluationDataset:
    return EvaluationDataset.model_validate_json(path.read_text(encoding="utf-8"))


def _ratio(numerator: int, denominator: int) -> RatioMeasurement:
    rate = numerator / denominator if denominator else None
    return RatioMeasurement(numerator=numerator, denominator=denominator, rate=rate)


def _percentile(values: Sequence[float], percentile: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * percentile
    lower_index = int(position)
    upper_index = min(lower_index + 1, len(ordered) - 1)
    fraction = position - lower_index
    return ordered[lower_index] + (ordered[upper_index] - ordered[lower_index]) * fraction


def _classification_matches(case: EvaluationCase, result: AuditableProcessingResult) -> bool:
    expected = case.expected
    return (
        result.category == expected.category
        and result.urgency == expected.urgency
        and result.language == expected.language
        and result.sentiment == expected.sentiment
    )


def _cost_measurement(
    results: Sequence[AuditableProcessingResult],
    pricing: TokenPricing | None,
) -> CostMeasurement:
    if pricing is None:
        return CostMeasurement(status="unavailable", reason="pricing_not_supplied")
    if any(result.usage is None for result in results):
        return CostMeasurement(status="unavailable", reason="usage_unavailable")

    input_tokens = sum(result.usage.input_tokens for result in results if result.usage is not None)
    output_tokens = sum(
        result.usage.output_tokens for result in results if result.usage is not None
    )
    amount_usd = (
        input_tokens * pricing.input_usd_per_million
        + output_tokens * pricing.output_usd_per_million
    ) / 1_000_000
    return CostMeasurement(
        status="measured",
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        amount_usd=round(amount_usd, 12),
    )


def build_evaluation_report(
    dataset: EvaluationDataset,
    results: Sequence[AuditableProcessingResult],
    *,
    execution_mode: ExecutionMode,
    pricing: TokenPricing | None = None,
) -> EvaluationReport:
    if len(results) != len(dataset.cases):
        raise ValueError("One processing result is required for every evaluation case")
    if not results:
        raise ValueError("Evaluation results cannot be empty")

    pairs = tuple(zip(dataset.cases, results, strict=True))
    if any(case.ticket_id != result.ticket_id for case, result in pairs):
        raise ValueError("Evaluation results must preserve labeled ticket IDs and order")

    configuration_ids = {result.configuration_id for result in results}
    if len(configuration_ids) != 1:
        raise ValueError("Evaluation results must use one configuration ID")

    case_count = len(pairs)
    classification_matches = sum(
        _classification_matches(case, result) for case, result in pairs
    )
    safety_matches = sum(
        set(result.safety_flags) == set(case.expected.safety_flags) for case, result in pairs
    )
    grounding_matches = sum(
        result.answer_status == case.expected.answer_status for case, result in pairs
    )
    citation_matches = sum(
        tuple(citation.source_id for citation in result.citations)
        == case.expected.citation_source_ids
        for case, result in pairs
    )
    review_count = sum(result.human_review_required for result in results)
    expected_review_pairs = tuple(
        (case, result) for case, result in pairs if case.expected.human_review_required
    )
    expected_no_review_pairs = tuple(
        (case, result) for case, result in pairs if not case.expected.human_review_required
    )
    review_true_positives = sum(result.human_review_required for _, result in expected_review_pairs)
    false_reviews = sum(result.human_review_required for _, result in expected_no_review_pairs)
    review_reason_matches = sum(
        set(result.review_reasons) == set(case.expected.review_reasons)
        for case, result in pairs
    )
    abstention_count = sum(
        result.answer_status == AnswerStatus.ABSTAINED for result in results
    )
    drafted_results = tuple(
        result for result in results if result.answer_status == AnswerStatus.DRAFTED
    )
    unsupported_drafts = sum(not result.citations for result in drafted_results)
    safety_pairs = tuple(
        (case, result) for case, result in pairs if case.expected.safety_flags
    )
    critical_violations = sum(
        not set(case.expected.safety_flags).issubset(result.safety_flags)
        or not result.human_review_required
        for case, result in safety_pairs
    )
    latencies = tuple(result.latency_ms for result in results)

    return EvaluationReport(
        dataset_id=dataset.dataset_id,
        configuration_id=next(iter(configuration_ids)),
        execution_mode=execution_mode,
        synthetic=dataset.synthetic,
        case_count=case_count,
        case_kinds=tuple(sorted({case.kind for case in dataset.cases}, key=str)),
        classification_accuracy=_ratio(classification_matches, case_count),
        safety_accuracy=_ratio(safety_matches, case_count),
        grounding_accuracy=_ratio(grounding_matches, case_count),
        citation_validity=_ratio(citation_matches, case_count),
        review_rate=_ratio(review_count, case_count),
        review_recall=_ratio(review_true_positives, len(expected_review_pairs)),
        false_review_rate=_ratio(false_reviews, len(expected_no_review_pairs)),
        review_reason_accuracy=_ratio(review_reason_matches, case_count),
        abstention_frequency=_ratio(abstention_count, case_count),
        unsupported_claim_rate=_ratio(unsupported_drafts, len(drafted_results)),
        critical_policy_violations=_ratio(critical_violations, len(safety_pairs)),
        latency=LatencyMeasurement(
            sample_count=case_count,
            p50_ms=_percentile(latencies, 0.50),
            p95_ms=_percentile(latencies, 0.95),
        ),
        cost=_cost_measurement(results, pricing),
    )


def run_offline_evaluation(
    evaluation_set_path: Path,
    snapshot_path: Path,
    *,
    configuration_id: str = DEFAULT_CONFIGURATION_ID,
) -> EvaluationReport:
    dataset = load_evaluation_dataset(evaluation_set_path)
    results = tuple(
        process_offline_ticket(
            ticket_id=case.ticket_id,
            text=case.text,
            snapshot_path=snapshot_path,
            configuration_id=configuration_id,
        )
        for case in dataset.cases
    )
    return build_evaluation_report(
        dataset,
        results,
        execution_mode=ExecutionMode.OFFLINE_FIXTURE,
    )
