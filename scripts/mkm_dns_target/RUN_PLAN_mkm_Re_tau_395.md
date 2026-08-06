# Run plan: MKM channel DNS at nominal Re_tau = 395

## Material Passport

- Origin Skill: experiment-agent
- Origin Mode: plan
- Origin Date: 2026-07-27
- Verification Status: CentOS numerical/I/O gates passed; refined-step and physical-acceptance gates pending
- Version Label: code_plan_v5

## Status and execution gate

This document is a pre-production plan. Short Re_tau=395 numerical verification
pilots have been run, but no spin-up or stationary production record has been
started. Production execution begins only after the mesh, initialization,
time-step, MPI-decomposition, diagnostic, and storage gates below have passed
on the target server and the plan has been approved.

As of 27 July 2026, the Re_tau=395 profile initialization, independent-state
writer, round-trip validator, and CentOS/SLURM submission templates have been
prepared and exercised. A four-rank Ubuntu test established that the optimized
Shenfun Chebyshev biharmonic solver fails for odd wall-normal sizes but passes
the matched even-size test. The baseline has therefore been revised to 192
wall-normal points. The full shape subsequently passed two-step allocation
tests at 16, 32, and 64 MPI ranks and a 64-rank, 192-plane state/velocity
round trip. A reduced two-stage checkpoint/restart and append test also
passed. CentOS jobs 3200--3204 then passed the small-grid, 16/32/64-rank
full-shape allocation, and 64-rank state-I/O gates. The former
`dt=0.00025` full-resolution pilot in job 3206 was rejected after its CFL
exceeded one and the solution became non-finite. The revised candidate is
`dt=0.00005`; its target-server stability/performance pilot and all
physical-acceptance gates remain pending.

The matching technical note is:

```text
docs/mkm_channel_dns_sampling_and_constraints_Re_tau_395.tex
```

The CentOS/SLURM test and staged submission files are documented in:

```text
re395_server/README.md
```

Passwords and other credentials must not be written to run scripts, logs,
configuration JSON, or handoff documents.

## Reference case and proposed baseline

The Moser--Kim--Mansour (MKM) 1999 Re_tau approximately 395 case used:

```text
actual reference Re_tau = 392.24
domain                  = 2*pi*h by 2*h by pi*h
paper order             = Nx by Ny by Nz = 256 by 193 by 192
Delta x+                = about 10.0
Delta z+                = about 6.5
Delta y_center+         = about 6.5
```

The corresponding Shenfun proposal is:

```text
nominal Re_tau          = 395
solver order --n        = 192 256 192
                         (wall-normal, streamwise, spanwise)
domain                  = ((-1,1), (0,2*pi), (0,pi))
saved wall mesh         = quadrature (Chebyshev-Gauss)
horizontal sizes        = even
wall-normal size        = even
requested padded sizes  = 288 384 288
padding-factor          = 1.5, 1.5, 1.5
refined production dt candidate = 0.00005
time stepper            = IMEXRK222
```

At Re_tau=395, this grid has the nominal spacings:

```text
Delta x+                        = 2*pi*395/256 = 9.69476
Delta z+                        = pi*395/192   = 6.46317
Chebyshev-Gauss center gap+     = 2*395*sin(pi/(2*192)) = 6.46310
nearest saved point to center+  = 395*sin(pi/(2*192)) = 3.23155
first saved point from a wall+  = 395*(1-cos(pi/(2*192))) = 0.01322
saved points below y+=10        = 14 per wall
```

The official MKM mean profile is normalized by the reference friction
velocity and has actual Re_tau=392.24. Integrating that half-channel mean
profile gives the planning value

```text
Ub/u_tau = 17.5447511436
```

for the constant-flux target. For the current domain, the corresponding
integrated flux is approximately 692.639012411. The final run must report the
measured wall stress and actual Re_tau; it must not assume that setting
`nu=1/395` alone proves the achieved friction Reynolds number.

## Why the paper uses an odd count but this solver uses 192

The odd values 129, 193, and 257 in the MKM table are numerical grid
conventions, not a turbulence requirement. In the classical
Chebyshev--Gauss--Lobatto representation, an even maximum polynomial degree
gives one more nodal value, so the point count is odd. This convention includes
both walls and the centerline and gives transform lengths such as 128, 192,
and 256 between the endpoints.

Shenfun's present `family=C` setup uses Chebyshev-Gauss quadrature nodes rather
than the paper's endpoint-including Lobatto grid. The transforms and composite
bases can represent odd sizes, but the optimized biharmonic linear solver used
by the MKM wall-normal-velocity equation splits the system into equal
even/odd parity blocks. A real `N_wall=17` test was finite after initialization
but produced non-finite velocity coefficients in the first Runge--Kutta
substage. The matched `N_wall=18` case remained finite for 40 steps and passed
the exact state/velocity round trip on all planes.

Consequently, an odd wall-normal size must not be used with this solver
implementation. The user-selected `N_wall=192` is one point (0.52 percent)
below the paper's count, retains 14 Gauss points per wall below `y+=10`, and
has a center gap essentially equal to the reference center spacing. A literal
padding factor 1.5 gives the integer padded wall size 288. Keep both Fourier
sizes even for FFT efficiency, real-transform/Nyquist conventions, and
convenient MPI decomposition.

## Gate 1: make the Re_tau=395 inputs honest

Do not launch the full mesh by changing only `--re`. Before any production
job, update and test the driver/initialization so that the following quantities
are explicit run inputs and are recorded in JSON:

1. Nominal Re_tau and viscosity.
2. Target `Ub/u_tau` and integrated flux.
3. The initial mean profile or its parameterization.
4. Perturbation amplitudes and wavelengths in wall units.
5. The intended padded sizes after integer rounding.
6. An all-plane state writer: the solver's independent wall-normal-velocity
   and wall-normal-vorticity coefficient arrays, plus the two separately
   evolved zero-horizontal-mode velocity profiles, every 100 steps; online
   block moments at the chosen statistics cadence; and a complete audit
   velocity field every 200000 steps. The current runner has only one
   full-field `modsave` cadence, so this writer and its decoder must be
   implemented and smoke-tested before stationary sampling.

The current `demo/MKM.py` still contains Re_tau=180-specific values:

```text
Um = 46.9091*u_tau
bulk_velocity default = 618.97/(4*pi^2)
comments and perturbation choices marked for Re=180
```

Recommended initialization for the new case:

- interpolate the official MKM Re_tau=392.24 mean profile onto the
  Chebyshev-Gauss nodes, reflected across the centerline;
- use that profile only as an initial condition/reference, not as sampled DNS
  evidence;
- add low-amplitude, divergence-compatible perturbations with wavelengths
  defined explicitly in wall/outer units;
- confirm no-slip and divergence residuals after the initial forward/backward
  projections.

## Gate 2: add run diagnostics needed to verify Re_tau

The production log or a sidecar diagnostics file must include, at a fixed
cadence:

```text
time and time step
bulk flux and Ub
wall shear at each wall
u_tau at each wall and their average
actual Re_tau = u_tau*h/nu
streamwise, spanwise, and wall-normal kinetic energy
maximum divergence norm
maximum velocity and a documented CFL estimate
mean-profile checkpoints
Reynolds-stress-profile checkpoints
high-wavenumber spectral-tail ratios in x and z
```

The wall derivative must be evaluated consistently from the Chebyshev
representation at z=+-1. Acceptance uses the measured, time-averaged wall
stress. A planning tolerance is:

```text
abs(Re_tau_actual - 395)/395 <= 0.02
```

If this is missed, adjust the constant-flux target and repeat a short
calibration continuation before the long sampling stage.

## Gate 3: local and server smoke tests

Run these tests before physical spin-up:

1. A small even-wall mesh, `--n 18 32 24`, through initialization, one
   restart, quadrature output, state reconstruction, and a full NaN/Inf audit.
2. A full-shape allocation/decomposition test at `--n 192 256 192` for a few
   steps without snapshots.
3. Full-shape benchmarks at feasible MPI sizes, initially 16, 32, and 64
   ranks, retaining only decompositions that work for both the unpadded
   `(192,256,192)` and padded `(288,384,288)` shapes.
4. A forced-checkpoint/restart comparison in which the restarted state matches
   the uninterrupted state to roundoff-level solver tolerance.
5. A short HDF5 write/read test on the production filesystem.

On the Ubuntu server the full shape passed at 16, 32, and 64 ranks; the
64-rank two-step wrapper time was 9.56 s, compared with 14.04 s and 14.71 s
at 16 and 32 ranks. These very short timings include startup and checkpoint
I/O and are not production scaling measurements. The first 64-rank launch
also exposed a Matplotlib font-cache lock race, fixed by warming the cache
serially before `mpiexec`. CentOS jobs 3201--3203 also passed at 16, 32, and
64 ranks; job 3204 passed the 64-rank full-shape I/O gate. The submission
scripts reserve two SLURM tasks per MPI rank, so a 64-rank run requests
`--ntasks=128` and explicitly launches `mpiexec -n 64`. Select the final MPI
size from refined-step timing and memory headroom.

## Gate 4: time-step and spatial-resolution pilot

Job 3206 tested the full mesh with:

```text
dt = 0.00025
```

That candidate is rejected. The reported CFL was already `1.007` at `t=0.1`,
rose to approximately `1.60`, and the spanwise kinetic energy increased from
`0.3907` to `12.8004` by `t=0.8`. At `t=0.9` all 28,311,552 physical velocity
values were non-finite. The 192-point Chebyshev-Gauss mesh has a minimum
wall-normal spacing about one ninth that of the old 64-point mesh. Scaling the
old Re_tau=180 step `0.0005` by that spacing ratio gives approximately
`5.56e-5`. The revised conservative candidate is therefore:

```text
dt = 0.00005
```

Run the first refined full-mesh continuation only to `t=1`, with diagnostics
every `0.1` outer units. Accept it only if CFL remains comfortably below one,
all values remain finite, energy and divergence remain controlled, restart is
consistent, and high-wavenumber spectra show no pile-up. Do not increase the
step without a separate accepted comparison.

The revised step/cadence combination passed a 4-rank, 200-step
`(18,32,24)` Ubuntu round trip on 27 July 2026: all 20 samples reconstructed
exactly, no non-finite values were found, maximum divergence was `1.06e-15`,
and CFL remained at or below `0.00609`. This is a software/I/O check only; it
does not replace the full-mesh `t=1` stability gate.

The full-mesh pilot must also check:

- no energy pile-up at the largest retained streamwise/spanwise wavenumbers;
- mean and Reynolds-stress profiles against the official MKM reference;
- two-point correlations close to zero at half-box separation;
- at least 13 wall-normal points below y+=10 (the proposal has 14 saved Gauss
  points per wall);
- symmetry between the two channel halves;
- constraint residuals on the even Chebyshev-Gauss grid.

If the spectral tails or reference comparisons fail, increase resolution or
correct the numerical setup before increasing run length.

## Gate 5: spin-up/development

Use the established two-stage separation:

- stage label `spinup`;
- no target velocity snapshots;
- diagnostics enabled;
- forced final checkpoint;
- extend in restartable segments rather than committing to one long job.

Do not prescribe an accepted spin-up end solely from the Re_tau=180 value
`t=20`. The user-selected sampling start is fixed at `t=120`. Begin with the
refined-step `t=1` calibration, then use five-outer-unit restart segments if
their measured runtime fits the allocation. Inspect physical reviews at outer
times 20, 40, 60, 80, 100, and 120. No retained temporal sampling is permitted
before 120. Transfer the `t=120` checkpoint only when:

1. bulk flux is at the target;
2. measured Re_tau is within tolerance and has no block drift;
3. all three kinetic-energy components are statistically steady;
4. block mean and Reynolds-stress profiles are steady;
5. divergence and boundary residuals are small;
6. spectral-tail and half-box-correlation checks pass.

## Gate 6: stationary sampling

After accepting the spin-up checkpoint at `t=120`, retain the fixed window
through `t=300`:

- restart into a new sampling-stage velocity file;
- use a dense temporal cadence of `Delta t_temporal=0.005` outer time units;
- write the complete independent MKM spectral state at the dense cadence:
  wall-normal velocity, wall-normal vorticity, and the two zero-horizontal-mode
  profiles;
- reconstruct all three velocities on all 192 horizontal planes during
  postprocessing;
- accumulate all-wall block mean/Reynolds moments online;
- retain a complete audit field only every 10 outer time units and at the final
  accepted state;
- append into 1,000-sample, five-outer-time-unit state shards while retaining
  40-time-unit convergence review segments;
- force a checkpoint at every segment end;
- evaluate candidate retained windows after every segment;
- use at least 12 time blocks and the existing 5 percent field mean/Reynolds
  tolerance as the first acceptance gate;
- retain the scalar-energy caveat separately, as in the Re_tau=180 handoff;
- prefer a 3 percent sensitivity check before declaring the final production
  window.

For `dt=0.00005`, the dense temporal cadence corresponds to every 100 DNS
steps, while a complete audit field is written every 200000 DNS steps:

```text
Delta t_temporal = 0.005 = 100*dt
Delta t_temporal+ = Re_tau*Delta t_temporal = 1.975
temporal Nyquist angular frequency = pi/0.005 = 628.319 u_tau/h

Delta t_audit_field = 10 = 200000*dt
sampling start step = 120/0.00005 = 2400000
sampling end step   = 300/0.00005 = 6000000
stationary DNS steps = 3600000
stationary duration = 180
retained samples    = 180/0.005 = 36000
```

Before committing to the dense cadence, run a short sensitivity record every
50 DNS steps (`Delta t=0.0025`, `Delta t+=0.9875`) and compare temporal
correlations and spectra with the record decimated to 0.005. Use 0.0025 for
production only if the 0.005 record measurably aliases or changes the frequency
band of interest.

The dense temporal output is not a selected-plane record. It contains the
solver-native independent state needed to reconstruct all three velocity
components at every wall-normal level and every retained horizontal mode. The
state is stored in complex128/float64 with lossless compression only.
Selected-mode CSD/resolvent products can be extracted later without limiting
the permanent record to those modes. Online block statistics remain as an
independent convergence/reconstruction audit.

For the fixed 180-unit stationary record, 0.005 gives 36,000 temporal samples.
A Hann/Welch estimate with 8,192-sample segments and 50 percent overlap has a
segment duration of 40.96 and angular-frequency spacing about 0.1534; a
full-record diagnostic periodogram has spacing about 0.03491. Store the dense
sampling times and the exact realized spacing in every temporal product.

`lag_0` and `lag_1` covariance datasets are not part of this run. Set
`--max-lag -1` in any use of the legacy target postprocessor, and do not create
the `lag_covariance` group.

The detailed sufficient-data design, output schemas, storage calculation, and
short-run numerical-equivalence test are in
`TEMPORAL_SAMPLING_REMEDY_Re_tau_395.md`.

## Storage and postprocessing gate

The new mesh is exactly 72 times larger in physical points than the old
`(64,64,32)` solver mesh. Approximate uncompressed sizes are:

```text
one physical velocity snapshot                        0.210938 GiB
36,000 dense three-component physical samples          7.41577 TiB
one independent spectral-state sample                 0.142093 GiB
36,000 independent spectral-state samples              4.99545 TiB
18 complete audit fields                               3.79688 GiB
full equal-time B0_DNS, if retained                  about 243 GiB
```

Therefore:

1. Check free space, quotas, inode limits, HDF5 throughput, and backup policy
   before sampling.
2. Capacity approval uses the 5.00 TiB uncompressed state budget plus
   checkpoints, derived products, scratch, and safety headroom; target at least
   7 TiB excluding any large disposable reconstruction cache.
3. Produce mean/Reynolds statistics and convergence reports from online block
   raw moments as an independent audit, while retaining the all-plane temporal
   state for correlation and spectrum calculations.
4. Use only exact reductions: the native real-to-complex half-spectrum, the
   two independent MKM state variables, the required zero modes, and benchmarked
   lossless compression. Do not use float32, lossy compression, mode
   truncation, wall-normal subsampling, or further temporal decimation without
   a separate accepted error study.
5. Store state in appendable 1,000-sample shards (about 142.09 GiB each before
   compression), with per-shard manifests and checksums.
6. Decide explicitly whether an approximately 243 GiB full equal-time
   covariance is needed.
7. Benchmark and, if needed, extend the constraint builder and postprocessor;
   both the 49,152-mode SVD audit and the full covariance are much larger than
   in the old workflow.
8. Before production, perform a 512-sample dual-write test and require
   reconstructed fields, all-plane correlations, and all-plane spectra to
   agree with conventional dense output to the documented roundoff/FFT
   tolerance.

## Planned command card (not yet executable as production)

After Gates 1--4 pass, the common settings should resolve to the following.
The 64-rank and refined-step values remain subject to the `t=1` pilot; the
spin-up and sampling endpoints are fixed at 120 and 300.

```bash
export TMPDIR=/media/jay/data1/tmp
ENV=/media/jay/data1/conda_envs/shenfun_dns_np126_20260702
REPO=/media/jay/data1/shenfun
OUT=/media/jay/data1/shenfun_dns_runs/production_mkm_Re395_N192_256_192_dt5em5
PREFIX=MKM_production_Re395_N192_256_192_dt5em5
NP=64
SLURM_NTASKS=128
DT=0.00005

"$ENV/bin/mpiexec" -n "$NP" "$ENV/bin/python" -u \
  "$REPO/scripts/mkm_dns_target/run_mkm_dns.py" \
  --output-dir "$OUT" \
  --n 192 256 192 \
  --re 395 \
  --bulk-velocity 17.54475114359453 \
  --dt "$DT" \
  --padding-factor 1.5 1.5 1.5 \
  --end-time 120 \
  --modsave 100000000 \
  --checkpoint 100000 \
  --moderror 2000 \
  --modplot -1 \
  --stage-label spinup \
  --disable-snapshots \
  --force-final-checkpoint \
  --skip-xdmf \
  --filename "$PREFIX"
```

The sampling command is formed only after the `t=120` spin-up checkpoint is accepted
and the all-plane state writer/decoder has passed its dual-write round trip.
For `DT=0.00005`, save the independent state every 100 steps, close a shard
every 1,000 samples, and save a complete audit velocity field every 200000
steps through the fixed final time `t=300`. The legacy target postprocessor
must use `--max-lag -1`; no `lag_0` or `lag_1` is generated.

## Acceptance and handoff

The production handoff must record:

- code revision and local uncommitted changes relevant to the run;
- all resolved inputs, including the initialization and integer padded sizes;
- server paths, environment, MPI size, and measured performance;
- actual time-averaged Re_tau and wall-stress symmetry;
- accepted spin-up checkpoint and sampling window;
- block convergence and scalar diagnostics;
- spectra, correlations, mean/Reynolds comparisons to MKM;
- raw/processed file sizes and checksums;
- constraint construction and target audit results;
- the dense temporal cadence, state-reconstruction version, round-trip report,
  lossless filter, and estimator settings, plus any deliberate omission of
  dense physical fields.
