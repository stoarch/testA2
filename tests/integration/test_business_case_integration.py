from pathlib import Path

from support_copilot.business_case import (
    Conclusion,
    generate_business_case,
    render_business_case_markdown,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_PATH = PROJECT_ROOT / "reports" / "business-case-input.json"


def test_three_configuration_business_case_preserves_evidence_gate() -> None:
    report = generate_business_case(INPUT_PATH)

    assert report.monthly_volume == 10_000
    assert {projection.configuration_id for projection in report.projections} == {
        "A",
        "B",
        "C",
    }
    assert len(report.projections) == 9
    assert all(projection.projection_kind == "estimate" for projection in report.projections)
    assert report.recommendation_configuration_id is None
    assert report.conclusion is Conclusion.NO_GO
    assert any("30" in reason for reason in report.decision_reasons)
    assert any("not measured" in reason for reason in report.decision_reasons)
    assert render_business_case_markdown(report) == (
        PROJECT_ROOT / "reports" / "business-case.md"
    ).read_text(encoding="utf-8")
