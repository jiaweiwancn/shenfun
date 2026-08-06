# Re_tau=395 CentOS/SLURM submission package

## Material Passport

- Origin Skill: experiment-agent
- Origin Mode: run preparation
- Origin Date: 2026-07-27
- Verification Status: CentOS numerical/I/O gates passed; refined-step production pilot pending
- Version Label: re395_server_jobs_v5

## Execution status

These files prepare the updated all-plane plan for the CentOS 7 server.  The
solver, writer, validator, and auditor passed the numerical and HDF5 gates on
both the Ubuntu test server and the CentOS/SLURM server.  CentOS jobs
3200--3204 established the small-grid round trip, full-shape allocations at
16, 32, and 64 MPI ranks, and the 64-rank full-shape state-I/O round trip.
Job 3206 then showed that the former full-resolution step
`dt=0.00025` was unstable.  This version refines the production step to
`dt=0.00005`; a new refined-step production pilot remains mandatory before
long spin-up or stationary sampling.

The package assumes the validated paths from
`HANDOFF_SHENFUN_SERVER_JOB_SUBMISSION.md`:

```text
repository  /share/home/dkyzdsys_wanjiawei/shenfun-master
environment /share/home/dkyzdsys_wanjiawei/shenfun_offline_centos_install/env
partition   cpu02
launcher    HYDRA_LAUNCHER=fork, one node only
```

The requested allocation policy reserves two SLURM tasks for each launched
MPI rank.  For example, every 64-rank job has `#SBATCH --ntasks=128`, while
the launcher explicitly executes `mpiexec -n 64`.  `re395_common.sh` validates
this 2:1 ratio, reports both numbers, and rejects an odd `SLURM_NTASKS`.
The second allocated task per rank is intentionally not launched.

## Files that must be copied to the server repository

Preserve their repository-relative paths:

```text
demo/MKM.py
scripts/mkm_dns_target/run_mkm_dns.py
scripts/mkm_dns_target/mkm_state_io.py
scripts/mkm_dns_target/validate_mkm_state_roundtrip.py
scripts/mkm_dns_target/inspect_mkm_state_shards.py
scripts/mkm_dns_target/re395_server/validate_re395_schedule.py
scripts/mkm_dns_target/data/chan395.means
scripts/mkm_dns_target/re395_server/*
```

The official profile checksum is:

```text
211c6b8149cc7ef5cd20323716b47a45dd98cca55486a9554acfd4a7975d737a
```

Source:
`https://turbulence.oden.utexas.edu/data/MKM/chan395/profiles/chan395.means`
(retrieved 24 July 2026). The bundled file is unchanged.

The job scripts verify this checksum before running.

## One-time server preparation

On the login node:

```bash
mkdir -p /share/home/dkyzdsys_wanjiawei/shenfun_runs/logs
mkdir -p /share/home/dkyzdsys_wanjiawei/shenfun_runs/re395

cd /share/home/dkyzdsys_wanjiawei/shenfun-master
source /share/home/dkyzdsys_wanjiawei/shenfun_offline_centos_install/activate_shenfun.sh

python scripts/mkm_dns_target/run_mkm_dns.py --help
python scripts/mkm_dns_target/validate_mkm_state_roundtrip.py --help
python scripts/mkm_dns_target/inspect_mkm_state_shards.py --help
python scripts/mkm_dns_target/re395_server/validate_re395_schedule.py --help
sha256sum scripts/mkm_dns_target/data/chan395.means

bash -n scripts/mkm_dns_target/re395_server/*.sh
bash -n scripts/mkm_dns_target/re395_server/*.sbatch
```

Do not install or update packages in the offline environment.

The jobs require the nounset-safe activation helper distributed with the
updated CentOS handoff.  Its checksum is:

```text
cbc2b58388e5dea858f0d861ebbd7607a1a9a4c06633a9957870a8e5c6f854dd
```

Verify the copied install support files before submitting:

```bash
cd /share/home/dkyzdsys_wanjiawei/shenfun_offline_centos_install
sha256sum -c SHA256SUMS
```

Each SLURM script starts with `set -eo pipefail`.  The shared runtime activates
the relocated environment and then immediately enables `set -u`.  This ordering
avoids the generated Conda activation script reading an unset `CONDA_PREFIX`,
while retaining strict nounset checking for the simulation itself.

The shared runtime also imports Matplotlib once before `mpiexec`.  This
serially creates the per-run font cache and prevents a first high-rank launch
from contending for the same `fontlist` lock file.

Git provenance is optional.  The shared runtime first checks whether `git`
exists and uses a repository-local command only when it does.  On compute
nodes without Git it prints
`git_provenance=unavailable reason=git_not_found`; it does not emit a shell
error or stop the job.

## Ubuntu verification record

The upload candidate was tested in an isolated repository copy at
`/media/jay/data1/tmp/re395_n192_validation_fEdJVNep/repo`; the existing
Ubuntu repository and production data were not modified.  The environment
used Shenfun 4.3.0, NumPy 1.26.4, SciPy 1.15.2, h5py 3.11 with MPI, and MPICH
4.2.1.

Verified on 24 July 2026:

- the 4-rank `(18,32,24)` test completed 40 steps and 20 paired samples,
  with zero physical reconstruction error, no NaN/Inf, and maximum divergence
  `1.26e-15`;
- the full `(192,256,192)` shape with padded `(288,384,288)` completed two
  DNS steps at 16, 32, and 64 ranks;
- the 64-rank full-shape I/O test reconstructed all 192 planes from one
  independent-state sample, with maximum absolute component error
  `2.14e-14`, maximum relative error `1.06e-15`, maximum divergence
  `9.53e-16`, and no NaN/Inf;
- the measured full-shape state file was `152,594,328` bytes and its paired
  physical velocity file was `226,523,696` bytes; and
- a reduced spin-up plus two consecutive sampling segments passed checkpoint
  restart, velocity-file append, two state-shard continuity checks, and exact
  reconstruction for all eight retained samples; and
- the fixed-window schedule validator passed Ubuntu boundary tests for the
  `t=120` checkpoint, intermediate segments, the `t=300` completion with
  36,000 samples, and rejection of an end time beyond 300.

The first 64-rank attempt exposed a Matplotlib font-cache lock race before the
solver imported.  The serial cache warm-up in `re395_common.sh` fixed that
startup defect; the corrected 64-rank rerun passed.  These are functional
pilots, not a stationarity or turbulence-resolution validation.

The v5 candidate was revalidated on Ubuntu on 27 July 2026.  Its 4-rank
`(18,32,24)` test completed 200 refined steps with 20 samples at the preserved
`0.0005` output spacing.  CFL remained at or below `0.00609`, the state
manifest found zero non-finite values, maximum divergence was
`1.06e-15`, and every reconstructed physical velocity value matched the
conventional output exactly.

## Target-server verification and time-step decision

CentOS jobs 3200--3204 passed the small round trip, full-shape allocations at
16, 32, and 64 MPI ranks, and the 64-rank full-shape I/O test.  Job 3206 was
the first longer full-resolution production pilot with `dt=0.00025`; it is a
failed stability result, not a usable checkpoint.  Its CFL was `1.007` at
`t=0.1`, reached approximately `1.60`, and its spanwise energy rose from
`0.3907` to `12.8004` by `t=0.8`.  At `t=0.9`, all 28,311,552 physical
velocity values were non-finite.

For Chebyshev-Gauss grids, the nearest-wall spacing at 192 points is about one
ninth that at 64 points.  Scaling the prior Re_tau=180 step `0.0005` by this
ratio gives approximately `0.0000556`; this package uses the conservative
rounded value `0.00005`.  Do not continue from job 3206.

## Why the package now uses an even wall-normal size

The MKM reference table uses 193 wall-normal points in its endpoint-including
Chebyshev convention.  Shenfun's optimized Chebyshev biharmonic solver splits
the coefficient system into equal even/odd parity blocks.  A real four-rank
test with `N_wall=17` initialized successfully but generated non-finite
coefficients in the first Runge--Kutta substage.  Its matched `N_wall=18`
control remained finite and passed the exact all-plane state round trip.

The selected Shenfun production size is therefore `N_wall=192`.  This is less
than the paper's count by one point (about 0.52 percent), retains 14 saved
points per wall below `y+=10`, and is compatible with the current solver.
The runner rejects odd Chebyshev wall sizes before allocation.

## Gate A: small even-grid round trip

Submit this first:

```bash
cd /share/home/dkyzdsys_wanjiawei/shenfun-master/scripts/mkm_dns_target/re395_server
JOB_ID=$(sbatch --parsable 01_small_even_roundtrip.sbatch | cut -d';' -f1)
echo "$JOB_ID"
```

Monitor:

```bash
squeue -j "$JOB_ID"
tail -f /share/home/dkyzdsys_wanjiawei/shenfun_runs/logs/mkm395_small_rt_${JOB_ID}.out
tail -f /share/home/dkyzdsys_wanjiawei/shenfun_runs/logs/mkm395_small_rt_${JOB_ID}.err
sacct -j "$JOB_ID" --format=JobID,JobName,State,ExitCode,Elapsed,AllocCPUS,NodeList
```

Expected terminal markers:

```text
"status": "PASS"
SMALL_EVEN_ROUNDTRIP_PASS
```

The test uses:

```text
mesh                  18 x 32 x 24
MPI ranks             4
SLURM tasks           8
DNS steps             200
dense/state cadence   every 10 steps
paired samples        20
state compression     none
```

It checks all 18 wall-normal planes and all three velocities, rejects any
NaN/Inf in both archives, and writes only small test data.

After completion, make a return bundle:

```bash
RUN_DIR=/share/home/dkyzdsys_wanjiawei/shenfun_runs/re395/test_small_even_${JOB_ID}
bash collect_test_bundle.sh "$JOB_ID" "$RUN_DIR" --include-h5
```

Copy `return_bundle_${JOB_ID}.tar.gz` back for inspection. The most important
files are the SLURM output/error logs, run-config JSON, round-trip JSON, state
HDF5, and conventional velocity HDF5.

### Optional small lossless-compression check

Only after the uncompressed test passes:

```bash
JOB_ID=$(sbatch --parsable \
  --export=ALL,STATE_COMPRESSION=gzip \
  01_small_even_roundtrip.sbatch | cut -d';' -f1)
echo "$JOB_ID"
```

This verifies exact decompression on a small job. It does not establish that
parallel gzip will scale efficiently at the production mesh.

## Gate B: full-shape allocation and decomposition

After Gate A is accepted:

```bash
JOB_ID=$(sbatch --parsable 02_fullshape_allocation.sbatch | cut -d';' -f1)
echo "$JOB_ID"
```

This runs ten refined DNS steps at `(192,256,192)` with padded shape
`(288,384,288)`, 16 MPI ranks from 32 allocated SLURM tasks, no velocity or
temporal-state output, and a final checkpoint. Return the SLURM logs and
run-config JSON; the checkpoint need not be copied back.

Repeat successful allocation tests with explicit allocation overrides:

```bash
sbatch --ntasks=64 02_fullshape_allocation.sbatch   # launches 32 ranks
sbatch --ntasks=128 02_fullshape_allocation.sbatch  # launches 64 ranks
```

Do not set `--ntasks=64` when intending to launch 64 ranks: under this package
that allocation launches 32 ranks.  The target-server results from jobs
3201--3203 support a 64-rank production candidate, but refined-step timing
still has to be measured.

## Gate C: one-sample full-shape state I/O

After a full-shape rank count works:

```bash
JOB_ID=$(sbatch --parsable 02b_fullshape_state_io.sbatch | cut -d';' -f1)
echo "$JOB_ID"
```

The header allocates 128 tasks and launches 64 MPI ranks, matching the
successful target-server Gate B result.
The job writes one conventional physical field and one independent-state
sample, then performs the same all-plane round trip. Expected marker:

```text
FULLSHAPE_STATE_IO_PASS
```

Return logs, run-config JSON, and round-trip JSON. The approximately
hundreds-of-MiB HDF5 files need not be copied back unless the JSON comparison
fails.

## Gate D: spin-up segments

This is a production template, not authorization to submit. Select the rank
count from Gates B/C and review the measured step time and memory first.

The fixed spin-up target is `t=120`, or 2,400,000 DNS steps. Use restartable
segments rather than attempting all 120 outer units in one allocation.  First
measure a refined-step calibration segment to `t=1`:

```bash
sbatch --ntasks=128 \
  --export=ALL,END_TIME=1,FROM_CHECKPOINT=0 \
  03_spinup_segment.sbatch
```

Only after its CFL, energy, finite-value, wall-stress, memory, and wall-clock
records are accepted, continue to outer time 5:

```bash
sbatch --ntasks=128 \
  --export=ALL,END_TIME=5,FROM_CHECKPOINT=1 \
  03_spinup_segment.sbatch
```

`END_TIME` is absolute, not a duration.  If the measured throughput fits the
24-hour limit, use five-outer-unit continuations through `t=120`, with
physical reviews at 20, 40, 60, 80, 100, and 120.  Do not assume a larger
segment is safe merely because its schedule is valid.  The schedule validator
refuses any spin-up end after 120.  The checkpoint at 120 is transferred to
sampling only if the stationarity criteria pass. Each job:

- allocates 128 SLURM tasks and launches 64 MPI ranks;
- uses `dt=0.00005`;
- writes no velocity/state time series;
- checkpoints every 100,000 steps (five outer time units);
- reports energy, flux, divergence, two wall stresses, measured `Re_tau`, and
  a documented CFL estimate every 2,000 steps (0.1 outer units);
- forces a final checkpoint; and
- writes a job-tagged run-config JSON.

Stationarity acceptance still requires profile, stress, spectral-tail,
half-box-correlation, and symmetry review. Scalar log stability alone is not
sufficient.

## Gate E: stationary all-plane sampling

After the `t=120` spin-up checkpoint is accepted, isolate it:

```bash
bash prepare_sampling_checkpoint.sh \
  /share/home/dkyzdsys_wanjiawei/shenfun_runs/re395/production_mkm_Re395_N192_256_192_spinup/MKM_Re395_N192_256_192_spinup.chk.h5
```

The preparation script rejects a checkpoint that is not exactly at `t=120`
(`tstep=2400000`). The first five-unit sampling job is:

```bash
sbatch --ntasks=128 \
  --export=ALL,END_TIME=125,STATE_COMPRESSION=none \
  04_sampling_segment.sbatch
```

After each successful job, continue with absolute end times 130, 135, and so
on through 300.  Each job therefore closes exactly one 1,000-sample shard.
Do not submit the next segment until the prior checkpoint and manifest have
passed. The scripts reject sampling before 120 or after 300.  The fixed
180-outer-time-unit window contains 36,000 state samples and 36 complete
1,000-sample shards.

The sampling template:

- allocates 128 SLURM tasks and launches 64 MPI ranks;
- saves the independent spectral state every 100 DNS steps
  (`Delta t_sample=0.005`);
- creates a closed state shard every 1,000 samples/five outer time units;
- uses complex128/float64 without wall-normal or modal truncation;
- saves a conventional audit field every 200,000 steps/ten outer time units;
- checkpoints every 100,000 steps/five outer time units; and
- refuses to overwrite existing state shards.

Use `STATE_COMPRESSION=none` for capacity and performance planning until the
gzip pilot is accepted. Compression is lossless but its ratio and parallel
write cost are empirical.

## Failure handling

- Do not resubmit blindly after any traceback, MPI abort, HDF5 error, nonzero
  SLURM exit code, or leftover `*.partial.h5`.
- Preserve the SLURM logs, checkpoint, completed state shards, and partial
  shard.
- Never rename a partial shard to a completed `.h5`.
- Do not overwrite the sampling checkpoint or audit file.
- Return a log/JSON bundle for diagnosis. Retry decisions are made after the
  failure is understood.

## Expected storage

At the production mesh:

```text
one independent-state sample          0.142093 GiB uncompressed
one 1,000-sample state shard         142.09 GiB uncompressed
36,000 samples / 180 outer units       4.9954 TiB uncompressed
equivalent dense velocity archive      7.4158 TiB uncompressed
18 complete audit velocity fields      3.7969 GiB uncompressed
```

Target at least 7 TiB for the retained baseline record, checkpoints, audit
fields, derived outputs, and safety headroom, excluding any disposable
postprocessing cache.
