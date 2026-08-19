# Final report: Comte-Bellot--Corrsin decaying-HIT DNS

## Material Passport

- Origin Skill: experiment-agent
- Origin Mode: run and validation
- Origin Date: 2026-08-19
- Verification Status: VERIFIED
- Version Label: hit_dns_centos_production_3363_v1
- Source implementation commit: `12cd59a3edb761cd0960ba2c24c461f66aedadee`
- Runtime source provenance: checksum-verified CentOS submission package;
  station metadata records `git_commit=unavailable` because the deployed tree
  was extracted rather than cloned
- Lightweight archive SHA-256:
  `2e027dcca3703bee983ce200678b45fe48a8e0c37c79488603a2abc6f58f725d`

## Outcome

The 32-rank, $384^3$ Fourier DNS completed the requested unforced decay from
$tU_0/M=42$ to 171. Stage 1 (SLURM job 3362) reached station 98 at elapsed DNS
time 0.28448 s and step 2845. Stage 2 (job 3363) restarted from the complete,
inspector-validated `station_0098.h5` and reached station 171 at 0.65532 s and
step 6554. Its error log is empty and its output ends with
`HIT_STATION_171_COMPLETE`.

All large HDF5 fields and checkpoints remain on the CentOS server. The returned
archive contains only station CSV/JSON products, the combined diagnostics,
logs, and checksums. Every embedded SHA-256 check passed and no HDF5 file is
present in the archive.

## Configuration

| Item | Value |
|---|---:|
| Domain | $[0,10\pi)^3$ cm |
| Base grid | $384^3$ |
| Padded nonlinear grid | $576^3$ |
| MPI ranks | 32 |
| Backend | Shenfun 4.3.0 |
| Decomposition | pencil |
| Integrator | classical RK4 |
| Nominal timestep | $10^{-4}$ s |
| Kinematic viscosity | $0.1494117647\ \mathrm{cm^2\,s^{-1}}$ |
| Random seed | 421971 |
| Initializer | Mann isotropic spectral factorization |
| FFT planner | `FFTW_MEASURE` |

## Numerical verification

The combined production diagnostics contain 68 strictly increasing steps and
times. Kinetic energy decreases monotonically from 789.7263 to 125.0264
$\mathrm{cm^2\,s^{-2}}$, an 84.17% decay. Trapezoidal integration of the 100-step diagnostic
dissipation samples differs from the observed energy loss by 0.33%; this small
residual includes the deliberately coarse diagnostic sampling.

| Gate | Observed | Requirement | Status |
|---|---:|---:|---:|
| Maximum CFL | 0.431244 | $\leq0.5$ | PASS |
| Minimum $k_{max}\eta$ | 1.136420 | $\geq1$ | PASS |
| Maximum relative divergence | $2.5931\times10^{-15}$ | $<10^{-12}$ | PASS |
| Maximum Parseval error | $5.5132\times10^{-16}$ | $<10^{-10}$ | PASS |
| Finite station states | 3/3 | 3/3 | PASS |
| $E(k)$ integral closure | roundoff at all stations | required | PASS |
| $E_{11}^{(1)}$ integral closure | roundoff at all stations | required | PASS |

The complete HIT test suite passes: `21 passed`. This includes regression
test added after final comparison exposed a stale Table 4 field name in
`compare_results.py`. The corrected mapping uses the authoritative
`u1_rms_cm_s` column, plus a check that generated comparison CSVs use portable
LF line endings. A second independent comparison execution produced
byte-identical JSON, CSV, and PNG outputs.

## Spectrum comparison with Tables 2 and 3

Experimental points below 0.2 cm-1 are marked box-unresolved and excluded from
the metrics. No missing experimental point is extrapolated. Metrics are
descriptive; the plan did not define an experimental-agreement pass threshold.

| Station | Spectrum | Points | Relative L2 | Log10 RMSE | Median DNS/experiment | Maximum factor error |
|---:|---|---:|---:|---:|---:|---:|
| 42 | $E$ | 19 | 0.1540 | 0.0649 | 0.9990 | 1.7425 |
| 42 | $E_{11}^{(1)}$ | 19 | 0.0914 | 0.0573 | 1.0614 | 1.3098 |
| 98 | $E$ | 19 | 0.1951 | 0.1355 | 1.1710 | 1.7229 |
| 98 | $E_{11}^{(1)}$ | 20 | 0.1281 | 0.1765 | 1.2752 | 2.2600 |
| 171 | $E$ | 17 | 0.1654 | 0.1215 | 1.0894 | 1.9808 |
| 171 | $E_{11}^{(1)}$ | 20 | 0.0447 | 0.1546 | 1.2925 | 1.9042 |

The DNS reproduces the spectral shape and decay across all three stations. The
largest factor error is 2.26 for $E_{11}^{(1)}$ at 22.5 cm-1 at station 98,
where the spectrum is already in the dissipative tail. At station 171 the
energy-weighted relative L2 error of $E_{11}^{(1)}$ is 4.5%, although its median
point ratio is 1.29 because the DNS is systematically higher across several
smaller high-wavenumber values.

## Bulk comparison with Table 4

| Station | $u'$ difference | $\epsilon$ difference | $\eta$ difference | $\lambda$ difference | $R_\lambda$ difference |
|---:|---:|---:|---:|---:|---:|
| 42 | +3.36% | -8.26% | +2.05% | +7.63% | +11.73% |
| 98 | +8.09% | +32.75% | -7.01% | -6.48% | +1.33% |
| 171 | +2.01% | +23.68% | -4.93% | -8.66% | -6.21% |

Velocity RMS remains within 8.1% of the experiment at every station. The
clearest discrepancy is excess dissipation after initialization: 32.8% at
station 98 and 23.7% at station 171. The associated Kolmogorov length remains
within 7.1%, and the Taylor-scale Reynolds number remains within 6.3% at the
two evolved stations.

## N384 versus N256 resolution comparison

The station-98 resolution check uses the common represented range
$0.2\leq k\leq20$ cm-1.

| Spectrum | Points | Relative L2 | Log10 RMSE | Median N384/N256 | Maximum factor error |
|---|---:|---:|---:|---:|---:|
| $E$ | 100 | 0.1086 | 0.0208 | 1.0371 | 1.2581 |
| $E_{11}^{(1)}$ | 100 | 0.0844 | 0.0131 | 1.0239 | 1.1042 |

The median differences are 3.7% for $E$ and 2.4% for $E_{11}^{(1)}$, and the
log-space RMS differences correspond to factors of approximately 1.05 and
1.03. The production resolution therefore does not materially change the
resolved experimental-wavenumber comparison relative to the N256 pilot.

## Artifacts

- `light/`: station 42, 98, and 171 spectra and summaries plus the combined
  production diagnostics.
- `logs/`: the station-98-to-171 stdout and empty stderr logs.
- `comparison/comparison_metrics.json`: spectrum and resolution metrics.
- `comparison/spectrum_comparison_points.csv`: pointwise DNS/experiment data.
- `comparison/bulk_comparison.csv`: Table 4 comparison.
- `comparison/E_comparison.{png,pdf}`: three-station $E(k)$ comparison.
- `comparison/E11_comparison.{png,pdf}`: three-station
  $E_{11}^{(1)}(k_1)$ comparison.

Both PNG figures and independently rendered one-page PDFs were visually
inspected. Labels, legends, curves, experimental markers, and unresolved-box
shading are legible and unclipped.

## Limitations

- One fixed-seed Gaussian realization is compared with ensemble experimental
  statistics; no uncertainty interval is available for the realization error.
- The periodic box cannot represent wavenumbers below 0.2 cm-1.
- Experimental comparison metrics are descriptive because no acceptance
  threshold was registered before execution.
- The lightweight bundle contains the job-3363 solver log but not a separate
  `sacct` export. Completion is supported by the empty error log, exact final
  state, required station products, and terminal completion marker.

## Conclusion

The requested DNS is numerically complete, stable, divergence-free to
roundoff, and adequately resolved throughout. It reproduces the measured
spectral decay with moderate pointwise differences and shows a well-bounded
resolution sensitivity. The main physical mismatch is overpredicted
dissipation at the two downstream stations; that discrepancy is retained in
the result rather than tuned away.
