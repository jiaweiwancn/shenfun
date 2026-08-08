"""Parallel raw checkpoints and lightweight station outputs for HIT DNS."""

from __future__ import annotations

import csv
import json
import os
from pathlib import Path
from typing import Any

import h5py
import numpy as np
from mpi4py import MPI


SCHEMA_VERSION = "hit_dns_checkpoint_v1"


def _json_default(value: Any) -> Any:
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, np.ndarray):
        return value.tolist()
    raise TypeError(f"Cannot serialize {type(value).__name__}")


def json_text(value: Any) -> str:
    return json.dumps(value, default=_json_default, sort_keys=True)


def ensure_directory(path: Path, comm: MPI.Comm = MPI.COMM_WORLD) -> None:
    if comm.rank == 0:
        path.mkdir(parents=True, exist_ok=True)
    comm.Barrier()


def station_slug(station: float) -> str:
    text = f"{float(station):09.4f}".rstrip("0").rstrip(".")
    return text.replace(".", "p")


def write_checkpoint(
    path: Path,
    context: Any,
    global_shape: tuple[int, int, int],
    time_s: float,
    tstep: int,
    nominal_dt_s: float,
    configuration: dict[str, Any],
    initialization: dict[str, Any],
    station: float | None = None,
    comm: MPI.Comm = MPI.COMM_WORLD,
) -> None:
    """Collectively write a spectral checkpoint, then atomically publish it."""

    ensure_directory(path.parent, comm)
    partial = path.with_name(path.name + ".partial")
    global_spectral_shape = (
        3,
        global_shape[0],
        global_shape[1],
        global_shape[2] // 2 + 1,
    )
    local_slice = (slice(None),) + tuple(context.T.local_slice(True))
    with h5py.File(partial, "w", driver="mpio", comm=comm) as output:
        velocity = output.create_dataset("U_hat", global_spectral_shape, dtype=context.U_hat.dtype)
        velocity[local_slice] = np.asarray(context.U_hat)
        output.attrs["schema_version"] = SCHEMA_VERSION
        output.attrs["time_s"] = float(time_s)
        output.attrs["tstep"] = int(tstep)
        output.attrs["nominal_dt_s"] = float(nominal_dt_s)
        output.attrs["station_tU0_over_M"] = np.nan if station is None else float(station)
        output.attrs["configuration_json"] = json_text(configuration)
        output.attrs["initialization_json"] = json_text(initialization)
    comm.Barrier()
    if comm.rank == 0:
        os.replace(partial, path)
    comm.Barrier()


def load_checkpoint(
    path: Path,
    context: Any,
    global_shape: tuple[int, int, int],
    comm: MPI.Comm = MPI.COMM_WORLD,
) -> dict[str, Any]:
    """Collectively restore ``U_hat`` and return checkpoint metadata."""

    expected_shape = (3, global_shape[0], global_shape[1], global_shape[2] // 2 + 1)
    local_slice = (slice(None),) + tuple(context.T.local_slice(True))
    with h5py.File(path, "r", driver="mpio", comm=comm) as source:
        if source.attrs.get("schema_version") != SCHEMA_VERSION:
            raise ValueError(f"Unsupported checkpoint schema in {path}")
        if tuple(source["U_hat"].shape) != expected_shape:
            raise ValueError(
                f"Checkpoint shape {source['U_hat'].shape} does not match {expected_shape}"
            )
        context.U_hat[...] = source["U_hat"][local_slice]
        station_value = float(source.attrs["station_tU0_over_M"])
        metadata = {
            "time_s": float(source.attrs["time_s"]),
            "tstep": int(source.attrs["tstep"]),
            "nominal_dt_s": float(source.attrs["nominal_dt_s"]),
            "station_tU0_over_M": None if np.isnan(station_value) else station_value,
            "configuration": json.loads(source.attrs["configuration_json"]),
            "initialization": json.loads(source.attrs["initialization_json"]),
        }
    return metadata


def write_station_lightweight(
    output_dir: Path,
    station: float,
    summary: dict[str, Any],
    spectra: dict[str, Any],
    comm: MPI.Comm = MPI.COMM_WORLD,
) -> None:
    """Write small JSON and CSV products; all raw fields remain server-side."""

    ensure_directory(output_dir, comm)
    if comm.rank != 0:
        return
    slug = station_slug(station)
    summary_path = output_dir / f"station_{slug}_summary.json"
    summary_path.write_text(json.dumps(summary, default=_json_default, indent=2, sort_keys=True) + "\n")
    np.savetxt(
        output_dir / f"station_{slug}_E.csv",
        np.column_stack((spectra["k_cm^-1"], spectra["E_cm3_s^-2"], spectra["shell_mode_multiplicity"])),
        delimiter=",",
        header="k_cm^-1,E_cm3_s^-2,shell_mode_multiplicity",
        comments="",
    )
    np.savetxt(
        output_dir / f"station_{slug}_E11.csv",
        np.column_stack((spectra["k1_cm^-1"], spectra["E11_cm3_s^-2"])),
        delimiter=",",
        header="k1_cm^-1,E11_cm3_s^-2",
        comments="",
    )


def append_diagnostic_row(
    path: Path,
    row: dict[str, Any],
    comm: MPI.Comm = MPI.COMM_WORLD,
) -> None:
    """Append one root-rank row to the lightweight monitoring log."""

    if comm.rank != 0:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    exists = path.exists()
    with path.open("a", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(row))
        if not exists:
            writer.writeheader()
        writer.writerow(row)
