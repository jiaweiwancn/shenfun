#!/usr/bin/env python
"""Compute a single-mode MKM channel-flow resolvent."""

from __future__ import annotations

import argparse
from pathlib import Path

import h5py
import numpy as np

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


FOURIER_TIME_CONVENTION = "q(x,y,z,t)=qhat(z)*exp(i*kappa*x + i*lambda*y - i*omega*t)"
RESOLVENT_FORMULA = "H(omega)=(-1j*omega*I - A)^(-1), A=Q^* Wq L_raw Q"
LINEAR_OPERATOR_FORMULA = (
    "L_raw q = -1j*kappa*U*q - u_z*Uprime*e_stream "
    "+ (D_wall@D_wall - (kappa^2+lambda^2)I)q/Re_tau"
)
WEIGHT_DEFINITION = (
    "Fejer first-rule physical L2 weights on [-1,1], repeated for level-major "
    "velocity components; no kinetic-energy 1/2 factor"
)
SVD_CONVENTION = "H = Psi Sigma Phi^*, response_modes=Q@Psi, forcing_modes=Q@Phi"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target-h5", required=True, help="Input MKM target HDF5 file.")
    parser.add_argument("--constraint-file", required=True, help="Matching constraint recipe HDF5 file.")
    parser.add_argument("--output", required=True, help="Output resolvent HDF5 file.")
    parser.add_argument("--mode-index", nargs=2, type=int, required=True, metavar=("I", "J"))
    parser.add_argument("--omega", nargs="+", type=float, required=True, help="Angular frequencies.")
    parser.add_argument("--n-singular", type=int, default=6, help="Number of singular modes to store.")
    parser.add_argument("--re-tau", type=float, help="Override Re_tau. Defaults to target attr or 180.")
    parser.add_argument("--svd-rtol", type=float, help="Constraint SVD relative tolerance.")
    parser.add_argument("--overwrite", action="store_true", help="Replace an existing output file.")
    return parser.parse_args()


def _as_real_scalar(value: complex) -> float:
    return float(np.real_if_close(value, tol=1000).real)


def _resolve_re_tau(target: dict[str, object], override: float | None) -> float:
    if override is not None:
        return float(override)
    re_tau = float(target.get("Re_tau", np.nan))
    if np.isfinite(re_tau):
        return re_tau
    return 180.0


def _validate_grid_and_wavenumbers(
    target: dict[str, object],
    operators: dict[str, object],
    mode_i: int,
    mode_j: int,
) -> None:
    z_target = np.asarray(target["z_wall"])
    z_constraint = np.asarray(operators["z_wall"])
    if z_target.shape != z_constraint.shape or not np.allclose(z_target, z_constraint):
        raise ValueError("target and constraint wall-normal grids do not match")

    k_stream = np.asarray(operators["k_stream"])
    k_span = np.asarray(operators["k_span"])
    if mode_i < 0 or mode_i >= k_stream.size:
        raise IndexError(f"streamwise mode index {mode_i} is outside [0, {k_stream.size})")
    if mode_j < 0 or mode_j >= k_span.size:
        raise IndexError(f"spanwise mode index {mode_j} is outside [0, {k_span.size})")

    target_k_stream = target.get("k_stream")
    target_k_span = target.get("k_span")
    if target_k_stream is not None and not np.allclose(target_k_stream, k_stream):
        raise ValueError("target and constraint k_stream arrays do not match")
    if target_k_span is not None and not np.allclose(target_k_span, k_span):
        raise ValueError("target and constraint k_span arrays do not match")


def _energy_norm_error(q_modes: np.ndarray, Wq: np.ndarray) -> np.ndarray:
    errors = np.empty(q_modes.shape[1], dtype=float)
    for mode_index in range(q_modes.shape[1]):
        q = q_modes[:, mode_index]
        energy = q.conj().T @ Wq @ q
        errors[mode_index] = abs(_as_real_scalar(energy) - 1.0)
    return errors


def _constraint_residuals(Gtilde: np.ndarray, q_modes: np.ndarray) -> np.ndarray:
    return np.linalg.norm(Gtilde @ q_modes, axis=0)


def _critical_layer_tables(
    z: np.ndarray,
    U: np.ndarray,
    kappa: float,
    omega: np.ndarray,
    Re_tau: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    roots_by_frequency = [critical_layer_locations(z, U, kappa, value) for value in omega]
    max_roots = max(1, max((roots.size for roots in roots_by_frequency), default=0))
    z_table = np.full((omega.size, max_roots), np.nan, dtype=float)
    y_plus_table = np.full_like(z_table, np.nan)
    count = np.zeros(omega.size, dtype=np.int32)
    for index, roots in enumerate(roots_by_frequency):
        count[index] = roots.size
        if roots.size:
            z_table[index, :roots.size] = roots
            distance_to_nearest_wall = np.minimum(roots + 1.0, 1.0 - roots)
            y_plus_table[index, :roots.size] = Re_tau * distance_to_nearest_wall
    return z_table, y_plus_table, count


def compute_single_mode_resolvent(
    target_h5: str | Path,
    constraint_file: str | Path,
    output: str | Path,
    mode_index: tuple[int, int],
    omega: np.ndarray,
    n_singular: int,
    *,
    re_tau: float | None = None,
    svd_rtol: float | None = None,
    overwrite: bool = False,
) -> dict[str, float | int | str]:
    """Compute and write a single-mode resolvent HDF5 file."""

    target_path = Path(target_h5).expanduser().resolve()
    constraint_path = Path(constraint_file).expanduser().resolve()
    output_path = Path(output).expanduser().resolve()
    if n_singular <= 0:
        raise ValueError("n_singular must be positive")
    if omega.size == 0:
        raise ValueError("at least one omega value is required")
    if output_path.exists() and not overwrite:
        raise FileExistsError(f"{output_path} exists; pass --overwrite to replace it")

    target = load_target_metadata(target_path)
    operators = load_constraint_operators(constraint_path)
    mode_i, mode_j = mode_index
    _validate_grid_and_wavenumbers(target, operators, mode_i, mode_j)

    z = np.asarray(target["z_wall"], dtype=float)
    U = np.asarray(target["U"], dtype=float)
    D_wall = np.asarray(operators["D_wall"], dtype=float)
    Re_tau = _resolve_re_tau(target, re_tau)
    rtol = float(operators["svd_rtol"] if svd_rtol is None else svd_rtol)
    k_stream = np.asarray(operators["k_stream"], dtype=float)
    k_span = np.asarray(operators["k_span"], dtype=float)
    kappa = float(k_stream[mode_i])
    lambda_ = float(k_span[mode_j])

    singular_values_constraint, Gtilde, Nmat, rank = rebuild_gtilde_and_nullspace(
        operators,
        kappa,
        lambda_,
        rtol=rtol,
    )
    weights_z = chebyshev_gauss_physical_weights(z)
    Wq = velocity_energy_weight(weights_z)
    Q = energy_orthonormal_basis(Nmat, Wq)
    energy_orthonormality_error = float(np.linalg.norm(Q.conj().T @ Wq @ Q - np.eye(Q.shape[1])))
    basis_constraint_residual = float(np.linalg.norm(Gtilde @ Q))

    Uprime = compute_uprime(U, D_wall)
    L_raw = build_linearized_velocity_operator(U, Uprime, D_wall, Re_tau, kappa, lambda_)
    A = Q.conj().T @ Wq @ L_raw @ Q
    n_admissible = Q.shape[1]
    n_keep = min(n_singular, n_admissible)
    identity = np.eye(n_admissible, dtype=complex)

    n_omega = omega.size
    modal_dim = 3 * z.size
    singular_values = np.empty((n_omega, n_keep), dtype=float)
    response_modes = np.empty((n_omega, n_keep, modal_dim), dtype=np.complex128)
    forcing_modes = np.empty_like(response_modes)
    response_energy_density = np.empty((n_omega, n_keep, z.size), dtype=float)
    component_energy_density = np.empty((n_omega, n_keep, z.size, 3), dtype=float)
    constraint_residual_response = np.empty((n_omega, n_keep), dtype=float)
    constraint_residual_forcing = np.empty_like(constraint_residual_response)
    response_energy_norm_error = np.empty_like(constraint_residual_response)
    forcing_energy_norm_error = np.empty_like(constraint_residual_response)
    resolvent_matrix_condition = np.empty(n_omega, dtype=float)

    for omega_index, omega_value in enumerate(omega):
        shifted_operator = -1j * omega_value * identity - A
        resolvent_matrix_condition[omega_index] = float(np.linalg.cond(shifted_operator))
        H = np.linalg.solve(shifted_operator, identity)
        Psi, Sigma, Vh = np.linalg.svd(H, full_matrices=False)
        Phi = Vh.conj().T

        singular_values[omega_index] = Sigma[:n_keep]
        response = Q @ Psi[:, :n_keep]
        forcing = Q @ Phi[:, :n_keep]
        response_modes[omega_index] = response.T
        forcing_modes[omega_index] = forcing.T
        constraint_residual_response[omega_index] = _constraint_residuals(Gtilde, response)
        constraint_residual_forcing[omega_index] = _constraint_residuals(Gtilde, forcing)
        response_energy_norm_error[omega_index] = _energy_norm_error(response, Wq)
        forcing_energy_norm_error[omega_index] = _energy_norm_error(forcing, Wq)

        for mode_number in range(n_keep):
            energy = modal_energy_density(response[:, mode_number], weights_z)
            response_energy_density[omega_index, mode_number] = energy["total_density"]
            component_energy_density[omega_index, mode_number] = energy["component_density"]

    critical_z, critical_y_plus, critical_count = _critical_layer_tables(z, U, kappa, omega, Re_tau)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with h5py.File(output_path, "w") as f:
        f.attrs["description"] = "Single-mode MKM channel-flow velocity resolvent."
        f.attrs["source_target_h5"] = str(target_path)
        f.attrs["source_constraint_file"] = str(constraint_path)
        f.attrs["fourier_time_convention"] = FOURIER_TIME_CONVENTION
        f.attrs["resolvent_formula"] = RESOLVENT_FORMULA
        f.attrs["linear_operator_formula"] = LINEAR_OPERATOR_FORMULA
        f.attrs["svd_convention"] = SVD_CONVENTION
        f.attrs["component_order_level_major"] = target["component_order_level_major"]
        f.attrs["component_names"] = ",".join(target["component_names"])
        f.attrs["Re_tau"] = Re_tau
        f.attrs["response_modes_energy_normalized"] = True
        f.attrs["forcing_modes_energy_normalized"] = True
        f.attrs["energy_weight_definition"] = WEIGHT_DEFINITION
        f.attrs["requested_n_singular"] = int(n_singular)
        f.attrs["stored_n_singular"] = int(n_keep)
        f.attrs["constraint_svd_rtol"] = rtol

        f.create_dataset("geometry/z_wall", data=z)
        f.create_dataset("geometry/k_stream", data=k_stream)
        f.create_dataset("geometry/k_span", data=k_span)
        f.create_dataset("mean/U", data=U)
        f.create_dataset("mean/Uprime", data=Uprime)
        f.create_dataset("mode/index", data=np.array([mode_i, mode_j], dtype=np.int32))
        f.create_dataset("mode/kappa", data=kappa)
        f.create_dataset("mode/lambda", data=lambda_)
        f["mode"].attrs["rank"] = rank
        f["mode"].attrs["nullity"] = Nmat.shape[1]
        f.create_dataset("frequencies/omega", data=omega)

        ds = f.create_dataset("critical_layers/z", data=critical_z)
        ds.attrs["axes"] = "omega,critical_layer_location"
        ds.attrs["description"] = "NaN-padded roots of U(z)=omega/kappa; empty for kappa=0."
        ds = f.create_dataset("critical_layers/y_plus_nearest_wall", data=critical_y_plus)
        ds.attrs["axes"] = "omega,critical_layer_location"
        ds.attrs["definition"] = "Re_tau * min(z+1, 1-z)"
        f.create_dataset("critical_layers/count", data=critical_count)

        ds = f.create_dataset("resolvent/singular_values", data=singular_values)
        ds.attrs["axes"] = "omega,singular_index"
        ds = f.create_dataset("resolvent/response_modes", data=response_modes)
        ds.attrs["axes"] = "omega,singular_index,level_major_velocity"
        ds.attrs["normalization"] = "q^* Wq q = 1"
        ds = f.create_dataset("resolvent/forcing_modes", data=forcing_modes)
        ds.attrs["axes"] = "omega,singular_index,level_major_velocity"
        ds.attrs["normalization"] = "q^* Wq q = 1"
        ds = f.create_dataset("resolvent/response_energy_density", data=response_energy_density)
        ds.attrs["axes"] = "omega,singular_index,z"
        ds.attrs["definition"] = "sum_component |u_component(z)|^2 for response modes"
        ds = f.create_dataset("resolvent/component_energy_density", data=component_energy_density)
        ds.attrs["axes"] = "omega,singular_index,z,component"
        ds.attrs["component_order"] = ",".join(target["component_names"])

        f.create_dataset("diagnostics/constraint_residual_response", data=constraint_residual_response)
        f.create_dataset("diagnostics/constraint_residual_forcing", data=constraint_residual_forcing)
        f.create_dataset("diagnostics/response_energy_norm_error", data=response_energy_norm_error)
        f.create_dataset("diagnostics/forcing_energy_norm_error", data=forcing_energy_norm_error)
        f.create_dataset("diagnostics/energy_orthonormality_error", data=energy_orthonormality_error)
        f.create_dataset("diagnostics/basis_constraint_residual", data=basis_constraint_residual)
        f.create_dataset("diagnostics/resolvent_matrix_condition", data=resolvent_matrix_condition)
        f.create_dataset("diagnostics/constraint_singular_values", data=singular_values_constraint)

    return {
        "output": str(output_path),
        "mode_i": mode_i,
        "mode_j": mode_j,
        "kappa": kappa,
        "lambda": lambda_,
        "rank": rank,
        "nullity": Nmat.shape[1],
        "stored_n_singular": n_keep,
        "energy_orthonormality_error": energy_orthonormality_error,
        "basis_constraint_residual": basis_constraint_residual,
        "max_response_constraint_residual": float(np.max(constraint_residual_response)),
        "max_forcing_constraint_residual": float(np.max(constraint_residual_forcing)),
        "max_response_energy_norm_error": float(np.max(response_energy_norm_error)),
        "max_forcing_energy_norm_error": float(np.max(forcing_energy_norm_error)),
    }


def main() -> int:
    args = parse_args()
    omega = np.asarray(args.omega, dtype=float)
    result = compute_single_mode_resolvent(
        args.target_h5,
        args.constraint_file,
        args.output,
        tuple(args.mode_index),
        omega,
        args.n_singular,
        re_tau=args.re_tau,
        svd_rtol=args.svd_rtol,
        overwrite=args.overwrite,
    )
    print(f"wrote={result['output']}")
    print(
        "mode="
        f"({result['mode_i']},{result['mode_j']}) "
        f"kappa={result['kappa']:.12g} lambda={result['lambda']:.12g}"
    )
    print(
        f"rank={result['rank']} nullity={result['nullity']} "
        f"stored_n_singular={result['stored_n_singular']}"
    )
    print(f"energy_orthonormality_error={result['energy_orthonormality_error']:.6e}")
    print(f"basis_constraint_residual={result['basis_constraint_residual']:.6e}")
    print(f"max_response_constraint_residual={result['max_response_constraint_residual']:.6e}")
    print(f"max_forcing_constraint_residual={result['max_forcing_constraint_residual']:.6e}")
    print(f"max_response_energy_norm_error={result['max_response_energy_norm_error']:.6e}")
    print(f"max_forcing_energy_norm_error={result['max_forcing_energy_norm_error']:.6e}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
