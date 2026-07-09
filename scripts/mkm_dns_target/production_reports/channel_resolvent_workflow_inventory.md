# Channel Resolvent Workflow Inventory

This inventory summarizes the implemented selected-mode channel-resolvent
proof-of-concept workflow and the production report artifacts currently
available locally. It is a review aid, not a new analysis result.

## Implemented Scripts

Core utilities and solver:

- `mkm_channel_resolvent_utils.py`: shared HDF5 loading, constraint rebuild,
  Chebyshev-Gauss quadrature weights, level-major velocity energy weights,
  admissible energy-orthonormal bases, raw velocity operator assembly, modal
  energy diagnostics, and critical-layer interpolation.
- `compute_mkm_channel_resolvent.py`: single-horizontal-mode channel
  resolvent CLI and callable implementation. It writes singular values,
  physical response/forcing modes, energy diagnostics, critical layers, and
  numerical diagnostics.
- `plot_mkm_channel_resolvent.py`: first plotting layer for existing
  single-mode resolvent HDF5 files: mode shapes, gain curves, peak energy with
  critical layers, and reconstructed physical fields.
- `compute_mkm_modal_csd.py`: selected-mode temporal DNS CSD estimator from
  either target `modal/u_hat` or raw velocity snapshots with selected
  horizontal FFT modes computed on the fly.
- `project_mkm_dns_onto_resolvent.py`: projection of selected-mode DNS CSD
  onto stored resolvent response modes, including leading and cumulative
  captured energy fractions.

Workflow, production wrappers, and reports:

- `run_mkm_channel_resolvent_selected_modes.py`: selected-mode orchestration
  driver that composes CSD, single-mode resolvent, projection, plotting, and a
  manifest JSON.
- `run_mkm_channel_resolvent_production_smoke.py`: small production-file smoke
  wrapper for the single-mode resolvent.
- `run_mkm_channel_resolvent_production_selected_modes.py`: production wrapper
  around the selected-mode workflow with `/media/jay/data1` defaults, clean
  missing-file handling, dry-run output, and an SSH command printer.
- `report_mkm_channel_resolvent_workflow.py`: Markdown report generator from
  a selected-mode workflow manifest and its generated HDF5/PDF outputs.
- `run_channel_resolvent_smoke_suite.py`: consolidated local smoke-test runner
  for the implemented proof-of-concept workflow.

## Smoke Tests

- `smoke_channel_resolvent_utils.py`: utility-layer nullspace, quadrature,
  energy basis, and critical-layer checks.
- `smoke_channel_resolvent_single_mode.py`: synthetic single-mode resolvent
  solve and HDF5 schema checks.
- `smoke_channel_resolvent_plot.py`: synthetic plotting smoke that verifies
  expected PDFs are created.
- `smoke_modal_csd.py`: synthetic selected-mode CSD estimator check, including
  Parseval behavior for a rectangular full segment.
- `smoke_project_dns_onto_resolvent.py`: synthetic aligned-CSD projection
  check where leading response-mode capture is near unity.
- `smoke_selected_modes_workflow.py`: synthetic end-to-end selected-mode
  workflow over two modes, including CSD, resolvent, projection, plotting, and
  manifest checks.
- `smoke_production_selected_modes_wrapper.py`: dry-run and missing-file
  checks for the production wrapper without requiring production HDF5 files.
- `smoke_workflow_report.py`: synthetic selected-mode workflow report
  generation check.

Exact local smoke-suite command:

```bash
/opt/anaconda3/bin/python scripts/mkm_dns_target/run_channel_resolvent_smoke_suite.py --json-summary /private/tmp/mkm_channel_resolvent_smoke_suite_final_review.json
```

## Local Production Reports

Sparse target-CSD selected-mode run:

- Directory: `scripts/mkm_dns_target/production_reports/target_csd_selected_modes/`
- Source: stored target `modal/u_hat`
- Modes: `(1,0)`, `(1,1)`, `(2,1)`
- Omega bins: `0.12271846303085827`, `0.24543692606171655`,
  `0.3681553890925748`, `0.4908738521234331`
- Key files fetched locally: manifest JSON, Markdown report, and four PDFs per
  mode. No production HDF5 files were fetched.

Dense temporal-CSD selected-mode run:

- Directory: `scripts/mkm_dns_target/production_reports/dense_csd_selected_modes/`
- Source: selected horizontal modes computed from dense raw velocity snapshots
- Modes: `(1,0)`, `(1,1)`, `(2,1)`
- Omega bins: `0.30679615757740725`, `0.6135923151548145`,
  `0.9203884727322218`, `1.227184630309629`, `1.5339807878870364`,
  `1.8407769454644436`
- Key files fetched locally: manifest JSON, Markdown report, and four PDFs per
  mode. No production HDF5 files were fetched.

Comparison note:

- `scripts/mkm_dns_target/production_reports/channel_resolvent_selected_modes_comparison.md`
- Summary: `(1,1)` showed the strongest leading response-mode alignment in
  both runs; dense temporal CSD raised its leading fraction from about `0.16`
  to about `0.22`. Rank 6 captured about `0.22` to `0.49` of the sparse
  target-CSD energy and about `0.26` to `0.42` of the dense temporal-CSD
  energy across these selected modes and low-frequency bins.

## Server-Side HDF5 Outputs

Sparse target-CSD run output directory:

```text
/media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes
```

HDF5 files left on the server:

- `MKM_channel_modal_csd_selected_modes.h5`: `906,118,744` bytes
- `MKM_channel_resolvent_i1_j0.h5`: `223,000` bytes
- `MKM_channel_resolvent_i1_j1.h5`: `223,000` bytes
- `MKM_channel_resolvent_i2_j1.h5`: `223,000` bytes
- `MKM_channel_resolvent_projection_i1_j0.h5`: `21,904` bytes
- `MKM_channel_resolvent_projection_i1_j1.h5`: `21,904` bytes
- `MKM_channel_resolvent_projection_i2_j1.h5`: `21,904` bytes

Dense temporal-CSD run output directory:

```text
/media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes_dense_csd
```

HDF5 files left on the server:

- `MKM_channel_modal_csd_selected_modes.h5`: `3,624,745,664` bytes
- `MKM_channel_resolvent_i1_j0.h5`: `321,864` bytes
- `MKM_channel_resolvent_i1_j1.h5`: `321,864` bytes
- `MKM_channel_resolvent_i2_j1.h5`: `321,864` bytes
- `MKM_channel_resolvent_projection_i1_j0.h5`: `25,208` bytes
- `MKM_channel_resolvent_projection_i1_j1.h5`: `25,208` bytes
- `MKM_channel_resolvent_projection_i2_j1.h5`: `25,208` bytes

## Recommended Production Rerun Commands

Sparse target-CSD selected-mode workflow:

```bash
ssh jay@100.88.70.60 'cd /media/jay/data1/shenfun && TMPDIR=/media/jay/data1/tmp /media/jay/data1/conda_envs/shenfun_dns_np126_20260702/bin/python scripts/mkm_dns_target/run_mkm_channel_resolvent_production_selected_modes.py --target-h5 /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/MKM_production_64_64_32_target_t60_t180.h5 --constraint-file /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/MKM_constraints_N64_64_32_cheb_quadrature_spectral.h5 --dense-velocity-h5 /media/jay/data1/shenfun_dns_runs/dense_temporal_mkm_64_64_32_t180_t300_20260703/MKM_dense_temporal_64_64_32_t180_t300_U.h5 --output-dir /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes --csd-source target --mode-index-list 1 0 1 1 2 1 --omega-count 4 --segment-length 512 --window hann --demean-temporal --n-singular 6 --make-figures --no-tex --overwrite'
```

Dense temporal-CSD selected-mode workflow:

```bash
ssh jay@100.88.70.60 'cd /media/jay/data1/shenfun && TMPDIR=/media/jay/data1/tmp /media/jay/data1/conda_envs/shenfun_dns_np126_20260702/bin/python scripts/mkm_dns_target/run_mkm_channel_resolvent_production_selected_modes.py --target-h5 /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/MKM_production_64_64_32_target_t60_t180.h5 --constraint-file /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/MKM_constraints_N64_64_32_cheb_quadrature_spectral.h5 --dense-velocity-h5 /media/jay/data1/shenfun_dns_runs/dense_temporal_mkm_64_64_32_t180_t300_20260703/MKM_dense_temporal_64_64_32_t180_t300_U.h5 --output-dir /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes_dense_csd --csd-source dense --mode-index-list 1 0 1 1 2 1 --omega-count 6 --segment-length 2048 --overlap 0.5 --window hann --demean-temporal --dt 0.0005 --t-min 180 --t-max 300 --n-singular 6 --make-figures --no-tex --overwrite'
```

Report regeneration after either workflow:

```bash
ssh jay@100.88.70.60 'cd /media/jay/data1/shenfun && /media/jay/data1/conda_envs/shenfun_dns_np126_20260702/bin/python scripts/mkm_dns_target/report_mkm_channel_resolvent_workflow.py --manifest /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes/MKM_channel_resolvent_selected_modes_manifest.json'
ssh jay@100.88.70.60 'cd /media/jay/data1/shenfun && /media/jay/data1/conda_envs/shenfun_dns_np126_20260702/bin/python scripts/mkm_dns_target/report_mkm_channel_resolvent_workflow.py --manifest /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes_dense_csd/MKM_channel_resolvent_selected_modes_manifest.json'
```

## Next Scientific Steps

- Run broader selected-mode and wavenumber sweeps rather than only three
  low-cost modes.
- Choose frequency bands around energetic CSD peaks, not only the first
  positive low-frequency bins.
- Compare wall-normal response-energy peaks with critical-layer locations
  across more modes and frequencies.
- Inspect component energy distributions and reconstructed fields for the
  strongest aligned modes.
- Add longer-box and/or higher-Reynolds-number DNS before making VLSM scaling
  claims.
- Optionally add an Orr-Sommerfeld/Squire formulation cross-check against the
  velocity-only admissible-subspace implementation.

## Caveats

This is a selected-mode proof of concept. Low leading projection fraction does
not invalidate the resolvent model by itself: finite rank, forcing structure,
short-box and low-Reynolds-number effects, frequency-grid choice, and CSD
estimation details all affect the captured DNS spectral energy.
