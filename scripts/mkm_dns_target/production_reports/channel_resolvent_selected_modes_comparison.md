# Channel Resolvent Selected-Mode Production Comparison

## Purpose and Scope

This note compares the two completed production selected-mode channel-resolvent
proof-of-concept runs for the MKM `Re_tau = 180`, `N = (64,64,32)` channel DNS
target:

1. Sparse target CSD, using stored target `modal/u_hat`.
2. Dense temporal CSD, using selected horizontal modes computed from dense raw
   velocity snapshots.

Both runs use the same selected horizontal modes:

```text
(i,j) = (1,0), (1,1), (2,1)
```

The comparison is deliberately limited. It is not a full mode sweep, not a
complete frequency optimization, and not a high-Reynolds-number or long-box
VLSM scaling claim. The streamwise box is `Lx = 2*pi`, and the selected modes
should be read as low-wavenumber proof-of-concept channel modes rather than a
canonical VLSM hierarchy.

The scientific purpose is narrower but useful: verify that McKeon-style
resolvent response modes, gain curves, critical-layer overlays, and DNS CSD
projection fractions can be produced from the production DNS target and from
the dense temporal continuation, then compare the first alignment signals.

## Data and Source Comparison

| Run | DNS CSD source | Selected record | sample_dt | segment_length | n_segments | window | selected omega rule |
| --- | --- | --- | --- | --- | --- | --- | --- |
| sparse target CSD | `target_modal_u_hat` | accepted target window `t=60..180` | `0.1` | `512` | `3` | `hann` | first 4 positive CSD bins |
| dense temporal CSD | `raw_velocity_fft2_selected_modes` | dense continuation `t=180..300` | `0.01` | `2048` | `10` | `hann` | first 6 positive CSD bins |

The frequency grids differ. The sparse target run has lower first positive
bins because the segment uses `sample_dt=0.1` over 512 samples; the dense run
has finer temporal sampling but `segment_length=2048`, giving
`Delta omega = 0.30679615757740725`. Therefore the two runs should be compared
as trend and alignment checks, not as exact same-frequency comparisons.

## Sparse Target-CSD Results

Sparse omega bins:

```text
0.122718, 0.245437, 0.368155, 0.490874
```

| mode | `(kappa, lambda)` | leading singular values | leading projection fractions | rank-6 cumulative fractions |
| --- | --- | --- | --- | --- |
| `(1,0)` | `(1,0)` | `0.145890, 0.147973, 0.150108, 0.152295` | `0.108022, 0.037702, 0.123227, 0.056511` | `0.353601, 0.241945, 0.407893, 0.406697` |
| `(1,1)` | `(1,2)` | `0.183654, 0.186719, 0.189871, 0.193115` | `0.158274, 0.161356, 0.114346, 0.034472` | `0.387042, 0.472809, 0.490194, 0.317179` |
| `(2,1)` | `(2,2)` | `0.092078, 0.092894, 0.093722, 0.094563` | `0.027805, 0.059074, 0.057288, 0.053907` | `0.260677, 0.215853, 0.265905, 0.233041` |

## Dense Temporal-CSD Results

Dense omega bins:

```text
0.306796, 0.613592, 0.920388, 1.227185, 1.533981, 1.840777
```

| mode | `(kappa, lambda)` | leading singular values | leading projection fractions | rank-6 cumulative fractions |
| --- | --- | --- | --- | --- |
| `(1,0)` | `(1,0)` | `0.149034, 0.154537, 0.160392, 0.166628, 0.173277, 0.180371` | `0.072008, 0.115051, 0.088259, 0.048182, 0.075430, 0.075190` | `0.293472, 0.335164, 0.324492, 0.277046, 0.293775, 0.258281` |
| `(1,1)` | `(1,2)` | `0.188284, 0.196453, 0.205236, 0.214696, 0.224903, 0.235934` | `0.219378, 0.147938, 0.080198, 0.081589, 0.092424, 0.107746` | `0.422372, 0.372225, 0.375353, 0.389396, 0.367008, 0.362858` |
| `(2,1)` | `(2,2)` | `0.093306, 0.095417, 0.097610, 0.099892, 0.102266, 0.104738` | `0.059642, 0.082318, 0.039605, 0.026305, 0.042329, 0.039128` | `0.272863, 0.356971, 0.318046, 0.258397, 0.284472, 0.310064` |

## Cross-Run Maxima

| mode | sparse max leading fraction | dense max leading fraction | sparse max rank-6 fraction | dense max rank-6 fraction |
| --- | --- | --- | --- | --- |
| `(1,0)` | `0.123227 @ omega=0.368155` | `0.115051 @ omega=0.613592` | `0.407893 @ omega=0.368155` | `0.335164 @ omega=0.613592` |
| `(1,1)` | `0.161356 @ omega=0.245437` | `0.219378 @ omega=0.306796` | `0.490194 @ omega=0.368155` | `0.422372 @ omega=0.306796` |
| `(2,1)` | `0.059074 @ omega=0.245437` | `0.082318 @ omega=0.613592` | `0.265905 @ omega=0.368155` | `0.356971 @ omega=0.613592` |

The strongest leading-response alignment observed here is mode `(1,1)` in the
dense temporal CSD run, with leading fraction `0.219378` at
`omega=0.306796`. The strongest rank-6 cumulative fraction is also mode
`(1,1)`, but in the sparse target run, with cumulative fraction `0.490194` at
`omega=0.368155`.

## Interpretation

Across both CSD sources, `(1,1)` is the most consistently aligned with the
leading response mode and the leading six response modes. In physical
wavenumber terms this is `(kappa,lambda)=(1,2)` for the present channel box.
The dense temporal run raises the leading-mode alignment for this mode from a
sparse-run maximum of about `16%` to about `22%`, suggesting that the denser
temporal estimate and its selected frequency bins identify a DNS CSD component
more strongly aligned with the first response mode.

The rank-6 cumulative fractions are substantially larger than the rank-1
fractions. For the selected modes and frequencies, rank 6 captures roughly
`22%..49%` of the weighted DNS CSD energy in the sparse run and roughly
`26%..42%` in the dense run. This is a useful first signal: the leading mode is
informative but not exhaustive, and a finite response subspace is needed even
for these low-wavenumber proof-of-concept modes.

Low leading fractions do not invalidate the resolvent model. The McKeon-style
resolvent SVD ranks velocity responses by amplification for a given harmonic
forcing direction, but the DNS CSD also reflects the actual nonlinear forcing
statistics. A low projection fraction can arise because the forcing is not
aligned with the leading forcing mode, because more response modes are needed,
because the current Reynolds number is low, because the streamwise box is short
for VLSM-scale claims, because selected frequencies are not centered on the
most energetic CSD bands, or because finite-sample/windowed CSD estimates add
noise and smoothing.

These runs nevertheless complete the first McKeon-style DNS comparison loop
for this channel dataset. For the selected modes we now have gain curves,
response/forcing mode shapes, critical-layer overlays, reconstructed physical
fields, DNS CSD matrices, and projection fractions. That is the infrastructure
needed to ask sharper scientific questions in mode/frequency space.

## Diagnostics

The numerical diagnostics are clean in both runs:

| diagnostic | sparse target CSD | dense temporal CSD |
| --- | --- | --- |
| max CSD Parseval relative error | `2.932579e-15` | `6.166581e-15` |
| max response constraint residual | `4.889762e-15` | `4.908845e-15` |
| max forcing constraint residual | `4.712708e-15` | `4.793922e-15` |
| max response energy norm error | `2.220446e-15` | `3.774758e-15` |
| max forcing energy norm error | `3.108624e-15` | `2.886580e-15` |
| max projection frequency match error | `0` | `0` |

The Parseval entries are reported as diagnostics rather than strict
rectangular-window conservation tests because both production runs used a Hann
window with overlapping segments. Constraint residuals, normalization errors,
and frequency matching are all near roundoff.

## Limitations and Next Scientific Steps

The next scientific steps should broaden the comparison before drawing
structure or scaling conclusions:

1. Run a wider selected-mode/wavenumber sweep, including multiple streamwise
   and spanwise indices and the streamwise-constant limit handled separately.
2. Select omega bands around energetic CSD peaks instead of only the first
   positive frequency bins.
3. Compare wall-normal DNS energy-density peaks against stored critical-layer
   locations and the resolvent peak-energy diagnostics.
4. Inspect whether projection fractions improve in neighborhoods of gain peaks
   or CSD-energy peaks.
5. Add longer-box and/or higher-Reynolds-number DNS before making VLSM scaling
   claims.
6. Optionally cross-check the velocity-only admissible-subspace formulation
   against an Orr-Sommerfeld/Squire formulation.

## Local Artifacts

Sparse target-CSD artifacts:

- [summary README](target_csd_selected_modes/README.md)
- [workflow report](target_csd_selected_modes/MKM_channel_resolvent_selected_modes_report.md)
- [manifest JSON](target_csd_selected_modes/MKM_channel_resolvent_selected_modes_manifest.json)
- [mode `(1,0)` figures](target_csd_selected_modes/figures_i1_j0/)
- [mode `(1,1)` figures](target_csd_selected_modes/figures_i1_j1/)
- [mode `(2,1)` figures](target_csd_selected_modes/figures_i2_j1/)

Dense temporal-CSD artifacts:

- [summary README](dense_csd_selected_modes/README.md)
- [workflow report](dense_csd_selected_modes/MKM_channel_resolvent_selected_modes_report.md)
- [manifest JSON](dense_csd_selected_modes/MKM_channel_resolvent_selected_modes_manifest.json)
- [mode `(1,0)` figures](dense_csd_selected_modes/figures_i1_j0/)
- [mode `(1,1)` figures](dense_csd_selected_modes/figures_i1_j1/)
- [mode `(2,1)` figures](dense_csd_selected_modes/figures_i2_j1/)

Representative PDF products in each mode directory:

```text
mkm_resolvent_mode_shapes.pdf
mkm_resolvent_gain_bode.pdf
mkm_resolvent_peak_location_gain.pdf
mkm_resolvent_reconstructed_fields.pdf
```

The production HDF5 files were intentionally not fetched; they remain on the
Linux server in the corresponding production output directories.
