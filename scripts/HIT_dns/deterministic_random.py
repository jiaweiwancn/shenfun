"""Decomposition-independent Gaussian random numbers for MPI fields."""

from __future__ import annotations

import numpy as np


_GOLDEN = np.uint64(0x9E3779B97F4A7C15)
_MIX1 = np.uint64(0xBF58476D1CE4E5B9)
_MIX2 = np.uint64(0x94D049BB133111EB)
_STREAM = np.uint64(0xD2B74407B1CE6E93)
_COMPONENT = np.uint64(0xCA5A826395121157)
_TWO_NEG_53 = 1.0 / float(1 << 53)


def _splitmix64(values: np.ndarray) -> np.ndarray:
    """Return a vectorized SplitMix64 hash."""

    with np.errstate(over="ignore"):
        z = values + _GOLDEN
        z = (z ^ (z >> np.uint64(30))) * _MIX1
        z = (z ^ (z >> np.uint64(27))) * _MIX2
        return z ^ (z >> np.uint64(31))


def local_linear_indices(
    local_slice: tuple[slice, slice, slice], global_shape: tuple[int, int, int]
) -> np.ndarray:
    """Return global C-order linear indices for a local physical-space block."""

    axes = []
    for axis_slice, extent in zip(local_slice, global_shape):
        start = 0 if axis_slice.start is None else axis_slice.start
        stop = extent if axis_slice.stop is None else axis_slice.stop
        step = 1 if axis_slice.step is None else axis_slice.step
        axes.append(np.arange(start, stop, step, dtype=np.uint64))
    i, j, k = axes
    return (
        (i[:, None, None] * np.uint64(global_shape[1]) + j[None, :, None])
        * np.uint64(global_shape[2])
        + k[None, None, :]
    )


def gaussian_from_indices(
    linear_indices: np.ndarray, seed: int, component: int
) -> np.ndarray:
    """Generate one standard-normal value for each global index.

    The value is a pure function of ``(seed, component, global index)`` and is
    therefore independent of MPI rank count and pencil/slab decomposition.
    """

    if not 0 <= seed < (1 << 64):
        raise ValueError("seed must be in [0, 2**64)")
    if component < 0:
        raise ValueError("component must be nonnegative")
    with np.errstate(over="ignore"):
        key = (
            np.asarray(linear_indices, dtype=np.uint64)
            + np.uint64(seed)
            + np.uint64(component) * _COMPONENT
        )
        bits1 = _splitmix64(key)
        bits2 = _splitmix64(key + _STREAM)
    uniform1 = ((bits1 >> np.uint64(11)).astype(np.float64) + 0.5) * _TWO_NEG_53
    uniform2 = ((bits2 >> np.uint64(11)).astype(np.float64) + 0.5) * _TWO_NEG_53
    return np.sqrt(-2.0 * np.log(uniform1)) * np.cos(2.0 * np.pi * uniform2)


def gaussian_for_local_block(
    local_slice: tuple[slice, slice, slice],
    global_shape: tuple[int, int, int],
    seed: int,
    component: int,
) -> np.ndarray:
    """Generate a deterministic standard-normal local physical-space block."""

    indices = local_linear_indices(local_slice, global_shape)
    return gaussian_from_indices(indices, seed, component)
