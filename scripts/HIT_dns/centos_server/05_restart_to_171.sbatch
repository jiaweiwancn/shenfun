#!/bin/bash
#SBATCH --job-name=hit_dns_to171
#SBATCH --partition=cpu02
#SBATCH --nodes=1
#SBATCH --ntasks=64
#SBATCH --cpus-per-task=1
#SBATCH --time=24:00:00
#SBATCH --output=/share/home/dkyzdsys_wanjiawei/shenfun_runs/logs/%x_%j.out
#SBATCH --error=/share/home/dkyzdsys_wanjiawei/shenfun_runs/logs/%x_%j.err

set -eo pipefail

: "${RESTART_H5:?Submit with --export=ALL,RESTART_H5=/absolute/path/to/latest/complete/checkpoint.h5}"

source /share/home/dkyzdsys_wanjiawei/shenfun-master/scripts/HIT_dns/centos_server/hit_dns_common.sh

RUN_DIR="$RUN_ROOT/production_hit_N384_dt1em4_shenfun"
RAW_DIR="$RUN_DIR/raw"
LIGHT_DIR="$RUN_DIR/light"
mkdir -p "$RAW_DIR" "$LIGHT_DIR"
activate_hit_runtime "$RUN_DIR"
verify_hit_inputs
print_hit_provenance "$RUN_DIR"

case "$RESTART_H5" in
    "$RAW_DIR"/*.h5) ;;
    *)
        echo "RESTART_H5 must be a complete HDF5 file below $RAW_DIR" >&2
        exit 2
        ;;
esac
test -s "$RESTART_H5"
"$ENV/bin/python" -u "$CHECKPOINT_INSPECTOR" "$RUN_DIR" --require "$RESTART_H5"

cd "$RUN_DIR"
run_hit_mpi "$ENV/bin/python" -u "$RUNNER" \
    --backend shenfun \
    --n 384 \
    --length-cm 31.41592653589793 \
    --viscosity-cm2-s 0.14941176470588236 \
    --dt-s 1e-4 \
    --stations 42,98,171 \
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
    --restart "$RESTART_H5" \
    --git-commit "$(hit_git_head)"

test -s "$RAW_DIR/station_0171.h5"
test -s "$LIGHT_DIR/station_0171_summary.json"
printf 'HIT_STATION_171_COMPLETE\n'
