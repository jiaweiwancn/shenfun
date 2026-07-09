#!/usr/bin/env python
"""Synthetic smoke test for selected-mode MKM modal CSD."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import h5py
import numpy as np

from build_mkm_constraints import chebyshev_gauss_nodes


SMOKE_DIR = Path("/private/tmp/mkm_modal_csd_smoke")


def write_synthetic_target(path: Path) -> tuple[float, int, int]:
    nt = 32
    nz = 6
    nx = 4
    ny = 4
    modal_dim = 3 * nz
    sample_dt = 0.25
    mode_a = (1, 1)
    mode_b = (2, 1)
    bin_a = 3
    bin_b = 5

    z = chebyshev_gauss_nodes(nz, -1.0, 1.0)
    k_stream = 2.0 * np.pi * np.fft.fftfreq(nx, d=(2.0 * np.pi) / nx)
    k_span = 2.0 * np.pi * np.fft.fftfreq(ny, d=np.pi / ny)
    times = np.arange(nt, dtype=float) * sample_dt
    q_a = np.zeros(modal_dim, dtype=np.complex128)
    q_b = np.zeros(modal_dim, dtype=np.complex128)
    q_a[0::3] = 1.0 + 0.2j
    q_a[1::3] = 0.35 - 0.1j
    q_a[2::3] = 0.15j
    q_b[0::3] = 0.2
    q_b[1::3] = 0.1 + 0.3j
    q_b[2::3] = -0.2j

    u_hat = np.zeros((nt, nx, ny, modal_dim), dtype=np.complex128)
    phase_a = np.exp(1j * 2.0 * np.pi * bin_a * np.arange(nt) / nt)
    phase_b = np.exp(1j * 2.0 * np.pi * bin_b * np.arange(nt) / nt)
    u_hat[:, mode_a[0], mode_a[1], :] = phase_a[:, None] * q_a[None, :]
    u_hat[:, mode_b[0], mode_b[1], :] = phase_b[:, None] * q_b[None, :]

    with h5py.File(path, "w") as f:
        f.attrs["component_order_level_major"] = "[streamwise, spanwise, wallnormal]"
        f.attrs["component_names"] = "streamwise,spanwise,wallnormal"
        f.attrs["snapshot_keys"] = ",".join(str(index) for index in range(nt))
        f.attrs["dt"] = sample_dt
        f.create_dataset("geometry/z_wall", data=z)
        f.create_dataset("geometry/k_stream", data=k_stream)
        f.create_dataset("geometry/k_span", data=k_span)
        f.create_dataset("sampling/t", data=times)
        mean = np.zeros((nz, 3), dtype=float)
        ds = f.create_dataset("mean_profile", data=mean)
        ds.attrs["columns"] = "streamwise,spanwise,wallnormal"
        f.create_dataset("modal/u_hat", data=u_hat)

    return sample_dt, bin_a, nt


def dataset_schema(path: Path) -> list[str]:
    lines: list[str] = []
    with h5py.File(path, "r") as f:
        def visitor(name: str, obj: h5py.Dataset | h5py.Group) -> None:
            if isinstance(obj, h5py.Dataset):
                lines.append(f"{name}: shape={obj.shape} dtype={obj.dtype}")

        f.visititems(visitor)
    return sorted(lines)


def main() -> int:
    SMOKE_DIR.mkdir(parents=True, exist_ok=True)
    target_h5 = SMOKE_DIR / "synthetic_modal_target.h5"
    output_h5 = SMOKE_DIR / "synthetic_modal_csd.h5"
    sample_dt, bin_a, nt = write_synthetic_target(target_h5)

    script = Path(__file__).with_name("compute_mkm_modal_csd.py")
    command = [
        sys.executable,
        str(script),
        "--target-h5",
        str(target_h5),
        "--output",
        str(output_h5),
        "--mode-index-list",
        "1",
        "1",
        "2",
        "1",
        "--segment-length",
        str(nt),
        "--overlap",
        "0.0",
        "--window",
        "none",
        "--overwrite",
    ]
    completed = subprocess.run(command, check=True, text=True, capture_output=True)

    with h5py.File(output_h5, "r") as f:
        Sqq = f["csd/Sqq"][:]
        omega = f["frequencies/omega"][:]
        energy_trace = f["csd/energy_trace"][:]
        parseval_error = f["diagnostics/parseval_relative_error"][:]
        mode_index = f["mode/index"][:]

    if Sqq.shape != (2, nt, 18, 18):
        raise AssertionError(f"unexpected Sqq shape {Sqq.shape}")
    expected_omega = np.sort(2.0 * np.pi * np.fft.fftfreq(nt, d=sample_dt))
    if not np.allclose(omega, expected_omega):
        raise AssertionError("frequency grid does not match sorted 2*pi*fftfreq")

    peak_index = int(np.argmax(energy_trace[0]))
    expected_peak = 2.0 * np.pi * bin_a / (nt * sample_dt)
    if abs(omega[peak_index] - expected_peak) > 1e-12:
        raise AssertionError(f"peak omega {omega[peak_index]} does not match {expected_peak}")

    hermitian_error = float(np.max(np.abs(Sqq - np.swapaxes(Sqq.conj(), -1, -2))))
    if hermitian_error > 1e-12:
        raise AssertionError(f"Sqq Hermitian error too large: {hermitian_error:.6e}")
    max_parseval_error = float(np.max(parseval_error))
    if max_parseval_error > 1e-12:
        raise AssertionError(f"Parseval relative error too large: {max_parseval_error:.6e}")
    if not np.array_equal(mode_index, np.array([[1, 1], [2, 1]], dtype=np.int32)):
        raise AssertionError(f"unexpected mode index table {mode_index}")

    print("smoke_modal_csd: ok")
    print("cli_stdout:")
    print(completed.stdout.strip())
    print(f"output_h5={output_h5}")
    print(f"Sqq_shape={Sqq.shape}")
    print(f"known_peak_omega={expected_peak:.12g}")
    print(f"detected_peak_omega={omega[peak_index]:.12g}")
    print(f"hermitian_error={hermitian_error:.6e}")
    print(f"max_parseval_relative_error={max_parseval_error:.6e}")
    print("hdf5_schema:")
    for line in dataset_schema(output_h5):
        print(f"  {line}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
