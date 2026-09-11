#!/usr/bin/env python3
"""Reduced dentate multi-psolve (1 rank): throwaway psolve(dt), then N stdinit+psolve(tstop).

Launch from a reduced_dentate ctest workdir (datasets + special).

Env:
  NRN_TEST_TSTOP       default 10
  NRN_TEST_MAX_CELLS   default 100
  NRN_DENTATE_NTHREAD  default 1
  NRN_DENTATE_ENGINE   cpu | gpu | cn_cpu | cn_gpu
  NRN_MULTI_PSOLVE_N   default 3
  NRN_GPU_PERMUTE      default 2
"""
from __future__ import annotations

import os
import sys


def main() -> None:
    cwd = os.getcwd()
    if cwd not in sys.path:
        sys.path.insert(0, cwd)

    from neuron import h

    mytstop = float(os.environ.get("NRN_TEST_TSTOP", "10"))
    max_cells = int(os.environ.get("NRN_TEST_MAX_CELLS", "100"))
    nthread = int(os.environ.get("NRN_DENTATE_NTHREAD", "1"))
    engine = os.environ.get("NRN_DENTATE_ENGINE", "cpu").strip().lower()
    nrep = int(os.environ.get("NRN_MULTI_PSOLVE_N", "3"))
    permute = int(os.environ.get("NRN_GPU_PERMUTE", "2"))

    # Pre-set vars before run.hoc default_var (run.hoc uses default_var so -c wins if set early)
    h(f"mytstop = {mytstop}")
    h(f"max_cells_per_type = {max_cells}")
    h("coreneuron = 0")
    h("gpu = 0")

    if engine == "gpu":
        from neuron import gpu

        # Product native path: coreneuron=0 gpu=0 in hoc; enable via neuron.gpu
        gpu.backend = "native"
        gpu.permute = permute
        gpu.enable = True
    elif engine == "cn_cpu":
        h("coreneuron = 1")
        h("gpu = 0")
    elif engine == "cn_gpu":
        h("coreneuron = 1")
        h("gpu = 1")
    elif engine != "cpu":
        raise SystemExit(f"unknown NRN_DENTATE_ENGINE={engine!r}")

    # Write a thin run_multi.hoc: run.hoc setup + nthread + main with multi prun.
    # Avoid rewriting main.hoc body; append multi after loading by replacing only
    # the final prun() invocation via a small wrapper main.
    run_hoc = os.path.join(cwd, "run.hoc")
    main_hoc = os.path.join(cwd, "main.hoc")
    if not os.path.isfile(run_hoc) or not os.path.isfile(main_hoc):
        raise SystemExit(f"need run.hoc and main.hoc in {cwd}")

    with open(main_hoc, "r", encoding="utf-8", errors="replace") as f:
        main_src = f.read()
    if "\nprun()\n" not in main_src:
        raise SystemExit("top-level prun() not found in main.hoc")

    head, _, _ = main_src.rpartition("\nprun()\n")
    spike_dir = os.environ.get("NRN_SPIKE_OUT_DIR", os.path.join(cwd, "_perf_spikes"))
    os.makedirs(spike_dir, exist_ok=True)
    spike_dir_hoc = spike_dir.replace("\\", "\\\\").replace('"', '\\"')
    # Throwaway psolve(dt) pays first-process copyin/mk_mech; then nrep full
    # stdinit+psolve(tstop). Last-psolve raster only.
    multi_tail = f"""
// multi-psolve: setup = psolve(dt) after the stdinit already done above;
// then nrep warms each starting with stdinit.
strdef spikeout_fname
proc multi_prun() {{ local i, tsav
  if (use_coreneuron) {{
    nrnpython("from neuron import coreneuron")
    nrnpython("coreneuron.enable = True")
    if (use_gpu) {{
      nrnpython("coreneuron.gpu = True")
    }} else {{
      nrnpython("coreneuron.gpu = False")
    }}
  }}
  tsav = startsw()
  pnm.pc.psolve(dt)
  if (pnm.pc.id == 0) {{
    printf("MULTI_PSOLVE setup psolve=%g\\n", startsw() - tsav)
  }}
  for i = 0, {nrep - 1} {{
    stdinit()
    if (i == {nrep - 1}) {{
      pnm.spikevec.resize(0)
      pnm.idvec.resize(0)
    }}
    if (use_coreneuron) {{
      pnm.pc.psolve(tstop)
      if (pnm.pc.id == 0) {{
        printf("MULTI_PSOLVE i=%d psolve_wall_mark=1\\n", i)
      }}
    }} else {{
      tsav = startsw()
      pnm.pc.psolve(tstop)
      if (pnm.pc.id == 0) {{
        printf("MULTI_PSOLVE i=%d psolve=%g\\n", i, startsw() - tsav)
      }}
    }}
  }}
  sprint(spikeout_fname, "{spike_dir_hoc}/spikeout_%d.dat", pnm.myid)
  spikeout(spikeout_fname, pnm.spikevec, pnm.idvec)
  if (pnm.pc.id == 0) {{
    printf("MULTI_PSOLVE_DONE n=%d engine=%s nthread=%d\\n", {nrep}, "{engine}", {nthread})
    printf("IDENTITY_N=%d dir={spike_dir_hoc}\\n", pnm.spikevec.size)
  }}
}}
multi_prun()
"""
    multi_main = head + "\n" + multi_tail
    # nthread after ParallelNetManager exists (no global pc before pnm).
    if nthread > 1:
        needle = "pnm = new ParallelNetManager(ncells)"
        if needle not in multi_main:
            raise SystemExit("could not find ParallelNetManager construction for nthread")
        multi_main = multi_main.replace(
            needle,
            needle
            + f"\npnm.pc.nthread({nthread})"
            + f'\nprintf("Info: pnm.pc.nthread(%d)\\n", {nthread})\n',
            1,
        )
    multi_main_path = os.path.join(cwd, "_perf_main_multi.hoc")
    with open(multi_main_path, "w", encoding="utf-8") as f:
        f.write(multi_main)

    # run.hoc clone + multi main
    wrapper = f"""
{{load_file("defvar.hoc")}}
strdef parameters
parameters="./parameters/Control.hoc"

default_var("coredat", "coredat")
default_var("outdir", ".")
default_var("mytstop", {mytstop})
default_var("coreneuron", 0)
default_var("gpu", 0)
default_var("dumpmodel", 0)
default_var("max_cells_per_type", {max_cells})

use_coreneuron = coreneuron
use_gpu = gpu
dump_coreneuron_model = dumpmodel
max_cells_per_type_to_load = max_cells_per_type

{{
    outdir = getcwd()
    sprint(coredat, "%s/%s", outdir, coredat)
    nrnpython("from commonutils import mkdir_p")
    strdef cmd
    sprint(cmd, "mkdir_p('%s')", coredat)
    nrnpython(cmd)
    sprint(cmd, "mkdir_p('%s/results')", outdir)
    nrnpython(cmd)
}}

load_file("_perf_main_multi.hoc")
"""
    wrap_path = os.path.join(cwd, "_perf_run_multi.hoc")
    with open(wrap_path, "w", encoding="utf-8") as f:
        f.write(wrapper)

    # Ensure coreneuron/gpu hoc flags match engine (default_var won't override if set)
    if engine == "cn_cpu":
        h("coreneuron = 1")
        h("gpu = 0")
    elif engine == "cn_gpu":
        h("coreneuron = 1")
        h("gpu = 1")

    h.load_file("_perf_run_multi.hoc")
    print("MULTI_PSOLVE_EXIT_OK", flush=True)


if __name__ == "__main__":
    main()
