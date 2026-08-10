# Devbench

**Path:** `~/neuron/devbench` (own git; not inside product trees)  
**Remote:** [nrnhines/nrngpu-devbench](https://github.com/nrnhines/nrngpu-devbench) (public; `origin`)  
**Kind:** platform — evidence and process around NEURON product work  
**Product context:** often `~/neuron/nrngpu` @ `local/gpu-native` (does not live here)

## Purpose (one sentence)

Keep product **“still green?”** checks, measured **campaigns**, and wall-time **hypotheses** honest and reusable — so progress does not live only in chat or one-off log folders.

## Layers

| Layer | What | Where |
|-------|------|--------|
| **L0** | Product bars (identity gates on tip) | Checklist in `l0/` — harnesses stay in **product** trees / ctest |
| **L1 / L2** | Campaigns (dated matrices) | `campaigns/` — **identity first**, wall time second; see `schema.md` |
| **Ledger** | Perf / residual claims | `hypotheses/` |
| **Harness** | Sidecar scripts (timing matrix, etc.) | `harness/` — points at product builds; not a second simulator |
| **Archive** | Frozen past runs | `archive/` — never overwrite in place |

## What this is not

- Not a replacement for `~/neuron/notes/PORTFOLIO.md` or per-tree `GROK-*.md`.  
- Not a place to land density / OpenACC product patches (those stay in `nrngpu`).  
- Not “run the full matrix every session” — campaigns are deliberate **Do** steps.

## Layout

```text
devbench/
  README.md           # this file
  schema.md           # campaign cell fields
  l0/PRODUCT_BARS.md  # how to re-check product gates
  hypotheses/LEDGER.md
  harness/            # matrix scripts (from notes/perf_matrix)
  campaigns/          # dated campaign results (git or gitignored logs)
  archive/            # frozen historical matrices
```

## Related notes (outside this repo)

| Path | Role |
|------|------|
| `~/neuron/notes/devbench.md` | Purpose bridge (may lag README) |
| `~/neuron/notes/SHARED-WORLD.md` | Where things live under `~/neuron` |
| `~/neuron/notes/plans/devbench-thin-plan.md` | Ordered steps + commit points |
| `~/neuron/notes/PORTFOLIO.md` | Active work map |

## Quick start (after product build)

```bash
# L0: product ctests — see l0/PRODUCT_BARS.md (run from nrngpu build tree)

# Timing matrix harness (identity not yet in cells — campaign work is plan 2.4+):
bash ~/neuron/devbench/harness/run_matrix.sh
python3 ~/neuron/devbench/harness/parse_matrix.py /tmp/perf-matrix
```

Large logs: write under `/tmp` or dated dirs; prefer gitignore over bloating history.
