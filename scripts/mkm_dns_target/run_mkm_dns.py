#!/usr/bin/env python
"""Run the MKM channel-flow demo with reproducible command-line settings."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
from time import time


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True, help="Directory for HDF5/XDMF/checkpoint output.")
    parser.add_argument("--filename", default="MKM_dns", help="Filename prefix, without _U.h5 suffix.")
    parser.add_argument("--n", nargs=3, type=int, default=(64, 64, 32), metavar=("NZ", "NX", "NY"),
                        help="Grid shape in solver order: wall-normal, streamwise, spanwise.")
    parser.add_argument("--domain", nargs=6, type=float,
                        default=(-1.0, 1.0, 0.0, 2.0 * 3.141592653589793, 0.0, 3.141592653589793),
                        metavar=("Z0", "Z1", "X0", "X1", "Y0", "Y1"),
                        help="Domain in solver order.")
    parser.add_argument("--re", type=float, default=180.0, help="Friction Reynolds number used by MKM.")
    parser.add_argument("--dt", type=float, default=0.0005, help="Time step.")
    parser.add_argument("--end-time", type=float, required=True, help="End time for this run.")
    parser.add_argument("--conv", type=int, choices=(0, 1), default=0, help="Convection form passed to MKM.")
    parser.add_argument("--family", default="C", help="Wall-normal polynomial family.")
    parser.add_argument("--padding-factor", nargs=3, type=float, default=(1.5, 1.5, 1.5),
                        metavar=("PZ", "PX", "PY"))
    parser.add_argument("--timestepper", default="IMEXRK222", help="Shenfun timestepper class name.")
    parser.add_argument("--modplot", type=int, default=-1, help="Plot cadence. Use -1 for no plotting.")
    parser.add_argument("--modsave", type=int, default=1000, help="Snapshot cadence in time steps.")
    parser.add_argument("--moderror", type=int, default=100, help="Diagnostic print cadence. Use -1 to disable.")
    parser.add_argument("--checkpoint", type=int, default=1000, help="Checkpoint cadence in time steps.")
    parser.add_argument("--save-mesh", choices=("quadrature", "uniform"), default="quadrature",
                        help="Wall-normal mesh used for saved HDF5 snapshots.")
    parser.add_argument("--velocity-file-mode", choices=("w", "a"), default="w",
                        help="HDF5 mode for velocity snapshots. Use 'a' to append a restarted sampling segment.")
    parser.add_argument("--from-checkpoint", action="store_true", help="Restart from existing checkpoint.")
    parser.add_argument("--stage-label", default="single", choices=("single", "spinup", "sampling"),
                        help="Label written to run metadata for staged DNS workflows.")
    parser.add_argument("--disable-snapshots", action="store_true",
                        help="Do not write velocity snapshots. Use this for spin-up/development runs.")
    parser.add_argument("--force-final-checkpoint", action="store_true",
                        help="Write a restart checkpoint at the final state even if the checkpoint cadence is not hit.")
    parser.add_argument("--skip-xdmf", action="store_true", help="Do not generate XDMF sidecar.")
    return parser.parse_args()


def expected_final_time_step(t: float, tstep: int, dt: float, end_time: float) -> tuple[float, int]:
    while t < end_time - 1e-8:
        t += dt
        tstep += 1
    return t, tstep


def write_final_checkpoint(solver, t: float, tstep: int) -> None:
    solver.checkpoint.open(mode="w")
    for key, val in solver.checkpoint.data.items():
        solver.checkpoint.write(int(key), val)
    solver.checkpoint.f.attrs["tstep"] = tstep
    solver.checkpoint.f.attrs["t"] = t
    solver.checkpoint.close()


class DeferredVelocityFile:
    def write(self, *args, **kwargs):
        raise RuntimeError("velocity file was used before the runner installed the selected output file")


def main() -> int:
    args = parse_args()
    if args.modsave <= 0:
        raise ValueError("--modsave must be positive; Shenfun uses modulo arithmetic.")
    if args.checkpoint <= 0:
        raise ValueError("--checkpoint must be positive; Shenfun uses modulo arithmetic.")
    if args.moderror == 0:
        raise ValueError("--moderror=0 triggers a modulo-by-zero in demo/MKM.py; use -1 to disable.")

    os.environ.setdefault("MPLBACKEND", "Agg")
    repo = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(repo))
    sys.path.insert(0, str(repo / "demo"))

    from mpi4py import MPI
    from mpi4py_fft import generate_xdmf
    from MKM import MKM
    import ChannelFlow
    from shenfun import ShenfunFile, cleanup

    comm = MPI.COMM_WORLD
    output_dir = Path(args.output_dir).expanduser().resolve()
    if comm.rank == 0:
        output_dir.mkdir(parents=True, exist_ok=True)
    comm.Barrier()
    os.chdir(output_dir)

    domain = ((args.domain[0], args.domain[1]),
              (args.domain[2], args.domain[3]),
              (args.domain[4], args.domain[5]))
    case = {
        "N": tuple(args.n),
        "domain": domain,
        "Re": args.re,
        "dt": args.dt,
        "conv": args.conv,
        "modplot": args.modplot,
        "modsave": args.modsave,
        "moderror": args.moderror,
        "filename": args.filename,
        "family": args.family,
        "padding_factor": tuple(args.padding_factor),
        "checkpoint": args.checkpoint,
        "timestepper": args.timestepper,
    }
    if comm.rank == 0:
        config_stem = f"{args.filename}_run_config"
        if args.stage_label != "single":
            config_stem = f"{args.filename}_{args.stage_label}_run_config"
        with open(output_dir / f"{config_stem}.json", "w", encoding="utf-8") as f:
            json.dump({**case, "domain": domain, "end_time": args.end_time,
                       "from_checkpoint": args.from_checkpoint, "mpi_size": comm.size,
                       "save_mesh": args.save_mesh, "stage_label": args.stage_label,
                       "velocity_file_mode": args.velocity_file_mode,
                       "disable_snapshots": args.disable_snapshots,
                       "force_final_checkpoint": args.force_final_checkpoint}, f, indent=2)
        print("MKM run configuration:")
        print(json.dumps({**case, "domain": domain, "end_time": args.end_time,
                          "from_checkpoint": args.from_checkpoint, "mpi_size": comm.size,
                          "save_mesh": args.save_mesh, "stage_label": args.stage_label,
                          "velocity_file_mode": args.velocity_file_mode,
                          "disable_snapshots": args.disable_snapshots,
                          "force_final_checkpoint": args.force_final_checkpoint}, indent=2),
              flush=True)

    original_channel_shenfun_file = None
    if args.velocity_file_mode == "a" and not args.disable_snapshots:
        original_channel_shenfun_file = ChannelFlow.ShenfunFile
        ChannelFlow.ShenfunFile = lambda *unused_args, **unused_kwargs: DeferredVelocityFile()
    try:
        solver = MKM(**case)
    finally:
        if original_channel_shenfun_file is not None:
            ChannelFlow.ShenfunFile = original_channel_shenfun_file
    if args.disable_snapshots:
        solver.tofile = lambda tstep: None
    else:
        solver.file_u = ShenfunFile("_".join((args.filename, "U")), solver.BD,
                                    backend="hdf5", mode=args.velocity_file_mode, mesh=args.save_mesh)

        def tofile_with_selected_mesh(tstep):
            solver.file_u.write(
                tstep,
                {"u": [solver.u_.backward(mesh=args.save_mesh)]},
                as_scalar=True,
            )

        solver.tofile = tofile_with_selected_mesh

    t, tstep = solver.initialize(from_checkpoint=args.from_checkpoint)
    final_t, final_tstep = expected_final_time_step(t, tstep, args.dt, args.end_time)
    start = time()
    solver.solve(t=t, tstep=tstep, end_time=args.end_time)
    elapsed = time() - start
    if args.force_final_checkpoint:
        write_final_checkpoint(solver, final_t, final_tstep)

    if comm.rank == 0:
        velocity_h5 = "_".join((args.filename, "U")) + ".h5"
        print(f"elapsed={elapsed:.6f}", flush=True)
        print(f"final_t={final_t:.12g}", flush=True)
        print(f"final_tstep={final_tstep}", flush=True)
        if args.force_final_checkpoint:
            print(f"checkpoint_h5={output_dir / (args.filename + '.chk.h5')}", flush=True)
        print(f"velocity_h5={output_dir / velocity_h5}", flush=True)
        if not args.disable_snapshots and not args.skip_xdmf:
            generate_xdmf(velocity_h5)
            print(f"velocity_xdmf={output_dir / velocity_h5.replace('.h5', '.xdmf')}", flush=True)

    cleanup(vars(solver))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
