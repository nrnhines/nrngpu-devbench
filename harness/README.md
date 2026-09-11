# Matrix harness (psolve wall + last-psolve identity)

8 configs × 4 engines: throwaway `psolve(dt)` + 3 `stdinit`/`psolve(tstop)`. **Not ctest wall.**
Cell: **setup / solve_min–solve_max**. setup is interpreter wall of the throwaway (copyin/mk_mech + one step). solve is three full tstop psolves (NEURON: psolve wall; CN: `Solver Time`).

```bash
source ~/neuron/bin/nrnenv nrngpu build-gpu
export NRN_GPU_BACKEND_TEST=native NRN_GPU_PERMUTE=2 OMP_NUM_THREADS=1
export PERF_MATRIX_OUT=${PERF_MATRIX_OUT:-/tmp/perf-matrix}
bash ~/neuron/devbench/harness/run_matrix.sh
python3 ~/neuron/devbench/harness/parse_matrix.py "$PERF_MATRIX_OUT"
```

Requires product build via `nrnenv nrngpu build-gpu` and Traub model/special paths as in `run_matrix.sh`. Rebuild the Traub ACC special before a campaign (`test/external/traub/run_traub_native.sh --rebuild` or equivalent).

## Identity

Last psolve ASCII raster vs **CPU of the same config** (`cpu_same_cell`). Vectors are cleared before the last iteration so the file is not a 3× concat.

| Model | Dump | Where |
|-------|------|--------|
| Ring | `spikeout` → `spk<nhost>.std` | `$OUT/spikes/<tag>/` |
| Dentate | `spikeout` → `spikeout_<rank>.dat` | same |
| Traub | `spike2file` → `out<nhost>.dat` (cwd, then `mv`) | same |

`parse_matrix.py` writes `results.csv` (`identity`, `n_spikes`) and `table.md`. Exact sorted `(t, gid)`.

Ring `nring=16\|160` is **not** the L0 688 gate. Traub 1/10 counts may match 4474/7873; that is a note, not a second golden.

## 4-rank dentate

Not in this harness (1 process). See campaign `2026-09-10-tip-psolve-matrix/META.md`.

## Campaign

Latest: `../campaigns/2026-09-11-psolve-setup-warm/`. Prior: `../campaigns/2026-09-10-tip-psolve-matrix/`. Do not overwrite `archive/2026-08-05-matrix/` or `2026-08-10-tip-l0-bars`.
