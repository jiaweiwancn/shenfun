# Handoff: production MKM channel-flow DNS target, N=(64,64,32)

This handoff records the real MKM channel-flow DNS dataset generated on the
Linux server after the two-stage workflow was validated. It supersedes the
short smoke-test handoff for production use.

## Status

The production run completed on 2026-07-02.

Final accepted target:

```text
/media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/MKM_production_64_64_32_target_t60_t180.h5
```

The retained target window is `t = 60` to `t = 180`, selected after checking
block convergence of the sampled velocity fields. Earlier sampled data remains
in the raw velocity file but is not used in the accepted target because the
full `t = 20.1` to `t = 180` window was still marginal by the Reynolds-stress
block criterion.

No matching production DNS or postprocessing processes were left running after
completion.

## Server environment

Server:

```text
jay@100.88.70.60
```

Repository clone:

```text
/media/jay/data1/shenfun
```

Conda environment:

```text
/media/jay/data1/conda_envs/shenfun_dns_np126_20260702
```

Temporary directory:

```text
TMPDIR=/media/jay/data1/tmp
```

The live server mount verified during the first channel-resolvent production
execution was `/media/jay/data1`. Older two-stage pilot notes may still mention
`/media/jay/data`; use `/media/jay/data1` for the current production server
unless a future path check shows otherwise.

## Production output directory

```text
/media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702
```

Key files:

```text
MKM_production_64_64_32_U.h5                          4.7G
MKM_production_64_64_32.chk.h5                        3.2M
MKM_constraints_N64_64_32_cheb_quadrature_spectral.h5 4.4M
MKM_production_64_64_32_target_t60_t180.h5            11G
MKM_production_64_64_32_target_t60_t180.constraints.h5 4.4M
MKM_production_64_64_32_audit_t60_t180.json           32K
MKM_production_64_64_32_projected_covariance_t60_t180.h5   1.2G
MKM_production_64_64_32_projected_covariance_t60_t180.json 1.3K
MKM_production_64_64_32_sampling_field_convergence_t60_t180.json 533K
MKM_production_64_64_32_sampling_t60_t180_diagnostics.json       42K
```

The raw velocity file contains all appended sampling snapshots from the
accepted and rejected sampling intervals. The target file contains only the
accepted `t = 60` to `t = 180` subset.

## Dense temporal continuation output directory

The accepted equal-time target remains
`MKM_production_64_64_32_target_t60_t180.h5`. A separate dense-sampling
continuation was run only for temporal auto-correlation and auto-spectrum
diagnostics, because the production target snapshots were saved every
`Delta t_sample = 0.1`.

Dense temporal directory:

```text
/media/jay/data1/shenfun_dns_runs/dense_temporal_mkm_64_64_32_t180_t300_20260703
```

Key files:

```text
MKM_dense_temporal_64_64_32_t180_t300_U.h5                         36G
MKM_dense_temporal_64_64_32_t180_t300.chk.h5                       3.2M
MKM_dense_temporal_64_64_32_t180_t300_sampling_run_config.json     681B
MKM_dense_temporal_64_64_32_t180_t300.log                          6.5K
MKM_dense_temporal_64_64_32_t180_t300_temporal_postprocess.log     4.6K
MKM_dense_temporal_64_64_32_t180_t300_velocity_autocovariance_lag2.h5 1.2M
MKM_dense_temporal_64_64_32_t180_t300_velocity_autocovariance_lag2_selected_z.pdf 115K
MKM_dense_temporal_64_64_32_t180_t300_velocity_autospectrum_hann.h5 19M
MKM_dense_temporal_64_64_32_t180_t300_velocity_autospectrum_hann_selected_z_loglog.pdf 389K
```

The dense velocity file is deliberately separate from
`MKM_production_64_64_32_U.h5`, so the production sparse cadence and the dense
temporal cadence are not mixed in one HDF5 file.

## Mesh and solver setup

The DNS uses `demo/MKM.py` through
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
MPI ranks used for production = 16
```

The saved wall-normal grid is the solver-native Chebyshev-Gauss quadrature
grid, not a uniform interpolation grid. The endpoints are not included in the
saved velocity grid.

The current mesh did not support a 64-rank decomposition; the attempted run
failed with an `mpi4py_fft` shape/decomposition assertion because one
distributed direction has length 32. The production run therefore used the
validated 16-rank configuration.

## DNS stages actually run

### Spin-up/development

Purpose: start from the demo initialization and allow the flow to develop
without writing target snapshots.

```text
stage_label = spinup
from_checkpoint = false
disable_snapshots = true
force_final_checkpoint = true
end_time = 20.0
modsave = 100000000
checkpoint = 100000000
moderror = 2000
MPI ranks = 16
```

Final spin-up state:

```text
final_t = 20
final_tstep = 40000
checkpoint = MKM_production_64_64_32.chk.h5
```

### Stationary sampling candidates

Sampling restarted from the spin-up checkpoint, wrote snapshots every
`modsave = 200` steps, and forced a checkpoint at the end of each segment.
With `dt = 0.0005`, the stored snapshot spacing is `Delta t_sample = 0.1`.

Segments:

```text
t = 20  to 60   initial sampling segment
t = 60  to 100  appended sampling segment
t = 100 to 140  appended sampling segment
t = 140 to 180  appended sampling segment
```

The append-mode segments used:

```text
--from-checkpoint
--velocity-file-mode a
--force-final-checkpoint
```

Final DNS state:

```text
final_t = 179.999999999
final_tstep = 360000
checkpoint_h5 = MKM_production_64_64_32.chk.h5
velocity_h5 = MKM_production_64_64_32_U.h5
```

The raw sampled velocity file contains:

```text
n_snapshots = 1600
sample_time_range = 20.1 to 180
```

## Accepted sampling window

The full sampled interval was checked first:

```text
window = 20.1 to 180
n_snapshots = 1600
max_mean_block_rel_to_all = 8.341829e-03
max_reynolds_block_rel_to_all = 5.360744e-02
converged_by_tolerance = false
```

Dropping only the earliest portion improved the result but was still marginal:

```text
window = 40 to 180
n_snapshots = 1401
max_mean_block_rel_to_all = 8.157623e-03
max_reynolds_block_rel_to_all = 5.094524e-02
converged_by_tolerance = false
```

The accepted field-statistical window is:

```text
window = 60 to 180
n_snapshots = 1201
max_mean_block_rel_to_all = 5.048126e-03
max_reynolds_block_rel_to_all = 4.166622e-02
tolerance = 0.05
converged_by_tolerance = true
```

This is the window used in the final target file.

Scalar diagnostics over the same retained interval are mostly steady, but the
coarse 12-block scalar parser still flags spanwise kinetic-energy fluctuation:

```text
diagnostic records = 48
diagnostic time range = 62.5 to 180
max_first_last_monitored = 7.231984e-02
max_successive_monitored = 7.372876e-02
stationary_by_tolerance = false
```

The scalar flag is driven mainly by spanwise energy. Over the same scalar
blocks, streamwise energy, wall-normal energy, and bulk flux are much steadier:

```text
first-last relative change, wallnormal energy = 1.037867e-03
first-last relative change, streamwise energy = 1.208379e-03
first-last relative change, spanwise energy   = 7.231984e-02
first-last relative change, flux              = 1.087099e-07
max divergence                                = 2.500295e-14
```

The production target uses the field mean/Reynolds convergence criterion,
while retaining this scalar caveat explicitly.

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

## Final target file layout

Target file:

```text
MKM_production_64_64_32_target_t60_t180.h5
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

Validated shapes for the accepted target:

```text
mean_profile:              (64, 3)
reynolds_stress_profile:   (64, 3, 3)
modal/u_hat:               (1201, 64, 32, 192)
modal/B0_DNS:              (64, 32, 192, 192)
lag_covariance/lag_0:      (64, 32, 192, 192)
lag_covariance/lag_1:      (64, 32, 192, 192)
```

The target was written with:

```text
sampling_stage_label = stationary_t60_t180
max_lag = 1
store_modal_coefficients = true
```

## Constraint file

Constraint file:

```text
MKM_constraints_N64_64_32_cheb_quadrature_spectral.h5
```

This is the solver-native Chebyshev/quadrature spectral constraint matching the
saved wall-normal grid. It was also copied beside the target as:

```text
MKM_production_64_64_32_target_t60_t180.constraints.h5
```

Saved operators:

```text
operators/D_wall
operators/B_boundary
operators/E_stream
operators/E_span
operators/E_wall
```

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

The streamwise/spanwise/wallnormal extraction matrices are component selectors
and do not differ between the Chebyshev/quadrature and uniform-grid constraint
options. The derivative and boundary interpolation operators are the parts that
change between the two options.

Rank audit for this mesh:

```text
rank 68: 1 mode
rank 70: 2047 modes
```

## Final audit

Audit report:

```text
MKM_production_64_64_32_audit_t60_t180.json
```

Key audit results:

```text
target_size_bytes = 11181644712
z_grid_match_constraint = true
z_grid_match_velocity   = true
constraint_residual_global_rel = 5.317322e-14
constraint_div_global_rel      = 5.317160e-14
constraint_bc_global_rel       = 4.155809e-16
```

These residuals confirm that the target covariance is consistent with the
saved Chebyshev/quadrature constraint to near machine precision.

## Projected covariance check

Projected covariance output:

```text
MKM_production_64_64_32_projected_covariance_t60_t180.h5
```

Diagnostics:

```text
MKM_production_64_64_32_projected_covariance_t60_t180.json
```

The projected covariance was computed by
`scripts/mkm_dns_target/project_mkm_dns_covariance.py` from `modal/B0_DNS` and
the saved Chebyshev/quadrature constraint recipe. For each horizontal mode the
script forms the row-orthonormal constraint projector

```text
P = I - Gtilde^* Gtilde
B_adm_DNS = P B0_DNS P
```

The exact-arithmetic identity is `B_adm_DNS = B0_DNS` whenever each sampled
modal coefficient satisfies the same saved constraint, because `P q = q`
sample by sample. The production residuals are therefore finite-precision
diagnostics rather than a physical correction to the target covariance.

Key diagnostics:

```text
n_modes_processed = 2048
gtilde_sources = saved_gtilde: 7, rebuilt_from_saved_operators: 2041
global_projection_rel_fro = 1.104603e-15
max_mode_projection_rel_fro = 5.654811e-15
trace_B0_total = 260.3681544959676
trace_Badm_total = 260.3681544959676
trace_projection_rel_change = 0.0
max_projected_constraint_residual = 8.898888e-17
reynolds_from_B0_rel_to_sampled = 2.942576e-15
reynolds_from_Badm_rel_to_sampled = 2.932555e-15
reynolds_from_Badm_rel_to_B0 = 2.037060e-16
max_abs_reynolds_Badm_minus_sampled = 3.819167e-14
```

The documentation figures were regenerated from the same script. In
`mkm_channel_dns_sampling_and_constraints.pdf`, Figure 8 plots the modewise
projection differences, Figure 9 draws the projected Reynolds-stress profiles
as black dashed curves with open colored markers so the exact overlap with the
sampled profiles is visible, and Figure 10 plots the profile differences
nondimensionalized by `u_tau^2`.

## Channel resolvent selected-mode proof of concept

The first real production channel-resolvent proof-of-concept run completed
using the accepted target file's stored sparse `modal/u_hat` time series. This
was a low-cost selected-mode verification, not the dense temporal CSD workflow.

Server output directory:

```text
/media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes
```

Inputs:

```text
target_h5      = /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/MKM_production_64_64_32_target_t60_t180.h5
constraint_h5  = /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/MKM_constraints_N64_64_32_cheb_quadrature_spectral.h5
csd_source     = target_modal_u_hat
segment_length = 512
window         = hann
n_segments     = 3
n_singular     = 6
```

Modes and frequencies:

```text
mode indices = (1,0), (1,1), (2,1)
omega        = 0.12271846303085827,
               0.24543692606171655,
               0.3681553890925748,
               0.4908738521234331
```

Summary table:

```text
mode   (kappa,lambda)  sigma1 over omega                         leading DNS fractions              rank-6 cumulative fractions
(1,0)  (1,0)           0.145890, 0.147973, 0.150108, 0.152295     0.108022, 0.037702, 0.123227, 0.056511  0.353601, 0.241945, 0.407893, 0.406697
(1,1)  (1,2)           0.183654, 0.186719, 0.189871, 0.193115     0.158274, 0.161356, 0.114346, 0.034472  0.387042, 0.472809, 0.490194, 0.317179
(2,1)  (2,2)           0.092078, 0.092894, 0.093722, 0.094563     0.027805, 0.059074, 0.057288, 0.053907  0.260677, 0.215853, 0.265905, 0.233041
```

Diagnostics were clean. Maximum response/forcing constraint residuals and
energy-normalization errors were all near `1e-15`; projection frequency match
error was zero for every mode. The shared CSD Parseval relative error reported
by the workflow was `2.932579e-15` for the Hann-windowed target-modal estimate.

HDF5 products were left on the server:

```text
MKM_channel_modal_csd_selected_modes.h5              906,118,744 bytes
MKM_channel_resolvent_i1_j0.h5                           223,000 bytes
MKM_channel_resolvent_i1_j1.h5                           223,000 bytes
MKM_channel_resolvent_i2_j1.h5                           223,000 bytes
MKM_channel_resolvent_projection_i1_j0.h5                 21,904 bytes
MKM_channel_resolvent_projection_i1_j1.h5                 21,904 bytes
MKM_channel_resolvent_projection_i2_j1.h5                 21,904 bytes
```

Only lightweight outputs were fetched locally:

```text
scripts/mkm_dns_target/production_reports/target_csd_selected_modes/
```

That local directory contains the fetched manifest JSON, Markdown report, and
the generated PDFs. It deliberately does not contain the production HDF5 files.

### Dense temporal CSD selected-mode run

The dense temporal selected-mode channel-resolvent workflow also completed,
using selected horizontal modes computed on the fly from the dense raw velocity
file rather than the sparse target `modal/u_hat` record.

Server output directory:

```text
/media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes_dense_csd
```

Inputs and CSD settings:

```text
dense_velocity_h5 = /media/jay/data1/shenfun_dns_runs/dense_temporal_mkm_64_64_32_t180_t300_20260703/MKM_dense_temporal_64_64_32_t180_t300_U.h5
csd_source        = raw_velocity_fft2_selected_modes
t_min, t_max      = 180, 300
dt                = 0.0005
sample_dt         = 0.01
n_times           = 12000
segment_length    = 2048
n_segments        = 10
window            = hann
n_singular        = 6
```

Modes and frequencies:

```text
mode indices = (1,0), (1,1), (2,1)
omega        = 0.30679615757740725,
               0.6135923151548145,
               0.9203884727322218,
               1.227184630309629,
               1.5339807878870364,
               1.8407769454644436
```

Summary table:

```text
mode   (kappa,lambda)  sigma1 over omega                                             leading DNS fractions                                      rank-6 cumulative fractions
(1,0)  (1,0)           0.149034, 0.154537, 0.160392, 0.166628, 0.173277, 0.180371     0.072008, 0.115051, 0.088259, 0.048182, 0.075430, 0.075190     0.293472, 0.335164, 0.324492, 0.277046, 0.293775, 0.258281
(1,1)  (1,2)           0.188284, 0.196453, 0.205236, 0.214696, 0.224903, 0.235934     0.219378, 0.147938, 0.080198, 0.081589, 0.092424, 0.107746     0.422372, 0.372225, 0.375353, 0.389396, 0.367008, 0.362858
(2,1)  (2,2)           0.093306, 0.095417, 0.097610, 0.099892, 0.102266, 0.104738     0.059642, 0.082318, 0.039605, 0.026305, 0.042329, 0.039128     0.272863, 0.356971, 0.318046, 0.258397, 0.284472, 0.310064
```

Diagnostics were again clean. Maximum response/forcing constraint residuals and
energy-normalization errors were all near `1e-15`; projection frequency match
error was zero for every mode. The dense CSD Parseval relative error reported
by the workflow was `6.166581e-15` for the Hann-windowed selected-mode raw
velocity estimate.

HDF5 products were left on the server:

```text
MKM_channel_modal_csd_selected_modes.h5            3,624,745,664 bytes
MKM_channel_resolvent_i1_j0.h5                           321,864 bytes
MKM_channel_resolvent_i1_j1.h5                           321,864 bytes
MKM_channel_resolvent_i2_j1.h5                           321,864 bytes
MKM_channel_resolvent_projection_i1_j0.h5                 25,208 bytes
MKM_channel_resolvent_projection_i1_j1.h5                 25,208 bytes
MKM_channel_resolvent_projection_i2_j1.h5                 25,208 bytes
```

Only lightweight outputs were fetched locally:

```text
scripts/mkm_dns_target/production_reports/dense_csd_selected_modes/
```

That local directory contains the fetched manifest JSON, Markdown report, and
the generated PDFs. It deliberately does not contain the dense production HDF5
files.

## Dense temporal continuation

The dense continuation restarted from a copy of the final production
`t = 180` checkpoint using a new filename prefix:

```text
prefix = MKM_dense_temporal_64_64_32_t180_t300
end_time = 300
modsave = 20
dt = 0.0005
Delta t_sample = 0.01
MPI ranks = 16
```

The run completed cleanly on 2026-07-03:

```text
final_t = 299.999999996
final_tstep = 600000
elapsed = 9942.532084 s
```

The first saved dense sample occurs after the restart checkpoint, so the dense
record is:

```text
n_snapshots = 12000
sample_time_range = 180.01 to 300
```

The dense continuation was not postprocessed into a modal covariance target.
It is used only for physical-space temporal diagnostics. For these diagnostics
the mean profile was recomputed from the dense continuation samples themselves.

Auto-covariance output:

```text
MKM_dense_temporal_64_64_32_t180_t300_velocity_autocovariance_lag2.h5
```

Datasets:

```text
autocovariance:  (201, 64, 3)  axes = lag, z, component
autocorrelation: (201, 64, 3)  axes = lag, z, component
lag_time:        (201,)        tau = 0, 0.01, ..., 2.0
```

The estimator is
`R_ii(tau_s; z) = average_{n,x,y} u_i'(t_{n+s},x,y,z) u_i'(t_n,x,y,z)`
with denominator `(N_s-s) Nx Ny`. The plotted quantity is
`R_ii(tau; z)/R_ii(0; z)`.

Auto-spectrum output:

```text
MKM_dense_temporal_64_64_32_t180_t300_velocity_autospectrum_hann.h5
```

Datasets:

```text
autospectrum: (12000, 64, 3)  axes = omega, z, component
omega:        (12000,)        two-sided angular-frequency grid
```

The estimator is the two-sided temporal periodogram at each
`(x_j,y_l,z_m)`, followed by the same `x-y` plane average. A Hann temporal
window was used for the documentation spectrum. The frequency metadata are:

```text
sample_dt = 0.01
Delta omega = 0.0523598775599
positive omega range = 0.0523598775599 to 314.106905482
Nyquist magnitude ~= 314.159265359
```

The selected-z figure plots the variance-normalized spectrum on log-log axes,
using the positive frequency branch and a dashed `omega^{-5/3}` slope reference
over `omega h/u_tau = 30` to `120`.

The selected wall-normal levels in both temporal figures are the nonsymmetric
half-channel set nearest

```text
z/h = 0, 0.5, 0.9
```

on the saved Chebyshev-Gauss grid, i.e.

```text
z/h = 0.0245412285, 0.4928981922, 0.8932243012
```

In `mkm_channel_dns_sampling_and_constraints.pdf`, Figure 6 shows the dense
auto-correlations and Figure 7 shows the dense variance-normalized
auto-spectra.

## Reproduction commands

Set common paths:

```bash
export TMPDIR=/media/jay/data1/tmp
ENV=/media/jay/data1/conda_envs/shenfun_dns_np126_20260702
REPO=/media/jay/data1/shenfun
OUT=/media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702
mkdir -p "$OUT"
cd "$OUT"
```

Spin-up/development stage:

```bash
"$ENV/bin/mpiexec" -n 16 "$ENV/bin/python" -u \
  "$REPO/scripts/mkm_dns_target/run_mkm_dns.py" \
  --output-dir "$OUT" \
  --n 64 64 32 \
  --dt 0.0005 \
  --end-time 20.0 \
  --modsave 100000000 \
  --checkpoint 100000000 \
  --moderror 2000 \
  --modplot -1 \
  --stage-label spinup \
  --disable-snapshots \
  --force-final-checkpoint \
  --skip-xdmf \
  --filename MKM_production_64_64_32
```

First sampling segment:

```bash
"$ENV/bin/mpiexec" -n 16 "$ENV/bin/python" -u \
  "$REPO/scripts/mkm_dns_target/run_mkm_dns.py" \
  --output-dir "$OUT" \
  --n 64 64 32 \
  --dt 0.0005 \
  --end-time 60.0 \
  --modsave 200 \
  --checkpoint 10000 \
  --moderror 5000 \
  --modplot -1 \
  --stage-label sampling \
  --from-checkpoint \
  --force-final-checkpoint \
  --filename MKM_production_64_64_32
```

Append sampling segments used the same command with `--end-time` advanced to
`100.0`, `140.0`, and `180.0`, plus:

```bash
--velocity-file-mode a
```

Dense temporal continuation from the final `t = 180` checkpoint:

```bash
DENSE_OUT=/media/jay/data1/shenfun_dns_runs/dense_temporal_mkm_64_64_32_t180_t300_20260703
DENSE_PREFIX=MKM_dense_temporal_64_64_32_t180_t300
mkdir -p "$DENSE_OUT"
cp "$OUT/MKM_production_64_64_32.chk.h5" "$DENSE_OUT/${DENSE_PREFIX}.chk.h5"
cd "$DENSE_OUT"

"$ENV/bin/mpiexec" -n 16 "$ENV/bin/python" -u \
  "$REPO/scripts/mkm_dns_target/run_mkm_dns.py" \
  --output-dir "$DENSE_OUT" \
  --n 64 64 32 \
  --dt 0.0005 \
  --end-time 300.0 \
  --modsave 20 \
  --checkpoint 10000 \
  --moderror 5000 \
  --modplot -1 \
  --stage-label sampling \
  --from-checkpoint \
  --force-final-checkpoint \
  --skip-xdmf \
  --filename "$DENSE_PREFIX"
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

Accepted-window field convergence check:

```bash
"$ENV/bin/python" "$REPO/scripts/mkm_dns_target/check_mkm_sampling_convergence.py" \
  --velocity-h5 "$OUT/MKM_production_64_64_32_U.h5" \
  --output "$OUT/MKM_production_64_64_32_sampling_field_convergence_t60_t180.json" \
  --dt 0.0005 \
  --t-min 60 \
  --n-blocks 12 \
  --tolerance 0.05
```

Final target postprocess:

```bash
"$ENV/bin/python" "$REPO/scripts/mkm_dns_target/postprocess_mkm_dns_target.py" \
  --velocity-h5 "$OUT/MKM_production_64_64_32_U.h5" \
  --output "$OUT/MKM_production_64_64_32_target_t60_t180.h5" \
  --dt 0.0005 \
  --t-min 60 \
  --constraint-file "$OUT/MKM_constraints_N64_64_32_cheb_quadrature_spectral.h5" \
  --sampling-stage-label stationary_t60_t180 \
  --mode-batch 4 \
  --store-modal-coefficients \
  --max-lag 1
```

Target audit:

```bash
"$ENV/bin/python" "$REPO/scripts/mkm_dns_target/audit_mkm_target.py" \
  --target-h5 "$OUT/MKM_production_64_64_32_target_t60_t180.h5" \
  --velocity-h5 "$OUT/MKM_production_64_64_32_U.h5" \
  --constraint-file "$OUT/MKM_constraints_N64_64_32_cheb_quadrature_spectral.h5" \
  --output "$OUT/MKM_production_64_64_32_audit_t60_t180.json"
```

Projected covariance check:

```bash
"$ENV/bin/python" "$REPO/scripts/mkm_dns_target/project_mkm_dns_covariance.py" \
  --target-h5 "$OUT/MKM_production_64_64_32_target_t60_t180.h5" \
  --constraint-file "$OUT/MKM_constraints_N64_64_32_cheb_quadrature_spectral.h5" \
  --output-h5 "$OUT/MKM_production_64_64_32_projected_covariance_t60_t180.h5" \
  --diagnostics-json "$OUT/MKM_production_64_64_32_projected_covariance_t60_t180.json" \
  --figure-dir "$OUT/projection_figures" \
  --friction-velocity 1.0 \
  --overwrite
```

Plane-averaged velocity auto-covariance through
`tau u_tau/h = 2.0`:

```bash
"$ENV/bin/python" "$REPO/scripts/mkm_dns_target/compute_mkm_velocity_autocovariance.py" \
  --velocity-h5 "$DENSE_OUT/${DENSE_PREFIX}_U.h5" \
  --output "$DENSE_OUT/${DENSE_PREFIX}_velocity_autocovariance_lag2.h5" \
  --dt 0.0005 \
  --t-min 180 \
  --t-max 300 \
  --max-lag 200 \
  --z-batch 2 \
  --normalize-plot \
  --max-plot-lag-time 2 \
  --selected-z 0.025 0.5 0.9 \
  --figure "$DENSE_OUT/${DENSE_PREFIX}_velocity_autocovariance_lag2_selected_z.pdf"
```

Plane-averaged velocity auto-spectrum:

```bash
"$ENV/bin/python" "$REPO/scripts/mkm_dns_target/compute_mkm_velocity_autospectrum.py" \
  --velocity-h5 "$DENSE_OUT/${DENSE_PREFIX}_U.h5" \
  --output "$DENSE_OUT/${DENSE_PREFIX}_velocity_autospectrum_hann.h5" \
  --dt 0.0005 \
  --t-min 180 \
  --t-max 300 \
  --z-batch 2 \
  --window hann \
  --log-x \
  --normalize-by-variance \
  --selected-z 0.025 0.5 0.9 \
  --reference-slope -1.6666666666666667 \
  --reference-omega-range 30 120 \
  --figure "$DENSE_OUT/${DENSE_PREFIX}_velocity_autospectrum_hann_selected_z_loglog.pdf"
```

The note figures were copied from the dense temporal outputs to:

```text
$REPO/scripts/mkm_dns_target/docs/figures/mkm_velocity_autocovariance_selected_z.pdf
$REPO/scripts/mkm_dns_target/docs/figures/mkm_velocity_autospectrum_selected_z_loglog.pdf
```

## Notes for future runs

1. Keep the two-stage separation: spin-up without snapshots, then sampling from
   an accepted checkpoint.
2. On this mesh, 16 MPI ranks is the validated production setting. Do not use
   64 ranks without changing the mesh/decomposition.
3. Use the Chebyshev/quadrature constraint as the default for solver-native
   MKM data.
4. Keep the raw velocity file and convergence reports beside the target so the
   retained sampling window can be audited later.
5. The projected covariance check is an exact-identity/roundoff audit when the
   same saved constraint is used for the sampled modal coefficients and the
   projector.
6. Keep the plane-averaged temporal diagnostic HDF5 outputs beside the raw
   velocity file when a reproduction run needs time-lag or frequency-domain
   checks.
7. If a stricter scalar-energy criterion is required, extend beyond `t = 180`
   and re-run the retained-window checks; the current target is accepted by the
   field mean/Reynolds criterion.
