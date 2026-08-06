# MKM Channel Resolvent Selected-Mode Report

## Summary
| Item | Value |
| --- | --- |
| Manifest | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/MKM_channel_resolvent_selected_modes_manifest.json |
| Output directory | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200 |
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
| Shared CSD HDF5 | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/MKM_channel_modal_csd_selected_modes.h5 |

## Shared CSD
| Field | Value |
| --- | --- |
| Path | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/MKM_channel_modal_csd_selected_modes.h5 |
| Size | 1.41 GiB |
| Source | target_modal_u_hat |
| Mode count | 5 |
| n_omega | 512 |
| sample_dt | 0.1 |
| segment_length | 512 |
| n_segments | 4 |
| window | hann |
| max Parseval relative error | 2.933239e-15 |
| Parseval relative errors | 2.138446e-15, 2.933239e-15, 2.876319e-15, 2.252929e-15, 2.434324e-15 |

## Mode Results
### Mode (1, 0)
| Field | Value |
| --- | --- |
| kappa | 0.5 |
| lambda | 0 |
| Resolvent HDF5 | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/MKM_channel_resolvent_i1_j0.h5 |
| Resolvent size | 218.32 KiB |
| Projection HDF5 | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/MKM_channel_resolvent_projection_i1_j0.h5 |
| Projection size | 21.39 KiB |
| Omega selection | positive_low_frequency_csd_bins |

| idx | omega | sigma1 | sigma2 | critical roots | lead fraction | cum fraction | rank1 Fro err |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0.122718 | 0.255031 | 0.218251 | 2 | 0.0982577 | 0.403618 | 0.985304 |
| 1 | 0.245437 | 0.261658 | 0.223182 | 2 | 0.130727 | 0.349096 | 0.978367 |
| 2 | 0.368155 | 0.268594 | 0.228316 | 2 | 0.0943751 | 0.434583 | 0.986613 |
| 3 | 0.490874 | 0.275859 | 0.233664 | 2 | 0.074846 | 0.439358 | 0.993416 |

| Diagnostic | Value | Status |
| --- | --- | --- |
| max response constraint residual | 4.271434e-15 | PASS |
| max forcing constraint residual | 4.304944e-15 | PASS |
| max response energy norm error | 2.442491e-15 | PASS |
| max forcing energy norm error | 2.664535e-15 | PASS |
| max projection frequency match error | 0.000000e+00 | PASS |

### Mode (1, 1)
| Field | Value |
| --- | --- |
| kappa | 0.5 |
| lambda | 2 |
| Resolvent HDF5 | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/MKM_channel_resolvent_i1_j1.h5 |
| Resolvent size | 218.32 KiB |
| Projection HDF5 | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/MKM_channel_resolvent_projection_i1_j1.h5 |
| Projection size | 21.39 KiB |
| Omega selection | positive_low_frequency_csd_bins |

| idx | omega | sigma1 | sigma2 | critical roots | lead fraction | cum fraction | rank1 Fro err |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0.122718 | 0.396685 | 0.389159 | 2 | 0.230144 | 0.41751 | 0.923138 |
| 1 | 0.245437 | 0.409547 | 0.401624 | 2 | 0.178911 | 0.482374 | 0.950823 |
| 2 | 0.368155 | 0.423113 | 0.414765 | 2 | 0.106152 | 0.43357 | 0.982618 |
| 3 | 0.490874 | 0.437435 | 0.42863 | 2 | 0.130706 | 0.423047 | 0.974243 |

| Diagnostic | Value | Status |
| --- | --- | --- |
| max response constraint residual | 3.613979e-15 | PASS |
| max forcing constraint residual | 3.809949e-15 | PASS |
| max response energy norm error | 2.553513e-15 | PASS |
| max forcing energy norm error | 2.442491e-15 | PASS |
| max projection frequency match error | 0.000000e+00 | PASS |

### Mode (2, 0)
| Field | Value |
| --- | --- |
| kappa | 1 |
| lambda | 0 |
| Resolvent HDF5 | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/MKM_channel_resolvent_i2_j0.h5 |
| Resolvent size | 218.32 KiB |
| Projection HDF5 | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/MKM_channel_resolvent_projection_i2_j0.h5 |
| Projection size | 21.39 KiB |
| Omega selection | positive_low_frequency_csd_bins |

| idx | omega | sigma1 | sigma2 | critical roots | lead fraction | cum fraction | rank1 Fro err |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0.122718 | 0.145406 | 0.132245 | 2 | 0.120823 | 0.319133 | 0.977495 |
| 1 | 0.245437 | 0.147479 | 0.133987 | 2 | 0.120193 | 0.298237 | 0.977913 |
| 2 | 0.368155 | 0.149603 | 0.135769 | 2 | 0.0877307 | 0.309066 | 0.98677 |
| 3 | 0.490874 | 0.15178 | 0.137592 | 2 | 0.020364 | 0.300109 | 0.999347 |

| Diagnostic | Value | Status |
| --- | --- | --- |
| max response constraint residual | 4.510664e-15 | PASS |
| max forcing constraint residual | 4.361154e-15 | PASS |
| max response energy norm error | 3.108624e-15 | PASS |
| max forcing energy norm error | 1.776357e-15 | PASS |
| max projection frequency match error | 0.000000e+00 | PASS |

### Mode (2, 1)
| Field | Value |
| --- | --- |
| kappa | 1 |
| lambda | 2 |
| Resolvent HDF5 | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/MKM_channel_resolvent_i2_j1.h5 |
| Resolvent size | 218.32 KiB |
| Projection HDF5 | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/MKM_channel_resolvent_projection_i2_j1.h5 |
| Projection size | 21.39 KiB |
| Omega selection | positive_low_frequency_csd_bins |

| idx | omega | sigma1 | sigma2 | critical roots | lead fraction | cum fraction | rank1 Fro err |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0.122718 | 0.182903 | 0.18059 | 2 | 0.0655299 | 0.327983 | 0.993443 |
| 1 | 0.245437 | 0.18595 | 0.183571 | 2 | 0.0590553 | 0.374398 | 0.995172 |
| 2 | 0.368155 | 0.189084 | 0.186636 | 2 | 0.0561546 | 0.322962 | 0.995433 |
| 3 | 0.490874 | 0.192309 | 0.18979 | 2 | 0.0487503 | 0.343451 | 0.99672 |

| Diagnostic | Value | Status |
| --- | --- | --- |
| max response constraint residual | 2.969364e-15 | PASS |
| max forcing constraint residual | 4.057081e-15 | PASS |
| max response energy norm error | 2.664535e-15 | PASS |
| max forcing energy norm error | 1.998401e-15 | PASS |
| max projection frequency match error | 0.000000e+00 | PASS |

### Mode (4, 1)
| Field | Value |
| --- | --- |
| kappa | 2 |
| lambda | 2 |
| Resolvent HDF5 | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/MKM_channel_resolvent_i4_j1.h5 |
| Resolvent size | 218.32 KiB |
| Projection HDF5 | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/MKM_channel_resolvent_projection_i4_j1.h5 |
| Projection size | 21.39 KiB |
| Omega selection | positive_low_frequency_csd_bins |

| idx | omega | sigma1 | sigma2 | critical roots | lead fraction | cum fraction | rank1 Fro err |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0.122718 | 0.0918099 | 0.0912233 | 2 | 0.070883 | 0.273344 | 0.992572 |
| 1 | 0.245437 | 0.0926213 | 0.092025 | 2 | 0.0882562 | 0.2821 | 0.987082 |
| 2 | 0.368155 | 0.0934452 | 0.092839 | 2 | 0.0807452 | 0.236519 | 0.990126 |
| 3 | 0.490874 | 0.0942818 | 0.0936654 | 2 | 0.0438109 | 0.235196 | 0.996458 |

| Diagnostic | Value | Status |
| --- | --- | --- |
| max response constraint residual | 5.245373e-15 | PASS |
| max forcing constraint residual | 4.568309e-15 | PASS |
| max response energy norm error | 2.664535e-15 | PASS |
| max forcing energy norm error | 3.330669e-15 | PASS |
| max projection frequency match error | 0.000000e+00 | PASS |

## Figures
| Mode | Figure | Size | Exists |
| --- | --- | --- | --- |
| (1, 0) | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/figures_i1_j0/mkm_resolvent_mode_shapes.pdf | 24.12 KiB | yes |
| (1, 0) | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/figures_i1_j0/mkm_resolvent_gain_bode.pdf | 16.13 KiB | yes |
| (1, 0) | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/figures_i1_j0/mkm_resolvent_peak_location_gain.pdf | 16.46 KiB | yes |
| (1, 0) | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/figures_i1_j0/mkm_resolvent_reconstructed_fields.pdf | 49.89 KiB | yes |
| (1, 1) | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/figures_i1_j1/mkm_resolvent_mode_shapes.pdf | 27.03 KiB | yes |
| (1, 1) | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/figures_i1_j1/mkm_resolvent_gain_bode.pdf | 15.40 KiB | yes |
| (1, 1) | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/figures_i1_j1/mkm_resolvent_peak_location_gain.pdf | 17.48 KiB | yes |
| (1, 1) | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/figures_i1_j1/mkm_resolvent_reconstructed_fields.pdf | 74.32 KiB | yes |
| (2, 0) | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/figures_i2_j0/mkm_resolvent_mode_shapes.pdf | 24.42 KiB | yes |
| (2, 0) | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/figures_i2_j0/mkm_resolvent_gain_bode.pdf | 16.32 KiB | yes |
| (2, 0) | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/figures_i2_j0/mkm_resolvent_peak_location_gain.pdf | 17.41 KiB | yes |
| (2, 0) | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/figures_i2_j0/mkm_resolvent_reconstructed_fields.pdf | 45.00 KiB | yes |
| (2, 1) | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/figures_i2_j1/mkm_resolvent_mode_shapes.pdf | 27.03 KiB | yes |
| (2, 1) | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/figures_i2_j1/mkm_resolvent_gain_bode.pdf | 15.41 KiB | yes |
| (2, 1) | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/figures_i2_j1/mkm_resolvent_peak_location_gain.pdf | 17.31 KiB | yes |
| (2, 1) | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/figures_i2_j1/mkm_resolvent_reconstructed_fields.pdf | 69.53 KiB | yes |
| (4, 1) | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/figures_i4_j1/mkm_resolvent_mode_shapes.pdf | 26.88 KiB | yes |
| (4, 1) | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/figures_i4_j1/mkm_resolvent_gain_bode.pdf | 16.56 KiB | yes |
| (4, 1) | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/figures_i4_j1/mkm_resolvent_peak_location_gain.pdf | 16.42 KiB | yes |
| (4, 1) | /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/figures_i4_j1/mkm_resolvent_reconstructed_fields.pdf | 63.19 KiB | yes |

## Diagnostics and Thresholds
| Check | Value | Status | Threshold |
| --- | --- | --- | --- |
| mode (1, 0): response constraint residual | 4.271434e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (1, 0): forcing constraint residual | 4.304944e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (1, 0): response energy norm error | 2.442491e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (1, 0): forcing energy norm error | 2.664535e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (1, 0): projection frequency match error | 0.000000e+00 | PASS | warn>1e-10 |
| mode (1, 1): response constraint residual | 3.613979e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (1, 1): forcing constraint residual | 3.809949e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (1, 1): response energy norm error | 2.553513e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (1, 1): forcing energy norm error | 2.442491e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (1, 1): projection frequency match error | 0.000000e+00 | PASS | warn>1e-10 |
| mode (2, 0): response constraint residual | 4.510664e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (2, 0): forcing constraint residual | 4.361154e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (2, 0): response energy norm error | 3.108624e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (2, 0): forcing energy norm error | 1.776357e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (2, 0): projection frequency match error | 0.000000e+00 | PASS | warn>1e-10 |
| mode (2, 1): response constraint residual | 2.969364e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (2, 1): forcing constraint residual | 4.057081e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (2, 1): response energy norm error | 2.664535e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (2, 1): forcing energy norm error | 1.998401e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (2, 1): projection frequency match error | 0.000000e+00 | PASS | warn>1e-10 |
| mode (4, 1): response constraint residual | 5.245373e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (4, 1): forcing constraint residual | 4.568309e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (4, 1): response energy norm error | 2.664535e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (4, 1): forcing energy norm error | 3.330669e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (4, 1): projection frequency match error | 0.000000e+00 | PASS | warn>1e-10 |
| shared CSD: Parseval relative error | 2.933239e-15 | INFO | diagnostic only for window=hann |

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
  "output_dir": "/media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200",
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
    "path": "/media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/MKM_channel_modal_csd_selected_modes.h5",
    "summary": {
      "output": "/media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/MKM_channel_modal_csd_selected_modes.h5",
      "source": "target_modal_u_hat",
      "n_modes": 5,
      "n_times": 1401,
      "modal_dim": 192,
      "n_omega": 512,
      "sample_dt": 0.09999999999999432,
      "segment_length": 512,
      "n_segments": 4,
      "window": "hann",
      "max_parseval_relative_error": 2.9332393435058758e-15
    }
  },
  "omega_selection_by_mode": [
    {
      "mode_index": [
        1,
        0
      ],
      "omega": [
        0.12271846303085827,
        0.24543692606171655,
        0.3681553890925748,
        0.4908738521234331
      ],
      "omega_selection": {
        "kind": "positive_low_frequency_csd_bins",
        "omega_count": 4,
        "source_csd": "/media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/MKM_channel_modal_csd_selected_modes.h5"
      }
    },
    {
      "mode_index": [
        1,
        1
      ],
      "omega": [
        0.12271846303085827,
        0.24543692606171655,
        0.3681553890925748,
        0.4908738521234331
      ],
      "omega_selection": {
        "kind": "positive_low_frequency_csd_bins",
        "omega_count": 4,
        "source_csd": "/media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/MKM_channel_modal_csd_selected_modes.h5"
      }
    },
    {
      "mode_index": [
        2,
        0
      ],
      "omega": [
        0.12271846303085827,
        0.24543692606171655,
        0.3681553890925748,
        0.4908738521234331
      ],
      "omega_selection": {
        "kind": "positive_low_frequency_csd_bins",
        "omega_count": 4,
        "source_csd": "/media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/MKM_channel_modal_csd_selected_modes.h5"
      }
    },
    {
      "mode_index": [
        2,
        1
      ],
      "omega": [
        0.12271846303085827,
        0.24543692606171655,
        0.3681553890925748,
        0.4908738521234331
      ],
      "omega_selection": {
        "kind": "positive_low_frequency_csd_bins",
        "omega_count": 4,
        "source_csd": "/media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/MKM_channel_modal_csd_selected_modes.h5"
      }
    },
    {
      "mode_index": [
        4,
        1
      ],
      "omega": [
        0.12271846303085827,
        0.24543692606171655,
        0.3681553890925748,
        0.4908738521234331
      ],
      "omega_selection": {
        "kind": "positive_low_frequency_csd_bins",
        "omega_count": 4,
        "source_csd": "/media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/MKM_channel_modal_csd_selected_modes.h5"
      }
    }
  ]
}
```

## HDF5 Schema
### /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/MKM_channel_modal_csd_selected_modes.h5
```text
csd/Sqq: shape=(5, 512, 192, 192) dtype=complex128
csd/component_trace: shape=(5, 512, 3) dtype=float64
csd/energy_trace: shape=(5, 512) dtype=float64
csd/trace: shape=(5, 512) dtype=float64
diagnostics/modal_series_energy_mean: shape=(5,) dtype=float64
diagnostics/parseval_energy_spectrum: shape=(5,) dtype=float64
diagnostics/parseval_energy_time: shape=(5,) dtype=float64
diagnostics/parseval_relative_error: shape=(5,) dtype=float64
diagnostics/weights_z: shape=(64,) dtype=float64
frequencies/omega: shape=(512,) dtype=float64
geometry/z_wall: shape=(64,) dtype=float64
metadata/demean_temporal: shape=() dtype=bool
metadata/overlap: shape=() dtype=float64
metadata/sample_dt: shape=() dtype=float64
metadata/segment_length: shape=() dtype=int64
metadata/segment_start_indices: shape=(4,) dtype=int32
metadata/selected_keys: shape=(1401,) dtype=object
metadata/selected_times: shape=(1401,) dtype=float64
metadata/source: shape=() dtype=object
metadata/window: shape=() dtype=object
metadata/window_energy: shape=() dtype=float64
mode/index: shape=(5, 2) dtype=int32
mode/k_span: shape=(5,) dtype=float64
mode/k_stream: shape=(5,) dtype=float64
```

### /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/MKM_channel_resolvent_i1_j0.h5
```text
critical_layers/count: shape=(4,) dtype=int32
critical_layers/y_plus_nearest_wall: shape=(4, 2) dtype=float64
critical_layers/z: shape=(4, 2) dtype=float64
diagnostics/basis_constraint_residual: shape=() dtype=float64
diagnostics/constraint_residual_forcing: shape=(4, 6) dtype=float64
diagnostics/constraint_residual_response: shape=(4, 6) dtype=float64
diagnostics/constraint_singular_values: shape=(70,) dtype=float64
diagnostics/energy_orthonormality_error: shape=() dtype=float64
diagnostics/forcing_energy_norm_error: shape=(4, 6) dtype=float64
diagnostics/resolvent_matrix_condition: shape=(4,) dtype=float64
diagnostics/response_energy_norm_error: shape=(4, 6) dtype=float64
frequencies/omega: shape=(4,) dtype=float64
geometry/k_span: shape=(32,) dtype=float64
geometry/k_stream: shape=(128,) dtype=float64
geometry/z_wall: shape=(64,) dtype=float64
mean/U: shape=(64,) dtype=float64
mean/Uprime: shape=(64,) dtype=float64
mode/index: shape=(2,) dtype=int32
mode/kappa: shape=() dtype=float64
mode/lambda: shape=() dtype=float64
resolvent/component_energy_density: shape=(4, 6, 64, 3) dtype=float64
resolvent/forcing_modes: shape=(4, 6, 192) dtype=complex128
resolvent/response_energy_density: shape=(4, 6, 64) dtype=float64
resolvent/response_modes: shape=(4, 6, 192) dtype=complex128
resolvent/singular_values: shape=(4, 6) dtype=float64
```

### /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/MKM_channel_resolvent_projection_i1_j0.h5
```text
diagnostics/frequency_match_error: shape=(4,) dtype=float64
diagnostics/max_response_energy_norm_error: shape=() dtype=float64
diagnostics/mode_match_error: shape=() dtype=float64
diagnostics/negative_fraction_count: shape=() dtype=int64
diagnostics/zero_or_negative_total_energy_count: shape=() dtype=int64
frequencies/csd_index: shape=(4,) dtype=int32
frequencies/csd_omega: shape=(4,) dtype=float64
frequencies/resolvent_omega: shape=(4,) dtype=float64
geometry/z_wall: shape=(64,) dtype=float64
mode/index: shape=(2,) dtype=int32
mode/k_span: shape=() dtype=float64
mode/k_stream: shape=() dtype=float64
projection/cumulative_energy_fraction: shape=(4, 6) dtype=float64
projection/energy_fraction: shape=(4, 6) dtype=float64
projection/energy_total: shape=(4,) dtype=float64
projection/modal_coefficients: shape=(4, 6, 6) dtype=complex128
projection/response_energy_norm: shape=(4, 6) dtype=float64
projection/response_renormalization: shape=(4, 6) dtype=float64
projection/weighted_frobenius_relative_error: shape=(4, 6) dtype=float64
```

### /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/MKM_channel_resolvent_i1_j1.h5
```text
critical_layers/count: shape=(4,) dtype=int32
critical_layers/y_plus_nearest_wall: shape=(4, 2) dtype=float64
critical_layers/z: shape=(4, 2) dtype=float64
diagnostics/basis_constraint_residual: shape=() dtype=float64
diagnostics/constraint_residual_forcing: shape=(4, 6) dtype=float64
diagnostics/constraint_residual_response: shape=(4, 6) dtype=float64
diagnostics/constraint_singular_values: shape=(70,) dtype=float64
diagnostics/energy_orthonormality_error: shape=() dtype=float64
diagnostics/forcing_energy_norm_error: shape=(4, 6) dtype=float64
diagnostics/resolvent_matrix_condition: shape=(4,) dtype=float64
diagnostics/response_energy_norm_error: shape=(4, 6) dtype=float64
frequencies/omega: shape=(4,) dtype=float64
geometry/k_span: shape=(32,) dtype=float64
geometry/k_stream: shape=(128,) dtype=float64
geometry/z_wall: shape=(64,) dtype=float64
mean/U: shape=(64,) dtype=float64
mean/Uprime: shape=(64,) dtype=float64
mode/index: shape=(2,) dtype=int32
mode/kappa: shape=() dtype=float64
mode/lambda: shape=() dtype=float64
resolvent/component_energy_density: shape=(4, 6, 64, 3) dtype=float64
resolvent/forcing_modes: shape=(4, 6, 192) dtype=complex128
resolvent/response_energy_density: shape=(4, 6, 64) dtype=float64
resolvent/response_modes: shape=(4, 6, 192) dtype=complex128
resolvent/singular_values: shape=(4, 6) dtype=float64
```

### /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/MKM_channel_resolvent_projection_i1_j1.h5
```text
diagnostics/frequency_match_error: shape=(4,) dtype=float64
diagnostics/max_response_energy_norm_error: shape=() dtype=float64
diagnostics/mode_match_error: shape=() dtype=float64
diagnostics/negative_fraction_count: shape=() dtype=int64
diagnostics/zero_or_negative_total_energy_count: shape=() dtype=int64
frequencies/csd_index: shape=(4,) dtype=int32
frequencies/csd_omega: shape=(4,) dtype=float64
frequencies/resolvent_omega: shape=(4,) dtype=float64
geometry/z_wall: shape=(64,) dtype=float64
mode/index: shape=(2,) dtype=int32
mode/k_span: shape=() dtype=float64
mode/k_stream: shape=() dtype=float64
projection/cumulative_energy_fraction: shape=(4, 6) dtype=float64
projection/energy_fraction: shape=(4, 6) dtype=float64
projection/energy_total: shape=(4,) dtype=float64
projection/modal_coefficients: shape=(4, 6, 6) dtype=complex128
projection/response_energy_norm: shape=(4, 6) dtype=float64
projection/response_renormalization: shape=(4, 6) dtype=float64
projection/weighted_frobenius_relative_error: shape=(4, 6) dtype=float64
```

### /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/MKM_channel_resolvent_i2_j0.h5
```text
critical_layers/count: shape=(4,) dtype=int32
critical_layers/y_plus_nearest_wall: shape=(4, 2) dtype=float64
critical_layers/z: shape=(4, 2) dtype=float64
diagnostics/basis_constraint_residual: shape=() dtype=float64
diagnostics/constraint_residual_forcing: shape=(4, 6) dtype=float64
diagnostics/constraint_residual_response: shape=(4, 6) dtype=float64
diagnostics/constraint_singular_values: shape=(70,) dtype=float64
diagnostics/energy_orthonormality_error: shape=() dtype=float64
diagnostics/forcing_energy_norm_error: shape=(4, 6) dtype=float64
diagnostics/resolvent_matrix_condition: shape=(4,) dtype=float64
diagnostics/response_energy_norm_error: shape=(4, 6) dtype=float64
frequencies/omega: shape=(4,) dtype=float64
geometry/k_span: shape=(32,) dtype=float64
geometry/k_stream: shape=(128,) dtype=float64
geometry/z_wall: shape=(64,) dtype=float64
mean/U: shape=(64,) dtype=float64
mean/Uprime: shape=(64,) dtype=float64
mode/index: shape=(2,) dtype=int32
mode/kappa: shape=() dtype=float64
mode/lambda: shape=() dtype=float64
resolvent/component_energy_density: shape=(4, 6, 64, 3) dtype=float64
resolvent/forcing_modes: shape=(4, 6, 192) dtype=complex128
resolvent/response_energy_density: shape=(4, 6, 64) dtype=float64
resolvent/response_modes: shape=(4, 6, 192) dtype=complex128
resolvent/singular_values: shape=(4, 6) dtype=float64
```

### /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/MKM_channel_resolvent_projection_i2_j0.h5
```text
diagnostics/frequency_match_error: shape=(4,) dtype=float64
diagnostics/max_response_energy_norm_error: shape=() dtype=float64
diagnostics/mode_match_error: shape=() dtype=float64
diagnostics/negative_fraction_count: shape=() dtype=int64
diagnostics/zero_or_negative_total_energy_count: shape=() dtype=int64
frequencies/csd_index: shape=(4,) dtype=int32
frequencies/csd_omega: shape=(4,) dtype=float64
frequencies/resolvent_omega: shape=(4,) dtype=float64
geometry/z_wall: shape=(64,) dtype=float64
mode/index: shape=(2,) dtype=int32
mode/k_span: shape=() dtype=float64
mode/k_stream: shape=() dtype=float64
projection/cumulative_energy_fraction: shape=(4, 6) dtype=float64
projection/energy_fraction: shape=(4, 6) dtype=float64
projection/energy_total: shape=(4,) dtype=float64
projection/modal_coefficients: shape=(4, 6, 6) dtype=complex128
projection/response_energy_norm: shape=(4, 6) dtype=float64
projection/response_renormalization: shape=(4, 6) dtype=float64
projection/weighted_frobenius_relative_error: shape=(4, 6) dtype=float64
```

### /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/MKM_channel_resolvent_i2_j1.h5
```text
critical_layers/count: shape=(4,) dtype=int32
critical_layers/y_plus_nearest_wall: shape=(4, 2) dtype=float64
critical_layers/z: shape=(4, 2) dtype=float64
diagnostics/basis_constraint_residual: shape=() dtype=float64
diagnostics/constraint_residual_forcing: shape=(4, 6) dtype=float64
diagnostics/constraint_residual_response: shape=(4, 6) dtype=float64
diagnostics/constraint_singular_values: shape=(70,) dtype=float64
diagnostics/energy_orthonormality_error: shape=() dtype=float64
diagnostics/forcing_energy_norm_error: shape=(4, 6) dtype=float64
diagnostics/resolvent_matrix_condition: shape=(4,) dtype=float64
diagnostics/response_energy_norm_error: shape=(4, 6) dtype=float64
frequencies/omega: shape=(4,) dtype=float64
geometry/k_span: shape=(32,) dtype=float64
geometry/k_stream: shape=(128,) dtype=float64
geometry/z_wall: shape=(64,) dtype=float64
mean/U: shape=(64,) dtype=float64
mean/Uprime: shape=(64,) dtype=float64
mode/index: shape=(2,) dtype=int32
mode/kappa: shape=() dtype=float64
mode/lambda: shape=() dtype=float64
resolvent/component_energy_density: shape=(4, 6, 64, 3) dtype=float64
resolvent/forcing_modes: shape=(4, 6, 192) dtype=complex128
resolvent/response_energy_density: shape=(4, 6, 64) dtype=float64
resolvent/response_modes: shape=(4, 6, 192) dtype=complex128
resolvent/singular_values: shape=(4, 6) dtype=float64
```

### /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/MKM_channel_resolvent_projection_i2_j1.h5
```text
diagnostics/frequency_match_error: shape=(4,) dtype=float64
diagnostics/max_response_energy_norm_error: shape=() dtype=float64
diagnostics/mode_match_error: shape=() dtype=float64
diagnostics/negative_fraction_count: shape=() dtype=int64
diagnostics/zero_or_negative_total_energy_count: shape=() dtype=int64
frequencies/csd_index: shape=(4,) dtype=int32
frequencies/csd_omega: shape=(4,) dtype=float64
frequencies/resolvent_omega: shape=(4,) dtype=float64
geometry/z_wall: shape=(64,) dtype=float64
mode/index: shape=(2,) dtype=int32
mode/k_span: shape=() dtype=float64
mode/k_stream: shape=() dtype=float64
projection/cumulative_energy_fraction: shape=(4, 6) dtype=float64
projection/energy_fraction: shape=(4, 6) dtype=float64
projection/energy_total: shape=(4,) dtype=float64
projection/modal_coefficients: shape=(4, 6, 6) dtype=complex128
projection/response_energy_norm: shape=(4, 6) dtype=float64
projection/response_renormalization: shape=(4, 6) dtype=float64
projection/weighted_frobenius_relative_error: shape=(4, 6) dtype=float64
```

### /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/MKM_channel_resolvent_i4_j1.h5
```text
critical_layers/count: shape=(4,) dtype=int32
critical_layers/y_plus_nearest_wall: shape=(4, 2) dtype=float64
critical_layers/z: shape=(4, 2) dtype=float64
diagnostics/basis_constraint_residual: shape=() dtype=float64
diagnostics/constraint_residual_forcing: shape=(4, 6) dtype=float64
diagnostics/constraint_residual_response: shape=(4, 6) dtype=float64
diagnostics/constraint_singular_values: shape=(70,) dtype=float64
diagnostics/energy_orthonormality_error: shape=() dtype=float64
diagnostics/forcing_energy_norm_error: shape=(4, 6) dtype=float64
diagnostics/resolvent_matrix_condition: shape=(4,) dtype=float64
diagnostics/response_energy_norm_error: shape=(4, 6) dtype=float64
frequencies/omega: shape=(4,) dtype=float64
geometry/k_span: shape=(32,) dtype=float64
geometry/k_stream: shape=(128,) dtype=float64
geometry/z_wall: shape=(64,) dtype=float64
mean/U: shape=(64,) dtype=float64
mean/Uprime: shape=(64,) dtype=float64
mode/index: shape=(2,) dtype=int32
mode/kappa: shape=() dtype=float64
mode/lambda: shape=() dtype=float64
resolvent/component_energy_density: shape=(4, 6, 64, 3) dtype=float64
resolvent/forcing_modes: shape=(4, 6, 192) dtype=complex128
resolvent/response_energy_density: shape=(4, 6, 64) dtype=float64
resolvent/response_modes: shape=(4, 6, 192) dtype=complex128
resolvent/singular_values: shape=(4, 6) dtype=float64
```

### /media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713/channel_resolvent_selected_modes_target_t60_t200/MKM_channel_resolvent_projection_i4_j1.h5
```text
diagnostics/frequency_match_error: shape=(4,) dtype=float64
diagnostics/max_response_energy_norm_error: shape=() dtype=float64
diagnostics/mode_match_error: shape=() dtype=float64
diagnostics/negative_fraction_count: shape=() dtype=int64
diagnostics/zero_or_negative_total_energy_count: shape=() dtype=int64
frequencies/csd_index: shape=(4,) dtype=int32
frequencies/csd_omega: shape=(4,) dtype=float64
frequencies/resolvent_omega: shape=(4,) dtype=float64
geometry/z_wall: shape=(64,) dtype=float64
mode/index: shape=(2,) dtype=int32
mode/k_span: shape=() dtype=float64
mode/k_stream: shape=() dtype=float64
projection/cumulative_energy_fraction: shape=(4, 6) dtype=float64
projection/energy_fraction: shape=(4, 6) dtype=float64
projection/energy_total: shape=(4,) dtype=float64
projection/modal_coefficients: shape=(4, 6, 6) dtype=complex128
projection/response_energy_norm: shape=(4, 6) dtype=float64
projection/response_renormalization: shape=(4, 6) dtype=float64
projection/weighted_frobenius_relative_error: shape=(4, 6) dtype=float64
```
