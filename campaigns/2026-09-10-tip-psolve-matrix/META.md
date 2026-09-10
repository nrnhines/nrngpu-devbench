# Campaign: 2026-09-10 tip psolve matrix (planned)

| Field | Value |
|-------|--------|
| `campaign_id` | `2026-09-10-tip-psolve-matrix` |
| `date` | `2026-09-10` (planned; fill ISO time when run) |
| `status` | **harness ready — not run** |
| `machine` | hines-ThinkStation-P5 / NVIDIA T1000 8GB |
| `product_tree` | `~/neuron/nrngpu` |
| `branch` | `local/gpu-native` |
| `tip_sha` | `76ba78245513594c38bc02435f71cacc73c82b19` (`76ba78245`) — post-`origin/master` merge |
| `identity_policy` | `cpu_same_cell` |
| `wall_method` | 3× psolve after one model build; cell = `cold / warm_min–warm_max`. NEURON CPU/native: `runtime=` / `psolve=`. CN / CN GPU: CoreNEURON `Solver Time`. **Not** ctest process wall. |
| `hypothesis_id` | `H-dentate-1rank-cngpu` (measure 1-rank Dentate nt1 native vs CN GPU ~3× if it reproduces) |
| `4-rank dentate` | **Omitted** from this matrix (see below) |

## Identity policy (`cpu_same_cell`)

Last psolve ASCII raster vs the **CPU run of the same config on this tip**.

- Sorted `(t, gid)` exact match → ✅  
- Count recorded even on fail (`spikes:N`)  
- Golden is **not** L0 688 unless the row *is* that product config (these ring rows are `nring=16\|160`, not the 688 gate)  
- Traub 1/10: CPU vs native/CN still `cpu_same_cell`; if CPU count is 4474 / 7873 that is L0-aligned (note in SUMMARY, not a second golden)

Spike files: last psolve only (record vectors cleared before the last iteration). Written under `$PERF_MATRIX_OUT/spikes/<tag>/`.

## Rows (1 process)

| Config | Engines | Notes |
|--------|---------|-------|
| Ring16 nt1, Ring16 nt4 | CPU, CN, CN GPU, GPU (native) | nt4 GPU is **not** the exclusive-GPU comparison |
| Ring160 nt1, Ring160 nt4 | same | |
| Dentate nt1, nt4 (1-rank, max_cells=100, tstop=10) | same | Where ~3× CN GPU vs native appeared |
| Traub 1/10 no-gap, gap (nthread=1, tstop=100) | same | `traub_multi_bench.hoc`, not `traub_native` ctest |

## 4-rank dentate (MPI + MPS)

**Not in this campaign.** Different topology from 1-rank exclusive GPU. Putting it in the same table as Dentate nt1 is how 2026-08-10 mixed a ~1.2 s 4-rank native bar with a ~0.53 s 1-rank CN GPU cell. Follow-up campaign if we want all four engines at 4-rank; launcher would be `mpiexec`, not this harness.

## What this is not

- Not an overwrite of `2026-08-10-tip-l0-bars` or `archive/2026-08-05-matrix/`  
- Not L0 ctest smoke (688 / 400 / 4474 / 7873 stay product scripts; optional footnote using psolve printed in those logs)  
- Not density coding — wait for measured `H-dentate-1rank-cngpu`

## Run (when Do)

```bash
source ~/neuron/bin/nrnenv nrngpu build-gpu
export NRN_GPU_BACKEND_TEST=native NRN_GPU_PERMUTE=2 OMP_NUM_THREADS=1
export PERF_MATRIX_OUT=$HOME/neuron/devbench/campaigns/2026-09-10-tip-psolve-matrix/raw
# exclusive GPU for GPU cells; no MPS on 1-rank rows
bash ~/neuron/devbench/harness/run_matrix.sh
python3 ~/neuron/devbench/harness/parse_matrix.py "$PERF_MATRIX_OUT"
```

Copy `table.md` / identity into `SUMMARY.md` after the run. Rebuild Traub ACC special first (`run_traub_native.sh --rebuild` or equivalent); do not assume a stale `/tmp/traub-nrngpu-acc`.
