"""
Test Suite: Statistical Tests, Correlations, and Hypotheses
"""

import pytest
import pandas as pd
import numpy as np
from src.statistics import (
    compute_descriptive_stats, compute_correlation_matrices, run_hypothesis_tests
)

def test_descriptive_stats():
    df = pd.DataFrame({
        "lead_score": [50, 60, 70, 80, 90],
        "deal_value_inr": [100000.0, 200000.0, 300000.0, 400000.0, 500000.0]
    })
    desc = compute_descriptive_stats(df)
    assert len(desc) == 2
    score_row = desc[desc["Metric / Column"] == "lead_score"].iloc[0]
    assert score_row["Mean"] == 70.0
    assert score_row["Median"] == 70.0
    assert score_row["Min"] == 50.0
    assert score_row["Max"] == 90.0

def test_hypothesis_testing():
    # Synthetic group where converted leads have high scores and non-converted have low scores
    df = pd.DataFrame({
        "lead_score": [85, 90, 88, 92, 95, 30, 35, 40, 25, 32],
        "is_converted": [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
        "lead_quality": ["High", "High", "High", "High", "High", "Low", "Low", "Low", "Low", "Low"],
        "source_name": ["Website", "Website", "Social", "Social", "Referral", "Website", "Social", "Website", "Social", "Referral"]
    })
    tests = run_hypothesis_tests(df)
    assert len(tests) >= 2
    # The t-test should be statistically significant
    t_test = [t for t in tests if "t-test" in t["test_name"]][0]
    assert t_test["is_significant"] == True
    assert t_test["p_value"] < 0.05
