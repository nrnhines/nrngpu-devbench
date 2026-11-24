# Campaign SUMMARY: 2026-11-24-tip-l0-bars

**Closed:** 2026-11-24  
**Kind:** L0 product-bar smoke on living tip (new campaign, fresh re-measure)  
**Tip:** `hines-grok/gpu-native` @ `f39717f74` (`f39717f745478885b0861364b3f7f1e20ac940a4`)  
**Machine:** hines-ThinkStation-P5 / NVIDIA T1000 8GB  
**Not:** reuse of `2026-08-10-tip-l0-bars`; not a timing matrix (`harness/run_matrix.sh` not run)

---

## Results

**Cell layout:** wall time on the first line(s); spike-raster identity mark **bottom-right** of the cell.

| Mark | Meaning |
|------|---------|
| ✅ | Spike identity **pass** (product golden / multiset / exact count) |
| ❌ | Spike identity **fail** |
| ➖ | Timing (or run) only — **identity not checked** for that backend |
| — | Not run this campaign |

**Wall format:** ring 1-rank is `runtime` seconds from prcell. Other GPU cells are ctest or psolve wall as noted.

| Config | CPU | CN | CN GPU | GPU (native) |
|--------|:----:|:--:|:------:|:------------:|
| **Ring @100** (1-rank) | <div align="right">0.388&nbsp;s<br>✅&nbsp;688</div> | — | — | <div align="right">0.851&nbsp;s<br>✅&nbsp;688</div> |
| **Ring @100** (2-rank MPI+MPS) | — | — | — | <div align="right">ctest&nbsp;1.67&nbsp;s<br>✅&nbsp;688</div> |
| **Dentate** product (4-rank MPS) | — | — | — | <div align="right">psolve&nbsp;0.936&nbsp;s<br>✅&nbsp;400</div> |
| **Traub no-gap** 1/10 | — | — | — | <div align="right">ctest&nbsp;79.5&nbsp;s<br>✅&nbsp;4474</div> |
| **Traub gap** 1/10 | — | — | — | <div align="right">ctest&nbsp;18.1&nbsp;s<br>✅&nbsp;7873</div> |

### Notes on cells

1. **Ring ✅ 688:** CPU and native GPU each wrote 688 spikes @ `tstop=100` (prcell path). 1-rank GPU `spk1.std` is 688 lines. 2-rank sorted `spk2.std` is 688 lines. prcellstate field diffs are noise-only (max \|d\| 9.95e-14; threshold dV = 0). `rdcellstate` exit 1 is not an identity fail.
2. **Dentate ✅ 400:** product `reduced_dentate_native` + `compare_results`. The four rank files total 400 lines and the sorted multiset matches the checked-in reference.
3. **Traub:** product ctest exact match vs checked-in refs (native↔CPU golden). No-gap ctest wall includes `Building Traub ACC special`. Gap ctest did not rebuild. CN columns not run.
4. Dentate nt1/nt4 and the rest of the timing matrix were not run.
5. Column order matches `2026-08-10-tip-l0-bars`: Config · CPU · CN · CN GPU · GPU (native).

---

## Verdict

| L0 bar | Result |
|--------|--------|
| Ring **688** | ✅ GREEN |
| Dentate **400** | ✅ GREEN |
| Traub **4474** / **7873** | ✅ GREEN |
| **Campaign** | **CLOSED GREEN** on tip `f39717f74` |

Raw logs: `raw/*.log`, `raw/results.txt`, `raw/ring_spk1_gpu.std`, `raw/ring_spk2_gpu.std`.

---

## Related

| Path | Role |
|------|------|
| `META.md` | Campaign metadata |
| `../2026-08-10-tip-l0-bars/` | Previous full L0 smoke @ `0bdfca4b1` |
| `../../l0/PRODUCT_BARS.md` | How to re-check without a campaign |
| `../IDENTITY.md` | Identity field design |

**Rendered on GitHub:** [SUMMARY.md](https://github.com/nrnhines/nrngpu-devbench/blob/main/campaigns/2026-11-24-tip-l0-bars/SUMMARY.md)
