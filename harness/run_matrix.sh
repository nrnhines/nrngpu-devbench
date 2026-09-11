#!/usr/bin/env bash
# Run 8×4 psolve matrix: throwaway psolve(dt) + 3 stdinit/psolve(tstop) per cell.
# Last-psolve ASCII rasters: $OUT/spikes/<tag>/ (identity vs CPU of the same config).
set -euo pipefail

source ~/neuron/bin/nrnenv nrngpu build-gpu
export OMP_NUM_THREADS=1
export NRN_GPU_PERMUTE="${NRN_GPU_PERMUTE:-2}"
export NRN_MULTI_PSOLVE_N=3

ROOT="$(cd "$(dirname "$0")" && pwd)"
OUT="${PERF_MATRIX_OUT:-/tmp/perf-matrix}"
mkdir -p "$OUT"
STAMP_BRANCH=$(cd ~/neuron/nrngpu && git branch --show-current)
STAMP_COMMIT=$(cd ~/neuron/nrngpu && git rev-parse --short HEAD)
STAMP_DATE=$(date -Iseconds)
echo "branch=$STAMP_BRANCH commit=$STAMP_COMMIT date=$STAMP_DATE" | tee "$OUT/stamp.txt"

# Product workdir: same special + ringtest.py (import-as-module breaks ParallelContext).
RING_WD="${RING_WD:-$HOME/neuron/nrngpu/build-gpu/test/external_ringtest/neuron_gpu_native_mpi}"
RING_SRC="${RING_SRC:-$RING_WD}"
RING_SPECIAL="${RING_SPECIAL:-$RING_WD/x86_64/special}"
export RING_SRC

DENT_CPU_DIR="${DENT_CPU_DIR:-$HOME/neuron/nrngpu/build-gpu/test/reduced_dentate/neuron}"
DENT_CN_DIR="${DENT_CN_DIR:-$HOME/neuron/nrngpu/build-gpu/test/reduced_dentate/coreneuron_gpu}"
DENT_GPU_DIR="${DENT_GPU_DIR:-$HOME/neuron/nrngpu/build-gpu/test/reduced_dentate_native/neuron_gpu_native}"
# Use coreneuron group special for CN (same mech md5 as neuron); native for GPU
DENT_CPU_SPECIAL="$DENT_CPU_DIR/x86_64/special"
DENT_CN_SPECIAL="$DENT_CN_DIR/x86_64/special"
DENT_GPU_SPECIAL="$DENT_GPU_DIR/x86_64/special"

TRAUB_MODEL="${TRAUB_MODEL:-$HOME/models/82894}"
TRAUB_SPECIAL="${TRAUB_SPECIAL:-/tmp/traub-nrngpu-acc/x86_64/special}"
TRAUB_HOC="$ROOT/traub_multi_bench.hoc"

run_one() {
  local tag=$1
  shift
  local log="$OUT/${tag}.log"
  mkdir -p "$OUT/spikes/$tag"
  export NRN_SPIKE_OUT_DIR="$OUT/spikes/$tag"
  echo "=== RUN $tag $(date -Iseconds) ===" | tee -a "$OUT/progress.txt"
  set +e
  # shellcheck disable=SC2068
  "$@" >"$log" 2>&1
  local rc=$?
  set -e
  if [[ $rc -eq 0 ]] && grep -q 'MULTI_PSOLVE_DONE' "$log"; then
    echo "OK $tag" | tee -a "$OUT/progress.txt"
  else
    echo "FAIL $tag (exit $rc)" | tee -a "$OUT/progress.txt"
  fi
}

# --- Ring rows 1-4 ---
ring_run() {
  local tag=$1 nring=$2 nt=$3 eng=$4
  local extra=()
  case "$eng" in
    cpu) ;;
    gpu) extra=(-gpu-native -permute 2) ;;
    cn_cpu) extra=(-coreneuron) ;;
    cn_gpu) extra=(-coreneuron -gpu -permute 2) ;;
    *) echo "bad eng $eng"; return 1 ;;
  esac
  run_one "$tag" env RING_SRC="$RING_SRC" \
    "$RING_SPECIAL" -notatty -python "$ROOT/ring_multi_psolve.py" \
    -nring "$nring" -nt "$nt" -tstop 100 "${extra[@]}"
}

for nt in 1 4; do
  for nring in 16 160; do
    for eng in cpu gpu cn_cpu cn_gpu; do
      ring_run "ring_n${nring}_nt${nt}_${eng}" "$nring" "$nt" "$eng"
    done
  done
done

# --- Dentate rows 5-6 (1 rank) ---
dent_run() {
  local tag=$1 nthread=$2 eng=$3
  local dir special
  case "$eng" in
    cpu)
      dir=$DENT_CPU_DIR; special=$DENT_CPU_SPECIAL
      ;;
    gpu)
      dir=$DENT_GPU_DIR; special=$DENT_GPU_SPECIAL
      ;;
    cn_cpu|cn_gpu)
      dir=$DENT_CN_DIR; special=$DENT_CN_SPECIAL
      ;;
    *) return 1 ;;
  esac
  run_one "$tag" env \
    NRN_DENTATE_ENGINE="$eng" \
    NRN_DENTATE_NTHREAD="$nthread" \
    NRN_TEST_TSTOP=10 \
    NRN_TEST_MAX_CELLS=100 \
    NRN_GPU_PERMUTE=2 \
    HOC_LIBRARY_PATH=templates \
    bash -c "cd \"$dir\" && HOC_LIBRARY_PATH=templates \"$special\" -notatty -python \"$ROOT/dentate_multi_psolve.py\""
}

for nt in 1 4; do
  for eng in cpu gpu cn_cpu cn_gpu; do
    dent_run "dent_nt${nt}_${eng}" "$nt" "$eng"
  done
done

# --- Traub rows 7-8 ---
traub_run() {
  local tag=$1 gap=$2 eng=$3
  local args=(-c "one_tenth_ncell=1" -c "use_gap=${gap}" -c "nthread=1" -c "mytstop=100" -c "benchmark_quiet=1" -c "n_multi_psolve=3")
  case "$eng" in
    cpu) args+=(-c "enable_gpu=0" -c "coreneuron=0" -c "coreneuron_gpu=0") ;;
    gpu) args+=(-c "enable_gpu=1" -c "coreneuron=0" -c "coreneuron_gpu=0") ;;
    cn_cpu) args+=(-c "enable_gpu=0" -c "coreneuron=1" -c "coreneuron_gpu=0") ;;
    cn_gpu) args+=(-c "enable_gpu=0" -c "coreneuron=1" -c "coreneuron_gpu=1") ;;
    *) return 1 ;;
  esac
  run_one "$tag" bash -c "cd \"$TRAUB_MODEL\" && \"$TRAUB_SPECIAL\" ${args[*]} \"$TRAUB_HOC\""
  # spike2file writes out<nhost>.dat in the model cwd; move to the per-tag spike dir.
  if [[ -n "${NRN_SPIKE_OUT_DIR:-}" ]]; then
    # spike2file writes out<nhost>.dat only (not out1_enable_gpu=*.dat leftovers).
    shopt -s nullglob
    for f in "$TRAUB_MODEL"/out[0-9]*.dat; do
      base=$(basename "$f")
      stem=${base%.dat}
      if [[ "$stem" =~ ^out[0-9]+$ && -f "$f" ]]; then
        mv -f "$f" "$NRN_SPIKE_OUT_DIR/$base"
      fi
    done
    shopt -u nullglob
  fi
}

for gap in 0 1; do
  gname=nogap
  [[ "$gap" == 1 ]] && gname=gap
  for eng in cpu gpu cn_cpu cn_gpu; do
    traub_run "traub_${gname}_${eng}" "$gap" "$eng"
  done
done

echo "All launches done. Parsing..." | tee -a "$OUT/progress.txt"
python3 "$ROOT/parse_matrix.py" "$OUT" | tee "$OUT/table.md"
echo "Wrote $OUT/table.md"
