#!/usr/bin/env python
"""Shared utilities for MKM channel-flow resolvent calculations."""

from __future__ import annotations

import contextlib
from pathlib import Path
from typing import Any

import h5py
import numpy as np


COMPONENT_NAMES = ("streamwise", "spanwise", "wallnormal")


def _decode_attr(value: Any) -> Any:
    if isinstance(value, bytes):
        return value.decode("utf-8")
    if isinstance(value, np.bytes_):
        return value.astype(str).item()
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, np.ndarray) and value.dtype.kind == "S":
        return np.array([item.decode("utf-8") for item in value])
    return value


def _attrs_to_dict(attrs: h5py.AttributeManager) -> dict[str, Any]:
    return {key: _decode_attr(value) for key, value in attrs.items()}


def _split_csv_attr(value: Any, default: tuple[str, ...]) -> tuple[str, ...]:
    value = _decode_attr(value)
    if value is None:
        return default
    if isinstance(value, str):
        parts = tuple(part.strip() for part in value.split(",") if part.strip())
        return parts or default
    return tuple(str(part) for part in value)


def _open_h5_read(source: str | Path | h5py.File | h5py.Group):
    if isinstance(source, (str, Path)):
        return h5py.File(Path(source).expanduser(), "r")
    return contextlib.nullcontext(source)


def _read_first_dataset(group: h5py.File | h5py.Group, paths: tuple[str, ...]) -> np.ndarray | None:
    for path in paths:
        if path in group:
            return group[path][:]
    return None


def _first_float(attrs: dict[str, Any], keys: tuple[str, ...]) -> float:
    for key in keys:
        if key in attrs:
            try:
                return float(attrs[key])
            except (TypeError, ValueError):
                pass
    return float("nan")


def load_target_metadata(target_h5: str | Path | h5py.File | h5py.Group) -> dict[str, Any]:
    """Load grid, mean-flow, wavenumber, Reynolds, and sampling metadata.

    The returned ``mean_profile`` keeps the target-file convention:
    ``(Nz, 3)`` in level-major component order
    ``[streamwise, spanwise, wallnormal]``.
    """

    with _open_h5_read(target_h5) as f:
        attrs = _attrs_to_dict(f.attrs)
        if "mean_profile" not in f:
            raise KeyError("target file is missing mean_profile")

        mean_profile = f["mean_profile"][:]
        if mean_profile.ndim != 2 or mean_profile.shape[1] != 3:
            raise ValueError(f"expected mean_profile shape (Nz, 3), got {mean_profile.shape}")

        mean_attrs = _attrs_to_dict(f["mean_profile"].attrs)
        component_names = _split_csv_attr(
            mean_attrs.get("columns", attrs.get("component_names")),
            COMPONENT_NAMES,
        )

        z_wall = _read_first_dataset(f, ("geometry/z_wall", "grid/z_wall"))
        if z_wall is None:
            raise KeyError("target file is missing geometry/z_wall")

        sampling: dict[str, Any] = {}
        if "sampling/t" in f:
            sampling["t"] = f["sampling/t"][:]
        for key in (
            "dt",
            "snapshot_keys",
            "sampling_stage_label",
            "selection_t_min",
            "selection_t_max",
            "selection_skip_snapshots",
            "selection_snapshot_stride",
            "selection_max_snapshots",
        ):
            if key in attrs:
                sampling[key] = attrs[key]

        metadata = {
            "z_wall": z_wall,
            "k_stream": _read_first_dataset(f, ("geometry/k_stream", "wavenumbers/k_stream")),
            "k_span": _read_first_dataset(f, ("geometry/k_span", "wavenumbers/k_span")),
            "x_stream": _read_first_dataset(f, ("geometry/x_stream", "grid/x_stream")),
            "x_span": _read_first_dataset(f, ("geometry/x_span", "grid/x_span")),
            "mean_profile": mean_profile,
            "U": mean_profile[:, 0],
            "Re_tau": _first_float(
                attrs,
                (
                    "Re_tau",
                    "re_tau",
                    "friction_Reynolds_number",
                    "Reynolds_number",
                    "Re",
                    "re",
                ),
            ),
            "component_names": component_names,
            "component_order_level_major": attrs.get(
                "component_order_level_major",
                "[streamwise, spanwise, wallnormal]",
            ),
            "sampling": sampling,
            "attrs": attrs,
        }
    return metadata


def load_constraint_operators(constraint_h5: str | Path | h5py.File | h5py.Group) -> dict[str, Any]:
    """Load saved channel constraint operators and wavenumber arrays."""

    with _open_h5_read(constraint_h5) as f:
        attrs = _attrs_to_dict(f.attrs)
        operators = {
            "z_wall": _read_first_dataset(f, ("grid/z_wall", "geometry/z_wall")),
            "k_stream": _read_first_dataset(f, ("wavenumbers/k_stream", "geometry/k_stream")),
            "k_span": _read_first_dataset(f, ("wavenumbers/k_span", "geometry/k_span")),
            "D_wall": f["operators/D_wall"][:],
            "B_boundary": f["operators/B_boundary"][:],
            "E_stream": f["operators/E_stream"][:],
            "E_span": f["operators/E_span"][:],
            "E_wall": f["operators/E_wall"][:],
            "attrs": attrs,
            "svd_rtol": float(attrs.get("svd_relative_tolerance", 1e-12)),
        }
        if operators["z_wall"] is None:
            raise KeyError("constraint file is missing grid/z_wall")
        if operators["k_stream"] is None or operators["k_span"] is None:
            raise KeyError("constraint file is missing saved wavenumber arrays")
        if "mode_audit/rank" in f:
            operators["rank_audit"] = f["mode_audit/rank"][:]
        if "mode_audit/nullity" in f:
            operators["nullity_audit"] = f["mode_audit/nullity"][:]

    operators["G_boundary"] = boundary_constraint_operator(
        operators["B_boundary"],
        operators["E_stream"],
        operators["E_span"],
        operators["E_wall"],
    )
    return operators


def boundary_constraint_operator(
    B_boundary: np.ndarray,
    E_stream: np.ndarray,
    E_span: np.ndarray,
    E_wall: np.ndarray,
) -> np.ndarray:
    """Return stacked no-slip rows in level-major component ordering."""

    return np.vstack((
        B_boundary @ E_stream,
        B_boundary @ E_span,
        B_boundary @ E_wall,
    )).astype(complex)


def raw_constraint_operator(operators: dict[str, Any], kappa: float, lambda_: float) -> np.ndarray:
    """Build the uncompressed divergence/no-slip constraint matrix."""

    D_wall = operators["D_wall"]
    E_stream = operators["E_stream"]
    E_span = operators["E_span"]
    E_wall = operators["E_wall"]
    Gdiv = 1j * kappa * E_stream + 1j * lambda_ * E_span + D_wall @ E_wall
    G_boundary = operators.get("G_boundary")
    if G_boundary is None:
        G_boundary = boundary_constraint_operator(
            operators["B_boundary"],
            E_stream,
            E_span,
            E_wall,
        )
    return np.vstack((Gdiv, G_boundary))


def rebuild_gtilde_and_nullspace(
    operators: dict[str, Any],
    kappa: float,
    lambda_: float,
    rtol: float = 1e-12,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, int]:
    """Rebuild ``Gtilde`` and ``Nmat`` using the constraint-builder SVD convention.

    This mirrors ``build_mkm_constraints.compress_constraint``:
    ``Gtilde = Vh[:rank, :]`` and ``Nmat = Vh[rank:, :].conj().T`` from
    ``np.linalg.svd(Graw, full_matrices=True)``.
    """

    Graw = raw_constraint_operator(operators, kappa, lambda_)
    _, singular_values, Vh = np.linalg.svd(Graw, full_matrices=True)
    if singular_values.size == 0 or singular_values[0] == 0.0:
        rank = 0
    else:
        rank = int(np.sum(singular_values > rtol * singular_values[0]))
    Gtilde = Vh[:rank, :]
    Nmat = Vh[rank:, :].conj().T
    return singular_values, Gtilde, Nmat, rank


def chebyshev_gauss_physical_weights(
    z: np.ndarray,
    *,
    check_nodes: bool = True,
    atol: float = 1e-10,
) -> np.ndarray:
    """Return Fejer first-rule weights for Chebyshev-Gauss nodes on ``[-1, 1]``.

    The weights approximate the physical integral ``int_{-1}^1 f(z) dz`` and
    are returned in the same order as ``z``. They do not include the kinetic
    energy factor ``1/2``.
    """

    z = np.asarray(z, dtype=float)
    if z.ndim != 1:
        raise ValueError("z must be one-dimensional")
    n = z.size
    if n == 0:
        raise ValueError("z must contain at least one node")

    theta = np.pi * (2 * np.arange(n) + 1) / (2 * n)
    canonical_nodes = np.cos(theta)
    canonical_weights = np.full(n, 2.0 / n, dtype=float)
    for m in range(1, (n - 1) // 2 + 1):
        canonical_weights -= (4.0 / n) * np.cos(2 * m * theta) / (4 * m * m - 1)

    input_order = np.argsort(z)
    canonical_order = np.argsort(canonical_nodes)
    if check_nodes and not np.allclose(
        z[input_order],
        canonical_nodes[canonical_order],
        rtol=0.0,
        atol=atol,
    ):
        raise ValueError("z does not match Chebyshev-Gauss nodes on [-1, 1]")

    weights = np.empty_like(canonical_weights)
    weights[input_order] = canonical_weights[canonical_order]
    return weights


def velocity_energy_weight(weights_z: np.ndarray, *, as_matrix: bool = True) -> np.ndarray:
    """Expand wall-normal weights to the level-major velocity vector."""

    weights_z = np.asarray(weights_z, dtype=float)
    if weights_z.ndim != 1:
        raise ValueError("weights_z must be one-dimensional")
    expanded = np.repeat(weights_z, 3)
    if as_matrix:
        return np.diag(expanded)
    return expanded


def _apply_weight(Wq: np.ndarray, X: np.ndarray) -> np.ndarray:
    Wq = np.asarray(Wq)
    if Wq.ndim == 1:
        return Wq[:, None] * X
    if Wq.ndim == 2:
        return Wq @ X
    raise ValueError("Wq must be a one-dimensional diagonal or a two-dimensional matrix")


def energy_orthonormal_basis(
    Nmat: np.ndarray,
    Wq: np.ndarray,
    *,
    rtol: float = 1e-12,
) -> np.ndarray:
    """Return an admissible basis ``Q`` satisfying ``Q.conj().T @ Wq @ Q = I``."""

    Nmat = np.asarray(Nmat, dtype=complex)
    if Nmat.ndim != 2:
        raise ValueError("Nmat must be two-dimensional")
    if Nmat.shape[1] == 0:
        return np.zeros_like(Nmat)

    WN = _apply_weight(Wq, Nmat)
    M = Nmat.conj().T @ WN
    M = 0.5 * (M + M.conj().T)
    evals, evecs = np.linalg.eigh(M)
    scale = max(float(np.max(np.abs(evals))), 1.0)
    if np.any(evals < -rtol * scale):
        raise ValueError("Nmat^* Wq Nmat is not positive semidefinite")
    keep = evals > rtol * scale
    if not np.any(keep):
        raise ValueError("no positive energy directions were found")
    if not np.all(keep):
        evals = evals[keep]
        evecs = evecs[:, keep]
    return Nmat @ (evecs / np.sqrt(evals)[None, :])


def compute_uprime(U: np.ndarray, D_wall: np.ndarray) -> np.ndarray:
    """Compute the wall-normal mean shear ``Uprime = D_wall @ U``."""

    U = np.asarray(U)
    D_wall = np.asarray(D_wall)
    if D_wall.ndim != 2 or D_wall.shape[1] != U.shape[0]:
        raise ValueError("D_wall shape is incompatible with U")
    return D_wall @ U


def build_linearized_velocity_operator(
    U: np.ndarray,
    Uprime: np.ndarray,
    D1: np.ndarray,
    Re_tau: float,
    kappa: float,
    lambda_: float,
) -> np.ndarray:
    """Build the raw velocity operator in level-major component ordering.

    The convention is ``qhat exp(i*kappa*x + i*lambda*y - i*omega*t)`` and
    ``L q = -i*kappa*U q - u_z*Uprime*e_x + Re_tau^{-1}(D2-k^2 I)q``.
    """

    U = np.asarray(U, dtype=float)
    Uprime = np.asarray(Uprime, dtype=float)
    D1 = np.asarray(D1, dtype=float)
    if U.ndim != 1 or Uprime.shape != U.shape:
        raise ValueError("U and Uprime must be one-dimensional arrays with the same shape")
    nz = U.size
    if D1.shape != (nz, nz):
        raise ValueError("D1 must have shape (Nz, Nz)")
    if Re_tau == 0.0:
        raise ValueError("Re_tau must be nonzero")

    D2 = D1 @ D1
    k2 = kappa * kappa + lambda_ * lambda_
    scalar_viscous = (D2 - k2 * np.eye(nz)) / Re_tau
    L = np.zeros((3 * nz, 3 * nz), dtype=complex)
    for a in range(nz):
        for b in range(nz):
            for component in range(3):
                L[3 * a + component, 3 * b + component] += scalar_viscous[a, b]
        for component in range(3):
            L[3 * a + component, 3 * a + component] += -1j * kappa * U[a]
        L[3 * a, 3 * a + 2] += -Uprime[a]
    return L


def modal_energy_density(q: np.ndarray, weights_z: np.ndarray) -> dict[str, np.ndarray | float]:
    """Return pointwise and integrated modal energy diagnostics.

    ``q`` may be a single vector with shape ``(3*Nz,)`` or a mode matrix with
    shape ``(3*Nz, n_modes)``. The returned densities are unweighted
    ``|u_i(z)|^2`` values; integrated energies use ``weights_z`` and omit the
    kinetic-energy factor ``1/2``.
    """

    q = np.asarray(q)
    weights_z = np.asarray(weights_z, dtype=float)
    if weights_z.ndim != 1:
        raise ValueError("weights_z must be one-dimensional")
    nz = weights_z.size
    if q.shape[0] != 3 * nz:
        raise ValueError("q leading dimension must be 3*Nz")

    if q.ndim == 1:
        component_density = np.abs(q.reshape(nz, 3)) ** 2
        total_density = np.sum(component_density, axis=1)
        component_energy = np.sum(weights_z[:, None] * component_density, axis=0)
        total_energy = float(np.sum(weights_z * total_density))
    elif q.ndim == 2:
        component_density = np.abs(q.reshape(nz, 3, q.shape[1])) ** 2
        total_density = np.sum(component_density, axis=1)
        component_energy = np.sum(weights_z[:, None, None] * component_density, axis=0)
        total_energy = np.sum(weights_z[:, None] * total_density, axis=0)
    else:
        raise ValueError("q must be one- or two-dimensional")

    return {
        "component_density": component_density,
        "total_density": total_density,
        "component_energy": component_energy,
        "total_energy": total_energy,
    }


def critical_layer_locations(
    z: np.ndarray,
    U: np.ndarray,
    kappa: float,
    omega: float,
    *,
    atol: float = 1e-12,
) -> np.ndarray:
    """Return linearly interpolated locations where ``U(z) = omega/kappa``.

    For ``kappa = 0`` there is no finite phase speed, so the function returns
    an empty array.
    """

    if abs(kappa) <= atol:
        return np.array([], dtype=float)

    phase_speed = omega / kappa
    if abs(np.imag(phase_speed)) > atol:
        raise ValueError("critical-layer phase speed must be real")
    c = float(np.real(phase_speed))

    z = np.asarray(z, dtype=float)
    U = np.asarray(U, dtype=float)
    if z.shape != U.shape or z.ndim != 1:
        raise ValueError("z and U must be one-dimensional arrays with the same shape")
    if z.size < 2:
        return np.array([], dtype=float)

    order = np.argsort(z)
    zz = z[order]
    values = U[order] - c
    scale = max(1.0, float(np.max(np.abs(U))), abs(c))
    zero_tol = atol * scale

    roots: list[float] = []
    for index, value in enumerate(values):
        if abs(value) <= zero_tol:
            roots.append(float(zz[index]))

    for index in range(zz.size - 1):
        left = values[index]
        right = values[index + 1]
        if abs(left) <= zero_tol or abs(right) <= zero_tol:
            continue
        if left * right < 0.0:
            fraction = -left / (right - left)
            roots.append(float(zz[index] + fraction * (zz[index + 1] - zz[index])))

    if not roots:
        return np.array([], dtype=float)

    roots = sorted(roots)
    unique = [roots[0]]
    for root in roots[1:]:
        if abs(root - unique[-1]) > 10.0 * zero_tol:
            unique.append(root)
    return np.array(unique, dtype=float)
