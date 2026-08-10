# Matrix harness (timing)

Imported from `~/neuron/notes/perf_matrix/` (scripts only; not the 2026-08-05 results).

```bash
bash ~/neuron/devbench/harness/run_matrix.sh
python3 ~/neuron/devbench/harness/parse_matrix.py /tmp/perf-matrix
```

Requires product build via `nrnenv nrngpu build-gpu` and Traub model/special paths as in `run_matrix.sh`.

**Identity:** these scripts are **timing-only**. Campaign identity fields are plan **2.4.2+** / `../schema.md`.
