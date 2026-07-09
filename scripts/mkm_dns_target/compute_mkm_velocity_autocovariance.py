#!/usr/bin/env python
"""Compute plane-averaged velocity auto-covariance from MKM samples.

For each target velocity component and wall-normal level, this estimates

    R_i(z, tau_s) = <u_i'(t + tau_s, x, y, z) u_i'(t, x, y, z)>_{t,x,y},

using the unbiased positive-lag denominator.  The horizontal average is taken
over points with the same wall-normal coordinate z.
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
        raise ValueError("at least two snapshots are needed for lag covariance")
    spacing = np.diff(times)
    sample_dt = float(np.median(spacing))
    if not np.allclose(spacing, sample_dt, rtol=1e-9, atol=1e-11):
        raise ValueError("selected snapshots are not uniformly spaced in time")
    return sample_dt


def next_power_of_two(n: int) -> int:
    return 1 << (n - 1).bit_length()


def autocovariance_fft(block: np.ndarray, max_lag: int) -> np.ndarray:
    """Return covariance with shape (max_lag + 1, z_batch)."""
    nt, _, nx, ny = block.shape
    nfft = next_power_of_two(2 * nt - 1)
    freq = np.fft.rfft(block, n=nfft, axis=0)
    power_sum = np.einsum("lzxy,lzxy->lz", freq.real, freq.real, optimize=True)
    power_sum += np.einsum("lzxy,lzxy->lz", freq.imag, freq.imag, optimize=True)
    corr_sum = np.fft.irfft(power_sum, n=nfft, axis=0)[: max_lag + 1]
    denom = (nt - np.arange(max_lag + 1, dtype=np.float64))[:, None] * (nx * ny)
    return corr_sum / denom


def compute_velocity_autocovariance(
    f: h5py.File,
    keys: list[str],
    mean_profile: np.ndarray,
    max_lag: int,
    z_batch: int,
) -> np.ndarray:
    first = f[f"{COMPONENT_GROUPS[0]}/3D/{keys[0]}"]
    nz, nx, ny = first.shape
    nt = len(keys)
    if max_lag >= nt:
        raise ValueError("--max-lag must be smaller than the selected snapshot count")
    if mean_profile.shape != (len(COMPONENT_GROUPS), nz):
        raise ValueError(
            f"mean profile shape {mean_profile.shape} does not match "
            f"({len(COMPONENT_GROUPS)}, {nz})"
        )

    z_batch = max(1, min(z_batch, nz))
    cov = np.empty((max_lag + 1, nz, len(COMPONENT_GROUPS)), dtype=np.float64)
    for component, group in enumerate(COMPONENT_GROUPS):
        print(f"component={COMPONENT_NAMES[component]}")
        for z0 in range(0, nz, z_batch):
            z1 = min(nz, z0 + z_batch)
            block = np.empty((nt, z1 - z0, nx, ny), dtype=np.float64)
            for n, key in enumerate(keys):
                values = f[f"{group}/3D/{key}"][z0:z1, :, :]
                block[n] = values - mean_profile[component, z0:z1, None, None]
            cov[:, z0:z1, component] = autocovariance_fft(block, max_lag)
            print(f"  z_batch={z0}:{z1}")
    return cov


def nearest_z_indices(z: np.ndarray, selected_z: Iterable[float]) -> list[int]:
    indices = []
    for value in selected_z:
        idx = int(np.argmin(np.abs(z - value)))
        if idx not in indices:
            indices.append(idx)
    return sorted(indices, key=lambda idx: z[idx])


def write_output(
    output: Path,
    cov: np.ndarray,
    z_wall: np.ndarray,
    selected_times: np.ndarray,
    selected_keys: list[str],
    source_velocity_h5: Path,
    target_h5: Path | None,
    max_lag: int,
) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        output.unlink()

    sample_dt = uniform_sample_spacing(selected_times)
    lag_index = np.arange(max_lag + 1, dtype=np.int64)
    lag_time = lag_index.astype(np.float64) * sample_dt
    variance = cov[0:1]
    with np.errstate(divide="ignore", invalid="ignore"):
        corr = cov / np.where(np.abs(variance) > 0.0, variance, np.nan)

    with h5py.File(output, "w") as f:
        f.attrs["source_velocity_h5"] = str(source_velocity_h5)
        if target_h5 is not None:
            f.attrs["source_target_h5"] = str(target_h5)
        f.attrs["component_order"] = ",".join(COMPONENT_NAMES)
        f.attrs["estimator"] = "unbiased positive-lag plane-averaged covariance"
        f.attrs["formula"] = "mean_{t,x,y} u_i'(t+lag,x,y,z) u_i'(t,x,y,z)"
        f.attrs["horizontal_average"] = "x-y plane at fixed z"
        f.create_dataset("sampling/t", data=selected_times)
        key_dtype = h5py.string_dtype(encoding="utf-8")
        f.create_dataset("sampling/snapshot_keys", data=np.array(selected_keys, dtype=object), dtype=key_dtype)
        f.create_dataset("lag_index", data=lag_index)
        f.create_dataset("lag_time", data=lag_time)
        f.create_dataset("geometry/z_wall", data=z_wall)
        ds = f.create_dataset("autocovariance", data=cov)
        ds.attrs["axes"] = "lag,z,component"
        ds.attrs["component_order"] = ",".join(COMPONENT_NAMES)
        ds = f.create_dataset("autocorrelation", data=corr)
        ds.attrs["axes"] = "lag,z,component"
        ds.attrs["normalization"] = "autocovariance(lag,z,component)/autocovariance(0,z,component)"


def plot_selected_z(
    autocov_h5: Path,
    figure: Path,
    selected_z: Iterable[float],
    normalize: bool,
    max_lag_time: float | None,
    half_height: float,
    friction_velocity: float,
) -> None:
    with h5py.File(autocov_h5, "r") as f:
        z = f["geometry/z_wall"][:]
        lag_time = f["lag_time"][:]
        dataset_name = "autocorrelation" if normalize else "autocovariance"
        values = f[dataset_name][:]

    lag_time = lag_time * friction_velocity / half_height
    z_plot = z / half_height
    if not normalize:
        values = values / friction_velocity**2
    if max_lag_time is not None:
        max_lag_time = max_lag_time * friction_velocity / half_height
    if max_lag_time is not None:
        keep = lag_time <= max_lag_time + 1e-12
        lag_time = lag_time[keep]
        values = values[keep]

    indices = nearest_z_indices(z, selected_z)
    fig, axes = plt.subplots(3, 1, figsize=(7.0, 7.8), sharex=True)
    ylabel = (
        r"$R_{ii}(\tau;z)/R_{ii}(0;z)$"
        if normalize
        else r"$R_{ii}(\tau;z)/u_\tau^2$"
    )
    for component, ax in enumerate(axes):
        for idx in indices:
            ax.plot(lag_time, values[:, idx, component], label=rf"$z/h={z_plot[idx]:.4g}$")
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
    axes[-1].set_xlabel(r"$\tau u_\tau/h$")
    axes[0].legend(ncols=min(3, len(indices)), frameon=False, loc="best")
    fig.tight_layout()
    figure.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(figure, bbox_inches="tight")
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--velocity-h5", required=True, help="Input MKM *_U.h5 file.")
    parser.add_argument("--output", required=True, help="Output HDF5 file for auto-covariance.")
    parser.add_argument("--target-h5", help="Optional target HDF5 file; supplies mean profile and sample times.")
    parser.add_argument("--dt", type=float, help="DNS solver timestep used to convert HDF5 keys to time.")
    parser.add_argument("--t-min", type=float, help="Minimum physical sample time when no target times are used.")
    parser.add_argument("--t-max", type=float, help="Maximum physical sample time when no target times are used.")
    parser.add_argument("--skip-snapshots", type=int, default=0)
    parser.add_argument("--snapshot-stride", type=int, default=1)
    parser.add_argument("--max-snapshots", type=int)
    parser.add_argument("--max-lag", type=int, help="Maximum lag in selected-snapshot steps. Default: all lags.")
    parser.add_argument("--z-batch", type=int, default=4, help="Number of z levels processed per FFT batch.")
    parser.add_argument("--recompute-mean", action="store_true",
                        help="Ignore target mean_profile and recompute the mean from selected snapshots.")
    parser.add_argument("--figure", help="Selected-z plot path. Default: OUTPUT with suffix _selected_z.pdf.")
    parser.add_argument("--selected-z", type=float, nargs="*", default=[0.025, 0.5, 0.9],
                        help="Wall-normal coordinates to plot; nearest saved z levels are used.")
    parser.add_argument("--normalize-plot", action="store_true",
                        help="Plot R(tau)/R(0) instead of the raw auto-covariance.")
    parser.add_argument("--max-plot-lag-time", type=float, help="Optional lag-time limit for the figure only.")
    parser.add_argument("--half-height", type=float, default=1.0)
    parser.add_argument("--friction-velocity", type=float, default=1.0)
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
        max_lag = len(keys) - 1 if args.max_lag is None else args.max_lag
        if max_lag >= len(keys):
            raise ValueError("--max-lag must be smaller than the selected snapshot count")

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
        print(f"max_lag={max_lag}")
        cov = compute_velocity_autocovariance(
            f,
            keys=keys,
            mean_profile=mean_profile,
            max_lag=max_lag,
            z_batch=args.z_batch,
        )

    write_output(
        output=output,
        cov=cov,
        z_wall=z_wall,
        selected_times=selected_times,
        selected_keys=keys,
        source_velocity_h5=velocity_h5,
        target_h5=target_h5,
        max_lag=max_lag,
    )

    figure = Path(args.figure).expanduser().resolve() if args.figure else output.with_name(f"{output.stem}_selected_z.pdf")
    plot_selected_z(
        autocov_h5=output,
        figure=figure,
        selected_z=args.selected_z,
        normalize=args.normalize_plot,
        max_lag_time=args.max_plot_lag_time,
        half_height=args.half_height,
        friction_velocity=args.friction_velocity,
    )
    print(f"wrote={output}")
    print(f"figure={figure}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
