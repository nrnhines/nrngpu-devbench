# Campaign SUMMARY: 2026-09-10 Dentate nt1 exclusive attribution

**Status:** L1 + L2 recorded (2026-09-10). No product recode this campaign.  
**Tip:** `local/gpu-native` @ `76ba78245`  
**Parent wall:** `2026-09-10-tip-psolve-matrix` — native warm ~1.80 s vs CN GPU ~0.53 s (≈3.4×), ✅ 400.  
**Plan:** `nrngpu/doc/gpu/dentate-nt1-attribution.md`

Exclusive 1-rank, `nthread=1`, `max_cells=100`, `tstop=10`. **Not** 4-rank MPS.

## L1 — phase timer (`NRN_NATIVE_GPU_PHASE_TIMER=1`)

Warm i=2 psolve **1.967 s** (timer tax vs product 1.80 s).

| Bucket | s |
|--------|---|
| lastpart | 0.762 (nonvint 0.373 + deliver 0.389) |
| setup-tree-matrix | 0.195 (rhs 0.185, lhs 0.010) |
| start deliver-events | 0.129 |
| deliver-tq (nested, start+lastpart) | **0.488** |
| deliver-nrb | **0.009** |
| gap gather+scatter | 0.037 |
| matrix-solver | 0.037 |
| coarse-sum | 1.14 (**uncovered ~0.83 s**) |

Traffic: `full_v_pulls=0` `bulk_mech_pushes=0` `h2d_scalar=0`. t=1 ms still ~0.78 s vs ~0.12 s other ms.

## L2 — ACC_TIME (wall inflated; native warm 3.22 s, CN Solver 1.02 s)

STATE/CURRENT kernel avgs **≈ CN** (na8st 119 vs 124 µs; Aradi_Ca 78 vs 79; CadepK 38 vs 40). Native `nrn_state_*` sum 0.31 s/psolve vs CN 0.34; `nrn_cur_*` 0.15 vs 0.22.

Native OpenACC API `acc_copyin` **308 063** / 0.73 s vs CN **828** / 0.009 s.  
`upload_soa_storage_to_device` mech floats: **292 620** H→D (~244 columns/step, 0.22 s/psolve). Caller: host NET_RECEIVE → `upload_present_mechanism_soa_to_device` (Gfluct3 / WATCH / BBCOREPOINTER).

## Decision

Do **not** recode density. Next: **H-dentate-nt1-host-nr-soa** — slim/elide full-mech SoA H→D after host NET_RECEIVE; re-measure this cell.

Raw logs (gitignored): `raw/dent_nt1_gpu_phase.log`, `raw/dent_nt1_gpu_acct.log`, `raw/dent_nt1_cn_gpu_acct.log`.
