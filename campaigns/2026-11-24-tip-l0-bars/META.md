# Campaign: 2026-11-24 tip L0 product bars

| Field | Value |
|-------|--------|
| `campaign_id` | `2026-11-24-tip-l0-bars` |
| `date` | `2026-11-24T10:50:17-05:00` |
| `machine` | hines-ThinkStation-P5 / NVIDIA T1000 8GB |
| `product_tree` | `~/neuron/nrngpu` |
| `branch` | `hines-grok/gpu-native` |
| `tip_sha` | `f39717f745478885b0861364b3f7f1e20ac940a4` (`f39717f74`) |
| `identity_policy` | `product_bars_required` (full L0: ring, dentate, Traub) |
| `golden_ring` | 688 spikes @ tstop=100; prcellstate gid 32 CPU vs native |
| `golden_dentate` | 400 sorted multiset; ctest reduced_dentate_native |
| `golden_traub_nogap` | 4474 |
| `golden_traub_gap` | 7873 |
| `wall_method` | ctest real time + ringtest runtime if printed; secondary only |
| `notes` | Fresh re-measure (not an append to `2026-08-10-tip-l0-bars`). `harness/run_matrix.sh` not run. Product source not edited. Binary banner `9.1.0.dev0-342-gf39717f74 hines-grok/gpu-native (f39717f74)`. |
