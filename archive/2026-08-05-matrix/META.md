# Archive: 2026-08-05 performance matrix

**Frozen:** 2026-08-06 (plan step **2.4.1**)  
**Source (do not overwrite in place):** `~/neuron/notes/perf_matrix/SUMMARY.md` + `results/`  
**Canonical copy:** this directory under `~/neuron/devbench`

## Provenance

| Field | Value |
|-------|--------|
| Measure date | 2026-08-05T13:47:31-04:00 |
| Product branch | `local/gpu-native` |
| Product tip (short) | `7ef35f6e2` |
| Product tip (full, from SUMMARY) | `7ef35f6e2420dcdfadcb5f3fc6b467232b6080d8` |
| Machine | NVIDIA T1000 8GB (dev GPU) |
| Kind | **Timing-only** (no spike identity ✓/✗ in cells) |
| Dentate native GPU | **ERR** (SEGV) on that tip — product SEGV later closed; see portfolio / L0 |

## Contents

| Path | Role |
|------|------|
| `SUMMARY.md` | Human method + timing table |
| `results/stamp.txt` | branch / commit / date |
| `results/results.csv`, `table.md` | Parsed matrix |
| `results/*.log` | Per-cell raw logs |

## Policy

- **Read-only freeze.** New campaigns go under `campaigns/`, not here.  
- Hypothesis: `H-matrix-2026-08-05` in `hypotheses/LEDGER.md`.
