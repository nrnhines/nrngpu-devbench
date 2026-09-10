#!/usr/bin/env python3
"""Parse psolve-matrix logs + last-psolve rasters into wall table + identity CSV."""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

from identity import identity_vs_cpu, load_spike_dir

SOLVER_RE = re.compile(r"Solver Time\s*:\s*([0-9.eE+-]+)")
MULTI_RE = re.compile(r"MULTI_PSOLVE i=(\d+)\s+runtime=([0-9.eE+-]+)")
MULTI_PSOLVE_RE = re.compile(r"MULTI_PSOLVE i=(\d+)\s+psolve=([0-9.eE+-]+)")
MULTI_MARK_RE = re.compile(r"MULTI_PSOLVE i=(\d+)\s+psolve_wall_mark")


def parse_log(text: str, engine: str) -> list[float] | None:
    """Return three seconds for this engine, or None if incomplete."""
    if engine in ("cn_cpu", "cn_gpu"):
        solvers = [float(m.group(1)) for m in SOLVER_RE.finditer(text)]
        if len(solvers) >= 3:
            return solvers[:3]
        # fallback: NEURON runtime markers if Solver Time missing
    times: list[tuple[int, float]] = []
    for m in MULTI_RE.finditer(text):
        times.append((int(m.group(1)), float(m.group(2))))
    if not times:
        for m in MULTI_PSOLVE_RE.finditer(text):
            times.append((int(m.group(1)), float(m.group(2))))
    if engine in ("cn_cpu", "cn_gpu") and len(solvers := [float(m.group(1)) for m in SOLVER_RE.finditer(text)]) >= 1:
        # Pair by order if we have 3 solver times
        if len(solvers) >= 3:
            return solvers[:3]
    if len(times) >= 3:
        times.sort(key=lambda x: x[0])
        return [t for _, t in times[:3]]
    if len(times) > 0:
        times.sort(key=lambda x: x[0])
        return [t for _, t in times]
    return None


def fmt_cell(vals: list[float] | None) -> str:
    # Use "/" not "|" so markdown tables stay valid.
    if not vals:
        return "ERR"
    if len(vals) == 1:
        return f"{vals[0]:.4g} / —"
    cold = vals[0]
    warm = vals[1:]
    if len(warm) == 1:
        return f"{cold:.4g} / {warm[0]:.4g}"
    return f"{cold:.4g} / {min(warm):.4g}–{max(warm):.4g}"


# row key -> (label, log_prefix pattern pieces)
ROWS = [
    ("ring_n16_nt1", "Ring16 nt1"),
    ("ring_n16_nt4", "Ring16 nt4"),
    ("ring_n160_nt1", "Ring160 nt1"),
    ("ring_n160_nt4", "Ring160 nt4"),
    ("dent_nt1", "Dentate nt1"),
    ("dent_nt4", "Dentate nt4"),
    ("traub_nogap", "Traub no-gap"),
    ("traub_gap", "Traub gap"),
]
# Display order matches campaign SUMMARY (GPU native last).
COLS = [("cpu", "CPU"), ("cn_cpu", "CN"), ("cn_gpu", "CN GPU"), ("gpu", "GPU (native)")]


def main() -> None:
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/perf-matrix")
    stamp = (out / "stamp.txt").read_text() if (out / "stamp.txt").exists() else ""
    rows_out: list[dict] = []
    table: dict[str, dict[str, str]] = {}

    for rkey, rlabel in ROWS:
        table[rkey] = {}
        cpu_spikes = load_spike_dir(out / "spikes" / f"{rkey}_cpu")
        for ckey, clabel in COLS:
            log = out / f"{rkey}_{ckey}.log"
            spike_dir = out / "spikes" / f"{rkey}_{ckey}"
            other_spikes = (
                cpu_spikes if ckey == "cpu" else load_spike_dir(spike_dir)
            )
            ident, nspk = identity_vs_cpu(cpu_spikes, other_spikes)
            if ckey == "cpu" and cpu_spikes is not None:
                ident, nspk = "pass", len(cpu_spikes)
            if not log.exists():
                table[rkey][ckey] = "MISS"
                rows_out.append(
                    {
                        "row": rlabel,
                        "engine": ckey,
                        "t0": "",
                        "t1": "",
                        "t2": "",
                        "cell": "MISS",
                        "identity": ident if other_spikes is not None else "miss",
                        "n_spikes": nspk if nspk is not None else "",
                        "log": str(log),
                    }
                )
                continue
            text = log.read_text(errors="replace")
            vals = parse_log(text, ckey)
            cell = fmt_cell(vals)
            table[rkey][ckey] = cell
            rec = {
                "row": rlabel,
                "engine": ckey,
                "t0": vals[0] if vals and len(vals) > 0 else "",
                "t1": vals[1] if vals and len(vals) > 1 else "",
                "t2": vals[2] if vals and len(vals) > 2 else "",
                "cell": cell,
                "identity": ident,
                "n_spikes": nspk if nspk is not None else "",
                "log": log.name,
            }
            rows_out.append(rec)

    csv_path = out / "results.csv"
    fields = ["row", "engine", "t0", "t1", "t2", "cell", "identity", "n_spikes", "log"]
    with csv_path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows_out)

    ident_by = {(r["row"], r["engine"]): r for r in rows_out}

    def ident_mark(rlabel: str, ckey: str) -> str:
        rec = ident_by.get((rlabel, ckey), {})
        ident = rec.get("identity", "")
        nspk = rec.get("n_spikes", "")
        if ident == "pass":
            return f"✅ {nspk}" if nspk != "" else "✅"
        if ident == "fail":
            return f"❌ {nspk}" if nspk != "" else "❌"
        if ident == "n/a":
            return f"➖ {nspk}" if nspk != "" else "➖"
        if ident == "miss":
            return "—"
        return ident or "—"

    lines = [
        "# Performance matrix",
        "",
        stamp.strip(),
        "",
        "Each cell: **cold / warm_min–warm_max** seconds (3 psolves in one process).",
        "NEURON columns: psolve wall. CN columns: CoreNEURON `Solver Time`.",
        "Identity: last-psolve raster vs **CPU of the same config** (exact sorted t,gid).",
        "",
        "| Config | CPU | CN | CN GPU | GPU (native) |",
        "|--------|-----|----|--------|--------------|",
    ]
    for rkey, rlabel in ROWS:
        c = table[rkey]
        lines.append(
            "| {lab} | {cpu} {icpu} | {cn} {icn} | {cng} {icng} | {gpu} {igpu} |".format(
                lab=rlabel,
                cpu=c.get("cpu", ""),
                cn=c.get("cn_cpu", ""),
                cng=c.get("cn_gpu", ""),
                gpu=c.get("gpu", ""),
                icpu=ident_mark(rlabel, "cpu"),
                icn=ident_mark(rlabel, "cn_cpu"),
                icng=ident_mark(rlabel, "cn_gpu"),
                igpu=ident_mark(rlabel, "gpu"),
            )
        )
    lines.append("")
    lines.append(f"Raw CSV: `{csv_path}`")
    text = "\n".join(lines) + "\n"
    print(text)
    (out / "table.md").write_text(text)


if __name__ == "__main__":
    main()
