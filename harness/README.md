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

## Traub CN −6 (prcellstate)

Not the 3-warm matrix. CoreNEURON Traub **gap** is **7867** vs CPU/native **7873**. Campaign rasters: CN matches CPU through **t=99.95**; CPU has six extra spikes at **t=99.975**, gids **47 51 153 266 276 347**. No-gap is exact 4474 (includes t=99.975). This is a CoreNEURON identity investigation, not a native-GPU recode.

Spikes first (no GPU):

```bash
python3 ~/neuron/devbench/harness/diff_rasters.py \
  ~/neuron/devbench/campaigns/2026-09-11-psolve-setup-warm/raw/spikes/traub_gap_cpu \
  ~/neuron/devbench/campaigns/2026-09-11-psolve-setup-warm/raw/spikes/traub_gap_cn_gpu
```

Then cell dumps (single `stdinit`+`psolve`; default gid 47). NEURON writes `<gid>_nrnCCC_tT.nrndat` after stdinit and after psolve. CN `--prcellgid` writes `<gid>_cpu_init.corenrn` / `<gid>_acc_gpu_t….corenrn` at CN init and tstop.

```bash
source ~/neuron/bin/nrnenv nrngpu build-gpu
export TRAUB_PRCS_OUT=/tmp/traub-prcs
bash ~/neuron/devbench/harness/traub_prcs.sh --gid 47 --tstop 100 --engines cpu,cn_cpu,cn_gpu
# last-dt hypothesis: tstop=99.95 should match 7867 on both
bash ~/neuron/devbench/harness/traub_prcs.sh --gid 47 --tstop 99.95 --engines cpu,cn_gpu --out /tmp/traub-prcs-99.95
cd "$TRAUB_PRCS_OUT"
# CN-internal dump is *.corenrn. The NEURON *.nrndat after a CN psolve is
# datareturn (incomplete RANGE) — not CN cell truth. t=0 NEURON dumps should match.
python -m neuron.debug.rdcellstate cpu/47_nrn000_t100.nrndat cn_gpu/47_acc_gpu_t1*.corenrn --ignore-unused --top 25
```

`--checkpoint-t T` arms native/CPU phase dumps (`pc.prcellstate_checkpoint`). CN has no phase checkpoints.

`--steps-per-ms N` sets `dt = 1/N` after `manage_setup` (`prcs_steps_per_ms`; the built-in `steps_per_ms` is reset from `dt` during setup). `N=64` (binary-exact dt) makes Traub gap CPU↔CN match at tstop=50, including the last-step-start spike; product `N=40` (dt=0.025) misses that step on CN.
