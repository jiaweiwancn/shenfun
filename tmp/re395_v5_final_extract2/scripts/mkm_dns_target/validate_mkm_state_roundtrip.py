#!/usr/bin/env python
"""Validate independent MKM state shards against conventional velocity output."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys

import h5py
import numpy as np


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state-h5", required=True)
    parser.add_argument("--velocity-h5", required=True)
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--max-samples", type=int,
                        help="Validate only the first N state samples. Default: every valid sample.")
    parser.add_argument("--absolute-tolerance", type=float, default=2e-11)
    parser.add_argument("--relative-tolerance", type=float, default=2e-11)
    return parser.parse_args()


def decode_attr(value):
    if isinstance(value, bytes):
        return value.decode("utf-8")
    return value


def open_parallel(path: Path, mode: str, comm):
    return h5py.File(path, mode, driver="mpio", comm=comm)


def global_max(comm, value: float) -> float:
    from mpi4py import MPI

    return float(comm.allreduce(float(value), op=MPI.MAX))


def require_global_finite(comm, values, label: str) -> None:
    from mpi4py import MPI

    array = np.asarray(values)
    local_nonfinite = int(array.size - np.count_nonzero(np.isfinite(array)))
    global_nonfinite = int(comm.allreduce(local_nonfinite, op=MPI.SUM))
    if global_nonfinite:
        raise ValueError(f"{label} contains {global_nonfinite} non-finite values")


def main() -> int:
    args = parse_args()
    os.environ.setdefault("MPLBACKEND", "Agg")

    repo = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(repo))
    sys.path.insert(0, str(repo / "demo"))

    from mpi4py import MPI
    from MKM import MKM
    from shenfun import cleanup

    comm = MPI.COMM_WORLD
    state_path = Path(args.state_h5).expanduser().resolve()
    velocity_path = Path(args.velocity_h5).expanduser().resolve()
    output_path = Path(args.output_json).expanduser().resolve()

    missing = None
    if comm.rank == 0:
        absent = [str(path) for path in (state_path, velocity_path) if not path.is_file()]
        if absent:
            missing = f"missing input files: {', '.join(absent)}"
    missing = comm.bcast(missing, root=0)
    if missing is not None:
        raise FileNotFoundError(missing)

    with open_parallel(state_path, "r", comm) as state:
        schema = decode_attr(state.attrs.get("schema_version", ""))
        if schema != "mkm-independent-state-v1":
            raise ValueError(f"unsupported state schema {schema!r}")
        valid_samples = int(state.attrs["valid_samples"])
        if valid_samples <= 0:
            raise ValueError("state shard has no valid samples")
        count = valid_samples
        if args.max_samples is not None:
            if args.max_samples <= 0:
                raise ValueError("--max-samples must be positive")
            count = min(count, args.max_samples)

        N = tuple(int(value) for value in state.attrs["global_shape_physical"])
        domain_flat = tuple(float(value) for value in state.attrs["domain_flat"])
        domain = (
            (domain_flat[0], domain_flat[1]),
            (domain_flat[2], domain_flat[3]),
            (domain_flat[4], domain_flat[5]),
        )
        padding_factor = tuple(float(value) for value in state.attrs["padding_factor"])
        Re = float(state.attrs["re_tau_nominal"])
        bulk_velocity = float(state.attrs["bulk_velocity"])
        dt = float(state.attrs["dns_dt"])
        timestepper = str(decode_attr(state.attrs["timestepper"]))
        convection_form = int(state.attrs.get("convection_form", 0))
        wall_family = str(decode_attr(state.attrs.get("wall_family", "C")))
        tsteps = np.asarray(state["sampling/tstep"][:count], dtype=np.int64)
        times = np.asarray(state["sampling/t"][:count], dtype=np.float64)

        if np.any(tsteps < 0) or np.any(~np.isfinite(times)):
            raise ValueError("valid state sample range contains unwritten time entries")
        if count > 1:
            expected_step_delta = int(state.attrs["sample_every_steps"])
            if not np.all(np.diff(tsteps) == expected_step_delta):
                raise ValueError("state time steps are not uniformly spaced")
            if not np.allclose(np.diff(times), expected_step_delta * dt, rtol=1e-10, atol=1e-12):
                raise ValueError("state physical times are not uniformly spaced")

        solver = MKM(
            N=N,
            domain=domain,
            Re=Re,
            bulk_velocity=bulk_velocity,
            dt=dt,
            conv=convection_form,
            modplot=-1,
            modsave=10**12,
            moderror=-1,
            filename=str(output_path.parent / "MKM_state_validation_scratch"),
            family=wall_family,
            padding_factor=padding_factor,
            checkpoint=10**12,
            timestepper=timestepper,
        )

        spectral_slice = tuple(solver.u_[0].local_slice())
        component_names = ("wallnormal", "streamwise", "spanwise")
        component_groups = ("u0", "u1", "u2")
        max_abs = np.zeros(3, dtype=np.float64)
        max_rel = np.zeros(3, dtype=np.float64)
        max_eta_consistency = 0.0
        max_divergence = 0.0

        with open_parallel(velocity_path, "r", comm) as velocity:
            for sample_index, tstep in enumerate(tsteps):
                key = str(int(tstep))
                for group in component_groups:
                    if f"{group}/3D/{key}" not in velocity:
                        raise KeyError(f"velocity file is missing {group}/3D/{key}")

                target = (sample_index,) + spectral_slice
                u_wall_sample = state["state/u_wall_hat"][target]
                eta_sample = state["state/eta_wall_hat"][target]
                require_global_finite(comm, u_wall_sample, f"u_wall_hat sample {sample_index}")
                require_global_finite(comm, eta_sample, f"eta_wall_hat sample {sample_index}")
                zero_stream = np.asarray(
                    state["state/u_stream_zero_mode"][sample_index],
                    dtype=np.float64,
                )
                zero_span = np.asarray(
                    state["state/u_span_zero_mode"][sample_index],
                    dtype=np.float64,
                )
                if not np.all(np.isfinite(zero_stream)) or not np.all(np.isfinite(zero_span)):
                    raise ValueError(f"zero-mode state sample {sample_index} contains non-finite values")
                solver.u_[0][:] = u_wall_sample
                solver.g_[:] = eta_sample

                derivative = solver.dudx()
                solver.u_[1] = 1j * (
                    solver.K_over_K2[0] * derivative
                    + solver.K_over_K2[1] * solver.g_
                )
                solver.u_[2] = 1j * (
                    solver.K_over_K2[1] * derivative
                    - solver.K_over_K2[0] * solver.g_
                )
                if comm.rank == 0:
                    solver.u_[1, :, 0, 0] = zero_stream
                    solver.u_[2, :, 0, 0] = zero_span

                eta_from_velocity = (
                    1j * solver.K[1] * solver.u_[2]
                    - 1j * solver.K[2] * solver.u_[1]
                )
                require_global_finite(
                    comm,
                    eta_from_velocity,
                    f"eta reconstructed from velocity sample {sample_index}",
                )
                local_eta_error = float(np.max(np.abs(eta_from_velocity - solver.g_)))
                max_eta_consistency = max(
                    max_eta_consistency,
                    global_max(comm, local_eta_error),
                )

                reconstructed = solver.u_.backward(mesh="quadrature")
                divergence = solver.divu().backward()
                require_global_finite(
                    comm,
                    divergence,
                    f"divergence sample {sample_index}",
                )
                max_divergence = max(
                    max_divergence,
                    global_max(comm, float(np.max(np.abs(divergence)))),
                )

                for component, group in enumerate(component_groups):
                    physical_slice = tuple(reconstructed[component].local_slice())
                    reference = velocity[f"{group}/3D/{key}"][physical_slice]
                    candidate = np.asarray(reconstructed[component])
                    require_global_finite(
                        comm,
                        reference,
                        f"reference {group} sample {sample_index}",
                    )
                    require_global_finite(
                        comm,
                        candidate,
                        f"reconstructed {group} sample {sample_index}",
                    )
                    if reference.shape != candidate.shape:
                        raise ValueError(
                            f"local shape mismatch for {group}/{key}: "
                            f"{reference.shape} != {candidate.shape}"
                        )
                    local_abs = float(np.max(np.abs(candidate - reference)))
                    global_abs = global_max(comm, local_abs)
                    reference_scale = global_max(
                        comm,
                        float(np.max(np.abs(reference))),
                    )
                    global_rel = global_abs / max(reference_scale, np.finfo(np.float64).tiny)
                    max_abs[component] = max(max_abs[component], global_abs)
                    max_rel[component] = max(max_rel[component], global_rel)

        passed = bool(
            np.all(max_abs <= args.absolute_tolerance)
            and np.all(max_rel <= args.relative_tolerance)
        )
        report = {
            "material_passport": {
                "origin_skill": "experiment-agent",
                "origin_mode": "validate",
                "origin_date": "2026-07-24",
                "verification_status": "VERIFIED" if passed else "ANALYZED",
                "version_label": "mkm_state_roundtrip_v1",
            },
            "status": "PASS" if passed else "FAIL",
            "state_h5": str(state_path),
            "velocity_h5": str(velocity_path),
            "schema_version": schema,
            "mpi_size": comm.size,
            "global_shape_physical": N,
            "wall_planes_checked": N[0],
            "samples_checked": count,
            "first_tstep": int(tsteps[0]),
            "last_tstep": int(tsteps[-1]),
            "first_time": float(times[0]),
            "last_time": float(times[-1]),
            "absolute_tolerance": args.absolute_tolerance,
            "relative_tolerance": args.relative_tolerance,
            "component_order": component_names,
            "max_absolute_error": {
                name: float(max_abs[index]) for index, name in enumerate(component_names)
            },
            "max_relative_error": {
                name: float(max_rel[index]) for index, name in enumerate(component_names)
            },
            "max_eta_consistency_error": max_eta_consistency,
            "max_divergence": max_divergence,
        }

    if comm.rank == 0:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as stream:
            json.dump(report, stream, indent=2)
        print(json.dumps(report, indent=2), flush=True)
        print(f"roundtrip_json={output_path}", flush=True)
    cleanup(vars(solver))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
