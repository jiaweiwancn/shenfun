#!/usr/bin/env python
"""Build channel-flow constraint recipes and optional Gtilde tables."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import h5py
import numpy as np


def fd_weights(nodes: np.ndarray, x0: float, deriv: int = 1) -> np.ndarray:
    n = len(nodes)
    powers = np.vstack([(nodes - x0) ** p for p in range(n)])
    rhs = np.zeros(n)
    rhs[deriv] = math.factorial(deriv)
    return np.linalg.solve(powers, rhs)


def derivative_matrix(z: np.ndarray, stencil_width: int) -> np.ndarray:
    n = len(z)
    width = min(stencil_width, n)
    if width < 2:
        raise ValueError("stencil_width must be at least 2")
    D = np.zeros((n, n), dtype=float)
    half = width // 2
    for i in range(n):
        start = min(max(i - half, 0), n - width)
        cols = np.arange(start, start + width)
        D[i, cols] = fd_weights(z[cols], z[i], 1)
    return D


def barycentric_weights(nodes: np.ndarray) -> np.ndarray:
    weights = np.ones(len(nodes), dtype=float)
    for j, xj in enumerate(nodes):
        weights[j] = 1.0 / np.prod(xj - np.delete(nodes, j))
    return weights


def spectral_derivative_matrix(nodes: np.ndarray) -> np.ndarray:
    weights = barycentric_weights(nodes)
    n = len(nodes)
    D = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(n):
            if i != j:
                D[i, j] = weights[j] / (weights[i] * (nodes[i] - nodes[j]))
        D[i, i] = -np.sum(D[i])
    return D


def interpolation_row(nodes: np.ndarray, x: float) -> np.ndarray:
    close = np.where(np.isclose(nodes, x, rtol=0.0, atol=1e-14))[0]
    row = np.zeros(len(nodes), dtype=float)
    if len(close):
        row[close[0]] = 1.0
        return row
    weights = barycentric_weights(nodes)
    terms = weights / (x - nodes)
    return terms / np.sum(terms)


def chebyshev_gauss_nodes(n: int, lower: float, upper: float) -> np.ndarray:
    reference = np.cos(np.pi * (2 * np.arange(n) + 1) / (2 * n))
    midpoint = 0.5 * (lower + upper)
    half_width = 0.5 * (upper - lower)
    return midpoint + half_width * reference


def extraction_matrices(nz: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    E_stream = np.zeros((nz, 3 * nz), dtype=float)
    E_span = np.zeros_like(E_stream)
    E_wall = np.zeros_like(E_stream)
    for a in range(nz):
        E_stream[a, 3 * a] = 1.0
        E_span[a, 3 * a + 1] = 1.0
        E_wall[a, 3 * a + 2] = 1.0
    return E_stream, E_span, E_wall


def compress_constraint(Graw: np.ndarray, rtol: float) -> tuple[np.ndarray, np.ndarray, np.ndarray, int]:
    _, singular_values, Vh = np.linalg.svd(Graw, full_matrices=True)
    rank = int(np.sum(singular_values > rtol * singular_values[0]))
    Gtilde = Vh[:rank, :]
    Nmat = Vh[rank:, :].conj().T
    return singular_values, Gtilde, Nmat, rank


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, help="Output HDF5 file.")
    parser.add_argument("--n", nargs=3, type=int, default=(64, 64, 32), metavar=("NZ", "NX", "NY"))
    parser.add_argument("--wall-domain", nargs=2, type=float, default=(-1.0, 1.0), metavar=("Z0", "Z1"))
    parser.add_argument("--stream-length", type=float, default=2.0 * np.pi)
    parser.add_argument("--span-length", type=float, default=np.pi)
    parser.add_argument("--stencil-width", type=int, default=7)
    parser.add_argument("--constraint-kind", choices=("chebyshev-quadrature-spectral", "uniform-fd"),
                        default="chebyshev-quadrature-spectral",
                        help="Vertical grid and derivative/boundary discretization.")
    parser.add_argument("--svd-rtol", type=float, default=1e-12)
    parser.add_argument("--save-all-gtilde", action="store_true",
                        help="Save dense Gtilde for every horizontal mode.")
    parser.add_argument("--save-all-nullspace", action="store_true",
                        help="When used with --save-all-gtilde, also save Nmat for every mode.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    nz, nx, ny = args.n
    if args.constraint_kind == "uniform-fd":
        z = np.linspace(args.wall_domain[0], args.wall_domain[1], nz)
        D_wall = derivative_matrix(z, args.stencil_width)
        B = np.zeros((2, nz), dtype=float)
        B[0, 0] = 1.0
        B[1, -1] = 1.0
        grid_description = "stored Shenfun uniform wall-normal grid"
        derivative_description = "local polynomial finite-difference first derivative"
        boundary_description = "boundary selector rows at first and last stored levels"
    else:
        z = chebyshev_gauss_nodes(nz, args.wall_domain[0], args.wall_domain[1])
        D_wall = spectral_derivative_matrix(z)
        B = np.vstack((
            interpolation_row(z, args.wall_domain[0]),
            interpolation_row(z, args.wall_domain[1]),
        ))
        grid_description = "Chebyshev-Gauss quadrature wall-normal grid"
        derivative_description = "barycentric spectral nodal first derivative"
        boundary_description = "barycentric endpoint interpolation rows"

    x_stream = np.arange(nx) * args.stream_length / nx
    x_span = np.arange(ny) * args.span_length / ny
    k_stream = 2.0 * np.pi * np.fft.fftfreq(nx, d=args.stream_length / nx)
    k_span = 2.0 * np.pi * np.fft.fftfreq(ny, d=args.span_length / ny)

    E_stream, E_span, E_wall = extraction_matrices(nz)
    G_boundary = np.vstack((B @ E_stream, B @ E_span, B @ E_wall)).astype(complex)

    def raw_constraint(ks: float, kp: float) -> np.ndarray:
        Gdiv = 1j * ks * E_stream + 1j * kp * E_span + D_wall @ E_wall
        return np.vstack((Gdiv, G_boundary))

    ranks = np.zeros((nx, ny), dtype=np.int32)
    nullities = np.zeros((nx, ny), dtype=np.int32)
    min_retained = np.zeros((nx, ny), dtype=float)
    for i, ks in enumerate(k_stream):
        for j, kp in enumerate(k_span):
            singular_values, _, _, rank = compress_constraint(raw_constraint(ks, kp), args.svd_rtol)
            ranks[i, j] = rank
            nullities[i, j] = 3 * nz - rank
            min_retained[i, j] = singular_values[rank - 1]

    output = Path(args.output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        output.unlink()

    with h5py.File(output, "w") as f:
        f.attrs["description"] = f"MKM channel-flow constraint recipe on the {grid_description}."
        f.attrs["constraint_kind"] = args.constraint_kind
        f.attrs["component_order_level_major"] = "[u_streamwise_from_HDF5_u1, u_spanwise_from_HDF5_u2, u_wallnormal_from_HDF5_u0]"
        f.attrs["solver_component_order"] = "[u_wallnormal, u_streamwise, u_spanwise]"
        f.attrs["Gdiv_formula"] = "1j*k_stream*E_stream + 1j*k_span*E_span + D_wall@E_wall"
        f.attrs["boundary_formula"] = "stack(B@E_stream, B@E_span, B@E_wall)"
        f.attrs["D_wall_kind"] = derivative_description
        f.attrs["D_wall_stencil_width"] = args.stencil_width
        f.attrs["B_boundary_kind"] = boundary_description
        f.attrs["svd_relative_tolerance"] = args.svd_rtol
        f.attrs["forward_fft_normalization"] = "np.fft.fft2(u_fluct, axes=(streamwise, spanwise))/(Nx*Ny)"
        f.create_dataset("grid/z_wall", data=z)
        f.create_dataset("grid/x_stream", data=x_stream)
        f.create_dataset("grid/x_span", data=x_span)
        f.create_dataset("wavenumbers/k_stream", data=k_stream)
        f.create_dataset("wavenumbers/k_span", data=k_span)
        f.create_dataset("operators/D_wall", data=D_wall)
        f.create_dataset("operators/B_boundary", data=B)
        f.create_dataset("operators/E_stream", data=E_stream)
        f.create_dataset("operators/E_span", data=E_span)
        f.create_dataset("operators/E_wall", data=E_wall)
        f.create_dataset("mode_audit/rank", data=ranks)
        f.create_dataset("mode_audit/nullity", data=nullities)
        f.create_dataset("mode_audit/min_retained_singular_value", data=min_retained)

        reps = [(0, 0), (1, 0), (0, 1), (1, 1), (nx // 2, 0), (0, ny // 2), (nx // 2, ny // 2)]
        rep_group = f.create_group("representative_modes")
        for i, j in reps:
            singular_values, Gtilde, Nmat, rank = compress_constraint(
                raw_constraint(k_stream[i], k_span[j]), args.svd_rtol)
            group = rep_group.create_group(f"i{i}_j{j}")
            group.attrs["mode_index_stream"] = i
            group.attrs["mode_index_span"] = j
            group.attrs["k_stream"] = k_stream[i]
            group.attrs["k_span"] = k_span[j]
            group.attrs["rank"] = rank
            group.attrs["nullity"] = 3 * nz - rank
            group.attrs["Gtilde_row_orthonormal_error"] = np.linalg.norm(
                Gtilde @ Gtilde.conj().T - np.eye(rank))
            group.attrs["Gtilde_Nmat_error"] = np.linalg.norm(Gtilde @ Nmat)
            group.create_dataset("singular_values", data=singular_values)
            group.create_dataset("Gtilde", data=Gtilde)
            group.create_dataset("Nmat", data=Nmat)

        if args.save_all_gtilde:
            all_group = f.create_group("modes")
            for i, ks in enumerate(k_stream):
                for j, kp in enumerate(k_span):
                    singular_values, Gtilde, Nmat, rank = compress_constraint(
                        raw_constraint(ks, kp), args.svd_rtol)
                    group = all_group.create_group(f"i{i}_j{j}")
                    group.attrs["k_stream"] = ks
                    group.attrs["k_span"] = kp
                    group.attrs["rank"] = rank
                    group.attrs["nullity"] = 3 * nz - rank
                    group.create_dataset("singular_values", data=singular_values)
                    group.create_dataset("Gtilde", data=Gtilde)
                    if args.save_all_nullspace:
                        group.create_dataset("Nmat", data=Nmat)

    rank_counts = {int(r): int((ranks == r).sum()) for r in np.unique(ranks)}
    print(f"wrote={output}")
    print(f"rank_counts={rank_counts}")
    print(f"size_bytes={output.stat().st_size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
