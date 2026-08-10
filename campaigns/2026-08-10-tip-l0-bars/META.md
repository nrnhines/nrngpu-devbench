# Campaign: 2026-08-10 tip L0 product bars

| Field | Value |
|-------|--------|
| `campaign_id` | `2026-08-10-tip-l0-bars` |
| `date` | `2026-08-10T10:44:46-04:00` |
| `machine` | hines-ThinkStation-P5 / NVIDIA T1000 8GB |
| `product_tree` | `~/neuron/nrngpu` |
| `branch` | `local/gpu-native` |
| `tip_sha` | `0bdfca4b1b046fae4cde2e503a10fae00844d3f4` (`0bdfca4b1`) |
| `identity_policy` | `product_bars_required` (full L0: ring, dentate, Traub) |
| `golden_ring` | 688 spikes @ tstop=100; prcellstate gid 32 CPU vs native |
| `golden_dentate` | 400 sorted multiset; ctest reduced_dentate_native |
| `golden_traub_nogap` | 4474 |
| `golden_traub_gap` | 7873 |
| `wall_method` | ctest real time + ringtest psolve if printed; secondary only |
| `notes` | Option **B**: new campaign (not append to 2026-08-06-tip-dentate). Fresh re-measure on tip. |
