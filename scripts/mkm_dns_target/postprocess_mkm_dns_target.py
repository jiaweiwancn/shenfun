#!/usr/bin/env python
"""Postprocess MKM HDF5 snapshots into the data-estimated target objects."""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
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
    data = np.stack(fields, axis=0)  # component, z, stream, span
    if mean_profile is not None:
        data = data - mean_profile[:, :, None, None]
    return data


def modal_vectors(fluctuation: np.ndarray) -> np.ndarray:
    _, nz, nx, ny = fluctuation.shape
    uhat = np.fft.fft2(fluctuation, axes=(2, 3)) / (nx * ny)
    return np.transpose(uhat, (2, 3, 1, 0)).reshape(nx, ny, 3 * nz)


def accumulate_mean_and_reynolds(f: h5py.File, keys: Iterable[str]) -> tuple[np.ndarray, np.ndarray]:
    keys = list(keys)
    first = read_snapshot(f, keys[0])
    ncomp, nz, _, _ = first.shape
    mean = np.zeros((ncomp, nz), dtype=float)
    for key in keys:
        data = read_snapshot(f, key)
        mean += data.mean(axis=(2, 3))
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


def write_modal_covariance(
    f_in: h5py.File,
    f_out: h5py.File,
    keys: list[str],
    mean: np.ndarray,
    mode_batch: int,
    store_modal_coefficients: bool,
    max_lag: int,
) -> None:
    sample = read_snapshot(f_in, keys[0], mean)
    _, nz, nx, ny = sample.shape
    modal_dim = 3 * nz

    modal_group = f_out.require_group("modal")
    b0 = modal_group.create_dataset(
        "B0_DNS",
        shape=(nx, ny, modal_dim, modal_dim),
        dtype=np.complex128,
        chunks=(1, 1, modal_dim, modal_dim),
    )
    modal_group.create_dataset("mode_energy", shape=(nx, ny), dtype=float)

    coeffs = None
    if store_modal_coefficients or max_lag >= 0:
        coeffs = modal_group.create_dataset(
            "u_hat",
            shape=(len(keys), nx, ny, modal_dim),
            dtype=np.complex128,
            chunks=(1, max(1, min(nx, 4)), ny, modal_dim),
        )
        for n, key in enumerate(keys):
            coeffs[n] = modal_vectors(read_snapshot(f_in, key, mean))

    if mode_batch <= 0 or mode_batch > nx:
        mode_batch = nx

    energy = np.empty((nx, ny), dtype=float)
    for i0 in range(0, nx, mode_batch):
        i1 = min(nx, i0 + mode_batch)
        accum = np.zeros((i1 - i0, ny, modal_dim, modal_dim), dtype=np.complex128)
        for n, key in enumerate(keys):
            if coeffs is None:
                batch = modal_vectors(read_snapshot(f_in, key, mean))[i0:i1]
            else:
                batch = coeffs[n, i0:i1]
            accum += batch[..., :, None] * batch[..., None, :].conj()
        accum /= len(keys)
        hermitian = 0.5 * (accum + np.swapaxes(accum.conj(), -1, -2))
        b0[i0:i1] = hermitian
        energy[i0:i1] = np.real(np.trace(hermitian, axis1=-2, axis2=-1))
    modal_group["mode_energy"][:] = energy

    if max_lag >= 0:
        if max_lag >= len(keys):
            raise ValueError("--max-lag must be smaller than the selected snapshot count")
        if coeffs is None:
            raise RuntimeError("internal error: lag covariance requires modal coefficients")
        lag_group = f_out.require_group("lag_covariance")
        lag_group.attrs["estimator"] = "unbiased positive-lag estimator"
        for lag in range(max_lag + 1):
            n_pairs = len(keys) - lag
            ds = lag_group.create_dataset(
                f"lag_{lag}",
                shape=(nx, ny, modal_dim, modal_dim),
                dtype=np.complex128,
                chunks=(1, 1, modal_dim, modal_dim),
            )
            for i0 in range(0, nx, mode_batch):
                i1 = min(nx, i0 + mode_batch)
                accum = np.zeros((i1 - i0, ny, modal_dim, modal_dim), dtype=np.complex128)
                for n in range(n_pairs):
                    a = coeffs[n + lag, i0:i1]
                    b = coeffs[n, i0:i1]
                    accum += a[..., :, None] * b[..., None, :].conj()
                ds[i0:i1] = accum / n_pairs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--velocity-h5", required=True, help="Input MKM *_U.h5 file.")
    parser.add_argument("--output", required=True, help="Output target HDF5 file.")
    parser.add_argument("--dt", type=float, required=True, help="DNS time step.")
    parser.add_argument("--t-min", type=float, help="Minimum physical sample time to include.")
    parser.add_argument("--t-max", type=float, help="Maximum physical sample time to include.")
    parser.add_argument("--skip-snapshots", type=int, default=0)
    parser.add_argument("--snapshot-stride", type=int, default=1)
    parser.add_argument("--max-snapshots", type=int)
    parser.add_argument("--sampling-stage-label", default="stationary",
                        help="Metadata label for the selected samples.")
    parser.add_argument("--mode-batch", type=int, default=4,
                        help="Number of streamwise modes to process per covariance batch.")
    parser.add_argument("--store-modal-coefficients", action="store_true")
    parser.add_argument("--max-lag", type=int, default=-1,
                        help="Maximum positive lag to store. -1 disables lag covariance.")
    parser.add_argument("--constraint-file", help="Optional constraint recipe HDF5 to copy into metadata.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    velocity_h5 = Path(args.velocity_h5).expanduser().resolve()
    output = Path(args.output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        output.unlink()

    with h5py.File(velocity_h5, "r") as f_in:
        keys = select_keys(
            sorted_snapshot_keys(f_in),
            skip=args.skip_snapshots,
            stride=args.snapshot_stride,
            max_snapshots=args.max_snapshots,
            dt=args.dt,
            t_min=args.t_min,
            t_max=args.t_max,
        )
        x_wall = f_in["u0/mesh/x0"][:]
        x_stream = f_in["u0/mesh/x1"][:]
        x_span = f_in["u0/mesh/x2"][:]
        nx = len(x_stream)
        ny = len(x_span)
        L_stream = x_stream[-1] + (x_stream[1] - x_stream[0]) - x_stream[0]
        L_span = x_span[-1] + (x_span[1] - x_span[0]) - x_span[0]
        k_stream = 2.0 * np.pi * np.fft.fftfreq(nx, d=L_stream / nx)
        k_span = 2.0 * np.pi * np.fft.fftfreq(ny, d=L_span / ny)
        times = np.array([int(key) * args.dt for key in keys], dtype=float)

        mean, reynolds = accumulate_mean_and_reynolds(f_in, keys)

        with h5py.File(output, "w") as f_out:
            f_out.attrs["source_velocity_h5"] = str(velocity_h5)
            f_out.attrs["component_order_level_major"] = "[u_streamwise_from_HDF5_u1, u_spanwise_from_HDF5_u2, u_wallnormal_from_HDF5_u0]"
            f_out.attrs["component_names"] = ",".join(COMPONENT_NAMES)
            f_out.attrs["forward_fft_normalization"] = "np.fft.fft2(u_fluct, axes=(streamwise, spanwise))/(Nx*Ny)"
            f_out.attrs["snapshot_keys"] = ",".join(keys)
            f_out.attrs["dt"] = args.dt
            f_out.attrs["sampling_stage_label"] = args.sampling_stage_label
            f_out.attrs["selection_t_min"] = np.nan if args.t_min is None else args.t_min
            f_out.attrs["selection_t_max"] = np.nan if args.t_max is None else args.t_max
            f_out.attrs["selection_skip_snapshots"] = args.skip_snapshots
            f_out.attrs["selection_snapshot_stride"] = args.snapshot_stride
            f_out.attrs["selection_max_snapshots"] = -1 if args.max_snapshots is None else args.max_snapshots
            f_out.create_dataset("geometry/z_wall", data=x_wall)
            f_out.create_dataset("geometry/x_stream", data=x_stream)
            f_out.create_dataset("geometry/x_span", data=x_span)
            f_out.create_dataset("geometry/k_stream", data=k_stream)
            f_out.create_dataset("geometry/k_span", data=k_span)
            f_out.create_dataset("sampling/t", data=times)
            f_out.create_dataset("mean_profile", data=mean.T)
            f_out["mean_profile"].attrs["columns"] = ",".join(COMPONENT_NAMES)
            f_out.create_dataset("reynolds_stress_profile", data=reynolds)
            f_out["reynolds_stress_profile"].attrs["component_order"] = ",".join(COMPONENT_NAMES)
            if args.constraint_file:
                constraint_path = Path(args.constraint_file).expanduser().resolve()
                f_out.attrs["constraint_file"] = str(constraint_path)
                if constraint_path.exists():
                    copied = output.with_suffix(".constraints.h5")
                    shutil.copy2(constraint_path, copied)
                    f_out.attrs["constraint_file_copy"] = str(copied)
            write_modal_covariance(
                f_in,
                f_out,
                keys,
                mean,
                mode_batch=args.mode_batch,
                store_modal_coefficients=args.store_modal_coefficients,
                max_lag=args.max_lag,
            )

    print(f"wrote={output}")
    print(f"snapshots={len(keys)}")
    print(f"sample_time_range={int(keys[0]) * args.dt:.12g},{int(keys[-1]) * args.dt:.12g}")
    print(f"size_bytes={output.stat().st_size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
