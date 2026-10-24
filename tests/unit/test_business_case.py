from support_copilot.business_case import (
    OperatingScenarioAssumptions,
    Sensitivity,
    calculate_scenario_projection,
)


def test_projection_calculates_value_cost_review_workload_and_break_even() -> None:
    assumptions = OperatingScenarioAssumptions(
        sensitivity=Sensitivity.BASE,
        eligible_share=0.50,
        draft_acceptance_rate=0.60,
        human_review_rate=0.40,
        baseline_aht_minutes=10.0,
        review_aht_minutes=4.0,
        model_cost_per_ticket=0.02,
        retrieval_cost_monthly=100.0,
        infrastructure_cost_monthly=200.0,
        maintenance_cost_monthly=700.0,
    )

    projection = calculate_scenario_projection(
        assumptions,
        monthly_volume=10_000,
        loaded_hourly_cost=30.0,
    )

    assert projection.eligible_tickets == 5_000
    assert projection.accepted_drafts == 3_000
    assert projection.review_tickets == 4_000
    assert projection.hours_saved == 300.0
    assert round(projection.review_workload_hours, 2) == 266.67
    assert projection.labor_value == 9_000.0
    assert projection.monthly_run_cost == 1_200.0
    assert projection.monthly_net_value == 7_800.0
    assert projection.cost_per_ticket == 0.12
    assert projection.break_even_accepted_drafts == 400.0
    assert projection.break_even_acceptance_rate == 0.08


def test_projection_rejects_review_time_above_baseline_time() -> None:
    try:
        OperatingScenarioAssumptions(
            sensitivity=Sensitivity.LOW,
            eligible_share=0.50,
            draft_acceptance_rate=0.50,
            human_review_rate=0.50,
            baseline_aht_minutes=4.0,
            review_aht_minutes=5.0,
            model_cost_per_ticket=0.0,
            retrieval_cost_monthly=0.0,
            infrastructure_cost_monthly=0.0,
            maintenance_cost_monthly=0.0,
        )
    except ValueError as error:
        assert "review AHT" in str(error)
    else:
        raise AssertionError("Expected invalid handling-time assumptions to fail")

