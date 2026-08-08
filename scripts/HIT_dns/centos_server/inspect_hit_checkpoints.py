#!/usr/bin/env python3
"""List complete HIT checkpoints and identify the latest restart candidate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import h5py


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--require", type=Path, help="Fail unless this file is valid and latest.")
    return parser.parse_args()


def inspect(path: Path) -> dict[str, object]:
    with h5py.File(path, "r") as source:
        schema = source.attrs.get("schema_version")
        if isinstance(schema, bytes):
            schema = schema.decode()
        if schema != "hit_dns_checkpoint_v1":
            raise ValueError(f"unexpected schema {schema!r}")
        configuration = json.loads(source.attrs["configuration_json"])
        shape = tuple(int(value) for value in source["U_hat"].shape)
        expected = (3, int(configuration["n"]), int(configuration["n"]), int(configuration["n"]) // 2 + 1)
        if shape != expected:
            raise ValueError(f"U_hat shape {shape} != {expected}")
        return {
            "path": str(path.resolve()),
            "time_s": float(source.attrs["time_s"]),
            "tstep": int(source.attrs["tstep"]),
            "station_tU0_over_M": float(source.attrs["station_tU0_over_M"]),
            "backend": configuration.get("backend", "unrecorded"),
            "shape": shape,
        }


def main() -> None:
    args = parse_args()
    raw_dir = args.run_dir.expanduser().resolve() / "raw"
    valid: list[dict[str, object]] = []
    invalid: list[tuple[Path, str]] = []
    for path in sorted(raw_dir.glob("*.h5")):
        try:
            valid.append(inspect(path))
        except (OSError, KeyError, TypeError, ValueError) as error:
            invalid.append((path, str(error)))

    for path, error in invalid:
        print(f"INVALID path={path} reason={error}")
    if not valid:
        raise SystemExit(f"no complete HIT checkpoints found below {raw_dir}")
    valid.sort(key=lambda item: (int(item["tstep"]), str(item["path"])))
    for item in valid:
        print(
            "VALID "
            f"tstep={item['tstep']} time_s={item['time_s']:.12g} "
            f"backend={item['backend']} path={item['path']}"
        )
    latest = valid[-1]
    print(f"LATEST_CHECKPOINT={latest['path']}")

    if args.require is not None:
        required = str(args.require.expanduser().resolve())
        if required != latest["path"]:
            raise SystemExit(
                f"required restart is not the latest complete checkpoint: {required} != {latest['path']}"
            )


if __name__ == "__main__":
    main()
