# Campaign identity design (2.4.2)

**Status:** agreed for first campaigns  
**Timing:** secondary — always optional; never substitutes for identity on product-relevant cells  
**Schema base:** `../schema.md`

---

## Principle

A campaign cell that claims product relevance must answer: **did the simulation still produce the agreed spike identity on this tip?** Wall time without that answer is archive-class timing-only (see `archive/2026-08-05-matrix/`).

---

## Golden sources (by model)

| Model | Identity gate | Golden / how checked | Product harness |
|-------|---------------|----------------------|-----------------|
| **Ring** | **688** spikes @ `tstop=100` (sorted multiset match product ref / CPU) | Product ctest / `prcellstate_native_gpu.sh` long gate | `test/external/ringtest/` |
| **Dentate** | **400** spikes sorted multiset @ max_cells=100, tstop=10 | Checked-in ref vs run (ctest) | `reduced_dentate_native::neuron_gpu_native` (4-rank; **MPS** on 1 GPU) |
| **Traub no-gap** | **4474** exact native↔CPU | Product ctest ref | `traub_native::neuron_gpu_native` |
| **Traub gap** | **7873** exact native↔CPU | Product ctest ref | `traub_native::neuron_gpu_native_gap` |

L0 checklist (how to re-check without a campaign): `../l0/PRODUCT_BARS.md`.

---

## Cell field encoding

Use the `identity` column from `schema.md`:

| Value | When |
|-------|------|
| `pass` | Gate matched golden for this config |
| `fail` | Gate did not match (attach log_ref) |
| `multiset:400` + status `ok`/`fail` | Explicit multiset size (dentate product) |
| `spikes:688` + status | Count-only if multiset not available (prefer multiset) |
| `n/a` | **Non-product** timing probe only (e.g. 1-rank wall matrix) — mark META `identity_scope` |
| `skip` | Not run this campaign |

### Product vs matrix cells

| Cell kind | Identity required? | Example |
|-----------|-------------------|---------|
| **Product bar cell** | **Yes** | 4-rank dentate MPS = L0 bar |
| **Timing probe cell** | No (`n/a`) if META says probes are wall-only; prefer still recording product bar once per campaign | 1-rank dentate multi-psolve from `harness/` |

First campaign (**2.4.3**): record **product dentate identity** (400) once per tip; timing probes for dent_nt1/nt4 may be `n/a` on identity with wall filled, **or** omitted if only product bar is run.

---

## META fields (identity)

| Field | Example |
|-------|---------|
| `identity_policy` | `product_bars_required` |
| `golden_dentate` | `400 sorted multiset; ctest reduced_dentate_native` |
| `golden_ring` | `688 @ tstop=100` |
| `golden_traub_nogap` | `4474` |
| `golden_traub_gap` | `7873` |

---

## Non-goals

- Do not re-home golden spike files into devbench (product owns refs).  
- Do not treat CoreNEURON spike deltas as native bars when product says native↔CPU is the bar (Traub gap CN −6 known).  
- Do not call a campaign “closed green” if product identity cells are `fail` or missing when required.
