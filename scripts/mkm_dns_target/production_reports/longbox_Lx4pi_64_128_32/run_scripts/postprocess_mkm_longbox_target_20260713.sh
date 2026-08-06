#!/usr/bin/env bash
set -euo pipefail

if (( $# != 1 )); then
    echo "usage: $0 T_MIN" >&2
    exit 2
fi

TMIN=$1
TMIN_TAG=${TMIN%.*}
TMAX=200
TAG=t${TMIN_TAG}_t${TMAX}

ENV=/media/jay/data1/conda_envs/shenfun_dns_np126_20260702
REPO=/media/jay/data1/shenfun
OUT=/media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713
PREFIX=MKM_production_Lx4pi_64_128_32
VELOCITY=$OUT/${PREFIX}_U.h5
CONSTRAINT=$OUT/MKM_constraints_Lx4pi_N64_128_32_cheb_quadrature_spectral.h5
TARGET=$OUT/${PREFIX}_target_${TAG}.h5
export TMPDIR=/media/jay/data1/tmp

"$ENV/bin/python" -u "$REPO/scripts/mkm_dns_target/postprocess_mkm_dns_target.py" \
    --velocity-h5 "$VELOCITY" \
    --output "$TARGET" \
    --dt 0.0005 \
    --t-min "$TMIN" \
    --t-max "$TMAX" \
    --constraint-file "$CONSTRAINT" \
    --sampling-stage-label "stationary_${TAG}" \
    --mode-batch 4 \
    --store-modal-coefficients \
    --max-lag 1

"$ENV/bin/python" -u "$REPO/scripts/mkm_dns_target/audit_mkm_target.py" \
    --target-h5 "$TARGET" \
    --velocity-h5 "$VELOCITY" \
    --constraint-file "$CONSTRAINT" \
    --output "$OUT/${PREFIX}_audit_${TAG}.json"

"$ENV/bin/python" -u "$REPO/scripts/mkm_dns_target/project_mkm_dns_covariance.py" \
    --target-h5 "$TARGET" \
    --constraint-file "$CONSTRAINT" \
    --output-h5 "$OUT/${PREFIX}_projected_covariance_${TAG}.h5" \
    --diagnostics-json "$OUT/${PREFIX}_projected_covariance_${TAG}.json" \
    --figure-dir "$OUT/projection_figures_${TAG}" \
    --friction-velocity 1.0 \
    --overwrite
