#!/usr/bin/env python
"""Project MKM DNS modal covariance into the discrete admissible subspace.

The script reads the production target covariance ``modal/B0_DNS`` and the
matching channel-flow constraint recipe. For each horizontal Fourier mode it
forms the row-orthonormal constraint matrix ``Gtilde``, computes

    B_adm = P B0_DNS P,   P = I - Gtilde^* Gtilde,

and compares the projected covariance against both the unprojected covariance
and the Reynolds-stress profile sampled directly from the DNS snapshots.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import h5py
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
    "axes.unicode_minus": False,
})


COMPONENT_NAMES = ("streamwise", "spanwise", "wallnormal")
COMPONENT_LABELS = (r"x", r"y", r"z")


def rel_norm(a: np.ndarray, b: np.ndarray) -> float:
    denom = np.linalg.norm(np.ravel(b))
    if denom == 0.0:
        denom = 1.0
    return float(np.linalg.norm(np.ravel(a - b)) / denom)


def sorted_wall(z: np.ndarray, *arrays: np.ndarray) -> tuple[np.ndarray, ...]:
    order = np.argsort(z)
    return (z[order],) + tuple(array[order] for array in arrays)


def load_gtilde_or_compute(
    f_constraint: h5py.File,
    i: int,
    j: int,
    svd_rtol: float,
    saved_operators: dict[str, np.ndarray],
) -> tuple[np.ndarray, str]:
    """Load a saved Gtilde if present, otherwise rebuild it from saved operators."""

    for group_name in (f"modes/i{i}_j{j}", f"representative_modes/i{i}_j{j}"):
        path = f"{group_name}/Gtilde"
        if path in f_constraint:
            return f_constraint[path][:], "saved_gtilde"

    k_stream = saved_operators["k_stream"][i]
    k_span = saved_operators["k_span"][j]
    g_div = (
        1j * k_stream * saved_operators["E_stream"]
        + 1j * k_span * saved_operators["E_span"]
        + saved_operators["D_wall"] @ saved_operators["E_wall"]
    )
    g_boundary = saved_operators["G_boundary"]
    g_raw = np.vstack((g_div, g_boundary))
    _, singular_values, vh = np.linalg.svd(g_raw, full_matrices=True)
    rank = int(np.sum(singular_values > svd_rtol * singular_values[0]))
    return vh[:rank, :], "rebuilt_from_saved_operators"


def project_covariance(b0: np.ndarray, gtilde: np.ndarray) -> np.ndarray:
    """Return P B0 P using the row-orthonormal constraint projector."""

    g_b = gtilde @ b0
    b_g_star = g_b.conj().T
    g_b_g_star = g_b @ gtilde.conj().T
    projected = (
        b0
        - gtilde.conj().T @ g_b
        - b_g_star @ gtilde
        + gtilde.conj().T @ g_b_g_star @ gtilde
    )
    return 0.5 * (projected + projected.conj().T)


def accumulate_reynolds_from_covariance(
    profile: np.ndarray,
    covariance: np.ndarray,
) -> None:
    nz = profile.shape[0]
    for z_index in range(nz):
        rows = slice(3 * z_index, 3 * z_index + 3)
        profile[z_index] += covariance[rows, rows].real


def save_json(path: Path, report: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"wrote={path}")


def save(fig: plt.Figure, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote={path}")


def plot_projection_errors(
    mode_rel: np.ndarray,
    mode_energy: np.ndarray,
    output_dir: Path,
) -> None:
    finite_rel = np.where(mode_energy > 0.0, mode_rel, np.nan)
    log_rel = np.log10(np.maximum(finite_rel, 1e-18))

    fig, axes = plt.subplots(1, 2, figsize=(8.0, 3.1), constrained_layout=True)
    im0 = axes[0].imshow(log_rel.T, origin="lower", aspect="auto", cmap="magma")
    axes[0].set_xlabel(r"streamwise mode index $p$")
    axes[0].set_ylabel(r"spanwise mode index $q$")
    axes[0].set_title(r"$\log_{10}\|B_{\rm adm}-B_0\|_F/\|B_0\|_F$")
    fig.colorbar(im0, ax=axes[0], fraction=0.046, pad=0.02)

    energy = np.maximum(mode_energy, 1e-300)
    axes[1].scatter(
        np.log10(energy.ravel()),
        np.log10(np.maximum(mode_rel.ravel(), 1e-18)),
        s=4,
        alpha=0.45,
        linewidths=0.0,
    )
    axes[1].set_xlabel(r"$\log_{10}\mathrm{tr}\, B_0$")
    axes[1].set_ylabel(r"$\log_{10}$ relative projection change", labelpad=8)
    axes[1].grid(True, color="0.9")
    save(fig, output_dir / "mkm_projected_covariance_mode_errors.pdf")


def plot_reynolds_profiles(
    z: np.ndarray,
    sampled: np.ndarray,
    from_b0: np.ndarray,
    from_badm: np.ndarray,
    output_dir: Path,
    friction_velocity: float,
) -> None:
    stress_scale = friction_velocity**2
    z_sorted, sampled_sorted, b0_sorted, badm_sorted = sorted_wall(
        z,
        sampled / stress_scale,
        from_b0 / stress_scale,
        from_badm / stress_scale,
    )

    fig, axes = plt.subplots(1, 2, figsize=(7.3, 3.4), sharey=True)
    diag = ((0, 0), (1, 1), (2, 2))
    marker_stride = max(1, len(z_sorted) // 10)
    for a, b in diag:
        label = rf"$R_{{{COMPONENT_LABELS[a]}{COMPONENT_LABELS[b]}}}$"
        sampled_line = axes[0].plot(
            sampled_sorted[:, a, b],
            z_sorted,
            linewidth=1.8,
            alpha=0.62,
            label=label,
        )[0]
        color = sampled_line.get_color()
        axes[0].plot(
            badm_sorted[:, a, b],
            z_sorted,
            color="black",
            linewidth=0.9,
            linestyle=(0, (4, 2)),
            zorder=3,
        )
        axes[0].plot(
            badm_sorted[::marker_stride, a, b],
            z_sorted[::marker_stride],
            linestyle="none",
            marker="o",
            markersize=3.0,
            markerfacecolor="white",
            markeredgecolor=color,
            markeredgewidth=0.9,
            zorder=4,
        )
    axes[0].set_xlabel(r"$R_{\alpha\alpha}/u_\tau^2$")
    axes[0].set_ylabel(r"$z/h$")
    axes[0].grid(True, color="0.9")
    axes[0].legend(frameon=False, loc="best")

    offdiag = ((0, 1), (0, 2), (1, 2))
    for a, b in offdiag:
        label = rf"$R_{{{COMPONENT_LABELS[a]}{COMPONENT_LABELS[b]}}}$"
        sampled_line = axes[1].plot(
            sampled_sorted[:, a, b],
            z_sorted,
            linewidth=1.8,
            alpha=0.62,
            label=label,
        )[0]
        color = sampled_line.get_color()
        axes[1].plot(
            badm_sorted[:, a, b],
            z_sorted,
            color="black",
            linewidth=0.9,
            linestyle=(0, (4, 2)),
            zorder=3,
        )
        axes[1].plot(
            badm_sorted[::marker_stride, a, b],
            z_sorted[::marker_stride],
            linestyle="none",
            marker="o",
            markersize=3.0,
            markerfacecolor="white",
            markeredgecolor=color,
            markeredgewidth=0.9,
            zorder=4,
        )
    axes[1].set_xlabel(r"$R_{\alpha\beta}/u_\tau^2$")
    axes[1].grid(True, color="0.9")
    axes[1].legend(frameon=False, loc="best")
    style_handles = [
        Line2D([0], [0], color="0.35", linewidth=1.8, alpha=0.62, label=r"$R^{\mathrm{sample}}$"),
        Line2D(
            [0],
            [0],
            color="black",
            linewidth=0.9,
            linestyle=(0, (4, 2)),
            marker="o",
            markerfacecolor="white",
            markeredgecolor="0.35",
            markersize=3.0,
            label=r"$R^{B_{\rm adm}}$",
        ),
    ]
    fig.legend(handles=style_handles, frameon=False, ncols=2, loc="upper center", bbox_to_anchor=(0.5, 1.03))
    save(fig, output_dir / "mkm_projected_reynolds_stress_profiles.pdf")

    error = badm_sorted - sampled_sorted
    fig, axes = plt.subplots(1, 2, figsize=(7.3, 3.4), sharey=True)
    for a, b in diag:
        axes[0].plot(error[:, a, b], z_sorted, label=rf"$\Delta R_{{{COMPONENT_LABELS[a]}{COMPONENT_LABELS[b]}}}$")
    axes[0].set_xlabel(r"$(R^{\rm adm}_{\alpha\alpha}-R^{\rm sample}_{\alpha\alpha})/u_\tau^2$")
    axes[0].set_ylabel(r"$z/h$")
    axes[0].grid(True, color="0.9")
    axes[0].legend(frameon=False)

    for a, b in offdiag:
        axes[1].plot(error[:, a, b], z_sorted, label=rf"$\Delta R_{{{COMPONENT_LABELS[a]}{COMPONENT_LABELS[b]}}}$")
    axes[1].set_xlabel(r"$(R^{\rm adm}_{\alpha\beta}-R^{\rm sample}_{\alpha\beta})/u_\tau^2$")
    axes[1].grid(True, color="0.9")
    axes[1].legend(frameon=False)
    save(fig, output_dir / "mkm_projected_reynolds_stress_errors.pdf")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target-h5", required=True, help="Input production target HDF5.")
    parser.add_argument("--constraint-file", required=True, help="Matching constraint recipe HDF5.")
    parser.add_argument("--output-h5", help="Optional HDF5 file for B_adm,DNS and derived profiles.")
    parser.add_argument("--diagnostics-json", required=True, help="Output JSON diagnostics.")
    parser.add_argument("--figure-dir", required=True, help="Directory for PDF diagnostic figures.")
    parser.add_argument("--svd-rtol", type=float, default=1e-12)
    parser.add_argument("--friction-velocity", type=float, default=1.0,
                        help="Velocity scale used to nondimensionalize Reynolds-stress plots.")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--max-modes", type=int, help="Debug option: process at most this many modes.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    target_h5 = Path(args.target_h5).expanduser().resolve()
    constraint_file = Path(args.constraint_file).expanduser().resolve()
    diagnostics_json = Path(args.diagnostics_json).expanduser().resolve()
    figure_dir = Path(args.figure_dir).expanduser().resolve()
    output_h5 = Path(args.output_h5).expanduser().resolve() if args.output_h5 else None
    if output_h5 and output_h5.exists():
        if not args.overwrite:
            raise FileExistsError(f"{output_h5} exists; pass --overwrite to replace it")
        output_h5.unlink()

    with h5py.File(target_h5, "r") as f_target, h5py.File(constraint_file, "r") as f_constraint:
        b0_ds = f_target["modal/B0_DNS"]
        nx, ny, modal_dim, _ = b0_ds.shape
        nz = modal_dim // 3
        sampled_reynolds = f_target["reynolds_stress_profile"][:]
        z = f_target["geometry/z_wall"][:]

        z_constraint = f_constraint["grid/z_wall"][:]
        if not np.allclose(z, z_constraint):
            raise ValueError("target and constraint wall-normal grids do not match")

        saved_operators = {
            "k_stream": f_constraint["wavenumbers/k_stream"][:],
            "k_span": f_constraint["wavenumbers/k_span"][:],
            "D_wall": f_constraint["operators/D_wall"][:],
            "B_boundary": f_constraint["operators/B_boundary"][:],
            "E_stream": f_constraint["operators/E_stream"][:],
            "E_span": f_constraint["operators/E_span"][:],
            "E_wall": f_constraint["operators/E_wall"][:],
        }
        saved_operators["G_boundary"] = np.vstack((
            saved_operators["B_boundary"] @ saved_operators["E_stream"],
            saved_operators["B_boundary"] @ saved_operators["E_span"],
            saved_operators["B_boundary"] @ saved_operators["E_wall"],
        )).astype(complex)

        reynolds_from_b0 = np.zeros_like(sampled_reynolds)
        reynolds_from_badm = np.zeros_like(sampled_reynolds)
        mode_rel = np.zeros((nx, ny), dtype=float)
        mode_abs = np.zeros((nx, ny), dtype=float)
        mode_energy = np.zeros((nx, ny), dtype=float)
        mode_constraint_resid = np.zeros((nx, ny), dtype=float)
        gtilde_sources: dict[str, int] = {}
        processed = 0
        total_b0_norm2 = 0.0
        total_diff_norm2 = 0.0
        total_b0_trace = 0.0
        total_badm_trace = 0.0

        out_file = h5py.File(output_h5, "w") if output_h5 else None
        try:
            badm_ds = None
            if out_file is not None:
                out_file.attrs["source_target_h5"] = str(target_h5)
                out_file.attrs["constraint_file"] = str(constraint_file)
                out_file.attrs["definition"] = "B_adm_DNS = P B0_DNS P, P = I - Gtilde^* Gtilde"
                out_file.attrs["svd_rtol"] = args.svd_rtol
                out_file.create_dataset("geometry/z_wall", data=z)
                out_file.create_dataset("geometry/k_stream", data=saved_operators["k_stream"])
                out_file.create_dataset("geometry/k_span", data=saved_operators["k_span"])
                badm_ds = out_file.create_dataset(
                    "modal/B_adm_DNS",
                    shape=b0_ds.shape,
                    dtype=np.complex128,
                    chunks=(1, 1, modal_dim, modal_dim),
                )

            for i in range(nx):
                for j in range(ny):
                    if args.max_modes is not None and processed >= args.max_modes:
                        break
                    b0 = b0_ds[i, j]
                    gtilde, source = load_gtilde_or_compute(
                        f_constraint,
                        i,
                        j,
                        args.svd_rtol,
                        saved_operators,
                    )
                    gtilde_sources[source] = gtilde_sources.get(source, 0) + 1
                    badm = project_covariance(b0, gtilde)
                    diff = badm - b0

                    b0_norm = np.linalg.norm(b0)
                    diff_norm = np.linalg.norm(diff)
                    mode_abs[i, j] = float(diff_norm)
                    mode_rel[i, j] = float(diff_norm / max(b0_norm, 1.0))
                    mode_energy[i, j] = float(np.trace(b0).real)
                    mode_constraint_resid[i, j] = float(
                        np.linalg.norm(gtilde @ badm) / max(np.linalg.norm(badm), 1.0)
                    )
                    total_b0_norm2 += float(b0_norm**2)
                    total_diff_norm2 += float(diff_norm**2)
                    total_b0_trace += float(np.trace(b0).real)
                    total_badm_trace += float(np.trace(badm).real)

                    accumulate_reynolds_from_covariance(reynolds_from_b0, b0)
                    accumulate_reynolds_from_covariance(reynolds_from_badm, badm)
                    if badm_ds is not None:
                        badm_ds[i, j] = badm
                    processed += 1
                if args.max_modes is not None and processed >= args.max_modes:
                    break

            if out_file is not None:
                out_file.create_dataset("profiles/reynolds_from_B0_DNS", data=reynolds_from_b0)
                out_file.create_dataset("profiles/reynolds_from_B_adm_DNS", data=reynolds_from_badm)
                out_file.create_dataset("profiles/reynolds_sampled", data=sampled_reynolds)
                out_file.create_dataset("mode_diagnostics/projection_abs_fro", data=mode_abs)
                out_file.create_dataset("mode_diagnostics/projection_rel_fro", data=mode_rel)
                out_file.create_dataset("mode_diagnostics/mode_energy_trace_B0", data=mode_energy)
                out_file.create_dataset("mode_diagnostics/projected_constraint_residual", data=mode_constraint_resid)
        finally:
            if out_file is not None:
                out_file.close()

    report = {
        "target_h5": str(target_h5),
        "constraint_file": str(constraint_file),
        "output_h5": str(output_h5) if output_h5 else None,
        "n_modes_processed": processed,
        "modal_shape": [int(nx), int(ny), int(modal_dim), int(modal_dim)],
        "component_order": COMPONENT_NAMES,
        "gtilde_sources": gtilde_sources,
        "global_projection_rel_fro": float(np.sqrt(total_diff_norm2 / max(total_b0_norm2, 1.0))),
        "max_mode_projection_rel_fro": float(np.max(mode_rel)),
        "max_mode_projection_abs_fro": float(np.max(mode_abs)),
        "trace_B0_total": total_b0_trace,
        "trace_Badm_total": total_badm_trace,
        "trace_projection_rel_change": float((total_badm_trace - total_b0_trace) / max(abs(total_b0_trace), 1.0)),
        "max_projected_constraint_residual": float(np.max(mode_constraint_resid)),
        "reynolds_from_B0_rel_to_sampled": rel_norm(reynolds_from_b0, sampled_reynolds),
        "reynolds_from_Badm_rel_to_sampled": rel_norm(reynolds_from_badm, sampled_reynolds),
        "reynolds_from_Badm_rel_to_B0": rel_norm(reynolds_from_badm, reynolds_from_b0),
        "max_abs_reynolds_Badm_minus_sampled": float(np.max(np.abs(reynolds_from_badm - sampled_reynolds))),
        "max_abs_reynolds_B0_minus_sampled": float(np.max(np.abs(reynolds_from_b0 - sampled_reynolds))),
    }
    save_json(diagnostics_json, report)
    plot_projection_errors(mode_rel, mode_energy, figure_dir)
    plot_reynolds_profiles(
        z,
        sampled_reynolds,
        reynolds_from_b0,
        reynolds_from_badm,
        figure_dir,
        friction_velocity=args.friction_velocity,
    )
    if output_h5 is not None:
        print(f"wrote={output_h5}")
    print(f"global_projection_rel_fro={report['global_projection_rel_fro']:.6e}")
    print(f"reynolds_from_Badm_rel_to_sampled={report['reynolds_from_Badm_rel_to_sampled']:.6e}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
