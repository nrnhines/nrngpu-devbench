# Campaign SUMMARY: 2026-09-11-native-cngpu-ratio

**Closed:** 2026-09-11T15:57:20-04:00  
**Kind:** 8×4 psolve matrix with throwaway `psolve(dt)` then 3 warms (identity `cpu_same_cell`; not ctest wall)  
**Tip:** `local/gpu-native` @ `0cebf94ff` (persist mirrors; Traub gap persist + CN integer n; Dentate nt1 exclusive recode closed)  
**Machine:** hines-ThinkStation-P5 / NVIDIA T1000 8GB  
**Launches:** 32/32 OK  
**4-rank dentate:** omitted

Stamp: `branch=local/gpu-native commit=0cebf94ff date=2026-09-11T15:43:38-04:00`

---

## Results

**Wall:** `setup / solve_min–solve_max` seconds.  
**setup** = interpreter wall of throwaway `psolve(dt)` (first-process copyin/mk_mech + one step).  
**solve** = three full-tstop psolves after `stdinit`. NEURON: `psolve=` / `runtime=`. CN: CoreNEURON `Solver Time` (last three).  
**native/CN GPU** = min(native solves) / min(CN GPU Solver Time). Native faster is `< 1`.

**Identity:** last-psolve raster vs CPU of the same config (exact sorted t,gid).

| Mark | Meaning |
|------|---------|
| ✅ | Spike identity **pass** |
| ❌ | Spike identity **fail** |

| Config | CPU | CN | CN GPU | GPU (native) | native/CN GPU |
|--------|:----:|:--:|:------:|:------------:|:-------------:|
| **Ring16 nt1** | 0.0002 / 0.484–0.487<br>✅ 688 | 0.138 / 0.551–0.555<br>✅ 688 | 0.216 / 1.555–1.615<br>✅ 688 | 0.308 / 0.961–1.057<br>✅ 688 | **0.62×** |
| **Ring16 nt4** | 0.0004 / 0.140–0.145<br>✅ 688 | 0.122 / 0.461–0.496<br>✅ 688 | 0.194 / 4.945–5.142<br>✅ 688 | 0.304 / 3.363–3.419<br>✅ 688 | **0.68×** |
| **Ring160 nt1** | 0.0017 / 5.759–6.094<br>✅ 6880 | 0.149 / 4.168–4.559<br>✅ 6880 | 0.254 / 2.724–2.789<br>✅ 6880 | 0.838 / 1.520–1.560<br>✅ 6880 | **0.56×** |
| **Ring160 nt4** | 0.0015 / 1.221–1.238<br>✅ 6880 | 0.158 / 4.418–4.586<br>✅ 6880 | 0.274 / 6.718–6.828<br>✅ 6880 | 0.951 / 4.085–4.118<br>✅ 6880 | **0.61×** |
| **Dentate nt1** (1-rank) | 0.0062 / 2.330–2.469<br>✅ 400 | 0.324 / 1.001–1.038<br>✅ 400 | 0.357 / 0.573–0.628<br>✅ 400 | 1.041 / 0.753–0.817<br>✅ 400 | **1.31×** |
| **Dentate nt4** (1-rank) | 0.0034 / 1.004–1.045<br>✅ 400 | 0.313 / 1.162–1.226<br>✅ 400 | 0.502 / 1.041–1.115<br>✅ 400 | 1.184 / 1.888–2.000<br>✅ 400 | **1.81×** |
| **Traub no-gap** 1/10 | 0.010 / 38.32–38.57<br>✅ 4474 | 0.695 / 29.45–30.90<br>✅ 4474 | 0.740 / 9.022–9.062<br>✅ 4474 | 3.937 / 8.000–8.286<br>✅ 4474 | **0.89×** |
| **Traub gap** 1/10 | 0.011 / 40.28–42.03<br>✅ 7873 | 0.628 / 30.65–31.99<br>✅ 7873 | 0.911 / 10.38–10.49<br>✅ 7873 | 3.792 / 9.485–9.789<br>✅ 7873 | **0.91×** |

---

## Notes

1. **New column** `native/CN GPU` is min of the three post-throwaway solves, not setup and not a mean. Parser: `harness/parse_matrix.py`. Do not fold the ratio into the GPU (native) cell.
2. **Traub gap identity closed on this matrix.** Native, CN, and CN GPU are all **7873** vs CPU (was native ❌ 7991 and CN ❌ 7867 on `2026-09-11-psolve-setup-warm` @ `75d218a3b`). Persist finitialize + CN integer-n are on tip `0cebf94ff`.
3. **Dentate nt1 exclusive GPU.** Native setup **1.041 s** / solve **0.753–0.817 s** vs CN GPU setup **0.357 s** / Solver **0.573–0.628 s**. Fast-warm ratio **1.31×** (0.753 / 0.573). Morning campaign @ `75d218a3b` was **1.24×** (0.657 / 0.530) — same spread, quieter clocks. Not a new residual.
4. **CN GPU Dentate i=0** is still first-touch (**0.628 s** vs **0.573 / 0.580**). Throwaway `psolve(dt)` does not buy CN’s full-run kernel first-touch.
5. **Ring and Traub native are faster than CN GPU** on the step loop (ratios **0.56–0.91×**). Ring16 nt1 native still declines 1.057 → 1.007 → 0.961 (`tstop=100` first-touch is not paid by one `dt`).
6. **nt=4 GPU** is still slower than nt1 on this T1000. Not the exclusive-GPU ratio.
7. Traub harness times **psolve only** (not `prun`’s stdinit). Native Traub setup (~3.8–3.9 s) is the copyin that used to sit in i=0 `runtime`.

Raw: `raw/*.log`, `raw/spikes/<tag>/`, `raw/results.csv`, `raw/table.md`. META: `META.md`.
