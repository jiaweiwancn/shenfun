# MKM Channel Resolvent Production Reports

This directory indexes lightweight artifacts fetched from selected-mode
channel-resolvent production runs. Large production HDF5 files remain on the
Linux server under `/media/jay/data1/...` and are not stored here.

## Reports

1. [Sparse target-CSD selected-mode run](target_csd_selected_modes/)
   - Source: accepted target `modal/u_hat`
   - Modes: `(1,0)`, `(1,1)`, `(2,1)`
   - Includes manifest JSON, Markdown workflow report, and generated PDFs.

2. [Dense temporal-CSD selected-mode run](dense_csd_selected_modes/)
   - Source: selected modes computed from dense raw velocity snapshots
   - Modes: `(1,0)`, `(1,1)`, `(2,1)`
   - Includes manifest JSON, Markdown workflow report, and generated PDFs.

3. [Sparse-vs-dense scientific comparison](channel_resolvent_selected_modes_comparison.md)
   - Compares omega bins, leading resolvent gains, projection fractions,
     diagnostics, limitations, and next scientific steps.

## Notes

These are selected-mode proof-of-concept products, not exhaustive mode sweeps.
They demonstrate the McKeon-style channel resolvent workflow on the MKM
production target and dense temporal continuation, but do not by themselves
support high-Reynolds-number or long-box VLSM scaling claims.
