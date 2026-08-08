from pathlib import Path
import sys

import numpy as np


HIT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HIT_DIR))

from reference_data import (  # noqa: E402
    M_CM,
    NU_CM2_S,
    U0_CM_S,
    finite_station_values,
    load_table2_e11,
    load_table3_e,
    load_table4_bulk,
    station_to_elapsed_seconds,
)


def test_dimensional_mapping():
    assert np.isclose(M_CM, 5.08)
    assert np.isclose(U0_CM_S, 1000.0)
    assert np.isclose(NU_CM2_S, 0.14941176470588236)
    assert np.isclose(station_to_elapsed_seconds(42), 0.0)
    assert np.isclose(station_to_elapsed_seconds(98), 0.28448)
    assert np.isclose(station_to_elapsed_seconds(171), 0.65532)


def test_table2_transcription_sentinels():
    table = load_table2_e11()
    assert table.k.size == 23
    assert np.isclose(table.by_station[42][0], 570.0)
    assert np.isnan(table.by_station[98][0])
    assert np.isclose(table.by_station[171][1], 181.0)
    assert np.isclose(table.by_station[42][-2], 0.0371)
    assert np.isclose(table.by_station[98][-1], 0.000298)
    assert np.isclose(table.by_station[171][-1], 0.0000217)


def test_table3_transcription_sentinels():
    table = load_table3_e()
    assert table.k.size == 20
    assert np.isnan(table.by_station[42][0])
    assert np.isclose(table.by_station[171][0], 49.7)
    assert np.isclose(table.by_station[42][5], 457.0)
    assert np.isclose(table.by_station[98][-1], 0.0330)
    assert np.isnan(table.by_station[171][-1])


def test_table4_bulk_consistency():
    bulk = load_table4_bulk()
    assert np.array_equal(bulk["station_tU0_over_M"], [42.0, 98.0, 171.0])
    assert np.allclose(bulk["R_lambda"], [71.6, 65.3, 60.7])
    inferred_nu = (bulk["eta_cm"] ** 4 * bulk["epsilon_cm2_s3"]) ** (1.0 / 3.0)
    assert np.allclose(inferred_nu, NU_CM2_S, rtol=0.004)
    assert np.allclose(1.0 / bulk["eta_cm"], [34.0, 21.0, 15.0], rtol=0.03)


def test_finite_station_values_removes_missing_cells():
    k, spectrum = finite_station_values(load_table3_e(), 42)
    assert np.isclose(k[0], 0.20)
    assert np.isclose(spectrum[0], 129.0)
    assert k.size == spectrum.size == 19
