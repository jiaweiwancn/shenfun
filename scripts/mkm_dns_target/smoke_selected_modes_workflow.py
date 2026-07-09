#!/usr/bin/env python
"""Synthetic smoke test for the selected-mode channel-resolvent workflow."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import h5py
import numpy as np

from plot_mkm_channel_resolvent import FIGURE_NAMES
from smoke_channel_resolvent_single_mode import write_tiny_fixtures


SMOKE_DIR = Path("/private/tmp/mkm_selected_modes_workflow_smoke")


def add_synthetic_modal_series(target_h5: Path) -> None:
    nt = 32
    sample_dt = 0.25
    times = np.arange(nt, dtype=float) * sample_dt

    with h5py.File(target_h5, "a") as f:
        z = f["geometry/z_wall"][:]
        k_stream = f["geometry/k_stream"][:]
        k_span = f["geometry/k_span"][:]
        nx = k_stream.size
        ny = k_span.size
        modal_dim = 3 * z.size

        u_hat = np.zeros((nt, nx, ny, modal_dim), dtype=np.complex128)
        q10 = np.zeros(modal_dim, dtype=np.complex128)
        q11 = np.zeros(modal_dim, dtype=np.complex128)
        q10[0::3] = 0.9 + 0.1j
        q10[1::3] = 0.2 - 0.15j
        q10[2::3] = 0.05j
        q11[0::3] = 0.35 - 0.2j
        q11[1::3] = 0.7 + 0.05j
        q11[2::3] = -0.1j

        phase_bin_1 = np.exp(1j * 2.0 * np.pi * np.arange(nt) / nt)
        phase_bin_2 = np.exp(1j * 4.0 * np.pi * np.arange(nt) / nt)
        u_hat[:, 1, 0, :] = phase_bin_1[:, None] * q10[None, :]
        u_hat[:, 1, 1, :] = phase_bin_2[:, None] * q11[None, :]

        f.attrs["snapshot_keys"] = ",".join(str(index) for index in range(nt))
        f.attrs["dt"] = sample_dt
        f.create_dataset("sampling/t", data=times)
        f.create_dataset("modal/u_hat", data=u_hat)


def assert_exists(path: Path) -> None:
    if not path.exists():
        raise AssertionError(f"expected output is missing: {path}")


def assert_nonempty(path: Path) -> None:
    assert_exists(path)
    if path.stat().st_size <= 0:
        raise AssertionError(f"expected non-empty output: {path}")


def main() -> int:
    SMOKE_DIR.mkdir(parents=True, exist_ok=True)
    target_h5, constraint_h5 = write_tiny_fixtures(SMOKE_DIR)
    add_synthetic_modal_series(target_h5)

    script = Path(__file__).with_name("run_mkm_channel_resolvent_selected_modes.py")
    command = [
        sys.executable,
        str(script),
        "--target-h5",
        str(target_h5),
        "--constraint-file",
        str(constraint_h5),
        "--output-dir",
        str(SMOKE_DIR),
        "--mode-index-list",
        "1",
        "0",
        "1",
        "1",
        "--compute-csd-from-target",
        "--segment-length",
        "32",
        "--overlap",
        "0.0",
        "--window",
        "none",
        "--omega-count",
        "2",
        "--n-singular",
        "3",
        "--make-figures",
        "--no-tex",
        "--overwrite",
    ]
    completed = subprocess.run(command, check=True, text=True, capture_output=True)

    manifest_path = SMOKE_DIR / "MKM_channel_resolvent_selected_modes_manifest.json"
    csd_h5 = SMOKE_DIR / "MKM_channel_modal_csd_selected_modes.h5"
    assert_nonempty(manifest_path)
    assert_nonempty(csd_h5)

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    modes = manifest["modes"]
    if len(modes) != 2:
        raise AssertionError(f"expected two mode entries, got {len(modes)}")
    if manifest["selected_modes"] != [[1, 0], [1, 1]]:
        raise AssertionError(f"unexpected selected_modes: {manifest['selected_modes']}")
    if manifest["csd"]["path"] != str(csd_h5):
        raise AssertionError("manifest does not point to the shared CSD")

    for entry in modes:
        mode = entry["mode_index"]
        i, j = mode
        resolvent_h5 = SMOKE_DIR / f"MKM_channel_resolvent_i{i}_j{j}.h5"
        projection_h5 = SMOKE_DIR / f"MKM_channel_resolvent_projection_i{i}_j{j}.h5"
        figure_dir = SMOKE_DIR / f"figures_i{i}_j{j}"
        assert_nonempty(resolvent_h5)
        assert_nonempty(projection_h5)
        if entry["resolvent_h5"] != str(resolvent_h5):
            raise AssertionError("manifest resolvent path mismatch")
        if entry["projection_h5"] != str(projection_h5):
            raise AssertionError("manifest projection path mismatch")
        if len(entry["omega"]) != 2:
            raise AssertionError(f"expected two omega values for mode {mode}, got {entry['omega']}")
        if "leading_singular_values" not in entry["resolvent_summary"]:
            raise AssertionError("manifest missing leading singular values")
        if "leading_energy_fraction" not in entry["projection_summary"]:
            raise AssertionError("manifest missing projection fractions")
        for figure_name in FIGURE_NAMES:
            assert_nonempty(figure_dir / figure_name)

    print("smoke_selected_modes_workflow: ok")
    print("workflow_stdout:")
    print(completed.stdout.strip())
    print(f"manifest_path={manifest_path}")
    print(f"shared_csd_h5={csd_h5}")
    print("mode_outputs:")
    for entry in modes:
        print(f"  mode={tuple(entry['mode_index'])}")
        print(f"    omega={entry['omega']}")
        print(f"    resolvent_h5={entry['resolvent_h5']}")
        print(f"    projection_h5={entry['projection_h5']}")
        print(f"    figure_dir={entry['figure_dir']}")
        print(f"    leading_singular_values={entry['resolvent_summary']['leading_singular_values']}")
        print(f"    leading_projection_fraction={entry['projection_summary']['leading_energy_fraction']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
