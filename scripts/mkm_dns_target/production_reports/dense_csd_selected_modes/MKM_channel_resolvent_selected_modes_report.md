# MKM Channel Resolvent Selected-Mode Report

## Summary
| Item | Value |
| --- | --- |
| Manifest | /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes_dense_csd/MKM_channel_resolvent_selected_modes_manifest.json |
| Output directory | /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes_dense_csd |
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
| Shared CSD HDF5 | /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes_dense_csd/MKM_channel_modal_csd_selected_modes.h5 |

## Shared CSD
| Field | Value |
| --- | --- |
| Path | /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes_dense_csd/MKM_channel_modal_csd_selected_modes.h5 |
| Size | 3.38 GiB |
| Source | raw_velocity_fft2_selected_modes |
| Mode count | 3 |
| n_omega | 2048 |
| sample_dt | 0.01 |
| segment_length | 2048 |
| n_segments | 10 |
| window | hann |
| max Parseval relative error | 6.166581e-15 |
| Parseval relative errors | 6.093512e-15, 5.412855e-15, 6.166581e-15 |

## Mode Results
### Mode (1, 0)
| Field | Value |
| --- | --- |
| kappa | 1 |
| lambda | 0 |
| Resolvent HDF5 | /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes_dense_csd/MKM_channel_resolvent_i1_j0.h5 |
| Resolvent size | 314.32 KiB |
| Projection HDF5 | /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes_dense_csd/MKM_channel_resolvent_projection_i1_j0.h5 |
| Projection size | 24.62 KiB |
| Omega selection | positive_low_frequency_csd_bins |

| idx | omega | sigma1 | sigma2 | critical roots | lead fraction | cum fraction | rank1 Fro err |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0.306796 | 0.149034 | 0.135353 | 2 | 0.0720082 | 0.293472 | 0.987639 |
| 1 | 0.613592 | 0.154537 | 0.139964 | 2 | 0.115051 | 0.335164 | 0.961394 |
| 2 | 0.920388 | 0.160392 | 0.144852 | 2 | 0.0882589 | 0.324492 | 0.978827 |
| 3 | 1.22718 | 0.166628 | 0.150039 | 2 | 0.0481823 | 0.277046 | 0.995351 |
| 4 | 1.53398 | 0.173277 | 0.155547 | 2 | 0.0754299 | 0.293775 | 0.985115 |
| 5 | 1.84078 | 0.180371 | 0.161403 | 2 | 0.0751901 | 0.258281 | 0.987206 |

| Diagnostic | Value | Status |
| --- | --- | --- |
| max response constraint residual | 4.355236e-15 | PASS |
| max forcing constraint residual | 4.324861e-15 | PASS |
| max response energy norm error | 2.220446e-15 | PASS |
| max forcing energy norm error | 2.220446e-15 | PASS |
| max projection frequency match error | 0.000000e+00 | PASS |

### Mode (1, 1)
| Field | Value |
| --- | --- |
| kappa | 1 |
| lambda | 2 |
| Resolvent HDF5 | /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes_dense_csd/MKM_channel_resolvent_i1_j1.h5 |
| Resolvent size | 314.32 KiB |
| Projection HDF5 | /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes_dense_csd/MKM_channel_resolvent_projection_i1_j1.h5 |
| Projection size | 24.62 KiB |
| Omega selection | positive_low_frequency_csd_bins |

| idx | omega | sigma1 | sigma2 | critical roots | lead fraction | cum fraction | rank1 Fro err |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0.306796 | 0.188284 | 0.186067 | 2 | 0.219378 | 0.422372 | 0.886963 |
| 1 | 0.613592 | 0.196453 | 0.194073 | 2 | 0.147938 | 0.372225 | 0.943013 |
| 2 | 0.920388 | 0.205236 | 0.202678 | 2 | 0.0801978 | 0.375353 | 0.984398 |
| 3 | 1.22718 | 0.214696 | 0.211941 | 2 | 0.0815895 | 0.389396 | 0.984428 |
| 4 | 1.53398 | 0.224903 | 0.221931 | 2 | 0.0924244 | 0.367008 | 0.978773 |
| 5 | 1.84078 | 0.235934 | 0.232722 | 2 | 0.107746 | 0.362858 | 0.972163 |

| Diagnostic | Value | Status |
| --- | --- | --- |
| max response constraint residual | 2.813108e-15 | PASS |
| max forcing constraint residual | 3.080670e-15 | PASS |
| max response energy norm error | 3.774758e-15 | PASS |
| max forcing energy norm error | 1.887379e-15 | PASS |
| max projection frequency match error | 0.000000e+00 | PASS |

### Mode (2, 1)
| Field | Value |
| --- | --- |
| kappa | 2 |
| lambda | 2 |
| Resolvent HDF5 | /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes_dense_csd/MKM_channel_resolvent_i2_j1.h5 |
| Resolvent size | 314.32 KiB |
| Projection HDF5 | /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes_dense_csd/MKM_channel_resolvent_projection_i2_j1.h5 |
| Projection size | 24.62 KiB |
| Omega selection | positive_low_frequency_csd_bins |

| idx | omega | sigma1 | sigma2 | critical roots | lead fraction | cum fraction | rank1 Fro err |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0.306796 | 0.0933061 | 0.0929145 | 2 | 0.0596418 | 0.272863 | 0.99076 |
| 1 | 0.613592 | 0.0954165 | 0.0950095 | 2 | 0.0823179 | 0.356971 | 0.980991 |
| 2 | 0.920388 | 0.0976103 | 0.0971871 | 2 | 0.0396046 | 0.318046 | 0.995238 |
| 3 | 1.22718 | 0.099892 | 0.0994515 | 2 | 0.0263053 | 0.258397 | 0.998247 |
| 4 | 1.53398 | 0.102266 | 0.101808 | 2 | 0.0423288 | 0.284472 | 0.9954 |
| 5 | 1.84078 | 0.104738 | 0.10426 | 2 | 0.0391278 | 0.310064 | 0.995716 |

| Diagnostic | Value | Status |
| --- | --- | --- |
| max response constraint residual | 4.908845e-15 | PASS |
| max forcing constraint residual | 4.793922e-15 | PASS |
| max response energy norm error | 2.886580e-15 | PASS |
| max forcing energy norm error | 2.886580e-15 | PASS |
| max projection frequency match error | 0.000000e+00 | PASS |

## Figures
| Mode | Figure | Size | Exists |
| --- | --- | --- | --- |
| (1, 0) | /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes_dense_csd/figures_i1_j0/mkm_resolvent_mode_shapes.pdf | 25.15 KiB | yes |
| (1, 0) | /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes_dense_csd/figures_i1_j0/mkm_resolvent_gain_bode.pdf | 15.82 KiB | yes |
| (1, 0) | /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes_dense_csd/figures_i1_j0/mkm_resolvent_peak_location_gain.pdf | 16.58 KiB | yes |
| (1, 0) | /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes_dense_csd/figures_i1_j0/mkm_resolvent_reconstructed_fields.pdf | 45.33 KiB | yes |
| (1, 1) | /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes_dense_csd/figures_i1_j1/mkm_resolvent_mode_shapes.pdf | 27.76 KiB | yes |
| (1, 1) | /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes_dense_csd/figures_i1_j1/mkm_resolvent_gain_bode.pdf | 16.09 KiB | yes |
| (1, 1) | /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes_dense_csd/figures_i1_j1/mkm_resolvent_peak_location_gain.pdf | 16.46 KiB | yes |
| (1, 1) | /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes_dense_csd/figures_i1_j1/mkm_resolvent_reconstructed_fields.pdf | 74.25 KiB | yes |
| (2, 1) | /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes_dense_csd/figures_i2_j1/mkm_resolvent_mode_shapes.pdf | 27.53 KiB | yes |
| (2, 1) | /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes_dense_csd/figures_i2_j1/mkm_resolvent_gain_bode.pdf | 16.17 KiB | yes |
| (2, 1) | /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes_dense_csd/figures_i2_j1/mkm_resolvent_peak_location_gain.pdf | 17.01 KiB | yes |
| (2, 1) | /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes_dense_csd/figures_i2_j1/mkm_resolvent_reconstructed_fields.pdf | 72.89 KiB | yes |

## Diagnostics and Thresholds
| Check | Value | Status | Threshold |
| --- | --- | --- | --- |
| mode (1, 0): response constraint residual | 4.355236e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (1, 0): forcing constraint residual | 4.324861e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (1, 0): response energy norm error | 2.220446e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (1, 0): forcing energy norm error | 2.220446e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (1, 0): projection frequency match error | 0.000000e+00 | PASS | warn>1e-10 |
| mode (1, 1): response constraint residual | 2.813108e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (1, 1): forcing constraint residual | 3.080670e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (1, 1): response energy norm error | 3.774758e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (1, 1): forcing energy norm error | 1.887379e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (1, 1): projection frequency match error | 0.000000e+00 | PASS | warn>1e-10 |
| mode (2, 1): response constraint residual | 4.908845e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (2, 1): forcing constraint residual | 4.793922e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (2, 1): response energy norm error | 2.886580e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (2, 1): forcing energy norm error | 2.886580e-15 | PASS | warn>1e-08, fail>1e-06 |
| mode (2, 1): projection frequency match error | 0.000000e+00 | PASS | warn>1e-10 |
| shared CSD: Parseval relative error | 6.166581e-15 | INFO | diagnostic only for window=hann |

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
  "output_dir": "/media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes_dense_csd",
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
    "path": "/media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes_dense_csd/MKM_channel_modal_csd_selected_modes.h5",
    "summary": {
      "output": "/media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes_dense_csd/MKM_channel_modal_csd_selected_modes.h5",
      "source": "raw_velocity_fft2_selected_modes",
      "n_modes": 3,
      "n_times": 12000,
      "modal_dim": 192,
      "n_omega": 2048,
      "sample_dt": 0.009999999999990905,
      "segment_length": 2048,
      "n_segments": 10,
      "window": "hann",
      "max_parseval_relative_error": 6.166581320930615e-15
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
        "source_csd": "/media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes_dense_csd/MKM_channel_modal_csd_selected_modes.h5"
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
        "source_csd": "/media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes_dense_csd/MKM_channel_modal_csd_selected_modes.h5"
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
        "source_csd": "/media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes_dense_csd/MKM_channel_modal_csd_selected_modes.h5"
      }
    }
  ]
}
```
