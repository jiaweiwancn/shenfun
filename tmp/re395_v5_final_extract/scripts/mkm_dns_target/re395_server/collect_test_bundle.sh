#!/bin/bash
# Collect small validation artifacts and SLURM logs for return inspection.

set -euo pipefail

if [[ $# -lt 2 || $# -gt 3 ]]; then
    echo "usage: bash collect_test_bundle.sh JOB_ID RUN_DIR [--include-h5]" >&2
    exit 2
fi

JOB_ID=$1
RUN_DIR=$2
INCLUDE_H5=${3:-}
LOG_ROOT=/share/home/dkyzdsys_wanjiawei/shenfun_runs/logs
BUNDLE_DIR="$RUN_DIR/return_bundle_${JOB_ID}"
BUNDLE_TGZ="$RUN_DIR/return_bundle_${JOB_ID}.tar.gz"

if [[ -e "$BUNDLE_TGZ" || -d "$BUNDLE_DIR" ]]; then
    echo "refusing to overwrite an existing return bundle" >&2
    exit 2
fi

mkdir -p "$BUNDLE_DIR"
cp -p "$LOG_ROOT"/*_"$JOB_ID".out "$BUNDLE_DIR/" 2>/dev/null || true
cp -p "$LOG_ROOT"/*_"$JOB_ID".err "$BUNDLE_DIR/" 2>/dev/null || true
find "$RUN_DIR" -maxdepth 1 -type f \
    \( -name '*.json' -o -name '*.txt' -o -name '*.log' \) \
    -exec cp -p {} "$BUNDLE_DIR/" \;

if [[ "$INCLUDE_H5" == --include-h5 ]]; then
    find "$RUN_DIR" -maxdepth 1 -type f -name '*.h5' \
        -exec cp -p {} "$BUNDLE_DIR/" \;
elif [[ -n "$INCLUDE_H5" ]]; then
    echo "third argument must be --include-h5" >&2
    exit 2
fi

(
    cd "$BUNDLE_DIR"
    find . -maxdepth 1 -type f ! -name SHA256SUMS -exec sha256sum {} \; \
        | LC_ALL=C sort
) > "$BUNDLE_DIR/SHA256SUMS"
tar -C "$RUN_DIR" -czf "$BUNDLE_TGZ" "$(basename "$BUNDLE_DIR")"
printf 'return_bundle=%s\n' "$BUNDLE_TGZ"
