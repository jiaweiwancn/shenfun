#!/usr/bin/env python
"""Run a selected-mode MKM channel-resolvent proof-of-concept workflow."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import h5py
import numpy as np

from compute_mkm_channel_resolvent import compute_single_mode_resolvent
from compute_mkm_modal_csd import compute_modal_csd
from plot_mkm_channel_resolvent import FIGURE_NAMES, plot_all
from project_mkm_dns_onto_resolvent import project_dns_onto_resolvent


MANIFEST_NAME = "MKM_channel_resolvent_selected_modes_manifest.json"
SHARED_CSD_NAME = "MKM_channel_modal_csd_selected_modes.h5"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target-h5", required=True, help="Input target HDF5 file.")
    parser.add_argument("--constraint-file", required=True, help="Matching constraint HDF5 file.")
    parser.add_argument("--output-dir", required=True, help="Output directory for workflow products.")
    parser.add_argument(
        "--mode-index-list",
        nargs="+",
        type=int,
        required=True,
        metavar=("I", "J"),
        help="Selected mode-index pairs: I J [I J ...].",
    )

    parser.add_argument("--omega", nargs="+", type=float, help="Explicit angular frequencies.")
    parser.add_argument("--omega-from-csd", help="Read frequency bins from an existing CSD HDF5.")
    parser.add_argument(
        "--omega-count",
        type=int,
        default=4,
        help="Number of positive low-frequency CSD bins to use when omega is selected from a CSD.",
    )
    parser.add_argument("--phase-speed", nargs="+", type=float, help="Phase speeds c; omega=kappa*c per mode.")

    parser.add_argument("--n-singular", type=int, default=6)
    parser.add_argument("--re-tau", type=float, default=180.0)
    parser.add_argument("--overwrite", action="store_true", help="Replace workflow HDF5/JSON outputs.")

    csd_group = parser.add_mutually_exclusive_group()
    csd_group.add_argument("--compute-csd-from-target", action="store_true", help="Compute CSD from target modal/u_hat.")
    csd_group.add_argument("--compute-csd-from-velocity", help="Compute selected modes from raw velocity snapshots.")
    csd_group.add_argument("--existing-csd", help="Use an existing selected-mode CSD HDF5.")

    parser.add_argument("--segment-length", type=int)
    parser.add_argument("--overlap", type=float, default=0.5)
    parser.add_argument("--window", choices=("none", "hann"), default="hann")
    parser.add_argument("--demean-temporal", action="store_true")
    parser.add_argument("--dt", type=float)
    parser.add_argument("--t-min", type=float)
    parser.add_argument("--t-max", type=float)
    parser.add_argument("--skip-snapshots", type=int, default=0)
    parser.add_argument("--snapshot-stride", type=int, default=1)
    parser.add_argument("--max-snapshots", type=int)

    parser.add_argument("--skip-projection", action="store_true")
    parser.add_argument("--frequency-tolerance", type=float, default=1e-10)

    parser.add_argument("--make-figures", action="store_true")
    parser.add_argument("--no-tex", action="store_true")
    parser.add_argument("--skip-plots", action="store_true")
    return parser.parse_args()


def parse_mode_index_list(values: list[int]) -> np.ndarray:
    if len(values) % 2:
        raise ValueError("--mode-index-list must contain an even number of integers")
    modes = np.asarray(values, dtype=np.int32).reshape(-1, 2)
    if modes.shape[0] == 0:
        raise ValueError("at least one mode index is required")
    return modes


def path_for_mode(output_dir: Path, stem: str, mode: np.ndarray) -> Path:
    i, j = (int(mode[0]), int(mode[1]))
    return output_dir / f"{stem}_i{i}_j{j}.h5"


def figures_dir_for_mode(output_dir: Path, mode: np.ndarray) -> Path:
    i, j = (int(mode[0]), int(mode[1]))
    return output_dir / f"figures_i{i}_j{j}"


def load_wavenumbers(target_h5: Path, constraint_file: Path) -> tuple[np.ndarray, np.ndarray]:
    for path in (target_h5, constraint_file):
        with h5py.File(path, "r") as f:
            if "geometry/k_stream" in f and "geometry/k_span" in f:
                return f["geometry/k_stream"][:], f["geometry/k_span"][:]
            if "wavenumbers/k_stream" in f and "wavenumbers/k_span" in f:
                return f["wavenumbers/k_stream"][:], f["wavenumbers/k_span"][:]
    raise KeyError("could not find k_stream/k_span arrays in target or constraint files")


def validate_modes(modes: np.ndarray, k_stream: np.ndarray, k_span: np.ndarray) -> None:
    for mode in modes:
        i, j = (int(mode[0]), int(mode[1]))
        if i < 0 or i >= k_stream.size:
            raise IndexError(f"streamwise mode index {i} is outside [0, {k_stream.size})")
        if j < 0 or j >= k_span.size:
            raise IndexError(f"spanwise mode index {j} is outside [0, {k_span.size})")


def load_csd_omega(csd_h5: Path) -> np.ndarray:
    with h5py.File(csd_h5, "r") as f:
        return np.asarray(f["frequencies/omega"][:], dtype=float)


def select_positive_low_frequency_bins(omega_grid: np.ndarray, count: int) -> np.ndarray:
    if count <= 0:
        raise ValueError("--omega-count must be positive")
    finite_positive = omega_grid[np.isfinite(omega_grid) & (omega_grid > 0.0)]
    if finite_positive.size:
        selected = np.sort(finite_positive)[:count]
    else:
        finite = omega_grid[np.isfinite(omega_grid)]
        if finite.size == 0:
            raise ValueError("CSD frequency grid has no finite values")
        selected = finite[np.argsort(np.abs(finite))[:count]]
    if selected.size == 0:
        raise ValueError("no CSD frequencies were selected")
    return np.asarray(selected, dtype=float)


def snap_to_csd_bins(requested: np.ndarray, omega_grid: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    snapped = np.empty(requested.size, dtype=float)
    errors = np.empty(requested.size, dtype=float)
    for index, value in enumerate(requested):
        nearest = int(np.argmin(np.abs(omega_grid - value)))
        snapped[index] = omega_grid[nearest]
        errors[index] = abs(omega_grid[nearest] - value)
    unique_indices = np.sort(np.unique([int(np.argmin(np.abs(omega_grid - value))) for value in snapped]))
    return omega_grid[unique_indices], errors


def omega_for_mode(
    mode: np.ndarray,
    k_stream: np.ndarray,
    args: argparse.Namespace,
    csd_for_frequency: Path | None,
) -> tuple[np.ndarray, dict[str, Any]]:
    i = int(mode[0])
    omega_grid = load_csd_omega(csd_for_frequency) if csd_for_frequency is not None else None
    selection: dict[str, Any] = {}

    if args.omega is not None:
        requested = np.asarray(args.omega, dtype=float)
        if omega_grid is not None and args.omega_from_csd is not None:
            selected, errors = snap_to_csd_bins(requested, omega_grid)
            selection = {
                "kind": "explicit_omega_snapped_to_csd",
                "requested": requested.tolist(),
                "snap_errors": errors.tolist(),
                "source_csd": str(csd_for_frequency),
            }
            return selected, selection
        selection = {"kind": "explicit_omega", "requested": requested.tolist()}
        return requested, selection

    if args.phase_speed is not None:
        phase_speed = np.asarray(args.phase_speed, dtype=float)
        requested = float(k_stream[i]) * phase_speed
        if omega_grid is not None and args.omega_from_csd is not None:
            selected, errors = snap_to_csd_bins(requested, omega_grid)
            selection = {
                "kind": "phase_speed_snapped_to_csd",
                "phase_speed": phase_speed.tolist(),
                "requested": requested.tolist(),
                "snap_errors": errors.tolist(),
                "source_csd": str(csd_for_frequency),
            }
            return selected, selection
        selection = {"kind": "phase_speed", "phase_speed": phase_speed.tolist()}
        return requested, selection

    if omega_grid is None:
        raise ValueError(
            "provide --omega, --phase-speed, --omega-from-csd, or a CSD source "
            "from which positive low-frequency bins can be selected"
        )
    selected = select_positive_low_frequency_bins(omega_grid, args.omega_count)
    selection = {
        "kind": "positive_low_frequency_csd_bins",
        "omega_count": int(args.omega_count),
        "source_csd": str(csd_for_frequency),
    }
    return selected, selection


def summarize_resolvent(path: Path) -> dict[str, Any]:
    with h5py.File(path, "r") as f:
        singular_values = f["resolvent/singular_values"][:]
        return {
            "leading_singular_values": singular_values[:, 0].tolist(),
            "singular_values_shape": list(singular_values.shape),
            "max_response_constraint_residual": float(np.max(f["diagnostics/constraint_residual_response"][:])),
            "max_forcing_constraint_residual": float(np.max(f["diagnostics/constraint_residual_forcing"][:])),
            "max_response_energy_norm_error": float(np.max(f["diagnostics/response_energy_norm_error"][:])),
            "max_forcing_energy_norm_error": float(np.max(f["diagnostics/forcing_energy_norm_error"][:])),
        }


def summarize_projection(path: Path) -> dict[str, Any]:
    with h5py.File(path, "r") as f:
        return {
            "leading_energy_fraction": f["projection/energy_fraction"][:, 0].tolist(),
            "final_cumulative_energy_fraction": f["projection/cumulative_energy_fraction"][:, -1].tolist(),
            "energy_total": f["projection/energy_total"][:].tolist(),
            "max_frequency_match_error": float(np.max(f["diagnostics/frequency_match_error"][:])),
            "mode_match_error": float(f["diagnostics/mode_match_error"][()]),
            "negative_fraction_count": int(f["diagnostics/negative_fraction_count"][()]),
        }


def existing_output_guard(paths: list[Path], overwrite: bool) -> None:
    if overwrite:
        return
    existing = [path for path in paths if path.exists()]
    if existing:
        formatted = "\n".join(f"  {path}" for path in existing)
        raise FileExistsError(f"workflow outputs already exist; pass --overwrite to replace them:\n{formatted}")


def determine_csd_path(args: argparse.Namespace, output_dir: Path) -> tuple[Path | None, str]:
    if args.existing_csd is not None:
        return Path(args.existing_csd).expanduser().resolve(), "existing_csd"
    if args.compute_csd_from_target or args.compute_csd_from_velocity is not None:
        return (output_dir / SHARED_CSD_NAME).resolve(), "computed_csd"
    if args.omega_from_csd is not None:
        return Path(args.omega_from_csd).expanduser().resolve(), "omega_from_csd_only"
    return None, "none"


def run_selected_modes_workflow(args: argparse.Namespace) -> dict[str, Any]:
    target_h5 = Path(args.target_h5).expanduser().resolve()
    constraint_file = Path(args.constraint_file).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    modes = parse_mode_index_list(args.mode_index_list)
    k_stream, k_span = load_wavenumbers(target_h5, constraint_file)
    validate_modes(modes, k_stream, k_span)

    if args.omega is not None and args.phase_speed is not None:
        raise ValueError("use either --omega or --phase-speed, not both")
    if args.skip_plots:
        make_plots = False
    else:
        make_plots = bool(args.make_figures)

    csd_path, csd_mode = determine_csd_path(args, output_dir)
    omega_frequency_source = Path(args.omega_from_csd).expanduser().resolve() if args.omega_from_csd else csd_path

    planned_outputs = [output_dir / MANIFEST_NAME]
    if csd_mode == "computed_csd" and csd_path is not None:
        planned_outputs.append(csd_path)
    for mode in modes:
        planned_outputs.append(path_for_mode(output_dir, "MKM_channel_resolvent", mode))
        if csd_path is not None and not args.skip_projection:
            planned_outputs.append(path_for_mode(output_dir, "MKM_channel_resolvent_projection", mode))
    existing_output_guard(planned_outputs, args.overwrite)

    manifest: dict[str, Any] = {
        "description": "Selected-mode MKM channel-resolvent proof-of-concept workflow.",
        "target_h5": str(target_h5),
        "constraint_file": str(constraint_file),
        "output_dir": str(output_dir),
        "selected_modes": modes.astype(int).tolist(),
        "n_singular": int(args.n_singular),
        "re_tau": float(args.re_tau),
        "csd": None,
        "modes": [],
    }

    if csd_mode == "computed_csd" and csd_path is not None:
        csd_result = compute_modal_csd(
            output=csd_path,
            target_h5=target_h5,
            velocity_h5=args.compute_csd_from_velocity,
            mode_index_list=modes,
            dt=args.dt,
            t_min=args.t_min,
            t_max=args.t_max,
            skip_snapshots=args.skip_snapshots,
            snapshot_stride=args.snapshot_stride,
            max_snapshots=args.max_snapshots,
            segment_length=args.segment_length,
            overlap=args.overlap,
            window=args.window,
            demean_temporal=args.demean_temporal,
            overwrite=True,
        )
        manifest["csd"] = {
            "mode": csd_mode,
            "path": str(csd_path),
            "summary": csd_result,
        }
        if omega_frequency_source is None:
            omega_frequency_source = csd_path
    elif csd_path is not None:
        manifest["csd"] = {
            "mode": csd_mode,
            "path": str(csd_path),
        }

    for mode in modes:
        mode_tuple = (int(mode[0]), int(mode[1]))
        omega, omega_selection = omega_for_mode(mode, k_stream, args, omega_frequency_source)
        if omega.size == 0:
            raise ValueError(f"no omega values selected for mode {mode_tuple}")

        resolvent_path = path_for_mode(output_dir, "MKM_channel_resolvent", mode)
        result = compute_single_mode_resolvent(
            target_h5,
            constraint_file,
            resolvent_path,
            mode_tuple,
            omega,
            args.n_singular,
            re_tau=args.re_tau,
            overwrite=True,
        )
        mode_entry: dict[str, Any] = {
            "mode_index": [mode_tuple[0], mode_tuple[1]],
            "kappa": float(k_stream[mode_tuple[0]]),
            "lambda": float(k_span[mode_tuple[1]]),
            "omega": omega.tolist(),
            "omega_selection": omega_selection,
            "resolvent_h5": str(resolvent_path),
            "resolvent_summary": summarize_resolvent(resolvent_path),
            "compute_resolvent_summary": result,
            "projection_h5": None,
            "projection_summary": None,
            "figure_dir": None,
            "figures": [],
        }

        if csd_path is not None and not args.skip_projection:
            projection_path = path_for_mode(output_dir, "MKM_channel_resolvent_projection", mode)
            project_dns_onto_resolvent(
                resolvent_h5=resolvent_path,
                csd_h5=csd_path,
                output=projection_path,
                max_rank=args.n_singular,
                frequency_tolerance=args.frequency_tolerance,
                overwrite=True,
            )
            mode_entry["projection_h5"] = str(projection_path)
            mode_entry["projection_summary"] = summarize_projection(projection_path)

        if make_plots:
            figure_dir = figures_dir_for_mode(output_dir, mode)
            figure_paths = plot_all(
                resolvent_path,
                figure_dir,
                omega_index=0,
                singular_index=0,
                n_shapes=min(3, args.n_singular),
                phase=0.0,
                n_stream=128,
                n_span=128,
                no_tex=args.no_tex,
            )
            mode_entry["figure_dir"] = str(figure_dir)
            mode_entry["figures"] = [str(path) for path in figure_paths]

        manifest["modes"].append(mode_entry)

    manifest_path = output_dir / MANIFEST_NAME
    manifest["manifest_path"] = str(manifest_path)
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    return manifest


def main() -> int:
    args = parse_args()
    manifest = run_selected_modes_workflow(args)
    print(f"wrote_manifest={manifest['manifest_path']}")
    if manifest["csd"] is not None:
        print(f"csd_h5={manifest['csd']['path']}")
    for entry in manifest["modes"]:
        mode = tuple(entry["mode_index"])
        print(f"mode={mode} resolvent_h5={entry['resolvent_h5']}")
        if entry["projection_h5"] is not None:
            print(f"mode={mode} projection_h5={entry['projection_h5']}")
        if entry["figure_dir"] is not None:
            print(f"mode={mode} figure_dir={entry['figure_dir']}")
        leading = entry["resolvent_summary"]["leading_singular_values"]
        print(f"mode={mode} leading_singular_values={leading}")
        if entry["projection_summary"] is not None:
            fractions = entry["projection_summary"]["leading_energy_fraction"]
            print(f"mode={mode} leading_projection_fraction={fractions}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
