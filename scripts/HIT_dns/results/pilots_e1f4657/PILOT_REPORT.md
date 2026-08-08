# HIT DNS pilot report

## Provenance and status

- Source commit: `e1f4657ebad808ad6c432f0560d835d59129fd00`
- Linux source worktree:
  `/media/jay/data1/shenfun_dns_runs/HIT_comte_bellot_1971/source-e1f4657`
- MPI runtime: 32 ranks for full-resolution and resolution pilots; one thread
  per rank.
- Status: pilot suite complete; production configuration locked.

Only lightweight CSV/JSON products are copied into this directory.  HDF5
fields and checkpoints remain under the Linux run root.

## Full-resolution initialization

The $384^3$ initialization/operator/output gate used `FFTW_ESTIMATE` and
finished in 14.68 s wall time.  `/usr/bin/time -v` reported a maximum resident
set of 1,485,164 KiB for the largest process and no swap activity.

| Quantity | Realized DNS | Table 4 / model | Relative difference |
|---|---:|---:|---:|
| Kinetic energy, cm2/s2 | 789.7263 | 775.3843 (continuous model) | +1.85% |
| Isotropic $u'$, cm/s | 22.9452 | 22.2 | +3.36% |
| Dissipation, cm2/s3 | 4348.345 | 4740 | -8.26% |
| Kolmogorov length, cm | 0.0295943 | 0.029 | +2.05% |
| $k_{max}\eta$ | 1.13642 | gate >= 1 | pass |
| CFL at $dt=10^{-4}$ s | 0.431244 | gate <= 0.5 | pass |

No realization rescaling or seed selection was applied.

At the resolved experimental wavenumbers, the station-42 shell/plane products
have median DNS-to-experiment ratios 0.99897 for $E$ and 1.06141 for
$E_{11}^{(1)}$.  Their relative L2 differences are 15.40% and 9.14%,
respectively.  The largest pointwise factor errors are 1.74 and 1.31; these
finite-shell realization fluctuations are retained without tuning.

## Full-resolution short evolution

Starting from the station-42 checkpoint, 11 RK4 steps reached station 42.2.
Full steps kept CFL in [0.4291, 0.4310], and $k_{max}\eta$ increased from
1.1364 to 1.1543.  The job finished in 129.62 s with diagnostics every step
and station HDF5 at both ends; this is a conservative cost sample because
production diagnostics are only every 100 steps.

## Timestep convergence

Two $128^3$ runs started from the identical station-42 HDF5 state and reached
station 50 ($t=0.04064$ s).  The candidate used $dt=10^{-4}$ s (407 steps),
and the reference used $dt=5\times10^{-5}$ s (813 steps).

| Difference at station 50 | Value |
|---|---:|
| Spectral velocity relative L2 | 1.3624e-7 |
| $E(k)$ relative L2 | 8.5985e-10 |
| $E_{11}^{(1)}(k_1)$ relative L2 | 8.0229e-10 |
| Kinetic-energy relative difference | 1.7084e-9 |
| Dissipation relative difference | 1.2613e-8 |

The provisional production timestep is therefore $10^{-4}$ s.  The
production CFL monitor remains authoritative and aborts above 0.5.

## Dissipative-tail sensitivity

The baseline Pao-type tail has fitted decay coefficient
$\beta=3.6114358042$ and is continuous with the measured $E(20)=0.8$.  Holding
that continuity while varying beta by +/-25% gives:

| Beta factor | Total energy, cm2/s2 | Tail energy fraction | Total dissipation, cm2/s3 | Tail dissipation fraction |
|---:|---:|---:|---:|---:|
| 0.75 | 776.2109 | 0.6388% | 4645.235 | 23.57% |
| 1.00 | 775.3843 | 0.5329% | 4371.529 | 18.78% |
| 1.25 | 774.8061 | 0.4586% | 4207.305 | 15.61% |

Thus the unmeasured tail contributes little total energy but materially affects
initial dissipation.  The fitted baseline is retained and this uncertainty is
reported rather than tuning beta to Table 4.

## Resolution pilot

The $256^3$ decay to station 98 used the same $dt=10^{-4}$ s and seed on 32
ranks.  It was intentionally below the production resolution gate at station
42 ($k_{max}\eta=0.7666$), crossed $k_{max}\eta=1$ during decay, and finished
with $k_{max}\eta=1.1508$.  The run took 1 h 46 min for 2845 steps, had no
swaps, and finished with CFL 0.1581.

At station 98 the reduced run gives $u'=13.499$ cm/s, dissipation 816.78
cm2/s3, $\eta=0.04495$ cm, $\lambda=0.7071$ cm, and $R_\lambda=63.89$.
Relative to experimental spectrum points, $E$ has 24.0% relative L2 error and
median DNS/experiment ratio 1.161; $E_{11}^{(1)}$ has 7.33% relative L2 error
and median ratio 1.259.  Its station-98 products will be compared over the
common wavenumber range with the $384^3$ production run.

## Locked production configuration

- Mesh/domain: $384^3$ in $[0,10\pi)^3$ cm.
- MPI/OpenMP: 32 ranks, one thread per rank, pencil decomposition.
- Nonlinearity/dealiasing: rotational form and 3/2 padding.
- Integrator/timestep: RK4 with nominal $dt=10^{-4}$ s and exact station
  landing.
- Monitoring: CFL <= 0.5, $k_{max}\eta\ge1$, diagnostics every 100 steps.
- Recovery: parallel checkpoint every 1000 steps plus station checkpoints.
- Seed/source: 421971 and commit `e1f4657ebad808ad6c432f0560d835d59129fd00`.
