# MKM Channel Resolvent Selected-Mode Report

## Summary
| Item | Value |
| --- | --- |
| Manifest | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/MKM_channel_resolvent_selected_modes_manifest.json |
| Output directory | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200 |
| Selected modes | [[1, 0], [1, 1], [2, 0], [2, 1], [4, 1]] |
| Reported modes | 5 |
| Truncated modes | 0 |
| n_singular | 6 |
| Re_tau | 180.0 |

## Inputs
| Input | Path |
| --- | --- |
| Target HDF5 | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/MKM_production_Lx4pi_64_128_32_target_t60_t200.h5 |
| Constraint HDF5 | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/MKM_constraints_Lx4pi_N64_128_32_cheb_quadrature_spectral.h5 |
| Shared CSD HDF5 | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/MKM_channel_modal_csd_selected_modes.h5 |

## Shared CSD
| Field | Value |
| --- | --- |
| Path | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/MKM_channel_modal_csd_selected_modes.h5 |
| Size | 5.63 GiB |
| Source | raw_velocity_fft2_selected_modes |
| Mode count | 5 |
| n_omega | 2048 |
| sample_dt | 0.01 |
| segment_length | 2048 |
| n_segments | 10 |
| window | hann |
| max Parseval relative error | 7.197777e-15 |
| Parseval relative errors | 6.626056e-15, 5.876078e-15, 6.405828e-15, 6.303049e-15, 7.197777e-15 |

## Mode Results
### Mode (1, 0)
| Field | Value |
| --- | --- |
| kappa | 0.5 |
| lambda | 0 |
| Resolvent HDF5 | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/MKM_channel_resolvent_i1_j0.h5 |
| Resolvent size | 315.93 KiB |
| Projection HDF5 | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/MKM_channel_resolvent_projection_i1_j0.h5 |
| Projection size | 24.62 KiB |
| Omega selection | positive_low_frequency_csd_bins |

| idx | omega | sigma1 | sigma2 | critical roots | lead fraction | cum fraction | rank1 Fro err |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0.306796 | 0.265086 | 0.225723 | 2 | 0.106173 | 0.337118 | 0.972491 |
| 1 | 0.613592 | 0.283474 | 0.239238 | 2 | 0.070129 | 0.330639 | 0.985918 |
| 2 | 0.920388 | 0.304201 | 0.254254 | 2 | 0.0653187 | 0.377876 | 0.988706 |
| 3 | 1.22718 | 0.327671 | 0.271004 | 2 | 0.0607594 | 0.344891 | 0.99079 |
| 4 | 1.53398 | 0.354372 | 0.289764 | 2 | 0.0645229 | 0.289679 | 0.988475 |
| 5 | 1.84078 | 0.384889 | 0.310864 | 2 | 0.0600511 | 0.285077 | 0.99121 |

| Diagnostic | Value | Status |
| --- | --- | --- |
| max response constraint residual | 4.301554e-15 | PASS |
| max forcing constraint residual | 4.282450e-15 | PASS |
| max response energy norm error | 2.886580e-15 | PASS |
| max forcing energy norm error | 3.330669e-15 | PASS |
| max projection frequency match error | 0.000000e+00 | PASS |

### Mode (1, 1)
| Field | Value |
| --- | --- |
| kappa | 0.5 |
| lambda | 2 |
| Resolvent HDF5 | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/MKM_channel_resolvent_i1_j1.h5 |
| Resolvent size | 315.93 KiB |
| Projection HDF5 | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/MKM_channel_resolvent_projection_i1_j1.h5 |
| Projection size | 24.62 KiB |
| Omega selection | positive_low_frequency_csd_bins |

| idx | omega | sigma1 | sigma2 | critical roots | lead fraction | cum fraction | rank1 Fro err |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0.306796 | 0.416239 | 0.408107 | 2 | 0.0929623 | 0.443494 | 0.979929 |
| 1 | 0.613592 | 0.452568 | 0.443273 | 2 | 0.0967445 | 0.481276 | 0.977069 |
| 2 | 0.920388 | 0.494376 | 0.483687 | 2 | 0.124887 | 0.512384 | 0.965145 |
| 3 | 1.22718 | 0.542798 | 0.530429 | 2 | 0.102911 | 0.429094 | 0.97497 |
| 4 | 1.53398 | 0.599265 | 0.584855 | 2 | 0.0930584 | 0.426184 | 0.981286 |
| 5 | 1.84078 | 0.665594 | 0.648685 | 2 | 0.0590124 | 0.448302 | 0.99334 |

| Diagnostic | Value | Status |
| --- | --- | --- |
| max response constraint residual | 3.487356e-15 | PASS |
| max forcing constraint residual | 3.935243e-15 | PASS |
| max response energy norm error | 3.330669e-15 | PASS |
| max forcing energy norm error | 2.775558e-15 | PASS |
| max projection frequency match error | 0.000000e+00 | PASS |

### Mode (2, 0)
| Field | Value |
| --- | --- |
| kappa | 1 |
| lambda | 0 |
| Resolvent HDF5 | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/MKM_channel_resolvent_i2_j0.h5 |
| Resolvent size | 315.93 KiB |
| Projection HDF5 | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/MKM_channel_resolvent_projection_i2_j0.h5 |
| Projection size | 24.62 KiB |
| Omega selection | positive_low_frequency_csd_bins |

| idx | omega | sigma1 | sigma2 | critical roots | lead fraction | cum fraction | rank1 Fro err |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0.306796 | 0.148534 | 0.134873 | 2 | 0.0547548 | 0.326462 | 0.993051 |
| 1 | 0.613592 | 0.154011 | 0.139457 | 2 | 0.0452236 | 0.263603 | 0.995085 |
| 2 | 0.920388 | 0.159839 | 0.144317 | 2 | 0.0945483 | 0.316952 | 0.978782 |
| 3 | 1.22718 | 0.166047 | 0.149473 | 2 | 0.0923022 | 0.34989 | 0.979083 |
| 4 | 1.53398 | 0.172667 | 0.15495 | 2 | 0.0570397 | 0.290821 | 0.991234 |
| 5 | 1.84078 | 0.179732 | 0.160772 | 2 | 0.0332744 | 0.255908 | 0.997309 |

| Diagnostic | Value | Status |
| --- | --- | --- |
| max response constraint residual | 4.415236e-15 | PASS |
| max forcing constraint residual | 4.379267e-15 | PASS |
| max response energy norm error | 3.330669e-15 | PASS |
| max forcing energy norm error | 2.220446e-15 | PASS |
| max projection frequency match error | 0.000000e+00 | PASS |

### Mode (2, 1)
| Field | Value |
| --- | --- |
| kappa | 1 |
| lambda | 2 |
| Resolvent HDF5 | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/MKM_channel_resolvent_i2_j1.h5 |
| Resolvent size | 315.93 KiB |
| Projection HDF5 | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/MKM_channel_resolvent_projection_i2_j1.h5 |
| Projection size | 24.62 KiB |
| Omega selection | positive_low_frequency_csd_bins |

| idx | omega | sigma1 | sigma2 | critical roots | lead fraction | cum fraction | rank1 Fro err |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0.306796 | 0.187506 | 0.185093 | 2 | 0.100912 | 0.402286 | 0.974037 |
| 1 | 0.613592 | 0.195627 | 0.193034 | 2 | 0.13231 | 0.371434 | 0.957927 |
| 2 | 0.920388 | 0.20436 | 0.201569 | 2 | 0.118225 | 0.367277 | 0.966103 |
| 3 | 1.22718 | 0.213765 | 0.210756 | 2 | 0.100987 | 0.346431 | 0.973146 |
| 4 | 1.53398 | 0.223912 | 0.220664 | 2 | 0.0524799 | 0.383624 | 0.993515 |
| 5 | 1.84078 | 0.23488 | 0.231366 | 2 | 0.12559 | 0.399196 | 0.960475 |

| Diagnostic | Value | Status |
| --- | --- | --- |
| max response constraint residual | 3.060396e-15 | PASS |
| max forcing constraint residual | 3.406053e-15 | PASS |
| max response energy norm error | 2.997602e-15 | PASS |
| max forcing energy norm error | 2.220446e-15 | PASS |
| max projection frequency match error | 0.000000e+00 | PASS |

### Mode (4, 1)
| Field | Value |
| --- | --- |
| kappa | 2 |
| lambda | 2 |
| Resolvent HDF5 | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/MKM_channel_resolvent_i4_j1.h5 |
| Resolvent size | 315.93 KiB |
| Projection HDF5 | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/MKM_channel_resolvent_projection_i4_j1.h5 |
| Projection size | 24.62 KiB |
| Omega selection | positive_low_frequency_csd_bins |

| idx | omega | sigma1 | sigma2 | critical roots | lead fraction | cum fraction | rank1 Fro err |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0.306796 | 0.0930317 | 0.0924305 | 2 | 0.0742484 | 0.34793 | 0.986933 |
| 1 | 0.613592 | 0.0951314 | 0.0945047 | 2 | 0.0807597 | 0.342541 | 0.984171 |
| 2 | 0.920388 | 0.097314 | 0.0966603 | 2 | 0.127032 | 0.36142 | 0.957174 |
| 3 | 1.22718 | 0.0995838 | 0.0989016 | 2 | 0.0881102 | 0.336106 | 0.97518 |
| 4 | 1.53398 | 0.101945 | 0.101233 | 2 | 0.0793809 | 0.315496 | 0.981218 |
| 5 | 1.84078 | 0.104404 | 0.10366 | 2 | 0.0932192 | 0.332207 | 0.977593 |

| Diagnostic | Value | Status |
| --- | --- | --- |
| max response constraint residual | 5.187898e-15 | PASS |
| max forcing constraint residual | 4.881671e-15 | PASS |
| max response energy norm error | 3.108624e-15 | PASS |
| max forcing energy norm error | 3.552714e-15 | PASS |
| max projection frequency match error | 0.000000e+00 | PASS |

## Figures
| Mode | Figure | Size | Exists |
| --- | --- | --- | --- |
| (1, 0) | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/figures_i1_j0/mkm_resolvent_mode_shapes.pdf | 24.88 KiB | yes |
| (1, 0) | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/figures_i1_j0/mkm_resolvent_gain_bode.pdf | 16.13 KiB | yes |
| (1, 0) | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/figures_i1_j0/mkm_resolvent_peak_location_gain.pdf | 17.21 KiB | yes |
| (1, 0) | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/figures_i1_j0/mkm_resolvent_reconstructed_fields.pdf | 49.56 KiB | yes |
| (1, 1) | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/figures_i1_j1/mkm_resolvent_mode_shapes.pdf | 27.79 KiB | yes |
| (1, 1) | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/figures_i1_j1/mkm_resolvent_gain_bode.pdf | 16.17 KiB | yes |
| (1, 1) | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/figures_i1_j1/mkm_resolvent_peak_location_gain.pdf | 16.30 KiB | yes |
| (1, 1) | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/figures_i1_j1/mkm_resolvent_reconstructed_fields.pdf | 74.16 KiB | yes |
| (2, 0) | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/figures_i2_j0/mkm_resolvent_mode_shapes.pdf | 25.15 KiB | yes |
| (2, 0) | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/figures_i2_j0/mkm_resolvent_gain_bode.pdf | 15.83 KiB | yes |
| (2, 0) | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/figures_i2_j0/mkm_resolvent_peak_location_gain.pdf | 16.58 KiB | yes |
| (2, 0) | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/figures_i2_j0/mkm_resolvent_reconstructed_fields.pdf | 45.06 KiB | yes |
| (2, 1) | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/figures_i2_j1/mkm_resolvent_mode_shapes.pdf | 27.76 KiB | yes |
| (2, 1) | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/figures_i2_j1/mkm_resolvent_gain_bode.pdf | 16.10 KiB | yes |
| (2, 1) | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/figures_i2_j1/mkm_resolvent_peak_location_gain.pdf | 16.47 KiB | yes |
| (2, 1) | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/figures_i2_j1/mkm_resolvent_reconstructed_fields.pdf | 69.66 KiB | yes |
| (4, 1) | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/figures_i4_j1/mkm_resolvent_mode_shapes.pdf | 27.58 KiB | yes |
| (4, 1) | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/figures_i4_j1/mkm_resolvent_gain_bode.pdf | 16.16 KiB | yes |
| (4, 1) | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/figures_i4_j1/mkm_resolvent_peak_location_gain.pdf | 17.02 KiB | yes |
| (4, 1) | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/figures_i4_j1/mkm_resolvent_reconstructed_fields.pdf | 64.38 KiB | yes |

## Diagnostics and Thresholds
| Check | Value | Status | Threshold |
| --- | --- | --- | --- |
| mode (1, 0): response constraint residual | 4.301554e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (1, 0): forcing constraint residual | 4.282450e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (1, 0): response energy norm error | 2.886580e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (1, 0): forcing energy norm error | 3.330669e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (1, 0): projection frequency match error | 0.000000e+00 | PASS | warn>1e-10 |
| mode (1, 1): response constraint residual | 3.487356e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (1, 1): forcing constraint residual | 3.935243e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (1, 1): response energy norm error | 3.330669e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (1, 1): forcing energy norm error | 2.775558e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (1, 1): projection frequency match error | 0.000000e+00 | PASS | warn>1e-10 |
| mode (2, 0): response constraint residual | 4.415236e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (2, 0): forcing constraint residual | 4.379267e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (2, 0): response energy norm error | 3.330669e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (2, 0): forcing energy norm error | 2.220446e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (2, 0): projection frequency match error | 0.000000e+00 | PASS | warn>1e-10 |
| mode (2, 1): response constraint residual | 3.060396e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (2, 1): forcing constraint residual | 3.406053e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (2, 1): response energy norm error | 2.997602e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (2, 1): forcing energy norm error | 2.220446e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (2, 1): projection frequency match error | 0.000000e+00 | PASS | warn>1e-10 |
| mode (4, 1): response constraint residual | 5.187898e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (4, 1): forcing constraint residual | 4.881671e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (4, 1): response energy norm error | 3.108624e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (4, 1): forcing energy norm error | 3.552714e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (4, 1): projection frequency match error | 0.000000e+00 | PASS | warn>1e-10 |
| shared CSD: Parseval relative error | 7.197777e-15 | INFO | diagnostic only for window=hann |

## Caveats
- Projection fractions quantify DNS CSD alignment with the stored response subspace; they do not by themselves model forcing statistics or DNS amplitudes.
- Resolvent/projection comparison requires frequency bins to match the CSD grid within tolerance.
- Hann-window or overlapping CSD Parseval values are reported as estimator diagnostics, not strict pass/fail conservation tests.
- This selected-mode report is not an exhaustive mode sweep and should not be used for broad scaling claims without additional runs.

## Reproduction Command/Config
```json
{
  "target_h5": "/media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/MKM_production_Lx4pi_64_128_32_target_t60_t200.h5",
  "constraint_file": "/media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/MKM_constraints_Lx4pi_N64_128_32_cheb_quadrature_spectral.h5",
  "output_dir": "/media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200",
  "selected_modes": [
    [
      1,
      0
    ],
    [
      1,
      1
    ],
    [
      2,
      0
    ],
    [
      2,
      1
    ],
    [
      4,
      1
    ]
  ],
  "n_singular": 6,
  "re_tau": 180.0,
  "csd": {
    "mode": "computed_csd",
    "path": "/media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/MKM_channel_modal_csd_selected_modes.h5",
    "summary": {
      "output": "/media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/MKM_channel_modal_csd_selected_modes.h5",
      "source": "raw_velocity_fft2_selected_modes",
      "n_modes": 5,
      "n_times": 12000,
      "modal_dim": 192,
      "n_omega": 2048,
      "sample_dt": 0.009999999999990905,
      "segment_length": 2048,
      "n_segments": 10,
      "window": "hann",
      "max_parseval_relative_error": 7.197777362354432e-15
    }
  },
  "omega_selection_by_mode": [
    {
      "mode_index": [
        1,
        0
      ],
      "omega": [
        0.30679615757740725,
        0.6135923151548145,
        0.9203884727322218,
        1.227184630309629,
        1.5339807878870364,
        1.8407769454644436
      ],
      "omega_selection": {
        "kind": "positive_low_frequency_csd_bins",
        "omega_count": 6,
        "source_csd": "/media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/MKM_channel_modal_csd_selected_modes.h5"
      }
    },
    {
      "mode_index": [
        1,
        1
      ],
      "omega": [
        0.30679615757740725,
        0.6135923151548145,
        0.9203884727322218,
        1.227184630309629,
        1.5339807878870364,
        1.8407769454644436
      ],
      "omega_selection": {
        "kind": "positive_low_frequency_csd_bins",
        "omega_count": 6,
        "source_csd": "/media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/MKM_channel_modal_csd_selected_modes.h5"
      }
    },
    {
      "mode_index": [
        2,
        0
      ],
      "omega": [
        0.30679615757740725,
        0.6135923151548145,
        0.9203884727322218,
        1.227184630309629,
        1.5339807878870364,
        1.8407769454644436
      ],
      "omega_selection": {
        "kind": "positive_low_frequency_csd_bins",
        "omega_count": 6,
        "source_csd": "/media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/MKM_channel_modal_csd_selected_modes.h5"
      }
    },
    {
      "mode_index": [
        2,
        1
      ],
      "omega": [
        0.30679615757740725,
        0.6135923151548145,
        0.9203884727322218,
        1.227184630309629,
        1.5339807878870364,
        1.8407769454644436
      ],
      "omega_selection": {
        "kind": "positive_low_frequency_csd_bins",
        "omega_count": 6,
        "source_csd": "/media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/MKM_channel_modal_csd_selected_modes.h5"
      }
    },
    {
      "mode_index": [
        4,
        1
      ],
      "omega": [
        0.30679615757740725,
        0.6135923151548145,
        0.9203884727322218,
        1.227184630309629,
        1.5339807878870364,
        1.8407769454644436
      ],
      "omega_selection": {
        "kind": "positive_low_frequency_csd_bins",
        "omega_count": 6,
        "source_csd": "/media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/MKM_channel_modal_csd_selected_modes.h5"
      }
    }
  ]
}
```

## HDF5 Schema
### /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/MKM_channel_modal_csd_selected_modes.h5
```text
csd/Sqq: shape=(5, 2048, 192, 192) dtype=complex128
csd/component_trace: shape=(5, 2048, 3) dtype=float64
csd/energy_trace: shape=(5, 2048) dtype=float64
csd/trace: shape=(5, 2048) dtype=float64
diagnostics/modal_series_energy_mean: shape=(5,) dtype=float64
diagnostics/parseval_energy_spectrum: shape=(5,) dtype=float64
diagnostics/parseval_energy_time: shape=(5,) dtype=float64
diagnostics/parseval_relative_error: shape=(5,) dtype=float64
diagnostics/weights_z: shape=(64,) dtype=float64
frequencies/omega: shape=(2048,) dtype=float64
geometry/z_wall: shape=(64,) dtype=float64
metadata/demean_temporal: shape=() dtype=bool
metadata/overlap: shape=() dtype=float64
metadata/sample_dt: shape=() dtype=float64
metadata/segment_length: shape=() dtype=int64
metadata/segment_start_indices: shape=(10,) dtype=int32
metadata/selected_keys: shape=(12000,) dtype=object
metadata/selected_times: shape=(12000,) dtype=float64
metadata/source: shape=() dtype=object
metadata/window: shape=() dtype=object
metadata/window_energy: shape=() dtype=float64
mode/index: shape=(5, 2) dtype=int32
mode/k_span: shape=(5,) dtype=float64
mode/k_stream: shape=(5,) dtype=float64
```

### /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/MKM_channel_resolvent_i1_j0.h5
```text
critical_layers/count: shape=(6,) dtype=int32
critical_layers/y_plus_nearest_wall: shape=(6, 2) dtype=float64
critical_layers/z: shape=(6, 2) dtype=float64
diagnostics/basis_constraint_residual: shape=() dtype=float64
diagnostics/constraint_residual_forcing: shape=(6, 6) dtype=float64
diagnostics/constraint_residual_response: shape=(6, 6) dtype=float64
diagnostics/constraint_singular_values: shape=(70,) dtype=float64
diagnostics/energy_orthonormality_error: shape=() dtype=float64
diagnostics/forcing_energy_norm_error: shape=(6, 6) dtype=float64
diagnostics/resolvent_matrix_condition: shape=(6,) dtype=float64
diagnostics/response_energy_norm_error: shape=(6, 6) dtype=float64
frequencies/omega: shape=(6,) dtype=float64
geometry/k_span: shape=(32,) dtype=float64
geometry/k_stream: shape=(128,) dtype=float64
geometry/z_wall: shape=(64,) dtype=float64
mean/U: shape=(64,) dtype=float64
mean/Uprime: shape=(64,) dtype=float64
mode/index: shape=(2,) dtype=int32
mode/kappa: shape=() dtype=float64
mode/lambda: shape=() dtype=float64
resolvent/component_energy_density: shape=(6, 6, 64, 3) dtype=float64
resolvent/forcing_modes: shape=(6, 6, 192) dtype=complex128
resolvent/response_energy_density: shape=(6, 6, 64) dtype=float64
resolvent/response_modes: shape=(6, 6, 192) dtype=complex128
resolvent/singular_values: shape=(6, 6) dtype=float64
```

### /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/MKM_channel_resolvent_projection_i1_j0.h5
```text
diagnostics/frequency_match_error: shape=(6,) dtype=float64
diagnostics/max_response_energy_norm_error: shape=() dtype=float64
diagnostics/mode_match_error: shape=() dtype=float64
diagnostics/negative_fraction_count: shape=() dtype=int64
diagnostics/zero_or_negative_total_energy_count: shape=() dtype=int64
frequencies/csd_index: shape=(6,) dtype=int32
frequencies/csd_omega: shape=(6,) dtype=float64
frequencies/resolvent_omega: shape=(6,) dtype=float64
geometry/z_wall: shape=(64,) dtype=float64
mode/index: shape=(2,) dtype=int32
mode/k_span: shape=() dtype=float64
mode/k_stream: shape=() dtype=float64
projection/cumulative_energy_fraction: shape=(6, 6) dtype=float64
projection/energy_fraction: shape=(6, 6) dtype=float64
projection/energy_total: shape=(6,) dtype=float64
projection/modal_coefficients: shape=(6, 6, 6) dtype=complex128
projection/response_energy_norm: shape=(6, 6) dtype=float64
projection/response_renormalization: shape=(6, 6) dtype=float64
projection/weighted_frobenius_relative_error: shape=(6, 6) dtype=float64
```

### /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/MKM_channel_resolvent_i1_j1.h5
```text
critical_layers/count: shape=(6,) dtype=int32
critical_layers/y_plus_nearest_wall: shape=(6, 2) dtype=float64
critical_layers/z: shape=(6, 2) dtype=float64
diagnostics/basis_constraint_residual: shape=() dtype=float64
diagnostics/constraint_residual_forcing: shape=(6, 6) dtype=float64
diagnostics/constraint_residual_response: shape=(6, 6) dtype=float64
diagnostics/constraint_singular_values: shape=(70,) dtype=float64
diagnostics/energy_orthonormality_error: shape=() dtype=float64
diagnostics/forcing_energy_norm_error: shape=(6, 6) dtype=float64
diagnostics/resolvent_matrix_condition: shape=(6,) dtype=float64
diagnostics/response_energy_norm_error: shape=(6, 6) dtype=float64
frequencies/omega: shape=(6,) dtype=float64
geometry/k_span: shape=(32,) dtype=float64
geometry/k_stream: shape=(128,) dtype=float64
geometry/z_wall: shape=(64,) dtype=float64
mean/U: shape=(64,) dtype=float64
mean/Uprime: shape=(64,) dtype=float64
mode/index: shape=(2,) dtype=int32
mode/kappa: shape=() dtype=float64
mode/lambda: shape=() dtype=float64
resolvent/component_energy_density: shape=(6, 6, 64, 3) dtype=float64
resolvent/forcing_modes: shape=(6, 6, 192) dtype=complex128
resolvent/response_energy_density: shape=(6, 6, 64) dtype=float64
resolvent/response_modes: shape=(6, 6, 192) dtype=complex128
resolvent/singular_values: shape=(6, 6) dtype=float64
```

### /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/MKM_channel_resolvent_projection_i1_j1.h5
```text
diagnostics/frequency_match_error: shape=(6,) dtype=float64
diagnostics/max_response_energy_norm_error: shape=() dtype=float64
diagnostics/mode_match_error: shape=() dtype=float64
diagnostics/negative_fraction_count: shape=() dtype=int64
diagnostics/zero_or_negative_total_energy_count: shape=() dtype=int64
frequencies/csd_index: shape=(6,) dtype=int32
frequencies/csd_omega: shape=(6,) dtype=float64
frequencies/resolvent_omega: shape=(6,) dtype=float64
geometry/z_wall: shape=(64,) dtype=float64
mode/index: shape=(2,) dtype=int32
mode/k_span: shape=() dtype=float64
mode/k_stream: shape=() dtype=float64
projection/cumulative_energy_fraction: shape=(6, 6) dtype=float64
projection/energy_fraction: shape=(6, 6) dtype=float64
projection/energy_total: shape=(6,) dtype=float64
projection/modal_coefficients: shape=(6, 6, 6) dtype=complex128
projection/response_energy_norm: shape=(6, 6) dtype=float64
projection/response_renormalization: shape=(6, 6) dtype=float64
projection/weighted_frobenius_relative_error: shape=(6, 6) dtype=float64
```

### /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/MKM_channel_resolvent_i2_j0.h5
```text
critical_layers/count: shape=(6,) dtype=int32
critical_layers/y_plus_nearest_wall: shape=(6, 2) dtype=float64
critical_layers/z: shape=(6, 2) dtype=float64
diagnostics/basis_constraint_residual: shape=() dtype=float64
diagnostics/constraint_residual_forcing: shape=(6, 6) dtype=float64
diagnostics/constraint_residual_response: shape=(6, 6) dtype=float64
diagnostics/constraint_singular_values: shape=(70,) dtype=float64
diagnostics/energy_orthonormality_error: shape=() dtype=float64
diagnostics/forcing_energy_norm_error: shape=(6, 6) dtype=float64
diagnostics/resolvent_matrix_condition: shape=(6,) dtype=float64
diagnostics/response_energy_norm_error: shape=(6, 6) dtype=float64
frequencies/omega: shape=(6,) dtype=float64
geometry/k_span: shape=(32,) dtype=float64
geometry/k_stream: shape=(128,) dtype=float64
geometry/z_wall: shape=(64,) dtype=float64
mean/U: shape=(64,) dtype=float64
mean/Uprime: shape=(64,) dtype=float64
mode/index: shape=(2,) dtype=int32
mode/kappa: shape=() dtype=float64
mode/lambda: shape=() dtype=float64
resolvent/component_energy_density: shape=(6, 6, 64, 3) dtype=float64
resolvent/forcing_modes: shape=(6, 6, 192) dtype=complex128
resolvent/response_energy_density: shape=(6, 6, 64) dtype=float64
resolvent/response_modes: shape=(6, 6, 192) dtype=complex128
resolvent/singular_values: shape=(6, 6) dtype=float64
```

### /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/MKM_channel_resolvent_projection_i2_j0.h5
```text
diagnostics/frequency_match_error: shape=(6,) dtype=float64
diagnostics/max_response_energy_norm_error: shape=() dtype=float64
diagnostics/mode_match_error: shape=() dtype=float64
diagnostics/negative_fraction_count: shape=() dtype=int64
diagnostics/zero_or_negative_total_energy_count: shape=() dtype=int64
frequencies/csd_index: shape=(6,) dtype=int32
frequencies/csd_omega: shape=(6,) dtype=float64
frequencies/resolvent_omega: shape=(6,) dtype=float64
geometry/z_wall: shape=(64,) dtype=float64
mode/index: shape=(2,) dtype=int32
mode/k_span: shape=() dtype=float64
mode/k_stream: shape=() dtype=float64
projection/cumulative_energy_fraction: shape=(6, 6) dtype=float64
projection/energy_fraction: shape=(6, 6) dtype=float64
projection/energy_total: shape=(6,) dtype=float64
projection/modal_coefficients: shape=(6, 6, 6) dtype=complex128
projection/response_energy_norm: shape=(6, 6) dtype=float64
projection/response_renormalization: shape=(6, 6) dtype=float64
projection/weighted_frobenius_relative_error: shape=(6, 6) dtype=float64
```

### /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/MKM_channel_resolvent_i2_j1.h5
```text
critical_layers/count: shape=(6,) dtype=int32
critical_layers/y_plus_nearest_wall: shape=(6, 2) dtype=float64
critical_layers/z: shape=(6, 2) dtype=float64
diagnostics/basis_constraint_residual: shape=() dtype=float64
diagnostics/constraint_residual_forcing: shape=(6, 6) dtype=float64
diagnostics/constraint_residual_response: shape=(6, 6) dtype=float64
diagnostics/constraint_singular_values: shape=(70,) dtype=float64
diagnostics/energy_orthonormality_error: shape=() dtype=float64
diagnostics/forcing_energy_norm_error: shape=(6, 6) dtype=float64
diagnostics/resolvent_matrix_condition: shape=(6,) dtype=float64
diagnostics/response_energy_norm_error: shape=(6, 6) dtype=float64
frequencies/omega: shape=(6,) dtype=float64
geometry/k_span: shape=(32,) dtype=float64
geometry/k_stream: shape=(128,) dtype=float64
geometry/z_wall: shape=(64,) dtype=float64
mean/U: shape=(64,) dtype=float64
mean/Uprime: shape=(64,) dtype=float64
mode/index: shape=(2,) dtype=int32
mode/kappa: shape=() dtype=float64
mode/lambda: shape=() dtype=float64
resolvent/component_energy_density: shape=(6, 6, 64, 3) dtype=float64
resolvent/forcing_modes: shape=(6, 6, 192) dtype=complex128
resolvent/response_energy_density: shape=(6, 6, 64) dtype=float64
resolvent/response_modes: shape=(6, 6, 192) dtype=complex128
resolvent/singular_values: shape=(6, 6) dtype=float64
```

### /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/MKM_channel_resolvent_projection_i2_j1.h5
```text
diagnostics/frequency_match_error: shape=(6,) dtype=float64
diagnostics/max_response_energy_norm_error: shape=() dtype=float64
diagnostics/mode_match_error: shape=() dtype=float64
diagnostics/negative_fraction_count: shape=() dtype=int64
diagnostics/zero_or_negative_total_energy_count: shape=() dtype=int64
frequencies/csd_index: shape=(6,) dtype=int32
frequencies/csd_omega: shape=(6,) dtype=float64
frequencies/resolvent_omega: shape=(6,) dtype=float64
geometry/z_wall: shape=(64,) dtype=float64
mode/index: shape=(2,) dtype=int32
mode/k_span: shape=() dtype=float64
mode/k_stream: shape=() dtype=float64
projection/cumulative_energy_fraction: shape=(6, 6) dtype=float64
projection/energy_fraction: shape=(6, 6) dtype=float64
projection/energy_total: shape=(6,) dtype=float64
projection/modal_coefficients: shape=(6, 6, 6) dtype=complex128
projection/response_energy_norm: shape=(6, 6) dtype=float64
projection/response_renormalization: shape=(6, 6) dtype=float64
projection/weighted_frobenius_relative_error: shape=(6, 6) dtype=float64
```

### /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/MKM_channel_resolvent_i4_j1.h5
```text
critical_layers/count: shape=(6,) dtype=int32
critical_layers/y_plus_nearest_wall: shape=(6, 2) dtype=float64
critical_layers/z: shape=(6, 2) dtype=float64
diagnostics/basis_constraint_residual: shape=() dtype=float64
diagnostics/constraint_residual_forcing: shape=(6, 6) dtype=float64
diagnostics/constraint_residual_response: shape=(6, 6) dtype=float64
diagnostics/constraint_singular_values: shape=(70,) dtype=float64
diagnostics/energy_orthonormality_error: shape=() dtype=float64
diagnostics/forcing_energy_norm_error: shape=(6, 6) dtype=float64
diagnostics/resolvent_matrix_condition: shape=(6,) dtype=float64
diagnostics/response_energy_norm_error: shape=(6, 6) dtype=float64
frequencies/omega: shape=(6,) dtype=float64
geometry/k_span: shape=(32,) dtype=float64
geometry/k_stream: shape=(128,) dtype=float64
geometry/z_wall: shape=(64,) dtype=float64
mean/U: shape=(64,) dtype=float64
mean/Uprime: shape=(64,) dtype=float64
mode/index: shape=(2,) dtype=int32
mode/kappa: shape=() dtype=float64
mode/lambda: shape=() dtype=float64
resolvent/component_energy_density: shape=(6, 6, 64, 3) dtype=float64
resolvent/forcing_modes: shape=(6, 6, 192) dtype=complex128
resolvent/response_energy_density: shape=(6, 6, 64) dtype=float64
resolvent/response_modes: shape=(6, 6, 192) dtype=complex128
resolvent/singular_values: shape=(6, 6) dtype=float64
```

### /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_dense_t60_t200/MKM_channel_resolvent_projection_i4_j1.h5
```text
diagnostics/frequency_match_error: shape=(6,) dtype=float64
diagnostics/max_response_energy_norm_error: shape=() dtype=float64
diagnostics/mode_match_error: shape=() dtype=float64
diagnostics/negative_fraction_count: shape=() dtype=int64
diagnostics/zero_or_negative_total_energy_count: shape=() dtype=int64
frequencies/csd_index: shape=(6,) dtype=int32
frequencies/csd_omega: shape=(6,) dtype=float64
frequencies/resolvent_omega: shape=(6,) dtype=float64
geometry/z_wall: shape=(64,) dtype=float64
mode/index: shape=(2,) dtype=int32
mode/k_span: shape=() dtype=float64
mode/k_stream: shape=() dtype=float64
projection/cumulative_energy_fraction: shape=(6, 6) dtype=float64
projection/energy_fraction: shape=(6, 6) dtype=float64
projection/energy_total: shape=(6,) dtype=float64
projection/modal_coefficients: shape=(6, 6, 6) dtype=complex128
projection/response_energy_norm: shape=(6, 6) dtype=float64
projection/response_renormalization: shape=(6, 6) dtype=float64
projection/weighted_frobenius_relative_error: shape=(6, 6) dtype=float64
```
