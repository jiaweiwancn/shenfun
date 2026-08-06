#!/bin/bash
#SBATCH --job-name=mkm395_spinup
#SBATCH --partition=cpu02
#SBATCH --nodes=1
#SBATCH --ntasks=128
#SBATCH --cpus-per-task=1
#SBATCH --time=24:00:00
#SBATCH --output=/share/home/dkyzdsys_wanjiawei/shenfun_runs/logs/%x_%j.out
#SBATCH --error=/share/home/dkyzdsys_wanjiawei/shenfun_runs/logs/%x_%j.err

set -eo pipefail

: "${END_TIME:?Submit with --export=ALL,END_TIME=<absolute_outer_time>,FROM_CHECKPOINT=0_or_1}"
FROM_CHECKPOINT=${FROM_CHECKPOINT:-0}
if [[ "$FROM_CHECKPOINT" != 0 && "$FROM_CHECKPOINT" != 1 ]]; then
    echo "FROM_CHECKPOINT must be 0 or 1" >&2
    exit 2
fi

source /share/home/dkyzdsys_wanjiawei/shenfun-master/scripts/mkm_dns_target/re395_server/re395_common.sh

RUN_DIR="$RUN_ROOT/production_mkm_Re395_N192_256_192_spinup"
PREFIX=MKM_Re395_N192_256_192_spinup
CHECKPOINT_H5="$RUN_DIR/${PREFIX}.chk.h5"
mkdir -p "$RUN_DIR"
activate_re395_runtime "$RUN_DIR"
verify_re395_inputs
print_re395_provenance "$RUN_DIR"
"$ENV/bin/python" -u "$SCHEDULE_VALIDATOR" spinup \
    --end "$END_TIME" \
    --target "$SPINUP_FINAL_TIME" \
    --dns-dt "$DNS_DT"

if [[ "$FROM_CHECKPOINT" == 1 ]]; then
    test -s "$CHECKPOINT_H5"
else
    if [[ -e "$CHECKPOINT_H5" ]]; then
        echo "Refusing to overwrite existing spin-up checkpoint: $CHECKPOINT_H5" >&2
        exit 2
    fi
fi

RUN_ARGS=(
    --output-dir "$RUN_DIR"
    --filename "$PREFIX"
    --run-tag "job${SLURM_JOB_ID}"
    --n 192 256 192
    --domain -1 1 0 6.283185307179586 0 3.141592653589793
    --re "$RE_TAU"
    --bulk-velocity "$BULK_VELOCITY"
    --initial-mean-profile "$PROFILE"
    --dt "$DNS_DT"
    --padding-factor "$PADDING_WALL" "$PADDING_STREAM" "$PADDING_SPAN"
    --end-time "$END_TIME"
    --modsave 100000000
    --checkpoint "$CHECKPOINT_EVERY_STEPS"
    --moderror "$DIAGNOSTIC_EVERY_STEPS"
    --modplot -1
    --stage-label spinup
    --disable-snapshots
    --force-final-checkpoint
    --skip-xdmf
)
if [[ "$FROM_CHECKPOINT" == 1 ]]; then
    RUN_ARGS+=(--from-checkpoint)
fi

cd "$RUN_DIR"
run_re395_mpi "$ENV/bin/python" -u "$RUNNER" "${RUN_ARGS[@]}"

test -s "$CHECKPOINT_H5"
"$ENV/bin/python" - "$CHECKPOINT_H5" "$END_TIME" <<'PY'
import h5py
import sys

path, expected = sys.argv[1], float(sys.argv[2])
with h5py.File(path, "r") as f:
    actual = float(f.attrs["t"])
    tstep = int(f.attrs["tstep"])
if abs(actual - expected) > 1e-8:
    raise SystemExit(f"checkpoint time mismatch: {actual} != {expected}")
print(f"SPINUP_SEGMENT_COMPLETE time={actual:.12g} tstep={tstep}")
PY
