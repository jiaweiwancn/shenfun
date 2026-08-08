# Decaying homogeneous-isotropic-turbulence DNS

This directory reproduces the Comte-Bellot--Corrsin 5.08 cm-grid decay from
the station $tU_0/M=42$ to stations 98 and 171.  The simulation uses cm and s,
so the tabulated spectra can be compared without unit conversion.

The approved scientific and execution plan is in
[`RUN_PLAN_HIT_DNS.md`](RUN_PLAN_HIT_DNS.md).  The original method and
experimental context remain in `docs/`; machine-readable transcriptions of
Tables 2--4 are in `data/`.

## Model

- $M=5.08$ cm, $U_0=1000$ cm/s, and
  $\nu=U_0M/34000=0.1494117647$ cm2/s.
- A $[0,10\pi)^3$ cm periodic cube on a $384^3$ Fourier mesh gives
  $\Delta k=0.2$ cm-1 and nominal $k_{max}=38.4$ cm-1.
- Nonlinear products use 3/2 padding, the rotational form
  $\boldsymbol{u}\times\boldsymbol{\omega}$, and a Leray projection.
- Time integration is classical RK4.  Pilot runs choose the fixed nominal
  timestep; shortened last steps land exactly on requested stations.
- The station-42 Table 3 spectrum is interpolated positively in log space,
  completed by $k^4$ below 0.2 cm-1, and by a fitted Pao-type tail above
  20 cm-1.
- The initial Gaussian field uses the Mann isotropic factorization.  Its
  stateless physical-space random stream is a pure function of global index,
  component, and seed, so it is invariant to MPI decomposition.  No seed
  selection or realization rescaling is performed.

## Files

- `reference_data.py`: constants, station/time map, and Tables 2--4 loaders.
- `spectrum_model.py`: continuous initial $E(k)$ and isotropic $E_{11}^{(1)}$.
- `deterministic_random.py`: rank-independent Gaussian stream.
- `mann_initializer.py`: spectral factorization and velocity initialization.
- `solver_backend.py`: explicit spectralDNS NS/RK4 setup and station landing.
- `hit_diagnostics.py`: invariants, CFL, bulk statistics, $E$, and $E_{11}$.
- `hit_io.py`: MPI HDF5 checkpoint/restart and lightweight CSV/JSON products.
- `run_hit_dns.py`: production and pilot command-line driver.
- `mpi_initial_condition_check.py`: small MPI initializer/operator gate.

## Linux environment

The audited server environment is
`/home/jay/anaconda3/envs/spectralDNS` and contains MPI-enabled h5py.  Keep one
thread per rank unless a later pilot explicitly justifies another setting:

```bash
export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
```

Run unit tests from this directory with:

```bash
/home/jay/anaconda3/envs/spectralDNS/bin/python -m pytest -q tests
```

Run the small MPI gate with:

```bash
/home/jay/anaconda3/envs/spectralDNS/bin/mpiexec -n 4 \
  /home/jay/anaconda3/envs/spectralDNS/bin/python \
  mpi_initial_condition_check.py --n 32 --steps 1 \
  --planner-effort FFTW_ESTIMATE
```

## Production command template

Do not use the placeholder timestep below until the pilot stage has locked it.
The production process runs only in an isolated Linux execution tree whose
source commit is recorded with `--git-commit`.

```bash
/home/jay/anaconda3/envs/spectralDNS/bin/mpiexec -n 32 \
  /home/jay/anaconda3/envs/spectralDNS/bin/python run_hit_dns.py \
  --n 384 --length-cm 31.41592653589793 \
  --viscosity-cm2-s 0.14941176470588236 \
  --dt-s PILOT_SELECTED_DT --stations 42,98,171 \
  --seed 421971 --decomposition pencil --threads 1 \
  --maximum-cfl 0.5 --minimum-kmax-eta 1.0 \
  --diagnostics-every 100 --checkpoint-every 1000 \
  --raw-dir /media/jay/data1/shenfun_dns_runs/HIT_comte_bellot_1971/production/raw \
  --light-dir /media/jay/data1/shenfun_dns_runs/HIT_comte_bellot_1971/production/light \
  --git-commit COMMITTED_SOURCE_HASH
```

Restart uses the same numerical parameters plus a checkpoint:

```bash
... run_hit_dns.py ... \
  --restart /path/to/checkpoint_step_00001000.h5
```

Fresh runs refuse to write where station HDF5 or station lightweight products
already exist.  A restart may write only into a deliberately selected output
directory.

## Output and gates

Raw spectral checkpoints (`*.h5`) are server-only.  Each station also produces
small `E.csv`, `E11.csv`, and `summary.json` files plus `diagnostics.csv`; only
these lightweight products are copied back to macOS.

Every diagnostic checks finite values, relative spectral divergence below
$10^{-12}$, Parseval closure below $10^{-10}$, CFL at most 0.5, and
$k_{max}\eta\ge1$ for production.  Station summaries also record package
versions, command, MPI size, host, Git commit, initialization parameters, and
both spectrum-integral closures.  The MPI gate additionally requires the
semi-discrete nonlinear energy residual below $10^{-12}$.
