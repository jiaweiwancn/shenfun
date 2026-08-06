#!/usr/bin/env bash
set -euo pipefail

ENV=/media/jay/data1/conda_envs/shenfun_dns_np126_20260702
REPO=/media/jay/data1/shenfun
OUT=/media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713
PREFIX=MKM_production_Lx4pi_64_128_32

TMIN=$("$ENV/bin/python" -c \
    "import json; from pathlib import Path; out=Path('$OUT'); prefix='$PREFIX'; candidates=(40,60,80); passing=[t for t in candidates if json.load(open(out/f'{prefix}_sampling_field_convergence_t{t}_t200.json'))['converged_by_tolerance']]; print(passing[0] if passing else '')")

if [[ -z "$TMIN" ]]; then
    echo "no candidate sparse window passed" >&2
    exit 3
fi

echo "$TMIN" > "$OUT/${PREFIX}_accepted_tmin.txt"
TAG=t${TMIN}_t200
TARGET=$OUT/${PREFIX}_target_${TAG}.h5

"$OUT/postprocess_mkm_longbox_target_20260713.sh" "$TMIN" \
    > "$OUT/${PREFIX}_target_${TAG}_postprocess_audit_projection.log" 2>&1

"$ENV/bin/python" -u "$REPO/scripts/mkm_dns_target/plot_mkm_dns_results.py" \
    --target-h5 "$TARGET" \
    --velocity-h5 "$OUT/${PREFIX}_U.h5" \
    --diagnostics-json "$OUT/${PREFIX}_sampling_t40_t200_diagnostics.json" \
    --output-dir "$OUT/figures_${TAG}" \
    --dt 0.0005 \
    --instant-time 200 \
    --accepted-t-min "$TMIN" \
    --half-height 1 \
    --friction-velocity 1 \
    --re-tau 180 \
    > "$OUT/${PREFIX}_figures_${TAG}.log" 2>&1

"$OUT/run_mkm_longbox_resolvent_20260713.sh" "$TMIN" target \
    > "$OUT/${PREFIX}_resolvent_target_${TAG}.log" 2>&1

"$OUT/run_mkm_longbox_dense_20260713.sh" \
    > "$OUT/${PREFIX}_dense_t200_t320_pipeline.log" 2>&1

"$OUT/run_mkm_longbox_resolvent_20260713.sh" "$TMIN" dense \
    > "$OUT/${PREFIX}_resolvent_dense_${TAG}.log" 2>&1
