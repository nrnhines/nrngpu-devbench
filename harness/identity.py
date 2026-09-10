"""Load last-psolve ASCII rasters and compare to the CPU cell of the same config."""
from __future__ import annotations

from pathlib import Path

_GLOBS = ("*.std", "*.dat", "spk*", "out*", "*spike*")


def load_spike_dir(directory: Path) -> list[tuple[float, int]] | None:
    if not directory.is_dir():
        return None
    files: list[Path] = []
    for pat in _GLOBS:
        files.extend(directory.glob(pat))
    files = sorted({p for p in files if p.is_file() and p.stat().st_size > 0})
    if not files:
        return None
    spikes: list[tuple[float, int]] = []
    for path in files:
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


def identity_vs_cpu(
    cpu: list[tuple[float, int]] | None,
    other: list[tuple[float, int]] | None,
) -> tuple[str, int | None]:
    """Return (identity, n_spikes). identity is pass/fail/n/a/miss."""
    if other is None:
        return "miss", None
    n = len(other)
    if cpu is None:
        return "n/a", n
    return ("pass" if other == cpu else "fail"), n
