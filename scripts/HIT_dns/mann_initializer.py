"""Mann-factorized Gaussian initial condition for decaying isotropic turbulence."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

import numpy as np

from deterministic_random import gaussian_for_local_block
from spectrum_model import InitialEnergySpectrum


def apply_mann_factor(
    white_hat: np.ndarray,
    wavenumbers: tuple[np.ndarray, np.ndarray, np.ndarray] | list[np.ndarray],
    k_squared: np.ndarray,
    spectrum: InitialEnergySpectrum,
    spectral_cell_volume: float,
    physical_point_count: int,
    output: np.ndarray | None = None,
) -> np.ndarray:
    r"""Apply the isotropic Mann factorization to normalized white-noise FFTs.

    ``white_hat`` is the normalized transform of three real, unit-variance
    white-noise fields.  Multiplication by ``sqrt(physical_point_count)`` gives
    unit-variance complex coefficients.  The extra factor ``1j`` makes those
    coefficients anti-Hermitian; multiplication by the odd Mann matrix then
    produces the Hermitian velocity coefficients required for a real field.
    """

    if white_hat.shape[0] != 3:
        raise ValueError("The Mann factor requires three independent noise components")
    result = np.empty_like(white_hat) if output is None else output
    k0, k1, k2 = wavenumbers
    magnitude = np.sqrt(k_squared)
    modeled_energy = np.asarray(spectrum(magnitude))
    amplitude = np.zeros_like(magnitude, dtype=float)
    nonzero = k_squared > 0.0
    amplitude[nonzero] = (
        np.sqrt(modeled_energy[nonzero])
        / (np.sqrt(4.0 * np.pi) * k_squared[nonzero])
        * np.sqrt(float(physical_point_count) * float(spectral_cell_volume))
    )

    result[0] = 1j * amplitude * (k2 * white_hat[1] - k1 * white_hat[2])
    result[1] = 1j * amplitude * (-k2 * white_hat[0] + k0 * white_hat[2])
    result[2] = 1j * amplitude * (k1 * white_hat[0] - k0 * white_hat[1])
    result[:, ~nonzero] = 0.0
    return result


def initialize_mann_velocity(
    context: Any,
    spectrum: InitialEnergySpectrum,
    seed: int,
    global_shape: tuple[int, int, int],
    domain_lengths_cm: tuple[float, float, float],
) -> dict[str, Any]:
    """Populate a spectralDNS NS context with the fixed-seed Mann field."""

    physical_slice = tuple(context.T.local_slice(False))
    for component in range(3):
        context.U[component] = gaussian_for_local_block(
            physical_slice, global_shape, seed, component
        )

    context.VT.forward(context.U, context.U_hat)
    white_hat = context.U_hat.copy()
    spectral_cell_volume = float(
        np.prod([2.0 * np.pi / length for length in domain_lengths_cm])
    )
    apply_mann_factor(
        white_hat,
        context.K,
        context.K2,
        spectrum,
        spectral_cell_volume,
        int(np.prod(global_shape)),
        output=context.U_hat,
    )
    if context.mask is not None:
        context.U_hat.mask_nyquist(context.mask)

    return {
        "method": "Mann isotropic spectral factorization",
        "seed": int(seed),
        "global_shape": list(global_shape),
        "domain_lengths_cm": list(domain_lengths_cm),
        "spectral_cell_volume_cm^-3": spectral_cell_volume,
        "tail_fit": asdict(spectrum.tail),
        "modeled_integral_energy_cm2_s^-2": spectrum.integral_energy(),
    }
