#!/usr/bin/env python
"""Audit MKM independent-state shard metadata and temporal continuity."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import h5py
import numpy as np


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--shards", nargs="+", required=True)
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--sha256", action="store_true",
                        help="Hash every complete shard; expensive for production-sized files.")
    parser.add_argument(
        "--check-finite",
        action="store_true",
        help="Scan every valid state value for NaN/Inf; expensive for production-sized shards.",
    )
    return parser.parse_args()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(16 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    args = parse_args()
    paths = sorted({Path(value).expanduser().resolve() for value in args.shards})
    if not paths:
        raise ValueError("no state shards supplied")

    errors: list[str] = []
    records: list[dict[str, object]] = []
    all_steps: list[np.ndarray] = []
    all_times: list[np.ndarray] = []
    reference: dict[str, object] | None = None

    for path in paths:
        if not path.is_file():
            errors.append(f"missing shard: {path}")
            continue
        with h5py.File(path, "r") as f:
            schema = f.attrs.get("schema_version", "")
            if isinstance(schema, bytes):
                schema = schema.decode("utf-8")
            valid = int(f.attrs.get("valid_samples", -1))
            complete = bool(f.attrs.get("complete", False))
            if schema != "mkm-independent-state-v1":
                errors.append(f"{path.name}: unexpected schema {schema!r}")
            if valid <= 0 or valid > f["sampling/tstep"].shape[0]:
                errors.append(f"{path.name}: invalid valid_samples={valid}")
                continue
            if not complete:
                errors.append(f"{path.name}: shard is not marked complete")

            steps = np.asarray(f["sampling/tstep"][:valid], dtype=np.int64)
            times = np.asarray(f["sampling/t"][:valid], dtype=np.float64)
            every = int(f.attrs["sample_every_steps"])
            dt = float(f.attrs["dns_dt"])
            shape_physical = tuple(int(v) for v in f.attrs["global_shape_physical"])
            shape_spectral = tuple(int(v) for v in f.attrs["global_shape_spectral"])
            precision = str(f.attrs["precision"])
            compression = str(f.attrs["compression"])
            if np.any(steps < 0) or np.any(~np.isfinite(times)):
                errors.append(f"{path.name}: unwritten entries occur inside valid range")
            if valid > 1 and not np.all(np.diff(steps) == every):
                errors.append(f"{path.name}: nonuniform step spacing")
            if valid > 1 and not np.allclose(np.diff(times), every * dt, rtol=1e-10, atol=1e-12):
                errors.append(f"{path.name}: nonuniform physical-time spacing")

            nonfinite_values = 0
            if args.check_finite:
                for dataset_name in (
                    "state/u_wall_hat",
                    "state/eta_wall_hat",
                    "state/u_stream_zero_mode",
                    "state/u_span_zero_mode",
                ):
                    dataset = f[dataset_name]
                    for sample_index in range(valid):
                        values = dataset[sample_index]
                        nonfinite_values += int(
                            values.size - np.count_nonzero(np.isfinite(values))
                        )
                if nonfinite_values:
                    errors.append(
                        f"{path.name}: valid state range contains "
                        f"{nonfinite_values} non-finite values"
                    )

            invariant = {
                "schema_version": schema,
                "sample_every_steps": every,
                "dns_dt": dt,
                "global_shape_physical": shape_physical,
                "global_shape_spectral": shape_spectral,
                "precision": precision,
            }
            if reference is None:
                reference = invariant
            elif invariant != reference:
                errors.append(f"{path.name}: invariant metadata differs from the first shard")

            record: dict[str, object] = {
                "path": str(path),
                "size_bytes": path.stat().st_size,
                "valid_samples": valid,
                "complete": complete,
                "first_tstep": int(steps[0]),
                "last_tstep": int(steps[-1]),
                "first_time": float(times[0]),
                "last_time": float(times[-1]),
                "compression": compression,
                "finite_values_checked": bool(args.check_finite),
                "nonfinite_values": int(nonfinite_values),
            }
            if args.sha256:
                record["sha256"] = sha256_file(path)
            records.append(record)
            all_steps.append(steps)
            all_times.append(times)

    if all_steps and reference is not None:
        order = np.argsort([int(steps[0]) for steps in all_steps])
        sorted_steps = [all_steps[int(index)] for index in order]
        sorted_times = [all_times[int(index)] for index in order]
        every = int(reference["sample_every_steps"])
        dt = float(reference["dns_dt"])
        for index in range(1, len(sorted_steps)):
            if int(sorted_steps[index][0] - sorted_steps[index - 1][-1]) != every:
                errors.append(
                    "gap or overlap between shards ending at "
                    f"{int(sorted_steps[index - 1][-1])} and starting at "
                    f"{int(sorted_steps[index][0])}"
                )
            time_delta = float(sorted_times[index][0] - sorted_times[index - 1][-1])
            if not np.isclose(time_delta, every * dt, rtol=1e-10, atol=1e-12):
                errors.append(
                    "physical-time gap or overlap between shards ending at "
                    f"{float(sorted_times[index - 1][-1]):.12g} and starting at "
                    f"{float(sorted_times[index][0]):.12g}"
                )

    status = "PASS" if not errors and len(records) == len(paths) else "FAIL"
    report = {
        "material_passport": {
            "origin_skill": "experiment-agent",
            "origin_mode": "validate",
            "origin_date": "2026-07-24",
            "verification_status": "VERIFIED" if status == "PASS" else "ANALYZED",
            "version_label": "mkm_state_manifest_v2",
        },
        "status": status,
        "sha256_enabled": bool(args.sha256),
        "finite_check_enabled": bool(args.check_finite),
        "shard_count": len(records),
        "total_valid_samples": int(sum(int(record["valid_samples"]) for record in records)),
        "total_size_bytes": int(sum(int(record["size_bytes"]) for record in records)),
        "invariant_metadata": reference,
        "errors": errors,
        "shards": records,
    }
    output = Path(args.output_json).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as stream:
        json.dump(report, stream, indent=2)
    print(json.dumps(report, indent=2))
    print(f"state_manifest_json={output}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
