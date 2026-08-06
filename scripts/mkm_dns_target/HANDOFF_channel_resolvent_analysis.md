% XeLaTeX can use any Mac OS X font. See the setromanfont command below.
% Input to XeLaTeX is full Unicode, so Unicode characters can be typed directly into the source.

% The next lines tell TeXShop to typeset with xelatex, and to open and save the source with Unicode encoding.

%!TEX TS-program = xelatex
%!TEX encoding = UTF-8 Unicode

\documentclass[12pt]{article}
\usepackage{geometry}                % See geometry.pdf to learn the layout options. There are lots.
\geometry{letterpaper}                   % ... or a4paper or a5paper or ... 
%\geometry{landscape}                % Activate for for rotated page geometry
%\usepackage[parfill]{parskip}    % Activate to begin paragraphs with an empty line rather than an indent
\usepackage{graphicx}
\usepackage{amssymb}

% Will Robertson's fontspec.sty can be used to simplify font choices.
% To experiment, open /Applications/Font Book to examine the fonts provided on Mac OS X,
% and change "Hoefler Text" to any of these choices.

\usepackage{fontspec,xltxtra,xunicode}
\defaultfontfeatures{Mapping=tex-text}
\setromanfont[Mapping=tex-text]{Hoefler Text}
\setsansfont[Scale=MatchLowercase,Mapping=tex-text]{Gill Sans}
\setmonofont[Scale=MatchLowercase]{Andale Mono}

\title{Brief Article}
\author{The Author}
%\date{}                                           % Activate to display a given date or no date

\begin{document}
\maketitle

% For many users, the previous commands will be enough.
% If you want to directly input Unicode, add an Input Menu or Keyboard to the menu bar 
% using the International Panel in System Preferences.
% Unicode must be typeset using a font containing the appropriate characters.
% Remove the comment signs below for examples.

% \newfontfamily{\A}{Geeza Pro}
% \newfontfamily{\H}[Scale=0.9]{Lucida Grande}
% \newfontfamily{\J}[Scale=0.85]{Osaka}

% Here are some multilingual Unicode fonts: this is Arabic text: {\A السلام عليكم}, this is Hebrew: {\H שלום}, 
% and here's some Japanese: {\J 今日は}.



\end{document}  # Handoff: selected-mode MKM channel resolvent analysis

This handoff records the selected-mode channel-resolvent analysis implemented
and run for the production MKM channel DNS target. It is intended to let a
future continuation pick up the workflow without rereading the full
conversation history.

## Status

The selected-mode channel-resolvent proof of concept is implemented, locally
smoke-tested, and has been run twice on the Linux server:

1. Sparse target-CSD run, using the accepted target file's stored
   `modal/u_hat` time series.
2. Dense temporal-CSD run, computing selected horizontal Fourier modes on the
   fly from dense raw velocity snapshots.

Both production runs used the selected mode indices

```text
(i,j) = (1,0), (1,1), (2,1)
```

which correspond to physical wavenumbers

```text
(kappa, lambda) = (1,0), (1,2), (2,2)
```

for the present channel box, where `Lx = 2*pi` and `Ly = pi`.

This is a selected-mode proof of concept. It is not a full wavenumber sweep,
not a complete frequency optimization, and not a high-Reynolds-number or
long-box VLSM scaling claim.

## Key Repository Artifacts

Detailed derivation and documentation:

- `docs/mkm_channel_dns_sampling_and_constraints.tex`
  - A new section, `Selected-mode channel resolvent analysis`, was appended.
  - It derives the energy-orthonormal admissible basis, pressure-eliminated
    velocity operator, reduced resolvent, response/forcing SVD convention,
    temporal CSD estimator, Parseval normalization, and DNS CSD projection
    fractions.
  - It also includes HDF5 output schemas and representative production figures.
- `docs/channel_resolvent_implementation_plan.md`
  - Progress/status plan for Steps 1-10 and production execution.
- `production_reports/channel_resolvent_workflow_inventory.md`
  - Inventory of scripts, smoke tests, local reports, server HDF5 outputs, and
    recommended production rerun commands.
- `production_reports/channel_resolvent_selected_modes_comparison.md`
  - Scientific comparison of the sparse target-CSD and dense temporal-CSD
    selected-mode runs.
- `production_reports/channel_resolvent_commit_manifest.md`
  - Explicit commit-candidate staging audit for this workflow.

Local lightweight production artifacts:

- `production_reports/target_csd_selected_modes/`
  - Sparse target-CSD manifest, Markdown report, and PDFs.
- `production_reports/dense_csd_selected_modes/`
  - Dense temporal-CSD manifest, Markdown report, and PDFs.

No production HDF5 files were fetched into the local repository.

## Implemented Workflow Scripts

Core utilities and solver:

- `mkm_channel_resolvent_utils.py`
  - Loads target metadata and constraint operators.
  - Rebuilds `Gtilde` and `Nmat` using the same SVD convention as
    `build_mkm_constraints.py`.
  - Constructs Chebyshev-Gauss physical quadrature weights and level-major
    velocity energy weights.
  - Builds the energy-orthonormal admissible basis `Q`.
  - Builds the raw linearized velocity operator, modal energy diagnostics, and
    critical-layer locations.
- `compute_mkm_channel_resolvent.py`
  - Computes a single-mode velocity-only channel resolvent.
  - Uses `q = Q a`, `Q^* Wq Q = I`, and
    `H(omega)=(-1j*omega*I - A)^(-1)`.
  - Writes singular values, response modes, forcing modes, energy-density
    diagnostics, critical layers, and numerical diagnostics.
- `plot_mkm_channel_resolvent.py`
  - Reads existing single-mode resolvent HDF5 files and writes mode-shape,
    gain, peak/critical-layer, and reconstructed-field PDFs.
- `compute_mkm_modal_csd.py`
  - Computes selected-mode temporal DNS CSD from either target `modal/u_hat`
    or raw velocity snapshots.
- `project_mkm_dns_onto_resolvent.py`
  - Projects DNS modal CSD onto stored response modes and reports leading and
    cumulative captured energy fractions.

Orchestration, production support, and reports:

- `run_mkm_channel_resolvent_selected_modes.py`
  - Composes CSD, single-mode resolvent, projection, plotting, and manifest
    creation.
- `run_mkm_channel_resolvent_production_selected_modes.py`
  - Production wrapper using `/media/jay/data1` defaults.
  - Handles missing local `/media/...` files cleanly and prints exact SSH
    commands.
- `report_mkm_channel_resolvent_workflow.py`
  - Builds Markdown reports from selected-mode workflow manifests.
- `run_channel_resolvent_smoke_suite.py`
  - Runs all synthetic and wrapper smoke tests in one command.

## Mathematical Formulation Implemented

The implemented solver uses a velocity-only admissible-subspace formulation.
For a fixed horizontal mode `(kappa, lambda)`, the full velocity state is
level-major:

```text
[u_x(z0), u_y(z0), u_z(z0), ..., u_x(zN), u_y(zN), u_z(zN)]
```

The discrete constraint matrix `Gtilde(kappa, lambda)` represents
incompressibility plus no-slip boundary constraints. Its null-space matrix
`Nmat` is rebuilt from the saved constraint operators. The energy inner product
uses Fejer first-rule physical Chebyshev-Gauss weights on `[-1,1]`, expanded
to all three velocity components:

```text
<a,b>_Wq = a^* Wq b
```

The admissible basis is built by diagonalizing `Nmat^* Wq Nmat` and forming
`Q` so that

```text
Gtilde Q = 0
Q^* Wq Q = I
q = Q a
```

The turbulent mean is the target streamwise mean profile `U(z)`, with
`Uprime = D_wall @ U`. The raw physical velocity operator is

```text
L_raw q =
  -1j*kappa*U*q
  - u_z*Uprime*e_x
  + (D_wall@D_wall - (kappa^2 + lambda^2) I) q / Re_tau
```

The reduced operator is

```text
A = Q^* Wq L_raw Q
```

with time convention

```text
qhat(z) exp(i*kappa*x + i*lambda*y - i*omega*t)
```

so the reduced resolvent is

```text
H(omega) = (-1j*omega*I - A)^(-1)
```

The SVD is

```text
H = Psi Sigma Phi^*
```

and the stored physical modes are

```text
response_modes = Q @ Psi
forcing_modes  = Q @ Phi
```

These modes are energy normalized under `Wq`.

Critical-layer locations are linearly interpolated roots of

```text
U(z) = omega / kappa
```

with a clean empty-table special case for `kappa = 0`.

## CSD and Projection Conventions

For selected DNS modal time series `q[n]`, the CSD estimator uses the
unnormalized temporal FFT of windowed segments:

```text
Q_k = FFT_t(window * q)_k
Sqq(omega_k) =
  sample_dt / (window_energy * n_segments)
  * sum_segments Q_k Q_k^*
```

The frequency grid is two-sided:

```text
omega = 2*pi*fftfreq(segment_length, sample_dt)
```

stored sorted ascending. With the rectangular full-record case, the
normalization satisfies the expected Parseval relation. With Hann-windowed
overlapping production segments, the reported Parseval diagnostic compares the
window-weighted segment-average modal energy to the integrated spectrum.

Projection uses response modes `Psi` in physical level-major coordinates:

```text
E_total = trace(Wq Sqq)
C       = Psi^* Wq Sqq Wq Psi
F_j     = real(C_jj) / E_total
F_<=r   = real(trace(C[:r,:r])) / E_total
```

The projection script also reports weighted Frobenius reconstruction errors
for rank-r response subspaces.

## Production Inputs

Server:

```text
jay@100.88.70.60
```

Repository:

```text
/media/jay/data1/shenfun
```

Python environment:

```text
/media/jay/data1/conda_envs/shenfun_dns_np126_20260702/bin/python
```

Production target:

```text
/media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/MKM_production_64_64_32_target_t60_t180.h5
```

Constraint file:

```text
/media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/MKM_constraints_N64_64_32_cheb_quadrature_spectral.h5
```

Dense temporal velocity file:

```text
/media/jay/data1/shenfun_dns_runs/dense_temporal_mkm_64_64_32_t180_t300_20260703/MKM_dense_temporal_64_64_32_t180_t300_U.h5
```

Temporary directory used for production workflows:

```text
TMPDIR=/media/jay/data1/tmp
```

Important path note: the live server root is `/media/jay/data1`, not
`/media/jay/data`.

## Sparse Target-CSD Production Run

Source:

```text
target modal/u_hat
```

Server output directory:

```text
/media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes
```

Local lightweight artifacts:

```text
scripts/mkm_dns_target/production_reports/target_csd_selected_modes/
```

Settings:

```text
csd-source       target
mode-index-list  1 0 1 1 2 1
omega-count      4
segment-length   512
window           hann
demean-temporal  true
n-singular       6
make-figures     true
no-tex           true
```

Frequency bins:

```text
0.12271846303085827
0.24543692606171655
0.3681553890925748
0.4908738521234331
```

Results:

| mode | `(kappa, lambda)` | leading singular values | leading DNS fractions | rank-6 cumulative fractions |
| --- | --- | --- | --- | --- |
| `(1,0)` | `(1,0)` | `0.145890, 0.147973, 0.150108, 0.152295` | `0.108022, 0.037702, 0.123227, 0.056511` | `0.353601, 0.241945, 0.407893, 0.406697` |
| `(1,1)` | `(1,2)` | `0.183654, 0.186719, 0.189871, 0.193115` | `0.158274, 0.161356, 0.114346, 0.034472` | `0.387042, 0.472809, 0.490194, 0.317179` |
| `(2,1)` | `(2,2)` | `0.092078, 0.092894, 0.093722, 0.094563` | `0.027805, 0.059074, 0.057288, 0.053907` | `0.260677, 0.215853, 0.265905, 0.233041` |

Diagnostics:

```text
max CSD Parseval relative error     2.932579e-15
max response constraint residual    4.889762e-15
max forcing constraint residual     4.712708e-15
max response energy norm error      2.220446e-15
max forcing energy norm error       3.108624e-15
max projection frequency mismatch   0
```

Server HDF5 products left in place:

```text
MKM_channel_modal_csd_selected_modes.h5              906,118,744 bytes
MKM_channel_resolvent_i1_j0.h5                           223,000 bytes
MKM_channel_resolvent_i1_j1.h5                           223,000 bytes
MKM_channel_resolvent_i2_j1.h5                           223,000 bytes
MKM_channel_resolvent_projection_i1_j0.h5                 21,904 bytes
MKM_channel_resolvent_projection_i1_j1.h5                 21,904 bytes
MKM_channel_resolvent_projection_i2_j1.h5                 21,904 bytes
```

## Dense Temporal-CSD Production Run

Source:

```text
raw dense temporal velocity snapshots, selected FFT modes computed on the fly
```

Server output directory:

```text
/media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes_dense_csd
```

Local lightweight artifacts:

```text
scripts/mkm_dns_target/production_reports/dense_csd_selected_modes/
```

Settings:

```text
csd-source       dense
mode-index-list  1 0 1 1 2 1
omega-count      6
segment-length   2048
overlap          0.5
window           hann
demean-temporal  true
dt               0.0005
t-min            180
t-max            300
n-singular       6
make-figures     true
no-tex           true
```

The dense CSD report records:

```text
n_times         12000
sample_dt       0.01
segment_length  2048
n_segments      10
window          hann
```

Frequency bins:

```text
0.30679615757740725
0.6135923151548145
0.9203884727322218
1.227184630309629
1.5339807878870364
1.8407769454644436
```

Results:

| mode | `(kappa, lambda)` | leading singular values | leading DNS fractions | rank-6 cumulative fractions |
| --- | --- | --- | --- | --- |
| `(1,0)` | `(1,0)` | `0.149034, 0.154537, 0.160392, 0.166628, 0.173277, 0.180371` | `0.072008, 0.115051, 0.088259, 0.048182, 0.075430, 0.075190` | `0.293472, 0.335164, 0.324492, 0.277046, 0.293775, 0.258281` |
| `(1,1)` | `(1,2)` | `0.188284, 0.196453, 0.205236, 0.214696, 0.224903, 0.235934` | `0.219378, 0.147938, 0.080198, 0.081589, 0.092424, 0.107746` | `0.422372, 0.372225, 0.375353, 0.389396, 0.367008, 0.362858` |
| `(2,1)` | `(2,2)` | `0.093306, 0.095417, 0.097610, 0.099892, 0.102266, 0.104738` | `0.059642, 0.082318, 0.039605, 0.026305, 0.042329, 0.039128` | `0.272863, 0.356971, 0.318046, 0.258397, 0.284472, 0.310064` |

Diagnostics:

```text
max CSD Parseval relative error     6.166581e-15
max response constraint residual    4.908845e-15
max forcing constraint residual     4.793922e-15
max response energy norm error      3.774758e-15
max forcing energy norm error       2.886580e-15
max projection frequency mismatch   0
```

Server HDF5 products left in place:

```text
MKM_channel_modal_csd_selected_modes.h5            3,624,745,664 bytes
MKM_channel_resolvent_i1_j0.h5                           321,864 bytes
MKM_channel_resolvent_i1_j1.h5                           321,864 bytes
MKM_channel_resolvent_i2_j1.h5                           321,864 bytes
MKM_channel_resolvent_projection_i1_j0.h5                 25,208 bytes
MKM_channel_resolvent_projection_i1_j1.h5                 25,208 bytes
MKM_channel_resolvent_projection_i2_j1.h5                 25,208 bytes
```

## Scientific Interpretation

The strongest leading-response alignment observed in these production runs is
mode `(1,1)` in the dense temporal-CSD run:

```text
mode          (1,1)
(kappa,lambda) (1,2)
omega         0.30679615757740725
rank-1 fraction 0.219378
rank-6 fraction 0.422372
```

The strongest rank-6 cumulative fraction is also mode `(1,1)`, but in the
sparse target-CSD run:

```text
omega           0.3681553890925748
rank-6 fraction 0.490194
```

Across these selected modes, rank 6 captures substantially more DNS CSD energy
than the first response mode alone. This means the leading response mode is
informative but not exhaustive for the sampled DNS CSD. Low rank-1 projection
fractions should not be read as a failure of the resolvent model: the DNS CSD
also reflects nonlinear forcing statistics, finite rank, finite sample/window
effects, short-box effects, and the choice of frequency bins.

The sparse and dense frequency grids are different. The sparse target run uses
lower positive frequency bins because `sample_dt = 0.1` with
`segment_length = 512`. The dense run has finer temporal sampling, but with
`segment_length = 2048` its first positive bin is
`Delta omega = 0.30679615757740725`. Compare trends and mode alignment rather
than one-to-one frequency values.

## Figures

Each production mode directory contains:

```text
mkm_resolvent_mode_shapes.pdf
mkm_resolvent_gain_bode.pdf
mkm_resolvent_peak_location_gain.pdf
mkm_resolvent_reconstructed_fields.pdf
```

Local sparse target-CSD figure directories:

```text
scripts/mkm_dns_target/production_reports/target_csd_selected_modes/figures_i1_j0/
scripts/mkm_dns_target/production_reports/target_csd_selected_modes/figures_i1_j1/
scripts/mkm_dns_target/production_reports/target_csd_selected_modes/figures_i2_j1/
```

Local dense temporal-CSD figure directories:

```text
scripts/mkm_dns_target/production_reports/dense_csd_selected_modes/figures_i1_j0/
scripts/mkm_dns_target/production_reports/dense_csd_selected_modes/figures_i1_j1/
scripts/mkm_dns_target/production_reports/dense_csd_selected_modes/figures_i2_j1/
```

The LaTeX note includes representative `(1,1)` figures from both CSD sources.

## Validation State

The final local smoke suite passed:

```text
/opt/anaconda3/bin/python scripts/mkm_dns_target/run_channel_resolvent_smoke_suite.py --json-summary /private/tmp/mkm_channel_resolvent_smoke_suite_commit_manifest.json

smoke_suite: ok passed=8 failed=0
```

The augmented LaTeX note was compiled into a temporary output directory:

```text
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=/private/tmp/mkm_channel_tex_check mkm_channel_dns_sampling_and_constraints.tex
```

The compile succeeded and produced:

```text
/private/tmp/mkm_channel_tex_check/mkm_channel_dns_sampling_and_constraints.pdf
```

No generated LaTeX auxiliary files from that check were written back into the
repository.

## Rerun Commands

Sparse target-CSD selected-mode workflow:

```bash
ssh jay@100.88.70.60 'cd /media/jay/data1/shenfun && TMPDIR=/media/jay/data1/tmp /media/jay/data1/conda_envs/shenfun_dns_np126_20260702/bin/python scripts/mkm_dns_target/run_mkm_channel_resolvent_production_selected_modes.py --target-h5 /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/MKM_production_64_64_32_target_t60_t180.h5 --constraint-file /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/MKM_constraints_N64_64_32_cheb_quadrature_spectral.h5 --dense-velocity-h5 /media/jay/data1/shenfun_dns_runs/dense_temporal_mkm_64_64_32_t180_t300_20260703/MKM_dense_temporal_64_64_32_t180_t300_U.h5 --output-dir /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes --csd-source target --mode-index-list 1 0 1 1 2 1 --omega-count 4 --segment-length 512 --window hann --demean-temporal --n-singular 6 --make-figures --no-tex --overwrite'
```

Dense temporal-CSD selected-mode workflow:

```bash
ssh jay@100.88.70.60 'cd /media/jay/data1/shenfun && TMPDIR=/media/jay/data1/tmp /media/jay/data1/conda_envs/shenfun_dns_np126_20260702/bin/python scripts/mkm_dns_target/run_mkm_channel_resolvent_production_selected_modes.py --target-h5 /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/MKM_production_64_64_32_target_t60_t180.h5 --constraint-file /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/MKM_constraints_N64_64_32_cheb_quadrature_spectral.h5 --dense-velocity-h5 /media/jay/data1/shenfun_dns_runs/dense_temporal_mkm_64_64_32_t180_t300_20260703/MKM_dense_temporal_64_64_32_t180_t300_U.h5 --output-dir /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes_dense_csd --csd-source dense --mode-index-list 1 0 1 1 2 1 --omega-count 6 --segment-length 2048 --overlap 0.5 --window hann --demean-temporal --dt 0.0005 --t-min 180 --t-max 300 --n-singular 6 --make-figures --no-tex --overwrite'
```

Report regeneration:

```bash
ssh jay@100.88.70.60 'cd /media/jay/data1/shenfun && /media/jay/data1/conda_envs/shenfun_dns_np126_20260702/bin/python scripts/mkm_dns_target/report_mkm_channel_resolvent_workflow.py --manifest /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes/MKM_channel_resolvent_selected_modes_manifest.json'

ssh jay@100.88.70.60 'cd /media/jay/data1/shenfun && /media/jay/data1/conda_envs/shenfun_dns_np126_20260702/bin/python scripts/mkm_dns_target/report_mkm_channel_resolvent_workflow.py --manifest /media/jay/data1/shenfun_dns_runs/production_mkm_64_64_32_20260702/channel_resolvent_selected_modes_dense_csd/MKM_channel_resolvent_selected_modes_manifest.json'
```

## Caveats

- This workflow currently covers selected modes only.
- Frequency selection used the first positive CSD bins, not a search around
  energetic DNS CSD peaks or gain peaks.
- The velocity-only admissible-subspace resolvent has not yet been cross-checked
  against an Orr-Sommerfeld/Squire implementation.
- The current DNS is `Re_tau = 180` in a short streamwise box. It is enough to
  validate workflow mechanics but not enough for broad VLSM scaling claims.
- Dense CSD runs are much more expensive because selected modes are computed
  from the raw velocity snapshot file.

## Recommended Next Work

1. Run a wider selected-mode/wavenumber sweep.
2. Choose frequency bands around energetic CSD peaks instead of only the first
   positive bins.
3. Compare wall-normal response-energy peaks with critical-layer locations
   across a wider mode/frequency set.
4. Inspect component energy distributions and reconstructed fields for modes
   with high projection fractions.
5. Add an optional Orr-Sommerfeld/Squire cross-check.
6. Plan longer-box and/or higher-Reynolds-number DNS before making VLSM-scale
   claims.

