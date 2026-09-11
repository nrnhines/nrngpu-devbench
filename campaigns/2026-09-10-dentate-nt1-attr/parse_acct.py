#!/usr/bin/env python3
"""Summarize NVCOMPILER_ACC_TIME kernel tables.

Prints top kernels by elapsed total, plus copyin tax and nrn_cur_/nrn_state_ sums.
ACC_TIME inflates wall — divide totals by n_psolve (default 3) for per-psolve.
"""
from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

# "elapsed time(us): total=123 avg=4.5 ..."
ELAPSED = re.compile(
    r"elapsed time\(us\):\s+total=([0-9.]+)\s+max=[0-9.]+\s+min=[0-9.]+\s+avg=([0-9.]+)"
)
# "data copies: memcpy ..." or "time(us): 123" under copyin
COPY = re.compile(r"time\(us\):\s+([0-9.]+)")
FUNC = re.compile(r"^\s{2}(\S+)\s+NVIDIA")
REGION = re.compile(r"compute region reached\s+(\d+)\s+times")


def parse(text: str, n_psolve: int = 3) -> None:
    lines = text.splitlines()
    kernels = []  # (name, calls, total_us, avg_us)
    i = 0
    while i < len(lines):
        m = FUNC.match(lines[i])
        if not m:
            i += 1
            continue
        name = m.group(1)
        total = avg = None
        calls = None
        copy_us = 0.0
        for j in range(i + 1, min(i + 40, len(lines))):
            if FUNC.match(lines[j]) and j > i:
                break
            rm = REGION.search(lines[j])
            if rm:
                calls = int(rm.group(1))
            em = ELAPSED.search(lines[j])
            if em:
                total = float(em.group(1))
                avg = float(em.group(2))
            if "copyin" in lines[j].lower() or "data copies" in lines[j].lower():
                cm = COPY.search(lines[j])
                if cm:
                    copy_us += float(cm.group(1))
        if total is not None:
            kernels.append((name, calls or 0, total, avg or 0.0, copy_us))
        i += 1

    if not kernels:
        print("no ACC_TIME kernel tables found")
        return

    kernels.sort(key=lambda r: -r[2])
    print(f"n_kernels={len(kernels)}  n_psolve={n_psolve} (totals / n_psolve = per-psolve s)")
    print(f"{'kernel':<40} {'calls':>8} {'avg_us':>10} {'total_s':>10} {'per_ps_s':>10} {'copy_s':>8}")
    cur = sta = jac = nrb = other = copy = 0.0
    for name, calls, total, avg, copy_us in kernels:
        tot_s = total / 1e6
        per = tot_s / n_psolve
        copy_s = copy_us / 1e6
        copy += copy_s
        low = name.lower()
        if "nrn_cur" in low or low.startswith("nrn_current"):
            cur += tot_s
        elif "nrn_state" in low:
            sta += tot_s
        elif "nrn_jacob" in low:
            jac += tot_s
        elif "net_buf" in low or "net_receive" in low:
            nrb += tot_s
        else:
            other += tot_s
        if tot_s >= 0.005 or copy_s >= 0.005:
            print(f"{name:<40} {calls:8d} {avg:10.1f} {tot_s:10.4f} {per:10.4f} {copy_s:8.4f}")

    print()
    print("sums (process total s / per-psolve s):")
    for label, v in (
        ("nrn_state_*", sta),
        ("nrn_cur_*", cur),
        ("nrn_jacob_*", jac),
        ("net_buf/receive", nrb),
        ("other kernels", other),
        ("all kernels", sta + cur + jac + nrb + other),
        ("listed copyin tax", copy),
    ):
        print(f"  {label:<20} {v:8.4f} / {v / n_psolve:8.4f}")


def main() -> None:
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    path = Path(sys.argv[1])
    parse(path.read_text(errors="replace"), n)


if __name__ == "__main__":
    main()
