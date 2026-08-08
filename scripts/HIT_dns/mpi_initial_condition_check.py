#!/usr/bin/env python3
"""Small MPI verification gate for the Mann initial condition and NS operator."""

from __future__ import annotations

import argparse
import json

from mpi4py import MPI

from hit_diagnostics import field_invariants, nonlinear_energy_residual
from mann_initializer import initialize_mann_velocity
from solver_backend import DNSParameters, advance_to_time, create_ns_context, create_rk4_stepper
from spectrum_model import create_initial_spectrum


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=32)
    parser.add_argument("--seed", type=int, default=421971)
    parser.add_argument("--decomposition", choices=("pencil", "slab"), default="pencil")
    parser.add_argument(
        "--backend", choices=("spectraldns", "shenfun"), default="spectraldns"
    )
    parser.add_argument("--planner-effort", default="FFTW_ESTIMATE")
    parser.add_argument("--steps", type=int, default=1)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    settings = DNSParameters(
        n=args.n,
        decomposition=args.decomposition,
        planner_effort=args.planner_effort,
        backend=args.backend,
    )
    solver, context = create_ns_context(settings)
    initialization = initialize_mann_velocity(
        context,
        create_initial_spectrum(),
        args.seed,
        settings.shape,
        settings.lengths,
    )
    initial_metrics = field_invariants(context, settings.shape)
    initial_metrics["relative_nonlinear_energy_residual"] = nonlinear_energy_residual(
        solver, context, settings.shape
    )
    if args.steps < 0:
        raise ValueError("steps must be nonnegative")
    if args.steps:
        stepper = create_rk4_stepper(solver, context)
        advance_to_time(
            solver,
            context,
            stepper,
            target_time_s=args.steps * settings.dt_s,
            nominal_dt_s=settings.dt_s,
        )
    final_metrics = field_invariants(context, settings.shape)
    passed = bool(
        initial_metrics["finite"]
        and initial_metrics["relative_spectral_divergence"] < 1.0e-12
        and initial_metrics["parseval_relative_error"] < 1.0e-10
        and initial_metrics["relative_nonlinear_energy_residual"] < 1.0e-12
        and final_metrics["finite"]
        and final_metrics["relative_spectral_divergence"] < 1.0e-12
        and final_metrics["parseval_relative_error"] < 1.0e-10
    )
    report = {
        "mpi_ranks": MPI.COMM_WORLD.size,
        "settings": settings.__dict__,
        "initialization": initialization,
        "initial_metrics": initial_metrics,
        "final_metrics": final_metrics,
        "steps": args.steps,
        "passed": passed,
    }
    if MPI.COMM_WORLD.rank == 0:
        print(json.dumps(report, indent=2, sort_keys=True))
    if hasattr(context.T, "destroy"):
        context.T.destroy()
    if not passed:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
