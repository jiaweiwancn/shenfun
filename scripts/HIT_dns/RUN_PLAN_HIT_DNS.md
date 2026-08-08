# Decaying HIT DNS: Comte-Bellot--Corrsin experiment

## Material Passport

- Origin Skill: experiment-agent
- Origin Mode: plan, approved for execution
- Origin Date: 2026-08-08
- Verification Status: UNVERIFIED until the production run and comparison finish
- Version Label: hit_dns_plan_v1

## Objective

Generate a divergence-free, homogeneous isotropic Gaussian velocity field from
the measured three-dimensional spectrum at $tU_0/M=42$, evolve it with an
unforced triply periodic incompressible Navier--Stokes DNS to $tU_0/M=171$,
and compare $E(k,t)$ and $E_{11}^{(1)}(k_1,t)$ with Tables 2 and 3 of
Comte-Bellot & Corrsin (1971).

## Physical mapping

- Grid mesh: $M=5.08$ cm.
- Upstream velocity: $U_0=1000$ cm/s.
- Kinematic viscosity: $\nu=U_0M/34000=0.1494117647$ cm2/s.
- DNS time zero corresponds to $tU_0/M=42$.
- Station 98: DNS elapsed time $(98-42)M/U_0=0.28448$ s.
- Station 171: DNS elapsed time $(171-42)M/U_0=0.65532$ s.

The simulation uses centimetres and seconds throughout, matching the units of
the tabulated spectra.

## Approved baseline configuration

- Domain: periodic cube $[0,10\pi)^3$ cm.
- Base resolution: $384^3$ Fourier grid.
- Dealiasing: 3/2 padding; nonlinear products are evaluated on $576^3$.
- Fundamental wavenumber: $\Delta k=0.2$ cm-1.
- Initial resolution: $k_{max}\eta\simeq38.4(0.029)=1.11$.
- Parallelism: 32 MPI ranks and one thread per rank.
- Equations: unforced incompressible Navier--Stokes equations in rotational
  form, with an algebraic Leray projection.
- Time integration: classical RK4 with a pilot-selected fixed timestep, a CFL
  ceiling of 0.5, and shortened final steps to land exactly on requested output
  stations.
- Initial random field: Mann spectral-representation factorization with a
  fixed seed, Gaussian coefficients, Hermitian reality, zero mean, and no
  post-hoc selection of a favourable realization.

## Spectrum completion

The measured Table 3 values at station 42 are authoritative at their tabulated
wavenumbers. Between them, the implementation uses a positive interpolation in
log-spectrum. The missing ends are completed as follows:

- Below 0.2 cm-1: $E(k)\propto k^4$.
- Above 20 cm-1: a positive dissipative tail fitted to the final measured
  points and checked against the measured $\epsilon$, $\eta$, and $k_K$.

Tail sensitivity is evaluated in the pilot stage. No experimental point is
silently extrapolated during the final comparison. In particular, the baseline
box cannot represent $E_{11}^{(1)}$ below $k_1=0.2$ cm-1; those data are marked
unresolved.

## Verification gates

1. Reference data transcribe Tables 2--4 exactly and pass dimensional checks.
2. Initial velocity has zero mean, finite values, relative spectral divergence
   below $10^{-12}$, and Parseval closure below $10^{-10}$.
3. Shell-integrated $E$ and plane-integrated $E_{11}^{(1)}$ reproduce their
   corresponding kinetic energies.
4. Inviscid nonlinear evaluation conserves energy to roundoff at the
   semi-discrete level.
5. MPI smoke tests pass at more than one rank count; checkpoint/restart lands on
   the same state within floating-point tolerance.
6. Production requires CFL <= 0.5 and $k_{max}\eta >= 1$ at every reported
   station.
7. A reduced-resolution comparison must show that the resolved experimental
   wavenumber range is not materially changed by the production resolution.

## Storage and provenance

- Source, small tables, summaries, and figures:
  `scripts/HIT_dns/` in the Git repository.
- Raw checkpoints and full spectral fields:
  `/media/jay/data1/shenfun_dns_runs/HIT_comte_bellot_1971/` on Linux only.
- The dirty Linux checkout at `/media/jay/data1/shenfun` is not pulled into or
  cleaned. Execution uses an isolated worktree or a checksum-verified copy.
- The repository's actual default branch is `master`; approved milestones are
  committed and pushed there.

## Execution stages

- [x] Audit papers, experimental tables, repository state, and Linux runtime.
- [x] Encode reference data and dimensional mapping.
- [x] Implement and test the Mann initializer and HIT solver.
- [x] Add spectra, diagnostics, checkpoint/restart, and documentation.
- [ ] Commit and push the implementation to `master`.
- [ ] Prepare isolated Linux execution and run MPI smoke tests.
- [ ] Run performance/resolution pilots and lock the production timestep.
- [ ] Run the 32-rank production decay through stations 98 and 171.
- [ ] Compare with Tables 2--4, copy lightweight results to macOS, verify,
      commit, and push.

After every stage, report the completed artifacts, checks, and any deviations
before proceeding.
