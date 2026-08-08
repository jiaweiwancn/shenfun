#!/bin/bash
#SBATCH --job-name=hit_dns_n384_pilot
#SBATCH --partition=cpu02
#SBATCH --nodes=1
#SBATCH --ntasks=64
#SBATCH --cpus-per-task=1
#SBATCH --time=02:00:00
#SBATCH --output=/share/home/dkyzdsys_wanjiawei/shenfun_runs/logs/%x_%j.out
#SBATCH --error=/share/home/dkyzdsys_wanjiawei/shenfun_runs/logs/%x_%j.err

set -eo pipefail

source /share/home/dkyzdsys_wanjiawei/shenfun-master/scripts/HIT_dns/centos_server/hit_dns_common.sh

RUN_DIR="$RUN_ROOT/short_pilot_${SLURM_JOB_ID}"
RAW_DIR="$RUN_DIR/raw"
LIGHT_DIR="$RUN_DIR/light"
mkdir -p "$RAW_DIR" "$LIGHT_DIR"
activate_hit_runtime "$RUN_DIR"
verify_hit_inputs
print_hit_provenance "$RUN_DIR"

cd "$RUN_DIR"
run_hit_mpi "$ENV/bin/python" -u "$RUNNER" \
    --backend shenfun \
    --n 384 \
    --length-cm 31.41592653589793 \
    --viscosity-cm2-s 0.14941176470588236 \
    --dt-s 1e-4 \
    --stations 42,42.2 \
    --seed 421971 \
    --decomposition pencil \
    --threads 1 \
    --maximum-cfl 0.5 \
    --minimum-kmax-eta 1.0 \
    --diagnostics-every 5 \
    --checkpoint-every 0 \
    --planner-effort FFTW_ESTIMATE \
    --raw-dir "$RAW_DIR" \
    --light-dir "$LIGHT_DIR" \
    --git-commit "$(hit_git_head)"

test -s "$RAW_DIR/station_0042.h5"
test -s "$RAW_DIR/station_0042p2.h5"
test -s "$LIGHT_DIR/station_0042p2_summary.json"
test -s "$LIGHT_DIR/diagnostics.csv"
printf 'HIT_SHORT_PILOT_PASS\n'
