# L0 — product bars (GPU-native tip)

**Role:** checklist only. Identity gates live in **product** trees and **ctest**, not in this repo.  
**Primary product tree:** `~/neuron/nrngpu`  
**Living tip (typical):** branch `local/gpu-native`  
**Env:** `source ~/neuron/bin/nrnenv nrngpu build-gpu`  
**Native defaults:** `NRN_GPU_BACKEND_TEST=native`, `NRN_GPU_PERMUTE=2`  
**Multi-rank one GPU:** prefer CUDA MPS (`bash ~/neuron/nrngpu/test/external/ensure_cuda_mps.sh`)

Record tip SHA when you re-check: `git -C ~/neuron/nrngpu rev-parse HEAD`.

---

## Bars (closed as product facts)

| Bar | Gate | Product location (approx.) | Notes |
|-----|------|----------------------------|--------|
| **Ring spikes** | **688** @ `tstop=100` | `build-gpu/test/external_ringtest/…`; harness `test/external/ringtest/prcellstate_native_gpu.sh` | Long identity gate; dV noise-only |
| **Dentate spikes** | **400** (sorted multiset) | `reduced_dentate_native::neuron_gpu_native` (4-rank product) | Use MPS on single GPU; SEGV path closed on tip |
| **Traub no-gap** | **4474** exact native↔CPU | `traub_native::neuron_gpu_native`; model `~/models/82894` | Skip if model missing |
| **Traub gap** | **7873** exact native↔CPU | `traub_native::neuron_gpu_native_gap` | CN gap 7867 known −6; native↔CPU is the bar |

---

## How to re-check (sketch)

Adjust build dir if yours differs (`build-gpu`).

```bash
source ~/neuron/bin/nrnenv nrngpu build-gpu
export NRN_GPU_BACKEND_TEST=native
export NRN_GPU_PERMUTE=2
cd ~/neuron/nrngpu/build-gpu

# Ring long gate (example product path; see tree docs if names differ)
# ctest -V -R 'external_ringtest'   # or prcellstate_native_gpu.sh 32 1

# Dentate product (multi-rank; start MPS first)
bash ~/neuron/nrngpu/test/external/ensure_cuda_mps.sh
ctest -V -R 'reduced_dentate_native::neuron_gpu_native'

# Traub product
ctest -V -R 'traub_native::neuron_gpu_native'
ctest -V -R 'traub_native::neuron_gpu_native_gap'
```

Authoritative harness details: `nrngpu/doc/gpu/native-coreneuron-parity.md`, `GROK-GPU-NATIVE.md`, `AGENTS.md`.

---

## L0 vs campaigns

| | L0 | L1/L2 campaign |
|--|----|----------------|
| Pass means | Product still correct on tip | Dated measurement + optional identity cells |
| Where | nrngpu ctest / scripts | `devbench/campaigns/` |
| Timing | Optional secondary | Recorded per schema |

Do **not** invent a second golden spike store here unless a campaign explicitly snapshots refs with tip SHA.
