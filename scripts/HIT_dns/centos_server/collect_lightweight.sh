#!/bin/bash
# Collect only lightweight outputs and SLURM logs for return to macOS.

set -euo pipefail

if [[ $# -ne 2 ]]; then
    echo "usage: bash collect_lightweight.sh JOB_ID RUN_DIR" >&2
    exit 2
fi

JOB_ID=$1
RUN_DIR=$2
LOG_ROOT=/share/home/dkyzdsys_wanjiawei/shenfun_runs/logs
BUNDLE_DIR="$RUN_DIR/lightweight_return_${JOB_ID}"
BUNDLE_TGZ="$RUN_DIR/lightweight_return_${JOB_ID}.tar.gz"

if [[ -e "$BUNDLE_TGZ" || -d "$BUNDLE_DIR" ]]; then
    echo "refusing to overwrite an existing return bundle" >&2
    exit 2
fi
test -d "$RUN_DIR/light"

mkdir -p "$BUNDLE_DIR/light" "$BUNDLE_DIR/logs"
find "$RUN_DIR/light" -maxdepth 1 -type f \
    \( -name '*.csv' -o -name '*.json' \) -exec cp -p {} "$BUNDLE_DIR/light/" \;
cp -p "$LOG_ROOT"/*_"$JOB_ID".out "$BUNDLE_DIR/logs/" 2>/dev/null || true
cp -p "$LOG_ROOT"/*_"$JOB_ID".err "$BUNDLE_DIR/logs/" 2>/dev/null || true

(
    cd "$BUNDLE_DIR"
    find . -type f ! -name SHA256SUMS -exec sha256sum {} \; | LC_ALL=C sort
) > "$BUNDLE_DIR/SHA256SUMS"
tar -C "$RUN_DIR" -czf "$BUNDLE_TGZ" "$(basename "$BUNDLE_DIR")"
printf 'lightweight_return_bundle=%s\n' "$BUNDLE_TGZ"
printf 'raw_hdf5_files_excluded=true\n'
