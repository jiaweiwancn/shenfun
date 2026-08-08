from pathlib import Path
import sys

import numpy as np
import pytest


HIT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HIT_DIR))

from reference_data import finite_station_values, load_table3_e  # noqa: E402
from spectrum_model import create_initial_spectrum  # noqa: E402


@pytest.fixture(scope="module")
def spectrum():
    return create_initial_spectrum()


def test_measured_values_are_exact(spectrum):
    k, measured = finite_station_values(load_table3_e(), 42.0)
    assert np.allclose(spectrum(k), measured, rtol=5.0e-15, atol=0.0)


def test_infrared_completion_is_k4(spectrum):
    assert np.isclose(spectrum(0.0), 0.0)
    assert np.isclose(spectrum(0.1) / spectrum(0.05), 16.0)
    assert np.isclose(spectrum(0.2), 129.0)


def test_tail_is_positive_continuous_and_decaying(spectrum):
    assert np.isclose(spectrum(20.0), 0.8)
    assert np.isclose(spectrum(20.0 * (1.0 + 1.0e-10)), 0.8, rtol=1.0e-8)
    tail = spectrum(np.array([20.0, 25.0, 30.0, 40.0, 60.0]))
    assert np.all(tail > 0.0)
    assert np.all(np.diff(tail) < 0.0)
    assert spectrum.tail.beta > 0.0


def test_spectrum_moments_are_finite(spectrum):
    energy = spectrum.integral_energy()
    assert np.isfinite(energy) and energy > 0.0
    e11_zero = spectrum.longitudinal_spectrum(0.0)
    assert np.isfinite(e11_zero) and e11_zero > 0.0
    assert spectrum.longitudinal_spectrum(1.0) < e11_zero


def test_negative_wavenumbers_are_rejected(spectrum):
    with pytest.raises(ValueError):
        spectrum(-0.1)
