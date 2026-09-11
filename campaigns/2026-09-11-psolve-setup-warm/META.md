# Campaign: 2026-09-11 psolve setup + three warms

| Field | Value |
|-------|--------|
| `campaign_id` | `2026-09-11-psolve-setup-warm` |
| `date` | 2026-09-11 |
| `status` | **closed** — 32/32 launches; Traub gap native identity fail (7991 vs 7873) |
| `machine` | hines-ThinkStation-P5 / NVIDIA T1000 8GB |
| `product_tree` | `~/neuron/nrngpu` |
| `branch` | `local/gpu-native` |
| `tip_sha` | `75d218a3b` (persist GPU mirrors across psolve) |
| `identity_policy` | `cpu_same_cell` |
| `wall_method` | throwaway `psolve(dt)` then 3× `stdinit`+`psolve(tstop)`. Cell = `setup / solve_min–solve_max`. setup = interpreter wall of throwaway (copyin/mk_mech + one step). NEURON solve: `psolve=` / `runtime=`. CN solve: CoreNEURON `Solver Time` (last three). **Not** ctest process wall. |
| `hypothesis_id` | square CN `Solver Time` vs native first-process copyin; isolate setup from the three homogeneous solves |
| `4-rank dentate` | **Omitted** (same as 2026-09-10-tip-psolve-matrix) |

## Protocol

```text
stdinit()                    # model setup
psolve(dt)                   # throwaway / setup
for i in 1..3:
    stdinit()
    psolve(tstop)            # timed solves; last raster = identity
```

Same 8×4 rows as `2026-09-10-tip-psolve-matrix`. Exclusive GPU; no MPS.

## Run

```bash
source ~/neuron/bin/nrnenv nrngpu build-gpu
export NRN_GPU_BACKEND_TEST=native NRN_GPU_PERMUTE=2 OMP_NUM_THREADS=1
export PERF_MATRIX_OUT=$HOME/neuron/devbench/campaigns/2026-09-11-psolve-setup-warm/raw
bash ~/neuron/devbench/harness/run_matrix.sh
```
