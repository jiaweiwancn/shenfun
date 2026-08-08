"""MPI-aware invariant diagnostics for the HIT spectral field."""

from __future__ import annotations

from typing import Any

import numpy as np
from mpi4py import MPI


def r2c_multiplicity(context: Any, n_last: int) -> np.ndarray:
    """Return Parseval multiplicities for the locally stored r2c modes."""

    spectral_slice = tuple(context.T.local_slice(True))
    last = spectral_slice[-1]
    start = 0 if last.start is None else last.start
    stop = n_last // 2 + 1 if last.stop is None else last.stop
    indices = np.arange(start, stop)
    weight = np.full(indices.shape, 2.0)
    weight[indices == 0] = 1.0
    if n_last % 2 == 0:
        weight[indices == n_last // 2] = 1.0
    return weight.reshape((1,) * (context.K2.ndim - 1) + (-1,))


def _global_sum(value: np.ndarray | float, comm: MPI.Comm) -> float:
    return float(comm.allreduce(float(np.sum(value)), op=MPI.SUM))


def field_invariants(
    context: Any,
    global_shape: tuple[int, int, int],
    comm: MPI.Comm = MPI.COMM_WORLD,
) -> dict[str, float | list[float]]:
    """Compute divergence, energy, component means, and Parseval closure."""

    weight = r2c_multiplicity(context, global_shape[-1])
    component_power = np.abs(context.U_hat) ** 2
    spectral_energy = 0.5 * _global_sum(weight * np.sum(component_power, axis=0), comm)

    context.VT.backward(context.U_hat, context.U)
    point_count = float(np.prod(global_shape))
    physical_energy = 0.5 * _global_sum(np.sum(context.U * context.U, axis=0), comm) / point_count
    component_means = [
        _global_sum(context.U[i], comm) / point_count for i in range(3)
    ]
    component_rms = [
        np.sqrt(_global_sum(context.U[i] ** 2, comm) / point_count) for i in range(3)
    ]

    divergence_hat = sum(context.K[i] * context.U_hat[i] for i in range(3))
    divergence_numerator = _global_sum(weight * np.abs(divergence_hat) ** 2, comm)
    divergence_denominator = _global_sum(
        weight * context.K2 * np.sum(component_power, axis=0), comm
    )
    relative_divergence = np.sqrt(
        divergence_numerator / max(divergence_denominator, np.finfo(float).tiny)
    )
    parseval_relative_error = abs(spectral_energy - physical_energy) / max(
        physical_energy, np.finfo(float).tiny
    )
    local_finite = bool(np.all(np.isfinite(context.U_hat)) and np.all(np.isfinite(context.U)))
    finite = bool(comm.allreduce(local_finite, op=MPI.LAND))
    return {
        "finite": finite,
        "spectral_energy_cm2_s^-2": spectral_energy,
        "physical_energy_cm2_s^-2": physical_energy,
        "parseval_relative_error": parseval_relative_error,
        "relative_spectral_divergence": relative_divergence,
        "component_mean_cm_s": component_means,
        "component_rms_cm_s": component_rms,
    }


def nonlinear_energy_residual(
    solver: Any,
    context: Any,
    global_shape: tuple[int, int, int],
    comm: MPI.Comm = MPI.COMM_WORLD,
) -> float:
    """Return normalized inviscid energy production of one nonlinear RHS."""

    rhs = solver.ComputeRHS(context.dU, context.U_hat, solver, **context)
    inviscid_rhs = rhs + solver.params.nu * context.K2 * context.U_hat
    weight = r2c_multiplicity(context, global_shape[-1])
    local_inner = weight * np.real(
        np.sum(np.conjugate(context.U_hat) * inviscid_rhs, axis=0)
    )
    inner = _global_sum(local_inner, comm)
    velocity_norm2 = _global_sum(
        weight * np.sum(np.abs(context.U_hat) ** 2, axis=0), comm
    )
    rhs_norm2 = _global_sum(weight * np.sum(np.abs(inviscid_rhs) ** 2, axis=0), comm)
    return abs(inner) / max(
        np.sqrt(velocity_norm2 * rhs_norm2), np.finfo(float).tiny
    )


def cfl_number(
    context: Any,
    dt_s: float,
    lengths_cm: tuple[float, float, float],
    global_shape: tuple[int, int, int],
    comm: MPI.Comm = MPI.COMM_WORLD,
) -> float:
    """Return the advective CFL estimate ``dt sum_i max|u_i|/dx_i``."""

    context.VT.backward(context.U_hat, context.U)
    maxima = [comm.allreduce(float(np.max(np.abs(context.U[i]))), op=MPI.MAX) for i in range(3)]
    spacings = np.asarray(lengths_cm) / np.asarray(global_shape)
    return float(dt_s * np.sum(np.asarray(maxima) / spacings))


def energy_spectra(
    context: Any,
    global_shape: tuple[int, int, int],
    lengths_cm: tuple[float, float, float],
    comm: MPI.Comm = MPI.COMM_WORLD,
) -> dict[str, np.ndarray | float]:
    """Return shell-integrated ``E(k)`` and plane-integrated ``E11(k1)``.

    The returned spectra are one-sided and use the cube's fundamental
    wavenumber as their bin width.  Their rectangle-rule integrals close to
    kinetic energy and streamwise component variance, respectively.
    """

    delta_k_axes = 2.0 * np.pi / np.asarray(lengths_cm, dtype=float)
    if not np.allclose(delta_k_axes, delta_k_axes[0]):
        raise ValueError("Current spectrum binning requires a cubic domain")
    delta_k = float(delta_k_axes[0])
    weight = np.broadcast_to(r2c_multiplicity(context, global_shape[-1]), context.K2.shape)
    modal_energy = 0.5 * weight * np.sum(np.abs(context.U_hat) ** 2, axis=0)

    shell_index = np.floor(np.sqrt(context.K2) / delta_k + 0.5).astype(np.int64)
    maximum_shell = int(np.floor(np.sqrt(3.0) * (max(global_shape) // 2) + 0.5))
    local_shell_energy = np.bincount(
        shell_index.ravel(), weights=modal_energy.ravel(), minlength=maximum_shell + 1
    )
    local_shell_modes = np.bincount(
        shell_index.ravel(), weights=weight.ravel(), minlength=maximum_shell + 1
    )
    shell_energy = np.empty_like(local_shell_energy)
    shell_modes = np.empty_like(local_shell_modes)
    comm.Allreduce(local_shell_energy, shell_energy, op=MPI.SUM)
    comm.Allreduce(local_shell_modes, shell_modes, op=MPI.SUM)

    plane_index = np.rint(np.abs(context.K[0]) / delta_k).astype(np.int64)
    plane_index = np.broadcast_to(plane_index, context.K2.shape)
    local_plane_variance = np.bincount(
        plane_index.ravel(),
        weights=(weight * np.abs(context.U_hat[0]) ** 2).ravel(),
        minlength=global_shape[0] // 2 + 1,
    )
    plane_variance = np.empty_like(local_plane_variance)
    comm.Allreduce(local_plane_variance, plane_variance, op=MPI.SUM)

    total_energy = _global_sum(modal_energy, comm)
    component_variance = _global_sum(weight * np.abs(context.U_hat[0]) ** 2, comm)
    e = shell_energy / delta_k
    e11 = plane_variance / delta_k
    return {
        "k_cm^-1": np.arange(shell_energy.size, dtype=float) * delta_k,
        "E_cm3_s^-2": e,
        "shell_mode_multiplicity": shell_modes,
        "k1_cm^-1": np.arange(plane_variance.size, dtype=float) * delta_k,
        "E11_cm3_s^-2": e11,
        "E_integral_cm2_s^-2": float(np.sum(e) * delta_k),
        "kinetic_energy_cm2_s^-2": total_energy,
        "E11_integral_cm2_s^-2": float(np.sum(e11) * delta_k),
        "u1_variance_cm2_s^-2": component_variance,
    }


def turbulence_statistics(
    context: Any,
    viscosity_cm2_s: float,
    global_shape: tuple[int, int, int],
    lengths_cm: tuple[float, float, float],
    comm: MPI.Comm = MPI.COMM_WORLD,
) -> dict[str, float | list[float] | bool]:
    """Return energetic, dissipative, resolution, and invariant statistics."""

    invariants = field_invariants(context, global_shape, comm)
    weight = r2c_multiplicity(context, global_shape[-1])
    dissipation = float(viscosity_cm2_s) * _global_sum(
        weight * context.K2 * np.sum(np.abs(context.U_hat) ** 2, axis=0), comm
    )
    kinetic_energy = float(invariants["spectral_energy_cm2_s^-2"])
    isotropic_component_variance = 2.0 * kinetic_energy / 3.0
    u_rms = np.sqrt(isotropic_component_variance)
    eta = (float(viscosity_cm2_s) ** 3 / dissipation) ** 0.25
    taylor_microscale = np.sqrt(
        15.0 * float(viscosity_cm2_s) * isotropic_component_variance / dissipation
    )
    reynolds_lambda = u_rms * taylor_microscale / float(viscosity_cm2_s)
    nominal_kmax = float(np.min(np.pi * np.asarray(global_shape) / np.asarray(lengths_cm)))
    return {
        **invariants,
        "dissipation_cm2_s^-3": dissipation,
        "isotropic_u_rms_cm_s": u_rms,
        "kolmogorov_length_cm": eta,
        "taylor_microscale_cm": taylor_microscale,
        "reynolds_lambda": reynolds_lambda,
        "nominal_kmax_cm^-1": nominal_kmax,
        "kmax_eta": nominal_kmax * eta,
    }
