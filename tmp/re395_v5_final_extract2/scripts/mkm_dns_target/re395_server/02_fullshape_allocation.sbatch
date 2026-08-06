#!/bin/bash
#SBATCH --job-name=mkm395_full_alloc
#SBATCH --partition=cpu02
#SBATCH --nodes=1
#SBATCH --ntasks=32
#SBATCH --cpus-per-task=1
#SBATCH --time=01:00:00
#SBATCH --output=/share/home/dkyzdsys_wanjiawei/shenfun_runs/logs/%x_%j.out
#SBATCH --error=/share/home/dkyzdsys_wanjiawei/shenfun_runs/logs/%x_%j.err

set -eo pipefail

source /share/home/dkyzdsys_wanjiawei/shenfun-master/scripts/mkm_dns_target/re395_server/re395_common.sh

RUN_DIR="$RUN_ROOT/test_fullshape_allocation_${SLURM_JOB_ID}"
PREFIX=MKM_Re395_fullshape_allocation
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
    --end-time 0.0005 \
    --modsave 100000000 \
    --checkpoint 10 \
    --moderror 5 \
    --modplot -1 \
    --stage-label spinup \
    --disable-snapshots \
    --force-final-checkpoint \
    --skip-xdmf

test -s "$RUN_DIR/${PREFIX}.chk.h5"
printf 'FULLSHAPE_ALLOCATION_PASS checkpoint_size_bytes=%s\n' \
    "$(stat -c %s "$RUN_DIR/${PREFIX}.chk.h5")"
