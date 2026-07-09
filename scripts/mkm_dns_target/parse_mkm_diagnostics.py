#!/usr/bin/env python
"""Parse MKM stdout diagnostics into a JSON stationarity summary."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import numpy as np


LINE_RE = re.compile(
    r"Time\s+"
    r"(?P<time>[-+0-9.eE]+)\s+Energy\s+"
    r"(?P<energy_wallnormal>[-+0-9.eE]+)\s+"
    r"(?P<energy_streamwise>[-+0-9.eE]+)\s+"
    r"(?P<energy_spanwise>[-+0-9.eE]+)\s+Flux\s+"
    r"(?P<flux>[-+0-9.eE]+)\s+"
    r"(?P<dp_correction>[-+0-9.eE]+)\s+div\s+"
    r"(?P<divergence_l2>[-+0-9.eE]+)"
)


COLUMNS = (
    "energy_wallnormal",
    "energy_streamwise",
    "energy_spanwise",
    "flux",
    "dp_correction",
    "divergence_l2",
)


def parse_logs(paths: list[Path]) -> list[dict[str, float | str]]:
    records: list[dict[str, float | str]] = []
    for path in paths:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for line_number, line in enumerate(f, start=1):
                match = LINE_RE.search(line)
                if not match:
                    continue
                record: dict[str, float | str] = {
                    "source": str(path),
                    "line_number": line_number,
                    "time": float(match.group("time")),
                }
                for column in COLUMNS:
                    record[column] = float(match.group(column))
                records.append(record)
    records.sort(key=lambda item: (float(item["time"]), str(item["source"]), int(item["line_number"])))
    return records


def rel_change(a: float, b: float, scale: float) -> float:
    return abs(b - a) / max(abs(scale), 1e-300)


def block_summaries(records: list[dict[str, float | str]], n_blocks: int) -> list[dict[str, object]]:
    n_blocks = min(max(1, n_blocks), len(records))
    blocks = np.array_split(np.arange(len(records)), n_blocks)
    summaries = []
    for block in blocks:
        if len(block) == 0:
            continue
        selected = [records[int(i)] for i in block]
        summary: dict[str, object] = {
            "n_records": len(selected),
            "time_range": [float(selected[0]["time"]), float(selected[-1]["time"])],
        }
        for column in COLUMNS:
            values = np.array([float(record[column]) for record in selected], dtype=float)
            summary[column] = {
                "mean": float(values.mean()),
                "std": float(values.std(ddof=0)),
                "first": float(values[0]),
                "last": float(values[-1]),
                "min": float(values.min()),
                "max": float(values.max()),
            }
        summaries.append(summary)
    return summaries


def global_summary(records: list[dict[str, float | str]]) -> dict[str, object]:
    summary: dict[str, object] = {
        "n_records": len(records),
        "time_range": [float(records[0]["time"]), float(records[-1]["time"])],
    }
    for column in COLUMNS:
        values = np.array([float(record[column]) for record in records], dtype=float)
        summary[column] = {
            "mean": float(values.mean()),
            "std": float(values.std(ddof=0)),
            "first": float(values[0]),
            "last": float(values[-1]),
            "min": float(values.min()),
            "max": float(values.max()),
        }
    return summary


def drift_summary(
    records: list[dict[str, float | str]],
    blocks: list[dict[str, object]],
    tolerance: float,
    divergence_threshold: float,
) -> dict[str, object]:
    all_stats = global_summary(records)
    first_block = blocks[0]
    last_block = blocks[-1]
    first_last_rel = {}
    for column in COLUMNS:
        first_mean = float(first_block[column]["mean"])  # type: ignore[index]
        last_mean = float(last_block[column]["mean"])  # type: ignore[index]
        scale = float(all_stats[column]["mean"])  # type: ignore[index]
        first_last_rel[column] = rel_change(first_mean, last_mean, scale)

    successive_rel: list[dict[str, object]] = []
    for i in range(1, len(blocks)):
        item: dict[str, object] = {"from_block": i - 1, "to_block": i}
        for column in COLUMNS:
            a = float(blocks[i - 1][column]["mean"])  # type: ignore[index]
            b = float(blocks[i][column]["mean"])  # type: ignore[index]
            scale = float(all_stats[column]["mean"])  # type: ignore[index]
            item[column] = rel_change(a, b, scale)
        successive_rel.append(item)

    monitored = ("energy_wallnormal", "energy_streamwise", "energy_spanwise", "flux")
    max_first_last_monitored = max(first_last_rel[column] for column in monitored)
    max_successive_monitored = 0.0
    if successive_rel:
        max_successive_monitored = max(
            float(item[column]) for item in successive_rel for column in monitored
        )
    max_divergence = max(float(record["divergence_l2"]) for record in records)
    stationary_by_tolerance = bool(
        max_first_last_monitored <= tolerance
        and max_successive_monitored <= 2.0 * tolerance
        and max_divergence <= divergence_threshold
    )
    return {
        "first_last_block_relative_change": first_last_rel,
        "successive_block_relative_change": successive_rel,
        "monitored_columns": monitored,
        "max_first_last_monitored": max_first_last_monitored,
        "max_successive_monitored": max_successive_monitored,
        "tolerance": tolerance,
        "max_divergence_l2": max_divergence,
        "divergence_threshold": divergence_threshold,
        "stationary_by_tolerance": stationary_by_tolerance,
        "note": (
            "This is a scalar diagnostic smoke test. A production decision should "
            "also inspect mean/Reynolds block convergence from sampled fields."
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--logs", nargs="+", required=True, help="MKM stdout log files.")
    parser.add_argument("--output", required=True, help="Output JSON report.")
    parser.add_argument("--n-blocks", type=int, default=4)
    parser.add_argument("--tolerance", type=float, default=0.02,
                        help="Relative tolerance for block-drift smoke flag.")
    parser.add_argument("--divergence-threshold", type=float, default=1e-10)
    parser.add_argument("--store-series", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    paths = [Path(path).expanduser().resolve() for path in args.logs]
    records = parse_logs(paths)
    if not records:
        raise ValueError("no MKM diagnostic lines found")

    blocks = block_summaries(records, args.n_blocks)
    report = {
        "logs": [str(path) for path in paths],
        "global": global_summary(records),
        "blocks": blocks,
        "drift": drift_summary(records, blocks, args.tolerance, args.divergence_threshold),
    }
    if args.store_series:
        report["series"] = records

    output = Path(args.output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with open(output, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"wrote={output}")
    print(f"records={len(records)}")
    print(f"time_range={records[0]['time']:.12g},{records[-1]['time']:.12g}")
    print(f"max_first_last_monitored={report['drift']['max_first_last_monitored']:.6e}")
    print(f"max_successive_monitored={report['drift']['max_successive_monitored']:.6e}")
    print(f"stationary_by_tolerance={report['drift']['stationary_by_tolerance']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
