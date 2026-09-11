# Hypothesis ledger

**Purpose:** attach wall / residual / perf claims to stable ids so sessions do not re-litigate from chat.  
**States:** `open` → `measured` → `closed` \| `no-merge` \| `parked`

Add a row when you form a claim; update state when measured. Link campaigns via `hypothesis_id` in `schema.md`.

---

## Active / recorded

| ID | Claim (one line) | State | Evidence / tip | Notes |
|----|------------------|-------|----------------|-------|
| H-density-math | Traub multi-warm residual ~1.07–1.10× CN is real STATE/CURRENT math, not a new H→D tax | measured | 2026-08-06 re-smoke; portfolio / parity log | Do not re-open ion SoA / net_buf / NSB without new wall hypothesis |
| H-matrix-2026-08-05 | 2026-08-05 matrix is **timing-only** (no spike ✓/✗); dentate native **ERR** on that tip | archived | `archive/2026-08-05-matrix/` @ tip `7ef35f6e2` (**2.4.1** frozen) | Source also under `notes/perf_matrix/`; do not overwrite |
| H-dentate-refill-2026-08 | Dentate product identity green on tip after SEGV era; 1-rank GPU wall probes complete | closed | campaign `2026-08-06-tip-dentate` @ `0bdfca4b1` — multiset:400 pass; psolve ~1.13 s (4-rank MPS) | Wall probes identity n/a by design |
| H-l0-smoke-2026-08-10 | Full L0 product bars green on tip (ring 688, dentate 400, Traub 4474/7873) | closed | campaign `2026-08-10-tip-l0-bars` @ `0bdfca4b1` | prcellstate rdcellstate exit 1 at float noise only (≤1e-13) |
| H-dentate-1rank-cngpu | 1-rank Dentate nt1 CN GPU warm is ~3× native GPU | closed | campaign `2026-09-11-psolve-setup-warm` @ `75d218a3b` — native setup 0.875 / solve 0.657–0.704 vs CN GPU setup 0.357 / Solver 0.530–0.630; ✅ 400 | Copyin isolated in setup. Warm ≈1.24× CN GPU (0.657/0.530). Supersedes 2026-09-10 3.4× cell. |
| H-traub-gap-persist | Traub gap native over-spikes after GPU-mirror persist | measured | campaign `2026-09-11-psolve-setup-warm` @ `75d218a3b` — 7991 vs CPU 7873; old 3× prun() also 7978 | Not throwaway-only. Gap buffers likely stale across stdinit. No-gap ✅ 4474. |
| H-dentate-nt1-host-nr-soa | Host NET_RECEIVE full-mech SoA H→D (`upload_present_mechanism_soa_to_device`) is the exclusive-GPU residual vs CN | measured | campaign `2026-09-10-dentate-nt1-attr` — 292 620 `update device` (~244 cols/step, ~0.22 s copyin); STATE/CURRENT kernels ≈ CN; deliver-tq ~0.49 s | Next recode: slim/elide that upload. Not density. Not 4-rank MPS |

---

## Template (copy a row)

| ID | Claim (one line) | State | Evidence / tip | Notes |
|----|------------------|-------|----------------|-------|
| H-… | … | open | | |

---

## State meanings

| State | Meaning |
|-------|---------|
| `open` | Claimed; not yet measured on a recorded tip |
| `measured` | Numbers or identity recorded; may still be open product work |
| `closed` | Done; no further action (or absorbed into product) |
| `no-merge` | Exploratory fix tried; wall flat or rejected for tip |
| `parked` | Valid claim; deliberately deferred |
| `archived` | Historical context only |
