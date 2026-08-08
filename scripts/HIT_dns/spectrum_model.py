"""Continuous initial energy spectrum for the Comte-Bellot--Corrsin DNS.

The measured station-42 values are preserved exactly.  A positive PCHIP is
used between measurements, a :math:`k^4` infrared completion is used below the
first measured point, and a Pao-type dissipative completion is used above the
last measured point.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.integrate import quad
from scipy.interpolate import PchipInterpolator

from reference_data import finite_station_values, load_table3_e, load_table4_bulk


@dataclass(frozen=True)
class TailFit:
    """Parameters of ``C k**(-5/3) exp(-beta (k eta)**(4/3))``."""

    beta: float
    coefficient: float
    eta_cm: float
    fit_k_min_cm1: float


class InitialEnergySpectrum:
    """Callable station-42 three-dimensional energy-spectrum model."""

    def __init__(self, tail_fit_k_min_cm1: float = 8.0) -> None:
        self.k_data, self.e_data = finite_station_values(load_table3_e(), 42.0)
        self.k_min = float(self.k_data[0])
        self.k_max = float(self.k_data[-1])
        self._log_interpolant = PchipInterpolator(
            np.log(self.k_data), np.log(self.e_data), extrapolate=False
        )

        bulk = load_table4_bulk()
        station_42 = bulk[np.isclose(bulk["station_tU0_over_M"], 42.0)][0]
        eta = float(station_42["eta_cm"])
        selected = self.k_data >= float(tail_fit_k_min_cm1)
        x = (self.k_data[selected] * eta) ** (4.0 / 3.0)
        y = np.log(self.e_data[selected] * self.k_data[selected] ** (5.0 / 3.0))
        slope, _intercept = np.polyfit(x, y, 1)
        beta = max(float(-slope), np.finfo(float).eps)

        # Preserve the final measured datum exactly; beta carries the fitted
        # decay rate while this coefficient enforces C0 continuity at k_max.
        coefficient = float(
            self.e_data[-1]
            * self.k_max ** (5.0 / 3.0)
            * np.exp(beta * (self.k_max * eta) ** (4.0 / 3.0))
        )
        self.tail = TailFit(beta, coefficient, eta, float(tail_fit_k_min_cm1))

    def __call__(self, k_cm1: np.ndarray | float) -> np.ndarray | float:
        """Evaluate ``E(k)`` in cm3/s2 for nonnegative ``k`` in cm-1."""

        k = np.asarray(k_cm1, dtype=float)
        if np.any(k < 0.0):
            raise ValueError("Energy-spectrum wavenumbers must be nonnegative")

        result = np.zeros_like(k)
        infrared = (k > 0.0) & (k < self.k_min)
        measured = (k >= self.k_min) & (k <= self.k_max)
        tail = k > self.k_max

        result[infrared] = self.e_data[0] * (k[infrared] / self.k_min) ** 4
        result[measured] = np.exp(self._log_interpolant(np.log(k[measured])))
        if np.any(tail):
            kt = k[tail]
            result[tail] = (
                self.tail.coefficient
                * kt ** (-5.0 / 3.0)
                * np.exp(-self.tail.beta * (kt * self.tail.eta_cm) ** (4.0 / 3.0))
            )
        return float(result) if result.ndim == 0 else result

    def longitudinal_spectrum(self, k1_cm1: float) -> float:
        r"""Return the isotropic longitudinal spectrum.

        .. math::

           E_{11}^{(1)}(k_1) = \int_{k_1}^{\infty}
             \frac{E(k)}{k}\left(1-\frac{k_1^2}{k^2}\right)\,dk.
        """

        k1 = float(k1_cm1)
        if k1 < 0.0:
            raise ValueError("Longitudinal wavenumber must be nonnegative")
        lower = max(k1, np.finfo(float).tiny)

        def integrand(k: float) -> float:
            return float(self(k)) / k * (1.0 - (k1 / k) ** 2)

        split_points = [value for value in self.k_data if value > lower]
        bounds = [lower, *split_points, np.inf]
        value = 0.0
        for left, right in zip(bounds[:-1], bounds[1:]):
            value += quad(integrand, left, right, epsabs=1.0e-10, epsrel=1.0e-9)[0]
        return value

    def integral_energy(self) -> float:
        """Return ``integral E(k) dk``, the modeled kinetic energy per mass."""

        bounds = [0.0, *self.k_data.tolist(), np.inf]
        return sum(
            quad(lambda k: float(self(k)), left, right, epsabs=1.0e-10, epsrel=1.0e-9)[0]
            for left, right in zip(bounds[:-1], bounds[1:])
        )


def create_initial_spectrum() -> InitialEnergySpectrum:
    """Construct the approved baseline station-42 spectrum."""

    return InitialEnergySpectrum()
