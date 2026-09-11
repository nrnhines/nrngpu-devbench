# Campaign SUMMARY: 2026-09-11-psolve-setup-warm

**Closed:** 2026-09-11T10:16:47-04:00  
**Kind:** 8×4 psolve matrix with throwaway `psolve(dt)` then 3 warms (identity `cpu_same_cell`; not ctest wall)  
**Tip:** `local/gpu-native` @ `75d218a3b` (GPU mirrors persist across psolve)  
**Machine:** hines-ThinkStation-P5 / NVIDIA T1000 8GB  
**Launches:** 32/32 OK (Traub gap native identity fail — see notes)  
**4-rank dentate:** omitted

Stamp: `branch=local/gpu-native commit=75d218a3b date=2026-09-11T10:04:56-04:00`

---

## Results

**Wall:** `setup / solve_min–solve_max` seconds.  
**setup** = interpreter wall of throwaway `psolve(dt)` (first-process copyin/mk_mech + one step).  
**solve** = three full-tstop psolves after `stdinit`. NEURON: `psolve=` / `runtime=`. CN: CoreNEURON `Solver Time` (last three).

**Identity:** last-psolve raster vs CPU of the same config (exact sorted t,gid).

| Mark | Meaning |
|------|---------|
| ✅ | Spike identity **pass** |
| ❌ | Spike identity **fail** |

| Config | CPU | CN | CN GPU | GPU (native) |
|--------|:----:|:--:|:------:|:------------:|
| **Ring16 nt1** | 0.0002 / 0.469–0.470<br>✅ 688 | 0.116 / 0.410–0.473<br>✅ 688 | 0.175 / 1.297–1.379<br>✅ 688 | 0.379 / 0.692–0.948<br>✅ 688 |
| **Ring16 nt4** | 0.0004 / 0.129–0.132<br>✅ 688 | 0.110 / 0.421–0.428<br>✅ 688 | 0.192 / 4.485–4.576<br>✅ 688 | 0.279 / 3.059–3.169<br>✅ 688 |
| **Ring160 nt1** | 0.0011 / 3.565–3.594<br>✅ 6880 | 0.152 / 3.902–4.063<br>✅ 6880 | 0.262 / 2.525–2.606<br>✅ 6880 | 0.751 / 1.373–1.444<br>✅ 6880 |
| **Ring160 nt4** | 0.0014 / 1.046–1.174<br>✅ 6880 | 0.139 / 3.793–3.801<br>✅ 6880 | 0.258 / 6.093–6.215<br>✅ 6880 | 0.845 / 3.550–3.619<br>✅ 6880 |
| **Dentate nt1** (1-rank) | 0.0059 / 2.174–2.185<br>✅ 400 | 0.285 / 0.944–0.951<br>✅ 400 | 0.357 / 0.530–0.630<br>✅ 400 | **0.875 / 0.657–0.704**<br>✅ 400 |
| **Dentate nt4** (1-rank) | 0.0028 / 0.848–0.899<br>✅ 400 | 0.311 / 0.996–1.001<br>✅ 400 | 0.354 / 0.940–0.990<br>✅ 400 | 0.980 / 1.645–1.711<br>✅ 400 |
| **Traub no-gap** 1/10 | 0.010 / 33.66–33.81<br>✅ 4474 | 0.582 / 27.32–27.77<br>✅ 4474 | 0.686 / 8.451–8.471<br>✅ 4474 | **3.28 / 7.369–7.546**<br>✅ 4474 |
| **Traub gap** 1/10 | 0.010 / 34.93–35.10<br>✅ 7873 | 0.573 / 27.42–27.58<br>❌ 7867 | 0.682 / 9.514–9.562<br>❌ 7867 | 3.36 / 8.648–8.855<br>❌ 7991 |

---

## Notes

1. **Dentate nt1 exclusive GPU (the cell this protocol was for).** Native **setup 0.875 s** (copyin + 1 dt) vs CN GPU setup **0.357 s** (interpreter wall of `psolve(dt)`, includes mk_mech). Native **solve 0.657–0.704 s** vs CN GPU **Solver Time 0.530–0.630 s**. Warm native vs best CN GPU ≈ **1.24×** (0.657 / 0.530). Campaign 2026-09-10 mixed native copyin into i=0 `psolve=` (2.053 / 1.80).
2. **CN GPU solve is not fully homogeneous after `psolve(dt)`.** Dentate CN GPU first of the three is still **0.630 s** vs **0.530–0.544** after. Throwaway one step does not buy CN’s full-run kernel first-touch; that still sits in the first *full* `tstop`. Native Dentate first solve 0.704 vs 0.657 is a much smaller leftover.
3. **Ring16 nt1 native** solve still declines 0.948 → 0.847 → 0.692: `tstop=100` first-touch is not paid by one `dt`. Ring160 nt1 native solve **1.37–1.44** vs CN GPU **2.53–2.61** (native faster on the step loop).
4. **Traub no-gap** native solve **7.37–7.55** vs CN GPU **8.45–8.47** (≈ **0.87×** CN; was ~1.21× when `prun` timed stdinit+psolve). ✅ 4474.
5. **Traub gap native ❌ 7991** vs CPU 7873. Not throwaway-only: old 3× `prun()` on this tip is **7978**. Persist GPU mirrors (`75d218a3b`) likely leave gap state across `stdinit`. CN / CN GPU ❌ 7867 is the known CoreNEURON −6.
6. **nt=4 GPU** still slower than nt1 on this T1000. Not the exclusive-GPU ratio.
7. Traub harness times **psolve only** (not `prun`’s stdinit). CPU Traub solve matches old warm (~33–35 s); native Traub setup (~3.2 s) is the copyin that used to sit in i=0 `runtime`.

Raw: `raw/*.log`, `raw/spikes/<tag>/`, `raw/results.csv`, `raw/table.md`. META: `META.md`.
