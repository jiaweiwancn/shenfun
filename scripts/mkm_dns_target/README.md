# MKM DNS target helpers

These scripts collect and postprocess channel-flow data from `demo/MKM.py` for
the horizontally periodic, wall-normal inhomogeneous target described in the
note.

They do not modify the solver. Run them from the cloned repository on the
Linux server with the data-backed environment:

```bash
ENV=/media/jay/data1/conda_envs/shenfun_dns_np126_20260702
REPO=/media/jay/data1/shenfun
OUT=/media/jay/data1/shenfun_dns_runs/pilot_mkm_64_64_32
```

The current production server mount is `/media/jay/data1`. If a future server
uses `/media/jay/data` instead, adjust the `ENV`, `REPO`, and `OUT` roots after
checking the paths.

## DNS collection

The production workflow is explicitly split into two stages:

1. **Spin-up/development**: start from the demo initialization, write no target
   snapshots, and force a checkpoint at the final developed state.
2. **Stationary sampling**: restart from that checkpoint, write only the
   snapshots used for statistics and target covariance estimation.

Short two-stage pilot on the current mesh:

```bash
mkdir -p "$OUT"
cd "$OUT"

# Stage 1: spin-up/development only.
$ENV/bin/mpiexec -n 16 $ENV/bin/python \
  "$REPO/scripts/mkm_dns_target/run_mkm_dns.py" \
  --output-dir "$OUT" \
  --n 64 64 32 \
  --dt 0.0005 \
  --end-time 0.01 \
  --modsave 100000000 \
  --checkpoint 100000000 \
  --moderror 10 \
  --stage-label spinup \
  --disable-snapshots \
  --force-final-checkpoint \
  --skip-xdmf \
  --filename MKM_two_stage_64_64_32

# Stage 2: stationary sampling from the spin-up checkpoint.
$ENV/bin/mpiexec -n 16 $ENV/bin/python \
  "$REPO/scripts/mkm_dns_target/run_mkm_dns.py" \
  --output-dir "$OUT" \
  --n 64 64 32 \
  --dt 0.0005 \
  --end-time 0.03 \
  --modsave 10 \
  --checkpoint 100 \
  --moderror 10 \
  --stage-label sampling \
  --from-checkpoint \
  --force-final-checkpoint \
  --filename MKM_two_stage_64_64_32
```

For a larger sampling run, increase `--end-time`, choose a `--modsave` snapshot
cadence, and run with more ranks, for example `mpiexec -n 64` or higher after a
pilot validates throughput and file sizes. The default saved wall-normal mesh is
`quadrature`, matching the solver-native Chebyshev constraint. Use
`--save-mesh uniform` only when intentionally building a uniform-grid data
target.

For production, choose the spin-up time from monitored diagnostics rather than
from the short pilot values above. Bulk flux, kinetic-energy components, wall
stress/friction velocity, mean profile, and Reynolds stresses should be checked
over time before the checkpoint is accepted as the stationary-stage initial
condition.

## Constraint recipes

The target modal vector is level-major in component order
`[streamwise, spanwise, wallnormal]`, corresponding to HDF5 groups
`[u1, u2, u0]`.

Chebyshev/quadrature spectral recipe matching the MKM solver discretization
(default):

```bash
$ENV/bin/python "$REPO/scripts/mkm_dns_target/build_mkm_constraints.py" \
  --output "$OUT/MKM_constraints_N64_64_32_cheb_quadrature_spectral.h5" \
  --n 64 64 32 \
  --wall-domain -1 1 \
  --stream-length 6.283185307179586 \
  --span-length 3.141592653589793
```

Uniform-grid recipe for intentionally uniform saved data:

```bash
$ENV/bin/python "$REPO/scripts/mkm_dns_target/build_mkm_constraints.py" \
  --output "$OUT/MKM_constraints_N64_64_32_uniform_fd7.h5" \
  --constraint-kind uniform-fd \
  --n 64 64 32 \
  --wall-domain -1 1 \
  --stream-length 6.283185307179586 \
  --span-length 3.141592653589793 \
  --stencil-width 7
```

This stores the wall-normal derivative matrix, boundary selector, extraction
operators, wavenumbers, rank/nullity audit for all modes, and representative
compressed `Gtilde`/null-space matrices. Use `--save-all-gtilde` only when a
full dense per-mode table is needed.

## Postprocessing

First check sampled-statistics convergence over blocks of the stationary-stage
snapshots:

```bash
$ENV/bin/python "$REPO/scripts/mkm_dns_target/check_mkm_sampling_convergence.py" \
  --velocity-h5 "$OUT/MKM_two_stage_64_64_32_U.h5" \
  --output "$OUT/MKM_two_stage_64_64_32_sampling_convergence.json" \
  --dt 0.0005 \
  --n-blocks 2
```

Then postprocess the stationary-stage file:

```bash
$ENV/bin/python "$REPO/scripts/mkm_dns_target/postprocess_mkm_dns_target.py" \
  --velocity-h5 "$OUT/MKM_two_stage_64_64_32_U.h5" \
  --output "$OUT/MKM_two_stage_64_64_32_target.h5" \
  --dt 0.0005 \
  --constraint-file "$OUT/MKM_constraints_N64_64_32_cheb_quadrature_spectral.h5" \
  --sampling-stage-label stationary \
  --max-lag 2 \
  --store-modal-coefficients
```

The postprocessor writes geometry, sampling times, mean profile, Reynolds
stress profile, horizontal modal coefficients when requested, equal-time modal
covariance, optional lag covariances, and a mode-energy audit.

Finally audit the target against the saved constraint:

```bash
$ENV/bin/python "$REPO/scripts/mkm_dns_target/audit_mkm_target.py" \
  --target-h5 "$OUT/MKM_two_stage_64_64_32_target.h5" \
  --velocity-h5 "$OUT/MKM_two_stage_64_64_32_U.h5" \
  --constraint-file "$OUT/MKM_constraints_N64_64_32_cheb_quadrature_spectral.h5" \
  --output "$OUT/MKM_two_stage_64_64_32_audit.json"
```

## Channel resolvent proof of concept

### Channel resolvent workflow status

The implemented proof-of-concept workflow is selected-mode rather than a full
batch sweep. It covers:

1. `mkm_channel_resolvent_utils.py` provides target/constraint loading,
   constraint nullspaces, Chebyshev-Gauss physical quadrature weights,
   energy-orthonormal admissible bases, the raw velocity operator, modal
   energy diagnostics, and critical-layer interpolation.
2. `compute_mkm_channel_resolvent.py` computes a single horizontal mode and a
   small explicit list of frequencies using the velocity-only admissible
   formulation.
3. `compute_mkm_modal_csd.py` estimates selected-mode temporal DNS CSD from
   stored `modal/u_hat` or selected raw velocity modes.
4. `project_mkm_dns_onto_resolvent.py` projects DNS CSD onto stored response
   modes.
5. `plot_mkm_channel_resolvent.py` generates first McKeon-style diagnostics.
6. `run_mkm_channel_resolvent_selected_modes.py` and
   `run_mkm_channel_resolvent_production_selected_modes.py` compose the
   selected-mode workflow locally or on the server.
7. `report_mkm_channel_resolvent_workflow.py` writes a Markdown audit report
   from a workflow manifest.
8. `run_channel_resolvent_smoke_suite.py` runs the synthetic and wrapper smoke
   checks in one command.

The first production target-modal selected-mode run has completed for modes
`(1,0)`, `(1,1)`, and `(2,1)` using the sparse accepted target `modal/u_hat`
record. The dense temporal selected-mode run has also completed for the same
modes using selected modes computed from the dense raw velocity snapshots.
Future work remains: broader mode/frequency sweeps, interpretation of broader
production outputs, higher-Reynolds-number or longer-box DNS, and a later
Orr-Sommerfeld/Squire cross-check.

### Local synthetic verification

Run the full smoke suite with an HDF5-capable Python:

```bash
/opt/anaconda3/bin/python scripts/mkm_dns_target/run_channel_resolvent_smoke_suite.py \
  --json-summary /private/tmp/mkm_channel_resolvent_smoke_suite_summary.json
```

For a narrower local sequence while developing, run:

```bash
/opt/anaconda3/bin/python scripts/mkm_dns_target/smoke_channel_resolvent_utils.py
/opt/anaconda3/bin/python scripts/mkm_dns_target/smoke_channel_resolvent_single_mode.py
/opt/anaconda3/bin/python scripts/mkm_dns_target/smoke_selected_modes_workflow.py
/opt/anaconda3/bin/python scripts/mkm_dns_target/smoke_workflow_report.py
```

Production-file smoke on the Linux server:

```bash
ENV=/media/jay/data1/conda_envs/shenfun_dns_np126_20260702
REPO=/media/jay/data1/shenfun
OUT=/media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702

cd "$REPO"
$ENV/bin/python "$REPO/scripts/mkm_dns_target/run_mkm_channel_resolvent_production_smoke.py" \
  --output-dir "$OUT" \
  --mode-index 1 1 \
  --omega 0.1 0.2 0.4 \
  --n-singular 4 \
  --re-tau 180
```

This writes, for example,
`$OUT/MKM_channel_resolvent_smoke_i1_j1.h5`, containing the selected
wavenumbers, frequencies, singular values, energy-normalized physical response
and forcing modes, response energy-density diagnostics, critical-layer roots,
and residual/norm diagnostics.

The first plotting layer reads an existing single-mode resolvent HDF5 and
generates mode-shape, gain, peak-location/critical-layer, and reconstructed
field PDFs. A synthetic plotting smoke creates its own small HDF5 under
`/private/tmp`:

```bash
/opt/anaconda3/bin/python scripts/mkm_dns_target/smoke_channel_resolvent_plot.py
```

To plot a production smoke output on the Linux server:

```bash
$ENV/bin/python "$REPO/scripts/mkm_dns_target/plot_mkm_channel_resolvent.py" \
  --resolvent-h5 "$OUT/MKM_channel_resolvent_smoke_i1_j1.h5" \
  --figure-dir "$OUT/MKM_channel_resolvent_smoke_figures" \
  --omega-index 0 \
  --singular-index 0 \
  --n-shapes 3
```

Add `--no-tex` if the Matplotlib LaTeX toolchain is unavailable.

This is still only a selected-mode proof-of-concept path; exhaustive sweeps
and broader production comparison figures remain future steps.

### Mode-resolved temporal CSD

`compute_mkm_modal_csd.py` estimates selected horizontal-mode temporal
cross-spectral-density matrices,
`Sqq(kappa,lambda,omega)`, either from stored target `modal/u_hat` or directly
from raw velocity snapshots. The estimator is two-sided in angular frequency
and stores the normalization needed for the Parseval check:

```text
Sqq = sample_dt/sum(window^2)/n_segments
      * sum_segments FFT_t(window*q) FFT_t(window*q)^*
```

Using stored modal coefficients from the accepted target:

```bash
$ENV/bin/python "$REPO/scripts/mkm_dns_target/compute_mkm_modal_csd.py" \
  --target-h5 "$OUT/MKM_production_64_64_32_target_t60_t180.h5" \
  --output "$OUT/MKM_production_modal_csd_smoke_i1_j1.h5" \
  --mode-index-list 1 1 \
  --segment-length 512 \
  --overlap 0.5 \
  --window hann \
  --demean-temporal \
  --overwrite
```

Computing only selected horizontal modes on the fly from dense raw snapshots:

```bash
DENSE=/media/jay/data1/shenfun_dns_runs/dense_temporal_mkm_64_64_32_t180_t300_20260703

$ENV/bin/python "$REPO/scripts/mkm_dns_target/compute_mkm_modal_csd.py" \
  --velocity-h5 "$DENSE/MKM_dense_temporal_64_64_32_t180_t300_U.h5" \
  --target-h5 "$OUT/MKM_production_64_64_32_target_t60_t180.h5" \
  --output "$DENSE/MKM_dense_temporal_modal_csd_selected_modes.h5" \
  --dt 0.0005 \
  --t-min 180 \
  --t-max 300 \
  --mode-index-list 1 1 1 2 2 1 \
  --segment-length 2048 \
  --overlap 0.5 \
  --window hann \
  --demean-temporal \
  --overwrite
```

The output schema includes:

```text
geometry/z_wall
mode/index
mode/k_stream
mode/k_span
frequencies/omega
csd/Sqq
csd/trace
csd/component_trace
csd/energy_trace
metadata/selected_times
metadata/selected_keys
metadata/window
metadata/window_energy
metadata/sample_dt
metadata/segment_length
metadata/overlap
metadata/source
diagnostics/parseval_energy_time
diagnostics/parseval_energy_spectrum
diagnostics/parseval_relative_error
```

For `window=none` and a single full-record segment, the Parseval diagnostic
compares the spectrum integral against the selected-record modal energy. With
Hann windows or overlapping segments, the diagnostic compares against the
window-weighted segment-average energy used by the estimator.

### DNS CSD projection onto resolvent modes

`project_mkm_dns_onto_resolvent.py` compares an existing single-mode
resolvent HDF5 against a selected-mode CSD HDF5. The resolvent frequencies must
match CSD frequency bins within `--frequency-tolerance`; in practice, choose
the resolvent `--omega` list from the CSD `frequencies/omega` values you want
to compare.

Example command:

```bash
$ENV/bin/python "$REPO/scripts/mkm_dns_target/project_mkm_dns_onto_resolvent.py" \
  --resolvent-h5 "$OUT/MKM_channel_resolvent_csd_bins_i1_j1.h5" \
  --csd-h5 "$OUT/MKM_production_modal_csd_smoke_i1_j1.h5" \
  --output "$OUT/MKM_channel_resolvent_dns_projection_i1_j1.h5" \
  --max-rank 4 \
  --frequency-tolerance 1e-8 \
  --overwrite
```

The projection output schema is:

```text
geometry/z_wall
mode/index
mode/k_stream
mode/k_span
frequencies/resolvent_omega
frequencies/csd_omega
frequencies/csd_index
projection/energy_total
projection/energy_fraction
projection/cumulative_energy_fraction
projection/modal_coefficients
projection/response_energy_norm
projection/response_renormalization
projection/weighted_frobenius_relative_error
diagnostics/frequency_match_error
diagnostics/mode_match_error
diagnostics/max_response_energy_norm_error
diagnostics/negative_fraction_count
diagnostics/zero_or_negative_total_energy_count
```

A high leading or cumulative fraction means the DNS CSD at that
`(kappa, lambda, omega)` is well aligned with the stored resolvent response
subspace. A low fraction can reflect the forcing statistics, missing response
modes, a frequency-bin mismatch, finite-sample CSD noise, or limitations of the
linearized resolvent model. This step still does not add batch resolvent sweeps
or new solver math.

### Selected-mode end-to-end workflow

`run_mkm_channel_resolvent_selected_modes.py` is a small orchestration layer
for proof-of-concept runs over a few selected mode indices. It composes the
existing single-mode resolvent, selected-mode CSD, projection, and plotting
tools. It does not add new solver math or DNS algorithms.

Synthetic local smoke:

```bash
/opt/anaconda3/bin/python scripts/mkm_dns_target/smoke_selected_modes_workflow.py
```

Production/server template:

```bash
ENV=/media/jay/data1/conda_envs/shenfun_dns_np126_20260702
REPO=/media/jay/data1/shenfun
OUT=/media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702

cd "$REPO"
$ENV/bin/python "$REPO/scripts/mkm_dns_target/run_mkm_channel_resolvent_selected_modes.py" \
  --target-h5 "$OUT/MKM_production_64_64_32_target_t60_t180.h5" \
  --constraint-file "$OUT/MKM_constraints_N64_64_32_cheb_quadrature_spectral.h5" \
  --output-dir "$OUT/MKM_channel_resolvent_selected_modes" \
  --mode-index-list 1 1 1 2 2 1 \
  --compute-csd-from-target \
  --segment-length 512 \
  --overlap 0.5 \
  --window hann \
  --demean-temporal \
  --omega-count 6 \
  --n-singular 4 \
  --make-figures \
  --re-tau 180 \
  --overwrite
```

The workflow writes:

```text
MKM_channel_modal_csd_selected_modes.h5
MKM_channel_resolvent_i{I}_j{J}.h5
MKM_channel_resolvent_projection_i{I}_j{J}.h5
figures_i{I}_j{J}/mkm_resolvent_*.pdf
MKM_channel_resolvent_selected_modes_manifest.json
```

Frequency selection is intentionally simple. Explicit `--omega` values are used
as given; `--phase-speed c...` uses `omega = kappa*c` per mode. If no explicit
frequency list is provided but a CSD is available or computed, the driver uses
the first `--omega-count` positive finite low-frequency CSD bins. Passing
`--omega-from-csd` with explicit `--omega` or `--phase-speed` snaps the
requested values to the nearest CSD bins. Projection still requires the final
resolvent frequencies to match the CSD grid within `--frequency-tolerance`.

The manifest records source files, selected modes, omega values per mode,
resolvent/projection/figure paths, leading singular values, residual
diagnostics, and projection fractions. This is a selected-mode proof of
concept, not an exhaustive mode sweep.

Generated file types are:

```text
*.h5      resolvent, CSD, and projection data products
*.pdf     mode-shape, gain, peak-location, and reconstructed-field figures
*.json    selected-mode workflow manifest and optional smoke-suite summary
*.md      post-run workflow audit report
```

### Production selected-mode channel resolvent workflow

`run_mkm_channel_resolvent_production_selected_modes.py` wraps the selected-mode
driver with production defaults from the handoff. It checks whether the
production HDF5 files are locally visible; if not, it exits cleanly and prints
the SSH command to run on the Linux server.

Low-cost production command using the target file's stored `modal/u_hat`:

```bash
ENV=/media/jay/data1/conda_envs/shenfun_dns_np126_20260702
REPO=/media/jay/data1/shenfun
OUT=/media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702
DENSE=/media/jay/data1/shenfun_dns_runs/dense_temporal_mkm_64_64_32_t180_t300_20260703

cd "$REPO"
$ENV/bin/python "$REPO/scripts/mkm_dns_target/run_mkm_channel_resolvent_production_selected_modes.py" \
  --target-h5 "$OUT/MKM_production_64_64_32_target_t60_t180.h5" \
  --constraint-file "$OUT/MKM_constraints_N64_64_32_cheb_quadrature_spectral.h5" \
  --dense-velocity-h5 "$DENSE/MKM_dense_temporal_64_64_32_t180_t300_U.h5" \
  --output-dir "$OUT/channel_resolvent_selected_modes" \
  --csd-source target \
  --mode-index-list 1 0 1 1 2 1 \
  --omega-count 4 \
  --segment-length 512 \
  --window hann \
  --demean-temporal \
  --n-singular 6 \
  --make-figures \
  --no-tex \
  --overwrite
```

Dense temporal CSD command, using the separate dense raw velocity file:

```bash
$ENV/bin/python "$REPO/scripts/mkm_dns_target/run_mkm_channel_resolvent_production_selected_modes.py" \
  --target-h5 "$OUT/MKM_production_64_64_32_target_t60_t180.h5" \
  --constraint-file "$OUT/MKM_constraints_N64_64_32_cheb_quadrature_spectral.h5" \
  --dense-velocity-h5 "$DENSE/MKM_dense_temporal_64_64_32_t180_t300_U.h5" \
  --output-dir "$OUT/channel_resolvent_selected_modes_dense_csd" \
  --csd-source dense \
  --mode-index-list 1 0 1 1 2 1 \
  --omega-count 6 \
  --dt 0.0005 \
  --t-min 180 \
  --t-max 300 \
  --segment-length 2048 \
  --overlap 0.5 \
  --window hann \
  --demean-temporal \
  --n-singular 6 \
  --make-figures \
  --no-tex \
  --overwrite
```

From the local Mac, first inspect the resolved command without running:

```bash
/opt/anaconda3/bin/python scripts/mkm_dns_target/run_mkm_channel_resolvent_production_selected_modes.py \
  --dry-run \
  --print-ssh-command \
  --mode-index-list 1 0 1 1 2 1 \
  --omega-count 4 \
  --skip-plots
```

If a future server uses a different mount root, pass explicit paths after
checking the target, constraint, dense velocity, and output directories.

The verified SSH form for the completed target-modal run is:

```bash
ssh jay@100.88.70.60 'cd /media/jay/data1/shenfun && TMPDIR=/media/jay/data1/tmp /media/jay/data1/conda_envs/shenfun_dns_np126_20260702/bin/python scripts/mkm_dns_target/run_mkm_channel_resolvent_production_selected_modes.py --target-h5 /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/MKM_production_64_64_32_target_t60_t180.h5 --constraint-file /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/MKM_constraints_N64_64_32_cheb_quadrature_spectral.h5 --dense-velocity-h5 /media/jay/data1/shenfun_dns_runs/dense_temporal_mkm_64_64_32_t180_t300_20260703/MKM_dense_temporal_64_64_32_t180_t300_U.h5 --output-dir /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes --csd-source target --mode-index-list 1 0 1 1 2 1 --omega-count 4 --segment-length 512 --window hann --demean-temporal --n-singular 6 --make-figures --no-tex --overwrite'
```

The completed target-CSD output directory is:

```text
/media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes
```

It contains the shared selected-mode CSD, one resolvent HDF5 per mode, one
projection HDF5 per mode, one `figures_i{I}_j{J}/` directory per mode, and
`MKM_channel_resolvent_selected_modes_manifest.json`.

For a first pass, use a handful of energetic low-wavenumber modes such as
`1 0`, `1 1`, and `2 1`. The default frequency behavior is CSD-bin friendly:
the wrapper computes or uses a CSD first and chooses the first `--omega-count`
positive finite bins. If you pass `--omega` or `--phase-speed`, the wrapper
snaps those requests to the CSD grid before projection. Dense CSD is much more
expensive because it FFTs selected modes from the 36 GB raw velocity file, but
it gives finer temporal frequency resolution than the target `modal/u_hat`.

Recommended production sequence:

```bash
# 1. Run the low-cost target-modal selected-mode workflow on the server.
ssh jay@100.88.70.60 'cd /media/jay/data1/shenfun && TMPDIR=/media/jay/data1/tmp /media/jay/data1/conda_envs/shenfun_dns_np126_20260702/bin/python scripts/mkm_dns_target/run_mkm_channel_resolvent_production_selected_modes.py --target-h5 /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/MKM_production_64_64_32_target_t60_t180.h5 --constraint-file /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/MKM_constraints_N64_64_32_cheb_quadrature_spectral.h5 --dense-velocity-h5 /media/jay/data1/shenfun_dns_runs/dense_temporal_mkm_64_64_32_t180_t300_20260703/MKM_dense_temporal_64_64_32_t180_t300_U.h5 --output-dir /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes --csd-source target --mode-index-list 1 0 1 1 2 1 --omega-count 4 --segment-length 512 --window hann --demean-temporal --n-singular 6 --make-figures --no-tex --overwrite'

# 2. Generate the Markdown audit report from the manifest.
ssh jay@100.88.70.60 'cd /media/jay/data1/shenfun && /media/jay/data1/conda_envs/shenfun_dns_np126_20260702/bin/python scripts/mkm_dns_target/report_mkm_channel_resolvent_workflow.py --manifest /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes/MKM_channel_resolvent_selected_modes_manifest.json'
```

The production manifest and report land in:

```text
/media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes
```

Completed target-modal production result:

```text
server output = /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes
local summary = scripts/mkm_dns_target/production_reports/target_csd_selected_modes/
```

The completed run used `--csd-source target`, modes `1 0`, `1 1`, and `2 1`,
the first four positive CSD bins
`0.12271846303085827, 0.24543692606171655, 0.3681553890925748,
0.4908738521234331`, `segment_length=512`, `window=hann`, and
`n_singular=6`. The generated report shows all constraint, normalization, and
frequency-match diagnostics passing at near-roundoff levels. The shared CSD
HDF5 is about 864 MiB and remains on the server; only the manifest, Markdown
report, and PDFs were fetched locally.

Completed dense temporal production result:

```text
server output = /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes_dense_csd
local summary = scripts/mkm_dns_target/production_reports/dense_csd_selected_modes/
```

The dense run used `--csd-source dense`, modes `1 0`, `1 1`, and `2 1`,
`t_min=180`, `t_max=300`, `segment_length=2048`, `window=hann`,
`n_singular=6`, and the first six positive dense-CSD bins
`0.30679615757740725, 0.6135923151548145, 0.9203884727322218,
1.227184630309629, 1.5339807878870364, 1.8407769454644436`. The generated
report shows all constraint, normalization, and frequency-match diagnostics
passing at near-roundoff levels. The shared dense CSD HDF5 is about 3.38 GiB
and remains on the server; only the manifest, Markdown report, and PDFs were
fetched locally.

### Workflow report

After a selected-mode workflow finishes, generate a compact Markdown audit
report from the manifest:

```bash
$ENV/bin/python "$REPO/scripts/mkm_dns_target/report_mkm_channel_resolvent_workflow.py" \
  --manifest "$OUT/channel_resolvent_selected_modes/MKM_channel_resolvent_selected_modes_manifest.json"
```

By default this writes:

```text
$OUT/channel_resolvent_selected_modes/MKM_channel_resolvent_selected_modes_report.md
```

The report summarizes inputs, selected modes and frequencies, leading
resolvent gains, constraint residuals, energy-normalization errors, CSD
Parseval diagnostics, projection energy fractions, weighted Frobenius
projection errors, and generated figure paths. Add
`--include-hdf5-schema` for a fuller schema appendix, or use `--max-modes` and
`--max-omega` to keep a production report short.

Diagnostics are reported with simple pass/warn/fail thresholds. Constraint
residuals and energy-norm errors warn above `1e-8` and fail above `1e-6`.
Rectangular-window CSD Parseval errors warn above `1e-6`; Hann/windowed CSD
Parseval values are treated as diagnostics because the estimator compares
against a window-weighted segment average.

## Temporal diagnostics

The target HDF5 stores equal-time and selected modal lag covariances. For the
reproduction run, two additional helpers compute physical-space temporal
statistics directly from the accepted velocity snapshots:

- `compute_mkm_velocity_autocovariance.py`: estimates
  `R_ii(tau; z)` and the normalized auto-correlation
  `R_ii(tau; z)/R_ii(0; z)` for every velocity component and wall-normal
  level, averaging over each homogeneous `x-y` plane.
- `compute_mkm_velocity_autospectrum.py`: estimates the two-sided
  angular-frequency periodogram `S_ii(omega; z)` for every component and
  wall-normal level, again plane-averaged over `x-y`. The selected-z plot can
  show the variance-normalized quantity `S_ii u_tau/[h R_ii(0; z)]` and an
  optional log-log reference slope.

For a production retained window whose target file records the accepted sample
times and mean profile, the commands are:

```bash
$ENV/bin/python "$REPO/scripts/mkm_dns_target/compute_mkm_velocity_autocovariance.py" \
  --velocity-h5 "$OUT/MKM_production_64_64_32_U.h5" \
  --target-h5 "$OUT/MKM_production_64_64_32_target_t60_t180.h5" \
  --output "$OUT/MKM_production_64_64_32_velocity_autocovariance_t60_t180_lag2.h5" \
  --max-lag 20 \
  --normalize-plot \
  --selected-z 0.025 0.5 0.9 \
  --figure "$OUT/MKM_production_64_64_32_velocity_autocovariance_t60_t180_lag2_selected_z.pdf"

$ENV/bin/python "$REPO/scripts/mkm_dns_target/compute_mkm_velocity_autospectrum.py" \
  --velocity-h5 "$OUT/MKM_production_64_64_32_U.h5" \
  --target-h5 "$OUT/MKM_production_64_64_32_target_t60_t180.h5" \
  --output "$OUT/MKM_production_64_64_32_velocity_autospectrum_t60_t180.h5" \
  --log-x \
  --normalize-by-variance \
  --selected-z 0.025 0.5 0.9 \
  --reference-slope -1.6666666666666667 \
  --reference-omega-range 0.7 2.0 \
  --figure "$OUT/MKM_production_64_64_32_velocity_autospectrum_t60_t180_selected_z_loglog.pdf"
```

The default selected wall-normal levels are a nonsymmetric half-channel set.
The nearest saved Chebyshev-Gauss points on the current mesh are
`z/h = 0.0245, 0.4929, 0.8932`. The documentation copies of these plots live
under `docs/figures/`.
