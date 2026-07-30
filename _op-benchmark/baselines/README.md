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
- `csharp-bid.baseline.arm64.jsonl` — run `Rcsbid1` (2026-07-30, 52 cells),
  decimal128-csharp-migration at baseline commit `7db6346`, pre-step-5: BID
  representation swap + identity ingress complete, AggressiveInlining stripped,
  gate redesign and per-site inlining not yet begun. The fixed "before" for all
  step-5 fast-path-gate and inlining measurements.
