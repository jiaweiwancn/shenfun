#!/usr/bin/env python
"""Run a tiny production-file smoke for the single-mode channel resolvent."""

from __future__ import annotations

import argparse
from pathlib import Path

import h5py
import numpy as np

from compute_mkm_channel_resolvent import compute_single_mode_resolvent


SERVER = "jay@100.88.70.60"
SERVER_REPO = Path("/media/jay/data1/shenfun")
SERVER_ENV_PYTHON = Path("/media/jay/data1/conda_envs/shenfun_dns_np126_20260702/bin/python")
PRODUCTION_DIR = Path("/media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702")
DEFAULT_TARGET = PRODUCTION_DIR / "MKM_production_64_64_32_target_t60_t180.h5"
DEFAULT_CONSTRAINT = PRODUCTION_DIR / "MKM_constraints_N64_64_32_cheb_quadrature_spectral.h5"
DEFAULT_MODE_INDEX = (1, 1)
DEFAULT_OMEGA = (0.1, 0.2, 0.4)
DEFAULT_N_SINGULAR = 4
DEFAULT_RE_TAU = 180.0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target-h5", default=str(DEFAULT_TARGET), help="Production target HDF5 file.")
    parser.add_argument("--constraint-file", default=str(DEFAULT_CONSTRAINT), help="Matching constraint HDF5 file.")
    parser.add_argument("--output-dir", default=None, help="Directory for the smoke resolvent HDF5.")
    parser.add_argument("--mode-index", nargs=2, type=int, default=DEFAULT_MODE_INDEX, metavar=("I", "J"))
    parser.add_argument("--omega", nargs="+", type=float, default=list(DEFAULT_OMEGA), help="Angular frequencies.")
    parser.add_argument("--n-singular", type=int, default=DEFAULT_N_SINGULAR)
    parser.add_argument("--re-tau", type=float, default=DEFAULT_RE_TAU, help="Re_tau passed to the resolvent CLI.")
    return parser.parse_args()


def expected_server_command(
    target_h5: Path,
    constraint_file: Path,
    output_dir: Path,
    mode_index: tuple[int, int],
    omega: np.ndarray,
    n_singular: int,
    re_tau: float | None,
) -> str:
    omega_args = " ".join(f"{value:.12g}" for value in omega)
    re_tau_arg = "" if re_tau is None else f" --re-tau {re_tau:.12g}"
    command = (
        f"cd {SERVER_REPO} && {SERVER_ENV_PYTHON} "
        "scripts/mkm_dns_target/run_mkm_channel_resolvent_production_smoke.py "
        f"--target-h5 {target_h5} "
        f"--constraint-file {constraint_file} "
        f"--output-dir {output_dir} "
        f"--mode-index {mode_index[0]} {mode_index[1]} "
        f"--omega {omega_args} "
        f"--n-singular {n_singular}"
        f"{re_tau_arg}"
    )
    return f"ssh {SERVER!s} '{command}'"


def output_path(output_dir: Path, mode_index: tuple[int, int]) -> Path:
    return output_dir / f"MKM_channel_resolvent_smoke_i{mode_index[0]}_j{mode_index[1]}.h5"


def print_missing_message(
    missing: list[Path],
    target_h5: Path,
    constraint_file: Path,
    output_dir: Path,
    mode_index: tuple[int, int],
    omega: np.ndarray,
    n_singular: int,
    re_tau: float | None,
) -> None:
    print("Production resolvent smoke could not run because required HDF5 files are missing locally.")
    print("Expected production target:")
    print(f"  {target_h5}")
    print("Expected production constraint:")
    print(f"  {constraint_file}")
    print("Missing paths:")
    for path in missing:
        print(f"  {path}")
    print()
    print("Recommended server command:")
    print(
        expected_server_command(
            target_h5,
            constraint_file,
            output_dir,
            mode_index,
            omega,
            n_singular,
            re_tau,
        )
    )


def print_output_summary(path: Path) -> None:
    with h5py.File(path, "r") as f:
        mode_index = f["mode/index"][:]
        kappa = float(f["mode/kappa"][()])
        lambda_ = float(f["mode/lambda"][()])
        omega = f["frequencies/omega"][:]
        singular_values = f["resolvent/singular_values"][:]
        max_response_constraint = float(np.max(f["diagnostics/constraint_residual_response"][:]))
        max_forcing_constraint = float(np.max(f["diagnostics/constraint_residual_forcing"][:]))
        max_response_energy_error = float(np.max(f["diagnostics/response_energy_norm_error"][:]))
        max_forcing_energy_error = float(np.max(f["diagnostics/forcing_energy_norm_error"][:]))
        critical_counts = f["critical_layers/count"][:]

    print(f"wrote={path}")
    print(f"mode_index=({int(mode_index[0])},{int(mode_index[1])})")
    print(f"kappa={kappa:.12g} lambda={lambda_:.12g}")
    print(f"n_omega={omega.size}")
    print(f"singular_values_shape={singular_values.shape}")
    print("leading_singular_values:")
    for omega_value, values in zip(omega, singular_values):
        formatted = " ".join(f"{value:.6e}" for value in values)
        print(f"  omega={omega_value:.12g}: {formatted}")
    print(f"max_response_constraint_residual={max_response_constraint:.6e}")
    print(f"max_forcing_constraint_residual={max_forcing_constraint:.6e}")
    print(f"max_response_energy_norm_error={max_response_energy_error:.6e}")
    print(f"max_forcing_energy_norm_error={max_forcing_energy_error:.6e}")
    print(f"critical_layer_counts={critical_counts.tolist()}")


def main() -> int:
    args = parse_args()
    target_h5 = Path(args.target_h5).expanduser()
    constraint_file = Path(args.constraint_file).expanduser()
    mode_index = (int(args.mode_index[0]), int(args.mode_index[1]))
    omega = np.asarray(args.omega, dtype=float)
    output_dir = (
        Path(args.output_dir).expanduser()
        if args.output_dir is not None
        else target_h5.parent
    )

    missing = [path for path in (target_h5, constraint_file) if not path.exists()]
    if missing:
        print_missing_message(
            missing,
            target_h5,
            constraint_file,
            output_dir,
            mode_index,
            omega,
            args.n_singular,
            args.re_tau,
        )
        return 2

    output = output_path(output_dir, mode_index)
    compute_single_mode_resolvent(
        target_h5,
        constraint_file,
        output,
        mode_index,
        omega,
        args.n_singular,
        re_tau=args.re_tau,
        overwrite=True,
    )
    print_output_summary(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
