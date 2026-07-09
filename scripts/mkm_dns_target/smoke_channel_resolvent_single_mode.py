#!/usr/bin/env python
"""Synthetic smoke test for the single-mode MKM channel resolvent CLI."""

from __future__ import annotations

import subprocess
import sys
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
    chebyshev_gauss_physical_weights,
    load_constraint_operators,
    rebuild_gtilde_and_nullspace,
    velocity_energy_weight,
)


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
        "k_stream": np.array([0.0, 1.5]),
        "k_span": np.array([0.0, 0.5]),
        "D_wall": D_wall,
        "B_boundary": B_boundary,
        "E_stream": E_stream,
        "E_span": E_span,
        "E_wall": E_wall,
    }
    return z, operators


def write_tiny_fixtures(directory: Path) -> tuple[Path, Path]:
    z, operators = synthetic_operators(nz=12)
    U = 1.0 - z**2
    target_h5 = directory / "synthetic_target.h5"
    constraint_h5 = directory / "synthetic_constraints.h5"

    with h5py.File(target_h5, "w") as f:
        f.attrs["Re_tau"] = 180.0
        f.attrs["component_order_level_major"] = "[streamwise, spanwise, wallnormal]"
        f.attrs["component_names"] = "streamwise,spanwise,wallnormal"
        f.create_dataset("geometry/z_wall", data=z)
        f.create_dataset("geometry/k_stream", data=operators["k_stream"])
        f.create_dataset("geometry/k_span", data=operators["k_span"])
        mean = np.column_stack((U, np.zeros_like(U), np.zeros_like(U)))
        ds = f.create_dataset("mean_profile", data=mean)
        ds.attrs["columns"] = "streamwise,spanwise,wallnormal"

    with h5py.File(constraint_h5, "w") as f:
        f.attrs["svd_relative_tolerance"] = 1e-12
        f.attrs["component_order_level_major"] = "[streamwise, spanwise, wallnormal]"
        f.create_dataset("grid/z_wall", data=z)
        f.create_dataset("wavenumbers/k_stream", data=operators["k_stream"])
        f.create_dataset("wavenumbers/k_span", data=operators["k_span"])
        f.create_dataset("operators/D_wall", data=operators["D_wall"])
        f.create_dataset("operators/B_boundary", data=operators["B_boundary"])
        f.create_dataset("operators/E_stream", data=operators["E_stream"])
        f.create_dataset("operators/E_span", data=operators["E_span"])
        f.create_dataset("operators/E_wall", data=operators["E_wall"])

    return target_h5, constraint_h5


def dataset_schema(path: Path) -> list[str]:
    lines: list[str] = []
    with h5py.File(path, "r") as f:
        def visitor(name: str, obj: h5py.Dataset | h5py.Group) -> None:
            if isinstance(obj, h5py.Dataset):
                lines.append(f"{name}: shape={obj.shape} dtype={obj.dtype}")

        f.visititems(visitor)
    return sorted(lines)


def assert_small(name: str, value: float, tolerance: float) -> None:
    if value > tolerance:
        raise AssertionError(f"{name}={value:.6e} exceeds tolerance={tolerance:.6e}")


def main() -> int:
    script = Path(__file__).with_name("compute_mkm_channel_resolvent.py")
    omega = np.array([0.45, 0.75, 1.05])

    with tempfile.TemporaryDirectory(prefix="mkm_resolvent_smoke_", dir="/private/tmp") as tmp:
        tmpdir = Path(tmp)
        target_h5, constraint_h5 = write_tiny_fixtures(tmpdir)
        output_h5 = tmpdir / "synthetic_resolvent.h5"
        command = [
            sys.executable,
            str(script),
            "--target-h5",
            str(target_h5),
            "--constraint-file",
            str(constraint_h5),
            "--output",
            str(output_h5),
            "--mode-index",
            "1",
            "1",
            "--omega",
            *(f"{value:.12g}" for value in omega),
            "--n-singular",
            "4",
            "--overwrite",
        ]
        completed = subprocess.run(command, check=True, text=True, capture_output=True)

        with h5py.File(output_h5, "r") as f:
            singular_values = f["resolvent/singular_values"][:]
            response_modes = f["resolvent/response_modes"][:]
            forcing_modes = f["resolvent/forcing_modes"][:]
            z = f["geometry/z_wall"][:]
            kappa = float(f["mode/kappa"][()])
            lambda_ = float(f["mode/lambda"][()])
            critical_z = f["critical_layers/z"][:]
            critical_count = f["critical_layers/count"][:]
            max_response_constraint = float(np.max(f["diagnostics/constraint_residual_response"][:]))
            max_forcing_constraint = float(np.max(f["diagnostics/constraint_residual_forcing"][:]))
            max_response_energy_error = float(np.max(f["diagnostics/response_energy_norm_error"][:]))
            max_forcing_energy_error = float(np.max(f["diagnostics/forcing_energy_norm_error"][:]))

        if singular_values.shape != (omega.size, 4):
            raise AssertionError(f"unexpected singular-value shape: {singular_values.shape}")
        if not np.all(np.isfinite(singular_values)):
            raise AssertionError("singular values contain nonfinite values")
        if not np.all(singular_values > 0.0):
            raise AssertionError("singular values are not strictly positive")
        if not np.all(np.diff(singular_values, axis=1) <= 1e-12):
            raise AssertionError("singular values are not sorted in nonincreasing order")

        operators = load_constraint_operators(constraint_h5)
        _, Gtilde, _, _ = rebuild_gtilde_and_nullspace(operators, kappa, lambda_, rtol=1e-12)
        weights_z = chebyshev_gauss_physical_weights(z)
        Wq = velocity_energy_weight(weights_z)
        checked_response_constraint = 0.0
        checked_forcing_constraint = 0.0
        checked_response_energy = 0.0
        checked_forcing_energy = 0.0
        for omega_index in range(response_modes.shape[0]):
            for mode_index in range(response_modes.shape[1]):
                response = response_modes[omega_index, mode_index]
                forcing = forcing_modes[omega_index, mode_index]
                checked_response_constraint = max(
                    checked_response_constraint,
                    float(np.linalg.norm(Gtilde @ response)),
                )
                checked_forcing_constraint = max(
                    checked_forcing_constraint,
                    float(np.linalg.norm(Gtilde @ forcing)),
                )
                checked_response_energy = max(
                    checked_response_energy,
                    abs(float(np.real(response.conj().T @ Wq @ response)) - 1.0),
                )
                checked_forcing_energy = max(
                    checked_forcing_energy,
                    abs(float(np.real(forcing.conj().T @ Wq @ forcing)) - 1.0),
                )

        middle_roots = critical_z[1, :critical_count[1]]
        expected_root_magnitude = np.sqrt(1.0 - omega[1] / kappa)
        if critical_count[1] != 2:
            raise AssertionError(f"expected two critical layers, got {critical_count[1]}")
        if not np.allclose(np.sort(np.abs(middle_roots)), expected_root_magnitude, atol=0.04):
            raise AssertionError(
                f"critical-layer roots {middle_roots} do not match +/-{expected_root_magnitude:.6f}"
            )

        assert_small("max_response_constraint", max_response_constraint, 1e-10)
        assert_small("max_forcing_constraint", max_forcing_constraint, 1e-10)
        assert_small("max_response_energy_error", max_response_energy_error, 1e-10)
        assert_small("max_forcing_energy_error", max_forcing_energy_error, 1e-10)
        assert_small("checked_response_constraint", checked_response_constraint, 1e-10)
        assert_small("checked_forcing_constraint", checked_forcing_constraint, 1e-10)
        assert_small("checked_response_energy", checked_response_energy, 1e-10)
        assert_small("checked_forcing_energy", checked_forcing_energy, 1e-10)

        print("smoke_channel_resolvent_single_mode: ok")
        print("cli_stdout:")
        print(completed.stdout.strip())
        print(f"singular_values_first_omega={singular_values[0]}")
        print(f"critical_layers_middle_omega={middle_roots}")
        print(f"max_response_constraint={max_response_constraint:.6e}")
        print(f"max_forcing_constraint={max_forcing_constraint:.6e}")
        print(f"max_response_energy_error={max_response_energy_error:.6e}")
        print(f"max_forcing_energy_error={max_forcing_energy_error:.6e}")
        print("hdf5_schema:")
        for line in dataset_schema(output_h5):
            print(f"  {line}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
