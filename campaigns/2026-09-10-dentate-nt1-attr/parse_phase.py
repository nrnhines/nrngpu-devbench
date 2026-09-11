#!/usr/bin/env python3
"""Parse NRN_NATIVE_GPU_PHASE_TIMER summaries + MULTI_PSOLVE walls.

Nested buckets double-count tracked-total. Print coarse vs psolve, then
absolute nested seconds.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

COARSE = {
    "deliver-events",
    "vecplay-sync",
    "setup-tree-matrix",
    "matrix-sync",
    "matrix-solver",
    "post-solve",
    "download-flush",
    "lastpart",
    "gap-sync",
}

LINE = re.compile(
    r"^\s+(\S+)\s+([0-9.]+)\s+([0-9.]+)%\s+calls=(\d+)\s*$"
)
TRACKED = re.compile(r"^\s+tracked-total\s+([0-9.]+)\s*$")
PSOLVE = re.compile(r"MULTI_PSOLVE i=(\d+) psolve=([0-9.eE+-]+)")
TRAFFIC = re.compile(r"^NRN_GAP_TRAFFIC")


def parse(text: str) -> None:
    psolves = PSOLVE.findall(text)
    print("psolve walls:")
    for i, s in psolves:
        print(f"  i={i}  {float(s):.6f} s")
    print()

    blocks = text.split("NRN_NATIVE_GPU_PHASE_TIMER summary")
    summaries = []
    for block in blocks[1:]:
        rows = {}
        tracked = None
        for line in block.splitlines():
            m = LINE.match(line)
            if m:
                name, sec, pct, calls = m.group(1), float(m.group(2)), float(m.group(3)), int(m.group(4))
                rows[name] = (sec, pct, calls)
                continue
            m = TRACKED.match(line)
            if m:
                tracked = float(m.group(1))
                break
        summaries.append((rows, tracked))

    for idx, (rows, tracked) in enumerate(summaries):
        print(f"=== summary {idx} (psolve i={idx} if 1:1) ===")
        coarse = 0.0
        print(f"{'phase':<22} {'sec':>10} {'%psolve':>8} {'calls':>8}")
        psolve = float(psolves[idx][1]) if idx < len(psolves) else None
        for name, (sec, _pct, calls) in rows.items():
            if name not in COARSE:
                continue
            coarse += sec
            pct_p = 100.0 * sec / psolve if psolve else float("nan")
            print(f"{name:<22} {sec:10.6f} {pct_p:7.1f}% {calls:8d}")
        print(f"{'coarse-sum':<22} {coarse:10.6f}")
        if psolve:
            print(f"{'psolve':<22} {psolve:10.6f}  uncovered={psolve - coarse:.4f}")
        print(f"{'tracked-total':<22} {(tracked or 0):10.6f}  (nested double-count)")
        print("nested (absolute s):")
        for name, (sec, _pct, calls) in rows.items():
            if name in COARSE:
                continue
            print(f"  {name:<28} {sec:10.6f}  calls={calls}")
        print()

    for line in text.splitlines():
        if "gap traffic" in line.lower() or line.startswith("NRN_GAP") or "full_v_pulls" in line or "bulk_mech" in line:
            print(line)


def main() -> None:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "-")
    text = sys.stdin.read() if str(path) == "-" else path.read_text(errors="replace")
    parse(text)


if __name__ == "__main__":
    main()
