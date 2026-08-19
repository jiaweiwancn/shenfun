# Decaying HIT DNS: Comte-Bellot--Corrsin experiment

## Material Passport

- Origin Skill: experiment-agent
- Origin Mode: plan, approved for execution
- Origin Date: 2026-08-08
- Verification Status: VERIFIED on the completed CentOS production run and
  experimental/N256 comparison
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
  `/share/home/dkyzdsys_wanjiawei/shenfun_runs/hit_dns/production_hit_N384_dt1em4_shenfun/raw/`
  on the CentOS server only. The terminated workstation attempt remains under
  `/media/jay/data1/shenfun_dns_runs/HIT_comte_bellot_1971/` and is not a
  production result.
- The dirty Linux checkout at `/media/jay/data1/shenfun` is not pulled into or
  cleaned. Execution uses an isolated worktree or a checksum-verified copy.
- The repository's actual default branch is `master`; approved milestones are
  committed and pushed there.

## Execution stages

- [x] Audit papers, experimental tables, repository state, and Linux runtime.
- [x] Encode reference data and dimensional mapping.
- [x] Implement and test the Mann initializer and HIT solver.
- [x] Add spectra, diagnostics, checkpoint/restart, and documentation.
- [x] Commit and push the implementation to `master`.
- [x] Prepare isolated Linux execution and run MPI smoke tests.
- [x] Run performance/resolution pilots and lock the production timestep.
- [x] Run the 32-rank production decay through stations 98 and 171.
- [x] Compare with Tables 2--4, copy lightweight results to macOS, verify,
      commit, and push.

After every stage, report the completed artifacts, checks, and any deviations
before proceeding.

## Execution status and CentOS migration (2026-08-08)

The first workstation production process was terminated at the user's request
after 51 minutes.  SIGTERM was sent to the resolved MPI launcher, all 32 worker
processes exited, and the process wrapper recorded exit status 15.  The latest
complete diagnostic was step 300 at elapsed DNS time 0.03 s: CFL 0.38498,
$k_{max}\eta=1.25883$, relative divergence $6.62\times10^{-16}$, and Parseval
error $1.64\times10^{-16}$.  The station-42 raw field remains on the Linux
server.  No periodic checkpoint had yet been written, so this partial run is
not a production restart source.

The recurring workstation monitor was deleted.  Execution is being migrated
to the validated CentOS 7/SLURM installation.  Because that immutable offline
environment includes Shenfun 4.3.0 but not spectralDNS, `solver_backend.py`
now provides a pure-Shenfun implementation of the same rotational,
Leray-projected, 3/2-dealiased RK4 operator.  On the Linux test host, the
Shenfun and spectralDNS backends produced bitwise-identical four-rank `32^3`
checkpoints after six RK4 steps (52,224 complex coefficients, maximum absolute
difference zero); both passed all invariant and nonlinear-energy gates.

The CentOS submission package is documented in
[`centos_server/README.md`](centos_server/README.md). Its mandatory sequence
is MPI smoke, full-shape allocation/operator, 32-rank short pilot, station 98,
then explicit latest-checkpoint restart to station 171.

## Final CentOS production result (2026-08-19)

All mandatory CentOS gates completed: jobs 3359, 3360, and 3361 passed the MPI,
full-shape, and 11-step checks; job 3362 advanced station 42 to 98; and job 3363
restarted from the inspector-validated `station_0098.h5` checkpoint and reached
station 171. The final state is at elapsed time 0.65532 s and step 6554. The
combined 68-row diagnostic history is strictly ordered and has monotonically
decreasing kinetic energy. Across the production trajectory, the maximum CFL
is 0.43124, minimum $k_{max}\eta$ is 1.13642, maximum relative divergence is
$2.60\times10^{-15}$, and maximum Parseval error is $5.52\times10^{-16}$.

Only the 44 KiB lightweight return archive was copied to macOS; its SHA-256 is
`2e027dcca3703bee983ce200678b45fe48a8e0c37c79488603a2abc6f58f725d`.
Every embedded checksum passed, the returned error log is empty, and the
archive contains no HDF5 file. The comparison with Tables 2--4 and the N256
pilot is reported in
[`results/lightweight_return_3363/FINAL_REPORT.md`](results/lightweight_return_3363/FINAL_REPORT.md).
The comparison is descriptive because no experimental-agreement threshold was
specified in advance. The strongest bulk discrepancy is dissipation, which is
32.8% above the experiment at station 98 and 23.7% above it at station 171;
velocity RMS differs by at most 8.1%. N384 versus N256 station-98 spectra are
close over the common resolved range: median N384/N256 ratios are 1.037 for
$E$ and 1.024 for $E_{11}^{(1)}$.
