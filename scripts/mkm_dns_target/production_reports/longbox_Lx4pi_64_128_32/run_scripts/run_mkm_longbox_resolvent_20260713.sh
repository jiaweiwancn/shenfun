#!/usr/bin/env bash
set -euo pipefail

if (( $# != 2 )); then
    echo "usage: $0 T_MIN target|dense" >&2
    exit 2
fi

TMIN=${1%.*}
SOURCE=$2
TAG=t${TMIN}_t200

ENV=/media/jay/data1/conda_envs/shenfun_dns_np126_20260702
REPO=/media/jay/data1/shenfun
OUT=/media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713
PREFIX=MKM_production_Lx4pi_64_128_32
TARGET=$OUT/${PREFIX}_target_${TAG}.h5
CONSTRAINT=$OUT/MKM_constraints_Lx4pi_N64_128_32_cheb_quadrature_spectral.h5
DENSE_OUT=/media/jay/data1/shenfun_dns_runs/dense_temporal_mkm_Lx4pi_64_128_32_t200_t320_20260713
DENSE_PREFIX=MKM_dense_temporal_Lx4pi_64_128_32_t200_t320
DENSE_VELOCITY=$DENSE_OUT/${DENSE_PREFIX}_U.h5
MODES=(1 0 1 1 2 0 2 1 4 1)
export TMPDIR=/media/jay/data1/tmp

case "$SOURCE" in
    target)
        RESULT_DIR=$OUT/channel_resolvent_selected_modes_target_${TAG}
        OMEGA_COUNT=4
        SEGMENT_LENGTH=512
        ;;
    dense)
        RESULT_DIR=$OUT/channel_resolvent_selected_modes_dense_${TAG}
        OMEGA_COUNT=6
        SEGMENT_LENGTH=2048
        test -f "$DENSE_VELOCITY"
        ;;
    *)
        echo "source must be target or dense" >&2
        exit 2
        ;;
esac

COMMAND=(
    "$ENV/bin/python" -u
    "$REPO/scripts/mkm_dns_target/run_mkm_channel_resolvent_production_selected_modes.py"
    --target-h5 "$TARGET"
    --constraint-file "$CONSTRAINT"
    --dense-velocity-h5 "$DENSE_VELOCITY"
    --output-dir "$RESULT_DIR"
    --csd-source "$SOURCE"
    --mode-index-list "${MODES[@]}"
    --omega-count "$OMEGA_COUNT"
    --segment-length "$SEGMENT_LENGTH"
    --overlap 0.5
    --window hann
    --demean-temporal
    --n-singular 6
    --make-figures
    --no-tex
    --overwrite
)

if [[ "$SOURCE" == dense ]]; then
    COMMAND+=(--dt 0.0005 --t-min 200 --t-max 320)
fi

"${COMMAND[@]}"

"$ENV/bin/python" \
    "$REPO/scripts/mkm_dns_target/report_mkm_channel_resolvent_workflow.py" \
    --manifest "$RESULT_DIR/MKM_channel_resolvent_selected_modes_manifest.json" \
    --include-hdf5-schema
