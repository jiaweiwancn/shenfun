#!/usr/bin/env python
"""Validate the fixed Re_tau=395 spin-up and sampling schedule."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def integral_count(duration: float, spacing: float, label: str) -> int:
    count = round(duration / spacing)
    if count < 0 or not math.isclose(
        count * spacing,
        duration,
        rel_tol=0.0,
        abs_tol=max(1e-10, 1e-9 * abs(duration)),
    ):
        raise ValueError(f"{label}={duration:.12g} is not an integer multiple of {spacing:.12g}")
    return count


def validate_spinup(args: argparse.Namespace) -> None:
    if args.end <= 0:
        raise ValueError("spin-up END_TIME must be positive")
    if args.end > args.target + 1e-9:
        raise ValueError(
            f"spin-up END_TIME={args.end:.12g} exceeds the fixed sampling "
            f"checkpoint time {args.target:.12g}"
        )
    steps = integral_count(args.end, args.dns_dt, "spin-up END_TIME")
    print(
        f"spinup_segment_end={args.end:.12g} "
        f"spinup_segment_end_step={steps} "
        f"sampling_checkpoint_target={args.target:.12g}"
    )
    if math.isclose(args.end, args.target, rel_tol=0.0, abs_tol=1e-9):
        print(f"SPINUP_TARGET_REACHED time={args.target:.12g}")


def validate_checkpoint(args: argparse.Namespace) -> None:
    import h5py

    path = Path(args.checkpoint).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(path)
    expected_tstep = integral_count(
        args.expected_start,
        args.dns_dt,
        "sampling start time",
    )
    with h5py.File(path, "r") as checkpoint:
        actual_time = float(checkpoint.attrs["t"])
        actual_tstep = int(checkpoint.attrs["tstep"])
    if not math.isclose(actual_time, args.expected_start, rel_tol=0.0, abs_tol=1e-8):
        raise ValueError(
            f"sampling checkpoint must be at t={args.expected_start:.12g}; "
            f"found t={actual_time:.12g}"
        )
    if actual_tstep != expected_tstep:
        raise ValueError(
            f"sampling checkpoint step must be {expected_tstep}; found {actual_tstep}"
        )
    print(
        f"sampling_checkpoint_time={actual_time:.12g} "
        f"sampling_checkpoint_tstep={actual_tstep}"
    )


def validate_segment(args: argparse.Namespace) -> None:
    tolerance = 1e-9
    if args.start < args.window_start - tolerance:
        raise ValueError(
            f"sampling cannot begin before t={args.window_start:.12g}; "
            f"checkpoint is at t={args.start:.12g}"
        )
    if args.start >= args.window_end - tolerance:
        raise ValueError(
            f"sampling window is already complete at t={args.window_end:.12g}"
        )
    if args.end <= args.start + tolerance:
        raise ValueError(
            f"END_TIME must exceed checkpoint time: {args.end:.12g} <= {args.start:.12g}"
        )
    if args.end > args.window_end + tolerance:
        raise ValueError(
            f"END_TIME={args.end:.12g} exceeds fixed sampling end "
            f"t={args.window_end:.12g}"
        )

    completed_before = integral_count(
        args.start - args.window_start,
        args.sample_dt,
        "time already sampled",
    )
    segment_samples = integral_count(
        args.end - args.start,
        args.sample_dt,
        "sampling segment duration",
    )
    if segment_samples % args.shard_samples:
        raise ValueError(
            f"segment contains {segment_samples} samples; it must contain a whole "
            f"number of {args.shard_samples}-sample state shards"
        )
    expected_total = completed_before + segment_samples
    print(f"sampling_window_start={args.window_start:.12g}")
    print(f"sampling_window_end={args.window_end:.12g}")
    print(f"sampling_segment_start={args.start:.12g}")
    print(f"sampling_segment_end={args.end:.12g}")
    print(f"sampling_segment_samples={segment_samples}")
    print(f"sampling_expected_total_samples={expected_total}")


def validate_manifest(args: argparse.Namespace) -> None:
    path = Path(args.manifest).expanduser().resolve()
    report = json.loads(path.read_text(encoding="utf-8"))
    if report.get("status") != "PASS":
        raise ValueError(f"state manifest did not pass: {report.get('status')!r}")
    expected_total = integral_count(
        args.segment_end - args.window_start,
        args.sample_dt,
        "completed sampling duration",
    )
    actual_total = int(report["total_valid_samples"])
    if actual_total != expected_total:
        raise ValueError(
            f"state manifest contains {actual_total} samples; expected "
            f"{expected_total} from t={args.window_start:.12g} through "
            f"t={args.segment_end:.12g}"
        )
    print(f"sampling_manifest_total_samples={actual_total}")
    if math.isclose(args.segment_end, args.window_end, rel_tol=0.0, abs_tol=1e-8):
        final_expected = integral_count(
            args.window_end - args.window_start,
            args.sample_dt,
            "full sampling window",
        )
        if actual_total != final_expected:
            raise ValueError(
                f"final sampling window must contain {final_expected} samples; "
                f"found {actual_total}"
            )
        print(
            f"SAMPLING_WINDOW_COMPLETE start={args.window_start:.12g} "
            f"end={args.window_end:.12g} samples={actual_total}"
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    spinup = subparsers.add_parser("spinup")
    spinup.add_argument("--end", type=float, required=True)
    spinup.add_argument("--target", type=float, required=True)
    spinup.add_argument("--dns-dt", type=float, required=True)
    spinup.set_defaults(func=validate_spinup)

    checkpoint = subparsers.add_parser("checkpoint")
    checkpoint.add_argument("--checkpoint", required=True)
    checkpoint.add_argument("--expected-start", type=float, required=True)
    checkpoint.add_argument("--dns-dt", type=float, required=True)
    checkpoint.set_defaults(func=validate_checkpoint)

    segment = subparsers.add_parser("segment")
    segment.add_argument("--start", type=float, required=True)
    segment.add_argument("--end", type=float, required=True)
    segment.add_argument("--window-start", type=float, required=True)
    segment.add_argument("--window-end", type=float, required=True)
    segment.add_argument("--sample-dt", type=float, required=True)
    segment.add_argument("--shard-samples", type=int, required=True)
    segment.set_defaults(func=validate_segment)

    manifest = subparsers.add_parser("manifest")
    manifest.add_argument("--manifest", required=True)
    manifest.add_argument("--segment-end", type=float, required=True)
    manifest.add_argument("--window-start", type=float, required=True)
    manifest.add_argument("--window-end", type=float, required=True)
    manifest.add_argument("--sample-dt", type=float, required=True)
    manifest.set_defaults(func=validate_manifest)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
