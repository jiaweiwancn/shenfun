#!/usr/bin/env python
"""Synthetic smoke test for selected-mode workflow Markdown reporting."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

from smoke_channel_resolvent_single_mode import write_tiny_fixtures
from smoke_selected_modes_workflow import add_synthetic_modal_series


SMOKE_BASE = Path("/private/tmp/mkm_workflow_report_smoke")


def main() -> int:
    SMOKE_BASE.mkdir(parents=True, exist_ok=True)
    run_dir = Path(tempfile.mkdtemp(prefix="run_", dir=SMOKE_BASE))
    target_h5, constraint_h5 = write_tiny_fixtures(run_dir)
    add_synthetic_modal_series(target_h5)

    workflow_script = Path(__file__).with_name("run_mkm_channel_resolvent_selected_modes.py")
    report_script = Path(__file__).with_name("report_mkm_channel_resolvent_workflow.py")
    workflow_command = [
        sys.executable,
        str(workflow_script),
        "--target-h5",
        str(target_h5),
        "--constraint-file",
        str(constraint_h5),
        "--output-dir",
        str(run_dir),
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
    workflow = subprocess.run(workflow_command, check=True, text=True, capture_output=True)

    manifest = run_dir / "MKM_channel_resolvent_selected_modes_manifest.json"
    report = run_dir / "MKM_channel_resolvent_selected_modes_report.md"
    report_command = [
        sys.executable,
        str(report_script),
        "--manifest",
        str(manifest),
        "--output",
        str(report),
        "--max-omega",
        "2",
    ]
    completed = subprocess.run(report_command, check=True, text=True, capture_output=True)

    if not report.exists() or report.stat().st_size <= 0:
        raise AssertionError(f"report was not created: {report}")
    text = report.read_text(encoding="utf-8")
    required = (
        "## Summary",
        "## Shared CSD",
        "## Mode Results",
        "### Mode (1, 0)",
        "### Mode (1, 1)",
        "mkm_resolvent_mode_shapes.pdf",
        "sigma1",
        "lead fraction",
    )
    for needle in required:
        if needle not in text:
            raise AssertionError(f"report does not contain {needle!r}")

    print("smoke_workflow_report: ok")
    print("workflow_stdout:")
    print(workflow.stdout.strip())
    print("report_stdout:")
    print(completed.stdout.strip())
    print(f"manifest_path={manifest}")
    print(f"report_path={report}")
    print("report_excerpt:")
    excerpt_lines = text.splitlines()[:42]
    print("\n".join(excerpt_lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
