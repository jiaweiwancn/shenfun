#!/usr/bin/env bash
set -euo pipefail

ENV=/media/jay/data1/conda_envs/shenfun_dns_np126_20260702
REPO=/media/jay/data1/shenfun
OUT=/media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713
PREFIX=MKM_production_Lx4pi_64_128_32
export TMPDIR=/media/jay/data1/tmp

cd "$OUT"
test -f "$OUT/${PREFIX}.chk.h5"

run_segment() {
    local start_label=$1
    local end_time=$2
    local file_mode=$3
    local log="$OUT/${PREFIX}_sampling_t${start_label}_t${end_time%.*}_n32.log"

    "$ENV/bin/mpiexec" -n 32 "$ENV/bin/python" -u \
        "$REPO/scripts/mkm_dns_target/run_mkm_dns.py" \
        --output-dir "$OUT" \
        --filename "$PREFIX" \
        --n 64 128 32 \
        --domain -1 1 0 12.566370614359172 0 3.141592653589793 \
        --bulk-velocity 15.678693259774453 \
        --dt 0.0005 \
        --end-time "$end_time" \
        --modsave 200 \
        --checkpoint 10000 \
        --moderror 5000 \
        --modplot -1 \
        --stage-label sampling \
        --from-checkpoint \
        --velocity-file-mode "$file_mode" \
        --force-final-checkpoint \
        --skip-xdmf \
        > "$log" 2>&1
}

run_segment 40 80.0 w
run_segment 80 120.0 a
run_segment 120 160.0 a
run_segment 160 200.0 a

"$ENV/bin/python" -c \
    "from mpi4py_fft import generate_xdmf; generate_xdmf('${PREFIX}_U.h5')"
