#!/bin/bash
# Prepare an isolated stationary-sampling directory from an accepted checkpoint.

set -eo pipefail

if [[ $# -ne 1 ]]; then
    echo "usage: bash prepare_sampling_checkpoint.sh /absolute/path/to/accepted_spinup.chk.h5" >&2
    exit 2
fi

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
source "$SCRIPT_DIR/re395_common.sh"

SOURCE_CHECKPOINT=$1
SAMPLING_DIR="$RUN_ROOT/production_mkm_Re395_N192_256_192_sampling"
SAMPLING_PREFIX=MKM_Re395_N192_256_192_sampling
DESTINATION="$SAMPLING_DIR/${SAMPLING_PREFIX}.chk.h5"

test -s "$SOURCE_CHECKPOINT"
if [[ -e "$DESTINATION" ]]; then
    echo "refusing to overwrite existing sampling checkpoint: $DESTINATION" >&2
    exit 2
fi

mkdir -p "$SAMPLING_DIR"
activate_re395_runtime "$SAMPLING_DIR"
"$ENV/bin/python" -u "$SCHEDULE_VALIDATOR" checkpoint \
    --checkpoint "$SOURCE_CHECKPOINT" \
    --expected-start "$SAMPLING_START_TIME" \
    --dns-dt "$DNS_DT"
cp -p "$SOURCE_CHECKPOINT" "$DESTINATION"
sha256sum "$DESTINATION"
printf 'sampling_checkpoint=%s\n' "$DESTINATION"
printf 'sampling_window_start=%s\n' "$SAMPLING_START_TIME"
printf 'sampling_window_end=%s\n' "$SAMPLING_FINAL_TIME"
