#!/bin/bash
# Shared, source-only configuration for Re_tau=395 SLURM jobs.

INSTALL=/share/home/dkyzdsys_wanjiawei/shenfun_offline_centos_install
ENV="$INSTALL/env"
REPO=/share/home/dkyzdsys_wanjiawei/shenfun-master
RUN_ROOT=/share/home/dkyzdsys_wanjiawei/shenfun_runs/re395
LOG_ROOT=/share/home/dkyzdsys_wanjiawei/shenfun_runs/logs

RUNNER="$REPO/scripts/mkm_dns_target/run_mkm_dns.py"
VALIDATOR="$REPO/scripts/mkm_dns_target/validate_mkm_state_roundtrip.py"
STATE_AUDITOR="$REPO/scripts/mkm_dns_target/inspect_mkm_state_shards.py"
SCHEDULE_VALIDATOR="$REPO/scripts/mkm_dns_target/re395_server/validate_re395_schedule.py"
PROFILE="$REPO/scripts/mkm_dns_target/data/chan395.means"
PROFILE_SHA256=211c6b8149cc7ef5cd20323716b47a45dd98cca55486a9554acfd4a7975d737a

RE_TAU=395
BULK_VELOCITY=17.54475114359453
DNS_DT=0.00005
SPINUP_FINAL_TIME=120
SAMPLING_START_TIME=120
SAMPLING_FINAL_TIME=300
SAMPLING_DT=0.005
STATE_SHARD_SAMPLES=1000
DIAGNOSTIC_EVERY_STEPS=2000
CHECKPOINT_EVERY_STEPS=100000
STATE_EVERY_STEPS=100
AUDIT_EVERY_STEPS=200000
SLURM_TASKS_PER_MPI_RANK=2
PADDING_WALL=1.5
PADDING_STREAM=1.5
PADDING_SPAN=1.5

re395_mpi_ranks() {
    local allocated_tasks="${SLURM_NTASKS:-$SLURM_TASKS_PER_MPI_RANK}"

    if [[ ! "$allocated_tasks" =~ ^[0-9]+$ ]] || (( allocated_tasks <= 0 )); then
        echo "SLURM_NTASKS must be a positive integer; got '$allocated_tasks'" >&2
        return 2
    fi
    if (( allocated_tasks % SLURM_TASKS_PER_MPI_RANK != 0 )); then
        echo "SLURM_NTASKS=$allocated_tasks is not divisible by the required allocation ratio $SLURM_TASKS_PER_MPI_RANK:1" >&2
        return 2
    fi
    printf '%s\n' "$(( allocated_tasks / SLURM_TASKS_PER_MPI_RANK ))"
}

activate_re395_runtime() {
    local run_dir=$1

    # Conda activation may inspect variables that are unset.  The calling
    # SLURM scripts deliberately defer nounset until activation has completed.
    # The updated activation helper is also safe if a caller already uses
    # nounset, so this remains a defence-in-depth boundary.
    source "$INSTALL/activate_shenfun.sh"
    set -u
    export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-1}"
    export OPENBLAS_NUM_THREADS=1
    export MKL_NUM_THREADS=1
    export NUMEXPR_NUM_THREADS=1
    export MPLBACKEND=Agg
    export MPLCONFIGDIR="$run_dir/mplconfig"
    export TMPDIR="$run_dir/tmp"
    mkdir -p "$MPLCONFIGDIR" "$TMPDIR"

    # MKM imports pyplot on every MPI rank even when plotting is disabled.
    # Populate the font cache once, before mpiexec, so a first high-rank job
    # cannot race on Matplotlib's shared cache lock.
    "$ENV/bin/python" -c \
        "import matplotlib.pyplot; print('matplotlib_cache_ready')"
}

verify_re395_inputs() {
    test -x "$ENV/bin/python"
    test -f "$RUNNER"
    test -f "$VALIDATOR"
    test -f "$STATE_AUDITOR"
    test -f "$SCHEDULE_VALIDATOR"
    test -f "$PROFILE"
    printf '%s  %s\n' "$PROFILE_SHA256" "$PROFILE" | sha256sum --check -
}

print_re395_provenance() {
    local run_dir=$1
    local git_head
    local mpi_ranks

    mpi_ranks=$(re395_mpi_ranks)

    printf 'timestamp_utc=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    printf 'job_id=%s\n' "${SLURM_JOB_ID:-not-in-slurm}"
    printf 'node_list=%s\n' "${SLURM_JOB_NODELIST:-not-in-slurm}"
    printf 'allocated_slurm_tasks=%s\n' "${SLURM_NTASKS:-$SLURM_TASKS_PER_MPI_RANK}"
    printf 'slurm_tasks_per_mpi_rank=%s\n' "$SLURM_TASKS_PER_MPI_RANK"
    printf 'mpi_ranks=%s\n' "$mpi_ranks"
    printf 'run_dir=%s\n' "$run_dir"
    printf 'repo=%s\n' "$REPO"
    printf 'runner=%s\n' "$RUNNER"
    printf 'spinup_final_time=%s\n' "$SPINUP_FINAL_TIME"
    printf 'sampling_window=%s,%s\n' "$SAMPLING_START_TIME" "$SAMPLING_FINAL_TIME"
    printf 'sampling_dt=%s\n' "$SAMPLING_DT"
    "$ENV/bin/python" -V
    "$ENV/bin/python" -c \
        "import h5py, numpy, scipy, shenfun; print('versions', shenfun.__version__, numpy.__version__, scipy.__version__, h5py.__version__, 'h5py_mpi='+str(h5py.get_config().mpi))"
    "$ENV/bin/python" -c \
        "from mpi4py import MPI; print(MPI.Get_library_version().splitlines()[0])"
    if command -v git >/dev/null 2>&1; then
        if git_head=$(cd "$REPO" && git rev-parse HEAD 2>/dev/null); then
            printf 'git_head=%s\n' "$git_head"
            (cd "$REPO" && git status --short 2>/dev/null) || true
        else
            printf 'git_provenance=unavailable reason=repository_not_readable\n'
        fi
    else
        printf 'git_provenance=unavailable reason=git_not_found\n'
    fi
}

run_re395_mpi() {
    local mpi_ranks

    mpi_ranks=$(re395_mpi_ranks)
    HYDRA_LAUNCHER=fork "$ENV/bin/mpiexec" -n "$mpi_ranks" "$@"
}
