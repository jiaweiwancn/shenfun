from pathlib import Path
import sys

import numpy as np


HIT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HIT_DIR))

from compare_results import (  # noqa: E402
    BULK_MAPPINGS,
    comparison_metrics,
    positive_log_interpolate,
    write_point_rows,
)
from reference_data import load_table4_bulk  # noqa: E402


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


def test_bulk_comparison_fields_match_reference_table_schema():
    table_fields = set(load_table4_bulk().dtype.names)
    assert {experiment_name for _, _, experiment_name in BULK_MAPPINGS} <= table_fields


def test_comparison_csv_uses_lf_line_endings(tmp_path):
    output = tmp_path / "comparison.csv"
    write_point_rows(output, [{"station": 42, "value": 1.0}])
    assert output.read_bytes() == b"station,value\n42,1.0\n"
