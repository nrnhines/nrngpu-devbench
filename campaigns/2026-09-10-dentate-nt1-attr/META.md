# Campaign: 2026-09-10 Dentate nt1 exclusive attribution (L1+)

| Field | Value |
|-------|--------|
| `campaign_id` | `2026-09-10-dentate-nt1-attr` |
| `date` | `2026-09-10` |
| `status` | **L1+L2 recorded** — next is H-dentate-nt1-host-nr-soa (not density) |
| `machine` | hines-ThinkStation-P5 / NVIDIA T1000 8GB exclusive (no MPS) |
| `product_tree` | `~/neuron/nrngpu` |
| `branch` | `local/gpu-native` |
| `tip_sha` | `76ba78245` (code); docs may be `245eb183f`+ |
| `identity_policy` | `cpu_same_cell` already ✅ 400 in parent campaign; this campaign is **timers**, not a new identity matrix |
| `parent_campaign` | `2026-09-10-tip-psolve-matrix` |
| `hypothesis_id` | `H-dentate-1rank-cngpu` |
| `plan` | `nrngpu/doc/gpu/dentate-nt1-attribution.md` |

## What this is

Split the measured 3.4× (native warm ~1.80 s vs CN GPU ~0.53 s) with phase timers → ACC_TIME → traffic. **Not** 4-rank MPS. **Not** density recode until a child hypothesis has a wall number.

## Runs

| Tag | Env | Purpose |
|-----|-----|---------|
| `dent_nt1_gpu_phase` | `NRN_NATIVE_GPU_PHASE_TIMER=1` | L1 coarse + nested + gap traffic |
| `dent_nt1_gpu_acct` | `NVCOMPILER_ACC_TIME=1` | L2 (after L1 names a bucket) |
| `dent_nt1_cn_gpu_acct` | same, `NRN_DENTATE_ENGINE=cn_gpu` | L2 CN kernel analogue |
