#!/bin/bash
# Deprecated compatibility guard.
#
# This filename existed in the first upload.  Keeping a non-running guard in
# later archives ensures that extracting an update over that upload cannot
# leave an unsafe odd-wall test behind.

echo "OBSOLETE: odd Chebyshev wall grids are rejected by this MKM solver." >&2
echo "Submit 01_small_even_roundtrip.sbatch instead." >&2
exit 2
