# Campaign SUMMARY: 2026-09-10-tip-psolve-matrix

**Closed:** 2026-09-10T18:28:07-04:00  
**Kind:** 8×4 psolve matrix (identity `cpu_same_cell`; not ctest wall)  
**Tip:** `local/gpu-native` @ `76ba78245` (`76ba78245513594c38bc02435f71cacc73c82b19`)  
**Machine:** hines-ThinkStation-P5 / NVIDIA T1000 8GB  
**Launches:** 32/32 OK  
**4-rank dentate:** omitted (see `META.md`)

Stamp: `branch=local/gpu-native commit=76ba78245 date=2026-09-10T18:15:59-04:00`

Build note: `ninja install` failed on RxD `ctng.cpp` (Cython / NumPy `PyDataType_*` vs `NPY_NO_DEPRECATED_API` on Python 3.14). nrniv was linked; `cmake --install` used for the prefix. Unused by this matrix.

---

## Results

**Wall:** `cold / warm_min–warm_max` seconds (3 psolves). NEURON: psolve/runtime. CN: Solver Time.

**Identity:** last-psolve raster vs CPU of the same config (exact sorted t,gid).

| Mark | Meaning |
|------|---------|
| ✅ | Spike identity **pass** |
| ❌ | Spike identity **fail** |
| — | Not run |

| Config | CPU | CN | CN GPU | GPU (native) |
|--------|:----:|:--:|:------:|:------------:|
| **Ring16 nt1** | <div align="right">0.356 / 0.358–0.359<br>✅ 688</div> | <div align="right">0.527 / 0.541–0.541<br>✅ 688</div> | <div align="right">1.38 / 1.271–1.273<br>✅ 688</div> | <div align="right">1.019 / 0.716–0.717<br>✅ 688</div> |
| **Ring16 nt4** | <div align="right">0.139 / 0.129–0.129<br>✅ 688</div> | <div align="right">0.408 / 0.426–0.428<br>✅ 688</div> | <div align="right">4.588 / 4.492–4.496<br>✅ 688</div> | <div align="right">3.216 / 2.916–2.997<br>✅ 688</div> |
| **Ring160 nt1** | <div align="right">3.627 / 3.616–3.628<br>✅ 6880</div> | <div align="right">3.907 / 3.906–3.914<br>✅ 6880</div> | <div align="right">2.641 / 2.536–2.552<br>✅ 6880</div> | <div align="right">2.334 / 1.806–1.815<br>✅ 6880</div> |
| **Ring160 nt4** | <div align="right">1.173 / 0.923–0.960<br>✅ 6880</div> | <div align="right">3.77 / 3.811–4.304<br>✅ 6880</div> | <div align="right">6.235 / 6.145–6.147<br>✅ 6880</div> | <div align="right">4.515 / 3.999–4.004<br>✅ 6880</div> |
| **Dentate nt1** (1-rank ×3) | <div align="right">2.209 / 2.180–2.186<br>✅ 400</div> | <div align="right">0.937 / 0.941–0.942<br>✅ 400</div> | <div align="right">0.627 / 0.529–0.532<br>✅ 400</div> | <div align="right">2.053 / 1.796–1.809<br>✅ 400</div> |
| **Dentate nt4** (1-rank ×3) | <div align="right">0.878 / 0.824–0.858<br>✅ 400</div> | <div align="right">1.021 / 1.005–1.010<br>✅ 400</div> | <div align="right">1.048 / 0.935–0.939<br>✅ 400</div> | <div align="right">3.262 / 2.989–3.041<br>✅ 400</div> |
| **Traub no-gap** 1/10 | <div align="right">33.34 / 33.06–33.42<br>✅ 4474</div> | <div align="right">27.48 / 26.80–27.47<br>✅ 4474</div> | <div align="right">8.523 / 8.429–8.469<br>✅ 4474</div> | <div align="right">11.06 / 10.17–10.17<br>✅ 4474</div> |
| **Traub gap** 1/10 | <div align="right">35.34 / 35.55–36.03<br>✅ 7873</div> | <div align="right">28.28 / 27.92–28.34<br>❌ 7867</div> | <div align="right">9.586 / 9.541–9.591<br>❌ 7867</div> | <div align="right">12.41 / 11.30–11.36<br>✅ 7873</div> |

---

## Notes

1. **Ring16** is the L0 688 gate (`nring=16`, tstop=100). Ring160 is 10× rings → 6880.
2. **Dentate nt1** (exclusive GPU): CN GPU warm **~0.53 s** vs native **~1.80 s** ≈ **3.4×**. Identity ✅ 400 all engines. This is `H-dentate-1rank-cngpu` **measured**. Do not compare this cell to 4-rank MPS product (~1.2 s).
3. **nt=4 GPU** is slower than nt1 on this T1000 (host threads vs one GPU). Not the exclusive-GPU ratio.
4. **Traub no-gap** native warm **~10.17 s** vs CN GPU **~8.43 s** ≈ **1.21×**. All four engines ✅ 4474 vs CPU.
5. **Traub gap** native ✅ 7873 vs CPU; CN / CN GPU ❌ **7867** (known CoreNEURON −6). Native warm **~11.3 s** vs CN GPU **~9.55 s** ≈ **1.18×**.
6. First parse mixed leftover `out1_enable_gpu=*.dat` into Traub no-gap CPU (false 4700). Loader now accepts only `out<digits>.dat` / `spk*.std` / `spikeout_*.dat`. Re-parse; no re-run.

Raw: `raw/*.log`, `raw/spikes/<tag>/`, `raw/results.csv`, `raw/table.md`. META: `META.md`.
