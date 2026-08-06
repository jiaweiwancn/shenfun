#!/bin/bash
#SBATCH --job-name=mkm395_small_rt
#SBATCH --partition=cpu02
#SBATCH --nodes=1
#SBATCH --ntasks=8
#SBATCH --cpus-per-task=1
#SBATCH --time=00:30:00
#SBATCH --output=/share/home/dkyzdsys_wanjiawei/shenfun_runs/logs/%x_%j.out
#SBATCH --error=/share/home/dkyzdsys_wanjiawei/shenfun_runs/logs/%x_%j.err

set -eo pipefail

STATE_COMPRESSION=${STATE_COMPRESSION:-none}
if [[ "$STATE_COMPRESSION" != none && "$STATE_COMPRESSION" != gzip ]]; then
    echo "STATE_COMPRESSION must be none or gzip" >&2
    exit 2
fi

source /share/home/dkyzdsys_wanjiawei/shenfun-master/scripts/mkm_dns_target/re395_server/re395_common.sh

RUN_DIR="$RUN_ROOT/test_small_even_${SLURM_JOB_ID}"
PREFIX=MKM_Re395_small_even
STATE_PREFIX="${PREFIX}_state"
mkdir -p "$RUN_DIR"
activate_re395_runtime "$RUN_DIR"
verify_re395_inputs
print_re395_provenance "$RUN_DIR"

cd "$RUN_DIR"
run_re395_mpi "$ENV/bin/python" -u "$RUNNER" \
    --output-dir "$RUN_DIR" \
    --filename "$PREFIX" \
    --n 18 32 24 \
    --domain -1 1 0 6.283185307179586 0 3.141592653589793 \
    --re "$RE_TAU" \
    --bulk-velocity "$BULK_VELOCITY" \
    --initial-mean-profile "$PROFILE" \
    --dt "$DNS_DT" \
    --padding-factor 1.5 1.5 1.5 \
    --end-time 0.01 \
    --modsave 10 \
    --checkpoint 100 \
    --moderror 10 \
    --modplot -1 \
    --save-mesh quadrature \
    --stage-label sampling \
    --state-every 10 \
    --state-shard-samples 20 \
    --state-prefix "$STATE_PREFIX" \
    --state-compression "$STATE_COMPRESSION" \
    --force-final-checkpoint \
    --skip-xdmf

STATE_H5="$RUN_DIR/${STATE_PREFIX}_tstep000000000010.h5"
VELOCITY_H5="$RUN_DIR/${PREFIX}_U.h5"
ROUNDTRIP_JSON="$RUN_DIR/${PREFIX}_state_roundtrip.json"

run_re395_mpi "$ENV/bin/python" -u "$VALIDATOR" \
    --state-h5 "$STATE_H5" \
    --velocity-h5 "$VELOCITY_H5" \
    --output-json "$ROUNDTRIP_JSON" \
    --max-samples 20 \
    --absolute-tolerance 2e-11 \
    --relative-tolerance 2e-11

"$ENV/bin/python" -u "$STATE_AUDITOR" \
    --shards "$STATE_H5" \
    --output-json "$RUN_DIR/${PREFIX}_state_manifest.json" \
    --check-finite \
    --sha256

"$ENV/bin/python" - "$RUN_DIR" <<'PY'
import json
from pathlib import Path
import sys

run_dir = Path(sys.argv[1])
report = json.loads((run_dir / "MKM_Re395_small_even_state_roundtrip.json").read_text())
assert report["status"] == "PASS", report
assert report["wall_planes_checked"] == 18, report
assert report["samples_checked"] == 20, report
manifest = json.loads((run_dir / "MKM_Re395_small_even_state_manifest.json").read_text())
assert manifest["status"] == "PASS", manifest
assert manifest["finite_check_enabled"] is True, manifest
assert manifest["shards"][0]["nonfinite_values"] == 0, manifest
print("SMALL_EVEN_ROUNDTRIP_PASS")
for path in sorted(run_dir.iterdir()):
    if path.is_file():
        print(f"output_file={path.name} size_bytes={path.stat().st_size}")
PY
