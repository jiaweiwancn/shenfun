#!/bin/bash
#SBATCH --job-name=mkm395_full_io
#SBATCH --partition=cpu02
#SBATCH --nodes=1
#SBATCH --ntasks=128
#SBATCH --cpus-per-task=1
#SBATCH --time=01:00:00
#SBATCH --output=/share/home/dkyzdsys_wanjiawei/shenfun_runs/logs/%x_%j.out
#SBATCH --error=/share/home/dkyzdsys_wanjiawei/shenfun_runs/logs/%x_%j.err

set -eo pipefail

source /share/home/dkyzdsys_wanjiawei/shenfun-master/scripts/mkm_dns_target/re395_server/re395_common.sh

RUN_DIR="$RUN_ROOT/test_fullshape_state_io_${SLURM_JOB_ID}"
PREFIX=MKM_Re395_fullshape_state_io
STATE_PREFIX="${PREFIX}_state"
mkdir -p "$RUN_DIR"
activate_re395_runtime "$RUN_DIR"
verify_re395_inputs
print_re395_provenance "$RUN_DIR"

cd "$RUN_DIR"
run_re395_mpi "$ENV/bin/python" -u "$RUNNER" \
    --output-dir "$RUN_DIR" \
    --filename "$PREFIX" \
    --n 192 256 192 \
    --domain -1 1 0 6.283185307179586 0 3.141592653589793 \
    --re "$RE_TAU" \
    --bulk-velocity "$BULK_VELOCITY" \
    --initial-mean-profile "$PROFILE" \
    --dt "$DNS_DT" \
    --padding-factor "$PADDING_WALL" "$PADDING_STREAM" "$PADDING_SPAN" \
    --end-time "$DNS_DT" \
    --modsave 1 \
    --checkpoint 1 \
    --moderror 1 \
    --modplot -1 \
    --save-mesh quadrature \
    --stage-label sampling \
    --state-every 1 \
    --state-shard-samples 1 \
    --state-prefix "$STATE_PREFIX" \
    --state-compression none \
    --force-final-checkpoint \
    --skip-xdmf

STATE_H5="$RUN_DIR/${STATE_PREFIX}_tstep000000000001.h5"
VELOCITY_H5="$RUN_DIR/${PREFIX}_U.h5"
ROUNDTRIP_JSON="$RUN_DIR/${PREFIX}_state_roundtrip.json"

run_re395_mpi "$ENV/bin/python" -u "$VALIDATOR" \
    --state-h5 "$STATE_H5" \
    --velocity-h5 "$VELOCITY_H5" \
    --output-json "$ROUNDTRIP_JSON" \
    --max-samples 1 \
    --absolute-tolerance 2e-11 \
    --relative-tolerance 2e-11

"$ENV/bin/python" -u "$STATE_AUDITOR" \
    --shards "$STATE_H5" \
    --output-json "$RUN_DIR/${PREFIX}_state_manifest.json" \
    --check-finite

grep -q '"status": "PASS"' "$ROUNDTRIP_JSON"
grep -q '"status": "PASS"' "$RUN_DIR/${PREFIX}_state_manifest.json"
printf 'FULLSHAPE_STATE_IO_PASS state_size_bytes=%s velocity_size_bytes=%s\n' \
    "$(stat -c %s "$STATE_H5")" \
    "$(stat -c %s "$VELOCITY_H5")"
