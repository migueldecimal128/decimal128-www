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
- `csharp-ubd.stabilization-xRcsubd2.x86_64.jsonl` + `csharp-bid.stabilization-xRcsbid2b.x86_64.jsonl`
  — a **confirmation pass**, not new measurements of anything: both arms re-run
  back-to-back on 2026-07-30, each with a forced clean build, and in the REVERSED
  order (UBD first). Kept because they establish two things the single pass could not.
  - **The BID effect reproduces.** BID/UBD within each pass: median 1.099 -> 1.117,
    geomean **1.138 -> 1.134** (0.4% apart), sum-of-cells 1.091 -> 1.098, cells
    slower 39/52 -> 38/52; comparing the two ratio sets cell-by-cell gives median
    1.004. Band structure holds (NQos 1.56->1.60, NQss 1.50->1.50, CP 1.26->1.23,
    ET 0.92->0.95, CD 0.98->0.98). Because the order was reversed and the builds
    made symmetric, neither ordering nor the original build asymmetry (`xRcsbid2`
    ran incremental, `xRcsubd1` clean) was contributing. **~1.10x median / ~1.14x
    geomean is the real cost.**
  - **The drift is persistent state, not run-to-run noise.** Same-session repeats
    agree to ~1% (UBD rerun/UBD median 1.005, sd 0.058; BID rerun/BID median 1.009,
    sd 0.041) while the 36 h gap reproduces at 11-13% (UBD-rerun/shipping 1.126,
    independently of UBD-published/shipping 1.115). Checked during the pass: AC
    power, `pmset -g therm` CPU_Speed_Limit=100, no thermal/perf warnings, 16 CPUs
    — cause unidentified (battery was charging, an unproven candidate).
  - Neither file is a baseline in the frozen-zero sense; they are evidence. The
    zero remains `csharp-ubd.baseline.x86_64.jsonl` (`xRcsubd1`), unmodified, and
    the live BID store still holds `xRcsbid2` — this pass changed neither.
- `csharp-bid.baseline.arm64.jsonl` — run `Rcsbid1` (2026-07-30, 52 cells),
  decimal128-csharp-migration at baseline commit `7db6346`, pre-step-5: BID
  representation swap + identity ingress complete, AggressiveInlining stripped,
  gate redesign and per-site inlining not yet begun. The fixed "before" for all
  step-5 fast-path-gate and inlining measurements.
- `csharp-ubd.baseline.arm64.jsonl` — run `Rcsubd1` (2026-07-30, 52 cells), the
  arm64 twin of the x86_64 UBD baseline above: decimal128-csharp-migration rolled
  back to the seed commit `cca61bb` (= decimal128-csharp @ `9c66a99`; UBD
  representation, AggressiveInlining intact), measured the same day as the BID
  run `Rcsbid3` for a same-session denominator. Rows carry `lang: "csharp-bid"`
  for the same emitter reason as the x86 file — they are UBD measurements.
- `csharp-ubd.stabilization-Rcsubd2.arm64.jsonl` — the arm64 confirmation pass,
  same spirit as the x86 stabilization files above: BID re-run `Rcsbid4` (now the
  live store; the first run `Rcsbid3` is preserved in git history) and UBD re-run
  `Rcsubd2` (this file), all four runs same-day 2026-07-30. Establishes:
  - **Both arms repeat at ~1% on the M3** (BID Rcsbid4/Rcsbid3 geomean 0.995,
    UBD Rcsubd2/Rcsubd1 geomean 0.987) — no day-scale drift, unlike the i9.
  - **Rare per-cell mode flips exist on the UBD side**: sub MQss P-gen measured
    15.91 (Jul-28) / 28.60 (`Rcsubd1`) / 17.83 (`Rcsubd2`) ns — the frozen
    baseline's 28.60 is the outlier mode, so that cell is BID/UBD parity, not the
    0.62x win the frozen zero alone suggests. `Rcsubd1`'s mul CP P-gen 2.52 ns is
    also its high mode (2.07-2.13 typical). Sub-4 ns cells jitter +-10%.
  - Headline arm64 BID/UBD: 1.152 / 1.162 across the two pairings — **~1.15x**.
  The frozen zero remains `csharp-ubd.baseline.arm64.jsonl` (`Rcsubd1`), unmodified;
  consult this file for the two known outlier cells before trusting a single-cell
  ratio against it.
