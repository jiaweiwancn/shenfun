#!/usr/bin/env python
"""Synthetic smoke test for DNS CSD projection onto resolvent response modes."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import h5py
import numpy as np

from compute_mkm_channel_resolvent import compute_single_mode_resolvent
from mkm_channel_resolvent_utils import chebyshev_gauss_physical_weights, velocity_energy_weight
from smoke_channel_resolvent_single_mode import write_tiny_fixtures


SMOKE_DIR = Path("/private/tmp/mkm_resolvent_projection_smoke")


def dataset_schema(path: Path) -> list[str]:
    lines: list[str] = []
    with h5py.File(path, "r") as f:
        def visitor(name: str, obj: h5py.Dataset | h5py.Group) -> None:
            if isinstance(obj, h5py.Dataset):
                lines.append(f"{name}: shape={obj.shape} dtype={obj.dtype}")

        f.visititems(visitor)
    return sorted(lines)


def write_aligned_csd(resolvent_h5: Path, output_h5: Path) -> None:
    with h5py.File(resolvent_h5, "r") as f_res:
        z = f_res["geometry/z_wall"][:]
        omega = f_res["frequencies/omega"][:]
        mode_index = f_res["mode/index"][:]
        kappa = float(f_res["mode/kappa"][()])
        lambda_ = float(f_res["mode/lambda"][()])
        response_modes = f_res["resolvent/response_modes"][:]

    weights_z = chebyshev_gauss_physical_weights(z)
    weights_q = velocity_energy_weight(weights_z, as_matrix=False)
    n_omega, _, modal_dim = response_modes.shape
    Sqq = np.empty((1, n_omega, modal_dim, modal_dim), dtype=np.complex128)
    strengths = np.linspace(2.0, 4.0, n_omega)
    for omega_index, strength in enumerate(strengths):
        psi = response_modes[omega_index, 0].astype(np.complex128)
        norm = float(np.einsum("i,i,i->", psi.conj(), weights_q, psi, optimize=True).real)
        psi = psi / np.sqrt(norm)
        Sqq[0, omega_index] = strength * np.outer(psi, psi.conj())

    trace = np.trace(Sqq, axis1=-2, axis2=-1).real
    diag = np.diagonal(Sqq, axis1=-2, axis2=-1).real
    component_trace = np.empty((1, n_omega, 3), dtype=float)
    for component in range(3):
        component_trace[0, :, component] = np.sum(
            diag[0, :, component::3] * weights_z[None, :],
            axis=1,
        )
    energy_trace = np.sum(component_trace, axis=-1)

    with h5py.File(output_h5, "w") as f:
        f.attrs["description"] = "Synthetic rank-1 CSD aligned with the leading response mode."
        f.attrs["component_order_level_major"] = "[streamwise, spanwise, wallnormal]"
        f.attrs["component_names"] = "streamwise,spanwise,wallnormal"
        f.create_dataset("geometry/z_wall", data=z)
        f.create_dataset("mode/index", data=mode_index[None, :].astype(np.int32))
        f.create_dataset("mode/k_stream", data=np.array([kappa], dtype=float))
        f.create_dataset("mode/k_span", data=np.array([lambda_], dtype=float))
        f.create_dataset("frequencies/omega", data=omega)
        f.create_dataset("csd/Sqq", data=Sqq)
        f.create_dataset("csd/trace", data=trace)
        f.create_dataset("csd/component_trace", data=component_trace)
        f.create_dataset("csd/energy_trace", data=energy_trace)


def main() -> int:
    SMOKE_DIR.mkdir(parents=True, exist_ok=True)
    target_h5, constraint_h5 = write_tiny_fixtures(SMOKE_DIR)
    resolvent_h5 = SMOKE_DIR / "synthetic_resolvent.h5"
    csd_h5 = SMOKE_DIR / "synthetic_aligned_csd.h5"
    projection_h5 = SMOKE_DIR / "synthetic_projection.h5"
    omega = np.array([0.45, 0.75, 1.05])

    compute_single_mode_resolvent(
        target_h5,
        constraint_h5,
        resolvent_h5,
        (1, 1),
        omega,
        4,
        overwrite=True,
    )
    write_aligned_csd(resolvent_h5, csd_h5)

    script = Path(__file__).with_name("project_mkm_dns_onto_resolvent.py")
    command = [
        sys.executable,
        str(script),
        "--resolvent-h5",
        str(resolvent_h5),
        "--csd-h5",
        str(csd_h5),
        "--output",
        str(projection_h5),
        "--max-rank",
        "4",
        "--overwrite",
    ]
    completed = subprocess.run(command, check=True, text=True, capture_output=True)

    with h5py.File(projection_h5, "r") as f:
        energy_total = f["projection/energy_total"][:]
        energy_fraction = f["projection/energy_fraction"][:]
        cumulative = f["projection/cumulative_energy_fraction"][:]
        response_norm_error = float(f["diagnostics/max_response_energy_norm_error"][()])
        frequency_match_error = f["diagnostics/frequency_match_error"][:]
        mode_match_error = float(f["diagnostics/mode_match_error"][()])
        weighted_fro = f["projection/weighted_frobenius_relative_error"][:]

    if not np.all(energy_total > 0.0):
        raise AssertionError(f"projection energy_total is not positive: {energy_total}")
    if not np.allclose(energy_fraction[:, 0], 1.0, atol=1e-10):
        raise AssertionError(f"leading fractions are not near one: {energy_fraction[:, 0]}")
    if np.max(np.abs(energy_fraction[:, 1:])) > 1e-10:
        raise AssertionError(f"higher-mode fractions should be near zero: {energy_fraction[:, 1:]}")
    if np.min(np.diff(cumulative, axis=1)) < -1e-12:
        raise AssertionError(f"cumulative fractions are not nondecreasing: {cumulative}")
    if not np.allclose(cumulative[:, -1], 1.0, atol=1e-10):
        raise AssertionError(f"final cumulative fractions are not near one: {cumulative[:, -1]}")
    if response_norm_error > 1e-10:
        raise AssertionError(f"response norm error too large: {response_norm_error:.6e}")
    if np.max(frequency_match_error) > 1e-12:
        raise AssertionError(f"frequency match error too large: {frequency_match_error}")
    if mode_match_error > 1e-12:
        raise AssertionError(f"mode match error too large: {mode_match_error:.6e}")
    if np.max(weighted_fro[:, 0]) > 1e-10:
        raise AssertionError(f"rank-1 weighted Frobenius error too large: {weighted_fro[:, 0]}")

    print("smoke_project_dns_onto_resolvent: ok")
    print("cli_stdout:")
    print(completed.stdout.strip())
    print(f"resolvent_h5={resolvent_h5}")
    print(f"csd_h5={csd_h5}")
    print(f"projection_h5={projection_h5}")
    print(f"energy_total={energy_total}")
    print(f"leading_energy_fraction={energy_fraction[:, 0]}")
    print(f"final_cumulative_energy_fraction={cumulative[:, -1]}")
    print(f"rank1_weighted_frobenius_error={weighted_fro[:, 0]}")
    print(f"max_response_energy_norm_error={response_norm_error:.6e}")
    print("hdf5_schema:")
    for line in dataset_schema(projection_h5):
        print(f"  {line}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
