# All-plane temporal sampling remedy for Re_tau = 395

## Material Passport

- Origin Skill: experiment-agent
- Origin Mode: plan
- Origin Date: 2026-07-27
- Verification Status: CentOS full-shape state/I/O verified; refined-step production gate pending
- Version Label: all_plane_state_plan_v5

## Decision

Temporal auto-correlations and auto-spectra are required at every one of the
192 saved wall-normal levels. Therefore the earlier selected-plane proposal is
withdrawn.

During the accepted stationary stage, sample the complete independent MKM
spectral state every

```text
Delta t_temporal = 0.005 outer time units
```

and reconstruct all three physical velocity components on all horizontal
planes during postprocessing. The record must use complex128/float64 and
lossless compression only. It must not use wall-normal subsampling, horizontal
mode truncation, reduced precision, or lossy compression.

The writer and decoder have passed both a 20-sample, 18-plane, four-rank
round trip and a one-sample, 192-plane, 64-rank full-shape round trip on the
Ubuntu test server, followed by the corresponding CentOS small/full-shape
gates, with independent NaN/Inf scans. A reduced spin-up plus two sampling
segments also passed checkpoint restart, HDF5 append, state-shard continuity,
and exact reconstruction for eight samples. Production sampling remains gated
by the refined-step stability pilot, a longer cadence/dual-write study, and
physical stationarity acceptance. `lag_0` and `lag_1` are omitted.

The v5 refined-step cadence was rechecked on Ubuntu with 200 reduced-grid DNS
steps and 20 retained samples. All reconstructed velocity values matched the
conventional record exactly, the state finite-value audit passed, and the
sample interval remained exactly `0.005`.

## Why the independent state is sufficient

In `demo/ChannelFlow.py`, the KMM formulation advances:

```text
u_wall_hat  = solver.u_[0]   # wall-normal velocity, TB space
eta_hat     = solver.g_      # wall-normal vorticity, TD space
```

Let `D_wall` be the same wall-normal spectral derivative/projector used by the
solver, and let `(k_stream,k_span)` be a nonzero horizontal wavenumber pair.
The solver reconstructs the other two velocity coefficients from
`D_wall(u_wall_hat)`, `eta_hat`, and incompressibility:

```text
u_stream_hat = i*(k_stream*D_wall(u_wall_hat)
                  + k_span*eta_hat)/(k_stream^2+k_span^2)

u_span_hat   = i*(k_span*D_wall(u_wall_hat)
                  - k_stream*eta_hat)/(k_stream^2+k_span^2)
```

The two `(k_stream,k_span)=(0,0)` profiles are evolved separately and must also
be saved:

```text
u_stream_hat[:,0,0]
u_span_hat[:,0,0]
```

Thus the exact analysis record per sampling time is:

1. all coefficients of `u_wall_hat`;
2. all coefficients of `eta_hat`;
3. the streamwise zero-horizontal-mode profile;
4. the spanwise zero-horizontal-mode profile; and
5. exact time, DNS step, and reconstruction metadata.

After restoring these arrays, the decoder uses the solver's own projection,
wavenumber, zero-mode insertion, and backward-transform paths. The resulting
physical velocity contains all three components on all 192 horizontal planes.
The real-to-complex Fourier layout already stores only the nonredundant
spanwise half-spectrum.

The analysis record is not a restart checkpoint: the usual checkpoints remain
responsible for the complete time-integrator state.

## Desired outputs retained

The reconstructed velocity record is sufficient for all of the following at
every saved wall-normal level:

- horizontal/time mean profiles;
- all Reynolds-stress profiles;
- plane-averaged temporal auto-covariance and auto-correlation functions;
- plane-averaged temporal auto-spectra for all three components;
- horizontal Fourier modal time series, CSDs, and resolvent projections;
- equal-time modal covariance `B0_DNS`, if explicitly requested; and
- arbitrary later selection of horizontal planes or horizontal modes.

The existing temporal estimators can be preserved: decode the samples in the
same time order and feed reconstructed float64 planes to the existing
autocovariance and autospectrum calculations. The remedy changes the
persistent representation, not the sample times or estimator definitions.

For processing memory, reconstruct one sampling time at a time and fill a
temporary time-by-horizontal-grid array for a small wall-normal batch. Apply
the current temporal FFT/correlation calculation to that batch, write the
result, release the batch, and continue. This avoids creating a second
permanent dense-velocity archive. A larger server-side scratch cache may be
used for speed, but it is disposable and is not part of the retained data.

## Sampling length and cadence

The fixed stationary target is:

```text
sampling start                     t=120
sampling end                       t=300
stationary duration                180 outer time units
refined DNS time step candidate       0.00005
temporal sample spacing             0.005
DNS steps per temporal sample       100
temporal sample spacing in wall time 1.975
number of temporal samples          36,000
Nyquist angular frequency           628.319 u_tau/h
sampling start DNS step             2,400,000
sampling end DNS step               6,000,000
stationary DNS steps                3,600,000
```

The former `dt=0.00025` full-resolution pilot is rejected: its CFL exceeded
one, reached approximately 1.6, and the solution became non-finite by
`t=0.9`. Sampling is accepted in convergence-tested append segments. A short
cadence pilot first writes the same state every 50 DNS steps
(`Delta t_temporal=0.0025`) and compares spectra/correlations with the record
decimated to 0.005. Retain 0.005 only if the comparison shows that it resolves
the frequency band of interest; otherwise the production cost doubles.

For the 36,000-sample record, a Hann/Welch estimate with 8,192-sample segments
and 50 percent overlap has segment duration 40.96 and angular-frequency
spacing about 0.1534. A full-record diagnostic periodogram has angular-
frequency spacing about 0.03491. The exact realized times, not nominal indices
alone, must be stored and checked for uniformity.

## Storage calculation

For `(N_wall,N_stream,N_span)=(192,256,192)`, a real physical velocity sample
contains

```text
3*192*256*192 float64 values
  = 226,492,416 bytes
  = 0.210938 GiB
```

The nonredundant real-to-complex spectral extent is
`192*256*(192/2+1)`. Saving two complex128 state arrays plus the two zero-mode
profiles contains

```text
2*192*256*97 complex128 values + 2*192 float64 values
  = 152,570,880 bytes
  = 0.142093 GiB per sample
```

The uncompressed stationary budgets are therefore:

```text
object                                      uncompressed retained size
36,000 dense physical velocity samples      7.4158 TiB
36,000 independent spectral-state samples   4.9954 TiB
18 complete audit velocity fields            3.797 GiB
full equal-time B0_DNS, if retained       about 243 GiB
```

The exact state saves about 32.64 percent relative to storing all three dense
physical components. It still provides all horizontal planes.

Use appendable shards of 1,000 samples, corresponding to five outer time units
at the proposed cadence. Each shard is about 142.09 GiB before compression.
This limits failure scope, makes checksums manageable, and permits completed
shards to become read-only while the next is written.

The TB and TD composite bases may contain fixed inactive tail coefficients.
Packing those coefficients is allowed only after the smoke test proves their
indices are invariant and identically zero for every MPI layout. The possible
extra saving is small and is not included in the budget.

## Lossless storage policy

Apply only representation-preserving reductions:

1. use the solver-native real-to-complex half-spectrum;
2. store only the two independent state variables and two required zero modes;
3. use HDF5 chunking suitable for one-time-sample reads;
4. benchmark `shuffle+gzip` and an available lossless Zstandard/bitshuffle
   filter on a real pilot record;
5. record filter names and versions, and verify checksums after decompression;
6. retain dense audit velocity fields only every 10 outer time units and at
   the final accepted state; and
7. store no spin-up temporal record.

Compression ratios for turbulent floating-point coefficients are not assumed.
Capacity approval uses the 5.00 TiB uncompressed state budget, plus checkpoint,
audit, derived-output, temporary-file, and safety headroom. Float32,
quantization, scale-offset filters, spectral truncation, or decimation below
the accepted cadence require a separate error study and are not the baseline.

## Proposed HDF5 schema

Each shard uses a self-describing schema such as:

```text
MKM_Re395_state_00000_00999.h5
  sampling/t                         # time
  sampling/tstep                     # integer DNS step
  state/u_wall_hat                   # time, wall_coeff, k_stream, k_span_r2c
  state/eta_wall_hat                 # time, wall_coeff, k_stream, k_span_r2c
  state/u_stream_zero_mode           # time, wall_coeff
  state/u_span_zero_mode             # time, wall_coeff
  geometry/wall_quadrature
  geometry/k_stream
  geometry/k_span_r2c
  metadata/global_shape
  metadata/local_slices
  metadata/component_order
  metadata/basis_TB
  metadata/basis_TD
  metadata/fft_normalization
  metadata/complex_layout
  metadata/dtype
  metadata/run_uuid
  metadata/source_checkpoint
  metadata/code_revision
  metadata/lossless_filter
```

The production writer must use collective or rank-safe parallel I/O and store
global array ordering. A shard is complete only after all datasets, sample
counts, and a manifest checksum are committed. Never make correctness depend
on an unstated MPI decomposition.

Derived products are separate:

```text
MKM_Re395_block_statistics.h5
MKM_Re395_temporal_autocovariance_all_planes.h5
MKM_Re395_temporal_autospectrum_all_planes.h5
MKM_Re395_selected_mode_csd.h5
MKM_Re395_B0_DNS.h5                         # optional
```

Online block sums for means and Reynolds stresses should still be kept. They
are cheap and provide an independent convergence and reconstruction audit, but
they do not replace the all-plane temporal state record.

## Mandatory round-trip validation

Before production, run at least 512 temporal samples while writing both the
ordinary dense velocity fields and the proposed state shards:

1. Reconstruct the three velocity components from the state record using the
   same solver code paths.
2. Compare every reconstructed coefficient and quadrature velocity with the
   conventional output, including the `(0,0)` horizontal mode.
3. Require exact agreement where the I/O path is bitwise identical; otherwise
   require a documented roundoff-level absolute and relative tolerance.
4. Compute mean profiles, all Reynolds stresses, all-plane temporal
   auto-correlations, and all-plane auto-spectra from both records.
5. Require estimator differences to remain within the tolerance implied by
   summation/FFT ordering, with no wall-normal plane excluded.
6. Restart the decoder under at least two MPI decompositions and require the
   same global results.
7. Exercise shard interruption, manifest recovery, checksum validation, and
   a complete lossless decompression round trip.
8. Measure write throughput and verify that writing every 100 DNS steps does
   not materially perturb the solver's time-to-solution.

Retain the validation report. Delete the temporary dense pilot record only
after the comparison has passed and the user has accepted the report.

## Go/no-go storage gate

Before the stationary stage, the new server must have:

```text
at least 5.00 TiB  independent state, uncompressed
plus checkpoints and 18 audit fields
plus optional 0.24 TiB if full B0_DNS is retained
plus derived temporal products
plus temporary postprocessing scratch
plus operational safety headroom
```

A practical allocation target is at least 7 TiB for the baseline record and
derived outputs, excluding any large disposable reconstruction cache. The
actual requirement must be revised from the measured pilot compression ratio,
checkpoint size, spectrum/correlation output shape, and scratch strategy.

## Limitation and fallback

This remedy is exact only after the mandatory round-trip validates the
solver-state reconstruction and I/O ordering. If that gate fails, the safe
fallback is to store all three full physical velocity components at every
accepted temporal sample, requiring about 7.42 TiB uncompressed for the
180-time-unit window. Reducing the wall-normal planes is not an allowed
fallback.
