# Campaign SUMMARY: 2026-08-06-tip-dentate

**Closed:** 2026-08-10 (plan **2.4.3** + **2.4.5**; **2.4.4** ring/Traub not run)  
**Tip:** `local/gpu-native` @ `0bdfca4b1` (`0bdfca4b1b046fae4cde2e503a10fae00844d3f4`)  
**Machine:** hines-ThinkStation-P5 / NVIDIA T1000 8GB  

For full L0 matrix layout see also **`../2026-08-10-tip-l0-bars/SUMMARY.md`**.

---

## Results

**Cell layout:** wall on first line; identity mark bottom-right.

| Mark | Meaning |
|------|---------|
| ✅ | Spike identity **pass** |
| ❌ | Spike identity **fail** |
| ➖ | Run completed; **identity not checked** |
| — | Not run |

| Config | CPU | CN | CN GPU | GPU (native) |
|--------|:----:|:--:|:------:|:------------:|
| **Dentate** product (4-rank MPS) | — | — | — | <div align="right">psolve&nbsp;1.133&nbsp;s<br>✅&nbsp;400</div> |
| **Dentate nt1** (1-rank ×3) | <div align="right">2.327&nbsp;/&nbsp;2.27–2.292<br>➖</div> | <div align="right">0.987&nbsp;/&nbsp;0.958–1.223<br>➖</div> | <div align="right">0.644&nbsp;/&nbsp;0.531–0.532<br>➖</div> | <div align="right">2.245&nbsp;/&nbsp;1.885–1.896<br>➖</div> |
| **Dentate nt4** (1-rank ×3) | <div align="right">0.905&nbsp;/&nbsp;0.875–0.892<br>➖</div> | <div align="right">1.042&nbsp;/&nbsp;1.06–1.071<br>➖</div> | <div align="right">1.048&nbsp;/&nbsp;0.956–0.963<br>➖</div> | <div align="right">3.547&nbsp;/&nbsp;3.004–3.134<br>➖</div> |

Product bar: sorted multiset **400** vs checked-in ref (`compare_results`). Spike files 106+97+101+96 = 400.  
Wall: `harness/dentate_multi_psolve.py` — cold / warm_min–warm_max. All eight 1-rank cells **OK** (no SEGV).

---

## Verdict

| Gate | Result |
|------|--------|
| Dentate **400** | ✅ GREEN |
| 1-rank wall probes | ➖ complete (no per-backend identity) |
| Ring / Traub | — skipped |

**Vs archive 2026-08-05:** timing-only + native **SEGV**; this tip product bar green.

Raw: `raw/ctest-*.log`, `raw/wall/`. Schema: `../../schema.md`.
