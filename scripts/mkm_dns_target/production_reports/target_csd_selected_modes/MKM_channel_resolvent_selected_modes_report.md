# MKM Channel Resolvent Selected-Mode Report

## Summary
| Item | Value |
| --- | --- |
| Manifest | /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes/MKM_channel_resolvent_selected_modes_manifest.json |
| Output directory | /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes |
| Selected modes | [[1, 0], [1, 1], [2, 1]] |
| Reported modes | 3 |
| Truncated modes | 0 |
| n_singular | 6 |
| Re_tau | 180.0 |

## Inputs
| Input | Path |
| --- | --- |
| Target HDF5 | /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/MKM_production_64_64_32_target_t60_t180.h5 |
| Constraint HDF5 | /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/MKM_constraints_N64_64_32_cheb_quadrature_spectral.h5 |
| Shared CSD HDF5 | /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes/MKM_channel_modal_csd_selected_modes.h5 |

## Shared CSD
| Field | Value |
| --- | --- |
| Path | /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes/MKM_channel_modal_csd_selected_modes.h5 |
| Size | 864.14 MiB |
| Source | target_modal_u_hat |
| Mode count | 3 |
| n_omega | 512 |
| sample_dt | 0.1 |
| segment_length | 512 |
| n_segments | 3 |
| window | hann |
| max Parseval relative error | 2.932579e-15 |
| Parseval relative errors | 2.184012e-15, 2.932579e-15, 2.772455e-15 |

## Mode Results
### Mode (1, 0)
| Field | Value |
| --- | --- |
| kappa | 1 |
| lambda | 0 |
| Resolvent HDF5 | /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes/MKM_channel_resolvent_i1_j0.h5 |
| Resolvent size | 217.77 KiB |
| Projection HDF5 | /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes/MKM_channel_resolvent_projection_i1_j0.h5 |
| Projection size | 21.39 KiB |
| Omega selection | positive_low_frequency_csd_bins |

| idx | omega | sigma1 | sigma2 | critical roots | lead fraction | cum fraction | rank1 Fro err |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0.122718 | 0.14589 | 0.13271 | 2 | 0.108022 | 0.353601 | 0.983823 |
| 1 | 0.245437 | 0.147973 | 0.134462 | 2 | 0.0377024 | 0.241945 | 0.998153 |
| 2 | 0.368155 | 0.150108 | 0.136254 | 2 | 0.123227 | 0.407893 | 0.981325 |
| 3 | 0.490874 | 0.152295 | 0.138088 | 2 | 0.0565114 | 0.406697 | 0.996223 |

| Diagnostic | Value | Status |
| --- | --- | --- |
| max response constraint residual | 4.464121e-15 | PASS |
| max forcing constraint residual | 4.347218e-15 | PASS |
| max response energy norm error | 2.220446e-15 | PASS |
| max forcing energy norm error | 2.664535e-15 | PASS |
| max projection frequency match error | 0.000000e+00 | PASS |

### Mode (1, 1)
| Field | Value |
| --- | --- |
| kappa | 1 |
| lambda | 2 |
| Resolvent HDF5 | /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes/MKM_channel_resolvent_i1_j1.h5 |
| Resolvent size | 217.77 KiB |
| Projection HDF5 | /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes/MKM_channel_resolvent_projection_i1_j1.h5 |
| Projection size | 21.39 KiB |
| Omega selection | positive_low_frequency_csd_bins |

| idx | omega | sigma1 | sigma2 | critical roots | lead fraction | cum fraction | rank1 Fro err |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0.122718 | 0.183654 | 0.181528 | 2 | 0.158274 | 0.387042 | 0.97073 |
| 1 | 0.245437 | 0.186719 | 0.184533 | 2 | 0.161356 | 0.472809 | 0.973558 |
| 2 | 0.368155 | 0.189871 | 0.187623 | 2 | 0.114346 | 0.490194 | 0.983972 |
| 3 | 0.490874 | 0.193115 | 0.190802 | 2 | 0.034472 | 0.317179 | 0.998597 |

| Diagnostic | Value | Status |
| --- | --- | --- |
| max response constraint residual | 3.016616e-15 | PASS |
| max forcing constraint residual | 2.997259e-15 | PASS |
| max response energy norm error | 1.887379e-15 | PASS |
| max forcing energy norm error | 1.998401e-15 | PASS |
| max projection frequency match error | 0.000000e+00 | PASS |

### Mode (2, 1)
| Field | Value |
| --- | --- |
| kappa | 2 |
| lambda | 2 |
| Resolvent HDF5 | /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes/MKM_channel_resolvent_i2_j1.h5 |
| Resolvent size | 217.77 KiB |
| Projection HDF5 | /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes/MKM_channel_resolvent_projection_i2_j1.h5 |
| Projection size | 21.39 KiB |
| Omega selection | positive_low_frequency_csd_bins |

| idx | omega | sigma1 | sigma2 | critical roots | lead fraction | cum fraction | rank1 Fro err |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0.122718 | 0.0920781 | 0.0916955 | 2 | 0.0278054 | 0.260677 | 0.999127 |
| 1 | 0.245437 | 0.0928937 | 0.0925051 | 2 | 0.0590743 | 0.215853 | 0.995251 |
| 2 | 0.368155 | 0.0937217 | 0.0933271 | 2 | 0.0572881 | 0.265905 | 0.995814 |
| 3 | 0.490874 | 0.0945626 | 0.0941619 | 2 | 0.0539067 | 0.233041 | 0.996511 |

| Diagnostic | Value | Status |
| --- | --- | --- |
| max response constraint residual | 4.889762e-15 | PASS |
| max forcing constraint residual | 4.712708e-15 | PASS |
| max response energy norm error | 2.220446e-15 | PASS |
| max forcing energy norm error | 3.108624e-15 | PASS |
| max projection frequency match error | 0.000000e+00 | PASS |

## Figures
| Mode | Figure | Size | Exists |
| --- | --- | --- | --- |
| (1, 0) | /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes/figures_i1_j0/mkm_resolvent_mode_shapes.pdf | 24.45 KiB | yes |
| (1, 0) | /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes/figures_i1_j0/mkm_resolvent_gain_bode.pdf | 16.33 KiB | yes |
| (1, 0) | /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes/figures_i1_j0/mkm_resolvent_peak_location_gain.pdf | 17.38 KiB | yes |
| (1, 0) | /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes/figures_i1_j0/mkm_resolvent_reconstructed_fields.pdf | 44.77 KiB | yes |
| (1, 1) | /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes/figures_i1_j1/mkm_resolvent_mode_shapes.pdf | 26.96 KiB | yes |
| (1, 1) | /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes/figures_i1_j1/mkm_resolvent_gain_bode.pdf | 15.42 KiB | yes |
| (1, 1) | /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes/figures_i1_j1/mkm_resolvent_peak_location_gain.pdf | 17.33 KiB | yes |
| (1, 1) | /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes/figures_i1_j1/mkm_resolvent_reconstructed_fields.pdf | 73.73 KiB | yes |
| (2, 1) | /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes/figures_i2_j1/mkm_resolvent_mode_shapes.pdf | 26.77 KiB | yes |
| (2, 1) | /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes/figures_i2_j1/mkm_resolvent_gain_bode.pdf | 16.56 KiB | yes |
| (2, 1) | /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes/figures_i2_j1/mkm_resolvent_peak_location_gain.pdf | 16.45 KiB | yes |
| (2, 1) | /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes/figures_i2_j1/mkm_resolvent_reconstructed_fields.pdf | 72.19 KiB | yes |

## Diagnostics and Thresholds
| Check | Value | Status | Threshold |
| --- | --- | --- | --- |
| mode (1, 0): response constraint residual | 4.464121e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (1, 0): forcing constraint residual | 4.347218e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (1, 0): response energy norm error | 2.220446e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (1, 0): forcing energy norm error | 2.664535e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (1, 0): projection frequency match error | 0.000000e+00 | PASS | warn>1e-10 |
| mode (1, 1): response constraint residual | 3.016616e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (1, 1): forcing constraint residual | 2.997259e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (1, 1): response energy norm error | 1.887379e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (1, 1): forcing energy norm error | 1.998401e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (1, 1): projection frequency match error | 0.000000e+00 | PASS | warn>1e-10 |
| mode (2, 1): response constraint residual | 4.889762e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (2, 1): forcing constraint residual | 4.712708e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (2, 1): response energy norm error | 2.220446e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (2, 1): forcing energy norm error | 3.108624e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (2, 1): projection frequency match error | 0.000000e+00 | PASS | warn>1e-10 |
| shared CSD: Parseval relative error | 2.932579e-15 | INFO | diagnostic only for window=hann |

## Caveats
- Projection fractions quantify DNS CSD alignment with the stored response subspace; they do not by themselves model forcing statistics or DNS amplitudes.
- Resolvent/projection comparison requires frequency bins to match the CSD grid within tolerance.
- Hann-window or overlapping CSD Parseval values are reported as estimator diagnostics, not strict pass/fail conservation tests.
- This selected-mode report is not an exhaustive mode sweep and should not be used for broad scaling claims without additional runs.

## Reproduction Command/Config
```json
{
  "target_h5": "/media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/MKM_production_64_64_32_target_t60_t180.h5",
  "constraint_file": "/media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/MKM_constraints_N64_64_32_cheb_quadrature_spectral.h5",
  "output_dir": "/media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes",
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
      1
    ]
  ],
  "n_singular": 6,
  "re_tau": 180.0,
  "csd": {
    "mode": "computed_csd",
    "path": "/media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes/MKM_channel_modal_csd_selected_modes.h5",
    "summary": {
      "output": "/media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes/MKM_channel_modal_csd_selected_modes.h5",
      "source": "target_modal_u_hat",
      "n_modes": 3,
      "n_times": 1201,
      "modal_dim": 192,
      "n_omega": 512,
      "sample_dt": 0.09999999999999432,
      "segment_length": 512,
      "n_segments": 3,
      "window": "hann",
      "max_parseval_relative_error": 2.93257888998019e-15
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
        "source_csd": "/media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes/MKM_channel_modal_csd_selected_modes.h5"
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
        "source_csd": "/media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes/MKM_channel_modal_csd_selected_modes.h5"
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
        "source_csd": "/media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes/MKM_channel_modal_csd_selected_modes.h5"
      }
    }
  ]
}
```
