"""Dealiased Navier--Stokes backends for the HIT calculation.

The original workstation path uses :mod:`spectralDNS`.  The validated CentOS
environment intentionally contains only Shenfun, so this module also provides
the same rotational-form, Leray-projected RK4 operator directly with Shenfun.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import SimpleNamespace
from typing import Any, Callable

import numpy as np

from reference_data import NU_CM2_S


@dataclass(frozen=True)
class DNSParameters:
    """Numerical parameters shared by pilot and production calculations."""

    n: int = 384
    length_cm: float = 10.0 * np.pi
    viscosity_cm2_s: float = NU_CM2_S
    dt_s: float = 1.0e-4
    threads: int = 1
    decomposition: str = "pencil"
    planner_effort: str = "FFTW_MEASURE"
    backend: str = "spectraldns"

    def validate(self) -> None:
        if self.n < 8 or self.n % 2:
            raise ValueError("n must be an even integer of at least 8")
        if self.length_cm <= 0.0 or self.viscosity_cm2_s <= 0.0 or self.dt_s <= 0.0:
            raise ValueError("length, viscosity, and dt must be positive")
        if self.threads < 1:
            raise ValueError("threads must be positive")
        if self.decomposition not in {"pencil", "slab"}:
            raise ValueError("decomposition must be 'pencil' or 'slab'")
        if self.backend not in {"spectraldns", "shenfun"}:
            raise ValueError("backend must be 'spectraldns' or 'shenfun'")

    @property
    def shape(self) -> tuple[int, int, int]:
        return (self.n, self.n, self.n)

    @property
    def lengths(self) -> tuple[float, float, float]:
        return (self.length_cm, self.length_cm, self.length_cm)

    @property
    def delta_k_cm1(self) -> float:
        return 2.0 * np.pi / self.length_cm


class _Context(dict):
    """Dictionary with attribute access, compatible with spectralDNS contexts."""

    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__


class _ShenfunNSSolver:
    """Minimal solver interface used by the common diagnostics and RK4 driver."""

    def __init__(self, settings: DNSParameters) -> None:
        self.params = SimpleNamespace(
            nu=float(settings.viscosity_cm2_s),
            dt=float(settings.dt_s),
            t=0.0,
            tstep=0,
        )

    @staticmethod
    def ComputeRHS(
        rhs: Any,
        u_hat: Any,
        _solver: Any,
        **context: Any,
    ) -> Any:
        """Return ``P(u x curl(u)) - nu*k^2*u`` on the base grid."""

        k = context["K"]
        curl_hat = context["curl_hat"]
        curl_hat[0] = 1j * (k[1] * u_hat[2] - k[2] * u_hat[1])
        curl_hat[1] = 1j * (k[2] * u_hat[0] - k[0] * u_hat[2])
        curl_hat[2] = 1j * (k[0] * u_hat[1] - k[1] * u_hat[0])

        context["VTp"].backward(u_hat, context["u_dealias"])
        context["VTp"].backward(curl_hat, context["curl_dealias"])
        context["cross_dealias"][...] = np.cross(
            context["u_dealias"], context["curl_dealias"], axis=0
        )
        context["VTp"].forward(context["cross_dealias"], rhs)
        if context["mask"] is not None:
            rhs.mask_nyquist(context["mask"])

        pressure = context["P_hat"]
        pressure[...] = np.sum(rhs * context["K_over_K2"], axis=0)
        for component in range(3):
            rhs[component] -= pressure * k[component]
        rhs -= float(_solver.params.nu) * context["K2"] * u_hat
        return rhs


def _create_spectraldns_context(settings: DNSParameters) -> tuple[Any, Any]:
    """Create the spectralDNS rotational-form, 3/2-dealiased NS context."""

    settings.validate()
    from spectralDNS import config, get_solver

    parse_args = [
        "--precision",
        "double",
        "--dealias",
        "3/2-rule",
        "--decomposition",
        settings.decomposition,
        "--threads",
        str(settings.threads),
        "--dt",
        repr(settings.dt_s),
        "--T",
        repr(settings.dt_s),
        "--nu",
        repr(settings.viscosity_cm2_s),
        "--convection",
        "Vortex",
        "--integrator",
        "RK4",
        "--no-verbose",
        "NS",
    ]
    solver = get_solver(parse_args=parse_args)
    # spectralDNS's CLI accepts powers of two through M.  Params explicitly
    # supports N, which also permits the approved 384^3 production mesh.
    config.params.N = settings.shape
    config.params.L = settings.lengths
    config.params.planner_effort["fft"] = settings.planner_effort
    config.params.t = 0.0
    config.params.tstep = 0
    context = solver.get_context()
    solver.conv = solver.getConvection("Vortex")
    return solver, context


def _create_shenfun_context(settings: DNSParameters) -> tuple[Any, _Context]:
    """Create the equivalent operator using only the public Shenfun API."""

    from mpi4py import MPI
    from shenfun import Array, Function, FunctionSpace, TensorProductSpace, VectorSpace

    bases = (
        FunctionSpace(settings.n, "F", dtype="D", domain=(0.0, settings.length_cm)),
        FunctionSpace(settings.n, "F", dtype="D", domain=(0.0, settings.length_cm)),
        FunctionSpace(settings.n, "F", dtype="d", domain=(0.0, settings.length_cm)),
    )
    transform_options = {
        "threads": settings.threads,
        "planner_effort": settings.planner_effort,
    }
    scalar_space = TensorProductSpace(
        MPI.COMM_WORLD,
        bases,
        dtype=float,
        slab=settings.decomposition == "slab",
        collapse_fourier=False,
        **transform_options,
    )
    vector_space = VectorSpace(scalar_space)
    padded_scalar_space = scalar_space.get_dealiased(padding_factor=1.5)
    padded_vector_space = VectorSpace(padded_scalar_space)

    wavenumbers = scalar_space.local_wavenumbers(scaled=True)
    k_squared = np.zeros(scalar_space.shape(True), dtype=float)
    for component in range(3):
        wavenumbers[component] = wavenumbers[component].astype(float)
        k_squared += wavenumbers[component] ** 2
    k_over_k_squared = np.zeros(vector_space.shape(True), dtype=float)
    denominator = np.where(k_squared == 0.0, 1.0, k_squared)
    for component in range(3):
        k_over_k_squared[component] = wavenumbers[component] / denominator

    context = _Context(
        T=scalar_space,
        VT=vector_space,
        Tp=padded_scalar_space,
        VTp=padded_vector_space,
        U=Array(vector_space),
        U_hat=Function(vector_space),
        dU=Function(vector_space),
        P_hat=Function(scalar_space),
        curl_hat=Function(vector_space),
        u_dealias=Array(padded_vector_space),
        curl_dealias=Array(padded_vector_space),
        cross_dealias=Array(padded_vector_space),
        K=wavenumbers,
        K2=k_squared,
        K_over_K2=k_over_k_squared,
        mask=scalar_space.get_mask_nyquist(),
    )
    return _ShenfunNSSolver(settings), context


def create_ns_context(settings: DNSParameters) -> tuple[Any, Any]:
    """Create the selected rotational-form, 3/2-dealiased NS context."""

    settings.validate()
    if settings.backend == "spectraldns":
        return _create_spectraldns_context(settings)
    return _create_shenfun_context(settings)


def create_rk4_stepper(solver: Any, context: Any) -> Callable[[], tuple[Any, float, float]]:
    """Return a classical RK4 stepper for the supplied context."""

    if hasattr(solver, "getintegrator"):
        return solver.getintegrator(context.dU, context.u, solver, context)

    u_hat = context.U_hat
    base = u_hat.copy()
    result = u_hat.copy()
    weights = (1.0 / 6.0, 1.0 / 3.0, 1.0 / 3.0, 1.0 / 6.0)
    stages = (0.5, 0.5, 1.0)

    def step() -> tuple[Any, float, float]:
        dt = float(solver.params.dt)
        base[...] = u_hat
        result[...] = u_hat
        for rk in range(4):
            rhs = solver.ComputeRHS(context.dU, u_hat, solver, **context)
            if rk < 3:
                u_hat[...] = base + stages[rk] * dt * rhs
            result[...] += weights[rk] * dt * rhs
        u_hat[...] = result
        return u_hat, dt, dt

    return step


def advance_to_time(
    solver: Any,
    context: Any,
    stepper: Callable[[], tuple[Any, float, float]],
    target_time_s: float,
    nominal_dt_s: float,
    after_step: Callable[[Any, Any], None] | None = None,
) -> None:
    """Advance with fixed nominal dt and a shortened step at the target."""

    params = solver.params
    target = float(target_time_s)
    tolerance = 32.0 * np.finfo(float).eps * max(1.0, abs(target))
    if target < params.t - tolerance:
        raise ValueError("target time precedes the current solver time")
    while params.t < target - tolerance:
        params.dt = min(float(nominal_dt_s), target - params.t)
        _u, _next_dt, dt_taken = stepper()
        params.t += float(dt_taken)
        params.tstep += 1
        if after_step is not None:
            after_step(solver, context)
    params.t = target
    params.dt = float(nominal_dt_s)
