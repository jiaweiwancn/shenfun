#!/usr/bin/env python
"""Lightweight smoke checks for MKM channel resolvent utilities."""

from __future__ import annotations

import tempfile
from pathlib import Path

import h5py
import numpy as np

from build_mkm_constraints import (
    chebyshev_gauss_nodes,
    extraction_matrices,
    interpolation_row,
    spectral_derivative_matrix,
)
from mkm_channel_resolvent_utils import (
    build_linearized_velocity_operator,
    chebyshev_gauss_physical_weights,
    compute_uprime,
    critical_layer_locations,
    energy_orthonormal_basis,
    load_constraint_operators,
    load_target_metadata,
    modal_energy_density,
    rebuild_gtilde_and_nullspace,
    velocity_energy_weight,
)


def assert_small(name: str, value: float, tolerance: float) -> None:
    if value > tolerance:
        raise AssertionError(f"{name}={value:.6e} exceeds tolerance={tolerance:.6e}")


def synthetic_operators(nz: int) -> tuple[np.ndarray, dict[str, np.ndarray]]:
    z = chebyshev_gauss_nodes(nz, -1.0, 1.0)
    D_wall = spectral_derivative_matrix(z)
    B_boundary = np.vstack((
        interpolation_row(z, -1.0),
        interpolation_row(z, 1.0),
    ))
    E_stream, E_span, E_wall = extraction_matrices(nz)
    operators = {
        "z_wall": z,
        "k_stream": np.array([0.0, 1.25]),
        "k_span": np.array([0.0, 0.75]),
        "D_wall": D_wall,
        "B_boundary": B_boundary,
        "E_stream": E_stream,
        "E_span": E_span,
        "E_wall": E_wall,
    }
    return z, operators


def write_tiny_hdf5_fixtures(
    directory: Path,
    z: np.ndarray,
    operators: dict[str, np.ndarray],
    U: np.ndarray,
) -> tuple[Path, Path]:
    target_h5 = directory / "tiny_target.h5"
    constraint_h5 = directory / "tiny_constraints.h5"

    with h5py.File(target_h5, "w") as f:
        f.attrs["Re_tau"] = 180.0
        f.attrs["component_order_level_major"] = "[streamwise, spanwise, wallnormal]"
        f.attrs["component_names"] = "streamwise,spanwise,wallnormal"
        f.attrs["dt"] = 0.5
        f.attrs["sampling_stage_label"] = "synthetic"
        f.create_dataset("geometry/z_wall", data=z)
        f.create_dataset("geometry/k_stream", data=operators["k_stream"])
        f.create_dataset("geometry/k_span", data=operators["k_span"])
        f.create_dataset("sampling/t", data=np.array([0.0, 0.5]))
        mean = np.column_stack((U, np.zeros_like(U), np.zeros_like(U)))
        ds = f.create_dataset("mean_profile", data=mean)
        ds.attrs["columns"] = "streamwise,spanwise,wallnormal"

    with h5py.File(constraint_h5, "w") as f:
        f.attrs["svd_relative_tolerance"] = 1e-12
        f.create_dataset("grid/z_wall", data=z)
        f.create_dataset("wavenumbers/k_stream", data=operators["k_stream"])
        f.create_dataset("wavenumbers/k_span", data=operators["k_span"])
        f.create_dataset("operators/D_wall", data=operators["D_wall"])
        f.create_dataset("operators/B_boundary", data=operators["B_boundary"])
        f.create_dataset("operators/E_stream", data=operators["E_stream"])
        f.create_dataset("operators/E_span", data=operators["E_span"])
        f.create_dataset("operators/E_wall", data=operators["E_wall"])

    return target_h5, constraint_h5


def main() -> int:
    nz = 10
    kappa = 1.25
    lambda_ = 0.75
    z, operators = synthetic_operators(nz)

    singular_values, Gtilde, Nmat, rank = rebuild_gtilde_and_nullspace(
        operators,
        kappa,
        lambda_,
        rtol=1e-12,
    )
    weights_z = chebyshev_gauss_physical_weights(z)
    Wq = velocity_energy_weight(weights_z)
    Q = energy_orthonormal_basis(Nmat, Wq)

    gtilde_nmat_norm = float(np.linalg.norm(Gtilde @ Nmat))
    gtilde_q_norm = float(np.linalg.norm(Gtilde @ Q))
    orthonormality_error = float(np.linalg.norm(Q.conj().T @ Wq @ Q - np.eye(Q.shape[1])))
    weight_sum_error = float(abs(np.sum(weights_z) - 2.0))
    x2_quadrature_error = float(abs(np.sum(weights_z * z**2) - 2.0 / 3.0))
    if not np.all(weights_z > 0.0):
        raise AssertionError("Chebyshev-Gauss physical quadrature weights are not all positive")

    U = 0.5 * (z + 1.0)
    Uprime = compute_uprime(U, operators["D_wall"])
    uprime_error = float(np.linalg.norm(Uprime - 0.5, ord=np.inf))

    critical_locations = critical_layer_locations(z, U, kappa=2.0, omega=1.2)
    if critical_locations.shape != (1,):
        raise AssertionError(f"expected one critical layer, got {critical_locations}")
    critical_location_error = float(abs(critical_locations[0] - 0.2))
    if critical_layer_locations(z, U, kappa=0.0, omega=1.0).size != 0:
        raise AssertionError("kappa=0 should return no finite critical-layer locations")

    first_mode_energy = modal_energy_density(Q[:, 0], weights_z)["total_energy"]
    energy_error = float(abs(first_mode_energy - 1.0))

    L_raw = build_linearized_velocity_operator(
        U,
        Uprime,
        operators["D_wall"],
        Re_tau=180.0,
        kappa=kappa,
        lambda_=lambda_,
    )
    if L_raw.shape != (3 * nz, 3 * nz) or not np.all(np.isfinite(L_raw)):
        raise AssertionError("linearized operator has an invalid shape or nonfinite values")

    with tempfile.TemporaryDirectory() as tmp:
        target_h5, constraint_h5 = write_tiny_hdf5_fixtures(Path(tmp), z, operators, U)
        target = load_target_metadata(target_h5)
        loaded_operators = load_constraint_operators(constraint_h5)
        if not np.allclose(target["U"], U) or target["Re_tau"] != 180.0:
            raise AssertionError("target metadata loader did not round-trip the tiny fixture")
        _, _, loaded_Nmat, loaded_rank = rebuild_gtilde_and_nullspace(
            loaded_operators,
            kappa,
            lambda_,
            rtol=loaded_operators["svd_rtol"],
        )
        if loaded_rank != rank or loaded_Nmat.shape != Nmat.shape:
            raise AssertionError("constraint loader changed the rebuilt rank/nullity")

    assert_small("Gtilde_Nmat_norm", gtilde_nmat_norm, 1e-10)
    assert_small("Gtilde_Q_norm", gtilde_q_norm, 1e-10)
    assert_small("energy_orthonormality_error", orthonormality_error, 1e-10)
    assert_small("weight_sum_error", weight_sum_error, 1e-14)
    assert_small("x2_quadrature_error", x2_quadrature_error, 1e-14)
    assert_small("Uprime_linear_profile_error", uprime_error, 1e-12)
    assert_small("critical_location_error", critical_location_error, 1e-12)
    assert_small("first_Q_mode_energy_error", energy_error, 1e-10)

    print("smoke_channel_resolvent_utils: ok")
    print(f"nz={nz} rank={rank} nullity={Nmat.shape[1]} min_singular={singular_values[rank - 1]:.6e}")
    print(f"Gtilde_Nmat_norm={gtilde_nmat_norm:.6e}")
    print(f"Gtilde_Q_norm={gtilde_q_norm:.6e}")
    print(f"energy_orthonormality_error={orthonormality_error:.6e}")
    print(f"weight_sum={np.sum(weights_z):.16e} x2_quadrature_error={x2_quadrature_error:.6e}")
    print(f"critical_layer_z={critical_locations[0]:.12f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
