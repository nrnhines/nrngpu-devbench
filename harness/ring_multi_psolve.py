#!/usr/bin/env python3
"""Ringtest multi-psolve: run ringtest.py as __main__ with 3× prun.

Must not *import* ringtest as a module — that can create a second ParallelContext
and fail native qualification (\"no active threads with nodes\").

CLI: same as ringtest.py after this script name.
"""
from __future__ import annotations

import os
import sys

RING_SRC = os.environ.get(
    "RING_SRC",
    os.path.expanduser("~/neuron/nrngpu/external/tests/ringtest"),
)
os.chdir(RING_SRC)
if RING_SRC not in sys.path:
    sys.path.insert(0, RING_SRC)

nrep = int(os.environ.get("NRN_MULTI_PSOLVE_N", "3"))
src_path = os.path.join(RING_SRC, "ringtest.py")
with open(src_path, "r", encoding="utf-8") as f:
    src = f.read()

old = """if __name__ == '__main__':

    model = create_rings()

    ## Run Simulation ##
    runsim()

    ## Write spike raster ##
    spikeout(".")

    h.quit()
"""

new = f"""if __name__ == '__main__':

    import os
    import commonutils as _cu

    model = create_rings()

    ## Multi-psolve (cold = i0, warm = i1..i2); last-psolve raster only ##
    arm_prcellstate_checkpoint()
    _spike_dir = os.environ.get("NRN_SPIKE_OUT_DIR", ".")
    os.makedirs(_spike_dir, exist_ok=True)
    for _i in range({nrep}):
        if _i > 0:
            h.stdinit()
        if _i == {nrep} - 1:
            _cu.tvec.resize(0)
            _cu.idvec.resize(0)
        runtime, load_balance, avg_comp_time, spk_time, gap_time = prun(tstop)
        pc.barrier()
        if settings.rank == 0:
            print(
                "MULTI_PSOLVE i=%d runtime=%g load_balance=%.1f%% avg_comp_time=%g"
                % (_i, runtime, load_balance * 100, avg_comp_time),
                flush=True,
            )
    spikeout(_spike_dir)
    if settings.rank == 0:
        print("MULTI_PSOLVE_DONE n={nrep}", flush=True)
        print(
            "IDENTITY_N=%d dir=%s"
            % (int(pc.allreduce(_cu.tvec.size(), 1)), _spike_dir),
            flush=True,
        )

    h.quit()
"""

if old not in src:
    # tolerate double-quote style
    old2 = old.replace("'", '"')
    if old2 in src:
        old = old2
    else:
        sys.stderr.write("ring_multi_psolve: could not patch ringtest.py main block\n")
        sys.exit(2)

src = src.replace(old, new, 1)

# ringtest parses sys.argv at load; drop this script name's directory noise —
# argv is already [this_script, ...flags] which parse_known_args accepts.
g = {"__name__": "__main__", "__file__": src_path}
exec(compile(src, src_path, "exec"), g)
