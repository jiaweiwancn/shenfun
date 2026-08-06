#!/usr/bin/env bash
set -euo pipefail

ENV=/media/jay/data1/conda_envs/shenfun_dns_np126_20260702
REPO=/media/jay/data1/shenfun
OUT=/media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713
PREFIX=MKM_production_Lx4pi_64_128_32
VELOCITY=$OUT/${PREFIX}_U.h5
export TMPDIR=/media/jay/data1/tmp

"$ENV/bin/python" "$REPO/scripts/mkm_dns_target/parse_mkm_diagnostics.py" \
    --logs \
    "$OUT/${PREFIX}_sampling_t40_t80_n32.log" \
    "$OUT/${PREFIX}_sampling_t80_t120_n32.log" \
    "$OUT/${PREFIX}_sampling_t120_t160_n32.log" \
    "$OUT/${PREFIX}_sampling_t160_t200_n32.log" \
    --output "$OUT/${PREFIX}_sampling_t40_t200_diagnostics.json" \
    --n-blocks 12 \
    --tolerance 0.05 \
    --divergence-threshold 1e-10 \
    --store-series

"$ENV/bin/python" "$REPO/scripts/mkm_dns_target/check_mkm_sampling_convergence.py" \
    --velocity-h5 "$VELOCITY" \
    --output "$OUT/${PREFIX}_sampling_field_convergence_t40_t200.json" \
    --dt 0.0005 \
    --n-blocks 12 \
    --tolerance 0.05

"$ENV/bin/python" "$REPO/scripts/mkm_dns_target/check_mkm_sampling_convergence.py" \
    --velocity-h5 "$VELOCITY" \
    --output "$OUT/${PREFIX}_sampling_field_convergence_t60_t200.json" \
    --dt 0.0005 \
    --t-min 60 \
    --n-blocks 12 \
    --tolerance 0.05

"$ENV/bin/python" "$REPO/scripts/mkm_dns_target/check_mkm_sampling_convergence.py" \
    --velocity-h5 "$VELOCITY" \
    --output "$OUT/${PREFIX}_sampling_field_convergence_t80_t200.json" \
    --dt 0.0005 \
    --t-min 80 \
    --n-blocks 12 \
    --tolerance 0.05
