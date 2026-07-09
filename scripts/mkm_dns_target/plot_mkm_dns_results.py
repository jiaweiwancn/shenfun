#!/usr/bin/env python
"""Plot production MKM DNS target diagnostics and profiles."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path

import h5py
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1 import axes_size, make_axes_locatable

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
    "axes.unicode_minus": False,
})


COMPONENT_GROUPS = ("u1", "u2", "u0")
COMPONENT_NAMES = ("streamwise", "spanwise", "wallnormal")
COLORBAR_WIDTH_IN = 0.07
COLORBAR_PAD_IN = 0.06


@dataclass(frozen=True)
class PlotScales:
    half_height: float
    friction_velocity: float
    re_tau: float

    def length(self, values: np.ndarray) -> np.ndarray:
        return values / self.half_height

    def velocity(self, values: np.ndarray) -> np.ndarray:
        return values / self.friction_velocity

    def stress(self, values: np.ndarray) -> np.ndarray:
        return values / self.friction_velocity**2

    def time(self, values: np.ndarray | float) -> np.ndarray | float:
        return values * self.friction_velocity / self.half_height


def sorted_snapshot_keys(f: h5py.File) -> list[str]:
    return sorted(f["u1/3D"].keys(), key=lambda key: int(key))


def nearest_key(keys: list[str], time: float, dt: float) -> str:
    target_step = int(round(time / dt))
    return min(keys, key=lambda key: abs(int(key) - target_step))


def sorted_wall(z: np.ndarray, *arrays: np.ndarray) -> tuple[np.ndarray, ...]:
    order = np.argsort(z)
    return (z[order],) + tuple(array[order] for array in arrays)


def figure_path(output_dir: Path, name: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir / name


def save(fig: plt.Figure, path: Path) -> None:
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote={path}")


def add_matched_colorbar(fig: plt.Figure, ax: plt.Axes, mappable, label: str) -> None:
    divider = make_axes_locatable(ax)
    cax = divider.append_axes(
        "right",
        size=axes_size.Fixed(COLORBAR_WIDTH_IN),
        pad=axes_size.Fixed(COLORBAR_PAD_IN),
    )
    cbar = fig.colorbar(mappable, cax=cax)
    cbar.set_label(label)


def plot_scalar_diagnostics(
    diagnostics_json: Path,
    output_dir: Path,
    accepted_t_min: float,
    scales: PlotScales,
) -> None:
    with open(diagnostics_json, "r", encoding="utf-8") as f:
        report = json.load(f)
    series = report.get("series", [])
    if not series:
        return

    time = scales.time(np.array([row["time"] for row in series], dtype=float))
    accepted_time = scales.time(accepted_t_min)
    e_wall = np.array([row["energy_wallnormal"] for row in series], dtype=float)
    e_stream = np.array([row["energy_streamwise"] for row in series], dtype=float)
    e_span = np.array([row["energy_spanwise"] for row in series], dtype=float)
    flux = np.array([row["flux"] for row in series], dtype=float)

    fig, axes = plt.subplots(2, 1, figsize=(6.8, 5.2), sharex=True)
    def rel(values: np.ndarray) -> np.ndarray:
        return values / values.mean() - 1.0

    axes[0].plot(time, rel(e_stream), label=r"$E_x$")
    axes[0].plot(time, rel(e_span), label=r"$E_y$")
    axes[0].plot(time, rel(e_wall), label=r"$E_z$")
    axes[0].axvline(accepted_time, color="0.25", linestyle="--", linewidth=1.0)
    axes[0].set_ylabel(r"$E_i/\langle E_i\rangle-1$")
    axes[0].legend(ncols=3, frameon=False, loc="best")
    axes[0].grid(True, color="0.9")

    axes[1].plot(time, rel(flux), color="tab:purple", label=r"\textrm{bulk flux}")
    axes[1].axvline(accepted_time, color="0.25", linestyle="--", linewidth=1.0)
    axes[1].set_xlabel(r"$t u_\tau/h$")
    axes[1].set_ylabel(r"$Q/\langle Q\rangle-1$")
    axes[1].grid(True, color="0.9")
    axes[1].legend(frameon=False, loc="best")

    save(fig, figure_path(output_dir, "mkm_production_sampling_diagnostics.pdf"))


def contour_slices(
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
    xz_plane: np.ndarray,
    yz_plane: np.ndarray,
    cbar_label: str,
    output_path: Path,
) -> None:
    z_sorted, xz_sorted, yz_sorted = sorted_wall(z, xz_plane, yz_plane)
    x_grid, xz_grid = np.meshgrid(x, z_sorted)
    y_grid, yz_grid = np.meshgrid(y, z_sorted)
    vmin = min(float(np.nanmin(xz_sorted)), float(np.nanmin(yz_sorted)))
    vmax = max(float(np.nanmax(xz_sorted)), float(np.nanmax(yz_sorted)))

    x_span = max(float(np.ptp(x)), 1.0)
    y_span = max(float(np.ptp(y)), 1.0)
    fig, axes = plt.subplots(
        1,
        2,
        figsize=(7.3, 2.65),
        sharey=True,
        gridspec_kw={"width_ratios": [x_span, y_span], "wspace": 0.42},
    )

    im0 = axes[0].pcolormesh(
        x_grid,
        xz_grid,
        xz_sorted,
        shading="auto",
        cmap="viridis",
        rasterized=True,
        vmin=vmin,
        vmax=vmax,
    )
    axes[0].set_xlabel(r"$x/h$")
    axes[0].set_ylabel(r"$z/h$")
    axes[0].set_aspect("equal", adjustable="box")
    add_matched_colorbar(fig, axes[0], im0, cbar_label)

    im1 = axes[1].pcolormesh(
        y_grid,
        yz_grid,
        yz_sorted,
        shading="auto",
        cmap="viridis",
        rasterized=True,
        vmin=vmin,
        vmax=vmax,
    )
    axes[1].set_xlabel(r"$y/h$")
    axes[1].set_aspect("equal", adjustable="box")
    add_matched_colorbar(fig, axes[1], im1, cbar_label)

    fig.subplots_adjust(left=0.08, right=0.96, bottom=0.18, top=0.96)
    save(fig, output_path)


def plot_contours(
    target_h5: Path,
    velocity_h5: Path,
    output_dir: Path,
    dt: float,
    instant_time: float,
    stream_index: int,
    span_index: int,
    scales: PlotScales,
) -> tuple[str, float]:
    with h5py.File(target_h5, "r") as f_target, h5py.File(velocity_h5, "r") as f_vel:
        z = f_target["geometry/z_wall"][:]
        x = f_target["geometry/x_stream"][:]
        y = f_target["geometry/x_span"][:]
        mean_ux = f_target["mean_profile"][:, 0]

        keys = sorted_snapshot_keys(f_vel)
        key = nearest_key(keys, instant_time, dt)
        actual_time = int(key) * dt
        ux = f_vel[f"u1/3D/{key}"][:]

    x = scales.length(x)
    y = scales.length(y)
    z = scales.length(z)
    actual_time = scales.time(actual_time)
    span_index = span_index % ux.shape[2]
    stream_index = stream_index % ux.shape[1]
    xz_instant = scales.velocity(ux[:, :, span_index])
    yz_instant = scales.velocity(ux[:, stream_index, :])
    mean_ux = scales.velocity(mean_ux)
    xz_mean = np.repeat(mean_ux[:, None], x.size, axis=1)
    yz_mean = np.repeat(mean_ux[:, None], y.size, axis=1)

    contour_slices(
        x,
        y,
        z,
        xz_instant,
        yz_instant,
        r"$u_x/u_\tau$",
        figure_path(output_dir, "mkm_production_instantaneous_contours.pdf"),
    )
    contour_slices(
        x,
        y,
        z,
        xz_mean,
        yz_mean,
        r"$\overline{u}_x/u_\tau$",
        figure_path(output_dir, "mkm_production_mean_contours.pdf"),
    )
    return key, actual_time


def plot_profiles(target_h5: Path, output_dir: Path, scales: PlotScales) -> None:
    with h5py.File(target_h5, "r") as f:
        z = f["geometry/z_wall"][:]
        mean = f["mean_profile"][:]
        reynolds = f["reynolds_stress_profile"][:]

    z_sorted, mean_sorted, reynolds_sorted = sorted_wall(
        scales.length(z),
        scales.velocity(mean),
        scales.stress(reynolds),
    )

    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.4), sharey=True)
    axes[0].plot(mean_sorted[:, 0], z_sorted, color="tab:blue", label=r"$\overline{u}_x/u_\tau$")
    axes[0].set_xlabel(r"$\overline{u}_x/u_\tau$")
    axes[0].set_ylabel(r"$z/h$")
    axes[0].grid(True, color="0.9")
    axes[0].legend(frameon=False)

    axes[1].plot(mean_sorted[:, 1], z_sorted, color="tab:orange", label=r"$\overline{u}_y/u_\tau$")
    axes[1].plot(mean_sorted[:, 2], z_sorted, color="tab:green", label=r"$\overline{u}_z/u_\tau$")
    axes[1].set_xlabel(r"$\overline{u}_{y,z}/u_\tau$")
    axes[1].grid(True, color="0.9")
    axes[1].legend(frameon=False)
    save(fig, figure_path(output_dir, "mkm_production_mean_velocity_profile.pdf"))

    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.4), sharey=True)
    diag = ((0, 0, r"$R_{xx}^+$"), (1, 1, r"$R_{yy}^+$"), (2, 2, r"$R_{zz}^+$"))
    for a, b, label in diag:
        axes[0].plot(reynolds_sorted[:, a, b], z_sorted, label=label)
    axes[0].set_xlabel(r"$R_{\alpha\alpha}/u_\tau^2$")
    axes[0].set_ylabel(r"$z/h$")
    axes[0].grid(True, color="0.9")
    axes[0].legend(frameon=False)

    offdiag = ((0, 1, r"$R_{xy}^+$"), (0, 2, r"$R_{xz}^+$"), (1, 2, r"$R_{yz}^+$"))
    for a, b, label in offdiag:
        axes[1].plot(reynolds_sorted[:, a, b], z_sorted, label=label)
    axes[1].set_xlabel(r"$R_{\alpha\beta}/u_\tau^2$")
    axes[1].grid(True, color="0.9")
    axes[1].legend(frameon=False)
    save(fig, figure_path(output_dir, "mkm_production_reynolds_stress_profiles.pdf"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target-h5", required=True)
    parser.add_argument("--velocity-h5", required=True)
    parser.add_argument("--diagnostics-json")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--dt", type=float, default=0.0005)
    parser.add_argument("--instant-time", type=float, default=180.0)
    parser.add_argument("--accepted-t-min", type=float, default=60.0)
    parser.add_argument("--stream-index", type=int, default=0)
    parser.add_argument("--span-index", type=int, default=0)
    parser.add_argument("--half-height", type=float, default=1.0)
    parser.add_argument("--friction-velocity", type=float, default=1.0)
    parser.add_argument("--re-tau", type=float, default=180.0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    target_h5 = Path(args.target_h5).expanduser().resolve()
    velocity_h5 = Path(args.velocity_h5).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    scales = PlotScales(
        half_height=args.half_height,
        friction_velocity=args.friction_velocity,
        re_tau=args.re_tau,
    )

    if args.diagnostics_json:
        plot_scalar_diagnostics(
            Path(args.diagnostics_json).expanduser().resolve(),
            output_dir,
            args.accepted_t_min,
            scales,
        )
    key, actual_time = plot_contours(
        target_h5,
        velocity_h5,
        output_dir,
        args.dt,
        args.instant_time,
        args.stream_index,
        args.span_index,
        scales,
    )
    plot_profiles(target_h5, output_dir, scales)
    print(f"instantaneous_key={key}")
    print(f"instantaneous_time={actual_time:.12g}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
