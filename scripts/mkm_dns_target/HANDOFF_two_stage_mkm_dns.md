# Handoff: two-stage MKM channel-flow DNS sample

> Production update: the real `N=(64,64,32)` dataset has now been generated.
> Use `HANDOFF_production_mkm_64_64_32.md` for the accepted production
> outputs, retained sampling window, convergence decision, and final target
> file. This file remains the historical smoke-test handoff for the staged
> workflow.

This handoff describes the sampled MKM channel-flow results produced on the
Linux server, how the samples were collected, how the postprocessed target file
was computed, and what validation was performed.

## Status

This is a workflow and layout validation sample, not a production stationary
DNS dataset. The run deliberately uses a very short spin-up and a very short
sampling window to test the staged pipeline on the current mesh.

The two-stage machinery is now in place:

- spin-up/development run writes no target snapshots
- final spin-up state is forced into a restart checkpoint
- sampling run restarts from the checkpoint and writes only sampling snapshots
- postprocessing reads only the sampling-stage file
- convergence and constraint audit reports are saved beside the data

## Server environment

Server:

```text
jay@100.88.70.60
```

Repository clone:

```text
/media/jay/data/shenfun
```

Conda environment:

```text
/media/jay/data/conda_envs/shenfun_dns_np126_20260702
```

Use `/media/jay/data/tmp` as `TMPDIR` to avoid the nearly full root filesystem.

## Result directory

```text
/media/jay/data/shenfun_dns_runs/two_stage_mkm_64_64_32_test_20260702
```

Files:

```text
MKM_constraints_N64_64_32_cheb_quadrature_spectral.h5  4.4M
MKM_two_stage_64_64_32.chk.h5                          3.2M
MKM_two_stage_64_64_32_U.h5                             13M
MKM_two_stage_64_64_32_U.xdmf                           5.5K
MKM_two_stage_64_64_32_audit.json                       1.7K
MKM_two_stage_64_64_32_sampling_convergence.json        3.6K
MKM_two_stage_64_64_32_sampling_run_config.json         632B
MKM_two_stage_64_64_32_spinup_run_config.json           643B
MKM_two_stage_64_64_32_target.constraints.h5            4.4M
MKM_two_stage_64_64_32_target.h5                        3.4G
```

## Current mesh and solver setup

The tested DNS setup used `demo/MKM.py` through
`scripts/mkm_dns_target/run_mkm_dns.py`.

Common parameters:

```text
N = (64, 64, 32) in solver order (wall-normal, streamwise, spanwise)
domain = ((-1, 1), (0, 2*pi), (0, pi))
Re_tau = 180
dt = 0.0005
conv = 0
family = C
padding_factor = (1.5, 1.5, 1.5)
timestepper = IMEXRK222
saved mesh = quadrature
MPI ranks = 16
```

The saved wall-normal grid is the solver-native Chebyshev-Gauss quadrature grid,
not the uniform interpolation grid. The endpoints are not included in the saved
velocity grid. For this mesh the first and last saved wall-normal coordinates
are approximately:

```text
z_first =  0.9996988186962042
z_last  = -0.9996988186962042
```

## Sampling stages

### Stage 1: spin-up/development

Purpose: allow the demo initialization to develop before any target snapshots
are sampled.

This short test used:

```text
stage_label = spinup
from_checkpoint = false
disable_snapshots = true
force_final_checkpoint = true
end_time = 0.01
modsave = 100000000
checkpoint = 100000000
```

The forced final checkpoint was written at:

```text
t = 0.01
tstep = 20
checkpoint = MKM_two_stage_64_64_32.chk.h5
```

### Stage 2: stationary sampling

Purpose: restart from the spin-up checkpoint and write only the samples used by
the postprocessor.

This short test used:

```text
stage_label = sampling
from_checkpoint = true
disable_snapshots = false
force_final_checkpoint = true
end_time = 0.03
modsave = 10
checkpoint = 100
```

The sampled velocity snapshots in `MKM_two_stage_64_64_32_U.h5` are:

```text
tstep keys = 30, 40, 50, 60
times      = 0.015, 0.020, 0.025, 0.030
```

No spin-up snapshots are present in the sampled velocity file.

## Component and vector ordering

The MKM solver stores velocity components in solver/HDF5 group order:

```text
u0 = wallnormal
u1 = streamwise
u2 = spanwise
```

The target postprocessor uses component order:

```text
streamwise, spanwise, wallnormal
```

For a fixed horizontal Fourier mode, the target modal vector is level-major:

```text
[u_streamwise(z0), u_spanwise(z0), u_wallnormal(z0),
 u_streamwise(z1), u_spanwise(z1), u_wallnormal(z1),
 ...
 u_streamwise(z63), u_spanwise(z63), u_wallnormal(z63)]
```

The modal vector dimension is:

```text
3 * Nz = 192
```

## Postprocessed target file layout

Target file:

```text
MKM_two_stage_64_64_32_target.h5
```

Important datasets:

```text
geometry/z_wall
geometry/x_stream
geometry/x_span
geometry/k_stream
geometry/k_span
sampling/t
mean_profile
reynolds_stress_profile
modal/u_hat
modal/B0_DNS
modal/mode_energy
lag_covariance/lag_0
lag_covariance/lag_1
```

Validated shapes:

```text
mean_profile:              (64, 3)
reynolds_stress_profile:   (64, 3, 3)
modal/u_hat:               (4, 64, 32, 192)
modal/B0_DNS:              (64, 32, 192, 192)
lag_covariance/lag_0:      (64, 32, 192, 192)
lag_covariance/lag_1:      (64, 32, 192, 192)
```

The target file records `sampling_stage_label = stationary`. For this test that
label means "the file came from the sampling stage after a restart", not that a
production stationarity criterion has been proven.

## How the target quantities are computed

For each selected snapshot key, the postprocessor reads:

```text
data[component, z, streamwise_index, spanwise_index]
```

in target component order:

```text
streamwise, spanwise, wallnormal
```

The mean profile is the average over all selected snapshots and both horizontal
directions:

```text
mean[c, z] = average_nxy u[c, z, x, y]
```

The fluctuation field is:

```text
u_fluct[c, z, x, y] = u[c, z, x, y] - mean[c, z]
```

The Reynolds-stress profile is:

```text
R[z, a, b] = average_nxy u_fluct[a, z, x, y] * u_fluct[b, z, x, y]
```

The horizontal Fourier coefficients are computed with NumPy FFTs:

```text
u_hat = fft2(u_fluct, axes=(streamwise, spanwise)) / (Nx * Ny)
```

They are then reshaped into modal vectors with shape:

```text
(Nx, Ny, 3*Nz)
```

The equal-time covariance for each horizontal mode is:

```text
B0_DNS[kx, ky] = average_n u_hat[n, kx, ky] * u_hat[n, kx, ky]^H
```

The stored `B0_DNS` is Hermitian symmetrized:

```text
B0_DNS = 0.5 * (B0_DNS + B0_DNS^H)
```

The positive-lag covariance uses the unbiased positive-lag estimator:

```text
lag_L[kx, ky] = average_{n=0}^{Ns-L-1}
                u_hat[n+L, kx, ky] * u_hat[n, kx, ky]^H
```

For this test `max_lag = 1`, so `lag_0` and `lag_1` were written.

## Constraint file

Constraint file:

```text
MKM_constraints_N64_64_32_cheb_quadrature_spectral.h5
```

The constraint is built on the same Chebyshev-Gauss quadrature grid as the
saved velocity snapshots.

Saved operators:

```text
operators/D_wall
operators/B_boundary
operators/E_stream
operators/E_span
operators/E_wall
```

The streamwise/spanwise/wallnormal extraction matrices are purely component
selectors and do not differ between the Chebyshev/quadrature and uniform-grid
constraint options.

For a horizontal mode `(k_stream, k_span)`, the raw divergence block is:

```text
Gdiv = 1j*k_stream*E_stream + 1j*k_span*E_span + D_wall@E_wall
```

The no-slip boundary block is:

```text
Gboundary = stack(B_boundary@E_stream,
                  B_boundary@E_span,
                  B_boundary@E_wall)
```

The raw constraint matrix is:

```text
Graw = stack(Gdiv, Gboundary)
```

For the Chebyshev/quadrature spectral option:

```text
D_wall      = barycentric spectral nodal first derivative
B_boundary = barycentric interpolation from quadrature nodes to z = -1 and z = 1
```

For each representative mode, the saved `Gtilde` is computed from an SVD of
`Graw`. `Gtilde` contains an orthonormal row basis for the retained constraint
space. A dense `Gtilde` table for every mode is not saved by default; use
`--save-all-gtilde` if it is needed later.

Rank audit:

```text
rank 68: 1 mode
rank 70: 2047 modes
```

## Validation and convergence reports

Sampling convergence report:

```text
MKM_two_stage_64_64_32_sampling_convergence.json
```

Selected samples:

```text
keys = 30, 40, 50, 60
sample time range = 0.015 to 0.030
n_snapshots = 4
```

Two-block smoke-test results:

```text
max block mean-profile relative deviation from all samples     = 1.613e-4
max block Reynolds-profile relative deviation from all samples = 1.631e-2
first/second half mean-profile relative change                 = 3.226e-4
first/second half Reynolds-profile relative change             = 3.220e-2
converged_by_tolerance at 5 percent                            = true
```

This is only a smoke-test tolerance over four snapshots. It verifies the
convergence-check machinery, but it does not prove production stationarity.

Target audit report:

```text
MKM_two_stage_64_64_32_audit.json
```

Key audit results:

```text
z_grid_match_constraint = true
z_grid_match_velocity   = true
constraint_residual_global_rel = 2.304731892618198e-14
constraint_div_global_rel      = 2.304450548678361e-14
constraint_bc_global_rel       = 3.601063103395398e-16
constraint_modes_above_energy_floor = 1953
constraint_max_mode_rel_nontrivial  = 2.8296227296357916e-11
representative_B0_hermitian_rel_max = 0.0
representative_lag0_minus_B0_rel_max = 1.7993530725287927e-17
```

## Reproduction commands

Set common paths:

```bash
export TMPDIR=/media/jay/data/tmp
ENV=/media/jay/data/conda_envs/shenfun_dns_np126_20260702
REPO=/media/jay/data/shenfun
OUT=/media/jay/data/shenfun_dns_runs/two_stage_mkm_64_64_32_test_20260702
mkdir -p "$OUT"
cd "$OUT"
```

Spin-up/development stage:

```bash
"$ENV/bin/mpiexec" -n 16 "$ENV/bin/python" \
  "$REPO/scripts/mkm_dns_target/run_mkm_dns.py" \
  --output-dir "$OUT" \
  --n 64 64 32 \
  --dt 0.0005 \
  --end-time 0.01 \
  --modsave 100000000 \
  --checkpoint 100000000 \
  --moderror 10 \
  --modplot -1 \
  --stage-label spinup \
  --disable-snapshots \
  --force-final-checkpoint \
  --skip-xdmf \
  --filename MKM_two_stage_64_64_32
```

Sampling stage:

```bash
"$ENV/bin/mpiexec" -n 16 "$ENV/bin/python" \
  "$REPO/scripts/mkm_dns_target/run_mkm_dns.py" \
  --output-dir "$OUT" \
  --n 64 64 32 \
  --dt 0.0005 \
  --end-time 0.03 \
  --modsave 10 \
  --checkpoint 100 \
  --moderror 10 \
  --modplot -1 \
  --stage-label sampling \
  --from-checkpoint \
  --force-final-checkpoint \
  --filename MKM_two_stage_64_64_32
```

Constraint construction:

```bash
"$ENV/bin/python" "$REPO/scripts/mkm_dns_target/build_mkm_constraints.py" \
  --output "$OUT/MKM_constraints_N64_64_32_cheb_quadrature_spectral.h5" \
  --n 64 64 32 \
  --wall-domain -1 1 \
  --stream-length 6.283185307179586 \
  --span-length 3.141592653589793
```

Sampling convergence check:

```bash
"$ENV/bin/python" "$REPO/scripts/mkm_dns_target/check_mkm_sampling_convergence.py" \
  --velocity-h5 "$OUT/MKM_two_stage_64_64_32_U.h5" \
  --output "$OUT/MKM_two_stage_64_64_32_sampling_convergence.json" \
  --dt 0.0005 \
  --n-blocks 2 \
  --tolerance 0.05
```

Target postprocess:

```bash
"$ENV/bin/python" "$REPO/scripts/mkm_dns_target/postprocess_mkm_dns_target.py" \
  --velocity-h5 "$OUT/MKM_two_stage_64_64_32_U.h5" \
  --output "$OUT/MKM_two_stage_64_64_32_target.h5" \
  --dt 0.0005 \
  --constraint-file "$OUT/MKM_constraints_N64_64_32_cheb_quadrature_spectral.h5" \
  --sampling-stage-label stationary \
  --mode-batch 4 \
  --store-modal-coefficients \
  --max-lag 1
```

Target audit:

```bash
"$ENV/bin/python" "$REPO/scripts/mkm_dns_target/audit_mkm_target.py" \
  --target-h5 "$OUT/MKM_two_stage_64_64_32_target.h5" \
  --velocity-h5 "$OUT/MKM_two_stage_64_64_32_U.h5" \
  --constraint-file "$OUT/MKM_constraints_N64_64_32_cheb_quadrature_spectral.h5" \
  --output "$OUT/MKM_two_stage_64_64_32_audit.json"
```

Temporal physical-space diagnostics were added after the production run:

```text
scripts/mkm_dns_target/compute_mkm_velocity_autocovariance.py
scripts/mkm_dns_target/compute_mkm_velocity_autospectrum.py
```

They compute `x-y` plane-averaged `R_ii(tau; z)` and `S_ii(omega; z)` from a
retained velocity snapshot window. They are mainly production/reproduction
diagnostics; the four-snapshot smoke-test data in this handoff is too short
for a meaningful temporal spectrum. See
`HANDOFF_production_mkm_64_64_32.md` for the accepted-window commands and
outputs.

## Production follow-up

For the real dataset:

1. Run a much longer spin-up stage.
2. Accept the spin-up checkpoint only after monitored quantities settle:
   bulk flux, kinetic-energy components, wall stress/friction velocity, mean
   profile, and Reynolds stresses.
3. Restart from that checkpoint for a longer stationary sampling run.
4. Use the convergence helper with more blocks and stricter tolerances.
5. Postprocess only the accepted stationary-stage samples.
6. Keep the saved Chebyshev/quadrature constraint beside the target file.
