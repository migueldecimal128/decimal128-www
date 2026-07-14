---
layout: default
permalink: /whitepapers/benchmark-results.html
title: "Benchmark Results Hub — Decimal128"
description: "The consolidated record of decimal128 as-measured benchmark results across all ports and alternative implementations."
heading: "Benchmark Results Hub"
---


*Created 2026-06-25. Living document — as-measured results.*

This is the single consolidated record of decimal128 **as-measured** benchmark
results across all ports and alternative implementations. It is **data only**:
the categories, magnitude profiles, units, parity settings, and methodology are
defined in the companion **`BenchmarkMatrix.md`** — read it first; this document
just records numbers produced under that contract.

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
arm64 (M3 Pro); JVM verify-off, `‡` = escape-forced alloc-inclusive. **Two views:** the
compact d128 matrices (band shape — fast vs slow path at a glance), then the relational
peer table (explicit ratios). Add/sub run to 34 digits, so only the full-width peers —
**libbid / decQuad / mpdecimal** (measured in C, valid for every port since operands are
identical) and **BigDecimal** (JVM) — can represent P-gen/P-max; the 28-digit compact peer
`rust_decimal` runs inline on the compact SQ/NQ/MQ bands (relational table below).

**P-gen — d128 (ns/op).** SQ/NQ/MQ are the **compact** regime (qExp ∈ [0,−8], result
< 10²⁸; §3.1) — recompacted this run so the 28-digit peers can run on the same operands;
OQ/FQ keep the full range. **MQ (Δ>4, the `qAlignDelta>4` no-round path) is the new
column** — 2–3× the pack-direct NQ, the one add/sub band where d128's alignment slope
shows.

<!-- BEGIN GENERATED add-pgen -->
| port | add SQ | add NQ | add MQ | add OQ | add FQ |
|------|-------:|-------:|-------:|-------:|-------:|
| c      |  2.21 |  3.82 | 10.54 | 12.67 |  6.91 |
| rust   |  2.79 |  4.87 | 13.10 | 10.74 |  6.60 |
| zig    |  3.09 |  5.97 | 12.18 | 12.91 |  8.04 |
| swift  |  4.52 |  6.04 | 15.27 | 17.37 | 13.15 |
| csharp |  2.74 | 12.21 | 18.55 | 21.77 | 12.93 |
| go     |  5.14 |  9.96 | 21.80 | 33.11 | 19.32 |
| java‡  |  5.39 |  7.05 | 12.16 | 19.20 | 14.52 |
| kotlin‡|  5.79 |  8.50 | 13.96 | 18.92 | 15.14 |
| python | 22.33 | 22.73 | 32.66 | 45.71 | 33.56 |
<!-- END GENERATED add-pgen -->

**P-gen — d128 (ns/op) — x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-pgen-x86 -->
| port | add SQ | add NQ | add MQ | add OQ | add FQ |
|------|-------:|-------:|-------:|-------:|-------:|
| c      |  9.54 | 12.06 | 27.62 | 36.16 | 27.27 |
| rust   | 10.25 | 13.93 | 27.09 | 39.53 | 22.56 |
| zig    | 11.30 | 15.83 | 25.58 | 35.06 | 21.25 |
| swift  | 11.21 | 14.53 | 30.78 | 41.06 | 30.26 |
| csharp | 11.61 | 27.12 | 53.61 | 68.98 | 42.20 |
| go     | 10.64 | 16.36 | 41.41 | 63.23 | 39.00 |
| java‡  | 13.94 | 19.56 | 36.25 | 60.81 | 41.83 |
| kotlin‡| 17.50 | 24.80 | 42.21 | 64.15 | 46.78 |
| python | 56.19 | 51.59 | 66.70 | 75.92 | 68.55 |
<!-- END GENERATED add-pgen-x86 -->

**P-max — d128 (ns/op):**

<!-- BEGIN GENERATED add-pmax -->
| port | add SQ | add OQ | add FQ |
|------|-------:|-------:|-------:|
| c      |  3.63 | 17.63 |  8.01 |
| rust   |  4.81 | 13.77 |  6.36 |
| zig    |  3.84 | 16.34 |  7.96 |
| swift  |  5.97 | 22.78 | 12.77 |
| csharp |  6.81 | 27.18 | 10.42 |
| go     |  8.55 | 43.38 | 18.97 |
| java‡  |  6.62 | 20.99 | 12.50 |
| kotlin‡|  7.02 | 21.53 | 11.39 |
| python | 26.31 | 50.06 | 35.72 |
<!-- END GENERATED add-pmax -->

**P-max — d128 (ns/op) — x86_64 (stress).**

<!-- BEGIN GENERATED add-pmax-x86 -->
| port | add SQ | add OQ | add FQ |
|------|-------:|-------:|-------:|
| c      | 11.44 | 40.12 | 22.29 |
| rust   | 12.81 | 43.90 | 21.60 |
| zig    | 13.99 | 39.32 | 21.42 |
| swift  | 13.60 | 46.05 | 27.44 |
| csharp | 22.90 | 88.55 | 38.49 |
| go     | 20.71 | 79.82 | 33.00 |
| java‡  | 22.46 | 62.81 | 33.34 |
| kotlin‡| 27.61 | 85.16 | 39.24 |
| python | 53.11 | 82.16 | 61.71 |
<!-- END GENERATED add-pmax-x86 -->

**Relational — d128 vs the universal reference `libbid`** (Intel BID, full 34-digit,
measured in the C arm on the identical swept operands ⇒ valid for every port; ratio =
libbid/ours, ≥1 ⇒ d128 faster). C additionally vs decQuad (DPD) and mpdecimal. **The
ratio carries each port's own harness/packaging term** (Swift `opaque()`, Go backend, …),
since d128 is timed in-port and libbid in C — same caveat as elsewhere. java/kotlin +
BigDecimal pending.

<!-- BEGIN GENERATED add-rel -->
| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | add | SQ | P-gen | arm64 | thru | 2.21 | libbid | 9.61 | **4.35×** | Rc2 |  |
| c | add | NQ | P-gen | arm64 | thru | 3.82 | libbid | 8.51 | **2.23×** | Rc2 |  |
| c | add | MQ | P-gen | arm64 | thru | 10.54 | libbid | 8.77 | **0.83×** | Rc2 |  |
| c | add | OQ | P-gen | arm64 | thru | 12.67 | libbid | 13.78 | **1.09×** | Rc2 |  |
| c | add | FQ | P-gen | arm64 | thru | 6.91 | libbid | 10.61 | **1.54×** | Rc2 |  |
| rust | add | SQ | P-gen | arm64 | thru | 2.79 | rust_decimal | 3.51 | **1.26×** | Rrsw2 | compact idiom peer |
| rust | add | NQ | P-gen | arm64 | thru | 4.87 | rust_decimal | 6.04 | **1.24×** | Rrsw2 | compact idiom peer |
| rust | add | MQ | P-gen | arm64 | thru | 13.10 | rust_decimal | 6.01 | **0.46×** | Rrsw2 | compact idiom peer |
| rust | add | OQ | P-gen | arm64 | thru | 10.74 | - | - | - | Rrsw2 |  |
| rust | add | FQ | P-gen | arm64 | thru | 6.60 | - | - | - | Rrsw2 |  |
| zig | add | SQ | P-gen | arm64 | thru | 3.09 | libbid | 9.61 | **3.11×** | Rzgsw2 |  |
| zig | add | NQ | P-gen | arm64 | thru | 5.97 | libbid | 8.51 | **1.43×** | Rzgsw2 |  |
| zig | add | MQ | P-gen | arm64 | thru | 12.18 | libbid | 8.77 | **0.72×** | Rzgsw2 |  |
| zig | add | OQ | P-gen | arm64 | thru | 12.91 | libbid | 13.78 | **1.07×** | Rzgsw2 |  |
| zig | add | FQ | P-gen | arm64 | thru | 8.04 | libbid | 10.61 | **1.32×** | Rzgsw2 |  |
| swift | add | SQ | P-gen | arm64 | thru | 4.52 | Foundation.Decimal | 312.74 | **69.19×** | Rswsw2 | compact idiom peer |
| swift | add | NQ | P-gen | arm64 | thru | 6.04 | Foundation.Decimal | 386.56 | **64.00×** | Rswsw2 | compact idiom peer |
| swift | add | MQ | P-gen | arm64 | thru | 15.27 | Foundation.Decimal | 391.44 | **25.63×** | Rswsw2 | compact idiom peer |
| swift | add | OQ | P-gen | arm64 | thru | 17.37 | Foundation.Decimal | 519.07 | **29.88×** | Rswsw2 | compact idiom peer |
| swift | add | FQ | P-gen | arm64 | thru | 13.15 | Foundation.Decimal | 276.22 | **21.01×** | Rswsw2 | compact idiom peer |
| csharp | add | SQ | P-gen | arm64 | thru | 2.74 | System.Decimal | 2.37 | **0.86×** | Rcssw2 | compact idiom peer |
| csharp | add | NQ | P-gen | arm64 | thru | 12.21 | System.Decimal | 3.45 | **0.28×** | Rcssw2 | compact idiom peer |
| csharp | add | MQ | P-gen | arm64 | thru | 18.55 | System.Decimal | 3.43 | **0.18×** | Rcssw2 | compact idiom peer |
| csharp | add | OQ | P-gen | arm64 | thru | 21.77 | - | - | - | Rcssw2 |  |
| csharp | add | FQ | P-gen | arm64 | thru | 12.93 | - | - | - | Rcssw2 |  |
| go | add | SQ | P-gen | arm64 | thru | 5.14 | - | - | - | Rgosw2 |  |
| go | add | NQ | P-gen | arm64 | thru | 9.96 | - | - | - | Rgosw2 |  |
| go | add | MQ | P-gen | arm64 | thru | 21.80 | - | - | - | Rgosw2 |  |
| go | add | OQ | P-gen | arm64 | thru | 33.11 | - | - | - | Rgosw2 |  |
| go | add | FQ | P-gen | arm64 | thru | 19.32 | - | - | - | Rgosw2 |  |
| java | add | SQ | P-gen | arm64 | thru‡ | 5.39 | BigDecimal | 18.06 | **3.35×** | Rjasw2 | compact idiom peer |
| java | add | NQ | P-gen | arm64 | thru‡ | 7.05 | BigDecimal | 30.20 | **4.28×** | Rjasw2 | compact idiom peer |
| java | add | MQ | P-gen | arm64 | thru‡ | 12.16 | BigDecimal | 29.90 | **2.46×** | Rjasw2 | compact idiom peer |
| java | add | OQ | P-gen | arm64 | thru‡ | 19.20 | BigDecimal | 74.76 | **3.89×** | Rjasw2 | compact idiom peer |
| java | add | FQ | P-gen | arm64 | thru‡ | 14.52 | BigDecimal | 87.46 | **6.02×** | Rjasw2 | compact idiom peer |
| kotlin | add | SQ | P-gen | arm64 | thru‡ | 5.79 | BigDecimal | 18.72 | **3.23×** | Rkosw2 | compact idiom peer |
| kotlin | add | NQ | P-gen | arm64 | thru‡ | 8.50 | BigDecimal | 30.08 | **3.54×** | Rkosw2 | compact idiom peer |
| kotlin | add | MQ | P-gen | arm64 | thru‡ | 13.96 | BigDecimal | 30.41 | **2.18×** | Rkosw2 | compact idiom peer |
| kotlin | add | OQ | P-gen | arm64 | thru‡ | 18.92 | BigDecimal | 77.17 | **4.08×** | Rkosw2 | compact idiom peer |
| kotlin | add | FQ | P-gen | arm64 | thru‡ | 15.14 | BigDecimal | 88.06 | **5.82×** | Rkosw2 | compact idiom peer |
| python | add | SQ | P-gen | arm64 | thru | 22.33 | decimal.Decimal | 59.24 | **2.65×** | Rpysw2 | compact idiom peer |
| python | add | NQ | P-gen | arm64 | thru | 22.73 | decimal.Decimal | 68.71 | **3.02×** | Rpysw2 | compact idiom peer |
| python | add | MQ | P-gen | arm64 | thru | 32.66 | decimal.Decimal | 71.16 | **2.18×** | Rpysw2 | compact idiom peer |
| python | add | OQ | P-gen | arm64 | thru | 45.71 | decimal.Decimal | 84.25 | **1.84×** | Rpysw2 | compact idiom peer |
| python | add | FQ | P-gen | arm64 | thru | 33.56 | decimal.Decimal | 80.69 | **2.40×** | Rpysw2 | compact idiom peer |
| c | add | SQ | P-gen | arm64 | thru | 2.21 | decQuad | 19.99 | **9.05×** | Rc2 |  |
| c | add | NQ | P-gen | arm64 | thru | 3.82 | decQuad | 30.05 | **7.87×** | Rc2 |  |
| c | add | MQ | P-gen | arm64 | thru | 10.54 | decQuad | 28.93 | **2.74×** | Rc2 |  |
| c | add | OQ | P-gen | arm64 | thru | 12.67 | decQuad | 33.72 | **2.66×** | Rc2 |  |
| c | add | FQ | P-gen | arm64 | thru | 6.91 | decQuad | 25.66 | **3.71×** | Rc2 |  |
| c | add | SQ | P-gen | arm64 | thru | 2.21 | mpdecimal | 13.06 | **5.91×** | Rc2 |  |
| c | add | NQ | P-gen | arm64 | thru | 3.82 | mpdecimal | 27.38 | **7.17×** | Rc2 |  |
| c | add | MQ | P-gen | arm64 | thru | 10.54 | mpdecimal | 27.50 | **2.61×** | Rc2 |  |
| c | add | OQ | P-gen | arm64 | thru | 12.67 | mpdecimal | 46.18 | **3.64×** | Rc2 |  |
| c | add | FQ | P-gen | arm64 | thru | 6.91 | mpdecimal | 39.34 | **5.69×** | Rc2 |  |
<!-- END GENERATED add-rel -->

**Relational vs peers — x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-x86 -->
| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | add | SQ | P-gen | x86_64 | thru | 9.54 | libbid | 30.50 | **3.20×** | xRc2 |  |
| c | add | NQ | P-gen | x86_64 | thru | 12.06 | libbid | 33.59 | **2.79×** | xRc2 |  |
| c | add | MQ | P-gen | x86_64 | thru | 27.62 | libbid | 31.32 | **1.13×** | xRc2 |  |
| c | add | OQ | P-gen | x86_64 | thru | 36.16 | libbid | 47.82 | **1.32×** | xRc2 |  |
| c | add | FQ | P-gen | x86_64 | thru | 27.27 | libbid | 29.22 | **1.07×** | xRc2 |  |
| rust | add | SQ | P-gen | x86_64 | thru | 10.25 | rust_decimal | 14.31 | **1.40×** | xRrsw2 | compact idiom peer |
| rust | add | NQ | P-gen | x86_64 | thru | 13.93 | rust_decimal | 20.68 | **1.48×** | xRrsw2 | compact idiom peer |
| rust | add | MQ | P-gen | x86_64 | thru | 27.09 | rust_decimal | 20.49 | **0.76×** | xRrsw2 | compact idiom peer |
| rust | add | OQ | P-gen | x86_64 | thru | 39.53 | - | - | - | xRrsw2 |  |
| rust | add | FQ | P-gen | x86_64 | thru | 22.56 | - | - | - | xRrsw2 |  |
| zig | add | SQ | P-gen | x86_64 | thru | 11.30 | libbid | 30.50 | **2.70×** | xRzgsw2 |  |
| zig | add | NQ | P-gen | x86_64 | thru | 15.83 | libbid | 33.59 | **2.12×** | xRzgsw2 |  |
| zig | add | MQ | P-gen | x86_64 | thru | 25.58 | libbid | 31.32 | **1.22×** | xRzgsw2 |  |
| zig | add | OQ | P-gen | x86_64 | thru | 35.06 | libbid | 47.82 | **1.36×** | xRzgsw2 |  |
| zig | add | FQ | P-gen | x86_64 | thru | 21.25 | libbid | 29.22 | **1.38×** | xRzgsw2 |  |
| swift | add | SQ | P-gen | x86_64 | thru | 11.21 | Foundation.Decimal | 776.04 | **69.23×** | xRswsw2 | compact idiom peer |
| swift | add | NQ | P-gen | x86_64 | thru | 14.53 | Foundation.Decimal | 955.48 | **65.76×** | xRswsw2 | compact idiom peer |
| swift | add | MQ | P-gen | x86_64 | thru | 30.78 | Foundation.Decimal | 948.43 | **30.81×** | xRswsw2 | compact idiom peer |
| swift | add | OQ | P-gen | x86_64 | thru | 41.06 | Foundation.Decimal | 1278.78 | **31.14×** | xRswsw2 | compact idiom peer |
| swift | add | FQ | P-gen | x86_64 | thru | 30.26 | Foundation.Decimal | 633.82 | **20.95×** | xRswsw2 | compact idiom peer |
| csharp | add | SQ | P-gen | x86_64 | thru | 11.61 | System.Decimal | 11.96 | **1.03×** | xRcssw2 | compact idiom peer |
| csharp | add | NQ | P-gen | x86_64 | thru | 27.12 | System.Decimal | 14.28 | **0.53×** | xRcssw2 | compact idiom peer |
| csharp | add | MQ | P-gen | x86_64 | thru | 53.61 | System.Decimal | 13.67 | **0.25×** | xRcssw2 | compact idiom peer |
| csharp | add | OQ | P-gen | x86_64 | thru | 68.98 | - | - | - | xRcssw2 |  |
| csharp | add | FQ | P-gen | x86_64 | thru | 42.20 | - | - | - | xRcssw2 |  |
| go | add | SQ | P-gen | x86_64 | thru | 10.64 | - | - | - | xRgosw2 |  |
| go | add | NQ | P-gen | x86_64 | thru | 16.36 | - | - | - | xRgosw2 |  |
| go | add | MQ | P-gen | x86_64 | thru | 41.41 | - | - | - | xRgosw2 |  |
| go | add | OQ | P-gen | x86_64 | thru | 63.23 | - | - | - | xRgosw2 |  |
| go | add | FQ | P-gen | x86_64 | thru | 39.00 | - | - | - | xRgosw2 |  |
| java | add | SQ | P-gen | x86_64 | thru‡ | 13.94 | BigDecimal | 51.28 | **3.68×** | xRjasw2 | compact idiom peer |
| java | add | NQ | P-gen | x86_64 | thru‡ | 19.56 | BigDecimal | 81.47 | **4.17×** | xRjasw2 | compact idiom peer |
| java | add | MQ | P-gen | x86_64 | thru‡ | 36.25 | BigDecimal | 82.69 | **2.28×** | xRjasw2 | compact idiom peer |
| java | add | OQ | P-gen | x86_64 | thru‡ | 60.81 | BigDecimal | 162.81 | **2.68×** | xRjasw2 | compact idiom peer |
| java | add | FQ | P-gen | x86_64 | thru‡ | 41.83 | BigDecimal | 189.28 | **4.52×** | xRjasw2 | compact idiom peer |
| kotlin | add | SQ | P-gen | x86_64 | thru‡ | 17.50 | BigDecimal | 59.71 | **3.41×** | xRkosw2 | compact idiom peer |
| kotlin | add | NQ | P-gen | x86_64 | thru‡ | 24.80 | BigDecimal | 86.64 | **3.49×** | xRkosw2 | compact idiom peer |
| kotlin | add | MQ | P-gen | x86_64 | thru‡ | 42.21 | BigDecimal | 88.29 | **2.09×** | xRkosw2 | compact idiom peer |
| kotlin | add | OQ | P-gen | x86_64 | thru‡ | 64.15 | BigDecimal | 170.38 | **2.66×** | xRkosw2 | compact idiom peer |
| kotlin | add | FQ | P-gen | x86_64 | thru‡ | 46.78 | BigDecimal | 214.20 | **4.58×** | xRkosw2 | compact idiom peer |
| python | add | SQ | P-gen | x86_64 | thru | 56.19 | decimal.Decimal | 117.69 | **2.09×** | xRpysw2 | compact idiom peer |
| python | add | NQ | P-gen | x86_64 | thru | 51.59 | decimal.Decimal | 143.12 | **2.77×** | xRpysw2 | compact idiom peer |
| python | add | MQ | P-gen | x86_64 | thru | 66.70 | decimal.Decimal | 141.28 | **2.12×** | xRpysw2 | compact idiom peer |
| python | add | OQ | P-gen | x86_64 | thru | 75.92 | decimal.Decimal | 169.05 | **2.23×** | xRpysw2 | compact idiom peer |
| python | add | FQ | P-gen | x86_64 | thru | 68.55 | decimal.Decimal | 163.08 | **2.38×** | xRpysw2 | compact idiom peer |
| c | add | SQ | P-gen | x86_64 | thru | 9.54 | decQuad | 54.89 | **5.75×** | xRc2 |  |
| c | add | NQ | P-gen | x86_64 | thru | 12.06 | decQuad | 83.52 | **6.93×** | xRc2 |  |
| c | add | MQ | P-gen | x86_64 | thru | 27.62 | decQuad | 79.35 | **2.87×** | xRc2 |  |
| c | add | OQ | P-gen | x86_64 | thru | 36.16 | decQuad | 87.92 | **2.43×** | xRc2 |  |
| c | add | FQ | P-gen | x86_64 | thru | 27.27 | decQuad | 73.76 | **2.70×** | xRc2 |  |
| c | add | SQ | P-gen | x86_64 | thru | 9.54 | mpdecimal | 36.66 | **3.84×** | xRc2 |  |
| c | add | NQ | P-gen | x86_64 | thru | 12.06 | mpdecimal | 56.63 | **4.70×** | xRc2 |  |
| c | add | MQ | P-gen | x86_64 | thru | 27.62 | mpdecimal | 53.70 | **1.94×** | xRc2 |  |
| c | add | OQ | P-gen | x86_64 | thru | 36.16 | mpdecimal | 128.81 | **3.56×** | xRc2 |  |
| c | add | FQ | P-gen | x86_64 | thru | 27.27 | mpdecimal | 84.72 | **3.11×** | xRc2 |  |
<!-- END GENERATED add-rel-x86 -->

## 2. Subtract — SQ · NQ · MQ · OQ · FQ

Same swept methodology, corpus, and peer set as §1 (Add): the compact SQ/NQ/MQ regime
(qExp ∈ [0,−8], result < 10²⁸ — recompacted so the 28-digit `rust_decimal` runs on the
same operands) plus the full-range OQ/FQ. **Two views** — the compact d128 matrices then
the relational peer table. arm64 (M3 Pro); `‡` = JVM escape-forced alloc-inclusive.

**P-gen — d128 (ns/op).**

<!-- BEGIN GENERATED sub-pgen -->
| port | sub SQ | sub NQ | sub MQ | sub OQ | sub FQ |
|------|-------:|-------:|-------:|-------:|-------:|
| c      |  1.70 |  4.27 | 10.65 | 12.53 |  7.14 |
| rust   |  1.88 |  5.11 | 13.83 | 10.95 |  7.56 |
| zig    |  1.87 |  5.91 | 12.63 | 12.86 |  7.32 |
| swift  |  2.94 |  5.53 | 14.60 | 17.39 | 12.44 |
| csharp |  2.09 |  9.18 | 17.19 | 21.27 | 12.24 |
| go     |  3.04 |  9.52 | 21.49 | 32.64 | 19.87 |
| java‡  |  4.44 |  7.40 | 12.44 | 18.98 | 14.89 |
| kotlin‡|  4.80 |  8.91 | 14.11 | 19.13 | 14.54 |
| python | 20.81 | 22.63 | 32.93 | 44.53 | 33.51 |
<!-- END GENERATED sub-pgen -->

**P-gen — d128 (ns/op) — x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-pgen-x86 -->
| port | sub SQ | sub NQ | sub MQ | sub OQ | sub FQ |
|------|-------:|-------:|-------:|-------:|-------:|
| c      |  6.84 | 11.75 | 28.24 | 36.47 | 28.62 |
| rust   |  7.72 | 14.10 | 26.02 | 38.76 | 22.74 |
| zig    |  8.64 | 16.47 | 26.84 | 36.03 | 22.52 |
| swift  |  7.64 | 13.66 | 30.85 | 40.29 | 29.67 |
| csharp |  9.67 | 23.41 | 53.12 | 68.74 | 41.07 |
| go     |  9.35 | 16.87 | 41.05 | 63.51 | 38.87 |
| java‡  | 13.40 | 20.60 | 36.79 | 61.14 | 40.60 |
| kotlin‡| 15.32 | 25.64 | 46.32 | 66.18 | 42.79 |
| python | 51.26 | 53.81 | 68.59 | 77.70 | 71.00 |
<!-- END GENERATED sub-pgen-x86 -->

**P-max — d128 (ns/op):**

<!-- BEGIN GENERATED sub-pmax -->
| port | sub SQ | sub OQ | sub FQ |
|------|-------:|-------:|-------:|
| c      |  3.27 | 17.53 |  8.19 |
| rust   |  4.23 | 13.56 |  6.99 |
| zig    |  3.75 | 16.77 |  6.68 |
| swift  |  4.51 | 22.94 | 11.90 |
| csharp |  4.24 | 24.37 |  9.21 |
| go     |  6.65 | 43.32 | 19.52 |
| java‡  |  6.44 | 20.42 | 12.17 |
| kotlin‡|  6.78 | 21.48 | 11.64 |
| python | 27.28 | 50.38 | 35.83 |
<!-- END GENERATED sub-pmax -->

**P-max — d128 (ns/op) — x86_64 (stress).**

<!-- BEGIN GENERATED sub-pmax-x86 -->
| port | sub SQ | sub OQ | sub FQ |
|------|-------:|-------:|-------:|
| c      | 12.11 | 40.11 | 22.62 |
| rust   | 14.46 | 43.39 | 21.94 |
| zig    | 16.44 | 40.47 | 22.11 |
| swift  | 14.33 | 46.09 | 26.68 |
| csharp | 18.48 | 86.96 | 35.53 |
| go     | 18.30 | 80.84 | 34.16 |
| java‡  | 22.96 | 63.32 | 33.64 |
| kotlin‡| 29.14 | 86.94 | 40.24 |
| python | 58.23 | 91.32 | 64.61 |
<!-- END GENERATED sub-pmax-x86 -->

**Relational — d128 vs the universal reference `libbid`** (Intel BID, full 34-digit,
measured in the C arm on the identical swept operands ⇒ valid for every port; ratio =
libbid/ours, ≥1 ⇒ d128 faster). C additionally vs decQuad (DPD) and mpdecimal. **The
ratio carries each port's own harness/packaging term** (Swift `opaque()`, Go backend, …),
since d128 is timed in-port and libbid in C — same caveat as elsewhere. java/kotlin +
BigDecimal pending.

<!-- BEGIN GENERATED sub-rel -->
| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | sub | SQ | P-gen | arm64 | thru | 1.70 | libbid | 9.27 | **5.45×** | Rc2 |  |
| c | sub | NQ | P-gen | arm64 | thru | 4.27 | libbid | 10.68 | **2.50×** | Rc2 |  |
| c | sub | MQ | P-gen | arm64 | thru | 10.65 | libbid | 8.84 | **0.83×** | Rc2 |  |
| c | sub | OQ | P-gen | arm64 | thru | 12.53 | libbid | 15.49 | **1.24×** | Rc2 |  |
| c | sub | FQ | P-gen | arm64 | thru | 7.14 | libbid | 10.19 | **1.43×** | Rc2 |  |
| rust | sub | SQ | P-gen | arm64 | thru | 1.88 | rust_decimal | 3.60 | **1.91×** | Rrsw2 | compact idiom peer |
| rust | sub | NQ | P-gen | arm64 | thru | 5.11 | rust_decimal | 5.76 | **1.13×** | Rrsw2 | compact idiom peer |
| rust | sub | MQ | P-gen | arm64 | thru | 13.83 | rust_decimal | 6.00 | **0.43×** | Rrsw2 | compact idiom peer |
| rust | sub | OQ | P-gen | arm64 | thru | 10.95 | - | - | - | Rrsw2 |  |
| rust | sub | FQ | P-gen | arm64 | thru | 7.56 | - | - | - | Rrsw2 |  |
| zig | sub | SQ | P-gen | arm64 | thru | 1.87 | libbid | 9.27 | **4.96×** | Rzgsw2 |  |
| zig | sub | NQ | P-gen | arm64 | thru | 5.91 | libbid | 10.68 | **1.81×** | Rzgsw2 |  |
| zig | sub | MQ | P-gen | arm64 | thru | 12.63 | libbid | 8.84 | **0.70×** | Rzgsw2 |  |
| zig | sub | OQ | P-gen | arm64 | thru | 12.86 | libbid | 15.49 | **1.20×** | Rzgsw2 |  |
| zig | sub | FQ | P-gen | arm64 | thru | 7.32 | libbid | 10.19 | **1.39×** | Rzgsw2 |  |
| swift | sub | SQ | P-gen | arm64 | thru | 2.94 | Foundation.Decimal | 317.16 | **107.88×** | Rswsw2 | compact idiom peer |
| swift | sub | NQ | P-gen | arm64 | thru | 5.53 | Foundation.Decimal | 389.53 | **70.44×** | Rswsw2 | compact idiom peer |
| swift | sub | MQ | P-gen | arm64 | thru | 14.60 | Foundation.Decimal | 395.39 | **27.08×** | Rswsw2 | compact idiom peer |
| swift | sub | OQ | P-gen | arm64 | thru | 17.39 | Foundation.Decimal | 521.97 | **30.02×** | Rswsw2 | compact idiom peer |
| swift | sub | FQ | P-gen | arm64 | thru | 12.44 | Foundation.Decimal | 279.66 | **22.48×** | Rswsw2 | compact idiom peer |
| csharp | sub | SQ | P-gen | arm64 | thru | 2.09 | System.Decimal | 2.24 | **1.07×** | Rcssw2 | compact idiom peer |
| csharp | sub | NQ | P-gen | arm64 | thru | 9.18 | System.Decimal | 3.64 | **0.40×** | Rcssw2 | compact idiom peer |
| csharp | sub | MQ | P-gen | arm64 | thru | 17.19 | System.Decimal | 3.53 | **0.21×** | Rcssw2 | compact idiom peer |
| csharp | sub | OQ | P-gen | arm64 | thru | 21.27 | - | - | - | Rcssw2 |  |
| csharp | sub | FQ | P-gen | arm64 | thru | 12.24 | - | - | - | Rcssw2 |  |
| go | sub | SQ | P-gen | arm64 | thru | 3.04 | - | - | - | Rgosw2 |  |
| go | sub | NQ | P-gen | arm64 | thru | 9.52 | - | - | - | Rgosw2 |  |
| go | sub | MQ | P-gen | arm64 | thru | 21.49 | - | - | - | Rgosw2 |  |
| go | sub | OQ | P-gen | arm64 | thru | 32.64 | - | - | - | Rgosw2 |  |
| go | sub | FQ | P-gen | arm64 | thru | 19.87 | - | - | - | Rgosw2 |  |
| java | sub | SQ | P-gen | arm64 | thru‡ | 4.44 | BigDecimal | 23.16 | **5.22×** | Rjasw2 | compact idiom peer |
| java | sub | NQ | P-gen | arm64 | thru‡ | 7.40 | BigDecimal | 32.74 | **4.42×** | Rjasw2 | compact idiom peer |
| java | sub | MQ | P-gen | arm64 | thru‡ | 12.44 | BigDecimal | 31.94 | **2.57×** | Rjasw2 | compact idiom peer |
| java | sub | OQ | P-gen | arm64 | thru‡ | 18.98 | BigDecimal | 77.52 | **4.08×** | Rjasw2 | compact idiom peer |
| java | sub | FQ | P-gen | arm64 | thru‡ | 14.89 | BigDecimal | 90.45 | **6.07×** | Rjasw2 | compact idiom peer |
| kotlin | sub | SQ | P-gen | arm64 | thru‡ | 4.80 | BigDecimal | 22.48 | **4.68×** | Rkosw2 | compact idiom peer |
| kotlin | sub | NQ | P-gen | arm64 | thru‡ | 8.91 | BigDecimal | 33.60 | **3.77×** | Rkosw2 | compact idiom peer |
| kotlin | sub | MQ | P-gen | arm64 | thru‡ | 14.11 | BigDecimal | 32.87 | **2.33×** | Rkosw2 | compact idiom peer |
| kotlin | sub | OQ | P-gen | arm64 | thru‡ | 19.13 | BigDecimal | 79.37 | **4.15×** | Rkosw2 | compact idiom peer |
| kotlin | sub | FQ | P-gen | arm64 | thru‡ | 14.54 | BigDecimal | 95.53 | **6.57×** | Rkosw2 | compact idiom peer |
| python | sub | SQ | P-gen | arm64 | thru | 20.81 | decimal.Decimal | 58.81 | **2.83×** | Rpysw2 | compact idiom peer |
| python | sub | NQ | P-gen | arm64 | thru | 22.63 | decimal.Decimal | 69.10 | **3.05×** | Rpysw2 | compact idiom peer |
| python | sub | MQ | P-gen | arm64 | thru | 32.93 | decimal.Decimal | 70.92 | **2.15×** | Rpysw2 | compact idiom peer |
| python | sub | OQ | P-gen | arm64 | thru | 44.53 | decimal.Decimal | 83.64 | **1.88×** | Rpysw2 | compact idiom peer |
| python | sub | FQ | P-gen | arm64 | thru | 33.51 | decimal.Decimal | 79.90 | **2.38×** | Rpysw2 | compact idiom peer |
| c | sub | SQ | P-gen | arm64 | thru | 1.70 | decQuad | 21.50 | **12.65×** | Rc2 |  |
| c | sub | NQ | P-gen | arm64 | thru | 4.27 | decQuad | 31.58 | **7.40×** | Rc2 |  |
| c | sub | MQ | P-gen | arm64 | thru | 10.65 | decQuad | 32.26 | **3.03×** | Rc2 |  |
| c | sub | OQ | P-gen | arm64 | thru | 12.53 | decQuad | 35.70 | **2.85×** | Rc2 |  |
| c | sub | FQ | P-gen | arm64 | thru | 7.14 | decQuad | 28.11 | **3.94×** | Rc2 |  |
| c | sub | SQ | P-gen | arm64 | thru | 1.70 | mpdecimal | 12.24 | **7.20×** | Rc2 |  |
| c | sub | NQ | P-gen | arm64 | thru | 4.27 | mpdecimal | 27.02 | **6.33×** | Rc2 |  |
| c | sub | MQ | P-gen | arm64 | thru | 10.65 | mpdecimal | 20.61 | **1.94×** | Rc2 |  |
| c | sub | OQ | P-gen | arm64 | thru | 12.53 | mpdecimal | 45.47 | **3.63×** | Rc2 |  |
| c | sub | FQ | P-gen | arm64 | thru | 7.14 | mpdecimal | 39.33 | **5.51×** | Rc2 |  |
<!-- END GENERATED sub-rel -->

**Relational vs peers — x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-x86 -->
| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | sub | SQ | P-gen | x86_64 | thru | 6.84 | libbid | 33.26 | **4.86×** | xRc2 |  |
| c | sub | NQ | P-gen | x86_64 | thru | 11.75 | libbid | 37.58 | **3.20×** | xRc2 |  |
| c | sub | MQ | P-gen | x86_64 | thru | 28.24 | libbid | 34.36 | **1.22×** | xRc2 |  |
| c | sub | OQ | P-gen | x86_64 | thru | 36.47 | libbid | 52.59 | **1.44×** | xRc2 |  |
| c | sub | FQ | P-gen | x86_64 | thru | 28.62 | libbid | 33.84 | **1.18×** | xRc2 |  |
| rust | sub | SQ | P-gen | x86_64 | thru | 7.72 | rust_decimal | 14.50 | **1.88×** | xRrsw2 | compact idiom peer |
| rust | sub | NQ | P-gen | x86_64 | thru | 14.10 | rust_decimal | 19.70 | **1.40×** | xRrsw2 | compact idiom peer |
| rust | sub | MQ | P-gen | x86_64 | thru | 26.02 | rust_decimal | 18.73 | **0.72×** | xRrsw2 | compact idiom peer |
| rust | sub | OQ | P-gen | x86_64 | thru | 38.76 | - | - | - | xRrsw2 |  |
| rust | sub | FQ | P-gen | x86_64 | thru | 22.74 | - | - | - | xRrsw2 |  |
| zig | sub | SQ | P-gen | x86_64 | thru | 8.64 | libbid | 33.26 | **3.85×** | xRzgsw2 |  |
| zig | sub | NQ | P-gen | x86_64 | thru | 16.47 | libbid | 37.58 | **2.28×** | xRzgsw2 |  |
| zig | sub | MQ | P-gen | x86_64 | thru | 26.84 | libbid | 34.36 | **1.28×** | xRzgsw2 |  |
| zig | sub | OQ | P-gen | x86_64 | thru | 36.03 | libbid | 52.59 | **1.46×** | xRzgsw2 |  |
| zig | sub | FQ | P-gen | x86_64 | thru | 22.52 | libbid | 33.84 | **1.50×** | xRzgsw2 |  |
| swift | sub | SQ | P-gen | x86_64 | thru | 7.64 | Foundation.Decimal | 782.22 | **102.38×** | xRswsw2 | compact idiom peer |
| swift | sub | NQ | P-gen | x86_64 | thru | 13.66 | Foundation.Decimal | 942.36 | **68.99×** | xRswsw2 | compact idiom peer |
| swift | sub | MQ | P-gen | x86_64 | thru | 30.85 | Foundation.Decimal | 947.71 | **30.72×** | xRswsw2 | compact idiom peer |
| swift | sub | OQ | P-gen | x86_64 | thru | 40.29 | Foundation.Decimal | 1285.15 | **31.90×** | xRswsw2 | compact idiom peer |
| swift | sub | FQ | P-gen | x86_64 | thru | 29.67 | Foundation.Decimal | 631.47 | **21.28×** | xRswsw2 | compact idiom peer |
| csharp | sub | SQ | P-gen | x86_64 | thru | 9.67 | System.Decimal | 11.79 | **1.22×** | xRcssw2 | compact idiom peer |
| csharp | sub | NQ | P-gen | x86_64 | thru | 23.41 | System.Decimal | 15.03 | **0.64×** | xRcssw2 | compact idiom peer |
| csharp | sub | MQ | P-gen | x86_64 | thru | 53.12 | System.Decimal | 13.76 | **0.26×** | xRcssw2 | compact idiom peer |
| csharp | sub | OQ | P-gen | x86_64 | thru | 68.74 | - | - | - | xRcssw2 |  |
| csharp | sub | FQ | P-gen | x86_64 | thru | 41.07 | - | - | - | xRcssw2 |  |
| go | sub | SQ | P-gen | x86_64 | thru | 9.35 | - | - | - | xRgosw2 |  |
| go | sub | NQ | P-gen | x86_64 | thru | 16.87 | - | - | - | xRgosw2 |  |
| go | sub | MQ | P-gen | x86_64 | thru | 41.05 | - | - | - | xRgosw2 |  |
| go | sub | OQ | P-gen | x86_64 | thru | 63.51 | - | - | - | xRgosw2 |  |
| go | sub | FQ | P-gen | x86_64 | thru | 38.87 | - | - | - | xRgosw2 |  |
| java | sub | SQ | P-gen | x86_64 | thru‡ | 13.40 | BigDecimal | 58.47 | **4.36×** | xRjasw2 | compact idiom peer |
| java | sub | NQ | P-gen | x86_64 | thru‡ | 20.60 | BigDecimal | 87.66 | **4.26×** | xRjasw2 | compact idiom peer |
| java | sub | MQ | P-gen | x86_64 | thru‡ | 36.79 | BigDecimal | 91.66 | **2.49×** | xRjasw2 | compact idiom peer |
| java | sub | OQ | P-gen | x86_64 | thru‡ | 61.14 | BigDecimal | 175.68 | **2.87×** | xRjasw2 | compact idiom peer |
| java | sub | FQ | P-gen | x86_64 | thru‡ | 40.60 | BigDecimal | 199.80 | **4.92×** | xRjasw2 | compact idiom peer |
| kotlin | sub | SQ | P-gen | x86_64 | thru‡ | 15.32 | BigDecimal | 63.83 | **4.17×** | xRkosw2 | compact idiom peer |
| kotlin | sub | NQ | P-gen | x86_64 | thru‡ | 25.64 | BigDecimal | 90.47 | **3.53×** | xRkosw2 | compact idiom peer |
| kotlin | sub | MQ | P-gen | x86_64 | thru‡ | 46.32 | BigDecimal | 99.34 | **2.14×** | xRkosw2 | compact idiom peer |
| kotlin | sub | OQ | P-gen | x86_64 | thru‡ | 66.18 | BigDecimal | 176.54 | **2.67×** | xRkosw2 | compact idiom peer |
| kotlin | sub | FQ | P-gen | x86_64 | thru‡ | 42.79 | BigDecimal | 211.15 | **4.93×** | xRkosw2 | compact idiom peer |
| python | sub | SQ | P-gen | x86_64 | thru | 51.26 | decimal.Decimal | 118.02 | **2.30×** | xRpysw2 | compact idiom peer |
| python | sub | NQ | P-gen | x86_64 | thru | 53.81 | decimal.Decimal | 139.05 | **2.58×** | xRpysw2 | compact idiom peer |
| python | sub | MQ | P-gen | x86_64 | thru | 68.59 | decimal.Decimal | 140.00 | **2.04×** | xRpysw2 | compact idiom peer |
| python | sub | OQ | P-gen | x86_64 | thru | 77.70 | decimal.Decimal | 166.32 | **2.14×** | xRpysw2 | compact idiom peer |
| python | sub | FQ | P-gen | x86_64 | thru | 71.00 | decimal.Decimal | 162.63 | **2.29×** | xRpysw2 | compact idiom peer |
| c | sub | SQ | P-gen | x86_64 | thru | 6.84 | decQuad | 56.95 | **8.33×** | xRc2 |  |
| c | sub | NQ | P-gen | x86_64 | thru | 11.75 | decQuad | 85.53 | **7.28×** | xRc2 |  |
| c | sub | MQ | P-gen | x86_64 | thru | 28.24 | decQuad | 82.17 | **2.91×** | xRc2 |  |
| c | sub | OQ | P-gen | x86_64 | thru | 36.47 | decQuad | 95.09 | **2.61×** | xRc2 |  |
| c | sub | FQ | P-gen | x86_64 | thru | 28.62 | decQuad | 74.97 | **2.62×** | xRc2 |  |
| c | sub | SQ | P-gen | x86_64 | thru | 6.84 | mpdecimal | 36.46 | **5.33×** | xRc2 |  |
| c | sub | NQ | P-gen | x86_64 | thru | 11.75 | mpdecimal | 54.87 | **4.67×** | xRc2 |  |
| c | sub | MQ | P-gen | x86_64 | thru | 28.24 | mpdecimal | 54.74 | **1.94×** | xRc2 |  |
| c | sub | OQ | P-gen | x86_64 | thru | 36.47 | mpdecimal | 126.85 | **3.48×** | xRc2 |  |
| c | sub | FQ | P-gen | x86_64 | thru | 28.62 | mpdecimal | 85.83 | **3.00×** | xRc2 |  |
<!-- END GENERATED sub-rel-x86 -->

## 3. Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared
`decimal128-resources/swept/P-gen/` corpus, byte-identical operands every port). arm64
(M3 Pro); JVM `‡` = escape-forced alloc-inclusive. **Two views:** the compact d128
matrices (band shape — the flat compact multiply vs the scaling wide paths), then the
relational peer table (explicit ratios). Only the full-width peers — **libbid / decQuad /
mpdecimal** (measured in C, valid for every port since operands are identical) — can
represent the wide WP/XP products; the 28-digit compact peers run only the compact **CP**
band — `rust_decimal`, `System.Decimal`, and `BigDecimal` appear inline in the relational
tables where representable.

**P-gen — d128 (ns/op).** **CP** is the **compact** product (≤34 digits, **no scaling** —
the cheap multiply); **WP** scales via the 128-bit `recipMulPow10`; **XP** via the 256-bit
kernel.

<!-- BEGIN GENERATED mul-pgen -->
| port | mul CP | mul WP | mul XP |
|------|-------:|-------:|-------:|
| c      |  2.14 | 19.64 | 26.16 |
| rust   |  1.51 | 13.69 | 24.06 |
| zig    |  3.43 | 18.08 | 24.62 |
| swift  |  4.01 | 19.87 | 26.31 |
| csharp |  2.19 | 21.67 | 46.34 |
| go     |  2.78 | 27.70 | 40.16 |
| java‡  |  5.04 | 20.37 | 44.81 |
| kotlin‡|  4.98 | 16.44 | 46.14 |
| python | 20.63 | 45.56 | 73.63 |
<!-- END GENERATED mul-pgen -->

**P-gen — d128 (ns/op) — x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-pgen-x86 -->
| port | mul CP | mul WP | mul XP |
|------|-------:|-------:|-------:|
| c      |  6.05 | 34.47 |  47.81 |
| rust   |  5.04 | 29.13 |  43.50 |
| zig    |  7.63 | 28.83 |  42.87 |
| swift  |  6.58 | 35.19 |  52.27 |
| csharp |  8.58 | 51.34 |  88.88 |
| go     |  6.96 | 49.37 |  71.01 |
| java‡  | 13.47 | 52.25 |  77.62 |
| kotlin‡| 14.25 | 47.77 |  85.09 |
| python | 43.93 | 78.07 | 106.03 |
<!-- END GENERATED mul-pgen-x86 -->

C's `mul XP` 36.56 predates the `Finalize.c` wide-product finalize fix (commit d98fd85);
the post-fix swept re-measure lands at **29.4** (P-max matrix above) — the one swept number
still due a refresh.

**P-max — d128 (ns/op).** Only XP is feasible at 33–34 digits:

<!-- BEGIN GENERATED mul-pmax -->
| port | mul XP |
|------|-------:|
| c      | 28.16 |
| rust   | 28.05 |
| zig    | 25.16 |
| swift  | 29.65 |
| csharp | 46.11 |
| go     | 42.49 |
| java‡  | 44.19 |
| kotlin‡| 44.63 |
| python | 94.46 |
<!-- END GENERATED mul-pmax -->

**P-max — d128 (ns/op) — x86_64 (stress).**

<!-- BEGIN GENERATED mul-pmax-x86 -->
| port | mul XP |
|------|-------:|
| c      |  47.19 |
| rust   |  47.08 |
| zig    |  44.59 |
| swift  |  49.93 |
| csharp |  86.61 |
| go     |  82.17 |
| java‡  |  70.43 |
| kotlin‡| 117.75 |
| python | 122.50 |
<!-- END GENERATED mul-pmax-x86 -->

**Relational — d128 vs the universal reference `libbid`** (Intel BID, measured in the C
arm on the identical swept operands ⇒ valid for every port; ratio = libbid/ours, ≥1 ⇒ d128
faster). C additionally vs decQuad (DPD) and mpdecimal. **The ratio carries each port's own
harness/packaging term** (Swift `opaque()`, Go backend, …), since d128 is timed in-port and
the peers in C (libbid/decQuad run `Rc`, mpdecimal run `Rmpd`). rust adds its compact idiom
peer `rust_decimal` on the CP band. java/kotlin + BigDecimal pending.

<!-- BEGIN GENERATED mul-rel -->
| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | mul | CP | P-gen | arm64 | thru | 2.14 | libbid | 23.17 | **10.83×** | Rc2 | **no scaling** — the cheap multiply |
| c | mul | WP | P-gen | arm64 | thru | 19.64 | libbid | 33.43 | **1.70×** | Rc2 | 128-bit recipMulPow10 |
| c | mul | XP | P-gen | arm64 | thru | 26.16 | libbid | 42.83 | **1.64×** | Rc2 | 256-bit recipMulPow10; **1.19× ≈ the recipmul-256 work-order's 1.18–1.54× band** |
| rust | mul | CP | P-gen | arm64 | thru | 1.51 | libbid | 23.17 | **15.34×** | Rrsw2 |  |
| rust | mul | WP | P-gen | arm64 | thru | 13.69 | libbid | 33.43 | **2.44×** | Rrsw2 |  |
| rust | mul | XP | P-gen | arm64 | thru | 24.06 | libbid | 42.83 | **1.78×** | Rrsw2 |  |
| zig | mul | CP | P-gen | arm64 | thru | 3.43 | libbid | 23.17 | **6.76×** | Rzgsw2 |  |
| zig | mul | WP | P-gen | arm64 | thru | 18.08 | libbid | 33.43 | **1.85×** | Rzgsw2 |  |
| zig | mul | XP | P-gen | arm64 | thru | 24.62 | libbid | 42.83 | **1.74×** | Rzgsw2 |  |
| swift | mul | CP | P-gen | arm64 | thru | 4.01 | Foundation.Decimal | 275.76 | **68.77×** | Rswsw2 | compact idiom peer |
| swift | mul | WP | P-gen | arm64 | thru | 19.87 | Foundation.Decimal | 293.26 | **14.76×** | Rswsw2 | compact idiom peer |
| swift | mul | XP | P-gen | arm64 | thru | 26.31 | Foundation.Decimal | 788.50 | **29.97×** | Rswsw2 | compact idiom peer |
| csharp | mul | CP | P-gen | arm64 | thru | 2.19 | - | - | - | Rcssw2 |  |
| csharp | mul | WP | P-gen | arm64 | thru | 21.67 | - | - | - | Rcssw2 |  |
| csharp | mul | XP | P-gen | arm64 | thru | 46.34 | - | - | - | Rcssw2 |  |
| go | mul | CP | P-gen | arm64 | thru | 2.78 | - | - | - | Rgosw2 |  |
| go | mul | WP | P-gen | arm64 | thru | 27.70 | - | - | - | Rgosw2 |  |
| go | mul | XP | P-gen | arm64 | thru | 40.16 | - | - | - | Rgosw2 |  |
| java | mul | CP | P-gen | arm64 | thru‡ | 5.04 | BigDecimal | 11.91 | **2.36×** | Rjasw2 | compact idiom peer |
| java | mul | WP | P-gen | arm64 | thru‡ | 20.37 | BigDecimal | 57.82 | **2.84×** | Rjasw2 | compact idiom peer |
| java | mul | XP | P-gen | arm64 | thru‡ | 44.81 | BigDecimal | 159.30 | **3.56×** | Rjasw2 | compact idiom peer |
| kotlin | mul | CP | P-gen | arm64 | thru‡ | 4.98 | BigDecimal | 11.84 | **2.38×** | Rkosw2 | compact idiom peer |
| kotlin | mul | WP | P-gen | arm64 | thru‡ | 16.44 | BigDecimal | 59.17 | **3.60×** | Rkosw2 | compact idiom peer |
| kotlin | mul | XP | P-gen | arm64 | thru‡ | 46.14 | BigDecimal | 152.99 | **3.32×** | Rkosw2 | compact idiom peer |
| python | mul | CP | P-gen | arm64 | thru | 20.63 | decimal.Decimal | 62.58 | **3.03×** | Rpysw2 | compact idiom peer |
| python | mul | WP | P-gen | arm64 | thru | 45.56 | decimal.Decimal | 71.94 | **1.58×** | Rpysw2 | compact idiom peer |
| python | mul | XP | P-gen | arm64 | thru | 73.63 | decimal.Decimal | 88.86 | **1.21×** | Rpysw2 | compact idiom peer |
| c | mul | CP | P-gen | arm64 | thru | 2.14 | decQuad | 21.97 | **10.27×** | Rc2 | vs DPD |
| c | mul | WP | P-gen | arm64 | thru | 19.64 | decQuad | 29.02 | **1.48×** | Rc2 | vs DPD |
| c | mul | XP | P-gen | arm64 | thru | 26.16 | decQuad | 30.88 | **1.18×** | Rc2 | **decQuad edges d128 on the widest product** (software DPD's flat cost; libbid still slower) |
| c | mul | CP | P-gen | arm64 | thru | 2.14 | mpdecimal | 22.98 | **10.74×** | Rc2 | no-scale multiply vs libmpdec |
| c | mul | WP | P-gen | arm64 | thru | 19.64 | mpdecimal | 53.52 | **2.73×** | Rc2 | 128-bit recipMulPow10 |
| c | mul | XP | P-gen | arm64 | thru | 26.16 | mpdecimal | 72.93 | **2.79×** | Rc2 | **d128 wins the widest product vs libmpdec** (unlike decQuad) |
<!-- END GENERATED mul-rel -->

**Relational vs peers — x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-x86 -->
| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | mul | CP | P-gen | x86_64 | thru | 6.05 | libbid | 46.01 | **7.60×** | xRc2 |  |
| c | mul | WP | P-gen | x86_64 | thru | 34.47 | libbid | 65.78 | **1.91×** | xRc2 |  |
| c | mul | XP | P-gen | x86_64 | thru | 47.81 | libbid | 93.50 | **1.96×** | xRc2 |  |
| rust | mul | CP | P-gen | x86_64 | thru | 5.04 | libbid | 46.01 | **9.13×** | xRrsw2 |  |
| rust | mul | WP | P-gen | x86_64 | thru | 29.13 | libbid | 65.78 | **2.26×** | xRrsw2 |  |
| rust | mul | XP | P-gen | x86_64 | thru | 43.50 | libbid | 93.50 | **2.15×** | xRrsw2 |  |
| zig | mul | CP | P-gen | x86_64 | thru | 7.63 | libbid | 46.01 | **6.03×** | xRzgsw2 |  |
| zig | mul | WP | P-gen | x86_64 | thru | 28.83 | libbid | 65.78 | **2.28×** | xRzgsw2 |  |
| zig | mul | XP | P-gen | x86_64 | thru | 42.87 | libbid | 93.50 | **2.18×** | xRzgsw2 |  |
| swift | mul | CP | P-gen | x86_64 | thru | 6.58 | Foundation.Decimal | 668.66 | **101.62×** | xRswsw2 | compact idiom peer |
| swift | mul | WP | P-gen | x86_64 | thru | 35.19 | Foundation.Decimal | 757.66 | **21.53×** | xRswsw2 | compact idiom peer |
| swift | mul | XP | P-gen | x86_64 | thru | 52.27 | Foundation.Decimal | 1952.38 | **37.35×** | xRswsw2 | compact idiom peer |
| csharp | mul | CP | P-gen | x86_64 | thru | 8.58 | - | - | - | xRcssw2 |  |
| csharp | mul | WP | P-gen | x86_64 | thru | 51.34 | - | - | - | xRcssw2 |  |
| csharp | mul | XP | P-gen | x86_64 | thru | 88.88 | - | - | - | xRcssw2 |  |
| go | mul | CP | P-gen | x86_64 | thru | 6.96 | - | - | - | xRgosw2 |  |
| go | mul | WP | P-gen | x86_64 | thru | 49.37 | - | - | - | xRgosw2 |  |
| go | mul | XP | P-gen | x86_64 | thru | 71.01 | - | - | - | xRgosw2 |  |
| java | mul | CP | P-gen | x86_64 | thru‡ | 13.47 | BigDecimal | 39.78 | **2.95×** | xRjasw2 | compact idiom peer |
| java | mul | WP | P-gen | x86_64 | thru‡ | 52.25 | BigDecimal | 151.62 | **2.90×** | xRjasw2 | compact idiom peer |
| java | mul | XP | P-gen | x86_64 | thru‡ | 77.62 | BigDecimal | 267.55 | **3.45×** | xRjasw2 | compact idiom peer |
| kotlin | mul | CP | P-gen | x86_64 | thru‡ | 14.25 | BigDecimal | 41.18 | **2.89×** | xRkosw2 | compact idiom peer |
| kotlin | mul | WP | P-gen | x86_64 | thru‡ | 47.77 | BigDecimal | 156.34 | **3.27×** | xRkosw2 | compact idiom peer |
| kotlin | mul | XP | P-gen | x86_64 | thru‡ | 85.09 | BigDecimal | 271.84 | **3.19×** | xRkosw2 | compact idiom peer |
| python | mul | CP | P-gen | x86_64 | thru | 43.93 | decimal.Decimal | 115.24 | **2.62×** | xRpysw2 | compact idiom peer |
| python | mul | WP | P-gen | x86_64 | thru | 78.07 | decimal.Decimal | 135.19 | **1.73×** | xRpysw2 | compact idiom peer |
| python | mul | XP | P-gen | x86_64 | thru | 106.03 | decimal.Decimal | 159.61 | **1.51×** | xRpysw2 | compact idiom peer |
| c | mul | CP | P-gen | x86_64 | thru | 6.05 | decQuad | 59.43 | **9.82×** | xRc2 |  |
| c | mul | WP | P-gen | x86_64 | thru | 34.47 | decQuad | 71.43 | **2.07×** | xRc2 |  |
| c | mul | XP | P-gen | x86_64 | thru | 47.81 | decQuad | 87.01 | **1.82×** | xRc2 |  |
| c | mul | CP | P-gen | x86_64 | thru | 6.05 | mpdecimal | 63.68 | **10.53×** | xRc2 |  |
| c | mul | WP | P-gen | x86_64 | thru | 34.47 | mpdecimal | 180.69 | **5.24×** | xRc2 |  |
| c | mul | XP | P-gen | x86_64 | thru | 47.81 | mpdecimal | 231.72 | **4.85×** | xRc2 |  |
<!-- END GENERATED mul-rel-x86 -->

## 4. Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; same shared `swept/P-gen/` corpus and
conventions as §3). arm64 (M3 Pro); JVM `‡` = escape-forced. **Two views:** the compact
d128 matrices, then the relational peer table. Bands: **CD** small divisor (1–4 digits,
128÷64 quotient-first, §2.4.10), **WD** (5–19 digits, 256÷64), **XD** (20–34 digits,
256÷128 Möller–Granlund), **ET** exact/terminating early-out (integer-divide `cx/cy`,
`R0==0` ⇒ no rounding/strip), **PT** power-of-ten divisor (`divPow10Divisor` exponent-only
fast path, §2.4.9). d128's **compact-divide weakness** shows at CD/WD (≈ parity / slight
loss vs libbid; ~8–13% run-to-run drift, libbid control stable); the **ET/PT early-outs win
clean**. Peers: libbid/decQuad/mpdecimal (C, universal); rust adds `rust_decimal` on the
CD/PT compact bands.

**P-gen — d128 (ns/op).**

<!-- BEGIN GENERATED div-pgen -->
| port | div CD | div WD | div XD | div ET | div PT |
|------|-------:|-------:|-------:|-------:|-------:|
| c      | 41.70 | 39.15 | 37.09 |  8.00 |  3.17 |
| rust   | 25.07 | 33.34 | 37.88 |  9.47 |  3.97 |
| zig    | 37.00 | 40.91 | 32.25 | 10.35 |  4.24 |
| swift  | 33.80 | 44.86 | 41.39 |  8.09 | 10.82 |
| csharp | 37.50 | 48.71 | 62.03 | 22.57 |  5.24 |
| go     | 44.84 | 61.95 | 53.39 | 14.78 |  6.68 |
| java‡  | 24.60 | 36.42 | 37.66 | 12.36 |  8.57 |
| kotlin‡| 25.54 | 37.01 | 37.64 | 16.26 |  9.33 |
| python | 66.43 | 71.20 | 73.00 | 25.17 | 19.43 |
<!-- END GENERATED div-pgen -->

**P-gen — d128 (ns/op) — x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-pgen-x86 -->
| port | div CD | div WD | div XD | div ET | div PT |
|------|-------:|-------:|-------:|-------:|-------:|
| c      |  84.26 |  87.22 |  78.01 | 31.38 |  7.54 |
| rust   |  69.75 |  81.09 |  82.93 | 28.42 |  9.53 |
| zig    |  70.40 |  88.46 |  75.69 | 32.00 | 11.97 |
| swift  |  71.21 |  90.52 |  92.24 | 29.90 | 11.97 |
| csharp |  90.89 | 105.72 | 112.44 | 42.67 | 12.48 |
| go     | 104.80 | 125.20 | 111.10 | 36.01 | 12.93 |
| java‡  |  87.51 | 113.52 | 120.99 | 45.60 | 23.29 |
| kotlin‡|  95.05 | 120.83 | 133.07 | 52.46 | 27.10 |
| python | 117.35 | 130.99 | 131.17 | 72.07 | 46.90 |
<!-- END GENERATED div-pgen-x86 -->

The C swept **PT** (3.16) is the coeff-1 (`1E3`) trivial encoding — ≡ the native ports'
`PT1`; the coeff-10ᵏ (`1000`) strip form runs ~10.5 ns (run `Rpt`). swift's swept PT (11.04)
is the strip form.

**P-max — d128 (ns/op).** Only XD is feasible at 33–34-digit divisors:

<!-- BEGIN GENERATED div-pmax -->
| port | div XD |
|------|-------:|
| c      | 32.23 |
| rust   | 40.30 |
| zig    | 32.60 |
| swift  | 39.85 |
| csharp | 58.50 |
| go     | 54.47 |
| java‡  | 29.51 |
| kotlin‡| 32.89 |
| python | 70.39 |
<!-- END GENERATED div-pmax -->

**P-max — d128 (ns/op) — x86_64 (stress).**

<!-- BEGIN GENERATED div-pmax-x86 -->
| port | div XD |
|------|-------:|
| c      |  72.46 |
| rust   |  75.61 |
| zig    |  68.43 |
| swift  |  91.13 |
| csharp | 108.54 |
| go     | 116.00 |
| java‡  |  91.81 |
| kotlin‡| 131.04 |
| python | 125.25 |
<!-- END GENERATED div-pmax-x86 -->

The **JVM 128-bit divide is competitive-to-ahead** here — HotSpot runs `div XD` at
28.4/31.4 (java/kotlin), *faster* than the LLVM natives' ~40.

**Relational — d128 vs the universal reference `libbid`** (measured in the C arm on the
identical swept operands ⇒ valid for every port; ratio = libbid/ours, ≥1 ⇒ d128 faster). C
additionally vs decQuad (DPD) and mpdecimal. The ratio carries each port's own
harness/packaging term, since d128 is timed in-port and the peers in C (libbid/decQuad run
`Rc`, mpdecimal run `Rmpd`). rust adds its compact idiom peer `rust_decimal`. java/kotlin +
BigDecimal pending.

<!-- BEGIN GENERATED div-rel -->
| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | div | CD | P-gen | arm64 | thru | 41.70 | libbid | 37.17 | **0.89×** | Rc2 | 128÷64 quotient-first (§2.4.10); **libbid wins** — the compact-divide weakness persists |
| c | div | WD | P-gen | arm64 | thru | 39.15 | libbid | 38.82 | **0.99×** | Rc2 | 256÷64; **≈ parity / slight loss** |
| c | div | XD | P-gen | arm64 | thru | 37.09 | libbid | 39.22 | **1.06×** | Rc2 | 256÷128 Möller–Granlund |
| c | div | ET | P-gen | arm64 | thru | 8.00 | libbid | 11.20 | **1.40×** | Rc2 | **quotient-first exact early-out** — beats libbid's exact fast path |
| c | div | PT | P-gen | arm64 | thru | 3.17 | libbid | 11.86 | **3.74×** | Rc2 | `divPow10Divisor` (§2.4.9); **d128's fastest divide** (coeff-1 form) |
| rust | div | CD | P-gen | arm64 | thru | 25.07 | libbid | 37.17 | **1.48×** | Rrsw2 |  |
| rust | div | WD | P-gen | arm64 | thru | 33.34 | libbid | 38.82 | **1.16×** | Rrsw2 |  |
| rust | div | XD | P-gen | arm64 | thru | 37.88 | libbid | 39.22 | **1.04×** | Rrsw2 |  |
| rust | div | ET | P-gen | arm64 | thru | 9.47 | libbid | 11.20 | **1.18×** | Rrsw2 |  |
| rust | div | PT | P-gen | arm64 | thru | 3.97 | libbid | 11.86 | **2.99×** | Rrsw2 |  |
| zig | div | CD | P-gen | arm64 | thru | 37.00 | libbid | 37.17 | **1.00×** | Rzgsw2 |  |
| zig | div | WD | P-gen | arm64 | thru | 40.91 | libbid | 38.82 | **0.95×** | Rzgsw2 |  |
| zig | div | XD | P-gen | arm64 | thru | 32.25 | libbid | 39.22 | **1.22×** | Rzgsw2 |  |
| zig | div | ET | P-gen | arm64 | thru | 10.35 | libbid | 11.20 | **1.08×** | Rzgsw2 |  |
| zig | div | PT | P-gen | arm64 | thru | 4.24 | libbid | 11.86 | **2.80×** | Rzgsw2 |  |
| swift | div | CD | P-gen | arm64 | thru | 33.80 | Foundation.Decimal | 1274.64 | **37.71×** | Rswsw2 | compact idiom peer |
| swift | div | WD | P-gen | arm64 | thru | 44.86 | Foundation.Decimal | 836.86 | **18.65×** | Rswsw2 | compact idiom peer |
| swift | div | XD | P-gen | arm64 | thru | 41.39 | Foundation.Decimal | 639.64 | **15.45×** | Rswsw2 | compact idiom peer |
| swift | div | ET | P-gen | arm64 | thru | 8.09 | Foundation.Decimal | 2997.74 | **370.55×** | Rswsw2 | compact idiom peer |
| swift | div | PT | P-gen | arm64 | thru | 10.82 | Foundation.Decimal | 2906.31 | **268.61×** | Rswsw2 | compact idiom peer |
| csharp | div | CD | P-gen | arm64 | thru | 37.50 | - | - | - | Rcssw2 |  |
| csharp | div | WD | P-gen | arm64 | thru | 48.71 | - | - | - | Rcssw2 |  |
| csharp | div | XD | P-gen | arm64 | thru | 62.03 | - | - | - | Rcssw2 |  |
| csharp | div | ET | P-gen | arm64 | thru | 22.57 | - | - | - | Rcssw2 |  |
| csharp | div | PT | P-gen | arm64 | thru | 5.24 | - | - | - | Rcssw2 |  |
| go | div | CD | P-gen | arm64 | thru | 44.84 | - | - | - | Rgosw2 |  |
| go | div | WD | P-gen | arm64 | thru | 61.95 | - | - | - | Rgosw2 |  |
| go | div | XD | P-gen | arm64 | thru | 53.39 | - | - | - | Rgosw2 |  |
| go | div | ET | P-gen | arm64 | thru | 14.78 | - | - | - | Rgosw2 |  |
| go | div | PT | P-gen | arm64 | thru | 6.68 | - | - | - | Rgosw2 |  |
| java | div | CD | P-gen | arm64 | thru‡ | 24.60 | BigDecimal | 145.87 | **5.93×** | Rjasw2 | compact idiom peer |
| java | div | WD | P-gen | arm64 | thru‡ | 36.42 | BigDecimal | 98.74 | **2.71×** | Rjasw2 | compact idiom peer |
| java | div | XD | P-gen | arm64 | thru‡ | 37.66 | BigDecimal | 247.99 | **6.58×** | Rjasw2 | compact idiom peer |
| java | div | ET | P-gen | arm64 | thru‡ | 12.36 | BigDecimal | 486.31 | **39.35×** | Rjasw2 | compact idiom peer |
| java | div | PT | P-gen | arm64 | thru‡ | 8.57 | BigDecimal | 447.67 | **52.24×** | Rjasw2 | compact idiom peer |
| kotlin | div | CD | P-gen | arm64 | thru‡ | 25.54 | BigDecimal | 144.82 | **5.67×** | Rkosw2 | compact idiom peer |
| kotlin | div | WD | P-gen | arm64 | thru‡ | 37.01 | BigDecimal | 118.07 | **3.19×** | Rkosw2 | compact idiom peer |
| kotlin | div | XD | P-gen | arm64 | thru‡ | 37.64 | BigDecimal | 213.64 | **5.68×** | Rkosw2 | compact idiom peer |
| kotlin | div | ET | P-gen | arm64 | thru‡ | 16.26 | BigDecimal | 468.55 | **28.82×** | Rkosw2 | compact idiom peer |
| kotlin | div | PT | P-gen | arm64 | thru‡ | 9.33 | BigDecimal | 435.17 | **46.64×** | Rkosw2 | compact idiom peer |
| python | div | CD | P-gen | arm64 | thru | 66.43 | decimal.Decimal | 98.30 | **1.48×** | Rpysw2 | compact idiom peer |
| python | div | WD | P-gen | arm64 | thru | 71.20 | decimal.Decimal | 99.15 | **1.39×** | Rpysw2 | compact idiom peer |
| python | div | XD | P-gen | arm64 | thru | 73.00 | decimal.Decimal | 160.27 | **2.20×** | Rpysw2 | compact idiom peer |
| python | div | ET | P-gen | arm64 | thru | 25.17 | decimal.Decimal | 90.58 | **3.60×** | Rpysw2 | compact idiom peer |
| python | div | PT | P-gen | arm64 | thru | 19.43 | decimal.Decimal | 88.58 | **4.56×** | Rpysw2 | compact idiom peer |
| c | div | CD | P-gen | arm64 | thru | 41.70 | decQuad | 71.62 | **1.72×** | Rc2 | vs DPD |
| c | div | WD | P-gen | arm64 | thru | 39.15 | decQuad | 118.30 | **3.02×** | Rc2 | vs DPD |
| c | div | XD | P-gen | arm64 | thru | 37.09 | decQuad | 174.74 | **4.71×** | Rc2 | vs DPD — decNumber divide is slow |
| c | div | ET | P-gen | arm64 | thru | 8.00 | decQuad | 45.65 | **5.71×** | Rc2 | vs DPD |
| c | div | PT | P-gen | arm64 | thru | 3.17 | decQuad | 43.47 | **13.71×** | Rc2 | vs DPD |
| c | div | CD | P-gen | arm64 | thru | 41.70 | mpdecimal | 61.16 | **1.47×** | Rc2 | **narrowest divide gap** (libmpdec's compact divide is its cheapest, like d128's weakness) |
| c | div | WD | P-gen | arm64 | thru | 39.15 | mpdecimal | 91.17 | **2.33×** | Rc2 | 256÷64 |
| c | div | XD | P-gen | arm64 | thru | 37.09 | mpdecimal | 143.98 | **3.88×** | Rc2 | Cowlishaw signature (CD 59 < WD 87 < XD 144) |
| c | div | ET | P-gen | arm64 | thru | 8.00 | mpdecimal | 57.52 | **7.19×** | Rc2 | libmpdec has no exact early-out |
| c | div | PT | P-gen | arm64 | thru | 3.17 | mpdecimal | 48.00 | **15.14×** | Rc2 | **d128's biggest divide win vs libmpdec** |
<!-- END GENERATED div-rel -->

**Relational vs peers — x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-x86 -->
| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | div | CD | P-gen | x86_64 | thru | 84.26 | libbid | 83.32 | **0.99×** | xRc2 |  |
| c | div | WD | P-gen | x86_64 | thru | 87.22 | libbid | 80.97 | **0.93×** | xRc2 |  |
| c | div | XD | P-gen | x86_64 | thru | 78.01 | libbid | 82.59 | **1.06×** | xRc2 |  |
| c | div | ET | P-gen | x86_64 | thru | 31.38 | libbid | 32.18 | **1.03×** | xRc2 |  |
| c | div | PT | P-gen | x86_64 | thru | 7.54 | libbid | 30.53 | **4.05×** | xRc2 |  |
| rust | div | CD | P-gen | x86_64 | thru | 69.75 | libbid | 83.32 | **1.19×** | xRrsw2 |  |
| rust | div | WD | P-gen | x86_64 | thru | 81.09 | libbid | 80.97 | **1.00×** | xRrsw2 |  |
| rust | div | XD | P-gen | x86_64 | thru | 82.93 | libbid | 82.59 | **1.00×** | xRrsw2 |  |
| rust | div | ET | P-gen | x86_64 | thru | 28.42 | libbid | 32.18 | **1.13×** | xRrsw2 |  |
| rust | div | PT | P-gen | x86_64 | thru | 9.53 | libbid | 30.53 | **3.20×** | xRrsw2 |  |
| zig | div | CD | P-gen | x86_64 | thru | 70.40 | libbid | 83.32 | **1.18×** | xRzgsw2 |  |
| zig | div | WD | P-gen | x86_64 | thru | 88.46 | libbid | 80.97 | **0.92×** | xRzgsw2 |  |
| zig | div | XD | P-gen | x86_64 | thru | 75.69 | libbid | 82.59 | **1.09×** | xRzgsw2 |  |
| zig | div | ET | P-gen | x86_64 | thru | 32.00 | libbid | 32.18 | **1.01×** | xRzgsw2 |  |
| zig | div | PT | P-gen | x86_64 | thru | 11.97 | libbid | 30.53 | **2.55×** | xRzgsw2 |  |
| swift | div | CD | P-gen | x86_64 | thru | 71.21 | Foundation.Decimal | 3085.61 | **43.33×** | xRswsw2 | compact idiom peer |
| swift | div | WD | P-gen | x86_64 | thru | 90.52 | Foundation.Decimal | 1983.19 | **21.91×** | xRswsw2 | compact idiom peer |
| swift | div | XD | P-gen | x86_64 | thru | 92.24 | Foundation.Decimal | 1482.03 | **16.07×** | xRswsw2 | compact idiom peer |
| swift | div | ET | P-gen | x86_64 | thru | 29.90 | Foundation.Decimal | 7029.82 | **235.11×** | xRswsw2 | compact idiom peer |
| swift | div | PT | P-gen | x86_64 | thru | 11.97 | Foundation.Decimal | 6822.38 | **569.96×** | xRswsw2 | compact idiom peer |
| csharp | div | CD | P-gen | x86_64 | thru | 90.89 | - | - | - | xRcssw2 |  |
| csharp | div | WD | P-gen | x86_64 | thru | 105.72 | - | - | - | xRcssw2 |  |
| csharp | div | XD | P-gen | x86_64 | thru | 112.44 | - | - | - | xRcssw2 |  |
| csharp | div | ET | P-gen | x86_64 | thru | 42.67 | - | - | - | xRcssw2 |  |
| csharp | div | PT | P-gen | x86_64 | thru | 12.48 | - | - | - | xRcssw2 |  |
| go | div | CD | P-gen | x86_64 | thru | 104.80 | - | - | - | xRgosw2 |  |
| go | div | WD | P-gen | x86_64 | thru | 125.20 | - | - | - | xRgosw2 |  |
| go | div | XD | P-gen | x86_64 | thru | 111.10 | - | - | - | xRgosw2 |  |
| go | div | ET | P-gen | x86_64 | thru | 36.01 | - | - | - | xRgosw2 |  |
| go | div | PT | P-gen | x86_64 | thru | 12.93 | - | - | - | xRgosw2 |  |
| java | div | CD | P-gen | x86_64 | thru‡ | 87.51 | BigDecimal | 354.02 | **4.05×** | xRjasw2 | compact idiom peer |
| java | div | WD | P-gen | x86_64 | thru‡ | 113.52 | BigDecimal | 251.50 | **2.22×** | xRjasw2 | compact idiom peer |
| java | div | XD | P-gen | x86_64 | thru‡ | 120.99 | BigDecimal | 339.59 | **2.81×** | xRjasw2 | compact idiom peer |
| java | div | ET | P-gen | x86_64 | thru‡ | 45.60 | BigDecimal | 1097.38 | **24.07×** | xRjasw2 | compact idiom peer |
| java | div | PT | P-gen | x86_64 | thru‡ | 23.29 | BigDecimal | 1007.33 | **43.25×** | xRjasw2 | compact idiom peer |
| kotlin | div | CD | P-gen | x86_64 | thru‡ | 95.05 | BigDecimal | 361.83 | **3.81×** | xRkosw2 | compact idiom peer |
| kotlin | div | WD | P-gen | x86_64 | thru‡ | 120.83 | BigDecimal | 268.82 | **2.22×** | xRkosw2 | compact idiom peer |
| kotlin | div | XD | P-gen | x86_64 | thru‡ | 133.07 | BigDecimal | 337.40 | **2.54×** | xRkosw2 | compact idiom peer |
| kotlin | div | ET | P-gen | x86_64 | thru‡ | 52.46 | BigDecimal | 1131.49 | **21.57×** | xRkosw2 | compact idiom peer |
| kotlin | div | PT | P-gen | x86_64 | thru‡ | 27.10 | BigDecimal | 1049.77 | **38.74×** | xRkosw2 | compact idiom peer |
| python | div | CD | P-gen | x86_64 | thru | 117.35 | decimal.Decimal | 216.45 | **1.84×** | xRpysw2 | compact idiom peer |
| python | div | WD | P-gen | x86_64 | thru | 130.99 | decimal.Decimal | 226.12 | **1.73×** | xRpysw2 | compact idiom peer |
| python | div | XD | P-gen | x86_64 | thru | 131.17 | decimal.Decimal | 332.91 | **2.54×** | xRpysw2 | compact idiom peer |
| python | div | ET | P-gen | x86_64 | thru | 72.07 | decimal.Decimal | 197.96 | **2.75×** | xRpysw2 | compact idiom peer |
| python | div | PT | P-gen | x86_64 | thru | 46.90 | decimal.Decimal | 179.56 | **3.83×** | xRpysw2 | compact idiom peer |
| c | div | CD | P-gen | x86_64 | thru | 84.26 | decQuad | 142.41 | **1.69×** | xRc2 |  |
| c | div | WD | P-gen | x86_64 | thru | 87.22 | decQuad | 242.94 | **2.79×** | xRc2 |  |
| c | div | XD | P-gen | x86_64 | thru | 78.01 | decQuad | 388.44 | **4.98×** | xRc2 |  |
| c | div | ET | P-gen | x86_64 | thru | 31.38 | decQuad | 103.92 | **3.31×** | xRc2 |  |
| c | div | PT | P-gen | x86_64 | thru | 7.54 | decQuad | 85.82 | **11.38×** | xRc2 |  |
| c | div | CD | P-gen | x86_64 | thru | 84.26 | mpdecimal | 158.06 | **1.88×** | xRc2 |  |
| c | div | WD | P-gen | x86_64 | thru | 87.22 | mpdecimal | 282.15 | **3.23×** | xRc2 |  |
| c | div | XD | P-gen | x86_64 | thru | 78.01 | mpdecimal | 351.41 | **4.50×** | xRc2 |  |
| c | div | ET | P-gen | x86_64 | thru | 31.38 | mpdecimal | 161.73 | **5.15×** | xRc2 |  |
| c | div | PT | P-gen | x86_64 | thru | 7.54 | mpdecimal | 100.98 | **13.39×** | xRc2 |  |
<!-- END GENERATED div-rel-x86 -->

## 5. FMA — FN (Barrett) · FF (fits-128) (run `Rprof`, arm64)

Swept `self + lhs·rhs` over the 3-operand FN/FF regimes (§3.4). `self` placement selects
the finalize path: **FN** keeps the wide product ⇒ 256-bit Barrett; **FF** swamps it ⇒
fits-128 fast path. The fast-path win (FN÷FF) is the whole story — universal **1.35–2.0×**
(JVM/BDN compress it via their packaging term). `‡` = JVM escape-forced. ns/op:

<!-- BEGIN GENERATED fma -->
| port | FN | FF | FN÷FF | run |
|------|---:|---:|---:|-----|
| c      |  79.12 | 41.31 | 1.92× | Rc2    |
| rust   |  79.17 | 42.70 | 1.85× | Rrsw2  |
| zig    |  66.71 | 44.01 | 1.52× | Rzgsw2 |
| swift  |  84.73 | 43.60 | 1.94× | Rswsw2 |
| csharp |  98.96 | 57.26 | 1.73× | Rcssw2 |
| go     | 173.10 | 73.39 | 2.36× | Rgosw2 |
| java‡  |  97.81 | 67.81 | 1.44× | Rjasw2 |
| kotlin‡| 100.01 | 69.55 | 1.44× | Rkosw2 |
| python | 135.43 | 88.16 | 1.54× | Rpysw2 |
<!-- END GENERATED fma -->

**FMA — d128 FN/FF band shape — x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-x86 -->
| port | FN | FF | FN÷FF | run |
|------|---:|---:|---:|-----|
| c      | 115.82 |  85.46 | 1.36× | xRc2    |
| rust   | 117.13 |  77.43 | 1.51× | xRrsw2  |
| zig    | 105.83 |  71.89 | 1.47× | xRzgsw2 |
| swift  | 147.28 |  84.54 | 1.74× | xRswsw2 |
| csharp | 192.15 | 134.80 | 1.43× | xRcssw2 |
| go     | 253.30 | 137.70 | 1.84× | xRgosw2 |
| java‡  | 216.24 | 194.37 | 1.11× | xRjasw2 |
| kotlin‡| 243.77 | 207.41 | 1.18× | xRkosw2 |
| python | 193.71 | 189.16 | 1.02× | xRpysw2 |
<!-- END GENERATED fma-x86 -->

**Peer head-to-head.** FMA is *not* peerless: every conformant reference exposes a true
fused multiply-add (one rounding) — Intel libbid (`bid128_fma`), IBM decQuad (`decQuadFMA`),
libmpdecimal (`mpd_qfma`), and Python's `decimal.Decimal.fma`. Ports with no in-language
fused-FMA peer pair against the libbid universal reference; `go`/`csharp` have neither and
show `-`. d128's fits-128 FF path is the standout (libbid ≈1.4×, decQuad ≈1.5×, mpd ≈3.5×):

<!-- BEGIN GENERATED fma-rel -->
| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | fma | FN | FMA | arm64 | thru | 79.12 | libbid | 81.81 | **1.03×** | Rc2 |  |
| c | fma | FF | FMA | arm64 | thru | 41.31 | libbid | 56.62 | **1.37×** | Rc2 |  |
| rust | fma | FN | FMA | arm64 | thru | 79.17 | libbid | 81.81 | **1.03×** | Rrsw2 |  |
| rust | fma | FF | FMA | arm64 | thru | 42.70 | libbid | 56.62 | **1.33×** | Rrsw2 |  |
| zig | fma | FN | FMA | arm64 | thru | 66.71 | libbid | 81.81 | **1.23×** | Rzgsw2 |  |
| zig | fma | FF | FMA | arm64 | thru | 44.01 | libbid | 56.62 | **1.29×** | Rzgsw2 |  |
| swift | fma | FN | FMA | arm64 | thru | 84.73 | libbid | 81.81 | **0.97×** | Rswsw2 |  |
| swift | fma | FF | FMA | arm64 | thru | 43.60 | libbid | 56.62 | **1.30×** | Rswsw2 |  |
| csharp | fma | FN | FMA | arm64 | thru | 98.96 | - | - | - | Rcssw2 |  |
| csharp | fma | FF | FMA | arm64 | thru | 57.26 | - | - | - | Rcssw2 |  |
| go | fma | FN | FMA | arm64 | thru | 173.10 | - | - | - | Rgosw2 |  |
| go | fma | FF | FMA | arm64 | thru | 73.39 | - | - | - | Rgosw2 |  |
| java | fma | FN | FMA | arm64 | thru‡ | 97.81 | libbid | 81.81 | **0.84×** | Rjasw2 |  |
| java | fma | FF | FMA | arm64 | thru‡ | 67.81 | libbid | 56.62 | **0.83×** | Rjasw2 |  |
| kotlin | fma | FN | FMA | arm64 | thru‡ | 100.01 | libbid | 81.81 | **0.82×** | Rkosw2 |  |
| kotlin | fma | FF | FMA | arm64 | thru‡ | 69.55 | libbid | 56.62 | **0.81×** | Rkosw2 |  |
| python | fma | FN | FMA | arm64 | thru | 135.43 | decimal.Decimal | 141.11 | **1.04×** | Rpysw2 | compact idiom peer |
| python | fma | FF | FMA | arm64 | thru | 88.16 | decimal.Decimal | 161.53 | **1.83×** | Rpysw2 | compact idiom peer |
| c | fma | FN | FMA | arm64 | thru | 79.12 | decQuad | 62.35 | **0.79×** | Rc2 |  |
| c | fma | FF | FMA | arm64 | thru | 41.31 | decQuad | 68.85 | **1.67×** | Rc2 |  |
| c | fma | FN | FMA | arm64 | thru | 79.12 | mpdecimal | 85.72 | **1.08×** | Rc2 |  |
| c | fma | FF | FMA | arm64 | thru | 41.31 | mpdecimal | 136.74 | **3.31×** | Rc2 |  |
<!-- END GENERATED fma-rel -->

**Relational vs peers — x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-x86 -->
| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | fma | FN | FMA | x86_64 | thru | 115.82 | libbid | 157.23 | **1.36×** | xRc2 |  |
| c | fma | FF | FMA | x86_64 | thru | 85.46 | libbid | 148.05 | **1.73×** | xRc2 |  |
| rust | fma | FN | FMA | x86_64 | thru | 117.13 | libbid | 157.23 | **1.34×** | xRrsw2 |  |
| rust | fma | FF | FMA | x86_64 | thru | 77.43 | libbid | 148.05 | **1.91×** | xRrsw2 |  |
| zig | fma | FN | FMA | x86_64 | thru | 105.83 | libbid | 157.23 | **1.49×** | xRzgsw2 |  |
| zig | fma | FF | FMA | x86_64 | thru | 71.89 | libbid | 148.05 | **2.06×** | xRzgsw2 |  |
| swift | fma | FN | FMA | x86_64 | thru | 147.28 | libbid | 157.23 | **1.07×** | xRswsw2 |  |
| swift | fma | FF | FMA | x86_64 | thru | 84.54 | libbid | 148.05 | **1.75×** | xRswsw2 |  |
| csharp | fma | FN | FMA | x86_64 | thru | 192.15 | - | - | - | xRcssw2 |  |
| csharp | fma | FF | FMA | x86_64 | thru | 134.80 | - | - | - | xRcssw2 |  |
| go | fma | FN | FMA | x86_64 | thru | 253.30 | - | - | - | xRgosw2 |  |
| go | fma | FF | FMA | x86_64 | thru | 137.70 | - | - | - | xRgosw2 |  |
| java | fma | FN | FMA | x86_64 | thru‡ | 216.24 | libbid | 157.23 | **0.73×** | xRjasw2 |  |
| java | fma | FF | FMA | x86_64 | thru‡ | 194.37 | libbid | 148.05 | **0.76×** | xRjasw2 |  |
| kotlin | fma | FN | FMA | x86_64 | thru‡ | 243.77 | libbid | 157.23 | **0.64×** | xRkosw2 |  |
| kotlin | fma | FF | FMA | x86_64 | thru‡ | 207.41 | libbid | 148.05 | **0.71×** | xRkosw2 |  |
| python | fma | FN | FMA | x86_64 | thru | 193.71 | decimal.Decimal | 274.45 | **1.42×** | xRpysw2 | compact idiom peer |
| python | fma | FF | FMA | x86_64 | thru | 189.16 | decimal.Decimal | 318.61 | **1.68×** | xRpysw2 | compact idiom peer |
| c | fma | FN | FMA | x86_64 | thru | 115.82 | decQuad | 146.12 | **1.26×** | xRc2 |  |
| c | fma | FF | FMA | x86_64 | thru | 85.46 | decQuad | 162.64 | **1.90×** | xRc2 |  |
| c | fma | FN | FMA | x86_64 | thru | 115.82 | mpdecimal | 254.18 | **2.19×** | xRc2 |  |
| c | fma | FF | FMA | x86_64 | thru | 85.46 | mpdecimal | 343.82 | **4.02×** | xRc2 |  |
<!-- END GENERATED fma-rel-x86 -->

## 6. P-fin — financial headline

`P-fin` is the realistic financial regime (`BenchmarkMatrix.md` §2.1): coefficients < 2⁶⁴
(≤ 19 digits, log-uniform), currency-style quanta, every operand ≥ 1 integer digit. Add/sub
run as **one realistic `MIX` stream** (75% same-quantum / 25% independent quantum — a blend of
same-exp, pack-align and >4-digit-gap alignment) rather than the per-band SQ/NQ/… split; multiply
is `CP`/`WP`; divide is `CD`/`WD`/`ET`/`PT`. This is the **headline** profile — closest to real
financial code — complementing the P-gen band-shape (§1–§5) and the P-max wide-path stress rows.
Swept 4096-input average, same corpus/method as §1–§5; arm64 (M3 Pro); JVM `‡` = escape-forced
alloc-inclusive.

**d128 band shape (ns/op):**

<!-- BEGIN GENERATED pfin-matrix -->
| port | add MIX | sub MIX | mul CP | mul WP | div CD | div WD | div ET | div PT |
|------|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|
| c      |  2.83 |  2.46 |  2.14 | 19.57 | 43.47 | 39.49 |  6.48 |  3.18 |
| rust   |  3.02 |  2.56 |  1.12 | 14.43 | 26.55 | 34.06 |  6.20 |  3.96 |
| zig    |  3.31 |  2.58 |  2.31 | 18.05 | 40.16 | 40.87 |  7.55 |  4.24 |
| swift  |  4.37 |  3.32 |  1.77 | 20.99 | 34.49 | 45.97 |  8.27 | 10.77 |
| csharp |  4.09 |  2.93 |  1.50 | 23.27 | 23.14 | 48.31 |  5.57 |  5.52 |
| go     |  5.58 |  4.31 |  2.32 | 27.88 | 49.85 | 63.94 | 12.02 |  6.89 |
| java‡  |  5.77 |  5.14 |  4.69 | 20.00 | 28.24 | 37.60 | 12.39 |  8.72 |
| kotlin‡|  6.86 |  5.57 |  4.93 | 17.66 | 28.82 | 38.22 | 16.66 |  9.65 |
| python | 24.10 | 22.96 | 16.52 | 46.71 | 66.52 | 73.96 | 22.57 | 19.46 |
<!-- END GENERATED pfin-matrix -->

**P-fin — d128 band shape — x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-matrix-x86 -->
| port | add MIX | sub MIX | mul CP | mul WP | div CD | div WD | div ET | div PT |
|------|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|
| c      | 10.44 |  8.37 |  6.03 | 36.31 |  74.91 |  94.45 | 16.55 |  7.25 |
| rust   | 11.46 |  9.05 |  3.18 | 29.03 |  68.34 |  83.05 | 22.73 |  9.67 |
| zig    | 13.30 | 11.29 |  7.12 | 28.99 |  66.25 |  90.13 | 20.64 | 11.96 |
| swift  | 12.78 |  9.84 |  3.93 | 35.27 |  69.23 |  90.59 | 20.98 | 11.98 |
| csharp | 15.12 | 13.11 |  5.08 | 53.68 |  78.04 | 106.38 | 21.49 | 11.80 |
| go     | 13.58 | 11.75 |  4.86 | 49.33 | 108.00 | 124.70 | 31.75 | 12.99 |
| java‡  | 18.43 | 15.92 | 13.91 | 55.68 | 104.15 | 121.45 | 43.57 | 23.08 |
| kotlin‡| 24.20 | 19.50 | 13.22 | 46.12 | 100.87 | 127.21 | 48.56 | 24.70 |
| python | 51.17 | 49.73 | 40.98 | 77.69 | 115.69 | 130.48 | 56.06 | 46.20 |
<!-- END GENERATED pfin-matrix-x86 -->

**Relational — d128 vs idiom peer** (else the universal reference `libbid`; `-` where the peer
cannot represent the band — the 28-digit compact peers `rust_decimal` / `System.Decimal` overflow
the CP/WP products, so multiply has no compact-peer column). C additionally vs decQuad + mpdecimal.
Ratio = alt / ours (> 1 ⇒ d128 faster).

<!-- BEGIN GENERATED pfin-rel -->
| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | add | MIX | P-fin | arm64 | thru | 2.83 | libbid | 10.87 | **3.84×** | Rc2 |  |
| c | sub | MIX | P-fin | arm64 | thru | 2.46 | libbid | 11.98 | **4.87×** | Rc2 |  |
| rust | add | MIX | P-fin | arm64 | thru | 3.02 | rust_decimal | 3.82 | **1.26×** | Rrsw2 | compact idiom peer |
| rust | sub | MIX | P-fin | arm64 | thru | 2.56 | rust_decimal | 3.73 | **1.46×** | Rrsw2 | compact idiom peer |
| zig | add | MIX | P-fin | arm64 | thru | 3.31 | libbid | 10.87 | **3.28×** | Rzgsw2 |  |
| zig | sub | MIX | P-fin | arm64 | thru | 2.58 | libbid | 11.98 | **4.64×** | Rzgsw2 |  |
| swift | add | MIX | P-fin | arm64 | thru | 4.37 | Foundation.Decimal | 329.07 | **75.30×** | Rswsw2 | compact idiom peer |
| swift | sub | MIX | P-fin | arm64 | thru | 3.32 | Foundation.Decimal | 328.60 | **98.98×** | Rswsw2 | compact idiom peer |
| csharp | add | MIX | P-fin | arm64 | thru | 4.09 | System.Decimal | 2.61 | **0.64×** | Rcssw2 | compact idiom peer |
| csharp | sub | MIX | P-fin | arm64 | thru | 2.93 | System.Decimal | 2.90 | **0.99×** | Rcssw2 | compact idiom peer |
| go | add | MIX | P-fin | arm64 | thru | 5.58 | - | - | - | Rgosw2 |  |
| go | sub | MIX | P-fin | arm64 | thru | 4.31 | - | - | - | Rgosw2 |  |
| java | add | MIX | P-fin | arm64 | thru‡ | 5.77 | BigDecimal | 25.46 | **4.41×** | Rjasw2 | compact idiom peer |
| java | sub | MIX | P-fin | arm64 | thru‡ | 5.14 | BigDecimal | 21.83 | **4.25×** | Rjasw2 | compact idiom peer |
| kotlin | add | MIX | P-fin | arm64 | thru‡ | 6.86 | BigDecimal | 20.17 | **2.94×** | Rkosw2 | compact idiom peer |
| kotlin | sub | MIX | P-fin | arm64 | thru‡ | 5.57 | BigDecimal | 23.13 | **4.15×** | Rkosw2 | compact idiom peer |
| python | add | MIX | P-fin | arm64 | thru | 24.10 | decimal.Decimal | 63.13 | **2.62×** | Rpysw2 | compact idiom peer |
| python | sub | MIX | P-fin | arm64 | thru | 22.96 | decimal.Decimal | 62.86 | **2.74×** | Rpysw2 | compact idiom peer |
| c | add | MIX | P-fin | arm64 | thru | 2.83 | decQuad | 21.39 | **7.56×** | Rc2 |  |
| c | sub | MIX | P-fin | arm64 | thru | 2.46 | decQuad | 22.42 | **9.11×** | Rc2 |  |
| c | add | MIX | P-fin | arm64 | thru | 2.83 | mpdecimal | 14.39 | **5.08×** | Rc2 |  |
| c | sub | MIX | P-fin | arm64 | thru | 2.46 | mpdecimal | 14.66 | **5.96×** | Rc2 |  |
| c | mul | CP | P-fin | arm64 | thru | 2.14 | libbid | 23.40 | **10.93×** | Rc2 |  |
| c | mul | WP | P-fin | arm64 | thru | 19.57 | libbid | 32.23 | **1.65×** | Rc2 |  |
| rust | mul | CP | P-fin | arm64 | thru | 1.12 | libbid | 23.40 | **20.89×** | Rrsw2 |  |
| rust | mul | WP | P-fin | arm64 | thru | 14.43 | libbid | 32.23 | **2.23×** | Rrsw2 |  |
| zig | mul | CP | P-fin | arm64 | thru | 2.31 | libbid | 23.40 | **10.13×** | Rzgsw2 |  |
| zig | mul | WP | P-fin | arm64 | thru | 18.05 | libbid | 32.23 | **1.79×** | Rzgsw2 |  |
| swift | mul | CP | P-fin | arm64 | thru | 1.77 | Foundation.Decimal | 286.79 | **162.03×** | Rswsw2 | compact idiom peer |
| swift | mul | WP | P-fin | arm64 | thru | 20.99 | Foundation.Decimal | 287.60 | **13.70×** | Rswsw2 | compact idiom peer |
| csharp | mul | CP | P-fin | arm64 | thru | 1.50 | - | - | - | Rcssw2 |  |
| csharp | mul | WP | P-fin | arm64 | thru | 23.27 | - | - | - | Rcssw2 |  |
| go | mul | CP | P-fin | arm64 | thru | 2.32 | - | - | - | Rgosw2 |  |
| go | mul | WP | P-fin | arm64 | thru | 27.88 | - | - | - | Rgosw2 |  |
| java | mul | CP | P-fin | arm64 | thru‡ | 4.69 | BigDecimal | 12.67 | **2.70×** | Rjasw2 | compact idiom peer |
| java | mul | WP | P-fin | arm64 | thru‡ | 20.00 | BigDecimal | 70.99 | **3.55×** | Rjasw2 | compact idiom peer |
| kotlin | mul | CP | P-fin | arm64 | thru‡ | 4.93 | BigDecimal | 12.32 | **2.50×** | Rkosw2 | compact idiom peer |
| kotlin | mul | WP | P-fin | arm64 | thru‡ | 17.66 | BigDecimal | 71.46 | **4.05×** | Rkosw2 | compact idiom peer |
| python | mul | CP | P-fin | arm64 | thru | 16.52 | decimal.Decimal | 62.21 | **3.77×** | Rpysw2 | compact idiom peer |
| python | mul | WP | P-fin | arm64 | thru | 46.71 | decimal.Decimal | 68.39 | **1.46×** | Rpysw2 | compact idiom peer |
| c | mul | CP | P-fin | arm64 | thru | 2.14 | decQuad | 22.21 | **10.38×** | Rc2 |  |
| c | mul | WP | P-fin | arm64 | thru | 19.57 | decQuad | 26.69 | **1.36×** | Rc2 |  |
| c | mul | CP | P-fin | arm64 | thru | 2.14 | mpdecimal | 17.36 | **8.11×** | Rc2 |  |
| c | mul | WP | P-fin | arm64 | thru | 19.57 | mpdecimal | 28.90 | **1.48×** | Rc2 |  |
| c | div | CD | P-fin | arm64 | thru | 43.47 | libbid | 35.07 | **0.81×** | Rc2 |  |
| c | div | WD | P-fin | arm64 | thru | 39.49 | libbid | 39.31 | **1.00×** | Rc2 |  |
| c | div | ET | P-fin | arm64 | thru | 6.48 | libbid | 6.02 | **0.93×** | Rc2 |  |
| c | div | PT | P-fin | arm64 | thru | 3.18 | libbid | 6.01 | **1.89×** | Rc2 |  |
| rust | div | CD | P-fin | arm64 | thru | 26.55 | rust_decimal | 14.80 | **0.56×** | Rrsw2 | compact idiom peer |
| rust | div | WD | P-fin | arm64 | thru | 34.06 | rust_decimal | 20.54 | **0.60×** | Rrsw2 | compact idiom peer |
| rust | div | ET | P-fin | arm64 | thru | 6.20 | rust_decimal | 3.76 | **0.61×** | Rrsw2 | compact idiom peer |
| rust | div | PT | P-fin | arm64 | thru | 3.96 | rust_decimal | 15.32 | **3.87×** | Rrsw2 | compact idiom peer |
| zig | div | CD | P-fin | arm64 | thru | 40.16 | libbid | 35.07 | **0.87×** | Rzgsw2 |  |
| zig | div | WD | P-fin | arm64 | thru | 40.87 | libbid | 39.31 | **0.96×** | Rzgsw2 |  |
| zig | div | ET | P-fin | arm64 | thru | 7.55 | libbid | 6.02 | **0.80×** | Rzgsw2 |  |
| zig | div | PT | P-fin | arm64 | thru | 4.24 | libbid | 6.01 | **1.42×** | Rzgsw2 |  |
| swift | div | CD | P-fin | arm64 | thru | 34.49 | Foundation.Decimal | 1254.63 | **36.38×** | Rswsw2 | compact idiom peer |
| swift | div | WD | P-fin | arm64 | thru | 45.97 | Foundation.Decimal | 671.80 | **14.61×** | Rswsw2 | compact idiom peer |
| swift | div | ET | P-fin | arm64 | thru | 8.27 | Foundation.Decimal | 3635.51 | **439.60×** | Rswsw2 | compact idiom peer |
| swift | div | PT | P-fin | arm64 | thru | 10.77 | Foundation.Decimal | 3552.06 | **329.81×** | Rswsw2 | compact idiom peer |
| csharp | div | CD | P-fin | arm64 | thru | 23.14 | System.Decimal | 10.98 | **0.47×** | Rcssw2 | compact idiom peer |
| csharp | div | WD | P-fin | arm64 | thru | 48.31 | System.Decimal | 18.95 | **0.39×** | Rcssw2 | compact idiom peer |
| csharp | div | ET | P-fin | arm64 | thru | 5.57 | System.Decimal | 4.55 | **0.82×** | Rcssw2 | compact idiom peer |
| csharp | div | PT | P-fin | arm64 | thru | 5.52 | System.Decimal | 10.62 | **1.92×** | Rcssw2 | compact idiom peer |
| go | div | CD | P-fin | arm64 | thru | 49.85 | - | - | - | Rgosw2 |  |
| go | div | WD | P-fin | arm64 | thru | 63.94 | - | - | - | Rgosw2 |  |
| go | div | ET | P-fin | arm64 | thru | 12.02 | - | - | - | Rgosw2 |  |
| go | div | PT | P-fin | arm64 | thru | 6.89 | - | - | - | Rgosw2 |  |
| java | div | CD | P-fin | arm64 | thru‡ | 28.24 | BigDecimal | 155.70 | **5.51×** | Rjasw2 | compact idiom peer |
| java | div | WD | P-fin | arm64 | thru‡ | 37.60 | BigDecimal | 91.07 | **2.42×** | Rjasw2 | compact idiom peer |
| java | div | ET | P-fin | arm64 | thru‡ | 12.39 | BigDecimal | 510.72 | **41.22×** | Rjasw2 | compact idiom peer |
| java | div | PT | P-fin | arm64 | thru‡ | 8.72 | BigDecimal | 486.55 | **55.80×** | Rjasw2 | compact idiom peer |
| kotlin | div | CD | P-fin | arm64 | thru‡ | 28.82 | BigDecimal | 160.26 | **5.56×** | Rkosw2 | compact idiom peer |
| kotlin | div | WD | P-fin | arm64 | thru‡ | 38.22 | BigDecimal | 96.62 | **2.53×** | Rkosw2 | compact idiom peer |
| kotlin | div | ET | P-fin | arm64 | thru‡ | 16.66 | BigDecimal | 502.90 | **30.19×** | Rkosw2 | compact idiom peer |
| kotlin | div | PT | P-fin | arm64 | thru‡ | 9.65 | BigDecimal | 484.29 | **50.19×** | Rkosw2 | compact idiom peer |
| python | div | CD | P-fin | arm64 | thru | 66.52 | decimal.Decimal | 96.17 | **1.45×** | Rpysw2 | compact idiom peer |
| python | div | WD | P-fin | arm64 | thru | 73.96 | decimal.Decimal | 99.11 | **1.34×** | Rpysw2 | compact idiom peer |
| python | div | ET | P-fin | arm64 | thru | 22.57 | decimal.Decimal | 87.96 | **3.90×** | Rpysw2 | compact idiom peer |
| python | div | PT | P-fin | arm64 | thru | 19.46 | decimal.Decimal | 85.06 | **4.37×** | Rpysw2 | compact idiom peer |
| c | div | CD | P-fin | arm64 | thru | 43.47 | decQuad | 71.64 | **1.65×** | Rc2 |  |
| c | div | WD | P-fin | arm64 | thru | 39.49 | decQuad | 117.50 | **2.98×** | Rc2 |  |
| c | div | ET | P-fin | arm64 | thru | 6.48 | decQuad | 39.89 | **6.16×** | Rc2 |  |
| c | div | PT | P-fin | arm64 | thru | 3.18 | decQuad | 38.30 | **12.04×** | Rc2 |  |
| c | div | CD | P-fin | arm64 | thru | 43.47 | mpdecimal | 57.74 | **1.33×** | Rc2 |  |
| c | div | WD | P-fin | arm64 | thru | 39.49 | mpdecimal | 85.11 | **2.16×** | Rc2 |  |
| c | div | ET | P-fin | arm64 | thru | 6.48 | mpdecimal | 53.84 | **8.31×** | Rc2 |  |
| c | div | PT | P-fin | arm64 | thru | 3.18 | mpdecimal | 44.54 | **14.01×** | Rc2 |  |
<!-- END GENERATED pfin-rel -->

**Relational vs peers — x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-x86 -->
| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | add | MIX | P-fin | x86_64 | thru | 10.44 | libbid | 30.88 | **2.96×** | xRc2 |  |
| c | sub | MIX | P-fin | x86_64 | thru | 8.37 | libbid | 35.20 | **4.21×** | xRc2 |  |
| rust | add | MIX | P-fin | x86_64 | thru | 11.46 | rust_decimal | 14.80 | **1.29×** | xRrsw2 | compact idiom peer |
| rust | sub | MIX | P-fin | x86_64 | thru | 9.05 | rust_decimal | 14.62 | **1.62×** | xRrsw2 | compact idiom peer |
| zig | add | MIX | P-fin | x86_64 | thru | 13.30 | libbid | 30.88 | **2.32×** | xRzgsw2 |  |
| zig | sub | MIX | P-fin | x86_64 | thru | 11.29 | libbid | 35.20 | **3.12×** | xRzgsw2 |  |
| swift | add | MIX | P-fin | x86_64 | thru | 12.78 | Foundation.Decimal | 796.07 | **62.29×** | xRswsw2 | compact idiom peer |
| swift | sub | MIX | P-fin | x86_64 | thru | 9.84 | Foundation.Decimal | 773.96 | **78.65×** | xRswsw2 | compact idiom peer |
| csharp | add | MIX | P-fin | x86_64 | thru | 15.12 | System.Decimal | 12.56 | **0.83×** | xRcssw2 | compact idiom peer |
| csharp | sub | MIX | P-fin | x86_64 | thru | 13.11 | System.Decimal | 12.46 | **0.95×** | xRcssw2 | compact idiom peer |
| go | add | MIX | P-fin | x86_64 | thru | 13.58 | - | - | - | xRgosw2 |  |
| go | sub | MIX | P-fin | x86_64 | thru | 11.75 | - | - | - | xRgosw2 |  |
| java | add | MIX | P-fin | x86_64 | thru‡ | 18.43 | BigDecimal | 61.84 | **3.36×** | xRjasw2 | compact idiom peer |
| java | sub | MIX | P-fin | x86_64 | thru‡ | 15.92 | BigDecimal | 72.49 | **4.55×** | xRjasw2 | compact idiom peer |
| kotlin | add | MIX | P-fin | x86_64 | thru‡ | 24.20 | BigDecimal | 61.42 | **2.54×** | xRkosw2 | compact idiom peer |
| kotlin | sub | MIX | P-fin | x86_64 | thru‡ | 19.50 | BigDecimal | 64.72 | **3.32×** | xRkosw2 | compact idiom peer |
| python | add | MIX | P-fin | x86_64 | thru | 51.17 | decimal.Decimal | 120.76 | **2.36×** | xRpysw2 | compact idiom peer |
| python | sub | MIX | P-fin | x86_64 | thru | 49.73 | decimal.Decimal | 121.14 | **2.44×** | xRpysw2 | compact idiom peer |
| c | add | MIX | P-fin | x86_64 | thru | 10.44 | decQuad | 58.57 | **5.61×** | xRc2 |  |
| c | sub | MIX | P-fin | x86_64 | thru | 8.37 | decQuad | 59.39 | **7.10×** | xRc2 |  |
| c | add | MIX | P-fin | x86_64 | thru | 10.44 | mpdecimal | 39.47 | **3.78×** | xRc2 |  |
| c | sub | MIX | P-fin | x86_64 | thru | 8.37 | mpdecimal | 39.66 | **4.74×** | xRc2 |  |
| c | mul | CP | P-fin | x86_64 | thru | 6.03 | libbid | 47.71 | **7.91×** | xRc2 |  |
| c | mul | WP | P-fin | x86_64 | thru | 36.31 | libbid | 58.07 | **1.60×** | xRc2 |  |
| rust | mul | CP | P-fin | x86_64 | thru | 3.18 | libbid | 47.71 | **15.00×** | xRrsw2 |  |
| rust | mul | WP | P-fin | x86_64 | thru | 29.03 | libbid | 58.07 | **2.00×** | xRrsw2 |  |
| zig | mul | CP | P-fin | x86_64 | thru | 7.12 | libbid | 47.71 | **6.70×** | xRzgsw2 |  |
| zig | mul | WP | P-fin | x86_64 | thru | 28.99 | libbid | 58.07 | **2.00×** | xRzgsw2 |  |
| swift | mul | CP | P-fin | x86_64 | thru | 3.93 | Foundation.Decimal | 680.97 | **173.27×** | xRswsw2 | compact idiom peer |
| swift | mul | WP | P-fin | x86_64 | thru | 35.27 | Foundation.Decimal | 751.40 | **21.30×** | xRswsw2 | compact idiom peer |
| csharp | mul | CP | P-fin | x86_64 | thru | 5.08 | - | - | - | xRcssw2 |  |
| csharp | mul | WP | P-fin | x86_64 | thru | 53.68 | - | - | - | xRcssw2 |  |
| go | mul | CP | P-fin | x86_64 | thru | 4.86 | - | - | - | xRgosw2 |  |
| go | mul | WP | P-fin | x86_64 | thru | 49.33 | - | - | - | xRgosw2 |  |
| java | mul | CP | P-fin | x86_64 | thru‡ | 13.91 | BigDecimal | 46.03 | **3.31×** | xRjasw2 | compact idiom peer |
| java | mul | WP | P-fin | x86_64 | thru‡ | 55.68 | BigDecimal | 174.46 | **3.13×** | xRjasw2 | compact idiom peer |
| kotlin | mul | CP | P-fin | x86_64 | thru‡ | 13.22 | BigDecimal | 42.94 | **3.25×** | xRkosw2 | compact idiom peer |
| kotlin | mul | WP | P-fin | x86_64 | thru‡ | 46.12 | BigDecimal | 161.22 | **3.50×** | xRkosw2 | compact idiom peer |
| python | mul | CP | P-fin | x86_64 | thru | 40.98 | decimal.Decimal | 114.63 | **2.80×** | xRpysw2 | compact idiom peer |
| python | mul | WP | P-fin | x86_64 | thru | 77.69 | decimal.Decimal | 126.92 | **1.63×** | xRpysw2 | compact idiom peer |
| c | mul | CP | P-fin | x86_64 | thru | 6.03 | decQuad | 65.65 | **10.89×** | xRc2 |  |
| c | mul | WP | P-fin | x86_64 | thru | 36.31 | decQuad | 68.66 | **1.89×** | xRc2 |  |
| c | mul | CP | P-fin | x86_64 | thru | 6.03 | mpdecimal | 34.50 | **5.72×** | xRc2 |  |
| c | mul | WP | P-fin | x86_64 | thru | 36.31 | mpdecimal | 44.85 | **1.24×** | xRc2 |  |
| c | div | CD | P-fin | x86_64 | thru | 74.91 | libbid | 77.08 | **1.03×** | xRc2 |  |
| c | div | WD | P-fin | x86_64 | thru | 94.45 | libbid | 87.31 | **0.92×** | xRc2 |  |
| c | div | ET | P-fin | x86_64 | thru | 16.55 | libbid | 20.18 | **1.22×** | xRc2 |  |
| c | div | PT | P-fin | x86_64 | thru | 7.25 | libbid | 19.36 | **2.67×** | xRc2 |  |
| rust | div | CD | P-fin | x86_64 | thru | 68.34 | rust_decimal | 53.43 | **0.78×** | xRrsw2 | compact idiom peer |
| rust | div | WD | P-fin | x86_64 | thru | 83.05 | rust_decimal | 72.43 | **0.87×** | xRrsw2 | compact idiom peer |
| rust | div | ET | P-fin | x86_64 | thru | 22.73 | rust_decimal | 13.48 | **0.59×** | xRrsw2 | compact idiom peer |
| rust | div | PT | P-fin | x86_64 | thru | 9.67 | rust_decimal | 49.72 | **5.14×** | xRrsw2 | compact idiom peer |
| zig | div | CD | P-fin | x86_64 | thru | 66.25 | libbid | 77.08 | **1.16×** | xRzgsw2 |  |
| zig | div | WD | P-fin | x86_64 | thru | 90.13 | libbid | 87.31 | **0.97×** | xRzgsw2 |  |
| zig | div | ET | P-fin | x86_64 | thru | 20.64 | libbid | 20.18 | **0.98×** | xRzgsw2 |  |
| zig | div | PT | P-fin | x86_64 | thru | 11.96 | libbid | 19.36 | **1.62×** | xRzgsw2 |  |
| swift | div | CD | P-fin | x86_64 | thru | 69.23 | Foundation.Decimal | 2940.37 | **42.47×** | xRswsw2 | compact idiom peer |
| swift | div | WD | P-fin | x86_64 | thru | 90.59 | Foundation.Decimal | 1517.47 | **16.75×** | xRswsw2 | compact idiom peer |
| swift | div | ET | P-fin | x86_64 | thru | 20.98 | Foundation.Decimal | 8132.42 | **387.63×** | xRswsw2 | compact idiom peer |
| swift | div | PT | P-fin | x86_64 | thru | 11.98 | Foundation.Decimal | 8045.96 | **671.62×** | xRswsw2 | compact idiom peer |
| csharp | div | CD | P-fin | x86_64 | thru | 78.04 | System.Decimal | 50.01 | **0.64×** | xRcssw2 | compact idiom peer |
| csharp | div | WD | P-fin | x86_64 | thru | 106.38 | System.Decimal | 97.82 | **0.92×** | xRcssw2 | compact idiom peer |
| csharp | div | ET | P-fin | x86_64 | thru | 21.49 | System.Decimal | 13.78 | **0.64×** | xRcssw2 | compact idiom peer |
| csharp | div | PT | P-fin | x86_64 | thru | 11.80 | System.Decimal | 57.63 | **4.88×** | xRcssw2 | compact idiom peer |
| go | div | CD | P-fin | x86_64 | thru | 108.00 | - | - | - | xRgosw2 |  |
| go | div | WD | P-fin | x86_64 | thru | 124.70 | - | - | - | xRgosw2 |  |
| go | div | ET | P-fin | x86_64 | thru | 31.75 | - | - | - | xRgosw2 |  |
| go | div | PT | P-fin | x86_64 | thru | 12.99 | - | - | - | xRgosw2 |  |
| java | div | CD | P-fin | x86_64 | thru‡ | 104.15 | BigDecimal | 399.71 | **3.84×** | xRjasw2 | compact idiom peer |
| java | div | WD | P-fin | x86_64 | thru‡ | 121.45 | BigDecimal | 220.49 | **1.82×** | xRjasw2 | compact idiom peer |
| java | div | ET | P-fin | x86_64 | thru‡ | 43.57 | BigDecimal | 1396.96 | **32.06×** | xRjasw2 | compact idiom peer |
| java | div | PT | P-fin | x86_64 | thru‡ | 23.08 | BigDecimal | 1347.54 | **58.39×** | xRjasw2 | compact idiom peer |
| kotlin | div | CD | P-fin | x86_64 | thru‡ | 100.87 | BigDecimal | 414.36 | **4.11×** | xRkosw2 | compact idiom peer |
| kotlin | div | WD | P-fin | x86_64 | thru‡ | 127.21 | BigDecimal | 216.64 | **1.70×** | xRkosw2 | compact idiom peer |
| kotlin | div | ET | P-fin | x86_64 | thru‡ | 48.56 | BigDecimal | 1441.34 | **29.68×** | xRkosw2 | compact idiom peer |
| kotlin | div | PT | P-fin | x86_64 | thru‡ | 24.70 | BigDecimal | 1374.35 | **55.64×** | xRkosw2 | compact idiom peer |
| python | div | CD | P-fin | x86_64 | thru | 115.69 | decimal.Decimal | 203.41 | **1.76×** | xRpysw2 | compact idiom peer |
| python | div | WD | P-fin | x86_64 | thru | 130.48 | decimal.Decimal | 222.15 | **1.70×** | xRpysw2 | compact idiom peer |
| python | div | ET | P-fin | x86_64 | thru | 56.06 | decimal.Decimal | 183.00 | **3.26×** | xRpysw2 | compact idiom peer |
| python | div | PT | P-fin | x86_64 | thru | 46.20 | decimal.Decimal | 173.94 | **3.76×** | xRpysw2 | compact idiom peer |
| c | div | CD | P-fin | x86_64 | thru | 74.91 | decQuad | 132.11 | **1.76×** | xRc2 |  |
| c | div | WD | P-fin | x86_64 | thru | 94.45 | decQuad | 249.35 | **2.64×** | xRc2 |  |
| c | div | ET | P-fin | x86_64 | thru | 16.55 | decQuad | 73.34 | **4.43×** | xRc2 |  |
| c | div | PT | P-fin | x86_64 | thru | 7.25 | decQuad | 66.79 | **9.21×** | xRc2 |  |
| c | div | CD | P-fin | x86_64 | thru | 74.91 | mpdecimal | 158.89 | **2.12×** | xRc2 |  |
| c | div | WD | P-fin | x86_64 | thru | 94.45 | mpdecimal | 272.72 | **2.89×** | xRc2 |  |
| c | div | ET | P-fin | x86_64 | thru | 16.55 | mpdecimal | 139.50 | **8.43×** | xRc2 |  |
| c | div | PT | P-fin | x86_64 | thru | 7.25 | mpdecimal | 95.74 | **13.21×** | xRc2 |  |
<!-- END GENERATED pfin-rel-x86 -->

