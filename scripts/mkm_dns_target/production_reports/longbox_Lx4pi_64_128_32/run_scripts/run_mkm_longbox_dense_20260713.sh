#!/usr/bin/env bash
set -euo pipefail

ENV=/media/jay/data1/conda_envs/shenfun_dns_np126_20260702
REPO=/media/jay/data1/shenfun
PROD=/media/jay/data1/shenfun_dns_runs/production_mkm_Lx4pi_64_128_32_20260713
PROD_PREFIX=MKM_production_Lx4pi_64_128_32
DENSE_OUT=/media/jay/data1/shenfun_dns_runs/dense_temporal_mkm_Lx4pi_64_128_32_t200_t320_20260713
DENSE_PREFIX=MKM_dense_temporal_Lx4pi_64_128_32_t200_t320
export TMPDIR=/media/jay/data1/tmp

"$ENV/bin/python" -c \
    "import h5py; f=h5py.File('$PROD/${PROD_PREFIX}.chk.h5','r'); assert abs(float(f.attrs['t'])-200.0)<1e-8; assert int(f.attrs['tstep'])==400000; f.close()"

test ! -e "$DENSE_OUT"
mkdir -p "$DENSE_OUT"
cp "$PROD/${PROD_PREFIX}.chk.h5" "$DENSE_OUT/${DENSE_PREFIX}.chk.h5"
cd "$DENSE_OUT"

"$ENV/bin/mpiexec" -n 32 "$ENV/bin/python" -u \
    "$REPO/scripts/mkm_dns_target/run_mkm_dns.py" \
    --output-dir "$DENSE_OUT" \
    --filename "$DENSE_PREFIX" \
    --n 64 128 32 \
    --domain -1 1 0 12.566370614359172 0 3.141592653589793 \
    --bulk-velocity 15.678693259774453 \
    --dt 0.0005 \
    --end-time 320.0 \
    --modsave 20 \
    --checkpoint 10000 \
    --moderror 5000 \
    --modplot -1 \
    --stage-label sampling \
    --from-checkpoint \
    --force-final-checkpoint \
    --skip-xdmf \
    > "$DENSE_OUT/${DENSE_PREFIX}_sampling_t200_t320_n32.log" 2>&1

"$ENV/bin/python" -u "$REPO/scripts/mkm_dns_target/compute_mkm_velocity_autocovariance.py" \
    --velocity-h5 "$DENSE_OUT/${DENSE_PREFIX}_U.h5" \
    --output "$DENSE_OUT/${DENSE_PREFIX}_velocity_autocovariance_lag2.h5" \
    --dt 0.0005 \
    --t-min 200 \
    --t-max 320 \
    --max-lag 200 \
    --z-batch 2 \
    --normalize-plot \
    --max-plot-lag-time 2 \
    --selected-z 0.025 0.5 0.9 \
    --figure "$DENSE_OUT/${DENSE_PREFIX}_velocity_autocovariance_lag2_selected_z.pdf" \
    > "$DENSE_OUT/${DENSE_PREFIX}_autocovariance.log" 2>&1

"$ENV/bin/python" -u "$REPO/scripts/mkm_dns_target/compute_mkm_velocity_autospectrum.py" \
    --velocity-h5 "$DENSE_OUT/${DENSE_PREFIX}_U.h5" \
    --output "$DENSE_OUT/${DENSE_PREFIX}_velocity_autospectrum_hann.h5" \
    --dt 0.0005 \
    --t-min 200 \
    --t-max 320 \
    --z-batch 2 \
    --window hann \
    --log-x \
    --normalize-by-variance \
    --selected-z 0.025 0.5 0.9 \
    --reference-slope -1.6666666666666667 \
    --reference-omega-range 30 120 \
    --figure "$DENSE_OUT/${DENSE_PREFIX}_velocity_autospectrum_hann_selected_z_loglog.pdf" \
    > "$DENSE_OUT/${DENSE_PREFIX}_autospectrum.log" 2>&1
