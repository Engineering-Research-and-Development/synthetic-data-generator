import pytest
import pandas as pd

from ai_lib.evaluate.TabularComparison import TabularComparisonEvaluator


@pytest.fixture()
def real_data():
    return pd.DataFrame(
        {"a": [1, 2, 3], "b": [4, 5, 6], "c": [7, 8, 9], "d": [10, 11, 12]}
    )


@pytest.fixture()
def synthetic_data():
    return pd.DataFrame(
        {"a": [1, 2, 3], "b": [4, 5, 6], "c": [7, 8, 9], "d": [10, 11, 12]}
    )


@pytest.fixture()
def evaluator_correct(real_data, synthetic_data):
    return TabularComparisonEvaluator(real_data, synthetic_data, ["a", "b"], ["c", "d"])


def test_init(evaluator_correct, real_data, synthetic_data):
    assert evaluator_correct._numerical_columns == ["a", "b"]
    assert evaluator_correct._categorical_columns == ["c", "d"]
    assert evaluator_correct._real_data.equals(real_data)
    assert evaluator_correct._synthetic_data.equals(synthetic_data)


def test_evaluate(evaluator_correct):
    report = evaluator_correct.compute()
    assert "statistical_metrics" in report
    assert "adherence_metrics" in report
    assert "novelty_metrics" in report


def test_evaluate_cramer_v_distance(evaluator_correct):
    cramer_v = evaluator_correct._evaluate_cramer_v_distance()
    print(cramer_v)
    assert 0 <= cramer_v <= 1


def test_evaluate_wasserstein_distance(evaluator_correct):
    wass_distance = evaluator_correct._evaluate_wasserstein_distance()
    assert 0 <= wass_distance <= 1


def test_evaluate_statistical_properties(evaluator_correct):
    report = evaluator_correct._evaluate_statistical_properties()
    assert "Total Statistical Compliance [%]" in report
    assert "Categorical Features Cramer's V [%]" in report
    assert "Numerical Features Wasserstein Distance [%]" in report


def test_evaluate_adherence(evaluator_correct):
    report = evaluator_correct._evaluate_adherence()
    assert "category_adherence_score [%]" in report
    assert "boundary_adherence_score [%]" in report
    assert len(report["category_adherence_score [%]"]) == len(
        evaluator_correct._categorical_columns
    )
    assert len(report["boundary_adherence_score [%]"]) == len(
        evaluator_correct._numerical_columns
    )


def test_evaluate_novelty(evaluator_correct):
    report = evaluator_correct._evaluate_novelty()
    assert "Unique Synthetic Data [%]" in report
    assert "New Synthetic Data [%]" in report
    assert 0 <= report["Unique Synthetic Data [%]"] <= 100
    assert 0 <= report["New Synthetic Data [%]"] <= 100
