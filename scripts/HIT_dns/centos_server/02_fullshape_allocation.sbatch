#!/bin/bash
#SBATCH --job-name=hit_dns_n384_alloc
#SBATCH --partition=cpu02
#SBATCH --nodes=1
#SBATCH --ntasks=32
#SBATCH --cpus-per-task=1
#SBATCH --time=01:00:00
#SBATCH --output=/share/home/dkyzdsys_wanjiawei/shenfun_runs/logs/%x_%j.out
#SBATCH --error=/share/home/dkyzdsys_wanjiawei/shenfun_runs/logs/%x_%j.err

set -eo pipefail

source /share/home/dkyzdsys_wanjiawei/shenfun-master/scripts/HIT_dns/centos_server/hit_dns_common.sh

RUN_DIR="$RUN_ROOT/fullshape_allocation_${SLURM_JOB_ID}"
mkdir -p "$RUN_DIR"
activate_hit_runtime "$RUN_DIR"
verify_hit_inputs
print_hit_provenance "$RUN_DIR"

cd "$RUN_DIR"
run_hit_mpi "$ENV/bin/python" -u "$MPI_CHECK" \
    --backend shenfun \
    --n 384 \
    --steps 0 \
    --decomposition pencil \
    --planner-effort FFTW_ESTIMATE

printf 'HIT_FULLSHAPE_ALLOCATION_PASS\n'
