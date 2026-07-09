#!/usr/bin/env python
"""Audit an MKM postprocessed target file against its constraint recipe."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import h5py
import numpy as np


def shape_or_none(group: h5py.File, path: str) -> list[int] | None:
    if path not in group:
        return None
    return list(group[path].shape)


def rank_counts(ranks: np.ndarray) -> dict[str, int]:
    return {str(int(rank)): int(np.sum(ranks == rank)) for rank in np.unique(ranks)}


def rel_norm(a: np.ndarray, b: np.ndarray) -> float:
    denom = np.linalg.norm(b.ravel())
    if denom == 0.0:
        denom = 1.0
    return float(np.linalg.norm((a - b).ravel()) / denom)


def constraint_residuals(f_target: h5py.File, f_constraint: h5py.File) -> dict[str, float] | None:
    if "modal/u_hat" not in f_target:
        return None

    energy_floor_rel = 1e-18
    u_hat = f_target["modal/u_hat"]
    k_stream = f_constraint["wavenumbers/k_stream"][:]
    k_span = f_constraint["wavenumbers/k_span"][:]
    d_wall = f_constraint["operators/D_wall"][:]
    b_boundary = f_constraint["operators/B_boundary"][:]
    e_stream = f_constraint["operators/E_stream"][:]
    e_span = f_constraint["operators/E_span"][:]
    e_wall = f_constraint["operators/E_wall"][:]

    d_wall_e_wall = d_wall @ e_wall
    g_boundary = np.vstack((
        b_boundary @ e_stream,
        b_boundary @ e_span,
        b_boundary @ e_wall,
    )).astype(complex)

    total_norm2 = 0.0
    div_norm2 = 0.0
    bc_norm2 = 0.0
    mode_totals_and_residuals = []
    nsnap, nx, ny, _ = u_hat.shape
    for i, ks in enumerate(k_stream):
        for j, kp in enumerate(k_span):
            u_mode = u_hat[:, i, j, :]
            total = float(np.sum(np.abs(u_mode) ** 2))
            if total == 0.0:
                continue
            g_div = 1j * ks * e_stream + 1j * kp * e_span + d_wall_e_wall
            div = u_mode @ g_div.T
            bc = u_mode @ g_boundary.T
            div2 = float(np.sum(np.abs(div) ** 2))
            bc2 = float(np.sum(np.abs(bc) ** 2))
            total_norm2 += total
            div_norm2 += div2
            bc_norm2 += bc2
            mode_totals_and_residuals.append((total, float(np.sqrt((div2 + bc2) / total))))

    denom = max(total_norm2, 1.0)
    nontrivial_floor = total_norm2 * energy_floor_rel
    nontrivial_residuals = [
        residual for total, residual in mode_totals_and_residuals
        if total >= nontrivial_floor
    ]
    return {
        "n_snapshots_checked": int(nsnap),
        "constraint_residual_global_rel": float(np.sqrt((div_norm2 + bc_norm2) / denom)),
        "constraint_div_global_rel": float(np.sqrt(div_norm2 / denom)),
        "constraint_bc_global_rel": float(np.sqrt(bc_norm2 / denom)),
        "constraint_mode_energy_floor_rel": energy_floor_rel,
        "constraint_modes_above_energy_floor": len(nontrivial_residuals),
        "constraint_max_mode_rel_nontrivial": float(max(nontrivial_residuals, default=0.0)),
    }


def representative_matrix_checks(f_target: h5py.File) -> dict[str, float] | None:
    if "modal/B0_DNS" not in f_target:
        return None
    b0 = f_target["modal/B0_DNS"]
    nx, ny = b0.shape[:2]
    reps = [(0, 0), (1, 0), (0, 1), (nx // 2, 0), (0, ny // 2), (nx - 1, ny - 1)]
    hermitian = []
    lag0_rel = []
    has_lag0 = "lag_covariance/lag_0" in f_target
    lag0 = f_target["lag_covariance/lag_0"] if has_lag0 else None
    for i, j in reps:
        mat = b0[i, j]
        hermitian.append(rel_norm(mat, mat.conj().T))
        if has_lag0:
            lag0_rel.append(rel_norm(lag0[i, j], mat))
    checks = {"representative_B0_hermitian_rel_max": float(max(hermitian))}
    if lag0_rel:
        checks["representative_lag0_minus_B0_rel_max"] = float(max(lag0_rel))
    return checks


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target-h5", required=True, help="Postprocessed target HDF5 file.")
    parser.add_argument("--constraint-file", required=True, help="Matching constraint recipe HDF5 file.")
    parser.add_argument("--velocity-h5", help="Optional source velocity HDF5 file for grid comparison.")
    parser.add_argument("--output", required=True, help="Output JSON audit report.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    target_h5 = Path(args.target_h5).expanduser().resolve()
    constraint_file = Path(args.constraint_file).expanduser().resolve()
    velocity_h5 = Path(args.velocity_h5).expanduser().resolve() if args.velocity_h5 else None
    output = Path(args.output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    with h5py.File(target_h5, "r") as f_target, h5py.File(constraint_file, "r") as f_constraint:
        z_target = f_target["geometry/z_wall"][:]
        z_constraint = f_constraint["grid/z_wall"][:]
        report: dict[str, object] = {
            "target_h5": str(target_h5),
            "target_size_bytes": target_h5.stat().st_size,
            "constraint_file": str(constraint_file),
            "constraint_size_bytes": constraint_file.stat().st_size,
            "sampling_stage_label": f_target.attrs.get("sampling_stage_label", ""),
            "snapshot_keys": f_target.attrs.get("snapshot_keys", ""),
            "dt": float(f_target.attrs.get("dt", np.nan)),
            "z_grid_match_constraint": bool(np.allclose(z_target, z_constraint)),
            "z_first_last": [float(z_target[0]), float(z_target[-1])],
            "mean_profile_shape": shape_or_none(f_target, "mean_profile"),
            "reynolds_shape": shape_or_none(f_target, "reynolds_stress_profile"),
            "B0_shape": shape_or_none(f_target, "modal/B0_DNS"),
            "u_hat_shape": shape_or_none(f_target, "modal/u_hat"),
            "rank_counts": rank_counts(f_constraint["mode_audit/rank"][:]),
        }
        if "lag_covariance" in f_target:
            report["lag_shapes"] = {
                name: list(f_target[f"lag_covariance/{name}"].shape)
                for name in sorted(f_target["lag_covariance"].keys())
            }
        if velocity_h5 is not None:
            with h5py.File(velocity_h5, "r") as f_velocity:
                z_velocity = f_velocity["u0/mesh/x0"][:]
                report["velocity_h5"] = str(velocity_h5)
                report["velocity_size_bytes"] = velocity_h5.stat().st_size
                report["z_grid_match_velocity"] = bool(np.allclose(z_target, z_velocity))
                report["velocity_snapshot_keys"] = sorted(
                    f_velocity["u0/3D"].keys(), key=lambda key: int(key)
                )
        residuals = constraint_residuals(f_target, f_constraint)
        if residuals is not None:
            report.update(residuals)
        matrix_checks = representative_matrix_checks(f_target)
        if matrix_checks is not None:
            report.update(matrix_checks)

    with open(output, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"wrote={output}")
    print(f"target_size_bytes={report['target_size_bytes']}")
    print(f"z_grid_match_constraint={report['z_grid_match_constraint']}")
    if "z_grid_match_velocity" in report:
        print(f"z_grid_match_velocity={report['z_grid_match_velocity']}")
    if "constraint_residual_global_rel" in report:
        print(f"constraint_residual_global_rel={report['constraint_residual_global_rel']:.6e}")
        print(f"constraint_div_global_rel={report['constraint_div_global_rel']:.6e}")
        print(f"constraint_bc_global_rel={report['constraint_bc_global_rel']:.6e}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
