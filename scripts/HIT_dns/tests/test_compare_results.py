from pathlib import Path
import sys

import numpy as np


HIT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HIT_DIR))

from compare_results import comparison_metrics, positive_log_interpolate  # noqa: E402


def test_positive_log_interpolation_exact_for_power_law():
    source_k = np.array([1.0, 2.0, 4.0, 8.0])
    source_value = source_k ** (-5.0 / 3.0)
    target = np.array([0.5, 1.0, 3.0, 8.0, 9.0])
    result = positive_log_interpolate(source_k, source_value, target)
    assert np.isnan(result[0]) and np.isnan(result[-1])
    assert np.allclose(result[1:-1], target[1:-1] ** (-5.0 / 3.0))


def test_comparison_metrics_identity():
    values = np.array([1.0, 2.0, 4.0])
    metrics = comparison_metrics(values, values)
    assert metrics["point_count"] == 3
    assert metrics["relative_l2"] == 0.0
    assert metrics["log10_rmse"] == 0.0
    assert metrics["median_ratio_dns_over_experiment"] == 1.0
    assert metrics["maximum_factor_error"] == 1.0
