# Campaign SUMMARY: 2026-08-10-tip-l0-bars

**Closed:** 2026-08-10  
**Kind:** L0 product-bar smoke on living tip (option **B** — new campaign, fresh re-measure)  
**Tip:** `local/gpu-native` @ `0bdfca4b1` (`0bdfca4b1b046fae4cde2e503a10fae00844d3f4`)  
**Machine:** hines-ThinkStation-P5 / NVIDIA T1000 8GB  
**Not:** reuse of archive 2026-08-05 timing cells; not an append to `2026-08-06-tip-dentate`

---

## Results

**Cell layout:** wall time on the first line(s); spike-raster identity mark **bottom-right** of the cell.

| Mark | Meaning |
|------|---------|
| ✅ | Spike identity **pass** (product golden / multiset / exact count) |
| ❌ | Spike identity **fail** |
| ➖ | Timing (or run) only — **identity not checked** for that backend |
| — | Not run this campaign |

**Wall format (where multi-psolve):** `cold / warm_min–warm_max` seconds (same as archive matrix).  
**NEURON** CPU / GPU (native): psolve / runtime wall. **CN** / **CN GPU:** Solver Time or ctest wall as noted.

| Config | CPU | CN | CN GPU | GPU (native) |
|--------|:----:|:--:|:------:|:------------:|
| **Ring @100** (1-rank) | <div align="right">0.391&nbsp;s<br>✅&nbsp;688</div> | — | — | <div align="right">0.880&nbsp;s<br>✅&nbsp;688</div> |
| **Ring @100** (2-rank MPI+MPS) | — | — | — | <div align="right">ctest&nbsp;1.73&nbsp;s<br>✅</div> |
| **Dentate** product (4-rank MPS) | — | — | — | <div align="right">psolve&nbsp;1.216&nbsp;s<br>✅&nbsp;400</div> |
| **Dentate nt1** (1-rank ×3) | <div align="right">2.327&nbsp;/&nbsp;2.27–2.292<br>➖</div> | <div align="right">0.987&nbsp;/&nbsp;0.958–1.223<br>➖</div> | <div align="right">0.644&nbsp;/&nbsp;0.531–0.532<br>➖</div> | <div align="right">2.245&nbsp;/&nbsp;1.885–1.896<br>➖</div> |
| **Dentate nt4** (1-rank ×3) | <div align="right">0.905&nbsp;/&nbsp;0.875–0.892<br>➖</div> | <div align="right">1.042&nbsp;/&nbsp;1.06–1.071<br>➖</div> | <div align="right">1.048&nbsp;/&nbsp;0.956–0.963<br>➖</div> | <div align="right">3.547&nbsp;/&nbsp;3.004–3.134<br>➖</div> |
| **Traub no-gap** 1/10 | — | — | — | <div align="right">ctest&nbsp;61.5&nbsp;s<br>✅&nbsp;4474</div> |
| **Traub gap** 1/10 | — | — | — | <div align="right">ctest&nbsp;16.8&nbsp;s<br>✅&nbsp;7873</div> |

### Notes on cells

1. **Ring ✅ 688:** both CPU and native GPU wrote 688 spikes @ `tstop=100` (prcell path + 1-rank GPU `spk2.std`). prcellstate field diffs are noise-only (max \|d\| ~1e-13); `rdcellstate` exit 1 is not treated as identity fail.  
2. **Dentate ✅ 400:** product `reduced_dentate_native` + `compare_results` only (4-rank).  
3. **Dentate nt1/nt4 wall rows:** same tip (`0bdfca4b1`), from campaign `2026-08-06-tip-dentate` multi-psolve harness — **run OK**, spike multiset **not** checked per backend → ➖. Contrast archive 2026-08-05 native GPU **ERR** (SEGV).  
4. **Traub:** product ctest exact match vs checked-in refs (native↔CPU golden). CN columns not re-run this campaign.  
5. Column order matches archive intent with **GPU (native)** last: Config · CPU · CN · CN GPU · GPU (native).

---

## Verdict

| L0 bar | Result |
|--------|--------|
| Ring **688** | ✅ GREEN |
| Dentate **400** | ✅ GREEN |
| Traub **4474** / **7873** | ✅ GREEN |
| **Campaign** | **CLOSED GREEN** on tip `0bdfca4b1` |

Raw logs: `raw/*.log`, `raw/results.txt`, `raw/ring_spk2_gpu.std`. Dentate wall logs: `../2026-08-06-tip-dentate/raw/wall/`.

---

## Related

| Path | Role |
|------|------|
| `META.md` | Campaign metadata |
| `../2026-08-06-tip-dentate/` | Dentate wall probes (same tip) |
| `../../archive/2026-08-05-matrix/` | Timing-only freeze (no identity marks) |
| `../../l0/PRODUCT_BARS.md` | How to re-check without a campaign |
| `../IDENTITY.md` | Identity field design |

**Rendered on GitHub:** [SUMMARY.md](https://github.com/nrnhines/nrngpu-devbench/blob/main/campaigns/2026-08-10-tip-l0-bars/SUMMARY.md)
