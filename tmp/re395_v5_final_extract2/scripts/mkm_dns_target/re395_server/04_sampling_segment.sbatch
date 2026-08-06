#!/bin/bash
#SBATCH --job-name=mkm395_sample
#SBATCH --partition=cpu02
#SBATCH --nodes=1
#SBATCH --ntasks=128
#SBATCH --cpus-per-task=1
#SBATCH --time=24:00:00
#SBATCH --output=/share/home/dkyzdsys_wanjiawei/shenfun_runs/logs/%x_%j.out
#SBATCH --error=/share/home/dkyzdsys_wanjiawei/shenfun_runs/logs/%x_%j.err

set -eo pipefail

: "${END_TIME:?Submit with --export=ALL,END_TIME=<absolute_outer_time>}"
STATE_COMPRESSION=${STATE_COMPRESSION:-none}
if [[ "$STATE_COMPRESSION" != none && "$STATE_COMPRESSION" != gzip ]]; then
    echo "STATE_COMPRESSION must be none or gzip" >&2
    exit 2
fi

source /share/home/dkyzdsys_wanjiawei/shenfun-master/scripts/mkm_dns_target/re395_server/re395_common.sh

RUN_DIR="$RUN_ROOT/production_mkm_Re395_N192_256_192_dt5em5_sampling"
PREFIX=MKM_Re395_N192_256_192_dt5em5_sampling
STATE_PREFIX="${PREFIX}_state"
CHECKPOINT_H5="$RUN_DIR/${PREFIX}.chk.h5"
AUDIT_H5="$RUN_DIR/${PREFIX}_U.h5"
test -s "$CHECKPOINT_H5"

activate_re395_runtime "$RUN_DIR"
verify_re395_inputs
print_re395_provenance "$RUN_DIR"

CURRENT_TIME=$(
    "$ENV/bin/python" - "$CHECKPOINT_H5" <<'PY'
import h5py
import sys
with h5py.File(sys.argv[1], "r") as f:
    print(f"{float(f.attrs['t']):.12g}")
PY
)

PARTIAL_STATE=$(find "$RUN_DIR" -maxdepth 1 -name "${STATE_PREFIX}_*.partial.h5" -print -quit)
if [[ -n "$PARTIAL_STATE" ]]; then
    echo "Refusing to continue while a partial state shard exists: $PARTIAL_STATE" >&2
    exit 1
fi

shopt -s nullglob
EXISTING_STATE_SHARDS=("$RUN_DIR"/"${STATE_PREFIX}"_tstep*.h5)
if (( ${#EXISTING_STATE_SHARDS[@]} == 0 )); then
    "$ENV/bin/python" - "$CURRENT_TIME" "$SAMPLING_START_TIME" <<'PY'
import math
import sys

actual, expected = map(float, sys.argv[1:])
if not math.isclose(actual, expected, rel_tol=0.0, abs_tol=1e-8):
    raise SystemExit(
        f"the first sampling segment must start at t={expected:.12g}; "
        f"checkpoint is at t={actual:.12g}"
    )
print(f"first_sampling_segment_start={actual:.12g}")
PY
else
    PREFLIGHT_MANIFEST="$RUN_DIR/${PREFIX}_state_manifest_preflight_job${SLURM_JOB_ID}.json"
    "$ENV/bin/python" -u "$STATE_AUDITOR" \
        --shards "${EXISTING_STATE_SHARDS[@]}" \
        --output-json "$PREFLIGHT_MANIFEST"
    "$ENV/bin/python" -u "$SCHEDULE_VALIDATOR" manifest \
        --manifest "$PREFLIGHT_MANIFEST" \
        --segment-end "$CURRENT_TIME" \
        --window-start "$SAMPLING_START_TIME" \
        --window-end "$SAMPLING_FINAL_TIME" \
        --sample-dt "$SAMPLING_DT"
fi

"$ENV/bin/python" -u "$SCHEDULE_VALIDATOR" segment \
    --start "$CURRENT_TIME" \
    --end "$END_TIME" \
    --window-start "$SAMPLING_START_TIME" \
    --window-end "$SAMPLING_FINAL_TIME" \
    --sample-dt "$SAMPLING_DT" \
    --shard-samples "$STATE_SHARD_SAMPLES"

if [[ -e "$AUDIT_H5" ]]; then
    VELOCITY_MODE=a
else
    VELOCITY_MODE=w
fi

cd "$RUN_DIR"
run_re395_mpi "$ENV/bin/python" -u "$RUNNER" \
    --output-dir "$RUN_DIR" \
    --filename "$PREFIX" \
    --run-tag "job${SLURM_JOB_ID}" \
    --n 192 256 192 \
    --domain -1 1 0 6.283185307179586 0 3.141592653589793 \
    --re "$RE_TAU" \
    --bulk-velocity "$BULK_VELOCITY" \
    --initial-mean-profile "$PROFILE" \
    --dt "$DNS_DT" \
    --padding-factor "$PADDING_WALL" "$PADDING_STREAM" "$PADDING_SPAN" \
    --end-time "$END_TIME" \
    --modsave "$AUDIT_EVERY_STEPS" \
    --checkpoint "$CHECKPOINT_EVERY_STEPS" \
    --moderror "$DIAGNOSTIC_EVERY_STEPS" \
    --modplot -1 \
    --save-mesh quadrature \
    --velocity-file-mode "$VELOCITY_MODE" \
    --stage-label sampling \
    --from-checkpoint \
    --state-every "$STATE_EVERY_STEPS" \
    --state-shard-samples "$STATE_SHARD_SAMPLES" \
    --state-prefix "$STATE_PREFIX" \
    --state-compression "$STATE_COMPRESSION" \
    --state-gzip-level 4 \
    --force-final-checkpoint \
    --skip-xdmf

test -s "$CHECKPOINT_H5"
PARTIAL_STATE=$(find "$RUN_DIR" -maxdepth 1 -name "${STATE_PREFIX}_*.partial.h5" -print -quit)
if [[ -n "$PARTIAL_STATE" ]]; then
    echo "A partial state shard remains after a nominally completed job: $PARTIAL_STATE" >&2
    exit 1
fi
"$ENV/bin/python" - "$CHECKPOINT_H5" "$END_TIME" <<'PY'
import h5py
import sys

path, expected = sys.argv[1], float(sys.argv[2])
with h5py.File(path, "r") as f:
    actual = float(f.attrs["t"])
    tstep = int(f.attrs["tstep"])
if abs(actual-expected) > 1e-8:
    raise SystemExit(f"checkpoint time mismatch: {actual} != {expected}")
print(f"SAMPLING_SEGMENT_COMPLETE time={actual:.12g} tstep={tstep}")
PY

MANIFEST_JSON="$RUN_DIR/${PREFIX}_state_manifest_job${SLURM_JOB_ID}.json"
"$ENV/bin/python" -u "$STATE_AUDITOR" \
    --shards "$RUN_DIR"/"${STATE_PREFIX}"_tstep*.h5 \
    --output-json "$MANIFEST_JSON"

"$ENV/bin/python" -u "$SCHEDULE_VALIDATOR" manifest \
    --manifest "$MANIFEST_JSON" \
    --segment-end "$END_TIME" \
    --window-start "$SAMPLING_START_TIME" \
    --window-end "$SAMPLING_FINAL_TIME" \
    --sample-dt "$SAMPLING_DT"
