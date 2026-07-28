#!/bin/bash
# =============================================================================
#  update_benchmark_stores.sh  —  STAGE A: run the benchmarks, update the store.
# =============================================================================
#  This is a STORE-ONLY stage. It runs each port's emit_<lang>.py SERIALLY
#  (concurrent benches contaminate ns/op) and writes ONLY the arch-split JSONL
#  store for THIS box's architecture:
#       results.<lang>.<arch>.jsonl   +   runs.<arch>.jsonl
#
#  It NEVER splices a report page. Regenerating the www benchmark-*.md pages is
#  a SEPARATE stage — run ./splice_benchmark_reports.sh for that. Crossing this
#  boundary (splicing from here, or benchmarking from the splice script) is a
#  defect. See ArchSplitStoreWorkOrder.md.
#
#  Arch is auto-detected: arm64 mints R* run-ids, x86_64 mints xR* — so the two
#  boxes write disjoint files and never clobber each other.
#
#  Usage:
#    ./update_benchmark_stores.sh                 # all 9 ports, serial
#    ./update_benchmark_stores.sh rust zig        # a subset, serial
#    ./update_benchmark_stores.sh csharp --profiles P-fin   # one port + passthrough
#                                                 # (surgical single-profile re-run)
# =============================================================================
set -u

# Hold a power assertion for the whole sweep. An unattended run on a laptop can
# otherwise idle-sleep mid-benchmark, and the cost is not just wall time: the
# throttled window around sleep/wake inflates whatever is running. Seen
# 2026-07-28 -- a go run slept 292s on battery and came back with three control
# rows uniformly 1.76x their true value, while every other port that day sat
# within normal drift.
#
# Caveat: this stops IDLE sleep. It cannot stop lid-close (clamshell) sleep --
# leave the lid open for an unattended sweep.
#
# Re-exec self under caffeinate once; D128_CAFFEINATED makes that idempotent.
if [ -z "${D128_CAFFEINATED:-}" ] && command -v caffeinate >/dev/null 2>&1; then
  export D128_CAFFEINATED=1
  exec caffeinate -dimsu "$0" "$@"
fi

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE"

MACH="$(uname -m)"
case "$MACH" in
  arm64|aarch64) ARCH=arm64;  PFX="" ;;
  x86_64|amd64)  ARCH=x86_64; PFX="x" ;;
  *) echo "unknown arch '$MACH'"; exit 2 ;;
esac

CBIN="${CBIN:-$HOME/decimal128/c/build-bench/benchmark/bench_libbid_vs_d128}"
CMINTIME="${CMINTIME:-0.5s}"
LOG="${LOG:-${TMPDIR:-/tmp}/decimal128_bench_logs}"; mkdir -p "$LOG"

ALL=(c rust zig swift go python java kotlin csharp)

# run-id base per port (arm64 form); the x86 box gets the same id with an 'x' prefix.
runid() { case "$1" in
  c) echo Rc2;; rust) echo Rrsw2;; zig) echo Rzgsw2;; swift) echo Rswsw2;;
  go) echo Rgosw2;; python) echo Rpysw2;; java) echo Rjasw2;; kotlin) echo Rkosw2;;
  csharp) echo Rcs11;; esac; }

# the emit invocation for one port (extra pass-through args in $2..)
emit_cmd() {
  local p="$1"; shift
  local rid="${PFX}$(runid "$p")"
  case "$p" in
    c)      echo python3 emit_c.py "$CBIN" --run-id "$rid" --min-time "$CMINTIME" "$@" ;;
    rust)   echo python3 emit_rust.py   --run-id "$rid" "$@" ;;
    zig)    echo python3 emit_zig.py    --run-id "$rid" "$@" ;;
    swift)  echo python3 emit_swift.py  --run-id "$rid" "$@" ;;
    go)     echo python3 emit_go.py     --run-id "$rid" "$@" ;;
    python) echo python3 emit_python.py --run-id "$rid" "$@" ;;
    java)   echo python3 emit_java.py   --run-id "$rid" "$@" ;;
    kotlin) echo python3 emit_kotlin.py --run-id "$rid" "$@" ;;
    csharp) echo python3 emit_csharp.py --run-id "$rid" "$@" ;;
  esac
}

is_port() { local x="$1" p; for p in "${ALL[@]}"; do [ "$p" = "$x" ] && return 0; done; return 1; }

# Argument parsing:
#  - "port extra args..."  → one port with pass-through (if 1st arg is a port and more follow)
#  - "port [port ...]"     → subset, no pass-through
#  - (none)                → all ports
PASSTHRU=()
if [ "$#" -ge 1 ] && is_port "$1"; then
  FIRST="$1"; shift
  if [ "$#" -ge 1 ] && ! is_port "$1"; then PORTS=("$FIRST"); PASSTHRU=("$@")
  else PORTS=("$FIRST" "$@"); fi
elif [ "$#" -ge 1 ]; then
  echo "unknown port '$1' (valid: ${ALL[*]})"; exit 2
else
  PORTS=("${ALL[@]}")
fi

if printf '%s\n' "${PORTS[@]}" | grep -qx c; then
  # emit_c.py rebuilds CBIN from its CMake tree before benching; it only needs
  # the build dir configured once (ThinLTO). A missing path here means no tree.
  [ -e "$CBIN" ] || { echo "C bench binary path not found: $CBIN"; echo "configure the build dir once (ThinLTO), or set CBIN=..."; exit 2; }
fi

echo "===== update_benchmark_stores  arch=$ARCH  ports: ${PORTS[*]}  ($(date)) ====="
echo "logs: $LOG"
: > "$LOG/status.txt"
fail=0
for p in "${PORTS[@]}"; do
  cmd="$(emit_cmd "$p" ${PASSTHRU[@]+"${PASSTHRU[@]}"})"
  t0=$(date +%s)
  echo "[$(date '+%H:%M:%S')] START  $p   ($cmd)"
  eval "$cmd" >"$LOG/$p.log" 2>&1; rc=$?
  echo "[$(date '+%H:%M:%S')] DONE   $p   rc=$rc  ($(( $(date +%s)-t0 ))s)"
  echo "$p rc=$rc" >> "$LOG/status.txt"
  [ $rc -eq 0 ] || fail=1
done

echo "===== stores updated ($ARCH). status: ====="
cat "$LOG/status.txt"
echo
echo ">>> Reports were NOT regenerated. To publish, run:  ./splice_benchmark_reports.sh"
exit $fail
