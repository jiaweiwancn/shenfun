"""Thin, explicit driver around spectralDNS's dealiased NS operator."""

from __future__ import annotations

from dataclasses import dataclass
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

    def validate(self) -> None:
        if self.n < 8 or self.n % 2:
            raise ValueError("n must be an even integer of at least 8")
        if self.length_cm <= 0.0 or self.viscosity_cm2_s <= 0.0 or self.dt_s <= 0.0:
            raise ValueError("length, viscosity, and dt must be positive")
        if self.threads < 1:
            raise ValueError("threads must be positive")
        if self.decomposition not in {"pencil", "slab"}:
            raise ValueError("decomposition must be 'pencil' or 'slab'")

    @property
    def shape(self) -> tuple[int, int, int]:
        return (self.n, self.n, self.n)

    @property
    def lengths(self) -> tuple[float, float, float]:
        return (self.length_cm, self.length_cm, self.length_cm)

    @property
    def delta_k_cm1(self) -> float:
        return 2.0 * np.pi / self.length_cm


def create_ns_context(settings: DNSParameters) -> tuple[Any, Any]:
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


def create_rk4_stepper(solver: Any, context: Any) -> Callable[[], tuple[Any, float, float]]:
    """Return spectralDNS's classical RK4 stepper for the supplied context."""

    return solver.getintegrator(context.dU, context.u, solver, context)


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
