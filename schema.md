# Campaign result schema (L1 / L2)

**Purpose:** one row = one measured cell, comparable across tips and dates.  
**Identity first; timing second.** Timing-only matrices are incomplete campaigns.

---

## Campaign metadata (once per campaign dir)

| Field | Required | Example |
|-------|----------|---------|
| `campaign_id` | yes | `2026-08-06-tip-refill` |
| `date` | yes | `2026-08-06` |
| `machine` | yes | host + GPU model |
| `product_tree` | yes | `~/neuron/nrngpu` |
| `branch` | yes | `local/gpu-native` |
| `tip_sha` | yes | full or short git SHA |
| `notes` | no | free text / link to hypothesis ids |

Suggested layout:

```text
campaigns/<campaign_id>/
  META.md          # metadata table
  SUMMARY.md       # human table (identity + timing)
  results.csv      # optional machine-readable (often gitignored if huge)
  raw/             # logs (gitignored)
```

---

## Cell fields (each matrix cell / row)

| Field | Required | Description |
|-------|----------|-------------|
| `config` | yes | Human id, e.g. `dent_nt1`, `ring_n160_nt1`, `traub_nogap` |
| `backend` | yes | `cpu` \| `gpu_native` \| `cn_cpu` \| `cn_gpu` (or product-local names) |
| `identity` | **yes for L1+** | See below |
| `wall_cold_s` | no | First psolve / cold |
| `wall_warm_s` | no | Warm range or mean (document method) |
| `wall_method` | if wall present | e.g. `3× psolve cold/warm_min–warm_max` |
| `hypothesis_id` | no | Link into `hypotheses/LEDGER.md` |
| `status` | yes | `ok` \| `fail` \| `skip` \| `err` |
| `log_ref` | no | Path under `raw/` or external |

### Identity values

Prefer one of:

| Value | Meaning |
|-------|---------|
| `pass` / `fail` | Agreed gate vs golden (document gate in META) |
| `multiset:N` + `pass`/`fail` | Spike count multiset size N matched / not |
| `spikes:N` | Count only (weaker; say if sorted multiset) |
| `n/a` | Timing-only cell (**legacy**; mark campaign as timing-only) |

Golden source must be stated in META (e.g. product ctest ref, CPU run same tip, or archived ref file + SHA).

---

## L1 vs L2 (lightweight)

| | L1 | L2 |
|--|----|-----|
| Scope | One model family or small matrix | Broader matrix / multi-machine |
| Identity | Required on product-relevant cells | Required |
| Hypothesis | Optional | Prefer linking residuals |

---

## CSV columns (optional)

```text
config,backend,identity,wall_cold_s,wall_warm_s,wall_method,hypothesis_id,status,log_ref
```

---

## Preferred SUMMARY matrix (human table)

Column order (archive-like, **GPU (native)** last):

```text
Config | CPU | CN | CN GPU | GPU (native)
```

Each body cell:

1. Wall (or `—` if not run) on the first line(s).  
2. Identity mark **bottom-right** (second line, right-aligned in HTML for GitHub):

| Mark | Meaning |
|------|---------|
| ✅ | Spike raster / multiset identity **pass** |
| ❌ | Identity **fail** |
| ➖ | Timing/run only — identity not checked |

Example cell (GFM + HTML, renders on GitHub):

```html
<div align="right">2.245 / 1.885–1.896<br>✅ 400</div>
```

See `campaigns/2026-08-10-tip-l0-bars/SUMMARY.md`.

## Non-goals

- Do not replace L0 product ctests.  
- Do not overwrite `archive/` or prior campaign SUMMARY in place.  
- Full matrix re-run only when a plan step says so.
