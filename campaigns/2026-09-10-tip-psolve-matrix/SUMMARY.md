# Campaign SUMMARY: 2026-09-10-tip-psolve-matrix

**Status:** planned / harness ready — **not run**  
**Tip (intended):** `local/gpu-native` @ `76ba78245`  
**Identity:** last-psolve raster vs CPU of the same cell (`cpu_same_cell`)  
**Wall:** 3× psolve; not ctest

Fill this table after `run_matrix.sh`. Column order: CPU · CN · CN GPU · GPU (native).  
4-rank dentate is **omitted** (see `META.md`).

| Config | CPU | CN | CN GPU | GPU (native) |
|--------|:----:|:--:|:------:|:------------:|
| Ring16 nt1 | — | — | — | — |
| Ring16 nt4 | — | — | — | — |
| Ring160 nt1 | — | — | — | — |
| Ring160 nt4 | — | — | — | — |
| Dentate nt1 (1-rank ×3) | — | — | — | — |
| Dentate nt4 (1-rank ×3) | — | — | — | — |
| Traub no-gap 1/10 | — | — | — | — |
| Traub gap 1/10 | — | — | — | — |

Related: `META.md`, `../../harness/README.md`, `../IDENTITY.md`.
