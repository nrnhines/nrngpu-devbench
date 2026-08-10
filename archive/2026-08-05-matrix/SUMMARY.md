# Performance matrix

**Branch:** `local/gpu-native`  
**Commit:** `7ef35f6e2` (`7ef35f6e2420dcdfadcb5f3fc6b467232b6080d8`)  
**Measure date:** 2026-08-05T13:47:31-04:00  
**Machine:** NVIDIA T1000 8GB (dev GPU)

## Method

- One process per cell; **3 psolves** after one model build.
- Cell format: **`cold / warm_min–warm_max`** seconds  
  - cold = psolve #1  
  - warm = min–max of psolves #2 and #3  
- **NEURON** (CPU, native GPU): psolve wall (`runtime=` / `psolve=`).  
- **CoreNEURON** (CN CPU, CN GPU): `Solver Time`.  
- Ring: single ACC+CN special (`external_ringtest/neuron_gpu_native_mpi`).  
- Ring: 1 rank, `-nring 16|160`, `-nt 1|4`, `tstop=100`, **no gap**.  
- Dentate: 1 rank, max_cells=100, tstop=10, nthread 1|4.  
- Traub: ModelDB 82894 1/10, nthread=1, tstop=100, no-gap and gap.  
- Harnesses (canonical now): `~/neuron/devbench/harness/` (this dir is legacy; see `README.md`)  
- Raw logs + CSV: `~/neuron/notes/perf_matrix/results/` and `/tmp/perf-matrix/`

## Results (seconds)

| Config | CPU | GPU (native) | CN CPU | CN GPU |
|--------|-----|--------------|--------|--------|
| Ring16 nt1 | 0.483 / 0.483–0.483 | 1.231 / 0.752–0.946 | 0.410 / 0.425–0.428 | 1.501 / 1.320–1.344 |
| Ring16 nt4 | 0.134 / 0.129–0.129 | 3.489 / 3.114–3.147 | 0.537 / 0.554–0.556 | 4.706 / 4.550–4.577 |
| Ring160 nt1 | 3.653 / 3.667–3.673 | 2.264 / 1.852–1.856 | 3.915 / 3.917–3.948 | 2.634 / 2.535–2.538 |
| Ring160 nt4 | 1.199 / 0.969–1.162 | 4.542 / 4.020–4.048 | 3.834 / 3.860–4.155 | 6.274 / 6.184–6.186 |
| Dentate nt1 | 2.254 / 2.242–2.282 | **ERR** (SEGV) | 0.972 / 0.969–0.974 | 0.830 / 0.800–0.808 |
| Dentate nt4 | 1.016 / 0.869–0.908 | **ERR** (SEGV) | 1.041 / 1.028–1.030 | 1.032 / 0.937–0.946 |
| Traub no-gap | 35.00 / 34.15–34.23 | 17.90 / 15.85–15.86 | 28.32 / 28.06–28.14 | 8.578 / 8.448–8.602 |
| Traub gap | 36.71 / 36.36–36.47 | 19.67 / 18.79–19.11 | 27.82 / 27.96–28.01 | 9.599 / 9.527–9.551 |

## Notes

1. **Small ring (n=16, nt=1):** NEURON CPU and CN CPU beat GPU on this T1000 — problem is too small for device overhead.  
2. **Larger ring (n=160, nt=1):** native GPU warm **1.85 s** ≲ CN GPU **2.54 s** ≲ CPU **3.67 s**.  
3. **nt=4 + GPU** is often *slower* (host threads thrashing one GPU); prefer nt=1 for exclusive GPU.  
4. **Traub no-gap warm:** native **~15.9 s** vs CN GPU **~8.5 s** (~**1.9×**). Portfolio tip multi-warm was ~11.3 vs ~10 (~1.13×) — this run is slower; re-check special freshness / exclusivity if comparing to portfolio.  
5. **Dentate native GPU:** product path **SEGV** at first psolve on this tip/special today (same with `run_dentate_native.py`). CPU/CN columns OK.  
6. Extend later: append rows (e.g. ring gap) using the same CSV schema in `results/results.csv`.

## Re-run

```bash
bash ~/neuron/devbench/harness/run_matrix.sh
# Dentate needs HOC_LIBRARY_PATH=templates (in run_matrix.sh)
python3 ~/neuron/devbench/harness/parse_matrix.py /tmp/perf-matrix
# Do not overwrite this SUMMARY in place — archive first (plan 2.4.1)
```
