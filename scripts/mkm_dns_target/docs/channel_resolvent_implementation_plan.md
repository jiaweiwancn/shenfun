# Channel resolvent and critical-layer implementation plan

This plan describes how to adapt the McKeon and Sharma critical-layer
resolvent framework to the existing MKM channel-flow DNS target. The goal is to
produce McKeon-style response modes, gain curves, critical-layer diagnostics,
and DNS comparison products while reusing the current Chebyshev/Fourier target
layout and constraint files.

## Current proof-of-concept status

Steps 1-10 are implemented for a selected-mode proof-of-concept workflow. The
current tooling covers shared channel-resolvent utilities, single-mode
resolvent solves, synthetic and production-file smoke paths, first diagnostic
plots, selected-mode temporal DNS CSD estimation, projection of DNS CSD onto
stored response modes, selected-mode orchestration, production/server wrappers,
Markdown report generation, and a consolidated smoke-test suite.

The first real production selected-mode run is complete for the sparse target
`modal/u_hat` CSD source on modes `(1,0)`, `(1,1)`, and `(2,1)` using the first
four positive CSD frequency bins. The generated manifest, Markdown report, and
PDFs were fetched to
`scripts/mkm_dns_target/production_reports/target_csd_selected_modes/`; the
larger HDF5 products remain on the Linux server under
`/media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes`.

The dense temporal selected-mode production run is also complete for the same
modes using selected modes computed on the fly from the dense raw velocity
snapshots. Its manifest, Markdown report, and PDFs were fetched to
`scripts/mkm_dns_target/production_reports/dense_csd_selected_modes/`; the
larger dense CSD/resolvent/projection HDF5 products remain on the server under
`/media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes_dense_csd`.

Remaining future work is intentionally outside this proof-of-concept layer:
full mode/frequency sweeps, higher-Reynolds-number or longer-box DNS, a later
Orr-Sommerfeld/Squire cross-check, and physical analysis of broader production
outputs.

## 0. Implementation progress

Current status:

1. Step 1 is implemented: shared utilities cover target/constraint loading,
   rebuilt constraint nullspaces, Chebyshev-Gauss physical quadrature weights,
   energy-orthonormal admissible bases, raw velocity operator assembly, modal
   energy diagnostics, and critical-layer interpolation.
2. Step 2 is implemented for a single horizontal mode and explicit frequency
   list in `compute_mkm_channel_resolvent.py`, with a synthetic smoke test.
3. Step 3 is partially implemented as a production-file smoke wrapper,
   `run_mkm_channel_resolvent_production_smoke.py`, which runs the single-mode
   solver when the production HDF5 files are present and otherwise prints the
   exact server command to run.
4. Step 4 is partially implemented as a first plotting layer,
   `plot_mkm_channel_resolvent.py`, for existing single-mode resolvent HDF5
   files. It generates mode-shape, gain, peak-location/critical-layer, and
   reconstructed-field PDFs, with a synthetic plotting smoke test.
5. Step 5 is implemented as selected-mode temporal DNS CSD estimation in
   `compute_mkm_modal_csd.py`, supporting stored target `modal/u_hat` and
   selected raw velocity modes computed on the fly. A synthetic CSD smoke test
   verifies the frequency grid, Hermitian CSD matrices, and Parseval
   normalization for a full rectangular segment.
6. Step 6 is implemented as DNS CSD projection onto existing single-mode
   resolvent response modes in `project_mkm_dns_onto_resolvent.py`, with a
   synthetic rank-1 aligned-CSD smoke test.
7. Step 7 is implemented as a selected-mode orchestration driver,
   `run_mkm_channel_resolvent_selected_modes.py`, composing the existing
   single-mode resolvent, modal CSD, projection, and plotting scripts with a
   manifest JSON and synthetic end-to-end smoke test.
8. Step 8 is implemented as a production/server wrapper,
   `run_mkm_channel_resolvent_production_selected_modes.py`, which resolves the
   MKM production paths, handles missing local `/media/...` files cleanly,
   prints an exact SSH command, and delegates to the Step 7 selected-mode
   workflow when files are available. The first target-modal production
   selected-mode run and the dense temporal selected-mode run have completed
   on the Linux server.
9. Step 9 is implemented as a workflow report generator,
   `report_mkm_channel_resolvent_workflow.py`, which reads the selected-mode
   manifest and generated HDF5/PDF outputs and writes a compact Markdown audit
   report with diagnostics, figure paths, caveats, and reproduction config.
10. Step 10 is implemented as a consolidated smoke-test runner,
    `run_channel_resolvent_smoke_suite.py`, plus final README/plan
    documentation polish for the selected-mode proof-of-concept workflow.

Exhaustive batch resolvent sweeps and broader production figure workflows
remain unimplemented.

## 1. Scope and expected result

Implement a channel-flow resolvent analysis around the accepted turbulent mean
profile in `MKM_production_64_64_32_target_t60_t180.h5`.

The finished workflow should produce:

1. A channel resolvent HDF5 file containing singular values, forcing modes,
   response modes, wall-normal energy density, and critical-layer locations for
   selected `(k_stream, k_span, omega)` combinations.
2. A mode-resolved DNS temporal cross-spectral-density file for comparison
   against the resolvent modes.
3. A projection/comparison HDF5 file quantifying how much DNS modal energy is
   captured by the leading response modes.
4. A figure directory with direct analogues of the key figures in
   `docs/mckeon2010.md`.
5. A Markdown report summarizing selected-mode workflow outputs, diagnostics,
   figure paths, and interpretation caveats for post-run review.

The first implementation should be a proof of concept on the existing
`Re_tau = 180`, `N = (64,64,32)` data. Strong VLSM scaling claims should be
deferred until longer-box and/or higher-Reynolds-number runs are available.

## 2. Existing inputs to reuse

Use the existing target and constraint products rather than changing the DNS
solver.

Required files:

1. Production target:
   `/media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/MKM_production_64_64_32_target_t60_t180.h5`
2. Matching constraint file:
   `/media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/MKM_constraints_N64_64_32_cheb_quadrature_spectral.h5`
3. Optional dense temporal raw snapshots for better frequency resolution:
   `/media/jay/data1/shenfun_dns_runs/dense_temporal_mkm_64_64_32_t180_t300_20260703/MKM_dense_temporal_64_64_32_t180_t300_U.h5`

Important existing datasets:

1. `mean_profile`: accepted turbulent mean in target component order
   `[streamwise, spanwise, wallnormal]`.
2. `geometry/z_wall`, `geometry/k_stream`, `geometry/k_span`: grid and
   wavenumber arrays.
3. `modal/u_hat`: DNS modal time series, shape `(Ns,Nx,Ny,3*Nz)`, when present.
4. `modal/B0_DNS`: equal-time modal covariance, shape `(Nx,Ny,3*Nz,3*Nz)`.
5. `operators/D_wall`, `operators/B_boundary`, `operators/E_stream`,
   `operators/E_span`, `operators/E_wall`: constraint operators.
6. Representative `Gtilde` and `Nmat` matrices, plus enough saved operators to
   rebuild them for any mode.

## 3. Mathematical formulation to implement first

Use a velocity-only admissible-subspace formulation as the first working
implementation. This matches the current target vector:

```text
q = [u_x(z0), u_y(z0), u_z(z0), ..., u_x(zNz-1), u_y(zNz-1), u_z(zNz-1)].
```

For each horizontal mode `(kappa, lambda)`, enforce incompressibility and
no-slip through the existing constraint matrix:

```text
Gtilde(kappa,lambda) q = 0.
```

Build a nullspace basis `Nmat(kappa,lambda)` so that:

```text
q = Nmat a.
```

Use the turbulent mean profile:

```text
U(z)    = mean_profile[:, streamwise]
Uprime = D_wall @ U
```

For the convention

```text
q(x,y,z,t) = qhat(z) exp(i*kappa*x + i*lambda*y - i*omega*t),
```

the raw linearized velocity operator before pressure elimination is:

```text
L_raw q =
    -i*kappa*U(z) q
    -u_z * Uprime(z) e_x
    + (1/Re_tau) * (D2 - (kappa^2 + lambda^2) I) q.
```

Here `D2 = D_wall @ D_wall`, applied componentwise. The pressure term is removed
by projecting into the admissible divergence-free/no-slip subspace. Record the
sign convention explicitly in the output file and verify that the critical-layer
denominator behaves like:

```text
omega - kappa*U(z).
```

The reduced operator should be formed in an energy-orthonormal admissible basis.
Let `Wq` be the discrete kinetic-energy weight on the full velocity vector and
let:

```text
M = Nmat^* Wq Nmat.
```

Use a Cholesky or eigenvalue factorization of `M` to define an admissible basis
`Q` satisfying:

```text
Q^* Wq Q = I,
Gtilde Q = 0.
```

Then compute:

```text
A = Q^* Wq L_raw Q
H(kappa,lambda,omega) = (-i*omega I - A)^(-1)
```

or the equivalent sign convention chosen in the code. The implementation must
store enough metadata for the convention to be unambiguous.

Compute the singular value decomposition:

```text
H = Psi Sigma Phi^*
```

where `Psi` are response modes and `Phi` are forcing modes in the
energy-orthonormal admissible coordinates. Map response modes back to physical
modal vectors with:

```text
q_response = Q @ Psi[:, j].
```

## 4. Add shared utilities

Create a helper module:

```text
scripts/mkm_dns_target/mkm_channel_resolvent_utils.py
```

Functions to implement:

1. `load_target_metadata(target_h5)`: load grid, mean profile, Reynolds number,
   wavenumbers, component order, and sampling metadata.
2. `load_constraint_operators(constraint_h5)`: load `D_wall`, `B_boundary`,
   extraction matrices, and wavenumbers.
3. `rebuild_gtilde_and_nullspace(operators, kappa, lambda, rtol)`: reuse the
   same SVD compression recipe as `build_mkm_constraints.py`.
4. `chebyshev_gauss_physical_weights(z)`: compute diagonal quadrature weights
   for the physical `L2` kinetic-energy norm on `[-1,1]`. Start with Fejer
   first-rule weights for Chebyshev-Gauss nodes and verify polynomial
   integration accuracy.
5. `velocity_energy_weight(weights_z)`: expand wall-normal quadrature weights
   to the level-major `3*Nz` velocity vector.
6. `energy_orthonormal_basis(Nmat, Wq)`: build `Q` with `Q^* Wq Q = I`.
7. `build_linearized_velocity_operator(U, Uprime, D1, Re_tau, kappa, lambda)`:
   return `L_raw` in level-major component ordering.
8. `critical_layer_locations(z, U, kappa, omega)`: return all roots of
   `U(z) = omega/kappa`; handle `kappa = 0` as a special non-propagating case.
9. `modal_energy_density(q, Wz)`: return componentwise and total energy density
   versus `z`.

Validation for this module:

1. `Gtilde @ Q` is near zero.
2. `Q^* Wq Q` is identity to roundoff.
3. Rebuilt ranks match the existing rank audit: one rank-68 mode and 2047
   rank-70 modes on the production mesh.
4. The `D_wall`, `B_boundary`, and extraction matrix conventions reproduce the
   current constraint audit.

## 5. Implement single-mode resolvent CLI

Create:

```text
scripts/mkm_dns_target/compute_mkm_channel_resolvent.py
```

First make it work for one mode and a small list of frequencies:

```bash
python scripts/mkm_dns_target/compute_mkm_channel_resolvent.py \
  --target-h5 "$OUT/MKM_production_64_64_32_target_t60_t180.h5" \
  --constraint-file "$OUT/MKM_constraints_N64_64_32_cheb_quadrature_spectral.h5" \
  --output "$OUT/MKM_channel_resolvent_test_i1_j1.h5" \
  --mode-index 1 1 \
  --omega 0.1 0.2 0.4 0.8 1.2 \
  --n-singular 6
```

HDF5 layout:

```text
geometry/z_wall
geometry/k_stream
geometry/k_span
mean/U
mean/Uprime
mode_index
frequencies/omega
critical_layers/z
critical_layers/y_plus_nearest_wall
resolvent/singular_values
resolvent/response_modes
resolvent/forcing_modes
resolvent/response_energy_density
resolvent/component_energy_density
diagnostics/constraint_residual_response
diagnostics/energy_orthonormality_error
diagnostics/operator_convention
```

Store response and forcing modes in physical level-major component ordering
after mapping back from the admissible coordinates. Include enough attributes
to state whether the stored modes are energy-normalized and what time/Fourier
sign convention was used.

## 6. Add batch mode and frequency grids

Extend `compute_mkm_channel_resolvent.py` to support:

1. `--mode-index-list i0 j0 i1 j1 ...`
2. `--wavenumber-filter`: select modes by wavelength, e.g. `lambda_x/h` and
   `lambda_y/h`.
3. `--omega-min`, `--omega-max`, `--n-omega`, `--omega-spacing linear|log`.
4. `--phase-speed-grid`: construct `omega = kappa*c` from a supplied
   phase-speed range.
5. `--mode-batch`: process multiple horizontal modes in one run.

Recommended proof-of-concept mode families:

1. Near-wall cycle candidate:
   `lambda_x^+ ~= 1000`, `lambda_y^+ ~= 100`.
2. Largest streamwise wavelengths available in current box:
   low streamwise index `i = 1`, with several low spanwise indices.
3. Streamwise-constant/lift-up limit:
   `kappa = 0`, treated separately because `omega/kappa` is undefined.

The current `Lx = 2*pi` box does not cleanly contain `lambda_x ~= 10h` VLSMs.
Label low-streamwise modes as LSM/global-mode candidates unless a longer box is
generated.

## 7. Implement McKeon-style plotting

Create:

```text
scripts/mkm_dns_target/plot_mkm_channel_resolvent.py
```

Figures to generate:

1. `mkm_resolvent_mode_shapes.pdf`
   - Analogue of McKeon Fig. 2.
   - Plot `|u_x(z)|`, `|u_y(z)|`, `|u_z(z)|` and optionally phase for the first
     3 response modes at selected `(kappa,lambda,omega)`.
2. `mkm_resolvent_gain_bode.pdf`
   - Analogue of McKeon Fig. 3.
   - Plot `sigma_j(omega)` for fixed `(kappa,lambda)`.
3. `mkm_resolvent_reconstructed_fields.pdf`
   - Analogues of McKeon Figs. 4-6.
   - Reconstruct real physical fields in `(x,z)` and `(y,z)` slices from a
     selected response mode.
4. `mkm_resolvent_phase_speed_energy.pdf`
   - Analogue of McKeon Fig. 7.
   - Plot wall-normal energy density versus phase speed `c = omega/kappa`.
5. `mkm_resolvent_peak_location_gain.pdf`
   - Analogue of McKeon Fig. 8.
   - Plot peak energy location against phase speed, overlay `U(z)`, and plot
     leading gain.
6. `mkm_resolvent_spanwise_wavenumber_sweep.pdf`
   - Analogue of McKeon Fig. 9.
   - Sweep spanwise wavenumber at fixed streamwise wavenumber.
7. `mkm_resolvent_scaling_inner_outer.pdf`
   - Analogues of McKeon Figs. 10-11.
   - Only meaningful after adding multiple Reynolds numbers. For now, create
     the plotting hook and mark single-Re output as diagnostic only.
8. `mkm_resolvent_critical_layer_scaling.pdf`
   - Analogue of McKeon Fig. 13.
   - Deferred until multiple `Re_tau` targets exist.
9. `mkm_resolvent_left_right_superposition.pdf`
   - Analogue of McKeon Fig. 15.
   - Superpose `+lambda` and `-lambda` modes and visualize streamwise streak
     structure.

Every figure should be reproducible from HDF5 outputs without re-solving the
resolvent.

## 8. Implement DNS mode-resolved temporal spectra

Create:

```text
scripts/mkm_dns_target/compute_mkm_modal_csd.py
```

Purpose:

Compute mode-resolved temporal cross-spectral-density matrices:

```text
Sqq(kappa,lambda,omega) =
    average_segments qhat(kappa,lambda,omega) qhat(kappa,lambda,omega)^*
```

Input options:

1. Use `modal/u_hat` from the accepted production target for a first sparse
   check.
2. Use dense temporal raw snapshots and compute only requested modes on the fly
   for better frequency resolution.

Recommended initial CLI:

```bash
python scripts/mkm_dns_target/compute_mkm_modal_csd.py \
  --velocity-h5 "$DENSE_OUT/MKM_dense_temporal_64_64_32_t180_t300_U.h5" \
  --target-h5 "$OUT/MKM_production_64_64_32_target_t60_t180.h5" \
  --output "$DENSE_OUT/MKM_dense_temporal_modal_csd_selected_modes.h5" \
  --dt 0.0005 \
  --t-min 180 \
  --t-max 300 \
  --mode-index-list 1 1 1 2 1 4 2 2 \
  --segment-length 2048 \
  --overlap 0.5 \
  --window hann
```

HDF5 layout:

```text
geometry/z_wall
mode_index
wavenumbers/k_stream
wavenumbers/k_span
frequencies/omega
csd/Sqq
csd/trace
csd/component_trace
metadata/window
metadata/segment_length
metadata/overlap
```

Use the same forward FFT normalization and target component ordering as
`postprocess_mkm_dns_target.py`.

## 9. Project DNS spectra/covariance onto resolvent modes

Create:

```text
scripts/mkm_dns_target/project_mkm_dns_onto_resolvent.py
```

For each matching `(kappa,lambda,omega)`, load the resolvent response modes
`psi_j` and DNS CSD `Sqq`. Compute:

```text
E_total = trace(Wq Sqq)
E_j     = psi_j^* Wq Sqq Wq psi_j
fraction_j = E_j / E_total
```

Also compute cumulative fractions for the first `r` response modes and
componentwise reconstruction errors.

Outputs:

```text
projection/energy_fraction
projection/cumulative_energy_fraction
projection/modal_coefficients
projection/reconstructed_csd_rank_r
projection/profile_error_rank_r
diagnostics/frequency_match_error
diagnostics/constraint_residual_projected
```

Generate comparison figures:

1. DNS CSD trace versus resolvent gain.
2. Leading response-mode energy fraction versus frequency.
3. DNS wall-normal energy profile versus rank-1 and rank-r resolvent
   reconstructions.
4. Critical-layer location overlaid on DNS spectral-energy peak location.

## 10. Add verification and smoke tests

Add lightweight smoke tests that can run locally without the full 11 GB target.
Use synthetic small grids and/or a tiny generated HDF5 fixture under
`/private/tmp`.

Tests:

1. Constraint reconstruction:
   - Build `Gtilde`, `Nmat`, and `Q`.
   - Assert `||Gtilde Q|| < 1e-10`.
   - Assert `||Q^* Wq Q - I|| < 1e-10`.
2. Operator shape and finite SVD:
   - Build one small operator.
   - Evaluate a few frequencies.
   - Assert singular values are finite and nonnegative.
3. Sign convention:
   - For a monotone half-channel mean, verify that gain peaks occur near
     frequencies where `omega/kappa` falls inside the range of `U(z)`.
4. DNS projection algebra:
   - Use synthetic CSD made from a known response mode and verify near-unit
     leading-mode energy fraction.
5. Plot smoke:
   - Generate one PDF figure into `/private/tmp`.

Avoid requiring the full production HDF5 files in automated local tests.

## 11. Documentation updates

Update:

```text
scripts/mkm_dns_target/README.md
scripts/mkm_dns_target/HANDOFF_production_mkm_64_64_32.md
scripts/mkm_dns_target/docs/mkm_channel_dns_sampling_and_constraints.tex
```

Add:

1. A short "Channel resolvent analysis" section to the README.
2. Exact production commands after the first successful run.
3. HDF5 schema descriptions for the resolvent, CSD, and projection files.
4. Figure references and interpretation notes.
5. Explicit limitations of the current `Re_tau = 180`, `Lx = 2*pi` data.

## 12. Suggested implementation order

1. Add `mkm_channel_resolvent_utils.py`.
2. Implement and validate energy weights, constraint nullspaces, and the
   energy-orthonormal admissible basis.
3. Implement one-mode resolvent SVD in `compute_mkm_channel_resolvent.py`.
4. Generate the first one-mode HDF5 and inspect singular values/mode shapes.
5. Add the first plotting routines: mode shapes, gain curves, and critical-layer
   overlays.
6. Add batch frequency and mode sweeps.
7. Implement `compute_mkm_modal_csd.py` using existing `modal/u_hat` first.
8. Extend modal CSD computation to dense raw velocity snapshots for selected
   modes.
9. Implement DNS projection onto resolvent response modes.
10. Add comparison plots and update documentation.
11. Run a production proof of concept for several representative modes.
12. Decide whether the next DNS run should increase `Lx`, `Re_tau`, or both
    before making VLSM scaling claims.

## 13. First proof-of-concept target

Use a small resolvent sweep:

```text
streamwise indices: 1, 2, 4
spanwise indices:   0, 1, 2, 4, 8
phase speeds:       0.2 Uc to 1.0 Uc
singular modes:     first 6
```

Expected first deliverables:

```text
MKM_channel_resolvent_selected_modes_t60_t180.h5
MKM_channel_resolvent_figures/mkm_resolvent_mode_shapes.pdf
MKM_channel_resolvent_figures/mkm_resolvent_gain_bode.pdf
MKM_channel_resolvent_figures/mkm_resolvent_peak_location_gain.pdf
MKM_channel_resolvent_figures/mkm_resolvent_reconstructed_fields.pdf
```

Success criteria:

1. Response modes satisfy the saved divergence/no-slip constraint to roundoff.
2. Response modes have unit kinetic-energy norm under `Wq`.
3. Gain curves are smooth in frequency.
4. Critical-layer markers align with visible movement of response-mode energy
   as phase speed changes.
5. DNS CSD projections show interpretable leading-mode fractions for at least a
   few energetic low-wavenumber modes.

## 14. Known limitations and decisions to revisit

1. The current Reynolds number is low for asymptotic critical-layer scaling.
2. The current streamwise box cannot represent the longest canonical VLSM
   wavelength cleanly.
3. Energy inner-product weights on Chebyshev-Gauss nodes must be verified
   carefully; incorrect weights will distort the SVD.
4. The nullspace-projected velocity formulation should be benchmarked later
   against an Orr-Sommerfeld/Squire formulation.
5. Resolvent gain alone does not predict DNS amplitude unless forcing
   statistics are modeled or measured.
6. For `kappa = 0`, phase speed and critical-layer diagnostics do not apply;
   those modes should be reported separately as streamwise-constant/lift-up
   responses.
