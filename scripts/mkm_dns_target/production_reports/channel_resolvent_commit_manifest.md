# Channel Resolvent Commit Candidate Manifest

This manifest is a staging audit for the selected-mode channel-resolvent
workflow. It is intentionally explicit because `git status --short` reports
the whole `scripts/` tree as untracked in this checkout.

## Files to Stage

Implementation and workflow scripts:

- `scripts/mkm_dns_target/build_mkm_constraints.py`
- `scripts/mkm_dns_target/mkm_channel_resolvent_utils.py`
- `scripts/mkm_dns_target/compute_mkm_channel_resolvent.py`
- `scripts/mkm_dns_target/plot_mkm_channel_resolvent.py`
- `scripts/mkm_dns_target/compute_mkm_modal_csd.py`
- `scripts/mkm_dns_target/project_mkm_dns_onto_resolvent.py`
- `scripts/mkm_dns_target/run_mkm_channel_resolvent_selected_modes.py`
- `scripts/mkm_dns_target/run_mkm_channel_resolvent_production_smoke.py`
- `scripts/mkm_dns_target/run_mkm_channel_resolvent_production_selected_modes.py`
- `scripts/mkm_dns_target/report_mkm_channel_resolvent_workflow.py`
- `scripts/mkm_dns_target/run_channel_resolvent_smoke_suite.py`

Smoke tests:

- `scripts/mkm_dns_target/smoke_channel_resolvent_utils.py`
- `scripts/mkm_dns_target/smoke_channel_resolvent_single_mode.py`
- `scripts/mkm_dns_target/smoke_channel_resolvent_plot.py`
- `scripts/mkm_dns_target/smoke_modal_csd.py`
- `scripts/mkm_dns_target/smoke_project_dns_onto_resolvent.py`
- `scripts/mkm_dns_target/smoke_selected_modes_workflow.py`
- `scripts/mkm_dns_target/smoke_production_selected_modes_wrapper.py`
- `scripts/mkm_dns_target/smoke_workflow_report.py`

Documentation:

- `scripts/mkm_dns_target/README.md`
- `scripts/mkm_dns_target/HANDOFF_production_mkm_64_64_32.md`
- `scripts/mkm_dns_target/docs/channel_resolvent_implementation_plan.md`
- `scripts/mkm_dns_target/docs/mckeon2010.md`

Production report notes and manifests:

- `scripts/mkm_dns_target/production_reports/README.md`
- `scripts/mkm_dns_target/production_reports/channel_resolvent_selected_modes_comparison.md`
- `scripts/mkm_dns_target/production_reports/channel_resolvent_workflow_inventory.md`
- `scripts/mkm_dns_target/production_reports/channel_resolvent_commit_manifest.md`
- `scripts/mkm_dns_target/production_reports/target_csd_selected_modes/README.md`
- `scripts/mkm_dns_target/production_reports/target_csd_selected_modes/MKM_channel_resolvent_selected_modes_manifest.json`
- `scripts/mkm_dns_target/production_reports/target_csd_selected_modes/MKM_channel_resolvent_selected_modes_report.md`
- `scripts/mkm_dns_target/production_reports/dense_csd_selected_modes/README.md`
- `scripts/mkm_dns_target/production_reports/dense_csd_selected_modes/MKM_channel_resolvent_selected_modes_manifest.json`
- `scripts/mkm_dns_target/production_reports/dense_csd_selected_modes/MKM_channel_resolvent_selected_modes_report.md`

Production report PDFs:

- `scripts/mkm_dns_target/production_reports/target_csd_selected_modes/figures_i1_j0/mkm_resolvent_gain_bode.pdf`
- `scripts/mkm_dns_target/production_reports/target_csd_selected_modes/figures_i1_j0/mkm_resolvent_mode_shapes.pdf`
- `scripts/mkm_dns_target/production_reports/target_csd_selected_modes/figures_i1_j0/mkm_resolvent_peak_location_gain.pdf`
- `scripts/mkm_dns_target/production_reports/target_csd_selected_modes/figures_i1_j0/mkm_resolvent_reconstructed_fields.pdf`
- `scripts/mkm_dns_target/production_reports/target_csd_selected_modes/figures_i1_j1/mkm_resolvent_gain_bode.pdf`
- `scripts/mkm_dns_target/production_reports/target_csd_selected_modes/figures_i1_j1/mkm_resolvent_mode_shapes.pdf`
- `scripts/mkm_dns_target/production_reports/target_csd_selected_modes/figures_i1_j1/mkm_resolvent_peak_location_gain.pdf`
- `scripts/mkm_dns_target/production_reports/target_csd_selected_modes/figures_i1_j1/mkm_resolvent_reconstructed_fields.pdf`
- `scripts/mkm_dns_target/production_reports/target_csd_selected_modes/figures_i2_j1/mkm_resolvent_gain_bode.pdf`
- `scripts/mkm_dns_target/production_reports/target_csd_selected_modes/figures_i2_j1/mkm_resolvent_mode_shapes.pdf`
- `scripts/mkm_dns_target/production_reports/target_csd_selected_modes/figures_i2_j1/mkm_resolvent_peak_location_gain.pdf`
- `scripts/mkm_dns_target/production_reports/target_csd_selected_modes/figures_i2_j1/mkm_resolvent_reconstructed_fields.pdf`
- `scripts/mkm_dns_target/production_reports/dense_csd_selected_modes/figures_i1_j0/mkm_resolvent_gain_bode.pdf`
- `scripts/mkm_dns_target/production_reports/dense_csd_selected_modes/figures_i1_j0/mkm_resolvent_mode_shapes.pdf`
- `scripts/mkm_dns_target/production_reports/dense_csd_selected_modes/figures_i1_j0/mkm_resolvent_peak_location_gain.pdf`
- `scripts/mkm_dns_target/production_reports/dense_csd_selected_modes/figures_i1_j0/mkm_resolvent_reconstructed_fields.pdf`
- `scripts/mkm_dns_target/production_reports/dense_csd_selected_modes/figures_i1_j1/mkm_resolvent_gain_bode.pdf`
- `scripts/mkm_dns_target/production_reports/dense_csd_selected_modes/figures_i1_j1/mkm_resolvent_mode_shapes.pdf`
- `scripts/mkm_dns_target/production_reports/dense_csd_selected_modes/figures_i1_j1/mkm_resolvent_peak_location_gain.pdf`
- `scripts/mkm_dns_target/production_reports/dense_csd_selected_modes/figures_i1_j1/mkm_resolvent_reconstructed_fields.pdf`
- `scripts/mkm_dns_target/production_reports/dense_csd_selected_modes/figures_i2_j1/mkm_resolvent_gain_bode.pdf`
- `scripts/mkm_dns_target/production_reports/dense_csd_selected_modes/figures_i2_j1/mkm_resolvent_mode_shapes.pdf`
- `scripts/mkm_dns_target/production_reports/dense_csd_selected_modes/figures_i2_j1/mkm_resolvent_peak_location_gain.pdf`
- `scripts/mkm_dns_target/production_reports/dense_csd_selected_modes/figures_i2_j1/mkm_resolvent_reconstructed_fields.pdf`

## Intentionally Excluded

- `scripts/mkm_dns_target/.DS_Store`
- `scripts/mkm_dns_target/docs/.DS_Store`
- `scripts/mkm_dns_target/__pycache__/`
- `scripts/mkm_dns_target/**/*.pyc`
- Any `*.h5` or `*.hdf5` file under `scripts/mkm_dns_target/`
- Local smoke outputs under `/private/tmp`, including synthetic HDF5/PDF/JSON
  files created by smoke tests
- Non-channel-resolvent MKM helper scripts that are not required by the
  selected-mode workflow commit candidate, such as DNS collection,
  covariance-only projection, velocity autocorrelation/autospectrum plotting,
  LaTeX auxiliary files, and old two-stage handoff notes

## HDF5 Check

No `.h5` or `.hdf5` files were found under
`scripts/mkm_dns_target/production_reports/` during this audit.

Production HDF5 products remain on the Linux server under `/media/jay/data1`,
not in the local repository:

- `/media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes`
- `/media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes_dense_csd`

## Smoke-Suite Status

Final command:

```bash
/opt/anaconda3/bin/python scripts/mkm_dns_target/run_channel_resolvent_smoke_suite.py --json-summary /private/tmp/mkm_channel_resolvent_smoke_suite_commit_manifest.json
```

Result:

```text
smoke_suite: ok passed=8 failed=0 elapsed=10.40s
json_summary=/private/tmp/mkm_channel_resolvent_smoke_suite_commit_manifest.json
```

## Production Report Locations

Sparse target-CSD selected-mode report:

- `scripts/mkm_dns_target/production_reports/target_csd_selected_modes/`

Dense temporal-CSD selected-mode report:

- `scripts/mkm_dns_target/production_reports/dense_csd_selected_modes/`

Cross-run comparison and workflow inventory:

- `scripts/mkm_dns_target/production_reports/channel_resolvent_selected_modes_comparison.md`
- `scripts/mkm_dns_target/production_reports/channel_resolvent_workflow_inventory.md`
