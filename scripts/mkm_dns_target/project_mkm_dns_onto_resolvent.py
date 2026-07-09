#!/usr/bin/env python
"""Project selected-mode DNS CSD onto stored channel-resolvent response modes."""

from __future__ import annotations

import argparse
from pathlib import Path

import h5py
import numpy as np

from mkm_channel_resolvent_utils import chebyshev_gauss_physical_weights, velocity_energy_weight


PROJECTION_FORMULA = (
    "For Wq-orthonormal response modes Psi, C = Psi^* Wq Sqq Wq Psi, "
    "E_total = trace(Wq Sqq), energy_fraction_j = real(C_jj)/E_total, and "
    "cumulative_energy_fraction_r = real(trace(C[:r,:r]))/E_total."
)
WEIGHTED_FROBENIUS_FORMULA = (
    "rank-r CSD reconstruction S_r = Psi_r C_r Psi_r^*, with relative error "
    "||Wq^(1/2)(Sqq-S_r)Wq^(1/2)||_F / ||Wq^(1/2)Sqq Wq^(1/2)||_F."
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--resolvent-h5", required=True, help="Single-mode resolvent HDF5 file.")
    parser.add_argument("--csd-h5", required=True, help="Selected-mode DNS modal CSD HDF5 file.")
    parser.add_argument("--output", required=True, help="Output projection HDF5 file.")
    parser.add_argument("--max-rank", type=int, help="Maximum number of stored response modes to use.")
    parser.add_argument("--frequency-tolerance", type=float, default=1e-10)
    parser.add_argument("--mode-tolerance", type=float, default=1e-10)
    parser.add_argument("--make-figure", help="Optional compact PDF of DNS energy fractions.")
    parser.add_argument("--overwrite", action="store_true", help="Replace an existing output file.")
    return parser.parse_args()


def _scalar_float(dataset: h5py.Dataset) -> float:
    return float(np.asarray(dataset[()]))


def _read_single_resolvent_mode(f: h5py.File) -> tuple[np.ndarray, float, float]:
    mode_index = np.asarray(f["mode/index"][:], dtype=np.int32)
    if mode_index.shape != (2,):
        raise ValueError(
            "this projector currently supports the single-mode resolvent layout "
            "with mode/index shape (2,)"
        )
    return mode_index, _scalar_float(f["mode/kappa"]), _scalar_float(f["mode/lambda"])


def match_csd_mode(
    resolvent_mode_index: np.ndarray,
    kappa: float,
    lambda_: float,
    csd_mode_index: np.ndarray,
    csd_k_stream: np.ndarray,
    csd_k_span: np.ndarray,
    tolerance: float,
) -> tuple[int, float]:
    """Return the CSD row matching the resolvent mode."""

    mode_errors = np.maximum(np.abs(csd_k_stream - kappa), np.abs(csd_k_span - lambda_))
    candidates = np.nonzero(mode_errors <= tolerance)[0]
    if candidates.size:
        selected = int(candidates[np.argmin(mode_errors[candidates])])
        return selected, float(mode_errors[selected])

    index_matches = np.nonzero(np.all(csd_mode_index == resolvent_mode_index[None, :], axis=1))[0]
    if index_matches.size:
        selected = int(index_matches[0])
        mode_error = float(mode_errors[selected])
        if mode_error > tolerance:
            raise ValueError(
                "CSD mode index matches the resolvent mode, but the stored "
                f"wavenumbers differ by {mode_error:.6e}, exceeding "
                f"--mode-tolerance={tolerance:.6e}"
            )
        return selected, mode_error

    nearest = int(np.argmin(mode_errors))
    raise ValueError(
        "could not match resolvent mode "
        f"index={tuple(int(v) for v in resolvent_mode_index)} "
        f"(kappa={kappa:.12g}, lambda={lambda_:.12g}) to any CSD mode. "
        "Nearest CSD mode is "
        f"row={nearest}, index={tuple(int(v) for v in csd_mode_index[nearest])}, "
        f"k_stream={csd_k_stream[nearest]:.12g}, k_span={csd_k_span[nearest]:.12g}, "
        f"error={mode_errors[nearest]:.6e}, tolerance={tolerance:.6e}."
    )


def match_frequencies(
    resolvent_omega: np.ndarray,
    csd_omega: np.ndarray,
    tolerance: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Return nearest CSD frequency indices and absolute matching errors."""

    indices = np.empty(resolvent_omega.size, dtype=np.int32)
    errors = np.empty(resolvent_omega.size, dtype=float)
    unmatched: list[str] = []
    for idx, value in enumerate(resolvent_omega):
        nearest = int(np.argmin(np.abs(csd_omega - value)))
        error = float(abs(csd_omega[nearest] - value))
        indices[idx] = nearest
        errors[idx] = error
        if error > tolerance:
            unmatched.append(
                f"omega={value:.12g}, nearest={csd_omega[nearest]:.12g}, diff={error:.6e}"
            )
    if unmatched:
        preview = "; ".join(unmatched[:8])
        if len(unmatched) > 8:
            preview += f"; ... ({len(unmatched)} unmatched total)"
        raise ValueError(
            "resolvent frequencies do not match the CSD grid within "
            f"--frequency-tolerance={tolerance:.6e}: {preview}"
        )
    return indices, errors


def response_norms_and_renormalize(
    response_modes: np.ndarray,
    weights_q: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return Wq-normalized response modes plus raw norms and scale factors."""

    norms = np.einsum("ij,i,ij->j", response_modes.conj(), weights_q, response_modes, optimize=True).real
    if np.any(norms <= 0.0):
        bad = np.nonzero(norms <= 0.0)[0]
        raise ValueError(f"nonpositive response-mode energy norm for columns {bad.tolist()}")
    renormalization = 1.0 / np.sqrt(norms)
    return response_modes * renormalization[None, :], norms, renormalization


def weighted_energy_trace(Sqq: np.ndarray, weights_q: np.ndarray) -> float:
    return float(np.sum(weights_q * np.diagonal(Sqq).real))


def weighted_frobenius_relative_errors(
    Sqq: np.ndarray,
    response_modes: np.ndarray,
    modal_coefficients: np.ndarray,
    weights_q: np.ndarray,
) -> np.ndarray:
    sqrt_weights = np.sqrt(weights_q)
    weighted_sqq = sqrt_weights[:, None] * Sqq * sqrt_weights[None, :]
    denominator = max(float(np.linalg.norm(weighted_sqq)), 1e-300)
    errors = np.empty(response_modes.shape[1], dtype=float)
    for rank in range(1, response_modes.shape[1] + 1):
        psi = response_modes[:, :rank]
        coeff = modal_coefficients[:rank, :rank]
        reconstructed = psi @ coeff @ psi.conj().T
        weighted_diff = sqrt_weights[:, None] * (Sqq - reconstructed) * sqrt_weights[None, :]
        errors[rank - 1] = float(np.linalg.norm(weighted_diff) / denominator)
    return errors


def project_single_frequency(
    Sqq: np.ndarray,
    response_modes: np.ndarray,
    weights_q: np.ndarray,
) -> tuple[float, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    normalized_modes, raw_norms, renormalization = response_norms_and_renormalize(response_modes, weights_q)
    Wpsi = weights_q[:, None] * normalized_modes
    coefficients = Wpsi.conj().T @ Sqq @ Wpsi
    coefficients = 0.5 * (coefficients + coefficients.conj().T)
    total_energy = weighted_energy_trace(Sqq, weights_q)

    energy_fraction = np.full(normalized_modes.shape[1], np.nan, dtype=float)
    cumulative_fraction = np.full_like(energy_fraction, np.nan)
    if total_energy > 0.0:
        modal_energy = np.diagonal(coefficients).real
        energy_fraction = modal_energy / total_energy
        cumulative_fraction = np.cumsum(modal_energy) / total_energy

    fro_errors = weighted_frobenius_relative_errors(Sqq, normalized_modes, coefficients, weights_q)
    return total_energy, energy_fraction, cumulative_fraction, coefficients, raw_norms, renormalization, fro_errors


def make_energy_fraction_figure(
    path: Path,
    omega: np.ndarray,
    energy_fraction: np.ndarray,
    cumulative_fraction: np.ndarray,
) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    path.parent.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.0), constrained_layout=True)
    ranks = np.arange(1, cumulative_fraction.shape[1] + 1)

    axes[0].plot(omega, energy_fraction[:, 0], marker="o", linewidth=1.4)
    axes[0].set_xlabel("omega")
    axes[0].set_ylabel("rank-1 fraction")
    axes[0].grid(True, color="0.9")

    for rank in ranks:
        axes[1].plot(omega, cumulative_fraction[:, rank - 1], marker="o", linewidth=1.1, label=f"r={rank}")
    axes[1].set_xlabel("omega")
    axes[1].set_ylabel("cumulative fraction")
    axes[1].set_ylim(bottom=0.0)
    axes[1].grid(True, color="0.9")
    axes[1].legend(frameon=False, fontsize=8)

    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def project_dns_onto_resolvent(
    resolvent_h5: str | Path,
    csd_h5: str | Path,
    output: str | Path,
    *,
    max_rank: int | None = None,
    frequency_tolerance: float = 1e-10,
    mode_tolerance: float = 1e-10,
    make_figure: str | Path | None = None,
    overwrite: bool = False,
) -> dict[str, object]:
    resolvent_path = Path(resolvent_h5).expanduser().resolve()
    csd_path = Path(csd_h5).expanduser().resolve()
    output_path = Path(output).expanduser().resolve()
    figure_path = Path(make_figure).expanduser().resolve() if make_figure else None

    if output_path.exists() and not overwrite:
        raise FileExistsError(f"{output_path} exists; pass --overwrite to replace it")
    if max_rank is not None and max_rank <= 0:
        raise ValueError("--max-rank must be positive")

    with h5py.File(resolvent_path, "r") as f_resolvent, h5py.File(csd_path, "r") as f_csd:
        z_resolvent = f_resolvent["geometry/z_wall"][:]
        z_csd = f_csd["geometry/z_wall"][:]
        if z_resolvent.shape != z_csd.shape or not np.allclose(z_resolvent, z_csd):
            raise ValueError("resolvent and CSD wall-normal grids do not match")

        mode_index, kappa, lambda_ = _read_single_resolvent_mode(f_resolvent)
        csd_mode_index = np.asarray(f_csd["mode/index"][:], dtype=np.int32)
        csd_k_stream = np.asarray(f_csd["mode/k_stream"][:], dtype=float)
        csd_k_span = np.asarray(f_csd["mode/k_span"][:], dtype=float)
        csd_mode_row, mode_match_error = match_csd_mode(
            mode_index,
            kappa,
            lambda_,
            csd_mode_index,
            csd_k_stream,
            csd_k_span,
            mode_tolerance,
        )

        resolvent_omega = np.asarray(f_resolvent["frequencies/omega"][:], dtype=float)
        csd_omega_grid = np.asarray(f_csd["frequencies/omega"][:], dtype=float)
        csd_frequency_indices, frequency_match_error = match_frequencies(
            resolvent_omega,
            csd_omega_grid,
            frequency_tolerance,
        )
        matched_csd_omega = csd_omega_grid[csd_frequency_indices]

        response_modes_all = f_resolvent["resolvent/response_modes"][:]
        if response_modes_all.ndim != 3:
            raise ValueError("expected resolvent/response_modes shape (omega, singular, modal_dim)")
        n_resolvent_omega, n_stored_modes, modal_dim = response_modes_all.shape
        if n_resolvent_omega != resolvent_omega.size:
            raise ValueError("resolvent response-mode omega axis does not match frequencies/omega")
        if modal_dim != 3 * z_resolvent.size:
            raise ValueError("resolvent modal dimension does not match geometry/z_wall")
        if f_csd["csd/Sqq"].shape[-2:] != (modal_dim, modal_dim):
            raise ValueError("CSD modal dimension does not match resolvent response modes")

        n_rank = n_stored_modes if max_rank is None else min(int(max_rank), n_stored_modes)
        weights_z = chebyshev_gauss_physical_weights(z_resolvent)
        weights_q = velocity_energy_weight(weights_z, as_matrix=False)

        energy_total = np.empty(resolvent_omega.size, dtype=float)
        energy_fraction = np.empty((resolvent_omega.size, n_rank), dtype=float)
        cumulative_fraction = np.empty_like(energy_fraction)
        modal_coefficients = np.empty((resolvent_omega.size, n_rank, n_rank), dtype=np.complex128)
        response_energy_norm = np.empty((resolvent_omega.size, n_rank), dtype=float)
        response_renormalization = np.empty_like(response_energy_norm)
        weighted_fro_error = np.empty_like(response_energy_norm)

        for omega_index, csd_frequency_index in enumerate(csd_frequency_indices):
            Sqq = f_csd["csd/Sqq"][csd_mode_row, int(csd_frequency_index)]
            response_modes = response_modes_all[omega_index, :n_rank, :].T
            (
                energy_total[omega_index],
                energy_fraction[omega_index],
                cumulative_fraction[omega_index],
                modal_coefficients[omega_index],
                response_energy_norm[omega_index],
                response_renormalization[omega_index],
                weighted_fro_error[omega_index],
            ) = project_single_frequency(Sqq, response_modes, weights_q)

    max_response_norm_error = float(np.max(np.abs(response_energy_norm - 1.0)))
    negative_fraction_count = int(np.count_nonzero(energy_fraction < -1e-12))
    zero_or_negative_total_energy_count = int(np.count_nonzero(energy_total <= 0.0))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.exists():
        output_path.unlink()
    with h5py.File(output_path, "w") as f:
        f.attrs["description"] = "Projection of DNS modal CSD onto MKM channel-resolvent response modes."
        f.attrs["source_resolvent_h5"] = str(resolvent_path)
        f.attrs["source_csd_h5"] = str(csd_path)
        f.attrs["projection_formula"] = PROJECTION_FORMULA
        f.attrs["weighted_frobenius_formula"] = WEIGHTED_FROBENIUS_FORMULA
        f.attrs["component_order_level_major"] = "[streamwise, spanwise, wallnormal]"
        f.attrs["response_modes_renormalized_before_projection"] = True
        f.attrs["requested_max_rank"] = -1 if max_rank is None else int(max_rank)
        f.attrs["stored_max_rank"] = int(n_rank)
        f.attrs["matched_csd_mode_row"] = int(csd_mode_row)

        f.create_dataset("geometry/z_wall", data=z_resolvent)
        f.create_dataset("mode/index", data=mode_index)
        f.create_dataset("mode/k_stream", data=kappa)
        f.create_dataset("mode/k_span", data=lambda_)
        f.create_dataset("frequencies/resolvent_omega", data=resolvent_omega)
        f.create_dataset("frequencies/csd_omega", data=matched_csd_omega)
        f.create_dataset("frequencies/csd_index", data=csd_frequency_indices)

        ds = f.create_dataset("projection/energy_total", data=energy_total)
        ds.attrs["axes"] = "omega"
        ds.attrs["definition"] = "real(trace(Wq*Sqq)) for the matched DNS CSD"
        ds = f.create_dataset("projection/energy_fraction", data=energy_fraction)
        ds.attrs["axes"] = "omega,response_mode"
        ds.attrs["definition"] = "real(diag(Psi^* Wq Sqq Wq Psi))/energy_total"
        ds = f.create_dataset("projection/cumulative_energy_fraction", data=cumulative_fraction)
        ds.attrs["axes"] = "omega,rank"
        ds.attrs["definition"] = "cumulative sum of modal captured energies divided by energy_total"
        ds = f.create_dataset("projection/modal_coefficients", data=modal_coefficients)
        ds.attrs["axes"] = "omega,response_mode,response_mode"
        ds.attrs["definition"] = "Psi^* Wq Sqq Wq Psi after response-mode renormalization"
        ds = f.create_dataset("projection/response_energy_norm", data=response_energy_norm)
        ds.attrs["axes"] = "omega,response_mode"
        ds.attrs["definition"] = "raw response-mode q^*Wq q before renormalization"
        ds = f.create_dataset("projection/response_renormalization", data=response_renormalization)
        ds.attrs["axes"] = "omega,response_mode"
        ds.attrs["definition"] = "multiplicative scale applied to each response mode before projection"
        ds = f.create_dataset("projection/weighted_frobenius_relative_error", data=weighted_fro_error)
        ds.attrs["axes"] = "omega,rank"

        f.create_dataset("diagnostics/frequency_match_error", data=frequency_match_error)
        f.create_dataset("diagnostics/mode_match_error", data=mode_match_error)
        f.create_dataset("diagnostics/max_response_energy_norm_error", data=max_response_norm_error)
        f.create_dataset("diagnostics/negative_fraction_count", data=negative_fraction_count)
        f.create_dataset("diagnostics/zero_or_negative_total_energy_count", data=zero_or_negative_total_energy_count)

    if figure_path is not None:
        make_energy_fraction_figure(figure_path, resolvent_omega, energy_fraction, cumulative_fraction)

    return {
        "output": str(output_path),
        "figure": str(figure_path) if figure_path is not None else None,
        "mode_index": tuple(int(v) for v in mode_index),
        "kappa": float(kappa),
        "lambda": float(lambda_),
        "matched_csd_mode_row": int(csd_mode_row),
        "n_omega": int(resolvent_omega.size),
        "max_rank": int(n_rank),
        "max_frequency_match_error": float(np.max(frequency_match_error)),
        "mode_match_error": float(mode_match_error),
        "max_response_energy_norm_error": max_response_norm_error,
        "negative_fraction_count": negative_fraction_count,
        "zero_or_negative_total_energy_count": zero_or_negative_total_energy_count,
        "leading_energy_fraction": energy_fraction[:, 0].copy(),
        "final_cumulative_energy_fraction": cumulative_fraction[:, -1].copy(),
    }


def main() -> int:
    args = parse_args()
    result = project_dns_onto_resolvent(
        resolvent_h5=args.resolvent_h5,
        csd_h5=args.csd_h5,
        output=args.output,
        max_rank=args.max_rank,
        frequency_tolerance=args.frequency_tolerance,
        mode_tolerance=args.mode_tolerance,
        make_figure=args.make_figure,
        overwrite=args.overwrite,
    )
    print(f"wrote={result['output']}")
    if result["figure"] is not None:
        print(f"wrote_figure={result['figure']}")
    print(
        "mode="
        f"{result['mode_index']} "
        f"kappa={result['kappa']:.12g} lambda={result['lambda']:.12g} "
        f"matched_csd_mode_row={result['matched_csd_mode_row']}"
    )
    print(f"n_omega={result['n_omega']} max_rank={result['max_rank']}")
    print(f"max_frequency_match_error={result['max_frequency_match_error']:.6e}")
    print(f"mode_match_error={result['mode_match_error']:.6e}")
    print(f"max_response_energy_norm_error={result['max_response_energy_norm_error']:.6e}")
    print(f"negative_fraction_count={result['negative_fraction_count']}")
    print(f"zero_or_negative_total_energy_count={result['zero_or_negative_total_energy_count']}")
    print(f"leading_energy_fraction={result['leading_energy_fraction']}")
    print(f"final_cumulative_energy_fraction={result['final_cumulative_energy_fraction']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
