# baselines/ — frozen benchmark snapshots

A baseline is a one-time copy of a `results.<lang>.<arch>.jsonl` store file, frozen
at a declared engine commit so future perf work has a fixed comparison point. The
live store files upsert-by-key on every emit — they always show the *current* state
of an arm; a baseline never changes after it is written.

Naming: `<lang>.baseline.<arch>.jsonl` (e.g. `csharp-bid.baseline.arm64.jsonl`).

Rules:
- **No emitter writes here.** A baseline is created by hand-copying the live results
  file once, immediately after the run that is declared the baseline.
- This directory deliberately does NOT match the `results.*.jsonl` glob that
  `gen_bench.load_results()` uses — baselines are never loaded into reports. Keep it
  that way: never name a file here `results.*`.
- The run record in `runs.<arch>.jsonl` (run id + `port_commit` + os_toolchain) is
  the provenance for a baseline; the baseline file's `run` fields point at it.
- To measure an enhancement: re-emit the live file, then diff it against the
  baseline per cell. Git history additionally archives every store state, but the
  frozen file is the working artifact.

Current baselines:
- `csharp-ubd.baseline.x86_64.jsonl` — run `xRcsubd1` (2026-07-30, 52 cells),
  decimal128-csharp-migration at the seed commit `cca61bb` = decimal128-csharp
  @ `9c66a99`: **UBD representation, AggressiveInlining still present** — the
  true "before" for the whole BID migration, the zero that `csharp-bid` rows are
  measured against. Verified byte-identical `src/` AND `benchmark/` to the
  shipping csharp port at `9c66a99`.
  - **The rows carry `lang: "csharp-bid"`** because `emit_csharp_bid.py` hardcodes
    that field. They are UBD measurements despite the label. Copied verbatim rather
    than hand-edited; harmless because `baselines/` is outside the `results.*.jsonl`
    glob and is never loaded into a report.
  - **Why this baseline exists rather than reusing `results.csharp.x86_64.jsonl`:**
    the shipping-csharp rows (`xRcs11`) were measured ~36 h earlier, and identical
    code re-measured here came out **11% slower** (median 1.115x, geo 1.110, range
    0.94-1.27, sd 0.052) with identical src, benchmark, SDK 11.0.100-preview.7.26376.106,
    OS and machine. For 25 of 52 cells that drift exceeds the BID effect being
    measured. **A/B comparisons in this arm must use same-session runs; a
    cross-day denominator roughly doubles the apparent BID cost** (1.24x vs the
    true 1.10x).
- `csharp-bid.baseline.arm64.jsonl` — run `Rcsbid1` (2026-07-30, 52 cells),
  decimal128-csharp-migration at baseline commit `7db6346`, pre-step-5: BID
  representation swap + identity ingress complete, AggressiveInlining stripped,
  gate redesign and per-site inlining not yet begun. The fixed "before" for all
  step-5 fast-path-gate and inlining measurements.
