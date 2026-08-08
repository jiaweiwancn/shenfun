# CentOS/SLURM submission package for decaying HIT

## Material Passport

- Origin Skill: experiment-agent
- Origin Mode: run preparation
- Origin Date: 2026-08-08
- Verification Status: pure-Shenfun backend matched spectralDNS bit-for-bit in
  a four-rank six-step checkpoint gate; CentOS gates are prepared but not yet
  submitted
- Version Label: hit_dns_centos_jobs_v1

This package runs the Comte-Bellot--Corrsin decaying-HIT calculation in the
validated, offline CentOS 7 environment.  It does not install or update any
package.  The CentOS environment has Shenfun 4.3.0 but no `spectralDNS`, so the
jobs select the in-repository `--backend shenfun` implementation.  That backend
uses the same rotational nonlinearity, Leray projection, 3/2 padding, and RK4
stages as the original workstation backend.  On the Linux test host, all
52,224 complex coefficients in the two four-rank `32^3` checkpoints were
bitwise equal after six steps (maximum absolute difference zero).

The package assumes the validated paths from
`HANDOFF_SHENFUN_SERVER_JOB_SUBMISSION.md`:

```text
repository  /share/home/dkyzdsys_wanjiawei/shenfun-master
environment /share/home/dkyzdsys_wanjiawei/shenfun_offline_centos_install/env
partition   cpu02
launcher    HYDRA_LAUNCHER=fork, one node only
run root    /share/home/dkyzdsys_wanjiawei/shenfun_runs/hit_dns
```

## Files to deploy

The prepared archive is
`scripts/HIT_dns/hit_dns_centos_submission_20260808.tar.gz`.  Copy it and its
`.sha256` file to the CentOS login node, verify the archive, and extract it at
the repository root:

```bash
cd /share/home/dkyzdsys_wanjiawei/shenfun-master
sha256sum --check hit_dns_centos_submission_20260808.tar.gz.sha256
tar -xzf hit_dns_centos_submission_20260808.tar.gz
```

The archive contains only the HIT Python sources, experimental CSV tables,
tests, and this `centos_server` directory.  It contains no raw DNS field.

## One-time preparation

SLURM opens output and error files before the job script starts, so create the
log and run roots on the login node first:

```bash
mkdir -p /share/home/dkyzdsys_wanjiawei/shenfun_runs/logs
mkdir -p /share/home/dkyzdsys_wanjiawei/shenfun_runs/hit_dns

cd /share/home/dkyzdsys_wanjiawei/shenfun-master
source /share/home/dkyzdsys_wanjiawei/shenfun_offline_centos_install/activate_shenfun.sh
bash -n scripts/HIT_dns/centos_server/*.sh
bash -n scripts/HIT_dns/centos_server/*.sbatch
python -m pytest -q scripts/HIT_dns/tests
python scripts/HIT_dns/run_hit_dns.py --help
python scripts/HIT_dns/mpi_initial_condition_check.py --help
sha256sum --check scripts/HIT_dns/centos_server/RUNTIME_SHA256SUMS
```

Expected unit-test result: `19 passed`.  Do not run `conda install`,
`conda update`, or `pip install`.

Every job reserves two SLURM tasks per launched MPI rank, matching the policy
already exercised on this cluster.  The smoke job therefore allocates eight
tasks and launches four ranks; production allocates 64 tasks and launches 32
ranks.  Every numerical-library thread count is fixed at one.

## Gate A: four-rank MPI smoke test

```bash
cd /share/home/dkyzdsys_wanjiawei/shenfun-master/scripts/HIT_dns/centos_server
JOB_ID=$(sbatch --parsable 01_mpi_smoke.sbatch | cut -d';' -f1)
echo "$JOB_ID"
```

Successful output ends with both `"passed": true` and
`HIT_MPI_SMOKE_PASS`.  Confirm `COMPLETED`, exit code `0:0`, and an empty error
log before continuing:

```bash
squeue -j "$JOB_ID"
sacct -j "$JOB_ID" --format=JobID,JobName,State,ExitCode,Elapsed,AllocCPUS,NodeList
tail -n 80 /share/home/dkyzdsys_wanjiawei/shenfun_runs/logs/hit_dns_smoke_${JOB_ID}.out
cat /share/home/dkyzdsys_wanjiawei/shenfun_runs/logs/hit_dns_smoke_${JOB_ID}.err
```

## Gate B: full-shape allocation and nonlinear operator

After Gate A passes:

```bash
JOB_ID=$(sbatch --parsable 02_fullshape_allocation.sbatch | cut -d';' -f1)
echo "$JOB_ID"
```

This allocates the `384^3` base mesh and `576^3` padded transforms on 16 MPI
ranks, initializes the fixed-seed field, and evaluates the nonlinear energy
gate without advancing time.  The terminal marker is
`HIT_FULLSHAPE_ALLOCATION_PASS`.

## Gate C: 32-rank, 11-step full-resolution pilot

After Gate B passes:

```bash
JOB_ID=$(sbatch --parsable 03_short_pilot.sbatch | cut -d';' -f1)
echo "$JOB_ID"
```

This uses the production mesh, timestep, 32 ranks, parallel HDF5, numerical
gates, and station output path.  It advances only from station 42 to 42.2.
Accept the production templates only after the log ends with
`HIT_SHORT_PILOT_PASS`, SLURM reports `COMPLETED 0:0`, CFL is at most 0.5,
`kmax_eta` is at least 1, and divergence/Parseval gates pass.

## Production stage 1: station 42 to 98

```bash
JOB98=$(sbatch --parsable 04_production_to_98.sbatch | cut -d';' -f1)
echo "$JOB98"
```

The stage uses a fixed run directory and refuses to overwrite any existing
production HDF5 or station product.  It launches 32 ranks for at most 24 hours,
writes a complete checkpoint every 500 steps, and ends with
`HIT_STATION_98_COMPLETE`.

## Production stage 2: restart to station 171

First identify the latest complete checkpoint.  The inspector ignores
`.partial` files, validates the schema and spectral shape, and prints one
`LATEST_CHECKPOINT=` line:

```bash
RUN_DIR=/share/home/dkyzdsys_wanjiawei/shenfun_runs/hit_dns/production_hit_N384_dt1em4_shenfun
python inspect_hit_checkpoints.py "$RUN_DIR"
```

Normally the latest file after stage 1 is `raw/station_0098.h5`.  Pass the
exact reported path explicitly:

```bash
RESTART_H5="$RUN_DIR/raw/station_0098.h5"
JOB171=$(sbatch --parsable \
  --export=ALL,RESTART_H5="$RESTART_H5" \
  05_restart_to_171.sbatch | cut -d';' -f1)
echo "$JOB171"
```

The restart job rejects a path outside the production raw directory and
rejects a valid-but-older checkpoint.  Successful completion requires
`HIT_STATION_171_COMPLETE`, SLURM `COMPLETED`, exit code `0:0`, no traceback or
MPI abort, and passing numerical gates at station 171.

If either production stage terminates early, do not silently resubmit it.
Inspect the SLURM state, both logs, and the latest complete checkpoint first.
Preserve every `.partial` file until restart safety is assessed.

## Return only lightweight results

After station 171 completes:

```bash
bash collect_lightweight.sh "$JOB171" "$RUN_DIR"
```

The resulting `lightweight_return_<job>.tar.gz` contains station CSV/JSON,
`diagnostics.csv`, logs, and checksums.  It deliberately excludes every raw
HDF5 field and checkpoint.  Keep those large files on CentOS.
