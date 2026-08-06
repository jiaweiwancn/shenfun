#!/usr/bin/env python
"""Parallel, restart-safe output for the independent MKM spectral state."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
from typing import Any

import h5py
import numpy as np


def _slice_bounds(local_slice: tuple[slice, ...]) -> tuple[np.ndarray, np.ndarray]:
    starts = np.array([0 if item.start is None else item.start for item in local_slice], dtype=np.int64)
    stops = np.array([item.stop for item in local_slice], dtype=np.int64)
    return starts, stops


def _open_h5(path: Path, mode: str, comm: Any) -> h5py.File:
    """Use MPI HDF5 in parallel and permit serial metadata tests locally."""
    comm_size = comm.size if hasattr(comm, "size") else comm.Get_size()
    if comm_size == 1 and not h5py.get_config().mpi:
        return h5py.File(path, mode)
    return h5py.File(path, mode, driver="mpio", comm=comm)


def _compression_kwargs(
    compression: str,
    gzip_level: int,
    global_shape: tuple[int, int, int],
) -> dict[str, Any]:
    if compression == "none":
        return {}
    if compression != "gzip":
        raise ValueError(f"unsupported state compression {compression!r}")
    nwall, nstream, nspan_r2c = global_shape
    return {
        "compression": "gzip",
        "compression_opts": gzip_level,
        "shuffle": True,
        "chunks": (1, min(8, nwall), nstream, nspan_r2c),
    }


@dataclass(frozen=True)
class ClosedShard:
    path: Path
    samples: int
    first_tstep: int
    last_tstep: int
    full: bool
    run_completed: bool


class MKMStateShardWriter:
    """Write lossless samples of the two independent KMM state variables.

    The two nonzero-horizontal-mode velocity components are reconstructed from
    ``u_wall_hat`` and ``eta_wall_hat``. The separately evolved streamwise and
    spanwise zero-horizontal-mode profiles are stored alongside them.
    """

    schema_version = "mkm-independent-state-v1"

    def __init__(
        self,
        solver: Any,
        output_dir: str | Path,
        prefix: str,
        every: int,
        shard_samples: int,
        dt: float,
        comm: Any,
        compression: str = "none",
        gzip_level: int = 4,
        run_metadata: dict[str, Any] | None = None,
    ) -> None:
        if every <= 0:
            raise ValueError("state sampling cadence must be positive")
        if shard_samples <= 0:
            raise ValueError("state shard sample count must be positive")
        if not 0 <= gzip_level <= 9:
            raise ValueError("gzip level must be between 0 and 9")

        self.solver = solver
        self.output_dir = Path(output_dir).expanduser().resolve()
        self.prefix = prefix
        self.every = int(every)
        self.shard_samples = int(shard_samples)
        self.dt = float(dt)
        self.comm = comm
        self.compression = compression
        self.gzip_level = int(gzip_level)
        self.run_metadata = dict(run_metadata or {})

        self.u_wall_hat = solver.u_[0]
        self.eta_wall_hat = solver.g_
        self.global_shape = tuple(int(value) for value in self.u_wall_hat.global_shape)
        if len(self.global_shape) != 3:
            raise ValueError(f"expected a three-dimensional scalar state, got {self.global_shape}")
        if tuple(int(value) for value in self.eta_wall_hat.global_shape) != self.global_shape:
            raise ValueError("wall-normal velocity and vorticity global shapes differ")
        self.local_slice = tuple(self.u_wall_hat.local_slice())
        if tuple(self.eta_wall_hat.local_slice()) != self.local_slice:
            raise ValueError("wall-normal velocity and vorticity MPI slices differ")

        if self.comm.rank == 0:
            self.output_dir.mkdir(parents=True, exist_ok=True)
        self.comm.Barrier()

        self.file: h5py.File | None = None
        self.partial_path: Path | None = None
        self.final_path: Path | None = None
        self.sample_index = 0
        self.first_tstep = -1
        self.last_tstep = -1
        self.closed_shards: list[ClosedShard] = []

    def _open_shard(self, first_tstep: int) -> None:
        stem = f"{self.prefix}_tstep{first_tstep:012d}"
        partial_path = self.output_dir / f"{stem}.partial.h5"
        final_path = self.output_dir / f"{stem}.h5"
        conflict = None
        if self.comm.rank == 0:
            for path in (partial_path, final_path):
                if path.exists():
                    conflict = str(path)
                    break
        conflict = self.comm.bcast(conflict, root=0)
        if conflict is not None:
            raise FileExistsError(
                f"refusing to overwrite an existing state shard: {conflict}; "
                "preserve or rename it before restarting"
            )

        f = _open_h5(partial_path, "w", self.comm)
        compression_kwargs = _compression_kwargs(
            self.compression,
            self.gzip_level,
            self.global_shape,
        )
        state_shape = (self.shard_samples,) + self.global_shape
        f.create_group("sampling")
        f.create_group("state")
        f.create_group("geometry")
        f.create_group("mpi")
        f.create_dataset("sampling/t", shape=(self.shard_samples,), dtype=np.float64, fillvalue=np.nan)
        f.create_dataset("sampling/tstep", shape=(self.shard_samples,), dtype=np.int64, fillvalue=-1)
        f.create_dataset(
            "state/u_wall_hat",
            shape=state_shape,
            dtype=np.complex128,
            **compression_kwargs,
        )
        f.create_dataset(
            "state/eta_wall_hat",
            shape=state_shape,
            dtype=np.complex128,
            **compression_kwargs,
        )
        f.create_dataset(
            "state/u_stream_zero_mode",
            shape=(self.shard_samples, self.global_shape[0]),
            dtype=np.float64,
        )
        f.create_dataset(
            "state/u_span_zero_mode",
            shape=(self.shard_samples, self.global_shape[0]),
            dtype=np.float64,
        )

        nwall, nstream, nspan_r2c = self.global_shape
        wall_a, wall_b = self.solver.B0.domain
        stream_a, stream_b = self.solver.F1.domain
        span_a, span_b = self.solver.F2.domain
        wall_theta = (2 * np.arange(nwall) + 1) * np.pi / (2 * nwall)
        wall_mesh = 0.5 * (wall_a + wall_b) + 0.5 * (wall_b - wall_a) * np.cos(wall_theta)
        stream_k = 2.0 * np.pi * np.fft.fftfreq(
            nstream,
            d=(stream_b - stream_a) / nstream,
        )
        physical_nspan = 2 * (nspan_r2c - 1)
        span_k = 2.0 * np.pi * np.fft.rfftfreq(
            physical_nspan,
            d=(span_b - span_a) / physical_nspan,
        )
        wall_ds = f.create_dataset("geometry/wall_quadrature", shape=wall_mesh.shape, dtype=np.float64)
        stream_ds = f.create_dataset("geometry/k_stream", shape=stream_k.shape, dtype=np.float64)
        span_ds = f.create_dataset("geometry/k_span_r2c", shape=span_k.shape, dtype=np.float64)
        if self.comm.rank == 0:
            wall_ds[:] = wall_mesh
            stream_ds[:] = stream_k
            span_ds[:] = span_k

        starts, stops = _slice_bounds(self.local_slice)
        gathered_starts = self.comm.gather(starts, root=0)
        gathered_stops = self.comm.gather(stops, root=0)
        start_ds = f.create_dataset("mpi/local_slice_start", shape=(self.comm.size, 3), dtype=np.int64)
        stop_ds = f.create_dataset("mpi/local_slice_stop", shape=(self.comm.size, 3), dtype=np.int64)
        if self.comm.rank == 0:
            start_ds[:] = np.asarray(gathered_starts)
            stop_ds[:] = np.asarray(gathered_stops)

        attrs = {
            "schema_version": self.schema_version,
            "valid_samples": 0,
            "first_tstep": int(first_tstep),
            "last_tstep": -1,
            "sample_every_steps": self.every,
            "dns_dt": self.dt,
            "sample_dt": self.every * self.dt,
            "global_shape_spectral": self.global_shape,
            "component_order_physical": "streamwise,spanwise,wallnormal",
            "state_variables": "u_wall_hat,eta_wall_hat,u_stream_zero_mode,u_span_zero_mode",
            "basis_u_wall": "TB:biharmonic-wall,complex-Fourier,real-to-complex-Fourier",
            "basis_eta_wall": "TD:Dirichlet-wall,complex-Fourier,real-to-complex-Fourier",
            "fft_layout": "full streamwise complex spectrum; nonnegative spanwise R2C half-spectrum",
            "precision": "complex128 state; float64 zero modes and time",
            "compression": self.compression,
            "gzip_level": self.gzip_level if self.compression == "gzip" else -1,
            "mpi_size": self.comm.size,
            "complete": False,
            "run_completed": False,
        }
        attrs.update(self.run_metadata)
        for key, value in attrs.items():
            f.attrs[key] = value
        f.flush()
        self.comm.Barrier()

        self.file = f
        self.partial_path = partial_path
        self.final_path = final_path
        self.sample_index = 0
        self.first_tstep = int(first_tstep)
        self.last_tstep = -1

    def maybe_write(self, t: float, tstep: int) -> bool:
        if tstep % self.every != 0:
            return False

        local_nonfinite = int(
            np.size(self.u_wall_hat) - np.count_nonzero(np.isfinite(self.u_wall_hat))
            + np.size(self.eta_wall_hat) - np.count_nonzero(np.isfinite(self.eta_wall_hat))
        )
        global_nonfinite = int(self.comm.allreduce(local_nonfinite))
        zero_mode_nonfinite = 0
        if self.comm.rank == 0:
            zero_modes = (
                np.asarray(self.solver.u_[1, :, 0, 0].real),
                np.asarray(self.solver.u_[2, :, 0, 0].real),
            )
            zero_mode_nonfinite = int(sum(
                np.size(values) - np.count_nonzero(np.isfinite(values))
                for values in zero_modes
            ))
        zero_mode_nonfinite = int(self.comm.bcast(zero_mode_nonfinite, root=0))
        if global_nonfinite or zero_mode_nonfinite or not np.isfinite(t):
            raise FloatingPointError(
                "refusing to write a non-finite MKM state sample at "
                f"tstep={tstep}, t={t:.12g}: distributed={global_nonfinite}, "
                f"zero_modes={zero_mode_nonfinite}"
            )

        if self.file is None:
            self._open_shard(tstep)
        if self.sample_index >= self.shard_samples:
            self._close_shard(full=True, run_completed=True)
            self._open_shard(tstep)

        assert self.file is not None
        index = self.sample_index
        target = (index,) + self.local_slice
        u_wall_ds = self.file["state/u_wall_hat"]
        eta_ds = self.file["state/eta_wall_hat"]
        if hasattr(u_wall_ds, "collective"):
            with u_wall_ds.collective:
                u_wall_ds[target] = np.asarray(self.u_wall_hat)
            with eta_ds.collective:
                eta_ds[target] = np.asarray(self.eta_wall_hat)
        else:
            u_wall_ds[target] = np.asarray(self.u_wall_hat)
            eta_ds[target] = np.asarray(self.eta_wall_hat)

        if self.comm.rank == 0:
            self.file["sampling/t"][index] = float(t)
            self.file["sampling/tstep"][index] = int(tstep)
            self.file["state/u_stream_zero_mode"][index] = np.asarray(
                self.solver.u_[1, :, 0, 0].real,
                dtype=np.float64,
            )
            self.file["state/u_span_zero_mode"][index] = np.asarray(
                self.solver.u_[2, :, 0, 0].real,
                dtype=np.float64,
            )

        self.sample_index += 1
        self.last_tstep = int(tstep)
        self.file.attrs["valid_samples"] = self.sample_index
        self.file.attrs["last_tstep"] = self.last_tstep
        if self.sample_index == self.shard_samples:
            self._close_shard(full=True, run_completed=True)
        return True

    def _close_shard(self, full: bool, run_completed: bool) -> None:
        if self.file is None:
            return
        assert self.partial_path is not None
        assert self.final_path is not None

        self.file.attrs["valid_samples"] = self.sample_index
        self.file.attrs["last_tstep"] = self.last_tstep
        self.file.attrs["complete"] = bool(full or run_completed)
        self.file.attrs["run_completed"] = bool(run_completed)
        self.file.flush()
        self.comm.Barrier()
        self.file.close()
        self.comm.Barrier()

        final_path = self.final_path
        if full or run_completed:
            if self.comm.rank == 0:
                os.replace(self.partial_path, final_path)
            self.comm.Barrier()
            recorded_path = final_path
        else:
            recorded_path = self.partial_path

        closed = ClosedShard(
            path=recorded_path,
            samples=self.sample_index,
            first_tstep=self.first_tstep,
            last_tstep=self.last_tstep,
            full=bool(full),
            run_completed=bool(run_completed),
        )
        self.closed_shards.append(closed)
        if self.comm.rank == 0:
            print(
                "STATE_SHARD_CLOSED "
                f"path={recorded_path} samples={closed.samples} "
                f"first_tstep={closed.first_tstep} last_tstep={closed.last_tstep} "
                f"full={int(closed.full)} run_completed={int(closed.run_completed)}",
                flush=True,
            )

        self.file = None
        self.partial_path = None
        self.final_path = None
        self.sample_index = 0
        self.first_tstep = -1
        self.last_tstep = -1

    def close(self, run_completed: bool) -> list[ClosedShard]:
        if self.file is not None:
            self._close_shard(
                full=self.sample_index == self.shard_samples,
                run_completed=run_completed,
            )
        return list(self.closed_shards)
