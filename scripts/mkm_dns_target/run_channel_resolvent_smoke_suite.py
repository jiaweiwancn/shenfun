#!/usr/bin/env python
"""Run the MKM channel-resolvent smoke-test suite."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


SMOKE_SCRIPTS = (
    "smoke_channel_resolvent_utils.py",
    "smoke_channel_resolvent_single_mode.py",
    "smoke_channel_resolvent_plot.py",
    "smoke_modal_csd.py",
    "smoke_project_dns_onto_resolvent.py",
    "smoke_selected_modes_workflow.py",
    "smoke_production_selected_modes_wrapper.py",
    "smoke_workflow_report.py",
)
TAIL_LINES = 24


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--python", default=sys.executable, help="Python executable used for each smoke.")
    parser.add_argument(
        "--stop-on-failure",
        dest="stop_on_failure",
        action="store_true",
        default=True,
        help="Stop after the first failing smoke. This is the default.",
    )
    parser.add_argument(
        "--keep-going",
        dest="stop_on_failure",
        action="store_false",
        help="Run all smokes even if one fails.",
    )
    parser.add_argument("--json-summary", help="Optional path for machine-readable run summary.")
    parser.add_argument("--quiet", action="store_true", help="Suppress per-smoke progress lines.")
    return parser.parse_args()


def output_tail(text: str, max_lines: int = TAIL_LINES) -> str:
    lines = text.splitlines()
    if len(lines) <= max_lines:
        return "\n".join(lines)
    return "\n".join(lines[-max_lines:])


def run_smoke(python: str, script: Path, quiet: bool) -> dict[str, Any]:
    command = [python, str(script)]
    if not quiet:
        print(f"running {script.name} ...", flush=True)
    start = time.perf_counter()
    completed = subprocess.run(command, text=True, capture_output=True, check=False)
    elapsed = time.perf_counter() - start
    combined_output = "\n".join(part for part in (completed.stdout, completed.stderr) if part)
    return {
        "name": script.name,
        "path": str(script),
        "command": command,
        "returncode": int(completed.returncode),
        "elapsed_seconds": elapsed,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "output_tail": output_tail(combined_output),
    }


def status_label(returncode: int) -> str:
    return "PASS" if returncode == 0 else "FAIL"


def print_table(results: list[dict[str, Any]]) -> None:
    name_width = max(len("Smoke"), *(len(result["name"]) for result in results))
    print()
    print(f"{'Smoke':<{name_width}}  {'Status':<6}  {'Return':>6}  {'Seconds':>8}")
    print(f"{'-' * name_width}  {'-' * 6}  {'-' * 6}  {'-' * 8}")
    for result in results:
        print(
            f"{result['name']:<{name_width}}  "
            f"{status_label(result['returncode']):<6}  "
            f"{result['returncode']:>6}  "
            f"{result['elapsed_seconds']:>8.2f}"
        )


def write_json_summary(path: Path, results: list[dict[str, Any]], exit_code: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "exit_code": exit_code,
        "all_passed": exit_code == 0,
        "smoke_count": len(results),
        "total_elapsed_seconds": float(sum(result["elapsed_seconds"] for result in results)),
        "results": [
            {
                "name": result["name"],
                "path": result["path"],
                "command": result["command"],
                "returncode": result["returncode"],
                "elapsed_seconds": result["elapsed_seconds"],
                "output_tail": result["output_tail"],
            }
            for result in results
        ],
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> int:
    args = parse_args()
    script_dir = Path(__file__).resolve().parent
    results: list[dict[str, Any]] = []

    for script_name in SMOKE_SCRIPTS:
        result = run_smoke(args.python, script_dir / script_name, args.quiet)
        results.append(result)
        if result["returncode"] != 0:
            print(f"\nFAILED: {script_name}")
            if result["output_tail"]:
                print("output tail:")
                print(result["output_tail"])
            if args.stop_on_failure:
                break

    failures = [result for result in results if result["returncode"] != 0]
    exit_code = 1 if failures else 0
    print_table(results)
    total_elapsed = sum(result["elapsed_seconds"] for result in results)
    print()
    print(
        f"smoke_suite: {'ok' if exit_code == 0 else 'failed'} "
        f"passed={len(results) - len(failures)} failed={len(failures)} "
        f"elapsed={total_elapsed:.2f}s"
    )
    if args.json_summary:
        summary_path = Path(args.json_summary).expanduser().resolve()
        write_json_summary(summary_path, results, exit_code)
        print(f"json_summary={summary_path}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
