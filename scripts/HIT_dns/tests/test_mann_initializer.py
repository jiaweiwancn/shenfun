from pathlib import Path
import sys

import numpy as np


HIT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HIT_DIR))

from mann_initializer import apply_mann_factor  # noqa: E402
from spectrum_model import create_initial_spectrum  # noqa: E402


def test_mann_factor_is_divergence_free_and_zero_mean():
    rng = np.random.default_rng(123)
    shape = (7, 5, 4)
    axes = [
        np.arange(-3, 4)[:, None, None],
        np.arange(-2, 3)[None, :, None],
        np.arange(0, 4)[None, None, :],
    ]
    k_squared = sum(axis * axis for axis in axes)
    white_hat = rng.normal(size=(3, *shape)) + 1j * rng.normal(size=(3, *shape))
    velocity_hat = apply_mann_factor(
        white_hat,
        axes,
        k_squared,
        create_initial_spectrum(),
        spectral_cell_volume=0.008,
        physical_point_count=128,
    )
    divergence = sum(axis * velocity_hat[i] for i, axis in enumerate(axes))
    assert np.max(np.abs(divergence)) < 5.0e-14
    assert np.array_equal(velocity_hat[:, 3, 2, 0], np.zeros(3, dtype=complex))
    assert np.all(np.isfinite(velocity_hat))
