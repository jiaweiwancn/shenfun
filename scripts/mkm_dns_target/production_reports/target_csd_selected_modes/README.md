# Production Target-CSD Selected-Mode Channel Resolvent Run

This directory contains lightweight artifacts fetched from the first real
production selected-mode channel-resolvent workflow. The run used the accepted
production target file's stored sparse `modal/u_hat` record, not the dense raw
velocity snapshots.

## Local Artifacts

Fetched locally:

```text
MKM_channel_resolvent_selected_modes_manifest.json
MKM_channel_resolvent_selected_modes_report.md
figures_i1_j0/mkm_resolvent_gain_bode.pdf
figures_i1_j0/mkm_resolvent_mode_shapes.pdf
figures_i1_j0/mkm_resolvent_peak_location_gain.pdf
figures_i1_j0/mkm_resolvent_reconstructed_fields.pdf
figures_i1_j1/mkm_resolvent_gain_bode.pdf
figures_i1_j1/mkm_resolvent_mode_shapes.pdf
figures_i1_j1/mkm_resolvent_peak_location_gain.pdf
figures_i1_j1/mkm_resolvent_reconstructed_fields.pdf
figures_i2_j1/mkm_resolvent_gain_bode.pdf
figures_i2_j1/mkm_resolvent_mode_shapes.pdf
figures_i2_j1/mkm_resolvent_peak_location_gain.pdf
figures_i2_j1/mkm_resolvent_reconstructed_fields.pdf
```

No production HDF5 files were fetched.

## Server Outputs

Server output directory:

```text
/media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes
```

HDF5 products left on the server:

```text
MKM_channel_modal_csd_selected_modes.h5              906,118,744 bytes
MKM_channel_resolvent_i1_j0.h5                           223,000 bytes
MKM_channel_resolvent_i1_j1.h5                           223,000 bytes
MKM_channel_resolvent_i2_j1.h5                           223,000 bytes
MKM_channel_resolvent_projection_i1_j0.h5                 21,904 bytes
MKM_channel_resolvent_projection_i1_j1.h5                 21,904 bytes
MKM_channel_resolvent_projection_i2_j1.h5                 21,904 bytes
```

## Production Command

Exact workflow command used on the server:

```bash
ssh jay@100.88.70.60 'cd /media/jay/data1/shenfun && TMPDIR=/media/jay/data1/tmp /media/jay/data1/conda_envs/shenfun_dns_np126_20260702/bin/python scripts/mkm_dns_target/run_mkm_channel_resolvent_production_selected_modes.py --target-h5 /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/MKM_production_64_64_32_target_t60_t180.h5 --constraint-file /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/MKM_constraints_N64_64_32_cheb_quadrature_spectral.h5 --dense-velocity-h5 /media/jay/data1/shenfun_dns_runs/dense_temporal_mkm_64_64_32_t180_t300_20260703/MKM_dense_temporal_64_64_32_t180_t300_U.h5 --output-dir /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes --csd-source target --mode-index-list 1 0 1 1 2 1 --omega-count 4 --segment-length 512 --window hann --demean-temporal --n-singular 6 --make-figures --no-tex --overwrite'
```

Report regeneration command:

```bash
ssh jay@100.88.70.60 'cd /media/jay/data1/shenfun && /media/jay/data1/conda_envs/shenfun_dns_np126_20260702/bin/python scripts/mkm_dns_target/report_mkm_channel_resolvent_workflow.py --manifest /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes/MKM_channel_resolvent_selected_modes_manifest.json'
```

## Key Results

All modes used the same four positive low-frequency target-CSD bins:

```text
omega = 0.12271846303085827,
        0.24543692606171655,
        0.3681553890925748,
        0.4908738521234331
```

| mode | `(kappa, lambda)` | leading singular values | leading DNS fractions | rank-6 cumulative fractions |
| --- | --- | --- | --- | --- |
| `(1,0)` | `(1,0)` | `0.145890, 0.147973, 0.150108, 0.152295` | `0.108022, 0.037702, 0.123227, 0.056511` | `0.353601, 0.241945, 0.407893, 0.406697` |
| `(1,1)` | `(1,2)` | `0.183654, 0.186719, 0.189871, 0.193115` | `0.158274, 0.161356, 0.114346, 0.034472` | `0.387042, 0.472809, 0.490194, 0.317179` |
| `(2,1)` | `(2,2)` | `0.092078, 0.092894, 0.093722, 0.094563` | `0.027805, 0.059074, 0.057288, 0.053907` | `0.260677, 0.215853, 0.265905, 0.233041` |

Diagnostics were clean: response and forcing constraint residuals,
energy-normalization errors, and frequency-match errors all passed the report
thresholds. The shared CSD was estimated from `target_modal_u_hat` with
`sample_dt = 0.1`, `segment_length = 512`, `n_segments = 3`, `window = hann`,
and maximum Parseval relative error `2.932579e-15`.

## Notes

Projection fractions measure DNS CSD alignment with the stored resolvent
response subspace. They do not model forcing statistics by themselves. This is
a selected-mode proof of concept from the sparse target record; the dense
temporal CSD workflow remains the next production verification step.
