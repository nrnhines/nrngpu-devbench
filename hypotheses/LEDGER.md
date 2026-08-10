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
