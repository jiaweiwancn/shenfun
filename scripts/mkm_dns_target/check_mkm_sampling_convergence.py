#!/usr/bin/env python
"""Check block convergence of MKM stationary-stage sampled snapshots."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

import h5py
import numpy as np


COMPONENT_GROUPS = ("u1", "u2", "u0")
COMPONENT_NAMES = ("streamwise", "spanwise", "wallnormal")


def sorted_snapshot_keys(f: h5py.File) -> list[str]:
    keys = sorted(f["u0/3D"].keys(), key=lambda k: int(k))
    for group in ("u1", "u2"):
        other = sorted(f[f"{group}/3D"].keys(), key=lambda k: int(k))
        if other != keys:
            raise ValueError(f"snapshot keys differ between u0 and {group}")
    return keys


def select_keys(
    keys: list[str],
    skip: int,
    stride: int,
    max_snapshots: int | None,
    dt: float,
    t_min: float | None,
    t_max: float | None,
) -> list[str]:
    selected = []
    for key in keys:
        t = int(key) * dt
        if t_min is not None and t < t_min - 1e-12:
            continue
        if t_max is not None and t > t_max + 1e-12:
            continue
        selected.append(key)
    selected = selected[skip::stride]
    if max_snapshots is not None:
        selected = selected[:max_snapshots]
    if not selected:
        raise ValueError("no snapshots selected")
    return selected


def read_snapshot(f: h5py.File, key: str, mean_profile: np.ndarray | None = None) -> np.ndarray:
    fields = [f[f"{group}/3D/{key}"][:] for group in COMPONENT_GROUPS]
    data = np.stack(fields, axis=0)
    if mean_profile is not None:
        data = data - mean_profile[:, :, None, None]
    return data


def accumulate_mean_and_reynolds(f: h5py.File, keys: Iterable[str]) -> tuple[np.ndarray, np.ndarray]:
    keys = list(keys)
    first = read_snapshot(f, keys[0])
    ncomp, nz, _, _ = first.shape
    mean = np.zeros((ncomp, nz), dtype=float)
    for key in keys:
        mean += read_snapshot(f, key).mean(axis=(2, 3))
    mean /= len(keys)

    reynolds = np.zeros((nz, ncomp, ncomp), dtype=float)
    samples_per_snapshot = first.shape[2] * first.shape[3]
    for key in keys:
        fluct = read_snapshot(f, key, mean)
        for a in range(nz):
            values = fluct[:, a, :, :].reshape(ncomp, -1)
            reynolds[a] += values @ values.T
    reynolds /= samples_per_snapshot * len(keys)
    return mean, reynolds


def rel_norm(a: np.ndarray, b: np.ndarray) -> float:
    denom = np.linalg.norm(b.ravel())
    if denom == 0.0:
        denom = 1.0
    return float(np.linalg.norm((a - b).ravel()) / denom)


def block_key_sets(keys: list[str], n_blocks: int) -> list[list[str]]:
    n_blocks = min(max(1, n_blocks), len(keys))
    return [list(block) for block in np.array_split(np.array(keys, dtype=object), n_blocks) if len(block)]


def scalar_series(f: h5py.File, keys: list[str], dt: float) -> list[dict[str, object]]:
    series = []
    for key in keys:
        data = read_snapshot(f, key)
        component_mean = data.mean(axis=(1, 2, 3))
        component_energy = (data * data).mean(axis=(1, 2, 3))
        series.append({
            "key": key,
            "time": int(key) * dt,
            "component_mean": {
                name: float(component_mean[i]) for i, name in enumerate(COMPONENT_NAMES)
            },
            "component_energy": {
                name: float(component_energy[i]) for i, name in enumerate(COMPONENT_NAMES)
            },
            "total_unweighted_energy": float(np.sum(component_energy)),
        })
    return series


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--velocity-h5", required=True, help="Input stationary-stage MKM *_U.h5 file.")
    parser.add_argument("--dt", type=float, required=True, help="DNS time step.")
    parser.add_argument("--output", required=True, help="Output JSON convergence report.")
    parser.add_argument("--t-min", type=float, help="Minimum physical sample time to include.")
    parser.add_argument("--t-max", type=float, help="Maximum physical sample time to include.")
    parser.add_argument("--skip-snapshots", type=int, default=0)
    parser.add_argument("--snapshot-stride", type=int, default=1)
    parser.add_argument("--max-snapshots", type=int)
    parser.add_argument("--n-blocks", type=int, default=4)
    parser.add_argument("--tolerance", type=float, default=0.05,
                        help="Relative block-deviation tolerance for the boolean convergence flag.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    velocity_h5 = Path(args.velocity_h5).expanduser().resolve()
    output = Path(args.output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    with h5py.File(velocity_h5, "r") as f:
        keys = select_keys(
            sorted_snapshot_keys(f),
            skip=args.skip_snapshots,
            stride=args.snapshot_stride,
            max_snapshots=args.max_snapshots,
            dt=args.dt,
            t_min=args.t_min,
            t_max=args.t_max,
        )
        all_mean, all_reynolds = accumulate_mean_and_reynolds(f, keys)
        blocks = block_key_sets(keys, args.n_blocks)
        block_reports = []
        block_stats = []
        for block in blocks:
            mean, reynolds = accumulate_mean_and_reynolds(f, block)
            block_stats.append((mean, reynolds))
            block_reports.append({
                "n_snapshots": len(block),
                "first_key": block[0],
                "last_key": block[-1],
                "first_time": int(block[0]) * args.dt,
                "last_time": int(block[-1]) * args.dt,
                "mean_profile_rel_to_all": rel_norm(mean, all_mean),
                "reynolds_profile_rel_to_all": rel_norm(reynolds, all_reynolds),
            })

        successive = []
        for i in range(1, len(block_stats)):
            mean_prev, reynolds_prev = block_stats[i - 1]
            mean_curr, reynolds_curr = block_stats[i]
            successive.append({
                "from_block": i - 1,
                "to_block": i,
                "mean_profile_rel_change": rel_norm(mean_curr, mean_prev),
                "reynolds_profile_rel_change": rel_norm(reynolds_curr, reynolds_prev),
            })

        first_second = None
        if len(keys) >= 2:
            midpoint = len(keys) // 2
            first_half = keys[:midpoint]
            second_half = keys[midpoint:]
            mean_first, reynolds_first = accumulate_mean_and_reynolds(f, first_half)
            mean_second, reynolds_second = accumulate_mean_and_reynolds(f, second_half)
            first_second = {
                "first_half_n_snapshots": len(first_half),
                "second_half_n_snapshots": len(second_half),
                "mean_profile_rel_change": rel_norm(mean_second, mean_first),
                "reynolds_profile_rel_change": rel_norm(reynolds_second, reynolds_first),
            }

        max_mean_block_rel = max(report["mean_profile_rel_to_all"] for report in block_reports)
        max_reynolds_block_rel = max(report["reynolds_profile_rel_to_all"] for report in block_reports)
        enough_blocks = len(blocks) >= 2 and all(len(block) >= 1 for block in blocks)
        converged_by_tolerance = bool(
            enough_blocks
            and max_mean_block_rel <= args.tolerance
            and max_reynolds_block_rel <= args.tolerance
        )

        report = {
            "source_velocity_h5": str(velocity_h5),
            "dt": args.dt,
            "selected_snapshot_keys": keys,
            "n_snapshots": len(keys),
            "sample_time_range": [int(keys[0]) * args.dt, int(keys[-1]) * args.dt],
            "selection": {
                "t_min": args.t_min,
                "t_max": args.t_max,
                "skip_snapshots": args.skip_snapshots,
                "snapshot_stride": args.snapshot_stride,
                "max_snapshots": args.max_snapshots,
            },
            "component_order": COMPONENT_NAMES,
            "diagnostic_kind": "block convergence of stationary-stage samples",
            "note": "A short pilot can exercise the workflow, but production stationarity requires a much longer physical window.",
            "n_blocks_requested": args.n_blocks,
            "n_blocks_used": len(blocks),
            "blocks": block_reports,
            "successive_block_changes": successive,
            "first_second_half_change": first_second,
            "max_mean_block_rel_to_all": max_mean_block_rel,
            "max_reynolds_block_rel_to_all": max_reynolds_block_rel,
            "tolerance": args.tolerance,
            "converged_by_tolerance": converged_by_tolerance,
            "scalar_time_series": scalar_series(f, keys, args.dt),
        }

    with open(output, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"wrote={output}")
    print(f"snapshots={report['n_snapshots']}")
    print(f"sample_time_range={report['sample_time_range'][0]:.12g},{report['sample_time_range'][1]:.12g}")
    print(f"max_mean_block_rel_to_all={max_mean_block_rel:.6e}")
    print(f"max_reynolds_block_rel_to_all={max_reynolds_block_rel:.6e}")
    print(f"converged_by_tolerance={converged_by_tolerance}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
