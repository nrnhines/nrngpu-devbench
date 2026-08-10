# Campaign SUMMARY: 2026-08-10-tip-l0-bars

**Closed:** 2026-08-10  
**Kind:** L0 product-bar smoke on living tip (option **B** — new campaign, fresh re-measure)  
**Tip:** `local/gpu-native` @ `0bdfca4b1` (`0bdfca4b1b046fae4cde2e503a10fae00844d3f4`)  
**Machine:** hines-ThinkStation-P5 / NVIDIA T1000 8GB  
**Not:** reuse of archive 2026-08-05 timing cells; not an append to `2026-08-06-tip-dentate`

---

## Identity (product bars)

| Config | Backend | Identity | Status | Wall (secondary) | How |
|--------|---------|----------|--------|------------------|-----|
| Ring spikes @ tstop=100 | `gpu_native` 1-rank | `spikes:688` | **pass** | runtime ~0.88 s (GPU leg of prcell path) | `ringtest.py -gpu-native -tstop 100` → `spk2.std` lines |
| Ring 2-rank MPI product | `gpu_native` + MPS | ctest green | **pass** | ctest real **1.73 s** | `external_ringtest::neuron_gpu_native_mpi` |
| Ring prcellstate gid 32 @ t=100 | CPU vs `gpu_native` | noise-only max \|d\| ~**1e-13** | **pass*** | CPU runtime ~0.39 s; GPU ~0.88 s | `prcellstate_native_gpu.sh 32 100` + `rdcellstate` |
| Dentate product 4-rank | `gpu_native` + MPS | `multiset:400` | **pass** | psolve **1.216 s**; ctest **4.57 s** | `reduced_dentate_native::neuron_gpu_native` + compare |
| Traub no-gap 1/10 | `gpu_native` | **4474** exact | **pass** | ctest **61.5 s** | `traub_native::neuron_gpu_native` |
| Traub gap 1/10 | `gpu_native` | **7873** exact | **pass** | ctest **16.8 s** | `traub_native::neuron_gpu_native_gap` |

\* `rdcellstate.py` exited **1** because it treats any non-zero float as a diff; all reported \|d\| are ≤ ~1e-13 (product “noise-only” convention). Spike identity **688** both legs. Not a product-bar fail.

---

## Verdict

| L0 bar | Result |
|--------|--------|
| Ring **688** | **GREEN** |
| Dentate **400** | **GREEN** |
| Traub **4474** / **7873** | **GREEN** |
| **Campaign** | **CLOSED GREEN** on tip `0bdfca4b1` |

Raw logs: `raw/*.log`, `raw/results.txt`, `raw/ring_spk2_gpu.std`.

---

## Related

| Path | Role |
|------|------|
| `META.md` | Campaign metadata |
| `../2026-08-06-tip-dentate/` | Earlier dentate-only refill (same tip family) |
| `../../archive/2026-08-05-matrix/` | Timing-only freeze (not this campaign) |
| `../../l0/PRODUCT_BARS.md` | How to re-check without a campaign |
| `../IDENTITY.md` | Identity field design |
