#!/usr/bin/env python3
"""Run the Comte-Bellot--Corrsin decaying-HIT DNS on an MPI Linux host."""

from __future__ import annotations

import argparse
from dataclasses import asdict
from importlib.metadata import PackageNotFoundError, version
import json
from pathlib import Path
import socket
import subprocess
import sys
from typing import Any

from mpi4py import MPI
import numpy as np

from hit_diagnostics import cfl_number, energy_spectra, nonlinear_energy_residual, turbulence_statistics
from hit_io import (
    append_diagnostic_row,
    ensure_directory,
    load_checkpoint,
    station_slug,
    write_checkpoint,
    write_station_lightweight,
)
from mann_initializer import initialize_mann_velocity
from reference_data import INITIAL_STATION, station_to_elapsed_seconds
from solver_backend import DNSParameters, advance_to_time, create_ns_context, create_rk4_stepper
from spectrum_model import create_initial_spectrum


def parse_station_list(text: str) -> list[float]:
    stations = sorted({float(value.strip()) for value in text.split(",") if value.strip()})
    if not stations or stations[0] < INITIAL_STATION:
        raise argparse.ArgumentTypeError("stations must be a comma list with values >= 42")
    return stations


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, default=384)
    parser.add_argument("--length-cm", type=float, default=10.0 * np.pi)
    parser.add_argument("--viscosity-cm2-s", type=float, default=0.14941176470588236)
    parser.add_argument("--dt-s", type=float, default=1.0e-4)
    parser.add_argument("--seed", type=int, default=421971)
    parser.add_argument("--stations", type=parse_station_list, default=parse_station_list("42,98,171"))
    parser.add_argument("--raw-dir", type=Path, required=True)
    parser.add_argument("--light-dir", type=Path, required=True)
    parser.add_argument("--restart", type=Path)
    parser.add_argument("--diagnostics-every", type=int, default=100)
    parser.add_argument("--checkpoint-every", type=int, default=1000)
    parser.add_argument("--maximum-cfl", type=float, default=0.5)
    parser.add_argument("--minimum-kmax-eta", type=float, default=1.0)
    parser.add_argument("--decomposition", choices=("pencil", "slab"), default="pencil")
    parser.add_argument("--threads", type=int, default=1)
    parser.add_argument("--planner-effort", default="FFTW_MEASURE")
    parser.add_argument("--git-commit", default=None)
    return parser.parse_args()


def package_version(name: str) -> str:
    try:
        return version(name)
    except PackageNotFoundError:
        return "unavailable"


def discover_git_commit() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"
    return result.stdout.strip()


def build_configuration(args: argparse.Namespace, settings: DNSParameters) -> dict[str, Any]:
    return {
        **asdict(settings),
        "seed": int(args.seed),
        "stations_tU0_over_M": list(args.stations),
        "maximum_cfl": float(args.maximum_cfl),
        "minimum_kmax_eta": float(args.minimum_kmax_eta),
        "diagnostics_every": int(args.diagnostics_every),
        "checkpoint_every": int(args.checkpoint_every),
        "git_commit": args.git_commit or discover_git_commit(),
        "command": [sys.executable, *sys.argv],
        "hostname": socket.gethostname(),
        "mpi_ranks": MPI.COMM_WORLD.size,
        "versions": {
            "python": sys.version.split()[0],
            "numpy": package_version("numpy"),
            "mpi4py": package_version("mpi4py"),
            "mpi4py-fft": package_version("mpi4py-fft"),
            "shenfun": package_version("shenfun"),
            "spectralDNS": package_version("spectralDNS"),
            "h5py": package_version("h5py"),
        },
    }


def check_fresh_output(args: argparse.Namespace) -> None:
    comm = MPI.COMM_WORLD
    conflict = False
    if comm.rank == 0 and args.restart is None:
        conflict = any(args.raw_dir.glob("*.h5")) or any(args.light_dir.glob("station_*"))
    conflict = comm.bcast(conflict, root=0)
    if conflict:
        raise FileExistsError(
            "Fresh run output already exists; choose new directories or use --restart"
        )


def flattened_log_row(
    station: float | None,
    time_s: float,
    tstep: int,
    cfl: float,
    statistics: dict[str, Any],
) -> dict[str, Any]:
    return {
        "station_tU0_over_M": "" if station is None else station,
        "time_s": time_s,
        "tstep": tstep,
        "cfl": cfl,
        "kinetic_energy_cm2_s^-2": statistics["spectral_energy_cm2_s^-2"],
        "dissipation_cm2_s^-3": statistics["dissipation_cm2_s^-3"],
        "isotropic_u_rms_cm_s": statistics["isotropic_u_rms_cm_s"],
        "kolmogorov_length_cm": statistics["kolmogorov_length_cm"],
        "taylor_microscale_cm": statistics["taylor_microscale_cm"],
        "reynolds_lambda": statistics["reynolds_lambda"],
        "kmax_eta": statistics["kmax_eta"],
        "relative_spectral_divergence": statistics["relative_spectral_divergence"],
        "parseval_relative_error": statistics["parseval_relative_error"],
    }


def main() -> None:
    args = parse_args()
    if args.diagnostics_every < 1 or args.checkpoint_every < 0:
        raise ValueError("diagnostics-every must be positive and checkpoint-every nonnegative")
    settings = DNSParameters(
        n=args.n,
        length_cm=args.length_cm,
        viscosity_cm2_s=args.viscosity_cm2_s,
        dt_s=args.dt_s,
        threads=args.threads,
        decomposition=args.decomposition,
        planner_effort=args.planner_effort,
    )
    settings.validate()
    ensure_directory(args.raw_dir)
    ensure_directory(args.light_dir)
    check_fresh_output(args)

    solver, context = create_ns_context(settings)
    configuration = build_configuration(args, settings)
    if args.restart is None:
        initialization = initialize_mann_velocity(
            context,
            create_initial_spectrum(),
            args.seed,
            settings.shape,
            settings.lengths,
        )
        nonlinear_residual = nonlinear_energy_residual(solver, context, settings.shape)
        if nonlinear_residual >= 1.0e-12:
            raise RuntimeError(f"Nonlinear energy gate failed: {nonlinear_residual:.6e}")
    else:
        restored = load_checkpoint(args.restart, context, settings.shape)
        initialization = restored["initialization"]
        solver.params.t = restored["time_s"]
        solver.params.tstep = restored["tstep"]
        checkpoint_configuration = restored["configuration"]
        for key, expected in (
            ("n", settings.n),
            ("length_cm", settings.length_cm),
            ("viscosity_cm2_s", settings.viscosity_cm2_s),
        ):
            if not np.isclose(checkpoint_configuration[key], expected):
                raise ValueError(f"Restart mismatch for {key}")

    diagnostic_path = args.light_dir / "diagnostics.csv"

    def evaluate_and_gate(station: float | None = None) -> dict[str, Any]:
        stats = turbulence_statistics(
            context,
            settings.viscosity_cm2_s,
            settings.shape,
            settings.lengths,
        )
        cfl = cfl_number(
            context,
            solver.params.dt,
            settings.lengths,
            settings.shape,
        )
        row = flattened_log_row(station, solver.params.t, solver.params.tstep, cfl, stats)
        append_diagnostic_row(diagnostic_path, row)
        if MPI.COMM_WORLD.rank == 0:
            print(json.dumps({"progress": row}, sort_keys=True), flush=True)
        if not stats["finite"]:
            raise FloatingPointError("Non-finite spectral or physical velocity")
        if cfl > args.maximum_cfl:
            raise RuntimeError(f"CFL gate failed: {cfl:.6g} > {args.maximum_cfl:.6g}")
        if stats["kmax_eta"] < args.minimum_kmax_eta:
            raise RuntimeError(
                f"Resolution gate failed: kmax*eta={stats['kmax_eta']:.6g}"
            )
        if stats["relative_spectral_divergence"] >= 1.0e-12:
            raise RuntimeError("Divergence gate failed")
        if stats["parseval_relative_error"] >= 1.0e-10:
            raise RuntimeError("Parseval gate failed")
        return {**stats, "cfl": cfl}

    def output_station(station: float) -> None:
        stats = evaluate_and_gate(station)
        spectra = energy_spectra(context, settings.shape, settings.lengths)
        summary = {
            "station_tU0_over_M": station,
            "elapsed_time_s": solver.params.t,
            "tstep": solver.params.tstep,
            "configuration": configuration,
            "initialization": initialization,
            "statistics": stats,
            "spectrum_closure": {
                key: spectra[key]
                for key in (
                    "E_integral_cm2_s^-2",
                    "kinetic_energy_cm2_s^-2",
                    "E11_integral_cm2_s^-2",
                    "u1_variance_cm2_s^-2",
                )
            },
        }
        slug = station_slug(station)
        write_checkpoint(
            args.raw_dir / f"station_{slug}.h5",
            context,
            settings.shape,
            solver.params.t,
            solver.params.tstep,
            settings.dt_s,
            configuration,
            initialization,
            station=station,
        )
        write_station_lightweight(args.light_dir, station, summary, spectra)

    tolerance = 32.0 * np.finfo(float).eps
    if args.restart is None:
        output_station(INITIAL_STATION)
    elif abs(solver.params.t - station_to_elapsed_seconds(INITIAL_STATION)) <= tolerance:
        output_station(INITIAL_STATION)

    def after_step(_solver: Any, _context: Any) -> None:
        if solver.params.tstep % args.diagnostics_every == 0:
            evaluate_and_gate()
        if args.checkpoint_every and solver.params.tstep % args.checkpoint_every == 0:
            write_checkpoint(
                args.raw_dir / f"checkpoint_step_{solver.params.tstep:08d}.h5",
                context,
                settings.shape,
                solver.params.t,
                solver.params.tstep,
                settings.dt_s,
                configuration,
                initialization,
            )

    stepper = create_rk4_stepper(solver, context)
    for station in args.stations:
        target_time = station_to_elapsed_seconds(station)
        if target_time <= solver.params.t + tolerance:
            continue
        advance_to_time(
            solver,
            context,
            stepper,
            target_time,
            settings.dt_s,
            after_step=after_step,
        )
        output_station(station)

    if MPI.COMM_WORLD.rank == 0:
        print(
            json.dumps(
                {
                    "completed": True,
                    "final_time_s": solver.params.t,
                    "final_tstep": solver.params.tstep,
                },
                sort_keys=True,
            ),
            flush=True,
        )
    if hasattr(context.T, "destroy"):
        context.T.destroy()


if __name__ == "__main__":
    main()
