#!/usr/bin/env python3
"""Parse /tmp/perf-matrix/*.log into cold | warm_min-warm_max table + CSV."""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

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
COLS = [("cpu", "CPU"), ("gpu", "GPU"), ("cn_cpu", "CN CPU"), ("cn_gpu", "CN GPU")]


def main() -> None:
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/perf-matrix")
    stamp = (out / "stamp.txt").read_text() if (out / "stamp.txt").exists() else ""
    rows_out: list[dict] = []
    table: dict[str, dict[str, str]] = {}

    for rkey, rlabel in ROWS:
        table[rkey] = {}
        for ckey, clabel in COLS:
            log = out / f"{rkey}_{ckey}.log"
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
                "log": log.name,
            }
            rows_out.append(rec)

    csv_path = out / "results.csv"
    with csv_path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["row", "engine", "t0", "t1", "t2", "cell", "log"])
        w.writeheader()
        w.writerows(rows_out)

    lines = [
        f"# Performance matrix",
        "",
        stamp.strip(),
        "",
        "Each cell: **cold / warm_min–warm_max** seconds (3 psolves in one process).",
        "NEURON columns: psolve wall. CN columns: CoreNEURON `Solver Time`.",
        "",
        "| Config | CPU | GPU | CN CPU | CN GPU |",
        "|--------|-----|-----|--------|--------|",
    ]
    for rkey, rlabel in ROWS:
        c = table[rkey]
        lines.append(
            f"| {rlabel} | {c.get('cpu','')} | {c.get('gpu','')} | {c.get('cn_cpu','')} | {c.get('cn_gpu','')} |"
        )
    lines.append("")
    lines.append(f"Raw CSV: `{csv_path}`")
    text = "\n".join(lines) + "\n"
    print(text)
    (out / "table.md").write_text(text)


if __name__ == "__main__":
    main()
