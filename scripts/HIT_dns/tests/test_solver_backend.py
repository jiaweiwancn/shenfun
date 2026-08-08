from pathlib import Path
import sys

import numpy as np
import pytest


HIT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HIT_DIR))

from solver_backend import DNSParameters  # noqa: E402


def test_approved_baseline_geometry():
    settings = DNSParameters()
    settings.validate()
    assert settings.shape == (384, 384, 384)
    assert np.isclose(settings.length_cm, 10.0 * np.pi)
    assert np.isclose(settings.delta_k_cm1, 0.2)


def test_invalid_mesh_is_rejected():
    with pytest.raises(ValueError):
        DNSParameters(n=63).validate()
