#!/usr/bin/env python
"""Smoke test the first channel-resolvent plotting layer."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import numpy as np

from compute_mkm_channel_resolvent import compute_single_mode_resolvent
from plot_mkm_channel_resolvent import FIGURE_NAMES
from smoke_channel_resolvent_single_mode import write_tiny_fixtures


SMOKE_DIR = Path("/private/tmp/mkm_channel_resolvent_plot_smoke")


def main() -> int:
    SMOKE_DIR.mkdir(parents=True, exist_ok=True)
    target_h5, constraint_h5 = write_tiny_fixtures(SMOKE_DIR)
    resolvent_h5 = SMOKE_DIR / "synthetic_resolvent_for_plots.h5"
    figure_dir = SMOKE_DIR / "figures"
    figure_dir.mkdir(parents=True, exist_ok=True)
    for name in FIGURE_NAMES:
        path = figure_dir / name
        if path.exists():
            path.unlink()

    compute_single_mode_resolvent(
        target_h5,
        constraint_h5,
        resolvent_h5,
        mode_index=(1, 1),
        omega=np.array([0.45, 0.75, 1.05]),
        n_singular=4,
        overwrite=True,
    )

    script = Path(__file__).with_name("plot_mkm_channel_resolvent.py")
    command = [
        sys.executable,
        str(script),
        "--resolvent-h5",
        str(resolvent_h5),
        "--figure-dir",
        str(figure_dir),
        "--omega-index",
        "1",
        "--singular-index",
        "0",
        "--n-shapes",
        "3",
        "--phase",
        "0.25",
        "--n-stream",
        "48",
        "--n-span",
        "48",
        "--no-tex",
    ]
    completed = subprocess.run(command, check=True, text=True, capture_output=True)

    missing_or_empty = []
    for name in FIGURE_NAMES:
        path = figure_dir / name
        if not path.exists() or path.stat().st_size <= 1024:
            missing_or_empty.append(path)
    if missing_or_empty:
        raise AssertionError(f"missing or empty plot outputs: {missing_or_empty}")

    print("smoke_channel_resolvent_plot: ok")
    print(f"resolvent_h5={resolvent_h5}")
    print("plotter_stdout:")
    print(completed.stdout.strip())
    print("figure_outputs:")
    for name in FIGURE_NAMES:
        path = figure_dir / name
        print(f"  {path} size_bytes={path.stat().st_size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
