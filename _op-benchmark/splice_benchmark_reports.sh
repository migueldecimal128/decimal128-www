#!/bin/bash
# =============================================================================
#  splice_benchmark_reports.sh  —  STAGE B: regenerate reports from the store.
# =============================================================================
#  Reads ONLY the JSONL store (results.*.jsonl / runs.*.jsonl) and rewrites the
#  generated tables inside the www report pages, in place, leaving hand-written
#  prose untouched. Then verifies every generated block matches the store.
#
#  This stage NEVER runs a benchmark and NEVER invokes an emit_<lang>.py.
#  Producing new numbers is the SEPARATE store-only stage
#  (./update_benchmark_stores.sh). Crossing this boundary is a defect.
#  See ArchSplitStoreWorkOrder.md.
#
#  Pages handled:
#    ../benchmark-*.md              (gen_bench.py)             — the per-port + compare reports
#    ../reviews/dotnet/net11-preview7.md  (gen_bench_net11_preview7.py) — the .NET 11 review edition
#
#  This edits working-tree .md files only. Committing/publishing is a separate,
#  explicit human step.
# =============================================================================
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE"

NET11_PAGE="../reviews/dotnet/net11-preview7.md"

echo "===== splice: benchmark-*.md (gen_bench.py) ====="
for f in ../benchmark-*.md; do
  if grep -q 'BEGIN GENERATED' "$f"; then
    echo "  splicing $f"
    python3 gen_bench.py --splice "$f"
  fi
done

if [ -f "$NET11_PAGE" ] && grep -q 'BEGIN GENERATED' "$NET11_PAGE"; then
  echo "===== splice: $NET11_PAGE (gen_bench_net11_preview7.py) ====="
  python3 gen_bench_net11_preview7.py --splice "$NET11_PAGE"
fi

echo "===== verify (every block must be [OK]; any [DIFF] fails) ====="
diffs=0
for f in ../benchmark-*.md; do
  if grep -q 'BEGIN GENERATED' "$f"; then
    out="$(python3 gen_bench.py --check "$f" 2>&1)"
    echo "$out" | grep '\[DIFF\]' && diffs=1
  fi
done
if [ -f "$NET11_PAGE" ] && grep -q 'BEGIN GENERATED' "$NET11_PAGE"; then
  out="$(python3 gen_bench_net11_preview7.py --check "$NET11_PAGE" 2>&1)"
  echo "$out" | grep '\[DIFF\]' && diffs=1
fi

if [ "$diffs" -eq 0 ]; then
  echo "all generated blocks in sync with the store [OK]"
else
  echo "!! DIFF remained after splice — investigate"; exit 1
fi
echo
echo ">>> Report pages regenerated. Review 'git status'/'git diff', then commit if desired."
