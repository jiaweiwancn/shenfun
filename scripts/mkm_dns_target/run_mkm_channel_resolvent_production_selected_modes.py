#!/usr/bin/env python
"""Run the selected-mode channel-resolvent workflow on production MKM files."""

from __future__ import annotations

import argparse
import shlex
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import numpy as np

from run_mkm_channel_resolvent_selected_modes import (
    MANIFEST_NAME,
    SHARED_CSD_NAME,
    run_selected_modes_workflow,
)


SERVER = "jay@100.88.70.60"
SERVER_REPO = Path("/media/jay/data1/shenfun")
SERVER_ENV_PYTHON = Path("/media/jay/data1/conda_envs/shenfun_dns_np126_20260702/bin/python")
PRODUCTION_DIR = Path("/media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702")
DENSE_DIR = Path("/media/jay/data1/shenfun_dns_runs/dense_temporal_mkm_64_64_32_t180_t300_20260703")
DEFAULT_TARGET = PRODUCTION_DIR / "MKM_production_64_64_32_target_t60_t180.h5"
DEFAULT_CONSTRAINT = PRODUCTION_DIR / "MKM_constraints_N64_64_32_cheb_quadrature_spectral.h5"
DEFAULT_DENSE_VELOCITY = DENSE_DIR / "MKM_dense_temporal_64_64_32_t180_t300_U.h5"
DEFAULT_OUTPUT_DIR = PRODUCTION_DIR / "channel_resolvent_selected_modes"
DEFAULT_MODE_INDEX_LIST = (1, 0, 1, 1, 2, 1)
DEFAULT_RE_TAU = 180.0
DEFAULT_N_SINGULAR = 6
DEFAULT_OMEGA_COUNT = 4
DEFAULT_DENSE_DT = 0.0005
DEFAULT_DENSE_T_MIN = 180.0
DEFAULT_DENSE_T_MAX = 300.0
DEFAULT_TARGET_SEGMENT_LENGTH = 512
DEFAULT_DENSE_SEGMENT_LENGTH = 2048


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target-h5", default=str(DEFAULT_TARGET), help="Production target HDF5 file.")
    parser.add_argument("--constraint-file", default=str(DEFAULT_CONSTRAINT), help="Matching constraint HDF5 file.")
    parser.add_argument("--dense-velocity-h5", default=str(DEFAULT_DENSE_VELOCITY), help="Dense temporal raw velocity HDF5 file.")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Output directory for workflow products.")
    parser.add_argument(
        "--mode-index-list",
        nargs="+",
        type=int,
        default=list(DEFAULT_MODE_INDEX_LIST),
        metavar=("I", "J"),
        help="Selected mode-index pairs: I J [I J ...].",
    )

    parser.add_argument("--omega", nargs="+", type=float, help="Explicit angular frequencies; snapped to CSD bins when a CSD is used.")
    parser.add_argument("--phase-speed", nargs="+", type=float, help="Phase speeds c; omega=kappa*c per mode, snapped to CSD bins when a CSD is used.")
    parser.add_argument("--omega-count", type=int, default=DEFAULT_OMEGA_COUNT, help="Positive low-frequency CSD bins to use when omega is not explicit.")
    parser.add_argument("--n-singular", type=int, default=DEFAULT_N_SINGULAR)
    parser.add_argument("--re-tau", type=float, default=DEFAULT_RE_TAU)

    parser.add_argument("--csd-source", choices=("target", "dense"), default="target", help="Source used when computing the shared selected-mode CSD.")
    parser.add_argument("--existing-csd", help="Use an existing selected-mode CSD HDF5 instead of computing one.")
    parser.add_argument("--dt", type=float, help=f"Dense raw snapshot time step. Default: {DEFAULT_DENSE_DT:g} for --csd-source dense.")
    parser.add_argument("--t-min", type=float, help=f"Dense raw snapshot lower time bound. Default: {DEFAULT_DENSE_T_MIN:g} for --csd-source dense.")
    parser.add_argument("--t-max", type=float, help=f"Dense raw snapshot upper time bound. Default: {DEFAULT_DENSE_T_MAX:g} for --csd-source dense.")
    parser.add_argument("--segment-length", type=int, help="CSD segment length. Default: 512 for target, 2048 for dense.")
    parser.add_argument("--overlap", type=float, default=0.5)
    parser.add_argument("--window", choices=("none", "hann"), default="hann")
    parser.add_argument("--demean-temporal", action="store_true")
    parser.add_argument("--skip-snapshots", type=int, default=0)
    parser.add_argument("--snapshot-stride", type=int, default=1)
    parser.add_argument("--max-snapshots", type=int)

    parser.add_argument("--skip-projection", action="store_true")
    parser.add_argument("--frequency-tolerance", type=float, default=1e-10)
    parser.add_argument("--make-figures", action="store_true", default=True, help="Generate the Step 4 PDFs. Enabled by default.")
    parser.add_argument("--no-tex", action="store_true")
    parser.add_argument("--skip-plots", action="store_true")
    parser.add_argument("--overwrite", action="store_true", help="Replace existing workflow products.")

    parser.add_argument("--dry-run", action="store_true", help="Print resolved workflow configuration without running.")
    parser.add_argument("--print-ssh-command", action="store_true", help="Print a one-line SSH command for running on the Linux server.")
    return parser.parse_args()


def resolved_segment_length(args: argparse.Namespace) -> int:
    if args.segment_length is not None:
        return int(args.segment_length)
    if args.existing_csd is not None:
        return DEFAULT_TARGET_SEGMENT_LENGTH
    if args.csd_source == "dense":
        return DEFAULT_DENSE_SEGMENT_LENGTH
    return DEFAULT_TARGET_SEGMENT_LENGTH


def selected_workflow_args(args: argparse.Namespace) -> SimpleNamespace:
    output_dir = Path(args.output_dir).expanduser()
    existing_csd = Path(args.existing_csd).expanduser() if args.existing_csd else None
    computed_csd = output_dir / SHARED_CSD_NAME
    csd_for_snapping = existing_csd if existing_csd is not None else computed_csd
    should_snap_to_csd = (args.omega is not None or args.phase_speed is not None) and not args.skip_projection
    use_dense_source = args.existing_csd is None and args.csd_source == "dense"
    dt = args.dt if args.dt is not None else (DEFAULT_DENSE_DT if use_dense_source else None)
    t_min = args.t_min if args.t_min is not None else (DEFAULT_DENSE_T_MIN if use_dense_source else None)
    t_max = args.t_max if args.t_max is not None else (DEFAULT_DENSE_T_MAX if use_dense_source else None)

    return SimpleNamespace(
        target_h5=str(Path(args.target_h5).expanduser()),
        constraint_file=str(Path(args.constraint_file).expanduser()),
        output_dir=str(output_dir),
        mode_index_list=list(args.mode_index_list),
        omega=args.omega,
        omega_from_csd=str(csd_for_snapping) if should_snap_to_csd else None,
        omega_count=int(args.omega_count),
        phase_speed=args.phase_speed,
        n_singular=int(args.n_singular),
        re_tau=float(args.re_tau),
        overwrite=bool(args.overwrite),
        compute_csd_from_target=(args.existing_csd is None and args.csd_source == "target"),
        compute_csd_from_velocity=(
            str(Path(args.dense_velocity_h5).expanduser())
            if args.existing_csd is None and args.csd_source == "dense"
            else None
        ),
        existing_csd=str(existing_csd) if existing_csd is not None else None,
        segment_length=resolved_segment_length(args),
        overlap=float(args.overlap),
        window=args.window,
        demean_temporal=bool(args.demean_temporal),
        dt=float(dt) if dt is not None else None,
        t_min=float(t_min) if t_min is not None else None,
        t_max=float(t_max) if t_max is not None else None,
        skip_snapshots=int(args.skip_snapshots),
        snapshot_stride=int(args.snapshot_stride),
        max_snapshots=args.max_snapshots,
        skip_projection=bool(args.skip_projection),
        frequency_tolerance=float(args.frequency_tolerance),
        make_figures=bool(args.make_figures),
        no_tex=bool(args.no_tex),
        skip_plots=bool(args.skip_plots),
    )


def selected_workflow_command(workflow_args: SimpleNamespace) -> list[str]:
    command = [
        "scripts/mkm_dns_target/run_mkm_channel_resolvent_selected_modes.py",
        "--target-h5",
        str(workflow_args.target_h5),
        "--constraint-file",
        str(workflow_args.constraint_file),
        "--output-dir",
        str(workflow_args.output_dir),
        "--mode-index-list",
        *(str(value) for value in workflow_args.mode_index_list),
        "--omega-count",
        str(workflow_args.omega_count),
        "--n-singular",
        str(workflow_args.n_singular),
        "--re-tau",
        f"{workflow_args.re_tau:.12g}",
        "--segment-length",
        str(workflow_args.segment_length),
        "--overlap",
        f"{workflow_args.overlap:.12g}",
        "--window",
        str(workflow_args.window),
        "--frequency-tolerance",
        f"{workflow_args.frequency_tolerance:.12g}",
    ]
    if workflow_args.omega is not None:
        command.extend(["--omega", *(f"{value:.12g}" for value in workflow_args.omega)])
    if workflow_args.phase_speed is not None:
        command.extend(["--phase-speed", *(f"{value:.12g}" for value in workflow_args.phase_speed)])
    if workflow_args.omega_from_csd is not None:
        command.extend(["--omega-from-csd", str(workflow_args.omega_from_csd)])
    if workflow_args.compute_csd_from_target:
        command.append("--compute-csd-from-target")
    if workflow_args.compute_csd_from_velocity is not None:
        command.extend(["--compute-csd-from-velocity", str(workflow_args.compute_csd_from_velocity)])
    if workflow_args.existing_csd is not None:
        command.extend(["--existing-csd", str(workflow_args.existing_csd)])
    if workflow_args.compute_csd_from_velocity is not None:
        command.extend([
            "--dt",
            f"{workflow_args.dt:.12g}",
            "--t-min",
            f"{workflow_args.t_min:.12g}",
            "--t-max",
            f"{workflow_args.t_max:.12g}",
        ])
    if workflow_args.demean_temporal:
        command.append("--demean-temporal")
    if workflow_args.skip_snapshots:
        command.extend(["--skip-snapshots", str(workflow_args.skip_snapshots)])
    if workflow_args.snapshot_stride != 1:
        command.extend(["--snapshot-stride", str(workflow_args.snapshot_stride)])
    if workflow_args.max_snapshots is not None:
        command.extend(["--max-snapshots", str(workflow_args.max_snapshots)])
    if workflow_args.skip_projection:
        command.append("--skip-projection")
    if workflow_args.skip_plots:
        command.append("--skip-plots")
    elif workflow_args.make_figures:
        command.append("--make-figures")
    if workflow_args.no_tex:
        command.append("--no-tex")
    if workflow_args.overwrite:
        command.append("--overwrite")
    return command


def wrapper_command(args: argparse.Namespace) -> list[str]:
    command = [
        "scripts/mkm_dns_target/run_mkm_channel_resolvent_production_selected_modes.py",
        "--target-h5",
        str(Path(args.target_h5).expanduser()),
        "--constraint-file",
        str(Path(args.constraint_file).expanduser()),
        "--dense-velocity-h5",
        str(Path(args.dense_velocity_h5).expanduser()),
        "--output-dir",
        str(Path(args.output_dir).expanduser()),
        "--mode-index-list",
        *(str(value) for value in args.mode_index_list),
        "--csd-source",
        args.csd_source,
        "--omega-count",
        str(args.omega_count),
        "--n-singular",
        str(args.n_singular),
        "--re-tau",
        f"{args.re_tau:.12g}",
        "--segment-length",
        str(resolved_segment_length(args)),
        "--overlap",
        f"{args.overlap:.12g}",
        "--window",
        args.window,
        "--frequency-tolerance",
        f"{args.frequency_tolerance:.12g}",
    ]
    if args.existing_csd is not None:
        command.extend(["--existing-csd", str(Path(args.existing_csd).expanduser())])
    if args.omega is not None:
        command.extend(["--omega", *(f"{value:.12g}" for value in args.omega)])
    if args.phase_speed is not None:
        command.extend(["--phase-speed", *(f"{value:.12g}" for value in args.phase_speed)])
    if args.csd_source == "dense" and args.existing_csd is None:
        dt = args.dt if args.dt is not None else DEFAULT_DENSE_DT
        t_min = args.t_min if args.t_min is not None else DEFAULT_DENSE_T_MIN
        t_max = args.t_max if args.t_max is not None else DEFAULT_DENSE_T_MAX
        command.extend([
            "--dt",
            f"{dt:.12g}",
            "--t-min",
            f"{t_min:.12g}",
            "--t-max",
            f"{t_max:.12g}",
        ])
    if args.demean_temporal:
        command.append("--demean-temporal")
    if args.skip_snapshots:
        command.extend(["--skip-snapshots", str(args.skip_snapshots)])
    if args.snapshot_stride != 1:
        command.extend(["--snapshot-stride", str(args.snapshot_stride)])
    if args.max_snapshots is not None:
        command.extend(["--max-snapshots", str(args.max_snapshots)])
    if args.skip_projection:
        command.append("--skip-projection")
    if args.skip_plots:
        command.append("--skip-plots")
    elif args.make_figures:
        command.append("--make-figures")
    if args.no_tex:
        command.append("--no-tex")
    if args.overwrite:
        command.append("--overwrite")
    return command


def quoted_command(command: list[str]) -> str:
    return " ".join(shlex.quote(str(part)) for part in command)


def expected_ssh_command(args: argparse.Namespace) -> str:
    inner = f"cd {shlex.quote(str(SERVER_REPO))} && {quoted_command([SERVER_ENV_PYTHON, *wrapper_command(args)])}"
    return f"ssh {SERVER} {shlex.quote(inner)}"


def required_input_paths(args: argparse.Namespace) -> list[Path]:
    paths = [
        Path(args.target_h5).expanduser(),
        Path(args.constraint_file).expanduser(),
    ]
    if args.existing_csd is not None:
        paths.append(Path(args.existing_csd).expanduser())
    elif args.csd_source == "dense":
        paths.append(Path(args.dense_velocity_h5).expanduser())
    return paths


def missing_paths(args: argparse.Namespace) -> list[Path]:
    return [path for path in required_input_paths(args) if not path.exists()]


def print_resolved_config(args: argparse.Namespace, workflow_args: SimpleNamespace) -> None:
    print("Resolved selected-mode production workflow:")
    print(f"  target_h5={workflow_args.target_h5}")
    print(f"  constraint_file={workflow_args.constraint_file}")
    print(f"  output_dir={workflow_args.output_dir}")
    print(f"  mode_index_list={workflow_args.mode_index_list}")
    print(f"  csd_source={'existing' if workflow_args.existing_csd else args.csd_source}")
    if workflow_args.compute_csd_from_velocity is not None:
        print(f"  dense_velocity_h5={workflow_args.compute_csd_from_velocity}")
    if workflow_args.existing_csd is not None:
        print(f"  existing_csd={workflow_args.existing_csd}")
    print(f"  segment_length={workflow_args.segment_length}")
    print(f"  omega_count={workflow_args.omega_count}")
    print(f"  omega={workflow_args.omega}")
    print(f"  phase_speed={workflow_args.phase_speed}")
    print(f"  omega_from_csd={workflow_args.omega_from_csd}")
    print(f"  n_singular={workflow_args.n_singular}")
    print(f"  make_figures={workflow_args.make_figures and not workflow_args.skip_plots}")
    print(f"  manifest={Path(workflow_args.output_dir) / MANIFEST_NAME}")
    print()
    print("Equivalent selected-mode workflow command:")
    print(quoted_command([SERVER_ENV_PYTHON, *selected_workflow_command(workflow_args)]))


def print_missing_message(args: argparse.Namespace, missing: list[Path]) -> None:
    print("Production selected-mode workflow could not run because required HDF5 files are missing locally.")
    print("Missing paths:")
    for path in missing:
        print(f"  {path}")
    print()
    print("Recommended server command:")
    print(expected_ssh_command(args))


def print_manifest_summary(manifest: dict[str, Any]) -> None:
    print(f"wrote_manifest={manifest['manifest_path']}")
    if manifest.get("csd") is not None:
        print(f"csd_h5={manifest['csd']['path']}")
    print(f"n_modes={len(manifest['modes'])}")
    for entry in manifest["modes"]:
        mode = tuple(entry["mode_index"])
        leading = entry["resolvent_summary"]["leading_singular_values"]
        print(f"mode={mode} omega={entry['omega']}")
        print(f"mode={mode} resolvent_h5={entry['resolvent_h5']}")
        if entry["projection_h5"] is not None:
            print(f"mode={mode} projection_h5={entry['projection_h5']}")
        if entry["figure_dir"] is not None:
            print(f"mode={mode} figure_dir={entry['figure_dir']}")
        print(f"mode={mode} leading_singular_values={leading}")
        if entry["projection_summary"] is not None:
            fractions = entry["projection_summary"]["leading_energy_fraction"]
            print(f"mode={mode} leading_projection_fraction={fractions}")


def main() -> int:
    args = parse_args()
    if len(args.mode_index_list) % 2:
        print("--mode-index-list must contain an even number of integers")
        return 2
    if args.omega is not None and args.phase_speed is not None:
        print("use either --omega or --phase-speed, not both")
        return 2

    workflow_args = selected_workflow_args(args)
    if args.dry_run:
        print_resolved_config(args, workflow_args)
        if args.print_ssh_command:
            print()
            print("Recommended SSH command:")
            print(expected_ssh_command(args))
        return 0

    if args.print_ssh_command:
        print("Recommended SSH command:")
        print(expected_ssh_command(args))
        print()

    missing = missing_paths(args)
    if missing:
        print_missing_message(args, missing)
        return 2

    manifest = run_selected_modes_workflow(workflow_args)
    print_manifest_summary(manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
