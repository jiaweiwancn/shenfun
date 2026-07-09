#!/usr/bin/env python
"""Plot first diagnostics from a single-mode MKM channel resolvent HDF5."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import h5py
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


COMPONENT_LABELS = (r"$u_x$", r"$u_y$", r"$u_z$")
COMPONENT_NAMES = ("streamwise", "spanwise", "wallnormal")
FIGURE_NAMES = (
    "mkm_resolvent_mode_shapes.pdf",
    "mkm_resolvent_gain_bode.pdf",
    "mkm_resolvent_peak_location_gain.pdf",
    "mkm_resolvent_reconstructed_fields.pdf",
)


@dataclass(frozen=True)
class ResolventData:
    z: np.ndarray
    omega: np.ndarray
    kappa: float
    lambda_: float
    singular_values: np.ndarray
    response_modes: np.ndarray
    forcing_modes: np.ndarray
    response_energy_density: np.ndarray
    critical_z: np.ndarray
    critical_count: np.ndarray
    component_names: tuple[str, ...]


def configure_matplotlib(no_tex: bool) -> None:
    plt.rcParams.update({
        "text.usetex": not no_tex,
        "font.family": "serif",
        "font.serif": ["Computer Modern Roman"],
        "axes.unicode_minus": False,
    })


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--resolvent-h5", required=True, help="Input single-mode resolvent HDF5.")
    parser.add_argument("--figure-dir", required=True, help="Output figure directory.")
    parser.add_argument("--omega-index", type=int, default=0)
    parser.add_argument("--singular-index", type=int, default=0)
    parser.add_argument("--n-shapes", type=int, default=3)
    parser.add_argument("--phase", type=float, default=0.0)
    parser.add_argument("--n-stream", type=int, default=128)
    parser.add_argument("--n-span", type=int, default=128)
    parser.add_argument("--no-tex", action="store_true", help="Disable Matplotlib LaTeX rendering.")
    return parser.parse_args()


def _decode_attr(value: object, default: str) -> str:
    if value is None:
        return default
    if isinstance(value, bytes):
        return value.decode("utf-8")
    return str(value)


def load_resolvent(path: Path) -> ResolventData:
    with h5py.File(path, "r") as f:
        component_names = tuple(
            part.strip()
            for part in _decode_attr(f.attrs.get("component_names"), ",".join(COMPONENT_NAMES)).split(",")
            if part.strip()
        )
        return ResolventData(
            z=f["geometry/z_wall"][:],
            omega=f["frequencies/omega"][:],
            kappa=float(f["mode/kappa"][()]),
            lambda_=float(f["mode/lambda"][()]),
            singular_values=f["resolvent/singular_values"][:],
            response_modes=f["resolvent/response_modes"][:],
            forcing_modes=f["resolvent/forcing_modes"][:],
            response_energy_density=f["resolvent/response_energy_density"][:],
            critical_z=f["critical_layers/z"][:],
            critical_count=f["critical_layers/count"][:],
            component_names=component_names or COMPONENT_NAMES,
        )


def validate_indices(data: ResolventData, omega_index: int, singular_index: int) -> None:
    n_omega, n_singular = data.singular_values.shape
    if omega_index < 0 or omega_index >= n_omega:
        raise IndexError(f"omega-index {omega_index} is outside [0, {n_omega})")
    if singular_index < 0 or singular_index >= n_singular:
        raise IndexError(f"singular-index {singular_index} is outside [0, {n_singular})")


def mode_components(vector: np.ndarray, nz: int) -> np.ndarray:
    if vector.shape[-1] != 3 * nz:
        raise ValueError(f"expected modal vector length {3 * nz}, got {vector.shape[-1]}")
    return vector.reshape(nz, 3)


def sorted_z_and_array(z: np.ndarray, array: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    order = np.argsort(z)
    return z[order], array[order]


def figure_path(figure_dir: Path, name: str) -> Path:
    figure_dir.mkdir(parents=True, exist_ok=True)
    return figure_dir / name


def save(fig: plt.Figure, path: Path) -> None:
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote={path}")


def plot_mode_shapes(
    data: ResolventData,
    figure_dir: Path,
    omega_index: int,
    n_shapes: int,
) -> None:
    n_available = data.singular_values.shape[1]
    n_plot = min(max(n_shapes, 1), n_available)
    z_sorted = np.sort(data.z)

    fig, axes = plt.subplots(2, 3, figsize=(8.1, 5.9), sharey=True, constrained_layout=True)
    for singular_index in range(n_plot):
        response = mode_components(data.response_modes[omega_index, singular_index], data.z.size)
        forcing = mode_components(data.forcing_modes[omega_index, singular_index], data.z.size)
        _, response_sorted = sorted_z_and_array(data.z, response)
        _, forcing_sorted = sorted_z_and_array(data.z, forcing)
        label = rf"$j={singular_index + 1}$"
        for component in range(3):
            axes[0, component].plot(
                np.abs(response_sorted[:, component]),
                z_sorted,
                linewidth=1.4,
                label=label,
            )
            axes[1, component].plot(
                np.abs(forcing_sorted[:, component]),
                z_sorted,
                linewidth=1.4,
                label=label,
            )

    omega_value = data.omega[omega_index]
    for component in range(3):
        axes[0, component].set_title(rf"response {COMPONENT_LABELS[component]}")
        axes[1, component].set_title(rf"forcing {COMPONENT_LABELS[component]}")
        axes[1, component].set_xlabel(r"amplitude")
        for row in range(2):
            axes[row, component].grid(True, color="0.9")
            axes[row, component].legend(frameon=False, fontsize=8)
    axes[0, 0].set_ylabel(r"$z/h$")
    axes[1, 0].set_ylabel(r"$z/h$")
    fig.suptitle(rf"Mode shapes at $\omega={omega_value:.4g}$")
    save(fig, figure_path(figure_dir, FIGURE_NAMES[0]))


def plot_gain_bode(data: ResolventData, figure_dir: Path) -> None:
    fig, ax = plt.subplots(figsize=(5.8, 3.8), constrained_layout=True)
    for singular_index in range(data.singular_values.shape[1]):
        ax.plot(
            data.omega,
            data.singular_values[:, singular_index],
            marker="o",
            markersize=3.5,
            linewidth=1.3,
            label=rf"$\sigma_{singular_index + 1}$",
        )
    if np.all(data.singular_values > 0.0):
        ax.set_yscale("log")
    ax.set_xlabel(r"$\omega$")
    ax.set_ylabel(r"singular value")
    ax.grid(True, color="0.9", which="both")
    ax.legend(frameon=False, ncols=2, fontsize=8)
    save(fig, figure_path(figure_dir, FIGURE_NAMES[1]))


def plot_peak_location_gain(data: ResolventData, figure_dir: Path) -> None:
    leading_density = data.response_energy_density[:, 0, :]
    peak_indices = np.argmax(leading_density, axis=1)
    peak_z = data.z[peak_indices]
    leading_gain = data.singular_values[:, 0]

    if abs(data.kappa) > 1e-14:
        x_values = data.omega / data.kappa
        x_label = r"$c=\omega/\kappa$"
    else:
        x_values = data.omega
        x_label = r"$\omega$"

    fig, axes = plt.subplots(1, 2, figsize=(8.0, 3.4), constrained_layout=True)
    axes[0].plot(x_values, peak_z, marker="o", linewidth=1.4, label=r"energy peak")
    critical_x = []
    critical_y = []
    for index, count in enumerate(data.critical_count):
        roots = data.critical_z[index, :count]
        finite = roots[np.isfinite(roots)]
        if finite.size:
            critical_x.extend([x_values[index]] * finite.size)
            critical_y.extend(finite.tolist())
    if critical_x:
        axes[0].scatter(critical_x, critical_y, s=22, color="black", marker="x", label=r"critical layer")
    axes[0].set_xlabel(x_label)
    axes[0].set_ylabel(r"$z/h$")
    axes[0].grid(True, color="0.9")
    axes[0].legend(frameon=False)

    axes[1].plot(x_values, leading_gain, marker="o", linewidth=1.4, color="tab:purple")
    if np.all(leading_gain > 0.0):
        axes[1].set_yscale("log")
    axes[1].set_xlabel(x_label)
    axes[1].set_ylabel(r"$\sigma_1$")
    axes[1].grid(True, color="0.9", which="both")
    save(fig, figure_path(figure_dir, FIGURE_NAMES[2]))


def _slice_extent(wavenumber: float) -> float:
    if abs(wavenumber) > 1e-14:
        return float(2.0 * np.pi / abs(wavenumber))
    return float(2.0 * np.pi)


def plot_reconstructed_fields(
    data: ResolventData,
    figure_dir: Path,
    omega_index: int,
    singular_index: int,
    phase: float,
    n_stream: int,
    n_span: int,
) -> None:
    n_stream = max(n_stream, 2)
    n_span = max(n_span, 2)
    components = mode_components(data.response_modes[omega_index, singular_index], data.z.size)
    z_sorted, components_sorted = sorted_z_and_array(data.z, components)

    x = np.linspace(0.0, _slice_extent(data.kappa), n_stream)
    y = np.linspace(0.0, _slice_extent(data.lambda_), n_span)
    x_grid, xz_grid = np.meshgrid(x, z_sorted)
    y_grid, yz_grid = np.meshgrid(y, z_sorted)
    exp_x = np.exp(1j * (data.kappa * x + phase))
    exp_y = np.exp(1j * (data.lambda_ * y + phase))

    fig, axes = plt.subplots(3, 2, figsize=(8.2, 7.0), sharey=True, constrained_layout=True)
    for component in range(3):
        xz_field = np.real(components_sorted[:, component, None] * exp_x[None, :])
        yz_field = np.real(components_sorted[:, component, None] * exp_y[None, :])
        vmax = max(float(np.max(np.abs(xz_field))), float(np.max(np.abs(yz_field))), 1e-14)
        im0 = axes[component, 0].pcolormesh(
            x_grid,
            xz_grid,
            xz_field,
            shading="auto",
            cmap="RdBu_r",
            vmin=-vmax,
            vmax=vmax,
            rasterized=True,
        )
        im1 = axes[component, 1].pcolormesh(
            y_grid,
            yz_grid,
            yz_field,
            shading="auto",
            cmap="RdBu_r",
            vmin=-vmax,
            vmax=vmax,
            rasterized=True,
        )
        axes[component, 0].set_ylabel(r"$z/h$")
        axes[component, 0].set_title(rf"{COMPONENT_LABELS[component]}(x,z), y=0")
        axes[component, 1].set_title(rf"{COMPONENT_LABELS[component]}(y,z), x=0")
        fig.colorbar(im0, ax=axes[component, 0], fraction=0.046, pad=0.02)
        fig.colorbar(im1, ax=axes[component, 1], fraction=0.046, pad=0.02)
    axes[-1, 0].set_xlabel(r"$x/h$")
    axes[-1, 1].set_xlabel(r"$y/h$")
    omega_value = data.omega[omega_index]
    fig.suptitle(
        rf"response mode $j={singular_index + 1}$, $\omega={omega_value:.4g}$, phase={phase:.3g}"
    )
    save(fig, figure_path(figure_dir, FIGURE_NAMES[3]))


def plot_all(
    resolvent_h5: Path,
    figure_dir: Path,
    omega_index: int,
    singular_index: int,
    n_shapes: int,
    phase: float,
    n_stream: int,
    n_span: int,
    no_tex: bool,
) -> list[Path]:
    configure_matplotlib(no_tex)
    data = load_resolvent(resolvent_h5)
    validate_indices(data, omega_index, singular_index)
    figure_dir.mkdir(parents=True, exist_ok=True)
    plot_mode_shapes(data, figure_dir, omega_index, n_shapes)
    plot_gain_bode(data, figure_dir)
    plot_peak_location_gain(data, figure_dir)
    plot_reconstructed_fields(
        data,
        figure_dir,
        omega_index,
        singular_index,
        phase,
        n_stream,
        n_span,
    )
    return [figure_dir / name for name in FIGURE_NAMES]


def main() -> int:
    args = parse_args()
    plot_all(
        Path(args.resolvent_h5).expanduser().resolve(),
        Path(args.figure_dir).expanduser().resolve(),
        args.omega_index,
        args.singular_index,
        args.n_shapes,
        args.phase,
        args.n_stream,
        args.n_span,
        args.no_tex,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
