from pathlib import Path
import sys

import numpy as np


HIT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HIT_DIR))

from deterministic_random import gaussian_for_local_block  # noqa: E402


def test_partition_independence():
    shape = (12, 10, 8)
    whole = gaussian_for_local_block(
        (slice(0, 12), slice(0, 10), slice(0, 8)), shape, seed=421971, component=1
    )
    pieces = [
        gaussian_for_local_block(
            (slice(start, stop), slice(0, 10), slice(0, 8)),
            shape,
            seed=421971,
            component=1,
        )
        for start, stop in ((0, 3), (3, 7), (7, 12))
    ]
    assert np.array_equal(whole, np.concatenate(pieces, axis=0))


def test_seed_and_component_select_independent_streams():
    local_slice = (slice(0, 8), slice(0, 8), slice(0, 8))
    shape = (8, 8, 8)
    baseline = gaussian_for_local_block(local_slice, shape, 1234, 0)
    assert not np.array_equal(baseline, gaussian_for_local_block(local_slice, shape, 1235, 0))
    assert not np.array_equal(baseline, gaussian_for_local_block(local_slice, shape, 1234, 1))


def test_large_sample_has_standard_normal_moments():
    shape = (64, 64, 32)
    values = gaussian_for_local_block(
        (slice(0, 64), slice(0, 64), slice(0, 32)), shape, 987654321, 2
    )
    assert abs(float(values.mean())) < 0.01
    assert abs(float(values.var()) - 1.0) < 0.02
