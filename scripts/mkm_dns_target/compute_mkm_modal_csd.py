#!/usr/bin/env python
"""Compute mode-resolved temporal CSD matrices for selected MKM modes."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import h5py
import numpy as np

from mkm_channel_resolvent_utils import chebyshev_gauss_physical_weights


COMPONENT_GROUPS = ("u1", "u2", "u0")
COMPONENT_NAMES = ("streamwise", "spanwise", "wallnormal")
NORMALIZATION = (
    "For each segment, Q_k = FFT_t(window*q)_k and "
    "Sqq(omega_k) = sample_dt/(window_energy*n_segments) * "
    "sum_segments Q_k Q_k^*. Frequencies are two-sided angular frequencies "
    "2*pi*fftfreq(segment_length, sample_dt), stored sorted ascending."
)
PARSEVAL_CONVENTION = (
    "(1/(2*pi))*sum_omega trace(Wq*Sqq(omega))*Delta_omega equals the "
    "window-weighted segment-average modal energy. For window=none and a "
    "single full-record segment this is the selected-record time mean energy."
)


@dataclass(frozen=True)
class ModalSourceData:
    series: np.ndarray
    selected_times: np.ndarray
    selected_keys: list[str]
    z_wall: np.ndarray
    k_stream: np.ndarray
    k_span: np.ndarray
    source: str
    source_target_h5: Path
    source_velocity_h5: Path | None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, help="Output CSD HDF5 file.")
    parser.add_argument(
        "--mode-index-list",
        nargs="+",
        type=int,
        required=True,
        metavar=("I", "J"),
        help="Selected mode-index pairs: I J [I J ...].",
    )
    parser.add_argument("--target-h5", required=True, help="Target HDF5 with modal/u_hat or mean metadata.")
    parser.add_argument("--velocity-h5", help="Optional raw MKM *_U.h5 file; computes selected modes on the fly.")
    parser.add_argument("--dt", type=float, help="Time step for raw velocity snapshot keys when needed.")
    parser.add_argument("--t-min", type=float)
    parser.add_argument("--t-max", type=float)
    parser.add_argument("--skip-snapshots", type=int, default=0)
    parser.add_argument("--snapshot-stride", type=int, default=1)
    parser.add_argument("--max-snapshots", type=int)
    parser.add_argument("--segment-length", type=int, help="Temporal segment length. Default: full selected record.")
    parser.add_argument("--overlap", type=float, default=0.5)
    parser.add_argument("--window", choices=("none", "hann"), default="hann")
    parser.add_argument(
        "--demean-temporal",
        action="store_true",
        help="Subtract each selected modal coefficient's selected-record temporal mean before segmentation.",
    )
    parser.add_argument("--overwrite", action="store_true", help="Replace an existing output file.")
    return parser.parse_args()


def parse_mode_index_list(values: list[int]) -> np.ndarray:
    if len(values) % 2:
        raise ValueError("--mode-index-list must contain an even number of integers")
    modes = np.asarray(values, dtype=np.int32).reshape(-1, 2)
    if modes.shape[0] == 0:
        raise ValueError("at least one mode index is required")
    return modes


def finite_or_none(value: object) -> float | None:
    if value is None:
        return None
    try:
        value = float(value)
    except (TypeError, ValueError):
        return None
    if not np.isfinite(value):
        return None
    return value


def uniform_sample_spacing(times: np.ndarray) -> float:
    if times.size < 2:
        raise ValueError("at least two selected snapshots are required")
    spacing = np.diff(times)
    sample_dt = float(np.median(spacing))
    if not np.allclose(spacing, sample_dt, rtol=1e-9, atol=1e-11):
        raise ValueError("selected snapshots are not uniformly spaced in time")
    return sample_dt


def select_time_indices(
    times: np.ndarray,
    skip: int,
    stride: int,
    max_snapshots: int | None,
    t_min: float | None,
    t_max: float | None,
) -> np.ndarray:
    keep = np.ones(times.shape, dtype=bool)
    if t_min is not None:
        keep &= times >= t_min - 1e-12
    if t_max is not None:
        keep &= times <= t_max + 1e-12
    indices = np.nonzero(keep)[0]
    indices = indices[skip::stride]
    if max_snapshots is not None:
        indices = indices[:max_snapshots]
    if indices.size == 0:
        raise ValueError("no snapshots selected")
    return indices


def split_snapshot_keys(value: object, count: int) -> list[str]:
    if isinstance(value, bytes):
        value = value.decode("utf-8")
    if isinstance(value, str) and value:
        keys = [part.strip() for part in value.split(",") if part.strip()]
        if len(keys) == count:
            return keys
    return [str(index) for index in range(count)]


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
        time = int(key) * dt
        if t_min is not None and time < t_min - 1e-12:
            continue
        if t_max is not None and time > t_max + 1e-12:
            continue
        selected.append(key)
    selected = selected[skip::stride]
    if max_snapshots is not None:
        selected = selected[:max_snapshots]
    if not selected:
        raise ValueError("no snapshots selected")
    return selected


def temporal_window(kind: str, n: int) -> np.ndarray:
    if kind == "none":
        return np.ones(n, dtype=np.float64)
    if kind == "hann":
        return np.hanning(n).astype(np.float64)
    raise ValueError(f"unknown temporal window {kind!r}")


def segment_starts(record_length: int, segment_length: int | None, overlap: float) -> tuple[int, np.ndarray]:
    if segment_length is None:
        segment_length = record_length
    if segment_length <= 1:
        raise ValueError("segment length must be at least 2")
    if segment_length > record_length:
        raise ValueError("segment length cannot exceed selected record length")
    if overlap < 0.0 or overlap >= 1.0:
        raise ValueError("--overlap must satisfy 0 <= overlap < 1")
    step = max(1, int(round(segment_length * (1.0 - overlap))))
    starts = np.arange(0, record_length - segment_length + 1, step, dtype=np.int32)
    if starts.size == 0:
        starts = np.array([0], dtype=np.int32)
    return segment_length, starts


def validate_modes(modes: np.ndarray, k_stream: np.ndarray, k_span: np.ndarray) -> None:
    for i, j in modes:
        if i < 0 or i >= k_stream.size:
            raise IndexError(f"streamwise mode index {int(i)} is outside [0, {k_stream.size})")
        if j < 0 or j >= k_span.size:
            raise IndexError(f"spanwise mode index {int(j)} is outside [0, {k_span.size})")


def read_target_modal_source(
    target_h5: Path,
    modes: np.ndarray,
    skip: int,
    stride: int,
    max_snapshots: int | None,
    t_min: float | None,
    t_max: float | None,
) -> ModalSourceData:
    with h5py.File(target_h5, "r") as f:
        if "modal/u_hat" not in f:
            raise KeyError("target file does not contain modal/u_hat; pass --velocity-h5 for raw snapshots")
        times = f["sampling/t"][:]
        indices = select_time_indices(times, skip, stride, max_snapshots, t_min, t_max)
        z_wall = f["geometry/z_wall"][:]
        k_stream = f["geometry/k_stream"][:]
        k_span = f["geometry/k_span"][:]
        validate_modes(modes, k_stream, k_span)
        u_hat = f["modal/u_hat"]
        modal_dim = u_hat.shape[-1]
        series = np.empty((indices.size, modes.shape[0], modal_dim), dtype=np.complex128)
        for mode_number, (i, j) in enumerate(modes):
            series[:, mode_number, :] = u_hat[indices, int(i), int(j), :]
        all_keys = split_snapshot_keys(f.attrs.get("snapshot_keys", ""), len(times))
        selected_keys = [all_keys[int(index)] for index in indices]
    return ModalSourceData(
        series=series,
        selected_times=times[indices],
        selected_keys=selected_keys,
        z_wall=z_wall,
        k_stream=k_stream,
        k_span=k_span,
        source="target_modal_u_hat",
        source_target_h5=target_h5,
        source_velocity_h5=None,
    )


def read_raw_snapshot_selected_modes(
    f: h5py.File,
    key: str,
    mean_profile_component_major: np.ndarray,
    modes: np.ndarray,
) -> np.ndarray:
    fields = [f[f"{group}/3D/{key}"][:] for group in COMPONENT_GROUPS]
    data = np.stack(fields, axis=0)
    data = data - mean_profile_component_major[:, :, None, None]
    _, nz, nx, ny = data.shape
    uhat = np.fft.fft2(data, axes=(2, 3)) / (nx * ny)
    vectors = np.empty((modes.shape[0], 3 * nz), dtype=np.complex128)
    for mode_number, (i, j) in enumerate(modes):
        vectors[mode_number] = np.transpose(uhat[:, :, int(i), int(j)], (1, 0)).reshape(3 * nz)
    return vectors


def infer_raw_dt(target_attrs: h5py.AttributeManager, dt: float | None) -> float:
    if dt is not None:
        return float(dt)
    attr_dt = finite_or_none(target_attrs.get("dt"))
    if attr_dt is None:
        raise ValueError("--dt is required for --velocity-h5 when target attrs do not provide dt")
    return attr_dt


def read_raw_modal_source(
    velocity_h5: Path,
    target_h5: Path,
    modes: np.ndarray,
    dt: float | None,
    skip: int,
    stride: int,
    max_snapshots: int | None,
    t_min: float | None,
    t_max: float | None,
) -> ModalSourceData:
    with h5py.File(target_h5, "r") as f_target, h5py.File(velocity_h5, "r") as f_velocity:
        raw_dt = infer_raw_dt(f_target.attrs, dt)
        keys = select_keys(
            sorted_snapshot_keys(f_velocity),
            skip=skip,
            stride=stride,
            max_snapshots=max_snapshots,
            dt=raw_dt,
            t_min=t_min,
            t_max=t_max,
        )
        selected_times = np.array([int(key) * raw_dt for key in keys], dtype=np.float64)
        z_wall = f_target["geometry/z_wall"][:]
        velocity_z = f_velocity["u0/mesh/x0"][:]
        if z_wall.shape != velocity_z.shape or not np.allclose(z_wall, velocity_z):
            raise ValueError("target geometry/z_wall does not match velocity u0/mesh/x0")
        k_stream = f_target["geometry/k_stream"][:]
        k_span = f_target["geometry/k_span"][:]
        validate_modes(modes, k_stream, k_span)
        mean_profile = f_target["mean_profile"][:]
        mean_profile_component_major = mean_profile.T
        nz = z_wall.size
        series = np.empty((len(keys), modes.shape[0], 3 * nz), dtype=np.complex128)
        for index, key in enumerate(keys):
            series[index] = read_raw_snapshot_selected_modes(
                f_velocity,
                key,
                mean_profile_component_major,
                modes,
            )
    return ModalSourceData(
        series=series,
        selected_times=selected_times,
        selected_keys=keys,
        z_wall=z_wall,
        k_stream=k_stream,
        k_span=k_span,
        source="raw_velocity_fft2_selected_modes",
        source_target_h5=target_h5,
        source_velocity_h5=velocity_h5,
    )


def preprocess_series(series: np.ndarray, demean_temporal: bool) -> np.ndarray:
    if not demean_temporal:
        return np.asarray(series, dtype=np.complex128)
    return series - np.mean(series, axis=0, keepdims=True)


def modal_energy_per_sample(q: np.ndarray, weights_q: np.ndarray) -> np.ndarray:
    return np.einsum("...i,i,...i->...", q.conj(), weights_q, q, optimize=True).real


def compute_component_and_energy_traces(
    Sqq: np.ndarray,
    weights_z: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    n_modes, n_omega, modal_dim, _ = Sqq.shape
    nz = weights_z.size
    if modal_dim != 3 * nz:
        raise ValueError("Sqq modal dimension does not match z weights")
    component_trace = np.empty((n_modes, n_omega, 3), dtype=np.float64)
    diag = np.diagonal(Sqq, axis1=-2, axis2=-1).real
    for component in range(3):
        component_diag = diag[..., component::3]
        component_trace[..., component] = np.sum(component_diag * weights_z[None, None, :], axis=-1)
    energy_trace = np.sum(component_trace, axis=-1)
    return component_trace, energy_trace


def estimate_csd(
    series: np.ndarray,
    sample_dt: float,
    segment_length: int,
    starts: np.ndarray,
    window: np.ndarray,
    weights_q: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    nt, n_modes, modal_dim = series.shape
    n_omega = segment_length
    n_segments = starts.size
    window_energy = float(np.sum(window * window))
    if window_energy <= 0.0:
        raise ValueError("temporal window has zero energy")
    scale = sample_dt / (window_energy * n_segments)
    Sqq = np.zeros((n_modes, n_omega, modal_dim, modal_dim), dtype=np.complex128)
    parseval_time = np.zeros(n_modes, dtype=np.float64)

    for start in starts:
        segment = series[start : start + segment_length]
        windowed = segment * window[:, None, None]
        weighted_energy = modal_energy_per_sample(segment, weights_q)
        parseval_time += np.sum((window * window)[:, None] * weighted_energy, axis=0) / window_energy
        fft_values = np.fft.fft(windowed, axis=0)
        for mode_number in range(n_modes):
            Sqq[mode_number] += scale * np.einsum(
                "ki,kj->kij",
                fft_values[:, mode_number, :],
                fft_values[:, mode_number, :].conj(),
                optimize=True,
            )

    parseval_time /= n_segments
    omega = 2.0 * np.pi * np.fft.fftfreq(segment_length, d=sample_dt)
    order = np.argsort(omega)
    omega = omega[order]
    Sqq = Sqq[:, order]
    Sqq = 0.5 * (Sqq + np.swapaxes(Sqq.conj(), -1, -2))
    trace = np.trace(Sqq, axis1=-2, axis2=-1).real
    return omega, Sqq, trace, parseval_time, order


def write_output(
    output: Path,
    source_data: ModalSourceData,
    modes: np.ndarray,
    omega: np.ndarray,
    Sqq: np.ndarray,
    trace: np.ndarray,
    component_trace: np.ndarray,
    energy_trace: np.ndarray,
    selected_series: np.ndarray,
    weights_z: np.ndarray,
    sample_dt: float,
    segment_length: int,
    starts: np.ndarray,
    overlap: float,
    window_kind: str,
    window_energy: float,
    demean_temporal: bool,
    parseval_time: np.ndarray,
    parseval_spectrum: np.ndarray,
    parseval_relative_error: np.ndarray,
) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        output.unlink()

    key_dtype = h5py.string_dtype(encoding="utf-8")
    with h5py.File(output, "w") as f:
        f.attrs["description"] = "Mode-resolved temporal CSD for selected MKM horizontal modes."
        f.attrs["source"] = source_data.source
        f.attrs["source_target_h5"] = str(source_data.source_target_h5)
        if source_data.source_velocity_h5 is not None:
            f.attrs["source_velocity_h5"] = str(source_data.source_velocity_h5)
        f.attrs["component_order_level_major"] = "[streamwise, spanwise, wallnormal]"
        f.attrs["component_names"] = ",".join(COMPONENT_NAMES)
        f.attrs["estimator"] = "selected-mode two-sided temporal CSD periodogram"
        f.attrs["normalization"] = NORMALIZATION
        f.attrs["parseval_convention"] = PARSEVAL_CONVENTION
        f.attrs["temporal_demean_behavior"] = (
            "selected-record coefficient mean removed before segmentation"
            if demean_temporal
            else "no temporal demeaning"
        )

        f.create_dataset("geometry/z_wall", data=source_data.z_wall)
        f.create_dataset("mode/index", data=modes.astype(np.int32))
        f.create_dataset("mode/k_stream", data=source_data.k_stream[modes[:, 0]])
        f.create_dataset("mode/k_span", data=source_data.k_span[modes[:, 1]])
        f.create_dataset("frequencies/omega", data=omega)

        ds = f.create_dataset("csd/Sqq", data=Sqq)
        ds.attrs["axes"] = "mode,omega,level_major_velocity,level_major_velocity"
        ds = f.create_dataset("csd/trace", data=trace)
        ds.attrs["axes"] = "mode,omega"
        ds.attrs["definition"] = "ordinary real trace of Sqq"
        ds = f.create_dataset("csd/component_trace", data=component_trace)
        ds.attrs["axes"] = "mode,omega,component"
        ds.attrs["definition"] = "wall-normal-weighted component energy spectrum"
        ds.attrs["component_order"] = ",".join(COMPONENT_NAMES)
        ds = f.create_dataset("csd/energy_trace", data=energy_trace)
        ds.attrs["axes"] = "mode,omega"
        ds.attrs["definition"] = "trace(Wq*Sqq), using physical Chebyshev-Gauss weights"

        f.create_dataset("metadata/selected_times", data=source_data.selected_times)
        f.create_dataset(
            "metadata/selected_keys",
            data=np.array(source_data.selected_keys, dtype=object),
            dtype=key_dtype,
        )
        f.create_dataset("metadata/window", data=window_kind, dtype=key_dtype)
        f.create_dataset("metadata/window_energy", data=window_energy)
        f.create_dataset("metadata/sample_dt", data=sample_dt)
        f.create_dataset("metadata/segment_length", data=segment_length)
        f.create_dataset("metadata/overlap", data=overlap)
        f.create_dataset("metadata/segment_start_indices", data=starts)
        f.create_dataset("metadata/source", data=source_data.source, dtype=key_dtype)
        f.create_dataset("metadata/demean_temporal", data=bool(demean_temporal))

        f.create_dataset("diagnostics/parseval_energy_time", data=parseval_time)
        f.create_dataset("diagnostics/parseval_energy_spectrum", data=parseval_spectrum)
        f.create_dataset("diagnostics/parseval_relative_error", data=parseval_relative_error)
        f.create_dataset("diagnostics/weights_z", data=weights_z)
        f.create_dataset("diagnostics/modal_series_energy_mean", data=np.mean(modal_energy_per_sample(selected_series, np.repeat(weights_z, 3)), axis=0))


def compute_modal_csd(
    output: str | Path,
    target_h5: str | Path,
    mode_index_list: Iterable[int] | np.ndarray,
    *,
    velocity_h5: str | Path | None = None,
    dt: float | None = None,
    t_min: float | None = None,
    t_max: float | None = None,
    skip_snapshots: int = 0,
    snapshot_stride: int = 1,
    max_snapshots: int | None = None,
    segment_length: int | None = None,
    overlap: float = 0.5,
    window: str = "hann",
    demean_temporal: bool = False,
    overwrite: bool = False,
) -> dict[str, object]:
    output_path = Path(output).expanduser().resolve()
    if output_path.exists() and not overwrite:
        raise FileExistsError(f"{output_path} exists; pass --overwrite to replace it")

    mode_array = np.asarray(mode_index_list, dtype=np.int32)
    if mode_array.ndim == 2:
        if mode_array.shape[1] != 2 or mode_array.shape[0] == 0:
            raise ValueError("mode_index_list array must have shape (n_modes, 2)")
        modes = mode_array
    else:
        modes = parse_mode_index_list(mode_array.ravel().tolist())
    target_path = Path(target_h5).expanduser().resolve()
    if velocity_h5 is None:
        source_data = read_target_modal_source(
            target_path,
            modes,
            skip_snapshots,
            snapshot_stride,
            max_snapshots,
            t_min,
            t_max,
        )
    else:
        source_data = read_raw_modal_source(
            Path(velocity_h5).expanduser().resolve(),
            target_path,
            modes,
            dt,
            skip_snapshots,
            snapshot_stride,
            max_snapshots,
            t_min,
            t_max,
        )

    selected_series = preprocess_series(source_data.series, demean_temporal)
    sample_dt = uniform_sample_spacing(source_data.selected_times)
    seg_length, starts = segment_starts(selected_series.shape[0], segment_length, overlap)
    window_values = temporal_window(window, seg_length)
    window_energy = float(np.sum(window_values * window_values))
    weights_z = chebyshev_gauss_physical_weights(source_data.z_wall)
    weights_q = np.repeat(weights_z, 3)
    omega, Sqq, trace, parseval_time, _ = estimate_csd(
        selected_series,
        sample_dt,
        seg_length,
        starts,
        window_values,
        weights_q,
    )
    component_trace, energy_trace = compute_component_and_energy_traces(Sqq, weights_z)
    if omega.size > 1:
        delta_omega = float(np.median(np.diff(omega)))
    else:
        delta_omega = 0.0
    parseval_spectrum = np.sum(energy_trace, axis=1) * delta_omega / (2.0 * np.pi)
    parseval_relative_error = np.abs(parseval_spectrum - parseval_time) / np.maximum(np.abs(parseval_time), 1e-300)

    write_output(
        output_path,
        source_data,
        modes,
        omega,
        Sqq,
        trace,
        component_trace,
        energy_trace,
        selected_series,
        weights_z,
        sample_dt,
        seg_length,
        starts,
        overlap,
        window,
        window_energy,
        demean_temporal,
        parseval_time,
        parseval_spectrum,
        parseval_relative_error,
    )
    return {
        "output": str(output_path),
        "source": source_data.source,
        "n_modes": int(modes.shape[0]),
        "n_times": int(selected_series.shape[0]),
        "modal_dim": int(selected_series.shape[-1]),
        "n_omega": int(omega.size),
        "sample_dt": sample_dt,
        "segment_length": int(seg_length),
        "n_segments": int(starts.size),
        "window": window,
        "max_parseval_relative_error": float(np.max(parseval_relative_error)),
    }


def main() -> int:
    args = parse_args()
    result = compute_modal_csd(
        output=args.output,
        target_h5=args.target_h5,
        velocity_h5=args.velocity_h5,
        mode_index_list=args.mode_index_list,
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
        overwrite=args.overwrite,
    )
    print(f"wrote={result['output']}")
    print(f"source={result['source']}")
    print(f"n_modes={result['n_modes']}")
    print(f"n_times={result['n_times']}")
    print(f"modal_dim={result['modal_dim']}")
    print(f"n_omega={result['n_omega']}")
    print(f"sample_dt={result['sample_dt']:.12g}")
    print(f"segment_length={result['segment_length']}")
    print(f"n_segments={result['n_segments']}")
    print(f"window={result['window']}")
    print(f"max_parseval_relative_error={result['max_parseval_relative_error']:.6e}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
