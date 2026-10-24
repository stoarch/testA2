from enum import StrEnum
from pathlib import Path
from typing import Literal

from pydantic import Field, model_validator

from support_copilot.contracts import ContractModel


class ConfigurationId(StrEnum):
    DETERMINISTIC = "A"
    GUARDED_LLM = "B"
    HYBRID = "C"


class Sensitivity(StrEnum):
    LOW = "low"
    BASE = "base"
    HIGH = "high"


class EvidenceStatus(StrEnum):
    MEASURED_OFFLINE_FIXTURE = "measured_offline_fixture"
    MEASURED_LIVE = "measured_live"
    NOT_MEASURED = "not_measured"


class Conclusion(StrEnum):
    GO = "go"
    CONDITIONAL_GO = "conditional_go"
    NO_GO = "no_go"


class ConfigurationEvidence(ContractModel):
    status: EvidenceStatus
    dataset_id: str | None = None
    case_count: int = Field(ge=0)
    grounding_rate: float | None = Field(default=None, ge=0.0, le=1.0)
    citation_rate: float | None = Field(default=None, ge=0.0, le=1.0)
    safety_rate: float | None = Field(default=None, ge=0.0, le=1.0)
    review_rate: float | None = Field(default=None, ge=0.0, le=1.0)
    critical_policy_violations: int | None = Field(default=None, ge=0)

    @model_validator(mode="after")
    def validate_measurement_state(self) -> "ConfigurationEvidence":
        measurements = (
            self.grounding_rate,
            self.citation_rate,
            self.safety_rate,
            self.review_rate,
            self.critical_policy_violations,
        )
        if self.status is EvidenceStatus.NOT_MEASURED:
            if self.dataset_id is not None or self.case_count != 0:
                raise ValueError("Unmeasured evidence cannot identify a dataset or cases")
            if any(value is not None for value in measurements):
                raise ValueError("Unmeasured evidence cannot contain measured values")
        elif self.dataset_id is None or self.case_count == 0 or any(
            value is None for value in measurements
        ):
            raise ValueError("Measured evidence requires a dataset, cases, and all quality values")
        return self


class OperatingScenarioAssumptions(ContractModel):
    sensitivity: Sensitivity
    eligible_share: float = Field(ge=0.0, le=1.0)
    draft_acceptance_rate: float = Field(ge=0.0, le=1.0)
    human_review_rate: float = Field(ge=0.0, le=1.0)
    baseline_aht_minutes: float = Field(gt=0.0)
    review_aht_minutes: float = Field(ge=0.0)
    model_cost_per_ticket: float = Field(ge=0.0)
    retrieval_cost_monthly: float = Field(ge=0.0)
    infrastructure_cost_monthly: float = Field(ge=0.0)
    maintenance_cost_monthly: float = Field(ge=0.0)

    @model_validator(mode="after")
    def validate_handling_times(self) -> "OperatingScenarioAssumptions":
        if self.review_aht_minutes > self.baseline_aht_minutes:
            raise ValueError("Assumed review AHT cannot exceed baseline AHT")
        return self


class ConfigurationPlan(ContractModel):
    configuration_id: ConfigurationId
    name: str = Field(min_length=1)
    evidence: ConfigurationEvidence
    scenarios: tuple[OperatingScenarioAssumptions, ...] = Field(min_length=3, max_length=3)

    @model_validator(mode="after")
    def validate_sensitivities(self) -> "ConfigurationPlan":
        sensitivities = [scenario.sensitivity for scenario in self.scenarios]
        if len(set(sensitivities)) != len(sensitivities):
            raise ValueError("Configuration sensitivities must be unique")
        if set(sensitivities) != set(Sensitivity):
            raise ValueError("Each configuration requires low, base, and high scenarios")
        return self


class BusinessCaseInput(ContractModel):
    report_id: str = Field(min_length=1)
    monthly_volume: int = Field(gt=0)
    currency: str = Field(min_length=3, max_length=3)
    loaded_hourly_cost: float = Field(gt=0.0)
    minimum_evaluation_cases: int = Field(gt=0)
    minimum_grounding_rate: float = Field(ge=0.0, le=1.0)
    minimum_citation_rate: float = Field(ge=0.0, le=1.0)
    configurations: tuple[ConfigurationPlan, ...] = Field(min_length=3, max_length=3)

    @model_validator(mode="after")
    def validate_configurations(self) -> "BusinessCaseInput":
        configuration_ids = [item.configuration_id for item in self.configurations]
        if len(set(configuration_ids)) != len(configuration_ids):
            raise ValueError("Business-case configuration IDs must be unique")
        if set(configuration_ids) != set(ConfigurationId):
            raise ValueError("Business case requires configurations A, B, and C")
        return self


class ScenarioProjection(ContractModel):
    configuration_id: ConfigurationId
    configuration_name: str
    sensitivity: Sensitivity
    projection_kind: Literal["estimate"] = "estimate"
    eligible_share: float
    draft_acceptance_rate: float
    human_review_rate: float
    baseline_aht_minutes: float
    review_aht_minutes: float
    model_cost_per_ticket: float
    eligible_tickets: float
    accepted_drafts: float
    review_tickets: float
    hours_saved: float
    review_workload_hours: float
    labor_value: float
    model_cost: float
    monthly_run_cost: float
    monthly_net_value: float
    cost_per_ticket: float
    break_even_accepted_drafts: float | None
    break_even_acceptance_rate: float | None


class BusinessCaseReport(ContractModel):
    report_id: str
    monthly_volume: int
    currency: str
    loaded_hourly_cost: float
    assumptions_are_estimates: Literal[True] = True
    configurations: tuple[ConfigurationPlan, ...]
    projections: tuple[ScenarioProjection, ...]
    recommendation_configuration_id: ConfigurationId | None
    conclusion: Conclusion
    decision_reasons: tuple[str, ...] = Field(min_length=1)


def load_business_case_input(path: Path) -> BusinessCaseInput:
    return BusinessCaseInput.model_validate_json(path.read_text(encoding="utf-8"))


def _rounded(value: float) -> float:
    return round(value, 6)


def calculate_scenario_projection(
    assumptions: OperatingScenarioAssumptions,
    *,
    monthly_volume: int,
    loaded_hourly_cost: float,
    configuration_id: ConfigurationId = ConfigurationId.DETERMINISTIC,
    configuration_name: str = "Test configuration",
) -> ScenarioProjection:
    eligible_tickets = monthly_volume * assumptions.eligible_share
    accepted_drafts = eligible_tickets * assumptions.draft_acceptance_rate
    review_tickets = monthly_volume * assumptions.human_review_rate
    minutes_saved_per_accepted_draft = (
        assumptions.baseline_aht_minutes - assumptions.review_aht_minutes
    )
    hours_saved = accepted_drafts * minutes_saved_per_accepted_draft / 60
    review_workload_hours = (
        review_tickets * assumptions.review_aht_minutes / 60
    )
    labor_value = hours_saved * loaded_hourly_cost
    model_cost = monthly_volume * assumptions.model_cost_per_ticket
    monthly_run_cost = (
        model_cost
        + assumptions.retrieval_cost_monthly
        + assumptions.infrastructure_cost_monthly
        + assumptions.maintenance_cost_monthly
    )
    monthly_net_value = labor_value - monthly_run_cost
    value_per_accepted_draft = minutes_saved_per_accepted_draft / 60 * loaded_hourly_cost
    break_even_accepted_drafts = (
        monthly_run_cost / value_per_accepted_draft if value_per_accepted_draft else None
    )
    break_even_acceptance_rate = (
        break_even_accepted_drafts / eligible_tickets
        if break_even_accepted_drafts is not None and eligible_tickets
        else None
    )

    return ScenarioProjection(
        configuration_id=configuration_id,
        configuration_name=configuration_name,
        sensitivity=assumptions.sensitivity,
        eligible_share=assumptions.eligible_share,
        draft_acceptance_rate=assumptions.draft_acceptance_rate,
        human_review_rate=assumptions.human_review_rate,
        baseline_aht_minutes=assumptions.baseline_aht_minutes,
        review_aht_minutes=assumptions.review_aht_minutes,
        model_cost_per_ticket=assumptions.model_cost_per_ticket,
        eligible_tickets=_rounded(eligible_tickets),
        accepted_drafts=_rounded(accepted_drafts),
        review_tickets=_rounded(review_tickets),
        hours_saved=_rounded(hours_saved),
        review_workload_hours=_rounded(review_workload_hours),
        labor_value=_rounded(labor_value),
        model_cost=_rounded(model_cost),
        monthly_run_cost=_rounded(monthly_run_cost),
        monthly_net_value=_rounded(monthly_net_value),
        cost_per_ticket=_rounded(monthly_run_cost / monthly_volume),
        break_even_accepted_drafts=(
            _rounded(break_even_accepted_drafts)
            if break_even_accepted_drafts is not None
            else None
        ),
        break_even_acceptance_rate=(
            _rounded(break_even_acceptance_rate)
            if break_even_acceptance_rate is not None
            else None
        ),
    )


def _evidence_failures(
    business_input: BusinessCaseInput,
    configuration: ConfigurationPlan,
) -> tuple[str, ...]:
    evidence = configuration.evidence
    prefix = f"Configuration {configuration.configuration_id.value}"
    if evidence.status is EvidenceStatus.NOT_MEASURED:
        return (f"{prefix}: quality and safety results are not measured.",)

    failures: list[str] = []
    if evidence.case_count < business_input.minimum_evaluation_cases:
        failures.append(
            f"{prefix}: measured set has {evidence.case_count} cases; "
            f"at least {business_input.minimum_evaluation_cases} are required."
        )
    if evidence.critical_policy_violations != 0:
        failures.append(f"{prefix}: critical policy violations are not zero.")
    if evidence.safety_rate != 1.0:
        failures.append(f"{prefix}: hard safety acceptance is below 100%.")
    if evidence.grounding_rate is None or (
        evidence.grounding_rate < business_input.minimum_grounding_rate
    ):
        failures.append(f"{prefix}: grounding quality is below the required threshold.")
    if evidence.citation_rate is None or (
        evidence.citation_rate < business_input.minimum_citation_rate
    ):
        failures.append(f"{prefix}: citation quality is below the required threshold.")
    return tuple(failures)


def build_business_case(business_input: BusinessCaseInput) -> BusinessCaseReport:
    projections = tuple(
        calculate_scenario_projection(
            scenario,
            monthly_volume=business_input.monthly_volume,
            loaded_hourly_cost=business_input.loaded_hourly_cost,
            configuration_id=configuration.configuration_id,
            configuration_name=configuration.name,
        )
        for configuration in business_input.configurations
        for scenario in configuration.scenarios
    )
    failures_by_configuration = {
        configuration.configuration_id: _evidence_failures(business_input, configuration)
        for configuration in business_input.configurations
    }
    qualified_ids = {
        configuration_id
        for configuration_id, failures in failures_by_configuration.items()
        if not failures
    }
    positive_base_projections = tuple(
        projection
        for projection in projections
        if projection.configuration_id in qualified_ids
        and projection.sensitivity is Sensitivity.BASE
        and projection.monthly_net_value > 0
    )

    if positive_base_projections:
        recommended = max(
            positive_base_projections,
            key=lambda projection: projection.monthly_net_value,
        )
        recommendation_configuration_id = recommended.configuration_id
        conclusion = Conclusion.CONDITIONAL_GO
        decision_reasons = (
            f"Configuration {recommended.configuration_id.value} passes the evidence gates "
            "and has the highest positive base-case net value.",
            "Financial outputs remain modeled estimates until operating assumptions are measured.",
        )
    else:
        recommendation_configuration_id = None
        conclusion = Conclusion.NO_GO
        decision_reasons = tuple(
            reason
            for configuration in business_input.configurations
            for reason in failures_by_configuration[configuration.configuration_id]
        ) or ("No evidence-qualified configuration has positive base-case net value.",)

    return BusinessCaseReport(
        report_id=business_input.report_id,
        monthly_volume=business_input.monthly_volume,
        currency=business_input.currency,
        loaded_hourly_cost=business_input.loaded_hourly_cost,
        assumptions_are_estimates=True,
        configurations=business_input.configurations,
        projections=projections,
        recommendation_configuration_id=recommendation_configuration_id,
        conclusion=conclusion,
        decision_reasons=decision_reasons,
    )


def generate_business_case(path: Path) -> BusinessCaseReport:
    return build_business_case(load_business_case_input(path))


def _money(value: float, currency: str) -> str:
    return f"{currency} {value:,.2f}"


def render_business_case_markdown(report: BusinessCaseReport) -> str:
    base_projections = tuple(
        projection
        for projection in report.projections
        if projection.sensitivity is Sensitivity.BASE
    )
    recommendation = (
        f"Conditional go for configuration {report.recommendation_configuration_id.value}."
        if report.recommendation_configuration_id is not None
        else "No configuration is justified for deployment yet."
    )
    lines = [
        "# Valetax Support Co-Pilot Business Case",
        "",
        f"- Status: {report.conclusion.value.replace('_', '-')}",
        f"- Planning volume: {report.monthly_volume:,} tickets/month",
        "- Evidence rule: financial outputs are modeled estimates, not measured savings",
        "",
        "## Recommendation",
        "",
        f"**{recommendation}**",
        "",
        *[f"- {reason}" for reason in report.decision_reasons],
        "",
        "## Base-case comparison",
        "",
        (
            "| Configuration | Evidence | Accepted drafts | Review hours | Labor value "
            "| Run cost | Net value | Cost/ticket | Break-even acceptance |"
        ),
        "|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    configuration_by_id = {
        configuration.configuration_id: configuration
        for configuration in report.configurations
    }
    for projection in base_projections:
        evidence = configuration_by_id[projection.configuration_id].evidence
        break_even = (
            f"{projection.break_even_acceptance_rate:.1%}"
            if projection.break_even_acceptance_rate is not None
            else "N/A"
        )
        lines.append(
            f"| {projection.configuration_id.value} - {projection.configuration_name} "
            f"| {evidence.status.value.replace('_', ' ')} | {projection.accepted_drafts:,.0f} "
            f"| {projection.review_workload_hours:,.1f} "
            f"| {_money(projection.labor_value, report.currency)} "
            f"| {_money(projection.monthly_run_cost, report.currency)} "
            f"| {_money(projection.monthly_net_value, report.currency)} "
            f"| {_money(projection.cost_per_ticket, report.currency)} "
            f"| {break_even} |"
        )

    lines.extend(
        [
            "",
            "## Low/base/high sensitivity",
            "",
            (
                "| Config | Case | Eligible | Acceptance | Review rate | Hours saved "
                "| Monthly cost | Monthly net value |"
            ),
            "|---|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for projection in report.projections:
        lines.append(
            f"| {projection.configuration_id.value} | {projection.sensitivity.value} "
            f"| {projection.eligible_share:.0%} | {projection.draft_acceptance_rate:.0%} "
            f"| {projection.human_review_rate:.0%} | {projection.hours_saved:,.1f} "
            f"| {_money(projection.monthly_run_cost, report.currency)} "
            f"| {_money(projection.monthly_net_value, report.currency)} |"
        )

    lines.extend(
        [
            "",
            "## Evidence and assumptions",
            "",
            (
                "Loaded labor cost is assumed at "
                f"{_money(report.loaded_hourly_cost, report.currency)}/hour. "
                "Configuration A has only a four-case offline synthetic measurement; "
                "B and C are unmeasured. Eligibility, acceptance, handling time, provider cost, "
                "infrastructure, and maintenance values are explicit sensitivity assumptions. "
                "Review workload is disclosed separately and the handling-time delta already "
                "reflects review effort, so it is not double-counted as another run cost."
            ),
            "",
            (
                "Phase 2 requires the 30+ case evaluation, measured operating handling times, "
                "provider pricing/usage, security and privacy approval, live KB ownership, and "
                "peak-capacity validation before deployment."
            ),
            "",
        ]
    )
    return "\n".join(lines)
