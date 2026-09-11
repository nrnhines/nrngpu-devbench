#!/usr/bin/env python3
"""Spikes-first compare of two Traub/ring/dentate ASCII rasters.

Prints counts, first sorted mismatch, and the (t, gid) leftovers on each side.
Does not require a GPU. Typical first step for CN Traub 7867 vs CPU 7873.

  python3 diff_rasters.py a.dat b.dat
  python3 diff_rasters.py dir_a/ dir_b/
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from identity import load_spike_dir, _is_raster  # noqa: E402


def load_spikes(path: Path) -> list[tuple[float, int]]:
    if path.is_dir():
        rows = load_spike_dir(path)
        if rows is not None:
            return rows
        # Empty out*.dat is a real raster (short tstop, zero spikes), not "missing".
        if any(p.is_file() and _is_raster(p) for p in path.iterdir()):
            return []
        raise SystemExit(f"no raster in directory {path}")
    if not path.is_file():
        raise SystemExit(f"not a file or directory: {path}")
    if not _is_raster(path) and path.suffix not in {".dat", ".std", ".srt"}:
        # still try: campaign leftovers / sortspike output
        pass
    spikes: list[tuple[float, int]] = []
    for line in path.read_text(errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        spikes.append((float(parts[0]), int(float(parts[1]))))
    spikes.sort()
    return spikes


def report(name_a: str, a: list[tuple[float, int]], name_b: str, b: list[tuple[float, int]]) -> int:
    ca, cb = Counter(a), Counter(b)
    only_a = ca - cb
    only_b = cb - ca
    print(f"{name_a}: n={len(a)}")
    print(f"{name_b}: n={len(b)}")
    print(f"multiset_equal={ca == cb}")
    n = min(len(a), len(b))
    first_i = None
    for i in range(n):
        if a[i] != b[i]:
            first_i = i
            print(f"first_sorted_mismatch i={i} {name_a}={a[i]} {name_b}={b[i]}")
            break
    if first_i is None and len(a) != len(b):
        extra = a[n] if len(a) > n else b[n]
        which = name_a if len(a) > n else name_b
        print(f"first_sorted_mismatch i={n} extra_on={which} spike={extra}")
    print(f"only_{name_a} n={sum(only_a.values())} unique={len(only_a)}")
    items_a = sorted(only_a.elements())
    for t, g in items_a:
        print(f"  t={t:.9g} gid={g}")
    if items_a:
        print(f"  gids={sorted({g for _, g in items_a})}")
        print(f"  t_min={items_a[0][0]:.9g} t_max={items_a[-1][0]:.9g}")
    print(f"only_{name_b} n={sum(only_b.values())} unique={len(only_b)}")
    items_b = sorted(only_b.elements())
    for t, g in items_b:
        print(f"  t={t:.9g} gid={g}")
    if items_b:
        print(f"  gids={sorted({g for _, g in items_b})}")
        print(f"  t_min={items_b[0][0]:.9g} t_max={items_b[-1][0]:.9g}")
    return 0 if ca == cb else 1


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    pa, pb = Path(sys.argv[1]), Path(sys.argv[2])
    a = load_spikes(pa)
    b = load_spikes(pb)
    return report(str(pa), a, str(pb), b)


if __name__ == "__main__":
    sys.exit(main())
