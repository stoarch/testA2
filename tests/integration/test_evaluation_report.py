from pathlib import Path

from support_copilot.evaluation import EvaluationCaseKind, run_offline_evaluation

PROJECT_ROOT = Path(__file__).resolve().parents[2]
EVALUATION_SET = (
    PROJECT_ROOT / "tests" / "fixtures" / "evaluation" / "synthetic_evaluation_set.json"
)
SNAPSHOT = PROJECT_ROOT / "tests" / "fixtures" / "kb" / "synthetic_snapshot.json"


def test_bounded_labeled_set_produces_a_reproducible_offline_report() -> None:
    report = run_offline_evaluation(EVALUATION_SET, SNAPSHOT)

    assert report.dataset_id == "evaluation-synthetic-001"
    assert report.execution_mode == "offline_fixture"
    assert report.case_count == 4
    assert set(report.case_kinds) == set(EvaluationCaseKind)
    assert report.classification_accuracy.denominator == 4
    assert report.safety_accuracy.denominator == 4
    assert report.grounding_accuracy.denominator == 4
    assert report.citation_validity.denominator == 4
    assert report.review_rate.denominator == 4
    assert report.latency.sample_count == 4
    assert report.cost.status == "unavailable"

