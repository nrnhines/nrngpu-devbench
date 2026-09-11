#!/usr/bin/env bash
# Traub 1/10 CN-vs-CPU prcellstate harness (spikes first, then dumps).
#
# Campaign fact (2026-09-11-psolve-setup-warm): Traub gap CN 7867 is CPU 7873
# with six extra CPU spikes at t=99.975, gids 47 51 153 266 276 347. No-gap is
# exact 4474 including t=99.975. Default --gid 47 is the first extra.
#
# Usage (exclusive GPU if an engine uses it):
#   source ~/neuron/bin/nrnenv nrngpu build-gpu
#   bash ~/neuron/devbench/harness/traub_prcs.sh
#   bash ~/neuron/devbench/harness/traub_prcs.sh --tstop 99.95 --gid 47
#   bash ~/neuron/devbench/harness/traub_prcs.sh --engines cpu,cn_gpu --gid 47
#
# Env: NRN_TRAUB_MODEL, TRAUB_SPECIAL, TRAUB_PRCS_OUT
set -euo pipefail

source ~/neuron/bin/nrnenv nrngpu build-gpu
export OMP_NUM_THREADS="${OMP_NUM_THREADS:-1}"
export NRN_GPU_PERMUTE="${NRN_GPU_PERMUTE:-2}"
export NRN_GPU_BACKEND_TEST="${NRN_GPU_BACKEND_TEST:-native}"

ROOT="$(cd "$(dirname "$0")" && pwd)"
MODEL="${NRN_TRAUB_MODEL:-$HOME/models/82894}"
SPECIAL="${TRAUB_SPECIAL:-/tmp/traub-nrngpu-acc/x86_64/special}"
HOC="$ROOT/traub_prcs.hoc"
OUT="${TRAUB_PRCS_OUT:-/tmp/traub-prcs}"

GAP=1
GID=47
TSTOP=100
STEPS_PER_MS=40
ENGINES="cpu,cn_cpu,cn_gpu"
DUMP_T0=1
CHECKPOINT_T=""

usage() {
  sed -n '2,16p' "$0"
  exit 0
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --gap) GAP="$2"; shift 2 ;;
    --no-gap) GAP=0; shift ;;
    --gid) GID="$2"; shift 2 ;;
    --tstop) TSTOP="$2"; shift 2 ;;
    --steps-per-ms) STEPS_PER_MS="$2"; shift 2 ;;
    --engines) ENGINES="$2"; shift 2 ;;
    --no-t0) DUMP_T0=0; shift ;;
    --checkpoint-t) CHECKPOINT_T="$2"; shift 2 ;;
    --out) OUT="$2"; shift 2 ;;
    -h|--help) usage ;;
    *) echo "unknown arg: $1" >&2; exit 2 ;;
  esac
done

if [[ ! -x "$SPECIAL" ]]; then
  echo "ERROR: Traub special missing: $SPECIAL (run test/external/traub/run_traub_native.sh --rebuild)" >&2
  exit 1
fi
if [[ ! -d "$MODEL" || ! -f "$HOC" ]]; then
  echo "ERROR: need model $MODEL and $HOC" >&2
  exit 1
fi

mkdir -p "$OUT"
echo "out=$OUT gap=$GAP gid=$GID tstop=$TSTOP steps_per_ms=$STEPS_PER_MS engines=$ENGINES" | tee "$OUT/stamp.txt"
git -C "$HOME/neuron/nrngpu" rev-parse --short HEAD >>"$OUT/stamp.txt" || true

run_eng() {
  local eng=$1
  local dir="$OUT/$eng"
  mkdir -p "$dir"
  local args=(-c "one_tenth_ncell=1" -c "use_gap=${GAP}" -c "nthread=1" -c "mytstop=${TSTOP}"
    -c "prcs_steps_per_ms=${STEPS_PER_MS}"
    -c "benchmark_quiet=1" -c "prcellstate_gid=${GID}" -c "prcellstate_dump_t0=${DUMP_T0}")
  case "$eng" in
    cpu) args+=(-c "enable_gpu=0" -c "coreneuron=0" -c "coreneuron_gpu=0") ;;
    gpu) args+=(-c "enable_gpu=1" -c "coreneuron=0" -c "coreneuron_gpu=0") ;;
    cn_cpu) args+=(-c "enable_gpu=0" -c "coreneuron=1" -c "coreneuron_gpu=0") ;;
    cn_gpu) args+=(-c "enable_gpu=0" -c "coreneuron=1" -c "coreneuron_gpu=1") ;;
    *) echo "bad engine $eng" >&2; return 1 ;;
  esac
  if [[ -n "$CHECKPOINT_T" ]]; then
    args+=(-c "prcellstate_checkpoint_t=${CHECKPOINT_T}")
  fi
  echo "=== RUN $eng $(date -Iseconds) ===" | tee -a "$OUT/progress.txt"
  (
    cd "$MODEL"
    rm -f out[0-9]*.dat ./*.nrndat ./*.corenrn 2>/dev/null || true
    "$SPECIAL" -notatty "${args[@]}" "$HOC"
  ) >"$dir/run.log" 2>&1
  # Collect raster + dumps from model cwd (spike2file / prcellstate / CN --prcellgid).
  shopt -s nullglob
  for f in "$MODEL"/out[0-9]*.dat "$MODEL"/*.nrndat "$MODEL"/*.corenrn; do
    [[ -f "$f" ]] || continue
    mv -f "$f" "$dir/"
  done
  shopt -u nullglob
  if grep -q 'PRCS_DONE' "$dir/run.log"; then
    echo "OK $eng" | tee -a "$OUT/progress.txt"
  else
    echo "FAIL $eng" | tee -a "$OUT/progress.txt"
    tail -40 "$dir/run.log" || true
    return 1
  fi
}

IFS=',' read -r -a eng_arr <<<"$ENGINES"
for eng in "${eng_arr[@]}"; do
  eng=$(echo "$eng" | tr -d ' ')
  [[ -n "$eng" ]] || continue
  run_eng "$eng"
done

echo "=== spikes-first ===" | tee "$OUT/diff.txt"
if [[ -d "$OUT/cpu" && -d "$OUT/cn_cpu" ]]; then
  python3 "$ROOT/diff_rasters.py" "$OUT/cpu" "$OUT/cn_cpu" | tee -a "$OUT/diff.txt" || true
fi
if [[ -d "$OUT/cpu" && -d "$OUT/cn_gpu" ]]; then
  python3 "$ROOT/diff_rasters.py" "$OUT/cpu" "$OUT/cn_gpu" | tee -a "$OUT/diff.txt" || true
fi
if [[ -d "$OUT/cpu" && -d "$OUT/gpu" ]]; then
  python3 "$ROOT/diff_rasters.py" "$OUT/cpu" "$OUT/gpu" | tee -a "$OUT/diff.txt" || true
fi

echo "=== dumps in $OUT ==="
find "$OUT" -type f \( -name '*.nrndat' -o -name '*.corenrn' -o -name 'out*.dat' \) | sort
echo "Done. rdcellstate from $OUT, e.g.:"
echo "  cd $OUT && python -m neuron.debug.rdcellstate cpu/<gid>_nrn000_t${TSTOP}.nrndat cn_gpu/<gid>_acc_gpu_t….corenrn --ignore-unused --top 25"
