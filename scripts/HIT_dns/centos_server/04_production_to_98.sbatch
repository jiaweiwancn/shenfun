#!/bin/bash
#SBATCH --job-name=hit_dns_to98
#SBATCH --partition=cpu02
#SBATCH --nodes=1
#SBATCH --ntasks=64
#SBATCH --cpus-per-task=1
#SBATCH --time=24:00:00
#SBATCH --output=/share/home/dkyzdsys_wanjiawei/shenfun_runs/logs/%x_%j.out
#SBATCH --error=/share/home/dkyzdsys_wanjiawei/shenfun_runs/logs/%x_%j.err

set -eo pipefail

source /share/home/dkyzdsys_wanjiawei/shenfun-master/scripts/HIT_dns/centos_server/hit_dns_common.sh

RUN_DIR="$RUN_ROOT/production_hit_N384_dt1em4_shenfun"
RAW_DIR="$RUN_DIR/raw"
LIGHT_DIR="$RUN_DIR/light"
mkdir -p "$RAW_DIR" "$LIGHT_DIR"
activate_hit_runtime "$RUN_DIR"
verify_hit_inputs
print_hit_provenance "$RUN_DIR"

if compgen -G "$RAW_DIR/*.h5" >/dev/null || compgen -G "$LIGHT_DIR/station_*" >/dev/null; then
    echo "Refusing to overwrite existing production output in $RUN_DIR" >&2
    exit 2
fi

cd "$RUN_DIR"
run_hit_mpi "$ENV/bin/python" -u "$RUNNER" \
    --backend shenfun \
    --n 384 \
    --length-cm 31.41592653589793 \
    --viscosity-cm2-s 0.14941176470588236 \
    --dt-s 1e-4 \
    --stations 42,98 \
    --seed 421971 \
    --decomposition pencil \
    --threads 1 \
    --maximum-cfl 0.5 \
    --minimum-kmax-eta 1.0 \
    --diagnostics-every 100 \
    --checkpoint-every 500 \
    --planner-effort FFTW_MEASURE \
    --raw-dir "$RAW_DIR" \
    --light-dir "$LIGHT_DIR" \
    --git-commit "$(hit_git_head)"

test -s "$RAW_DIR/station_0098.h5"
test -s "$LIGHT_DIR/station_0098_summary.json"
printf 'HIT_STATION_98_COMPLETE\n'
