# Handoff: selected-mode resolvent analysis for the 4*pi MKM channel DNS

This handoff records the selected-mode analysis associated with the long-box
production data in `HANDOFF_production_mkm_Lx4pi_64_128_32.md`.

## Geometry and mode mapping

The long-box horizontal periods and Fourier fundamentals are

```text
Lx = 4*pi       kappa_i = 0.5*i
Ly = pi         lambda_j = 2*j
```

The production analysis uses five unique mode indices:

| index `(i,j)` | physical `(kappa,lambda)` | purpose |
| --- | --- | --- |
| `(1,0)` | `(0.5,0)` | new long-box streamwise mode |
| `(1,1)` | `(0.5,2)` | new long-box oblique mode |
| `(2,0)` | `(1,0)` | matches old physical mode `(1,0)` |
| `(2,1)` | `(1,2)` | matches old physical mode `(1,1)` |
| `(4,1)` | `(2,2)` | matches old physical mode `(2,1)` |

This separates the effect of newly available low streamwise wavenumbers from
comparisons at unchanged physical wavenumber.

## CSD sources

Two selected-mode workflows were completed.

### Sparse target CSD

```text
source = accepted target modal/u_hat
sample_dt = 0.1
segment_length = 512
overlap = 0.5
window = hann
temporal demean = true
omega_count = 4
n_singular = 6
```

The first four positive bins were

```text
0.12271846303085827
0.24543692606171655
0.3681553890925748
0.4908738521234331
```

### Dense temporal CSD

```text
source = selected horizontal FFT modes from raw dense velocity
dense interval = t=200 to t=320
sample_dt = 0.01
n_times = 12000
segment_length = 2048
overlap = 0.5
window = hann
temporal demean = true
omega_count = 6
n_singular = 6
```

The first six positive bins were

```text
0.30679615757740725
0.6135923151548145
0.9203884727322218
1.227184630309629
1.5339807878870364
1.8407769454644436
```

## Outputs

Each CSD source writes one shared selected-mode CSD file and, for every mode,
one resolvent HDF5, one projection HDF5, and four PDFs:

```text
mkm_resolvent_mode_shapes.pdf
mkm_resolvent_gain_bode.pdf
mkm_resolvent_peak_location_gain.pdf
mkm_resolvent_reconstructed_fields.pdf
```

The workflow manifest and generated Markdown report must record constraint
residuals, energy-normalization errors, CSD Parseval checks, frequency-match
errors, singular values, projection fractions, and weighted Frobenius errors.

## Sparse target-CSD results

Server output:

```text
/media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200
```

The CSD used 1,401 target samples, four overlapping 512-sample Hann segments,
and had a maximum Parseval relative error of `2.933239e-15`. The shared CSD
file is 1,510,144,280 bytes.

| mode | `(kappa,lambda)` | leading gain range | max rank-1 fraction | max rank-6 fraction |
| --- | --- | --- | --- | --- |
| `(1,0)` | `(0.5,0)` | `0.255031–0.275859` | `0.130727` at `omega=0.245437` | `0.439358` at `omega=0.490874` |
| `(1,1)` | `(0.5,2)` | `0.396685–0.437435` | `0.230144` at `omega=0.122718` | `0.482374` at `omega=0.245437` |
| `(2,0)` | `(1,0)` | `0.145406–0.151780` | `0.120823` at `omega=0.122718` | `0.319133` at `omega=0.122718` |
| `(2,1)` | `(1,2)` | `0.182903–0.192309` | `0.065530` at `omega=0.122718` | `0.374398` at `omega=0.245437` |
| `(4,1)` | `(2,2)` | `0.091810–0.094282` | `0.088256` at `omega=0.245437` | `0.282100` at `omega=0.245437` |

Diagnostics:

```text
max response constraint residual = 5.245373e-15
max forcing constraint residual = 4.568309e-15
max response/forcing energy-norm error = 3.330669e-15
max projection frequency mismatch = 0
```

The new low-streamwise-wavenumber oblique mode `(1,1)`, physically
`(kappa,lambda)=(0.5,2)`, has the strongest sparse rank-1 and rank-6 alignment
among the tested modes.

## Dense temporal-CSD results

Server output:

```text
/media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200
```

The CSD used all 12,000 dense samples, ten overlapping 2,048-sample Hann
segments, and had a maximum Parseval relative error of `7.197777e-15`. The
shared CSD file is 6,040,828,608 bytes.

| mode | `(kappa,lambda)` | leading gain range | max rank-1 fraction | max rank-6 fraction |
| --- | --- | --- | --- | --- |
| `(1,0)` | `(0.5,0)` | `0.265086–0.384889` | `0.106173` at `omega=0.306796` | `0.377876` at `omega=0.920388` |
| `(1,1)` | `(0.5,2)` | `0.416239–0.665594` | `0.124887` at `omega=0.920388` | `0.512384` at `omega=0.920388` |
| `(2,0)` | `(1,0)` | `0.148534–0.179732` | `0.094548` at `omega=0.920388` | `0.349890` at `omega=1.227185` |
| `(2,1)` | `(1,2)` | `0.187506–0.234880` | `0.132310` at `omega=0.613592` | `0.402286` at `omega=0.306796` |
| `(4,1)` | `(2,2)` | `0.093032–0.104404` | `0.127032` at `omega=0.920388` | `0.361420` at `omega=0.920388` |

Diagnostics:

```text
max response constraint residual = 5.187898e-15
max forcing constraint residual = 4.881671e-15
max response/forcing energy-norm error = 3.552714e-15
max projection frequency mismatch = 0
```

The dense estimate puts the largest rank-1 fraction on physical mode
`(kappa,lambda)=(1,2)`, while the new `(0.5,2)` mode retains the largest
rank-6 fraction. The sparse and dense frequency grids differ, so their maxima
are trend comparisons rather than pointwise convergence values.

## Local lightweight archive

The workspace keeps the manifests, reports, and all generated PDFs without
duplicating the multi-gigabyte CSD files:

```text
scripts/mkm_dns_target/production_reports/longbox_Lx4pi_64_128_32/target_csd_selected_modes
scripts/mkm_dns_target/production_reports/longbox_Lx4pi_64_128_32/dense_csd_selected_modes
```
