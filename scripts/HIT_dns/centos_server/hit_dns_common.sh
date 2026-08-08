#!/bin/bash
# Shared, source-only configuration for CentOS/SLURM HIT jobs.

INSTALL=/share/home/dkyzdsys_wanjiawei/shenfun_offline_centos_install
ENV="$INSTALL/env"
REPO=/share/home/dkyzdsys_wanjiawei/shenfun-master
HIT_DIR="$REPO/scripts/HIT_dns"
RUN_ROOT=/share/home/dkyzdsys_wanjiawei/shenfun_runs/hit_dns
LOG_ROOT=/share/home/dkyzdsys_wanjiawei/shenfun_runs/logs

RUNNER="$HIT_DIR/run_hit_dns.py"
MPI_CHECK="$HIT_DIR/mpi_initial_condition_check.py"
CHECKPOINT_INSPECTOR="$HIT_DIR/centos_server/inspect_hit_checkpoints.py"
RUNTIME_MANIFEST="$HIT_DIR/centos_server/RUNTIME_SHA256SUMS"

# Match the allocation policy already validated on this cluster: reserve two
# SLURM tasks for each launched MPI rank and launch only one process per pair.
SLURM_TASKS_PER_MPI_RANK=2

hit_mpi_ranks() {
    local allocated_tasks="${SLURM_NTASKS:-$SLURM_TASKS_PER_MPI_RANK}"

    if [[ ! "$allocated_tasks" =~ ^[0-9]+$ ]] || (( allocated_tasks <= 0 )); then
        echo "SLURM_NTASKS must be a positive integer; got '$allocated_tasks'" >&2
        return 2
    fi
    if (( allocated_tasks % SLURM_TASKS_PER_MPI_RANK != 0 )); then
        echo "SLURM_NTASKS=$allocated_tasks is not divisible by $SLURM_TASKS_PER_MPI_RANK" >&2
        return 2
    fi
    printf '%s\n' "$(( allocated_tasks / SLURM_TASKS_PER_MPI_RANK ))"
}

activate_hit_runtime() {
    local run_dir=$1

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
}

verify_hit_inputs() {
    test -x "$ENV/bin/python"
    test -x "$ENV/bin/mpiexec"
    test -f "$RUNNER"
    test -f "$MPI_CHECK"
    test -f "$CHECKPOINT_INSPECTOR"
    test -f "$RUNTIME_MANIFEST"
    (
        cd "$REPO"
        sha256sum --check "$RUNTIME_MANIFEST"
    )
    "$ENV/bin/python" -c \
        "import h5py, mpi4py_fft, numpy, scipy, shenfun; assert shenfun.__version__ == '4.3.0'; assert h5py.get_config().mpi; print('centos_runtime_check=PASS', shenfun.__version__, numpy.__version__, scipy.__version__, mpi4py_fft.__version__, h5py.__version__)"
}

hit_git_head() {
    local git_head

    if command -v git >/dev/null 2>&1 && git_head=$(cd "$REPO" && git rev-parse HEAD 2>/dev/null); then
        printf '%s\n' "$git_head"
    else
        printf '%s\n' unavailable
    fi
}

print_hit_provenance() {
    local run_dir=$1

    printf 'timestamp_utc=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    printf 'job_id=%s\n' "${SLURM_JOB_ID:-not-in-slurm}"
    printf 'node_list=%s\n' "${SLURM_JOB_NODELIST:-not-in-slurm}"
    printf 'allocated_slurm_tasks=%s\n' "${SLURM_NTASKS:-$SLURM_TASKS_PER_MPI_RANK}"
    printf 'slurm_tasks_per_mpi_rank=%s\n' "$SLURM_TASKS_PER_MPI_RANK"
    printf 'mpi_ranks=%s\n' "$(hit_mpi_ranks)"
    printf 'run_dir=%s\n' "$run_dir"
    printf 'repo=%s\n' "$REPO"
    printf 'runner=%s\n' "$RUNNER"
    printf 'git_head=%s\n' "$(hit_git_head)"
    "$ENV/bin/python" -V
    "$ENV/bin/python" -c \
        "from mpi4py import MPI; print(MPI.Get_library_version().splitlines()[0])"
}

run_hit_mpi() {
    local mpi_ranks

    mpi_ranks=$(hit_mpi_ranks)
    HYDRA_LAUNCHER=fork "$ENV/bin/mpiexec" -n "$mpi_ranks" "$@"
}
