---
layout: default
permalink: /benchmark/op-results.html
title: "Op Benchmark Results — Decimal128"
description: "decimal128 measured per operation band against alternative implementations (Intel libbid, IBM decQuad, libmpdecimal, and in-language idiom peers), with explicit ratios."
heading: "Op Benchmark Results"
---

<div class="whitepaper" markdown="1">

<p class="whitepaper-meta">Created 2026-06-25. Living document — as-measured results.</p>

This is the per-operation record of decimal128 **as-measured** against alternative
implementations (libbid / decQuad / mpdecimal / in-language idiom peers), band by band,
with explicit ratios. It is **data only**: the categories, magnitude profiles, units, parity
settings, and methodology are defined in the companion **`BenchmarkMatrix.md`** — read it
first; this document just records numbers produced under that contract. Two sibling reports
share the same store and `gen_bench.py`: **`benchmark-port-compare.md`** (cross-port
d128 band-shape matrices, no alternatives) and **`benchmark-finmix.md`** (the realistic
P-fin financial mix vs peers).

## Key — categories, profiles & modes

Columns: port · category · profile · arch · mode · ours ns/op · alt · alt ns/op · ratio · run · notes.
*(Headline rows use P-fin/P-gen; P-max rows tagged `stress`.)*

ns/op figures are `Time / 4096` (4096 ops per measured iteration); `ratio = alt /
ours` (`> 1` ⇒ ours faster). `ours` = decimal128 `_ctx` rung vs `alt` = libbid
`__bid128_*`. P-gen here = the C generators' digit-length-uniform widths (per-band:
SQ/FQ 1–34, NQ 1–14, OQ 25–34) — **not** the P-fin 64-bit headline (pending).

### Category & column codes (`BenchmarkMatrix.md` §3 is authoritative)

**Add / subtract** — binned by the operands' qExp gap (alignment work), §3.1:

| code | name | what it exercises |
|---|---|---|
| `SQ` | Same qExp | Δexp = 0; pack-direct fast path, no align |
| `NQ` | Near qExp | small gap, **no** rounding (result still fits 34 digits) |
| `OQ` | Overlapping qExp | gap forces align **+ round** (the heaviest add path) |
| `FQ` | Far qExp | smaller operand fully swamped (gap ≫ 34) |
| `SQ-x` / `NQ-x` | …cancellation | subtract modifier: near-equal operands cancel (catastrophic) |

**Multiply** — binned by the exact product's digitLen, §3.2:

| code | name | what it exercises |
|---|---|---|
| `CP` | Compact Product | ≤ 34 digits — no scaling |
| `WP` | Wide Product | 35–38 digits — 128-bit recipMulPow10 |
| `XP` | eXtra-wide Product | > 38 (up to 68) — 256-bit recipMulPow10 |
| `CP-64` | …64-bit | CP with 64-bit (P-fin) operands |

**Divide** — binned by divisor digitLen (scaled dividend = 34 + digitLen(y)), §3.3:

| code | name | what it exercises |
|---|---|---|
| `CD` | Compact Divide | divisor 1–4 digits — 128÷64 |
| `WD` | Wide Divide | divisor 5–19 — 256÷64 |
| `XD` | eXtra Divide | divisor 20–34 — 256÷128 Möller–Granlund |
| `ET` | Exact / Terminating | `x/y` exact (residue `EXACT`) — full divide + trailing-zero strip |
| `PT` | Power-of-Ten divisor | `y = 10^k` — exact, coefficient-preserving result via the dedicated `divPow10Divisor` fast path (CrossPlatformArchitecture §2.4.9). Measured **3.16 ns, 3.62× vs libbid** (§4, run `Rc`; the pre-path `h2` measurement ran the CD kernel at 17.64 ns) |

**Profiles** (operand-magnitude regime, §2.1, mandatory per row): `P-fin` = financial
(64-bit/≤19-digit operands) · `P-gen` = general (digit-length-uniform) · `P-max` =
stress (34-digit; tagged `stress`, excluded from headline aggregates).
**Modes:** `thru` = throughput · `lat` = latency (dependent chain). `thru*` = best-case
fixed-operand throughput · `thru‡` = JVM escape-forced alloc-inclusive (each glossed in
the section that uses it). A bare `N` (e.g. "N (blend)") = an un-binned random baseline,
not a taxonomy code.

## 1. Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared
`decimal128-resources/swept/<profile>/` corpus, byte-identical operands every port).
arm64 (M3 Pro); JVM verify-off, `‡` = escape-forced alloc-inclusive. The cross-port d128
band-shape matrices moved to **`benchmark-port-compare.md`**; this section is the
**relational peer table** (explicit ratios). Add/sub run to 34 digits, so only the full-width peers —
**libbid / decQuad / mpdecimal** (measured in C, valid for every port since operands are
identical) and **BigDecimal** (JVM) — can represent P-gen/P-max; the 28-digit compact peer
`rust_decimal` runs inline on the compact SQ/NQ/MQ bands (relational table below).

**Relational — d128 vs the universal reference `libbid`** (Intel BID, full 34-digit,
measured in the C arm on the identical swept operands ⇒ valid for every port; ratio =
libbid/ours, ≥1 ⇒ d128 faster). C additionally vs decQuad (DPD) and mpdecimal. **The
ratio carries each port's own harness/packaging term** (Swift `opaque()`, Go backend, …),
since d128 is timed in-port and libbid in C — same caveat as elsewhere. java/kotlin +
BigDecimal pending.

<!-- BEGIN GENERATED add-rel -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | add | SQ | P-gen | arm64 | thru | 2.16 | libbid | 7.79 | **3.61×** | Rc2 |  |
| c | add | NQ | P-gen | arm64 | thru | 3.96 | libbid | 8.46 | **2.14×** | Rc2 |  |
| c | add | MQ | P-gen | arm64 | thru | 10.80 | libbid | 8.57 | **0.79×** | Rc2 |  |
| c | add | OQ | P-gen | arm64 | thru | 12.07 | libbid | 13.87 | **1.15×** | Rc2 |  |
| c | add | FQ | P-gen | arm64 | thru | 7.07 | libbid | 9.37 | **1.33×** | Rc2 |  |
| rust | add | SQ | P-gen | arm64 | thru | 2.73 | rust_decimal | 3.49 | **1.28×** | Rrsw2 | compact idiom peer |
| rust | add | NQ | P-gen | arm64 | thru | 4.97 | rust_decimal | 5.54 | **1.11×** | Rrsw2 | compact idiom peer |
| rust | add | MQ | P-gen | arm64 | thru | 13.87 | rust_decimal | 5.69 | **0.41×** | Rrsw2 | compact idiom peer |
| rust | add | OQ | P-gen | arm64 | thru | 10.88 | - | - | - | Rrsw2 |  |
| rust | add | FQ | P-gen | arm64 | thru | 6.65 | - | - | - | Rrsw2 |  |
| zig | add | SQ | P-gen | arm64 | thru | 2.54 | libbid | 7.79 | **3.07×** | Rzgsw2 |  |
| zig | add | NQ | P-gen | arm64 | thru | 6.07 | libbid | 8.46 | **1.39×** | Rzgsw2 |  |
| zig | add | MQ | P-gen | arm64 | thru | 12.18 | libbid | 8.57 | **0.70×** | Rzgsw2 |  |
| zig | add | OQ | P-gen | arm64 | thru | 12.83 | libbid | 13.87 | **1.08×** | Rzgsw2 |  |
| zig | add | FQ | P-gen | arm64 | thru | 7.58 | libbid | 9.37 | **1.24×** | Rzgsw2 |  |
| swift | add | SQ | P-gen | arm64 | thru | 4.15 | Foundation.Decimal | 306.15 | **73.77×** | Rswsw2 | compact idiom peer |
| swift | add | NQ | P-gen | arm64 | thru | 5.99 | Foundation.Decimal | 386.53 | **64.53×** | Rswsw2 | compact idiom peer |
| swift | add | MQ | P-gen | arm64 | thru | 15.93 | Foundation.Decimal | 392.09 | **24.61×** | Rswsw2 | compact idiom peer |
| swift | add | OQ | P-gen | arm64 | thru | 17.68 | Foundation.Decimal | 522.39 | **29.55×** | Rswsw2 | compact idiom peer |
| swift | add | FQ | P-gen | arm64 | thru | 12.84 | Foundation.Decimal | 271.65 | **21.16×** | Rswsw2 | compact idiom peer |
| csharp | add | SQ | P-gen | arm64 | thru | 3.01 | System.Decimal | 2.38 | **0.79×** | Rcssw2 | compact idiom peer |
| csharp | add | NQ | P-gen | arm64 | thru | 5.31 | System.Decimal | 3.61 | **0.68×** | Rcssw2 | compact idiom peer |
| csharp | add | MQ | P-gen | arm64 | thru | 14.13 | System.Decimal | 3.41 | **0.24×** | Rcssw2 | compact idiom peer |
| csharp | add | OQ | P-gen | arm64 | thru | 19.84 | - | - | - | Rcssw2 |  |
| csharp | add | FQ | P-gen | arm64 | thru | 11.23 | - | - | - | Rcssw2 |  |
| go | add | SQ | P-gen | arm64 | thru | 5.07 | - | - | - | Rgosw2 |  |
| go | add | NQ | P-gen | arm64 | thru | 10.38 | - | - | - | Rgosw2 |  |
| go | add | MQ | P-gen | arm64 | thru | 21.83 | - | - | - | Rgosw2 |  |
| go | add | OQ | P-gen | arm64 | thru | 32.50 | - | - | - | Rgosw2 |  |
| go | add | FQ | P-gen | arm64 | thru | 19.99 | - | - | - | Rgosw2 |  |
| java | add | SQ | P-gen | arm64 | thru‡ | 5.47 | BigDecimal | 18.86 | **3.45×** | Rjasw2 | compact idiom peer |
| java | add | NQ | P-gen | arm64 | thru‡ | 7.32 | BigDecimal | 29.70 | **4.06×** | Rjasw2 | compact idiom peer |
| java | add | MQ | P-gen | arm64 | thru‡ | 22.11 | BigDecimal | 29.96 | **1.36×** | Rjasw2 | compact idiom peer |
| java | add | OQ | P-gen | arm64 | thru‡ | 30.33 | BigDecimal | 68.94 | **2.27×** | Rjasw2 | compact idiom peer |
| java | add | FQ | P-gen | arm64 | thru‡ | 22.14 | BigDecimal | 81.19 | **3.67×** | Rjasw2 | compact idiom peer |
| kotlin | add | SQ | P-gen | arm64 | thru‡ | 6.02 | BigDecimal | 19.52 | **3.24×** | Rkosw2 | compact idiom peer |
| kotlin | add | NQ | P-gen | arm64 | thru‡ | 7.43 | BigDecimal | 31.03 | **4.18×** | Rkosw2 | compact idiom peer |
| kotlin | add | MQ | P-gen | arm64 | thru‡ | 21.91 | BigDecimal | 31.08 | **1.42×** | Rkosw2 | compact idiom peer |
| kotlin | add | OQ | P-gen | arm64 | thru‡ | 38.01 | BigDecimal | 72.43 | **1.91×** | Rkosw2 | compact idiom peer |
| kotlin | add | FQ | P-gen | arm64 | thru‡ | 18.26 | BigDecimal | 80.68 | **4.42×** | Rkosw2 | compact idiom peer |
| python | add | SQ | P-gen | arm64 | thru | 24.02 | decimal.Decimal | 61.64 | **2.57×** | Rpysw2 | compact idiom peer |
| python | add | NQ | P-gen | arm64 | thru | 22.34 | decimal.Decimal | 71.62 | **3.21×** | Rpysw2 | compact idiom peer |
| python | add | MQ | P-gen | arm64 | thru | 29.81 | decimal.Decimal | 71.71 | **2.41×** | Rpysw2 | compact idiom peer |
| python | add | OQ | P-gen | arm64 | thru | 39.74 | decimal.Decimal | 85.75 | **2.16×** | Rpysw2 | compact idiom peer |
| python | add | FQ | P-gen | arm64 | thru | 32.73 | decimal.Decimal | 80.83 | **2.47×** | Rpysw2 | compact idiom peer |
| c | add | SQ | P-gen | arm64 | thru | 2.16 | decQuad | 20.84 | **9.65×** | Rc2 |  |
| c | add | NQ | P-gen | arm64 | thru | 3.96 | decQuad | 30.10 | **7.60×** | Rc2 |  |
| c | add | MQ | P-gen | arm64 | thru | 10.80 | decQuad | 28.68 | **2.66×** | Rc2 |  |
| c | add | OQ | P-gen | arm64 | thru | 12.07 | decQuad | 35.77 | **2.96×** | Rc2 |  |
| c | add | FQ | P-gen | arm64 | thru | 7.07 | decQuad | 26.44 | **3.74×** | Rc2 |  |
| c | add | SQ | P-gen | arm64 | thru | 2.16 | mpdecimal | 12.41 | **5.75×** | Rc2 |  |
| c | add | NQ | P-gen | arm64 | thru | 3.96 | mpdecimal | 26.98 | **6.81×** | Rc2 |  |
| c | add | MQ | P-gen | arm64 | thru | 10.80 | mpdecimal | 26.02 | **2.41×** | Rc2 |  |
| c | add | OQ | P-gen | arm64 | thru | 12.07 | mpdecimal | 47.59 | **3.94×** | Rc2 |  |
| c | add | FQ | P-gen | arm64 | thru | 7.07 | mpdecimal | 40.65 | **5.75×** | Rc2 |  |

<!-- END GENERATED add-rel -->

**Relational vs peers — x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | add | SQ | P-gen | x86_64 | thru | 8.93 | libbid | 30.20 | **3.38×** | xRc2 |  |
| c | add | NQ | P-gen | x86_64 | thru | 13.67 | libbid | 33.46 | **2.45×** | xRc2 |  |
| c | add | MQ | P-gen | x86_64 | thru | 35.37 | libbid | 31.52 | **0.89×** | xRc2 |  |
| c | add | OQ | P-gen | x86_64 | thru | 46.17 | libbid | 51.83 | **1.12×** | xRc2 |  |
| c | add | FQ | P-gen | x86_64 | thru | 31.57 | libbid | 32.09 | **1.02×** | xRc2 |  |
| rust | add | SQ | P-gen | x86_64 | thru | 8.41 | rust_decimal | 15.83 | **1.88×** | xRrsw2 | compact idiom peer |
| rust | add | NQ | P-gen | x86_64 | thru | 12.40 | rust_decimal | 20.60 | **1.66×** | xRrsw2 | compact idiom peer |
| rust | add | MQ | P-gen | x86_64 | thru | 24.95 | rust_decimal | 20.29 | **0.81×** | xRrsw2 | compact idiom peer |
| rust | add | OQ | P-gen | x86_64 | thru | 37.99 | - | - | - | xRrsw2 |  |
| rust | add | FQ | P-gen | x86_64 | thru | 21.35 | - | - | - | xRrsw2 |  |
| zig | add | SQ | P-gen | x86_64 | thru | 10.78 | libbid | 30.20 | **2.80×** | xRzgsw2 |  |
| zig | add | NQ | P-gen | x86_64 | thru | 16.34 | libbid | 33.46 | **2.05×** | xRzgsw2 |  |
| zig | add | MQ | P-gen | x86_64 | thru | 25.55 | libbid | 31.52 | **1.23×** | xRzgsw2 |  |
| zig | add | OQ | P-gen | x86_64 | thru | 35.11 | libbid | 51.83 | **1.48×** | xRzgsw2 |  |
| zig | add | FQ | P-gen | x86_64 | thru | 21.19 | libbid | 32.09 | **1.51×** | xRzgsw2 |  |
| swift | add | SQ | P-gen | x86_64 | thru | 9.50 | Foundation.Decimal | 789.25 | **83.08×** | xRswsw2 | compact idiom peer |
| swift | add | NQ | P-gen | x86_64 | thru | 13.55 | Foundation.Decimal | 949.79 | **70.10×** | xRswsw2 | compact idiom peer |
| swift | add | MQ | P-gen | x86_64 | thru | 28.91 | Foundation.Decimal | 959.17 | **33.18×** | xRswsw2 | compact idiom peer |
| swift | add | OQ | P-gen | x86_64 | thru | 40.41 | Foundation.Decimal | 1286.86 | **31.85×** | xRswsw2 | compact idiom peer |
| swift | add | FQ | P-gen | x86_64 | thru | 29.03 | Foundation.Decimal | 626.53 | **21.58×** | xRswsw2 | compact idiom peer |
| csharp | add | SQ | P-gen | x86_64 | thru | 13.59 | System.Decimal | 11.55 | **0.85×** | xRcssw2 | compact idiom peer |
| csharp | add | NQ | P-gen | x86_64 | thru | 18.16 | System.Decimal | 15.87 | **0.87×** | xRcssw2 | compact idiom peer |
| csharp | add | MQ | P-gen | x86_64 | thru | 50.25 | System.Decimal | 15.12 | **0.30×** | xRcssw2 | compact idiom peer |
| csharp | add | OQ | P-gen | x86_64 | thru | 71.58 | - | - | - | xRcssw2 |  |
| csharp | add | FQ | P-gen | x86_64 | thru | 42.58 | - | - | - | xRcssw2 |  |
| go | add | SQ | P-gen | x86_64 | thru | 12.31 | - | - | - | xRgosw2 |  |
| go | add | NQ | P-gen | x86_64 | thru | 17.70 | - | - | - | xRgosw2 |  |
| go | add | MQ | P-gen | x86_64 | thru | 42.80 | - | - | - | xRgosw2 |  |
| go | add | OQ | P-gen | x86_64 | thru | 66.05 | - | - | - | xRgosw2 |  |
| go | add | FQ | P-gen | x86_64 | thru | 40.02 | - | - | - | xRgosw2 |  |
| java | add | SQ | P-gen | x86_64 | thru‡ | 13.52 | BigDecimal | 53.06 | **3.92×** | xRjasw2 | compact idiom peer |
| java | add | NQ | P-gen | x86_64 | thru‡ | 18.92 | BigDecimal | 82.51 | **4.36×** | xRjasw2 | compact idiom peer |
| java | add | MQ | P-gen | x86_64 | thru‡ | 37.06 | BigDecimal | 85.05 | **2.29×** | xRjasw2 | compact idiom peer |
| java | add | OQ | P-gen | x86_64 | thru‡ | 59.75 | BigDecimal | 173.14 | **2.90×** | xRjasw2 | compact idiom peer |
| java | add | FQ | P-gen | x86_64 | thru‡ | 40.06 | BigDecimal | 238.95 | **5.96×** | xRjasw2 | compact idiom peer |
| kotlin | add | SQ | P-gen | x86_64 | thru‡ | 16.74 | BigDecimal | 56.71 | **3.39×** | xRkosw2 | compact idiom peer |
| kotlin | add | NQ | P-gen | x86_64 | thru‡ | 23.55 | BigDecimal | 87.61 | **3.72×** | xRkosw2 | compact idiom peer |
| kotlin | add | MQ | P-gen | x86_64 | thru‡ | 43.19 | BigDecimal | 86.61 | **2.01×** | xRkosw2 | compact idiom peer |
| kotlin | add | OQ | P-gen | x86_64 | thru‡ | 70.87 | BigDecimal | 168.54 | **2.38×** | xRkosw2 | compact idiom peer |
| kotlin | add | FQ | P-gen | x86_64 | thru‡ | 45.86 | BigDecimal | 210.55 | **4.59×** | xRkosw2 | compact idiom peer |
| python | add | SQ | P-gen | x86_64 | thru | 46.56 | decimal.Decimal | 122.06 | **2.62×** | xRpysw2 | compact idiom peer |
| python | add | NQ | P-gen | x86_64 | thru | 48.77 | decimal.Decimal | 146.11 | **3.00×** | xRpysw2 | compact idiom peer |
| python | add | MQ | P-gen | x86_64 | thru | 64.72 | decimal.Decimal | 142.40 | **2.20×** | xRpysw2 | compact idiom peer |
| python | add | OQ | P-gen | x86_64 | thru | 72.84 | decimal.Decimal | 170.96 | **2.35×** | xRpysw2 | compact idiom peer |
| python | add | FQ | P-gen | x86_64 | thru | 64.31 | decimal.Decimal | 167.15 | **2.60×** | xRpysw2 | compact idiom peer |
| c | add | SQ | P-gen | x86_64 | thru | 8.93 | decQuad | 51.90 | **5.81×** | xRc2 |  |
| c | add | NQ | P-gen | x86_64 | thru | 13.67 | decQuad | 80.55 | **5.89×** | xRc2 |  |
| c | add | MQ | P-gen | x86_64 | thru | 35.37 | decQuad | 77.86 | **2.20×** | xRc2 |  |
| c | add | OQ | P-gen | x86_64 | thru | 46.17 | decQuad | 88.50 | **1.92×** | xRc2 |  |
| c | add | FQ | P-gen | x86_64 | thru | 31.57 | decQuad | 71.35 | **2.26×** | xRc2 |  |
| c | add | SQ | P-gen | x86_64 | thru | 8.93 | mpdecimal | 36.59 | **4.10×** | xRc2 |  |
| c | add | NQ | P-gen | x86_64 | thru | 13.67 | mpdecimal | 56.71 | **4.15×** | xRc2 |  |
| c | add | MQ | P-gen | x86_64 | thru | 35.37 | mpdecimal | 56.80 | **1.61×** | xRc2 |  |
| c | add | OQ | P-gen | x86_64 | thru | 46.17 | mpdecimal | 134.00 | **2.90×** | xRc2 |  |
| c | add | FQ | P-gen | x86_64 | thru | 31.57 | mpdecimal | 85.49 | **2.71×** | xRc2 |  |

<!-- END GENERATED add-rel-x86 -->

## 2. Subtract — SQ · NQ · MQ · OQ · FQ

Same swept methodology, corpus, and peer set as §1 (Add): the compact SQ/NQ/MQ regime
(qExp ∈ [0,−8], result < 10²⁸ — recompacted so the 28-digit `rust_decimal` runs on the
same operands) plus the full-range OQ/FQ. Band-shape matrices are in
**`benchmark-port-compare.md`**; this section is the relational peer table. arm64
(M3 Pro); `‡` = JVM escape-forced alloc-inclusive.

**Relational — d128 vs the universal reference `libbid`** (Intel BID, full 34-digit,
measured in the C arm on the identical swept operands ⇒ valid for every port; ratio =
libbid/ours, ≥1 ⇒ d128 faster). C additionally vs decQuad (DPD) and mpdecimal. **The
ratio carries each port's own harness/packaging term** (Swift `opaque()`, Go backend, …),
since d128 is timed in-port and libbid in C — same caveat as elsewhere. java/kotlin +
BigDecimal pending.

<!-- BEGIN GENERATED sub-rel -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | sub | SQ | P-gen | arm64 | thru | 1.24 | libbid | 9.17 | **7.40×** | Rc2 |  |
| c | sub | NQ | P-gen | arm64 | thru | 4.79 | libbid | 9.60 | **2.00×** | Rc2 |  |
| c | sub | MQ | P-gen | arm64 | thru | 11.35 | libbid | 9.40 | **0.83×** | Rc2 |  |
| c | sub | OQ | P-gen | arm64 | thru | 12.68 | libbid | 14.83 | **1.17×** | Rc2 |  |
| c | sub | FQ | P-gen | arm64 | thru | 7.14 | libbid | 9.37 | **1.31×** | Rc2 |  |
| rust | sub | SQ | P-gen | arm64 | thru | 1.75 | rust_decimal | 3.52 | **2.01×** | Rrsw2 | compact idiom peer |
| rust | sub | NQ | P-gen | arm64 | thru | 5.14 | rust_decimal | 5.49 | **1.07×** | Rrsw2 | compact idiom peer |
| rust | sub | MQ | P-gen | arm64 | thru | 14.49 | rust_decimal | 5.71 | **0.39×** | Rrsw2 | compact idiom peer |
| rust | sub | OQ | P-gen | arm64 | thru | 10.97 | - | - | - | Rrsw2 |  |
| rust | sub | FQ | P-gen | arm64 | thru | 6.66 | - | - | - | Rrsw2 |  |
| zig | sub | SQ | P-gen | arm64 | thru | 1.56 | libbid | 9.17 | **5.88×** | Rzgsw2 |  |
| zig | sub | NQ | P-gen | arm64 | thru | 7.64 | libbid | 9.60 | **1.26×** | Rzgsw2 |  |
| zig | sub | MQ | P-gen | arm64 | thru | 13.51 | libbid | 9.40 | **0.70×** | Rzgsw2 |  |
| zig | sub | OQ | P-gen | arm64 | thru | 14.44 | libbid | 14.83 | **1.03×** | Rzgsw2 |  |
| zig | sub | FQ | P-gen | arm64 | thru | 9.31 | libbid | 9.37 | **1.01×** | Rzgsw2 |  |
| swift | sub | SQ | P-gen | arm64 | thru | 2.58 | Foundation.Decimal | 312.74 | **121.22×** | Rswsw2 | compact idiom peer |
| swift | sub | NQ | P-gen | arm64 | thru | 5.61 | Foundation.Decimal | 388.64 | **69.28×** | Rswsw2 | compact idiom peer |
| swift | sub | MQ | P-gen | arm64 | thru | 15.39 | Foundation.Decimal | 396.68 | **25.78×** | Rswsw2 | compact idiom peer |
| swift | sub | OQ | P-gen | arm64 | thru | 17.42 | Foundation.Decimal | 522.49 | **29.99×** | Rswsw2 | compact idiom peer |
| swift | sub | FQ | P-gen | arm64 | thru | 12.97 | Foundation.Decimal | 274.32 | **21.15×** | Rswsw2 | compact idiom peer |
| csharp | sub | SQ | P-gen | arm64 | thru | 2.06 | System.Decimal | 2.26 | **1.10×** | Rcssw2 | compact idiom peer |
| csharp | sub | NQ | P-gen | arm64 | thru | 8.61 | System.Decimal | 3.61 | **0.42×** | Rcssw2 | compact idiom peer |
| csharp | sub | MQ | P-gen | arm64 | thru | 14.98 | System.Decimal | 3.54 | **0.24×** | Rcssw2 | compact idiom peer |
| csharp | sub | OQ | P-gen | arm64 | thru | 21.18 | - | - | - | Rcssw2 |  |
| csharp | sub | FQ | P-gen | arm64 | thru | 11.78 | - | - | - | Rcssw2 |  |
| go | sub | SQ | P-gen | arm64 | thru | 2.69 | - | - | - | Rgosw2 |  |
| go | sub | NQ | P-gen | arm64 | thru | 10.09 | - | - | - | Rgosw2 |  |
| go | sub | MQ | P-gen | arm64 | thru | 22.03 | - | - | - | Rgosw2 |  |
| go | sub | OQ | P-gen | arm64 | thru | 32.21 | - | - | - | Rgosw2 |  |
| go | sub | FQ | P-gen | arm64 | thru | 19.60 | - | - | - | Rgosw2 |  |
| java | sub | SQ | P-gen | arm64 | thru‡ | 4.41 | BigDecimal | 22.64 | **5.13×** | Rjasw2 | compact idiom peer |
| java | sub | NQ | P-gen | arm64 | thru‡ | 7.15 | BigDecimal | 34.09 | **4.77×** | Rjasw2 | compact idiom peer |
| java | sub | MQ | P-gen | arm64 | thru‡ | 22.10 | BigDecimal | 34.07 | **1.54×** | Rjasw2 | compact idiom peer |
| java | sub | OQ | P-gen | arm64 | thru‡ | 29.43 | BigDecimal | 75.20 | **2.56×** | Rjasw2 | compact idiom peer |
| java | sub | FQ | P-gen | arm64 | thru‡ | 20.77 | BigDecimal | 90.69 | **4.37×** | Rjasw2 | compact idiom peer |
| kotlin | sub | SQ | P-gen | arm64 | thru‡ | 5.01 | BigDecimal | 23.70 | **4.73×** | Rkosw2 | compact idiom peer |
| kotlin | sub | NQ | P-gen | arm64 | thru‡ | 7.74 | BigDecimal | 34.60 | **4.47×** | Rkosw2 | compact idiom peer |
| kotlin | sub | MQ | P-gen | arm64 | thru‡ | 22.09 | BigDecimal | 34.93 | **1.58×** | Rkosw2 | compact idiom peer |
| kotlin | sub | OQ | P-gen | arm64 | thru‡ | 39.16 | BigDecimal | 81.02 | **2.07×** | Rkosw2 | compact idiom peer |
| kotlin | sub | FQ | P-gen | arm64 | thru‡ | 18.04 | BigDecimal | 85.78 | **4.75×** | Rkosw2 | compact idiom peer |
| python | sub | SQ | P-gen | arm64 | thru | 21.12 | decimal.Decimal | 63.46 | **3.00×** | Rpysw2 | compact idiom peer |
| python | sub | NQ | P-gen | arm64 | thru | 22.47 | decimal.Decimal | 73.16 | **3.26×** | Rpysw2 | compact idiom peer |
| python | sub | MQ | P-gen | arm64 | thru | 29.81 | decimal.Decimal | 72.65 | **2.44×** | Rpysw2 | compact idiom peer |
| python | sub | OQ | P-gen | arm64 | thru | 39.48 | decimal.Decimal | 86.03 | **2.18×** | Rpysw2 | compact idiom peer |
| python | sub | FQ | P-gen | arm64 | thru | 32.58 | decimal.Decimal | 81.53 | **2.50×** | Rpysw2 | compact idiom peer |
| c | sub | SQ | P-gen | arm64 | thru | 1.24 | decQuad | 23.21 | **18.72×** | Rc2 |  |
| c | sub | NQ | P-gen | arm64 | thru | 4.79 | decQuad | 32.42 | **6.77×** | Rc2 |  |
| c | sub | MQ | P-gen | arm64 | thru | 11.35 | decQuad | 30.13 | **2.65×** | Rc2 |  |
| c | sub | OQ | P-gen | arm64 | thru | 12.68 | decQuad | 36.32 | **2.86×** | Rc2 |  |
| c | sub | FQ | P-gen | arm64 | thru | 7.14 | decQuad | 27.69 | **3.88×** | Rc2 |  |
| c | sub | SQ | P-gen | arm64 | thru | 1.24 | mpdecimal | 12.18 | **9.82×** | Rc2 |  |
| c | sub | NQ | P-gen | arm64 | thru | 4.79 | mpdecimal | 22.26 | **4.65×** | Rc2 |  |
| c | sub | MQ | P-gen | arm64 | thru | 11.35 | mpdecimal | 20.98 | **1.85×** | Rc2 |  |
| c | sub | OQ | P-gen | arm64 | thru | 12.68 | mpdecimal | 46.42 | **3.66×** | Rc2 |  |
| c | sub | FQ | P-gen | arm64 | thru | 7.14 | mpdecimal | 41.10 | **5.76×** | Rc2 |  |

<!-- END GENERATED sub-rel -->

**Relational vs peers — x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | sub | SQ | P-gen | x86_64 | thru | 5.57 | libbid | 34.25 | **6.15×** | xRc2 |  |
| c | sub | NQ | P-gen | x86_64 | thru | 14.00 | libbid | 36.66 | **2.62×** | xRc2 |  |
| c | sub | MQ | P-gen | x86_64 | thru | 35.32 | libbid | 36.66 | **1.04×** | xRc2 |  |
| c | sub | OQ | P-gen | x86_64 | thru | 46.78 | libbid | 51.52 | **1.10×** | xRc2 |  |
| c | sub | FQ | P-gen | x86_64 | thru | 32.92 | libbid | 34.71 | **1.05×** | xRc2 |  |
| rust | sub | SQ | P-gen | x86_64 | thru | 7.77 | rust_decimal | 14.52 | **1.87×** | xRrsw2 | compact idiom peer |
| rust | sub | NQ | P-gen | x86_64 | thru | 13.74 | rust_decimal | 19.94 | **1.45×** | xRrsw2 | compact idiom peer |
| rust | sub | MQ | P-gen | x86_64 | thru | 26.44 | rust_decimal | 19.51 | **0.74×** | xRrsw2 | compact idiom peer |
| rust | sub | OQ | P-gen | x86_64 | thru | 39.48 | - | - | - | xRrsw2 |  |
| rust | sub | FQ | P-gen | x86_64 | thru | 24.08 | - | - | - | xRrsw2 |  |
| zig | sub | SQ | P-gen | x86_64 | thru | 7.52 | libbid | 34.25 | **4.55×** | xRzgsw2 |  |
| zig | sub | NQ | P-gen | x86_64 | thru | 17.78 | libbid | 36.66 | **2.06×** | xRzgsw2 |  |
| zig | sub | MQ | P-gen | x86_64 | thru | 26.56 | libbid | 36.66 | **1.38×** | xRzgsw2 |  |
| zig | sub | OQ | P-gen | x86_64 | thru | 36.59 | libbid | 51.52 | **1.41×** | xRzgsw2 |  |
| zig | sub | FQ | P-gen | x86_64 | thru | 24.10 | libbid | 34.71 | **1.44×** | xRzgsw2 |  |
| swift | sub | SQ | P-gen | x86_64 | thru | 7.72 | Foundation.Decimal | 775.21 | **100.42×** | xRswsw2 | compact idiom peer |
| swift | sub | NQ | P-gen | x86_64 | thru | 14.40 | Foundation.Decimal | 1002.85 | **69.64×** | xRswsw2 | compact idiom peer |
| swift | sub | MQ | P-gen | x86_64 | thru | 30.22 | Foundation.Decimal | 976.20 | **32.30×** | xRswsw2 | compact idiom peer |
| swift | sub | OQ | P-gen | x86_64 | thru | 41.28 | Foundation.Decimal | 1360.36 | **32.95×** | xRswsw2 | compact idiom peer |
| swift | sub | FQ | P-gen | x86_64 | thru | 29.56 | Foundation.Decimal | 634.49 | **21.46×** | xRswsw2 | compact idiom peer |
| csharp | sub | SQ | P-gen | x86_64 | thru | 10.77 | System.Decimal | 11.52 | **1.07×** | xRcssw2 | compact idiom peer |
| csharp | sub | NQ | P-gen | x86_64 | thru | 22.60 | System.Decimal | 15.69 | **0.69×** | xRcssw2 | compact idiom peer |
| csharp | sub | MQ | P-gen | x86_64 | thru | 49.51 | System.Decimal | 14.59 | **0.29×** | xRcssw2 | compact idiom peer |
| csharp | sub | OQ | P-gen | x86_64 | thru | 70.90 | - | - | - | xRcssw2 |  |
| csharp | sub | FQ | P-gen | x86_64 | thru | 41.26 | - | - | - | xRcssw2 |  |
| go | sub | SQ | P-gen | x86_64 | thru | 9.46 | - | - | - | xRgosw2 |  |
| go | sub | NQ | P-gen | x86_64 | thru | 18.14 | - | - | - | xRgosw2 |  |
| go | sub | MQ | P-gen | x86_64 | thru | 43.77 | - | - | - | xRgosw2 |  |
| go | sub | OQ | P-gen | x86_64 | thru | 65.49 | - | - | - | xRgosw2 |  |
| go | sub | FQ | P-gen | x86_64 | thru | 41.29 | - | - | - | xRgosw2 |  |
| java | sub | SQ | P-gen | x86_64 | thru‡ | 12.56 | BigDecimal | 61.14 | **4.87×** | xRjasw2 | compact idiom peer |
| java | sub | NQ | P-gen | x86_64 | thru‡ | 20.46 | BigDecimal | 88.35 | **4.32×** | xRjasw2 | compact idiom peer |
| java | sub | MQ | P-gen | x86_64 | thru‡ | 42.84 | BigDecimal | 99.92 | **2.33×** | xRjasw2 | compact idiom peer |
| java | sub | OQ | P-gen | x86_64 | thru‡ | 61.25 | BigDecimal | 180.86 | **2.95×** | xRjasw2 | compact idiom peer |
| java | sub | FQ | P-gen | x86_64 | thru‡ | 42.44 | BigDecimal | 208.92 | **4.92×** | xRjasw2 | compact idiom peer |
| kotlin | sub | SQ | P-gen | x86_64 | thru‡ | 14.66 | BigDecimal | 65.42 | **4.46×** | xRkosw2 | compact idiom peer |
| kotlin | sub | NQ | P-gen | x86_64 | thru‡ | 24.86 | BigDecimal | 91.38 | **3.68×** | xRkosw2 | compact idiom peer |
| kotlin | sub | MQ | P-gen | x86_64 | thru‡ | 42.31 | BigDecimal | 96.31 | **2.28×** | xRkosw2 | compact idiom peer |
| kotlin | sub | OQ | P-gen | x86_64 | thru‡ | 66.25 | BigDecimal | 180.48 | **2.72×** | xRkosw2 | compact idiom peer |
| kotlin | sub | FQ | P-gen | x86_64 | thru‡ | 45.59 | BigDecimal | 213.83 | **4.69×** | xRkosw2 | compact idiom peer |
| python | sub | SQ | P-gen | x86_64 | thru | 42.63 | decimal.Decimal | 121.05 | **2.84×** | xRpysw2 | compact idiom peer |
| python | sub | NQ | P-gen | x86_64 | thru | 48.62 | decimal.Decimal | 142.87 | **2.94×** | xRpysw2 | compact idiom peer |
| python | sub | MQ | P-gen | x86_64 | thru | 64.47 | decimal.Decimal | 143.60 | **2.23×** | xRpysw2 | compact idiom peer |
| python | sub | OQ | P-gen | x86_64 | thru | 73.37 | decimal.Decimal | 171.05 | **2.33×** | xRpysw2 | compact idiom peer |
| python | sub | FQ | P-gen | x86_64 | thru | 65.59 | decimal.Decimal | 168.41 | **2.57×** | xRpysw2 | compact idiom peer |
| c | sub | SQ | P-gen | x86_64 | thru | 5.57 | decQuad | 58.96 | **10.59×** | xRc2 |  |
| c | sub | NQ | P-gen | x86_64 | thru | 14.00 | decQuad | 87.94 | **6.28×** | xRc2 |  |
| c | sub | MQ | P-gen | x86_64 | thru | 35.32 | decQuad | 84.25 | **2.39×** | xRc2 |  |
| c | sub | OQ | P-gen | x86_64 | thru | 46.78 | decQuad | 95.16 | **2.03×** | xRc2 |  |
| c | sub | FQ | P-gen | x86_64 | thru | 32.92 | decQuad | 78.18 | **2.37×** | xRc2 |  |
| c | sub | SQ | P-gen | x86_64 | thru | 5.57 | mpdecimal | 36.59 | **6.57×** | xRc2 |  |
| c | sub | NQ | P-gen | x86_64 | thru | 14.00 | mpdecimal | 55.74 | **3.98×** | xRc2 |  |
| c | sub | MQ | P-gen | x86_64 | thru | 35.32 | mpdecimal | 55.48 | **1.57×** | xRc2 |  |
| c | sub | OQ | P-gen | x86_64 | thru | 46.78 | mpdecimal | 131.30 | **2.81×** | xRc2 |  |
| c | sub | FQ | P-gen | x86_64 | thru | 32.92 | mpdecimal | 84.62 | **2.57×** | xRc2 |  |

<!-- END GENERATED sub-rel-x86 -->

## 3. Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared
`decimal128-resources/swept/P-gen/` corpus, byte-identical operands every port). arm64
(M3 Pro); JVM `‡` = escape-forced alloc-inclusive. The cross-port d128 band-shape matrices
(the flat compact multiply vs the scaling wide paths) moved to
**`benchmark-port-compare.md`**; this section is the relational peer table (explicit
ratios). Only the full-width peers — **libbid / decQuad /
mpdecimal** (measured in C, valid for every port since operands are identical) — can
represent the wide WP/XP products; the 28-digit compact peers run only the compact **CP**
band — `rust_decimal`, `System.Decimal`, and `BigDecimal` appear inline in the relational
tables where representable.

**Relational — d128 vs the universal reference `libbid`** (Intel BID, measured in the C
arm on the identical swept operands ⇒ valid for every port; ratio = libbid/ours, ≥1 ⇒ d128
faster). C additionally vs decQuad (DPD) and mpdecimal. **The ratio carries each port's own
harness/packaging term** (Swift `opaque()`, Go backend, …), since d128 is timed in-port and
the peers in C (libbid/decQuad run `Rc`, mpdecimal run `Rmpd`). rust adds its compact idiom
peer `rust_decimal` on the CP band. java/kotlin + BigDecimal pending.

<!-- BEGIN GENERATED mul-rel -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | mul | CP | P-gen | arm64 | thru | 1.39 | libbid | 24.24 | **17.44×** | Rc2 | **no scaling** — the cheap multiply |
| c | mul | WP | P-gen | arm64 | thru | 20.69 | libbid | 33.43 | **1.62×** | Rc2 | 128-bit recipMulPow10 |
| c | mul | XP | P-gen | arm64 | thru | 29.20 | libbid | 44.63 | **1.53×** | Rc2 | 256-bit recipMulPow10; **1.19× ≈ the recipmul-256 work-order's 1.18–1.54× band** |
| rust | mul | CP | P-gen | arm64 | thru | 1.56 | libbid | 24.24 | **15.54×** | Rrsw2 |  |
| rust | mul | WP | P-gen | arm64 | thru | 14.17 | libbid | 33.43 | **2.36×** | Rrsw2 |  |
| rust | mul | XP | P-gen | arm64 | thru | 25.22 | libbid | 44.63 | **1.77×** | Rrsw2 |  |
| zig | mul | CP | P-gen | arm64 | thru | 1.58 | libbid | 24.24 | **15.34×** | Rzgsw2 |  |
| zig | mul | WP | P-gen | arm64 | thru | 18.57 | libbid | 33.43 | **1.80×** | Rzgsw2 |  |
| zig | mul | XP | P-gen | arm64 | thru | 25.44 | libbid | 44.63 | **1.75×** | Rzgsw2 |  |
| swift | mul | CP | P-gen | arm64 | thru | 4.06 | Foundation.Decimal | 277.54 | **68.36×** | Rswsw2 | compact idiom peer |
| swift | mul | WP | P-gen | arm64 | thru | 20.99 | Foundation.Decimal | 294.38 | **14.02×** | Rswsw2 | compact idiom peer |
| swift | mul | XP | P-gen | arm64 | thru | 27.65 | Foundation.Decimal | 798.35 | **28.87×** | Rswsw2 | compact idiom peer |
| csharp | mul | CP | P-gen | arm64 | thru | 2.19 | - | - | - | Rcssw2 |  |
| csharp | mul | WP | P-gen | arm64 | thru | 18.31 | - | - | - | Rcssw2 |  |
| csharp | mul | XP | P-gen | arm64 | thru | 31.58 | - | - | - | Rcssw2 |  |
| go | mul | CP | P-gen | arm64 | thru | 2.50 | - | - | - | Rgosw2 |  |
| go | mul | WP | P-gen | arm64 | thru | 27.04 | - | - | - | Rgosw2 |  |
| go | mul | XP | P-gen | arm64 | thru | 37.51 | - | - | - | Rgosw2 |  |
| java | mul | CP | P-gen | arm64 | thru‡ | 4.95 | BigDecimal | 12.03 | **2.43×** | Rjasw2 | compact idiom peer |
| java | mul | WP | P-gen | arm64 | thru‡ | 26.03 | BigDecimal | 51.27 | **1.97×** | Rjasw2 | compact idiom peer |
| java | mul | XP | P-gen | arm64 | thru‡ | 52.40 | BigDecimal | 159.32 | **3.04×** | Rjasw2 | compact idiom peer |
| kotlin | mul | CP | P-gen | arm64 | thru‡ | 5.32 | BigDecimal | 12.15 | **2.28×** | Rkosw2 | compact idiom peer |
| kotlin | mul | WP | P-gen | arm64 | thru‡ | 31.21 | BigDecimal | 55.94 | **1.79×** | Rkosw2 | compact idiom peer |
| kotlin | mul | XP | P-gen | arm64 | thru‡ | 61.49 | BigDecimal | 161.89 | **2.63×** | Rkosw2 | compact idiom peer |
| python | mul | CP | P-gen | arm64 | thru | 19.12 | decimal.Decimal | 63.55 | **3.32×** | Rpysw2 | compact idiom peer |
| python | mul | WP | P-gen | arm64 | thru | 38.31 | decimal.Decimal | 73.27 | **1.91×** | Rpysw2 | compact idiom peer |
| python | mul | XP | P-gen | arm64 | thru | 47.89 | decimal.Decimal | 91.68 | **1.91×** | Rpysw2 | compact idiom peer |
| c | mul | CP | P-gen | arm64 | thru | 1.39 | decQuad | 21.74 | **15.64×** | Rc2 | vs DPD |
| c | mul | WP | P-gen | arm64 | thru | 20.69 | decQuad | 26.16 | **1.26×** | Rc2 | vs DPD |
| c | mul | XP | P-gen | arm64 | thru | 29.20 | decQuad | 27.77 | **0.95×** | Rc2 | **decQuad edges d128 on the widest product** (software DPD's flat cost; libbid still slower) |
| c | mul | CP | P-gen | arm64 | thru | 1.39 | mpdecimal | 22.03 | **15.85×** | Rc2 | no-scale multiply vs libmpdec |
| c | mul | WP | P-gen | arm64 | thru | 20.69 | mpdecimal | 53.26 | **2.57×** | Rc2 | 128-bit recipMulPow10 |
| c | mul | XP | P-gen | arm64 | thru | 29.20 | mpdecimal | 72.75 | **2.49×** | Rc2 | **d128 wins the widest product vs libmpdec** (unlike decQuad) |

<!-- END GENERATED mul-rel -->

**Relational vs peers — x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | mul | CP | P-gen | x86_64 | thru | 4.69 | libbid | 47.38 | **10.10×** | xRc2 |  |
| c | mul | WP | P-gen | x86_64 | thru | 46.64 | libbid | 65.94 | **1.41×** | xRc2 |  |
| c | mul | XP | P-gen | x86_64 | thru | 56.37 | libbid | 96.66 | **1.71×** | xRc2 |  |
| rust | mul | CP | P-gen | x86_64 | thru | 5.24 | libbid | 47.38 | **9.04×** | xRrsw2 |  |
| rust | mul | WP | P-gen | x86_64 | thru | 30.70 | libbid | 65.94 | **2.15×** | xRrsw2 |  |
| rust | mul | XP | P-gen | x86_64 | thru | 44.65 | libbid | 96.66 | **2.16×** | xRrsw2 |  |
| zig | mul | CP | P-gen | x86_64 | thru | 7.72 | libbid | 47.38 | **6.14×** | xRzgsw2 |  |
| zig | mul | WP | P-gen | x86_64 | thru | 28.79 | libbid | 65.94 | **2.29×** | xRzgsw2 |  |
| zig | mul | XP | P-gen | x86_64 | thru | 42.80 | libbid | 96.66 | **2.26×** | xRzgsw2 |  |
| swift | mul | CP | P-gen | x86_64 | thru | 6.56 | Foundation.Decimal | 674.34 | **102.80×** | xRswsw2 | compact idiom peer |
| swift | mul | WP | P-gen | x86_64 | thru | 35.16 | Foundation.Decimal | 772.76 | **21.98×** | xRswsw2 | compact idiom peer |
| swift | mul | XP | P-gen | x86_64 | thru | 53.78 | Foundation.Decimal | 1998.35 | **37.16×** | xRswsw2 | compact idiom peer |
| csharp | mul | CP | P-gen | x86_64 | thru | 9.59 | - | - | - | xRcssw2 |  |
| csharp | mul | WP | P-gen | x86_64 | thru | 50.34 | - | - | - | xRcssw2 |  |
| csharp | mul | XP | P-gen | x86_64 | thru | 77.47 | - | - | - | xRcssw2 |  |
| go | mul | CP | P-gen | x86_64 | thru | 7.44 | - | - | - | xRgosw2 |  |
| go | mul | WP | P-gen | x86_64 | thru | 54.27 | - | - | - | xRgosw2 |  |
| go | mul | XP | P-gen | x86_64 | thru | 75.89 | - | - | - | xRgosw2 |  |
| java | mul | CP | P-gen | x86_64 | thru‡ | 14.13 | BigDecimal | 38.76 | **2.74×** | xRjasw2 | compact idiom peer |
| java | mul | WP | P-gen | x86_64 | thru‡ | 52.55 | BigDecimal | 151.33 | **2.88×** | xRjasw2 | compact idiom peer |
| java | mul | XP | P-gen | x86_64 | thru‡ | 78.46 | BigDecimal | 281.91 | **3.59×** | xRjasw2 | compact idiom peer |
| kotlin | mul | CP | P-gen | x86_64 | thru‡ | 14.59 | BigDecimal | 42.30 | **2.90×** | xRkosw2 | compact idiom peer |
| kotlin | mul | WP | P-gen | x86_64 | thru‡ | 46.83 | BigDecimal | 156.51 | **3.34×** | xRkosw2 | compact idiom peer |
| kotlin | mul | XP | P-gen | x86_64 | thru‡ | 85.48 | BigDecimal | 279.37 | **3.27×** | xRkosw2 | compact idiom peer |
| python | mul | CP | P-gen | x86_64 | thru | 42.70 | decimal.Decimal | 118.82 | **2.78×** | xRpysw2 | compact idiom peer |
| python | mul | WP | P-gen | x86_64 | thru | 75.70 | decimal.Decimal | 141.21 | **1.87×** | xRpysw2 | compact idiom peer |
| python | mul | XP | P-gen | x86_64 | thru | 88.72 | decimal.Decimal | 164.32 | **1.85×** | xRpysw2 | compact idiom peer |
| c | mul | CP | P-gen | x86_64 | thru | 4.69 | decQuad | 58.68 | **12.51×** | xRc2 |  |
| c | mul | WP | P-gen | x86_64 | thru | 46.64 | decQuad | 74.20 | **1.59×** | xRc2 |  |
| c | mul | XP | P-gen | x86_64 | thru | 56.37 | decQuad | 91.45 | **1.62×** | xRc2 |  |
| c | mul | CP | P-gen | x86_64 | thru | 4.69 | mpdecimal | 63.30 | **13.50×** | xRc2 |  |
| c | mul | WP | P-gen | x86_64 | thru | 46.64 | mpdecimal | 186.07 | **3.99×** | xRc2 |  |
| c | mul | XP | P-gen | x86_64 | thru | 56.37 | mpdecimal | 238.19 | **4.23×** | xRc2 |  |

<!-- END GENERATED mul-rel-x86 -->

## 4. Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; same shared `swept/P-gen/` corpus and
conventions as §3). arm64 (M3 Pro); JVM `‡` = escape-forced. Band-shape matrices are in
**`benchmark-port-compare.md`**; this section is the relational peer table. Bands:
**CD** small divisor (1–4 digits,
128÷64 quotient-first, §2.4.10), **WD** (5–19 digits, 256÷64), **XD** (20–34 digits,
256÷128 Möller–Granlund), **ET** exact/terminating early-out (integer-divide `cx/cy`,
`R0==0` ⇒ no rounding/strip), **PT** power-of-ten divisor (`divPow10Divisor` exponent-only
fast path, §2.4.9). d128's **compact-divide weakness** shows at CD/WD (≈ parity / slight
loss vs libbid; ~8–13% run-to-run drift, libbid control stable); the **ET/PT early-outs win
clean**. Peers: libbid/decQuad/mpdecimal (C, universal); rust adds `rust_decimal` on the
CD/PT compact bands.

**Relational — d128 vs the universal reference `libbid`** (measured in the C arm on the
identical swept operands ⇒ valid for every port; ratio = libbid/ours, ≥1 ⇒ d128 faster). C
additionally vs decQuad (DPD) and mpdecimal. The ratio carries each port's own
harness/packaging term, since d128 is timed in-port and the peers in C (libbid/decQuad run
`Rc`, mpdecimal run `Rmpd`). rust adds its compact idiom peer `rust_decimal`. java/kotlin +
BigDecimal pending.

<!-- BEGIN GENERATED div-rel -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | div | CD | P-gen | arm64 | thru | 42.13 | libbid | 36.61 | **0.87×** | Rc2 | 128÷64 quotient-first (§2.4.10); **libbid wins** — the compact-divide weakness persists |
| c | div | WD | P-gen | arm64 | thru | 38.54 | libbid | 37.71 | **0.98×** | Rc2 | 256÷64; **≈ parity / slight loss** |
| c | div | XD | P-gen | arm64 | thru | 33.72 | libbid | 40.43 | **1.20×** | Rc2 | 256÷128 Möller–Granlund |
| c | div | ET | P-gen | arm64 | thru | 8.40 | libbid | 11.57 | **1.38×** | Rc2 | **quotient-first exact early-out** — beats libbid's exact fast path |
| c | div | PT | P-gen | arm64 | thru | 3.15 | libbid | 11.42 | **3.63×** | Rc2 | `divPow10Divisor` (§2.4.9); **d128's fastest divide** (coeff-1 form) |
| rust | div | CD | P-gen | arm64 | thru | 26.16 | libbid | 36.61 | **1.40×** | Rrsw2 |  |
| rust | div | WD | P-gen | arm64 | thru | 35.28 | libbid | 37.71 | **1.07×** | Rrsw2 |  |
| rust | div | XD | P-gen | arm64 | thru | 39.49 | libbid | 40.43 | **1.02×** | Rrsw2 |  |
| rust | div | ET | P-gen | arm64 | thru | 9.49 | libbid | 11.57 | **1.22×** | Rrsw2 |  |
| rust | div | PT | P-gen | arm64 | thru | 3.98 | libbid | 11.42 | **2.87×** | Rrsw2 |  |
| zig | div | CD | P-gen | arm64 | thru | 39.04 | libbid | 36.61 | **0.94×** | Rzgsw2 |  |
| zig | div | WD | P-gen | arm64 | thru | 42.29 | libbid | 37.71 | **0.89×** | Rzgsw2 |  |
| zig | div | XD | P-gen | arm64 | thru | 34.46 | libbid | 40.43 | **1.17×** | Rzgsw2 |  |
| zig | div | ET | P-gen | arm64 | thru | 10.69 | libbid | 11.57 | **1.08×** | Rzgsw2 |  |
| zig | div | PT | P-gen | arm64 | thru | 4.23 | libbid | 11.42 | **2.70×** | Rzgsw2 |  |
| swift | div | CD | P-gen | arm64 | thru | 33.87 | Foundation.Decimal | 1289.57 | **38.07×** | Rswsw2 | compact idiom peer |
| swift | div | WD | P-gen | arm64 | thru | 44.84 | Foundation.Decimal | 846.47 | **18.88×** | Rswsw2 | compact idiom peer |
| swift | div | XD | P-gen | arm64 | thru | 44.18 | Foundation.Decimal | 681.51 | **15.43×** | Rswsw2 | compact idiom peer |
| swift | div | ET | P-gen | arm64 | thru | 8.53 | Foundation.Decimal | 3204.05 | **375.62×** | Rswsw2 | compact idiom peer |
| swift | div | PT | P-gen | arm64 | thru | 7.63 | Foundation.Decimal | 3093.81 | **405.48×** | Rswsw2 | compact idiom peer |
| csharp | div | CD | P-gen | arm64 | thru | 38.21 | - | - | - | Rcssw2 |  |
| csharp | div | WD | P-gen | arm64 | thru | 47.42 | - | - | - | Rcssw2 |  |
| csharp | div | XD | P-gen | arm64 | thru | 60.26 | - | - | - | Rcssw2 |  |
| csharp | div | ET | P-gen | arm64 | thru | 22.55 | - | - | - | Rcssw2 |  |
| csharp | div | PT | P-gen | arm64 | thru | 5.44 | - | - | - | Rcssw2 |  |
| go | div | CD | P-gen | arm64 | thru | 46.91 | - | - | - | Rgosw2 |  |
| go | div | WD | P-gen | arm64 | thru | 59.31 | - | - | - | Rgosw2 |  |
| go | div | XD | P-gen | arm64 | thru | 60.13 | - | - | - | Rgosw2 |  |
| go | div | ET | P-gen | arm64 | thru | 14.92 | - | - | - | Rgosw2 |  |
| go | div | PT | P-gen | arm64 | thru | 6.56 | - | - | - | Rgosw2 |  |
| java | div | CD | P-gen | arm64 | thru‡ | 30.35 | BigDecimal | 133.22 | **4.39×** | Rjasw2 | compact idiom peer |
| java | div | WD | P-gen | arm64 | thru‡ | 51.05 | BigDecimal | 110.08 | **2.16×** | Rjasw2 | compact idiom peer |
| java | div | XD | P-gen | arm64 | thru‡ | 48.29 | BigDecimal | 217.98 | **4.51×** | Rjasw2 | compact idiom peer |
| java | div | ET | P-gen | arm64 | thru‡ | 12.73 | BigDecimal | 441.62 | **34.69×** | Rjasw2 | compact idiom peer |
| java | div | PT | P-gen | arm64 | thru‡ | 9.78 | BigDecimal | 406.69 | **41.58×** | Rjasw2 | compact idiom peer |
| kotlin | div | CD | P-gen | arm64 | thru‡ | 34.96 | BigDecimal | 138.00 | **3.95×** | Rkosw2 | compact idiom peer |
| kotlin | div | WD | P-gen | arm64 | thru‡ | 50.90 | BigDecimal | 135.90 | **2.67×** | Rkosw2 | compact idiom peer |
| kotlin | div | XD | P-gen | arm64 | thru‡ | 52.77 | BigDecimal | 212.43 | **4.03×** | Rkosw2 | compact idiom peer |
| kotlin | div | ET | P-gen | arm64 | thru‡ | 19.44 | BigDecimal | 421.37 | **21.68×** | Rkosw2 | compact idiom peer |
| kotlin | div | PT | P-gen | arm64 | thru‡ | 11.48 | BigDecimal | 391.04 | **34.06×** | Rkosw2 | compact idiom peer |
| python | div | CD | P-gen | arm64 | thru | 58.75 | decimal.Decimal | 98.62 | **1.68×** | Rpysw2 | compact idiom peer |
| python | div | WD | P-gen | arm64 | thru | 65.11 | decimal.Decimal | 100.54 | **1.54×** | Rpysw2 | compact idiom peer |
| python | div | XD | P-gen | arm64 | thru | 63.27 | decimal.Decimal | 163.86 | **2.59×** | Rpysw2 | compact idiom peer |
| python | div | ET | P-gen | arm64 | thru | 24.44 | decimal.Decimal | 91.88 | **3.76×** | Rpysw2 | compact idiom peer |
| python | div | PT | P-gen | arm64 | thru | 18.25 | decimal.Decimal | 90.38 | **4.95×** | Rpysw2 | compact idiom peer |
| c | div | CD | P-gen | arm64 | thru | 42.13 | decQuad | 71.03 | **1.69×** | Rc2 | vs DPD |
| c | div | WD | P-gen | arm64 | thru | 38.54 | decQuad | 123.03 | **3.19×** | Rc2 | vs DPD |
| c | div | XD | P-gen | arm64 | thru | 33.72 | decQuad | 179.14 | **5.31×** | Rc2 | vs DPD — decNumber divide is slow |
| c | div | ET | P-gen | arm64 | thru | 8.40 | decQuad | 47.96 | **5.71×** | Rc2 | vs DPD |
| c | div | PT | P-gen | arm64 | thru | 3.15 | decQuad | 44.54 | **14.14×** | Rc2 | vs DPD |
| c | div | CD | P-gen | arm64 | thru | 42.13 | mpdecimal | 60.61 | **1.44×** | Rc2 | **narrowest divide gap** (libmpdec's compact divide is its cheapest, like d128's weakness) |
| c | div | WD | P-gen | arm64 | thru | 38.54 | mpdecimal | 92.47 | **2.40×** | Rc2 | 256÷64 |
| c | div | XD | P-gen | arm64 | thru | 33.72 | mpdecimal | 147.57 | **4.38×** | Rc2 | Cowlishaw signature (CD 59 < WD 87 < XD 144) |
| c | div | ET | P-gen | arm64 | thru | 8.40 | mpdecimal | 58.94 | **7.02×** | Rc2 | libmpdec has no exact early-out |
| c | div | PT | P-gen | arm64 | thru | 3.15 | mpdecimal | 51.15 | **16.24×** | Rc2 | **d128's biggest divide win vs libmpdec** |

<!-- END GENERATED div-rel -->

**Relational vs peers — x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | div | CD | P-gen | x86_64 | thru | 88.17 | libbid | 82.50 | **0.94×** | xRc2 |  |
| c | div | WD | P-gen | x86_64 | thru | 103.94 | libbid | 84.36 | **0.81×** | xRc2 |  |
| c | div | XD | P-gen | x86_64 | thru | 92.88 | libbid | 84.37 | **0.91×** | xRc2 |  |
| c | div | ET | P-gen | x86_64 | thru | 29.28 | libbid | 30.87 | **1.05×** | xRc2 |  |
| c | div | PT | P-gen | x86_64 | thru | 10.10 | libbid | 31.09 | **3.08×** | xRc2 |  |
| rust | div | CD | P-gen | x86_64 | thru | 73.19 | libbid | 82.50 | **1.13×** | xRrsw2 |  |
| rust | div | WD | P-gen | x86_64 | thru | 86.65 | libbid | 84.36 | **0.97×** | xRrsw2 |  |
| rust | div | XD | P-gen | x86_64 | thru | 86.15 | libbid | 84.37 | **0.98×** | xRrsw2 |  |
| rust | div | ET | P-gen | x86_64 | thru | 29.09 | libbid | 30.87 | **1.06×** | xRrsw2 |  |
| rust | div | PT | P-gen | x86_64 | thru | 9.89 | libbid | 31.09 | **3.14×** | xRrsw2 |  |
| zig | div | CD | P-gen | x86_64 | thru | 75.13 | libbid | 82.50 | **1.10×** | xRzgsw2 |  |
| zig | div | WD | P-gen | x86_64 | thru | 99.07 | libbid | 84.36 | **0.85×** | xRzgsw2 |  |
| zig | div | XD | P-gen | x86_64 | thru | 77.92 | libbid | 84.37 | **1.08×** | xRzgsw2 |  |
| zig | div | ET | P-gen | x86_64 | thru | 32.73 | libbid | 30.87 | **0.94×** | xRzgsw2 |  |
| zig | div | PT | P-gen | x86_64 | thru | 12.32 | libbid | 31.09 | **2.52×** | xRzgsw2 |  |
| swift | div | CD | P-gen | x86_64 | thru | 71.35 | Foundation.Decimal | 3051.77 | **42.77×** | xRswsw2 | compact idiom peer |
| swift | div | WD | P-gen | x86_64 | thru | 97.19 | Foundation.Decimal | 2064.40 | **21.24×** | xRswsw2 | compact idiom peer |
| swift | div | XD | P-gen | x86_64 | thru | 91.69 | Foundation.Decimal | 1485.98 | **16.21×** | xRswsw2 | compact idiom peer |
| swift | div | ET | P-gen | x86_64 | thru | 29.37 | Foundation.Decimal | 7272.49 | **247.62×** | xRswsw2 | compact idiom peer |
| swift | div | PT | P-gen | x86_64 | thru | 12.33 | Foundation.Decimal | 6794.60 | **551.06×** | xRswsw2 | compact idiom peer |
| csharp | div | CD | P-gen | x86_64 | thru | 96.82 | - | - | - | xRcssw2 |  |
| csharp | div | WD | P-gen | x86_64 | thru | 113.00 | - | - | - | xRcssw2 |  |
| csharp | div | XD | P-gen | x86_64 | thru | 121.06 | - | - | - | xRcssw2 |  |
| csharp | div | ET | P-gen | x86_64 | thru | 44.04 | - | - | - | xRcssw2 |  |
| csharp | div | PT | P-gen | x86_64 | thru | 12.21 | - | - | - | xRcssw2 |  |
| go | div | CD | P-gen | x86_64 | thru | 108.90 | - | - | - | xRgosw2 |  |
| go | div | WD | P-gen | x86_64 | thru | 133.40 | - | - | - | xRgosw2 |  |
| go | div | XD | P-gen | x86_64 | thru | 116.20 | - | - | - | xRgosw2 |  |
| go | div | ET | P-gen | x86_64 | thru | 37.99 | - | - | - | xRgosw2 |  |
| go | div | PT | P-gen | x86_64 | thru | 13.33 | - | - | - | xRgosw2 |  |
| java | div | CD | P-gen | x86_64 | thru‡ | 88.03 | BigDecimal | 369.63 | **4.20×** | xRjasw2 | compact idiom peer |
| java | div | WD | P-gen | x86_64 | thru‡ | 117.29 | BigDecimal | 251.05 | **2.14×** | xRjasw2 | compact idiom peer |
| java | div | XD | P-gen | x86_64 | thru‡ | 124.42 | BigDecimal | 347.70 | **2.79×** | xRjasw2 | compact idiom peer |
| java | div | ET | P-gen | x86_64 | thru‡ | 44.96 | BigDecimal | 1151.20 | **25.60×** | xRjasw2 | compact idiom peer |
| java | div | PT | P-gen | x86_64 | thru‡ | 23.94 | BigDecimal | 1050.40 | **43.88×** | xRjasw2 | compact idiom peer |
| kotlin | div | CD | P-gen | x86_64 | thru‡ | 94.77 | BigDecimal | 377.00 | **3.98×** | xRkosw2 | compact idiom peer |
| kotlin | div | WD | P-gen | x86_64 | thru‡ | 121.81 | BigDecimal | 268.25 | **2.20×** | xRkosw2 | compact idiom peer |
| kotlin | div | XD | P-gen | x86_64 | thru‡ | 132.68 | BigDecimal | 344.00 | **2.59×** | xRkosw2 | compact idiom peer |
| kotlin | div | ET | P-gen | x86_64 | thru‡ | 49.99 | BigDecimal | 1154.84 | **23.10×** | xRkosw2 | compact idiom peer |
| kotlin | div | PT | P-gen | x86_64 | thru‡ | 27.06 | BigDecimal | 1096.99 | **40.54×** | xRkosw2 | compact idiom peer |
| python | div | CD | P-gen | x86_64 | thru | 115.88 | decimal.Decimal | 213.03 | **1.84×** | xRpysw2 | compact idiom peer |
| python | div | WD | P-gen | x86_64 | thru | 125.94 | decimal.Decimal | 235.91 | **1.87×** | xRpysw2 | compact idiom peer |
| python | div | XD | P-gen | x86_64 | thru | 117.43 | decimal.Decimal | 345.32 | **2.94×** | xRpysw2 | compact idiom peer |
| python | div | ET | P-gen | x86_64 | thru | 64.53 | decimal.Decimal | 205.85 | **3.19×** | xRpysw2 | compact idiom peer |
| python | div | PT | P-gen | x86_64 | thru | 44.58 | decimal.Decimal | 187.65 | **4.21×** | xRpysw2 | compact idiom peer |
| c | div | CD | P-gen | x86_64 | thru | 88.17 | decQuad | 141.08 | **1.60×** | xRc2 |  |
| c | div | WD | P-gen | x86_64 | thru | 103.94 | decQuad | 250.81 | **2.41×** | xRc2 |  |
| c | div | XD | P-gen | x86_64 | thru | 92.88 | decQuad | 386.79 | **4.16×** | xRc2 |  |
| c | div | ET | P-gen | x86_64 | thru | 29.28 | decQuad | 98.60 | **3.37×** | xRc2 |  |
| c | div | PT | P-gen | x86_64 | thru | 10.10 | decQuad | 84.57 | **8.37×** | xRc2 |  |
| c | div | CD | P-gen | x86_64 | thru | 88.17 | mpdecimal | 161.54 | **1.83×** | xRc2 |  |
| c | div | WD | P-gen | x86_64 | thru | 103.94 | mpdecimal | 284.94 | **2.74×** | xRc2 |  |
| c | div | XD | P-gen | x86_64 | thru | 92.88 | mpdecimal | 363.97 | **3.92×** | xRc2 |  |
| c | div | ET | P-gen | x86_64 | thru | 29.28 | mpdecimal | 157.26 | **5.37×** | xRc2 |  |
| c | div | PT | P-gen | x86_64 | thru | 10.10 | mpdecimal | 105.98 | **10.49×** | xRc2 |  |

<!-- END GENERATED div-rel-x86 -->

## 5. FMA — FN (Barrett) · FF (fits-128) (run `Rprof`, arm64)

Swept `self + lhs·rhs` over the 3-operand FN/FF regimes (§3.4). `self` placement selects
the finalize path: **FN** keeps the wide product ⇒ 256-bit Barrett; **FF** swamps it ⇒
fits-128 fast path. The d128 FN/FF band-shape matrices (and the FN÷FF fast-path win) are in
**`benchmark-port-compare.md`**; this section is the peer head-to-head. `‡` = JVM
escape-forced.

**Peer head-to-head.** FMA is *not* peerless: every conformant reference exposes a true
fused multiply-add (one rounding) — Intel libbid (`bid128_fma`), IBM decQuad (`decQuadFMA`),
libmpdecimal (`mpd_qfma`), and Python's `decimal.Decimal.fma`. Ports with no in-language
fused-FMA peer pair against the libbid universal reference; `go`/`csharp` have neither and
show `-`. d128's fits-128 FF path is the standout (libbid ≈1.4×, decQuad ≈1.5×, mpd ≈3.5×):

<!-- BEGIN GENERATED fma-rel -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | fma | FN | FMA | arm64 | thru | 79.12 | libbid | 82.34 | **1.04×** | Rc2 |  |
| c | fma | FF | FMA | arm64 | thru | 42.22 | libbid | 59.70 | **1.41×** | Rc2 |  |
| rust | fma | FN | FMA | arm64 | thru | 23.03 | libbid | 82.34 | **3.58×** | Rrsw2 |  |
| rust | fma | FF | FMA | arm64 | thru | 33.57 | libbid | 59.70 | **1.78×** | Rrsw2 |  |
| zig | fma | FN | FMA | arm64 | thru | 66.93 | libbid | 82.34 | **1.23×** | Rzgsw2 |  |
| zig | fma | FF | FMA | arm64 | thru | 44.61 | libbid | 59.70 | **1.34×** | Rzgsw2 |  |
| swift | fma | FN | FMA | arm64 | thru | 85.36 | libbid | 82.34 | **0.96×** | Rswsw2 |  |
| swift | fma | FF | FMA | arm64 | thru | 44.53 | libbid | 59.70 | **1.34×** | Rswsw2 |  |
| csharp | fma | FN | FMA | arm64 | thru | 94.91 | - | - | - | Rcssw2 |  |
| csharp | fma | FF | FMA | arm64 | thru | 58.04 | - | - | - | Rcssw2 |  |
| go | fma | FN | FMA | arm64 | thru | 157.70 | - | - | - | Rgosw2 |  |
| go | fma | FF | FMA | arm64 | thru | 76.56 | - | - | - | Rgosw2 |  |
| java | fma | FN | FMA | arm64 | thru‡ | 104.26 | libbid | 82.34 | **0.79×** | Rjasw2 |  |
| java | fma | FF | FMA | arm64 | thru‡ | 75.19 | libbid | 59.70 | **0.79×** | Rjasw2 |  |
| kotlin | fma | FN | FMA | arm64 | thru‡ | 111.02 | libbid | 82.34 | **0.74×** | Rkosw2 |  |
| kotlin | fma | FF | FMA | arm64 | thru‡ | 88.17 | libbid | 59.70 | **0.68×** | Rkosw2 |  |
| python | fma | FN | FMA | arm64 | thru | 112.13 | decimal.Decimal | 142.15 | **1.27×** | Rpysw2 | compact idiom peer |
| python | fma | FF | FMA | arm64 | thru | 81.48 | decimal.Decimal | 164.49 | **2.02×** | Rpysw2 | compact idiom peer |
| c | fma | FN | FMA | arm64 | thru | 79.12 | decQuad | 61.27 | **0.77×** | Rc2 |  |
| c | fma | FF | FMA | arm64 | thru | 42.22 | decQuad | 71.75 | **1.70×** | Rc2 |  |
| c | fma | FN | FMA | arm64 | thru | 79.12 | mpdecimal | 89.61 | **1.13×** | Rc2 |  |
| c | fma | FF | FMA | arm64 | thru | 42.22 | mpdecimal | 145.83 | **3.45×** | Rc2 |  |

<!-- END GENERATED fma-rel -->

**Relational vs peers — x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | fma | FN | FMA | x86_64 | thru | 151.81 | libbid | 161.79 | **1.07×** | xRc2 |  |
| c | fma | FF | FMA | x86_64 | thru | 93.23 | libbid | 124.13 | **1.33×** | xRc2 |  |
| rust | fma | FN | FMA | x86_64 | thru | 62.90 | libbid | 161.79 | **2.57×** | xRrsw2 |  |
| rust | fma | FF | FMA | x86_64 | thru | 67.82 | libbid | 124.13 | **1.83×** | xRrsw2 |  |
| zig | fma | FN | FMA | x86_64 | thru | 106.84 | libbid | 161.79 | **1.51×** | xRzgsw2 |  |
| zig | fma | FF | FMA | x86_64 | thru | 74.65 | libbid | 124.13 | **1.66×** | xRzgsw2 |  |
| swift | fma | FN | FMA | x86_64 | thru | 151.33 | libbid | 161.79 | **1.07×** | xRswsw2 |  |
| swift | fma | FF | FMA | x86_64 | thru | 85.41 | libbid | 124.13 | **1.45×** | xRswsw2 |  |
| csharp | fma | FN | FMA | x86_64 | thru | 195.58 | - | - | - | xRcssw2 |  |
| csharp | fma | FF | FMA | x86_64 | thru | 138.44 | - | - | - | xRcssw2 |  |
| go | fma | FN | FMA | x86_64 | thru | 264.80 | - | - | - | xRgosw2 |  |
| go | fma | FF | FMA | x86_64 | thru | 147.40 | - | - | - | xRgosw2 |  |
| java | fma | FN | FMA | x86_64 | thru‡ | 220.62 | libbid | 161.79 | **0.73×** | xRjasw2 |  |
| java | fma | FF | FMA | x86_64 | thru‡ | 198.30 | libbid | 124.13 | **0.63×** | xRjasw2 |  |
| kotlin | fma | FN | FMA | x86_64 | thru‡ | 259.22 | libbid | 161.79 | **0.62×** | xRkosw2 |  |
| kotlin | fma | FF | FMA | x86_64 | thru‡ | 225.88 | libbid | 124.13 | **0.55×** | xRkosw2 |  |
| python | fma | FN | FMA | x86_64 | thru | 219.47 | decimal.Decimal | 280.07 | **1.28×** | xRpysw2 | compact idiom peer |
| python | fma | FF | FMA | x86_64 | thru | 183.06 | decimal.Decimal | 332.59 | **1.82×** | xRpysw2 | compact idiom peer |
| c | fma | FN | FMA | x86_64 | thru | 151.81 | decQuad | 148.04 | **0.98×** | xRc2 |  |
| c | fma | FF | FMA | x86_64 | thru | 93.23 | decQuad | 155.81 | **1.67×** | xRc2 |  |
| c | fma | FN | FMA | x86_64 | thru | 151.81 | mpdecimal | 261.29 | **1.72×** | xRc2 |  |
| c | fma | FF | FMA | x86_64 | thru | 93.23 | mpdecimal | 339.01 | **3.64×** | xRc2 |  |

<!-- END GENERATED fma-rel-x86 -->

## 6. Sibling reports (band shape · financial mix) → moved

Two views split out of this document; both are spliced from the same JSONL store
(`op-benchmark/results.*.jsonl`) by the same `gen_bench.py`, not re-measured:
- **`benchmark-port-compare.md`** — the cross-port d128 **band-shape matrices** (P-gen
  §1–§5, P-max stress, and FMA FN/FF), d128-only, **no** alternatives.
- **`benchmark-finmix.md`** — the **P-fin** financial-headline mix (one `MIX` add/sub
  stream, mul `CP`/`WP`, div `CD`/`WD`/`ET`/`PT`) vs peers.

This document (`benchmark-op-results.md`) keeps the per-band **relational** tables — d128 vs
libbid / decQuad / mpdecimal / idiom peers with explicit ratios.


</div>
