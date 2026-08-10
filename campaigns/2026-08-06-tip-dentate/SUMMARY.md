# Campaign SUMMARY: 2026-08-06-tip-dentate

**Closed:** 2026-08-10 (plan **2.4.3** + **2.4.5**; **2.4.4** ring/Traub not run)  
**Tip:** `local/gpu-native` @ `0bdfca4b1` (`0bdfca4b1b046fae4cde2e503a10fae00844d3f4`)  
**Machine:** hines-ThinkStation-P5 / NVIDIA T1000 8GB  
**Identity policy:** product bars required for dentate; 1-rank multi-psolve = wall probes (`identity=n/a`)

---

## Identity (product bar)

| Config | Backend | Identity | Status | Wall (secondary) | Notes |
|--------|---------|----------|--------|------------------|-------|
| dentate product 4-rank | `gpu_native` + MPS | `multiset:400` vs checked-in ref | **pass** | psolve **1.133 s**; ctest real **4.77 s** | `reduced_dentate_native::neuron_gpu_native` + `compare_results` |
| dentate product compare | same | ref match | **pass** | 0.12 s | `neuron_gpu_native matches reference_file` |

Spike file line counts (4 ranks): 106+97+101+96 = **400**.

Logs (local, often gitignored): `raw/ctest-dentate-native.log`, `raw/ctest-dentate-compare.log`.

---

## Wall probes (1-rank multi-psolve, 3×; identity n/a)

Method: `harness/dentate_multi_psolve.py` — cold / warm_min–warm_max seconds.  
All eight cells **OK** (no SEGV; contrast archive 2026-08-05 native GPU **ERR**).

| Config | CPU | GPU (native) | CN CPU | CN GPU |
|--------|-----|--------------|--------|--------|
| Dentate nt1 | 2.327 / 2.27–2.292 | **2.245 / 1.885–1.896** | 0.987 / 0.958–1.223 | 0.644 / 0.531–0.532 |
| Dentate nt4 | 0.905 / 0.875–0.892 | **3.547 / 3.004–3.134** | 1.042 / 1.06–1.071 | 1.048 / 0.956–0.963 |

| Config | Backend | Identity | Status | Wall cold / warm |
|--------|---------|----------|--------|------------------|
| dent_nt1 | cpu | n/a | ok | 2.327 / 2.27–2.292 |
| dent_nt1 | gpu_native | n/a | ok | 2.245 / 1.885–1.896 |
| dent_nt1 | cn_cpu | n/a | ok | 0.987 / 0.958–1.223 |
| dent_nt1 | cn_gpu | n/a | ok | 0.644 / 0.531–0.532 |
| dent_nt4 | cpu | n/a | ok | 0.905 / 0.875–0.892 |
| dent_nt4 | gpu_native | n/a | ok | 3.547 / 3.004–3.134 |
| dent_nt4 | cn_cpu | n/a | ok | 1.042 / 1.06–1.071 |
| dent_nt4 | cn_gpu | n/a | ok | 1.048 / 0.956–0.963 |

Raw: `raw/wall/*.log`, `raw/wall/table.md`, `raw/wall/results.csv`.

---

## Verdict

| Gate | Result |
|------|--------|
| Dentate **400** identity on tip | **GREEN** |
| 1-rank native GPU wall probes | **GREEN** (runs complete; nt4 GPU slower as expected) |
| Ring / Traub this campaign | **skipped** (optional **2.4.4**) |

**Vs archive 2026-08-05:** that run was timing-only with dentate native **SEGV**; this tip product bar is green and 1-rank GPU probes finish.

---

## META

See `META.md`. Schema: `../../schema.md`. Identity design: `../IDENTITY.md`.
