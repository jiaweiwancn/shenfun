#!/usr/bin/env python
"""Compute plane-averaged velocity auto-spectrum from MKM samples.

For each target velocity component and wall-normal level, this estimates a
two-sided angular-frequency spectrum

    S_i(omega, z) = mean_{x,y} periodogram_t[u_i'(t, x, y, z)],

using the normalization consistent with

    R_i(0, z) ~= (1 / 2pi) integral S_i(omega, z) d omega.

The horizontal average is taken over points with the same wall-normal
coordinate z.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import h5py
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
    "axes.unicode_minus": False,
})


COMPONENT_GROUPS = ("u1", "u2", "u0")
COMPONENT_NAMES = ("streamwise", "spanwise", "wallnormal")
COMPONENT_SYMBOLS = (r"x", r"y", r"z")


@dataclass(frozen=True)
class TargetMetadata:
    mean_profile: np.ndarray
    z_wall: np.ndarray
    times: np.ndarray
    dt: float | None


def sorted_snapshot_keys(f: h5py.File) -> list[str]:
    keys = sorted(f["u0/3D"].keys(), key=lambda key: int(key))
    for group in ("u1", "u2"):
        other = sorted(f[f"{group}/3D"].keys(), key=lambda key: int(key))
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


def finite_or_none(value: float | None) -> float | None:
    if value is None:
        return None
    if not np.isfinite(value):
        return None
    return float(value)


def read_target_metadata(path: Path) -> TargetMetadata:
    with h5py.File(path, "r") as f:
        mean_profile = f["mean_profile"][:].T
        z_wall = f["geometry/z_wall"][:]
        times = f["sampling/t"][:]
        dt = finite_or_none(f.attrs.get("dt"))
    return TargetMetadata(
        mean_profile=mean_profile,
        z_wall=z_wall,
        times=times,
        dt=dt,
    )


def keys_matching_target_times(keys: list[str], target_times: np.ndarray, dt: float) -> list[str]:
    available = {int(key): key for key in keys}
    target_steps = [int(round(float(t) / dt)) for t in target_times]
    missing = [step for step in target_steps if step not in available]
    if missing:
        preview = ", ".join(str(step) for step in missing[:5])
        raise ValueError(f"velocity file is missing {len(missing)} target time steps: {preview}")
    return [available[step] for step in target_steps]


def accumulate_mean_profile(f: h5py.File, keys: Iterable[str]) -> np.ndarray:
    keys = list(keys)
    first = f[f"{COMPONENT_GROUPS[0]}/3D/{keys[0]}"]
    nz = first.shape[0]
    mean = np.zeros((len(COMPONENT_GROUPS), nz), dtype=np.float64)
    for key in keys:
        for component, group in enumerate(COMPONENT_GROUPS):
            mean[component] += f[f"{group}/3D/{key}"][:].mean(axis=(1, 2))
    mean /= len(keys)
    return mean


def sample_times_from_keys(keys: list[str], dt: float) -> np.ndarray:
    return np.array([int(key) * dt for key in keys], dtype=np.float64)


def uniform_sample_spacing(times: np.ndarray) -> float:
    if len(times) < 2:
        raise ValueError("at least two snapshots are needed for a temporal spectrum")
    spacing = np.diff(times)
    sample_dt = float(np.median(spacing))
    if not np.allclose(spacing, sample_dt, rtol=1e-9, atol=1e-11):
        raise ValueError("selected snapshots are not uniformly spaced in time")
    return sample_dt


def temporal_window(kind: str, n: int) -> np.ndarray:
    if kind == "none":
        return np.ones(n, dtype=np.float64)
    if kind == "hann":
        return np.hanning(n).astype(np.float64)
    raise ValueError(f"unknown temporal window {kind!r}")


def autospectrum_fft(block: np.ndarray, sample_dt: float, window: np.ndarray) -> np.ndarray:
    """Return two-sided spectrum with shape (nt, z_batch)."""
    nt, _, _, _ = block.shape
    weighted = block * window[:, None, None, None]
    freq = np.fft.fft(weighted, axis=0)
    power = np.einsum("tzxy,tzxy->tz", freq.real, freq.real, optimize=True)
    power += np.einsum("tzxy,tzxy->tz", freq.imag, freq.imag, optimize=True)
    horizontal_count = block.shape[2] * block.shape[3]
    window_energy = float(np.sum(window * window))
    return sample_dt * power / (window_energy * horizontal_count)


def compute_velocity_autospectrum(
    f: h5py.File,
    keys: list[str],
    mean_profile: np.ndarray,
    sample_dt: float,
    z_batch: int,
    window_kind: str,
) -> tuple[np.ndarray, np.ndarray]:
    first = f[f"{COMPONENT_GROUPS[0]}/3D/{keys[0]}"]
    nz, nx, ny = first.shape
    nt = len(keys)
    if mean_profile.shape != (len(COMPONENT_GROUPS), nz):
        raise ValueError(
            f"mean profile shape {mean_profile.shape} does not match "
            f"({len(COMPONENT_GROUPS)}, {nz})"
        )

    window = temporal_window(window_kind, nt)
    omega = 2.0 * np.pi * np.fft.fftfreq(nt, d=sample_dt)
    order = np.argsort(omega)
    spectrum = np.empty((nt, nz, len(COMPONENT_GROUPS)), dtype=np.float64)
    z_batch = max(1, min(z_batch, nz))
    for component, group in enumerate(COMPONENT_GROUPS):
        print(f"component={COMPONENT_NAMES[component]}")
        for z0 in range(0, nz, z_batch):
            z1 = min(nz, z0 + z_batch)
            block = np.empty((nt, z1 - z0, nx, ny), dtype=np.float64)
            for n, key in enumerate(keys):
                values = f[f"{group}/3D/{key}"][z0:z1, :, :]
                block[n] = values - mean_profile[component, z0:z1, None, None]
            spectrum[:, z0:z1, component] = autospectrum_fft(block, sample_dt, window)[order]
            print(f"  z_batch={z0}:{z1}")
    return omega[order], spectrum


def nearest_z_indices(z: np.ndarray, selected_z: Iterable[float]) -> list[int]:
    indices = []
    for value in selected_z:
        idx = int(np.argmin(np.abs(z - value)))
        if idx not in indices:
            indices.append(idx)
    return sorted(indices, key=lambda idx: z[idx])


def write_output(
    output: Path,
    omega: np.ndarray,
    spectrum: np.ndarray,
    z_wall: np.ndarray,
    selected_times: np.ndarray,
    selected_keys: list[str],
    source_velocity_h5: Path,
    target_h5: Path | None,
    window_kind: str,
) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        output.unlink()

    with h5py.File(output, "w") as f:
        f.attrs["source_velocity_h5"] = str(source_velocity_h5)
        if target_h5 is not None:
            f.attrs["source_target_h5"] = str(target_h5)
        f.attrs["component_order"] = ",".join(COMPONENT_NAMES)
        f.attrs["estimator"] = "two-sided plane-averaged temporal periodogram"
        f.attrs["normalization"] = "S = dt/sum(window^2) * mean_xy(|FFT_t(window*u_i')|^2)"
        f.attrs["fourier_convention"] = "R(0,z) ~= (1/(2*pi))*sum_omega S(omega,z)*Delta_omega"
        f.attrs["horizontal_average"] = "x-y plane at fixed z"
        f.attrs["temporal_window"] = window_kind
        f.create_dataset("sampling/t", data=selected_times)
        key_dtype = h5py.string_dtype(encoding="utf-8")
        f.create_dataset("sampling/snapshot_keys", data=np.array(selected_keys, dtype=object), dtype=key_dtype)
        f.create_dataset("omega", data=omega)
        f.create_dataset("geometry/z_wall", data=z_wall)
        ds = f.create_dataset("autospectrum", data=spectrum)
        ds.attrs["axes"] = "omega,z,component"
        ds.attrs["component_order"] = ",".join(COMPONENT_NAMES)


def plot_selected_z(
    spectrum_h5: Path,
    figure: Path,
    selected_z: Iterable[float],
    positive_omega: bool,
    logx: bool,
    logy: bool,
    max_omega: float | None,
    half_height: float,
    friction_velocity: float,
    normalize_by_variance: bool,
    reference_slope: float | None,
    reference_omega_range: tuple[float, float] | None,
) -> None:
    with h5py.File(spectrum_h5, "r") as f:
        z = f["geometry/z_wall"][:]
        omega = f["omega"][:]
        spectrum = f["autospectrum"][:]

    if normalize_by_variance:
        if len(omega) < 2:
            raise ValueError("at least two omega points are needed for variance normalization")
        delta_omega = float(np.median(np.diff(omega)))
        variance = spectrum.sum(axis=0) * delta_omega / (2.0 * np.pi)
        with np.errstate(divide="ignore", invalid="ignore"):
            spectrum = spectrum * friction_velocity / (half_height * variance[None, :, :])
    else:
        spectrum = spectrum / (friction_velocity * half_height)

    omega = omega * half_height / friction_velocity
    z_plot = z / half_height
    if max_omega is not None:
        max_omega = max_omega * half_height / friction_velocity
    if positive_omega:
        keep = omega >= -1e-12
        omega = omega[keep]
        spectrum = spectrum[keep]
    if logx:
        keep = omega > 0.0
        omega = omega[keep]
        spectrum = spectrum[keep]
    if max_omega is not None:
        keep = omega <= max_omega + 1e-12
        omega = omega[keep]
        spectrum = spectrum[keep]

    indices = nearest_z_indices(z, selected_z)
    fig, axes = plt.subplots(3, 1, figsize=(7.0, 7.8), sharex=True)
    for component, ax in enumerate(axes):
        for idx in indices:
            ax.plot(omega, spectrum[:, idx, component], label=rf"$z/h={z_plot[idx]:.4g}$")
        if reference_slope is not None:
            reference_label = (
                r"$\omega^{-5/3}$"
                if np.isclose(reference_slope, -5.0 / 3.0)
                else rf"$\omega^{{{reference_slope:.3g}}}$"
            )
            add_reference_slope(
                ax=ax,
                omega=omega,
                values=spectrum[:, indices, component],
                slope=reference_slope,
                omega_range=reference_omega_range,
                label=reference_label if component == 0 else None,
            )
        if logx:
            ax.set_xscale("log")
        if logy:
            ax.set_yscale("log")
        ylabel = (
            r"$S_{ii}u_\tau/[hR_{ii}(0;z)]$"
            if normalize_by_variance
            else r"$S_{ii}/(u_\tau h)$"
        )
        ax.set_ylabel(ylabel)
        ax.text(
            0.02,
            0.08,
            rf"$i={COMPONENT_SYMBOLS[component]}$",
            transform=ax.transAxes,
            ha="left",
            va="bottom",
        )
        ax.grid(True, color="0.9")
    axes[-1].set_xlabel(r"$\omega h/u_\tau$")
    legend_count = len(indices) + (1 if reference_slope is not None else 0)
    axes[0].legend(ncols=min(4, legend_count), frameon=False, loc="best")
    fig.tight_layout()
    figure.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(figure, bbox_inches="tight")
    plt.close(fig)


def add_reference_slope(
    ax: plt.Axes,
    omega: np.ndarray,
    values: np.ndarray,
    slope: float,
    omega_range: tuple[float, float] | None,
    label: str | None,
) -> None:
    finite_omega = omega[np.isfinite(omega) & (omega > 0.0)]
    finite_values = values[np.isfinite(values) & (values > 0.0)]
    if finite_omega.size < 2 or finite_values.size == 0:
        return

    if omega_range is None:
        log_omega = np.log10(finite_omega)
        x0 = float(10.0 ** np.quantile(log_omega, 0.38))
        x1 = float(10.0 ** np.quantile(log_omega, 0.56))
    else:
        x0, x1 = sorted(float(value) for value in omega_range)

    if x0 <= 0.0 or x1 <= x0:
        return

    local = (omega >= x0) & (omega <= x1)
    local_values = values[local]
    local_values = local_values[np.isfinite(local_values) & (local_values > 0.0)]
    if local_values.size == 0:
        local_values = finite_values

    x_mid = float(np.sqrt(x0 * x1))
    y_mid = float(np.quantile(local_values, 0.75))
    x_ref = np.array([x0, x1], dtype=np.float64)
    y_ref = y_mid * (x_ref / x_mid) ** slope
    ax.plot(x_ref, y_ref, color="0.15", linestyle="--", linewidth=1.2, label=label)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--velocity-h5", required=True, help="Input MKM *_U.h5 file.")
    parser.add_argument("--output", required=True, help="Output HDF5 file for auto-spectrum.")
    parser.add_argument("--target-h5", help="Optional target HDF5 file; supplies mean profile and sample times.")
    parser.add_argument("--dt", type=float, help="DNS solver timestep used to convert HDF5 keys to time.")
    parser.add_argument("--t-min", type=float, help="Minimum physical sample time when no target times are used.")
    parser.add_argument("--t-max", type=float, help="Maximum physical sample time when no target times are used.")
    parser.add_argument("--skip-snapshots", type=int, default=0)
    parser.add_argument("--snapshot-stride", type=int, default=1)
    parser.add_argument("--max-snapshots", type=int)
    parser.add_argument("--z-batch", type=int, default=4, help="Number of z levels processed per FFT batch.")
    parser.add_argument("--window", choices=("none", "hann"), default="none", help="Temporal periodogram window.")
    parser.add_argument("--recompute-mean", action="store_true",
                        help="Ignore target mean_profile and recompute the mean from selected snapshots.")
    parser.add_argument("--figure", help="Selected-z plot path. Default: OUTPUT with suffix _selected_z.pdf.")
    parser.add_argument("--selected-z", type=float, nargs="*", default=[0.025, 0.5, 0.9],
                        help="Wall-normal coordinates to plot; nearest saved z levels are used.")
    parser.add_argument("--two-sided-plot", action="store_true",
                        help="Plot the full two-sided angular-frequency axis instead of omega >= 0.")
    parser.add_argument("--log-x", action="store_true",
                        help="Use a logarithmic omega axis for the selected-z plot.")
    parser.add_argument("--linear-y", action="store_true", help="Use a linear y-axis instead of log scale.")
    parser.add_argument("--max-plot-omega", type=float, help="Optional omega limit for the figure only.")
    parser.add_argument("--half-height", type=float, default=1.0)
    parser.add_argument("--friction-velocity", type=float, default=1.0)
    parser.add_argument("--normalize-by-variance", action="store_true",
                        help="Plot S_ii*u_tau/(h*R_ii(0,z)) instead of S_ii/(u_tau*h).")
    parser.add_argument("--reference-slope", type=float,
                        help="Optional log-log reference slope, for example -1.6666667.")
    parser.add_argument("--reference-omega-range", type=float, nargs=2,
                        help="Optional reference-line omega range on the plotted omega*h/u_tau axis.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    velocity_h5 = Path(args.velocity_h5).expanduser().resolve()
    output = Path(args.output).expanduser().resolve()
    target_h5 = Path(args.target_h5).expanduser().resolve() if args.target_h5 else None
    target = read_target_metadata(target_h5) if target_h5 else None

    dt = args.dt
    if dt is None and target is not None:
        dt = target.dt
    if dt is None:
        raise ValueError("--dt is required when --target-h5 does not provide a dt attribute")

    with h5py.File(velocity_h5, "r") as f:
        all_keys = sorted_snapshot_keys(f)
        if target is not None:
            keys = keys_matching_target_times(all_keys, target.times, dt)
            keys = keys[args.skip_snapshots :: args.snapshot_stride]
            if args.max_snapshots is not None:
                keys = keys[: args.max_snapshots]
        else:
            keys = select_keys(
                all_keys,
                skip=args.skip_snapshots,
                stride=args.snapshot_stride,
                max_snapshots=args.max_snapshots,
                dt=dt,
                t_min=args.t_min,
                t_max=args.t_max,
            )
        if not keys:
            raise ValueError("no snapshots selected")

        selected_times = sample_times_from_keys(keys, dt)
        sample_dt = uniform_sample_spacing(selected_times)
        if target is not None and not args.recompute_mean:
            mean_profile = target.mean_profile
            z_wall = target.z_wall
            velocity_z = f["u0/mesh/x0"][:]
            if z_wall.shape != velocity_z.shape or not np.allclose(z_wall, velocity_z):
                raise ValueError("target geometry/z_wall does not match the velocity file wall-normal grid")
        else:
            mean_profile = accumulate_mean_profile(f, keys)
            z_wall = f["u0/mesh/x0"][:]

        print(f"snapshots={len(keys)}")
        print(f"sample_time_range={selected_times[0]:.12g},{selected_times[-1]:.12g}")
        print(f"sample_dt={sample_dt:.12g}")
        print(f"window={args.window}")
        omega, spectrum = compute_velocity_autospectrum(
            f,
            keys=keys,
            mean_profile=mean_profile,
            sample_dt=sample_dt,
            z_batch=args.z_batch,
            window_kind=args.window,
        )

    write_output(
        output=output,
        omega=omega,
        spectrum=spectrum,
        z_wall=z_wall,
        selected_times=selected_times,
        selected_keys=keys,
        source_velocity_h5=velocity_h5,
        target_h5=target_h5,
        window_kind=args.window,
    )

    figure = Path(args.figure).expanduser().resolve() if args.figure else output.with_name(f"{output.stem}_selected_z.pdf")
    plot_selected_z(
        spectrum_h5=output,
        figure=figure,
        selected_z=args.selected_z,
        positive_omega=not args.two_sided_plot,
        logx=args.log_x,
        logy=not args.linear_y,
        max_omega=args.max_plot_omega,
        half_height=args.half_height,
        friction_velocity=args.friction_velocity,
        normalize_by_variance=args.normalize_by_variance,
        reference_slope=args.reference_slope,
        reference_omega_range=tuple(args.reference_omega_range) if args.reference_omega_range else None,
    )
    print(f"wrote={output}")
    print(f"figure={figure}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
