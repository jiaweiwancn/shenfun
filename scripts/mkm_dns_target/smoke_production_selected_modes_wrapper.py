#!/usr/bin/env python
"""Smoke test the production selected-mode wrapper without production files."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


TMP_DIR = Path("/private/tmp/mkm_production_selected_modes_wrapper_smoke")


def main() -> int:
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    script = Path(__file__).with_name("run_mkm_channel_resolvent_production_selected_modes.py")

    dry_run_command = [
        sys.executable,
        str(script),
        "--dry-run",
        "--print-ssh-command",
        "--mode-index-list",
        "1",
        "0",
        "1",
        "1",
        "--omega-count",
        "2",
        "--skip-plots",
    ]
    dry_run = subprocess.run(dry_run_command, text=True, capture_output=True, check=True)
    required_dry_run_strings = (
        "Resolved selected-mode production workflow:",
        "Equivalent selected-mode workflow command:",
        "Recommended SSH command:",
        "ssh jay@100.88.70.60",
        "run_mkm_channel_resolvent_production_selected_modes.py",
        "MKM_channel_resolvent_selected_modes_manifest.json",
    )
    for text in required_dry_run_strings:
        if text not in dry_run.stdout:
            raise AssertionError(f"dry-run output did not contain {text!r}")
    if "Traceback" in dry_run.stdout or dry_run.stderr:
        raise AssertionError("dry-run produced a traceback")

    missing_command = [
        sys.executable,
        str(script),
        "--target-h5",
        str(TMP_DIR / "missing_target.h5"),
        "--constraint-file",
        str(TMP_DIR / "missing_constraints.h5"),
        "--output-dir",
        str(TMP_DIR / "out"),
        "--mode-index-list",
        "1",
        "0",
        "--skip-plots",
    ]
    missing = subprocess.run(missing_command, text=True, capture_output=True, check=False)
    if missing.returncode != 2:
        raise AssertionError(f"missing-file command returned {missing.returncode}, expected 2")
    required_missing_strings = (
        "Production selected-mode workflow could not run",
        "Missing paths:",
        "missing_target.h5",
        "missing_constraints.h5",
        "Recommended server command:",
        "ssh jay@100.88.70.60",
    )
    for text in required_missing_strings:
        if text not in missing.stdout:
            raise AssertionError(f"missing-file output did not contain {text!r}")
    if "Traceback" in missing.stdout or missing.stderr:
        raise AssertionError("missing-file path produced a traceback")

    print("smoke_production_selected_modes_wrapper: ok")
    print("dry_run_stdout:")
    print(dry_run.stdout.strip())
    print("missing_file_stdout:")
    print(missing.stdout.strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
