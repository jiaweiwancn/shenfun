# Production Dense-CSD Selected-Mode Channel Resolvent Run

This directory contains lightweight artifacts fetched from the production
selected-mode channel-resolvent workflow using the dense temporal raw velocity
file. This run used `--csd-source dense`, so selected horizontal Fourier modes
were computed on the fly from raw snapshots rather than read from the accepted
target file's stored sparse `modal/u_hat`.

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
/media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes_dense_csd
```

HDF5 products left on the server:

```text
MKM_channel_modal_csd_selected_modes.h5            3,624,745,664 bytes
MKM_channel_resolvent_i1_j0.h5                           321,864 bytes
MKM_channel_resolvent_i1_j1.h5                           321,864 bytes
MKM_channel_resolvent_i2_j1.h5                           321,864 bytes
MKM_channel_resolvent_projection_i1_j0.h5                 25,208 bytes
MKM_channel_resolvent_projection_i1_j1.h5                 25,208 bytes
MKM_channel_resolvent_projection_i2_j1.h5                 25,208 bytes
```

The server also retains `dense_workflow_run.log`, which captured the full
workflow stdout/stderr including Matplotlib font fallback messages.

## Production Command

Exact workflow command used on the server:

```bash
ssh jay@100.88.70.60 'mkdir -p /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes_dense_csd; cd /media/jay/data1/shenfun; TMPDIR=/media/jay/data1/tmp /media/jay/data1/conda_envs/shenfun_dns_np126_20260702/bin/python scripts/mkm_dns_target/run_mkm_channel_resolvent_production_selected_modes.py --target-h5 /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/MKM_production_64_64_32_target_t60_t180.h5 --constraint-file /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/MKM_constraints_N64_64_32_cheb_quadrature_spectral.h5 --dense-velocity-h5 /media/jay/data1/shenfun_dns_runs/dense_temporal_mkm_64_64_32_t180_t300_20260703/MKM_dense_temporal_64_64_32_t180_t300_U.h5 --output-dir /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes_dense_csd --csd-source dense --mode-index-list 1 0 1 1 2 1 --omega-count 6 --segment-length 2048 --overlap 0.5 --window hann --demean-temporal --dt 0.0005 --t-min 180 --t-max 300 --n-singular 6 --make-figures --no-tex --overwrite'
```

Report regeneration command:

```bash
ssh jay@100.88.70.60 'cd /media/jay/data1/shenfun && /media/jay/data1/conda_envs/shenfun_dns_np126_20260702/bin/python scripts/mkm_dns_target/report_mkm_channel_resolvent_workflow.py --manifest /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes_dense_csd/MKM_channel_resolvent_selected_modes_manifest.json'
```

## Key Results

The dense CSD was computed from `raw_velocity_fft2_selected_modes` with
`n_times = 12000`, `sample_dt = 0.01`, `segment_length = 2048`,
`n_segments = 10`, and `window = hann`.

All modes used the same first six positive dense-CSD bins:

```text
omega = 0.30679615757740725,
        0.6135923151548145,
        0.9203884727322218,
        1.227184630309629,
        1.5339807878870364,
        1.8407769454644436
```

| mode | `(kappa, lambda)` | leading singular values | leading DNS fractions | rank-6 cumulative fractions |
| --- | --- | --- | --- | --- |
| `(1,0)` | `(1,0)` | `0.149034, 0.154537, 0.160392, 0.166628, 0.173277, 0.180371` | `0.072008, 0.115051, 0.088259, 0.048182, 0.075430, 0.075190` | `0.293472, 0.335164, 0.324492, 0.277046, 0.293775, 0.258281` |
| `(1,1)` | `(1,2)` | `0.188284, 0.196453, 0.205236, 0.214696, 0.224903, 0.235934` | `0.219378, 0.147938, 0.080198, 0.081589, 0.092424, 0.107746` | `0.422372, 0.372225, 0.375353, 0.389396, 0.367008, 0.362858` |
| `(2,1)` | `(2,2)` | `0.093306, 0.095417, 0.097610, 0.099892, 0.102266, 0.104738` | `0.059642, 0.082318, 0.039605, 0.026305, 0.042329, 0.039128` | `0.272863, 0.356971, 0.318046, 0.258397, 0.284472, 0.310064` |

Diagnostics were clean: response and forcing constraint residuals,
energy-normalization errors, and frequency-match errors all passed the report
thresholds. The maximum dense CSD Parseval relative error was
`6.166581e-15`; because `window = hann`, this is reported as a windowed
estimator diagnostic.

## Notes

Projection fractions measure DNS CSD alignment with the stored resolvent
response subspace. They do not model forcing statistics by themselves. The
dense run has finer temporal sampling than the sparse target-modal run, but
with `segment_length = 2048` its frequency spacing is
`Delta omega = 0.30679615757740725`, so the first selected positive bins are
higher than the sparse target-modal run's first four bins.
