"""Load last-psolve ASCII rasters and compare to the CPU cell of the same config."""
from __future__ import annotations

from pathlib import Path

def _is_raster(path: Path) -> bool:
    name = path.name
    if name.endswith(".std") and name.startswith("spk"):
        return True
    if name.startswith("spikeout_") and name.endswith(".dat"):
        return True
    # Traub spike2file: out<nhost>.dat — not out1_enable_gpu=1.dat leftovers.
    if name.startswith("out") and name.endswith(".dat"):
        stem = name[3:-4]
        return stem.isdigit()
    return False


def load_spike_dir(directory: Path) -> list[tuple[float, int]] | None:
    if not directory.is_dir():
        return None
    files = sorted({p for p in directory.iterdir() if p.is_file() and p.stat().st_size > 0 and _is_raster(p)})
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
