# Campaign: 2026-08-06 tip dentate refill

| Field | Value |
|-------|--------|
| `campaign_id` | `2026-08-06-tip-dentate` |
| `date` | `2026-08-10T09:45:36-04:00` |
| `machine` | hines-ThinkStation-P5 / NVIDIA T1000 8GB |
| `product_tree` | `~/neuron/nrngpu` |
| `branch` | `local/gpu-native` |
| `tip_sha` | `0bdfca4b1b046fae4cde2e503a10fae00844d3f4` (`0bdfca4b1`) |
| `identity_policy` | `product_bars_required` (dentate only this campaign) |
| `golden_dentate` | 400 sorted multiset; ctest `reduced_dentate_native::neuron_gpu_native` |
| `wall_method` | product ctest wall; optional 1-rank multi-psolve cold/warm (3×) from harness |
| `hypothesis_id` | (none new; post-SEGV refill after H-matrix-2026-08-05 ERR) |
| `notes` | Plan **2.4.3** — dentate only; ring/Traub optional **2.4.4** skipped unless added later |
