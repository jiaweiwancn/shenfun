# Handoff: long-box MKM channel-flow DNS, N=(64,128,32), Lx=4*pi

This handoff records the long-box MKM channel-flow production workflow run on
the Linux server in July 2026. Solver-order mesh dimensions are wall-normal,
streamwise, and spanwise.

## Server environment

```text
server = jay@100.88.70.60
repository = /media/jay/data1/shenfun
environment = /media/jay/data1/conda_envs/shenfun_dns_np126_20260702
temporary directory = /media/jay/data1/tmp
```

Production output:

```text
/media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713
```

Run-specific drivers are archived in that directory:

```text
run_mkm_longbox_sampling_20260713.sh
analyze_mkm_longbox_sparse_20260713.sh
postprocess_mkm_longbox_target_20260713.sh
run_mkm_longbox_dense_20260713.sh
run_mkm_longbox_resolvent_20260713.sh
continue_mkm_longbox_after_convergence_20260713.sh
```

They are fail-fast and keep sparse and dense velocity files in separate
directories. Workspace copies are under
`production_reports/longbox_Lx4pi_64_128_32/run_scripts`.

## Long-box configuration

```text
N = (64,128,32) in solver order
domain = ((-1,1),(0,4*pi),(0,pi))
Re_tau = 180
dt = 0.0005
conv = 0
family = C
padding_factor = (1.5,1.5,1.5)
timestepper = IMEXRK222
saved mesh = quadrature
MPI ranks = 32
bulk velocity = 15.678693259774453
integrated flux target = 1237.94
```

Doubling both `Lx` and `Nx` preserves the streamwise physical spacing:

```text
4*pi/128 = 2*pi/64 = 0.09817477042468103
```

The streamwise Fourier fundamental is therefore `kappa_1=0.5`; the spanwise
fundamental remains `lambda_1=2`.

## Required solver-runner corrections

The historical MKM demo stored `618.97` as a box-integrated flux. Reusing that
number in the doubled box would halve the bulk velocity. The runner now passes
a box-independent bulk-velocity target, and `MKM` sets

```text
integrated_flux = bulk_velocity * domain_volume.
```

The historical streamwise initialization used the Fourier-domain endpoint to
set `alfaplus`. That would change the intended perturbation wavelength when
`Lx` changes. The initialization now uses `alfaplus=2*pi/200`, which preserves
the old `Lx=2*pi` behavior and makes the wavelength box independent.

Pre-change server copies were retained under `/media/jay/data1/tmp`.

## MPI pilot

Separate two-stage pilots were run with 16 and 32 ranks. Each advanced from
`t=0` to `0.1`, forced a checkpoint, restarted, and wrote samples through
`t=0.11`.

```text
16-rank spin-up elapsed = 10.439834 s
32-rank spin-up elapsed = 8.969231 s
16-rank restart elapsed = 1.299639 s
32-rank restart elapsed = 0.988707 s
maximum 16/32 snapshot difference = 8.260059303211165e-14
snapshot shape per component = (64,128,32)
```

Both decompositions were valid. The 32-rank layout was selected for production.

## Spin-up acceptance

The fresh spin-up first ran from `t=0` to `t=20` without snapshots. Its
`t=10` to `t=20` scalar check narrowly missed the five-percent threshold due
to wall-normal energy:

```text
max first/last monitored drift = 0.055548370648996793
max successive monitored drift = 0.048827355393965474
max divergence = 3.310905e-14
```

Spin-up was therefore extended without snapshots to `t=40`. The accepted
late window `t=30` to `t=40` gave:

```text
max first/last monitored drift = 0.016965992174834504
max successive monitored drift = 0.065470045074961
stationary_by_tolerance = true
checkpoint t = 40.00000000000897
checkpoint tstep = 80000
checkpoint size = 6.4 MB
```

The `t=40` checkpoint is the initial condition for sparse stationary
sampling.

## Sparse stationary sampling

Snapshots are written every 200 DNS steps:

```text
Delta t_sample = 200 * 0.0005 = 0.1
```

The sparse record is collected in four checkpointed segments:

```text
t=40  to 80    create velocity file
t=80  to 120   append
t=120 to 160   append
t=160 to 200   append
```

Completed segment solve times include:

```text
t=40  to 80  elapsed = 3032.884736 s
t=80  to 120 elapsed = 2981.820566 s
t=120 to 160 elapsed = 2928.128398 s
t=160 to 200 elapsed = 3228.277436 s
```

The completed full sparse record is `t=40.1` through `t=200`, with 1,600
snapshots. Candidate retained windows are checked with 12 blocks and a
five-percent mean/Reynolds-profile tolerance:

```text
full record = t=40.1 to 200
trimmed = t=60 to 200
primary candidate = t=80 to 200
```

Results:

| window | snapshots | max mean block rel. | max Reynolds block rel. | pass |
| --- | ---: | ---: | ---: | --- |
| `40.1 to 200` | 1600 | `5.165358e-03` | `5.065722e-02` | no |
| `60 to 200` | 1401 | `4.026336e-03` | `2.925941e-02` | yes |
| `80 to 200` | 1201 | `3.941224e-03` | `3.449893e-02` | yes |

The accepted target uses the earliest passing window, `t=60` to `t=200`,
with 1,401 snapshots. Its first/second-half changes are

```text
mean profile = 1.667416900191372e-03
Reynolds profile = 1.2028430111593633e-02
```

The 64-record scalar diagnostic over `t=42.5` to `t=200` also passes:

```text
max first/last monitored change = 2.3061555519371734e-02
max successive monitored change = 4.554951271847882e-02
max divergence = 3.433901e-14
stationary_by_tolerance = true
```

The final sparse velocity file is 9.4 GB. Its component groups have identical
1,600-key records, from step 80200 through step 400000, and every snapshot has
shape `(64,128,32)`.

## Constraint file

```text
MKM_constraints_Lx4pi_N64_128_32_cheb_quadrature_spectral.h5
size = 4564536 bytes
rank 68 = 1 mode
rank 70 = 4095 modes
```

The saved grid shapes are `(64,128,32)` in wall/stream/span order, with
`k_stream[:6] = [0,0.5,1,1.5,2,2.5]` and
`k_span[:4] = [0,2,4,6]`.

## Accepted target and audits

Accepted target:

```text
MKM_production_Lx4pi_64_128_32_target_t60_t200.h5
size = 24880260208 bytes
sampling_stage_label = stationary_t60_t200
```

Validated shapes:

```text
mean_profile = (64,3)
reynolds_stress_profile = (64,3,3)
modal/u_hat = (1401,128,32,192)
modal/B0_DNS = (128,32,192,192)
lag_covariance/lag_0 = (128,32,192,192)
lag_covariance/lag_1 = (128,32,192,192)
```

Target audit:

```text
z_grid_match_constraint = true
z_grid_match_velocity = true
constraint_residual_global_rel = 5.479612e-14
constraint_div_global_rel = 5.479488e-14
constraint_bc_global_rel = 3.680447e-16
```

Projected covariance diagnostics for all 4,096 modes:

```text
saved Gtilde = 7 modes
rebuilt Gtilde = 4089 modes
global projection relative Frobenius change = 1.096656319042733e-15
maximum modewise relative change = 2.1536693937487627e-15
trace B0 = 257.4582474840727
trace Badm = 257.4582474840726
relative trace change = -2.2078694085853497e-16
maximum projected constraint residual = 5.418214520756198e-17
Reynolds Badm relative to sampled = 2.4532169171503096e-15
maximum absolute Reynolds difference = 2.930988785010413e-14
```

The explicit projection is therefore a finite-precision identity check, as in
the earlier production target.

## Dense temporal continuation

The dense record is deliberately separate from the sparse equal-time target
record. It restarts from a copy of the final `t=200` checkpoint:

```text
output = /media/jay/data1/shenfun_dns_runs/dense_temporal_mkm_Lx4pi_64_128_32_t200_t320_20260713
prefix = MKM_dense_temporal_Lx4pi_64_128_32_t200_t320
interval = t=200 to 320
modsave = 20
Delta t_sample = 0.01
snapshots = 12000
MPI ranks = 32
```

The driver validates `checkpoint t=200` and `tstep=400000` before copying it.
The continuation completed without a restart:

```text
solve elapsed = 9700.196844 s
snapshot keys = 400020 through 640000
snapshot times = 200.01 through 320.00
snapshot shape per component = (64,128,32)
velocity file size = 75523367624 bytes
final checkpoint t = 319.99999999588897
final checkpoint tstep = 640000
final divergence = 3.512154e-14
```

After DNS collection it computes the plane-averaged velocity autocovariance
through `tau=2` and the Hann-windowed velocity autospectrum at selected
wall-normal levels near `z/h=0`, `0.5`, and `0.9`.

Completed temporal products:

```text
MKM_dense_temporal_Lx4pi_64_128_32_t200_t320_velocity_autocovariance_lag2.h5
  size = 1214352 bytes
  autocovariance shape = (201,64,3)
  autocorrelation shape = (201,64,3)
  lag range and spacing = 0 to 2 by 0.01

MKM_dense_temporal_Lx4pi_64_128_32_t200_t320_velocity_autospectrum_hann.h5
  size = 19121664 bytes
  autospectrum shape = (12000,64,3)
  omega range = -314.159265359265 to 314.10690548170516
  Delta omega = 0.052359877559872814
```

The two products have identical 12,000-sample time grids and identical
wall-normal grids. All covariance, correlation, and spectral values are
finite; the spectrum is nonnegative; and the stored lag-zero autocorrelation
differs from one by zero in double precision.

The server pipeline then completed the dense selected-mode resolvent analysis.
Its settings and results are recorded in
`HANDOFF_channel_resolvent_analysis_Lx4pi_64_128_32.md`.
