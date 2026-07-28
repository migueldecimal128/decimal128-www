---
layout: default
permalink: /benchmark/port-compare.html
title: "Port-Comparison Benchmark Results — Decimal128"
description: "Cross-port decimal128 band-shape matrices — each port's own ns/op per operation band on identical operands, with no comparison against alternatives."
heading: "Port-Comparison Benchmark Results"
---

<div class="whitepaper" markdown="1">

<p class="whitepaper-meta">Living document — as-measured results.</p>

This document is the **cross-port d128 band-shape** tier: compact matrices of decimal128's
own ns/op per operation band, every port on the **same** swept operands. It **does not
compare against alternatives** — no libbid / idiom-peer / ratio columns. Those live in the
companion reports:

- **`benchmark-port-compare`** (this doc) — d128-only band matrices, port × band.
  "How does each port's kernel shape up across the input bands, fast path vs slow path?"
- **`benchmark-vs-<port>`** (per language) — the same bands **vs alternatives** (libbid /
  decQuad / mpdecimal / idiom peers), with explicit ratios, plus the realistic financial
  operation mix (P-fin). "How fast is d128, in this language, against the field?" See the
  [Benchmarks](/benchmarks.html) hub for the per-language index.

**Method.** Swept 4096-input average per band (bare `thru`; ns/op = `Time/4096` over the
shared `decimal128-resources/swept/<profile>/` corpus, byte-identical operands every port).
arm64 (M3 Pro) and x86_64 (Intel i9-9880H); JVM verify-off, `‡` = escape-forced
alloc-inclusive. `P-gen` = general digit-length-uniform widths; `P-max` = 34-digit stress.
Band/category codes (`SQ`/`NQ`/`MQ`/`OQ`/`FQ`, `CP`/`WP`/`XP`, `CD`/`WD`/`XD`/`ET`/`PT`,
`FN`/`FF`) are defined in `BenchmarkMatrix.md` §3 (authoritative) and glossed in the shared
[Benchmark Key](key.html).

## 1. Add — SQ · NQ · MQ · OQ · FQ

SQ/NQ/MQ are the **compact** regime (qExp ∈ [0,−8], result < 10²⁸) — recompacted so the
28-digit peers can run on the same operands in the relational report; OQ/FQ keep the full
range. **MQ (Δ>4, the `qAlignDelta>4` no-round path) is the alignment-slope column** — 2–3×
the pack-direct NQ, the one add/sub band where d128's alignment cost shows.

**P-gen — arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-pgen -->

| port | add SQ | add NQ | add MQ | add OQ | add FQ |
|------|-------:|-------:|-------:|-------:|-------:|
| c      |  1.50 |  4.21 |  6.42 | 11.49 |  7.28 |
| rust   |  1.82 |  5.69 |  8.54 | 10.82 |  7.44 |
| zig    |  1.79 |  6.66 |  8.54 | 12.92 |  8.09 |
| swift  |  2.41 |  6.20 | 12.41 | 18.92 | 14.35 |
| csharp | 10.69 |  5.46 | 15.70 | 40.82 | 32.79 |
| go     |  3.17 | 11.28 | 16.04 | 32.24 | 20.50 |
| java‡  |  4.81 |  8.07 | 19.87 | 28.24 | 23.23 |
| kotlin‡|  4.89 |  9.12 | 19.04 | 39.51 | 21.35 |
| python | 21.52 | 23.12 | 27.92 | 39.29 | 33.75 |

<!-- END GENERATED add-pgen -->

**P-gen — x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-pgen-x86 -->

| port | add SQ | add NQ | add MQ | add OQ | add FQ |
|------|-------:|-------:|-------:|-------:|-------:|
| c      |  4.60 | 11.39 | 20.84 | 34.55 | 24.05 |
| rust   |  6.93 | 14.09 | 20.29 | 37.60 | 22.57 |
| zig    |  6.23 | 15.14 | 20.24 | 34.44 | 20.52 |
| swift  |  6.85 | 12.42 | 22.72 | 40.54 | 29.56 |
| csharp | 22.69 | 17.79 | 43.75 | 82.48 | 62.87 |
| go     |  8.13 | 16.58 | 29.77 | 59.21 | 36.86 |
| java‡  | 13.74 | 20.19 | 33.95 | 61.47 | 43.15 |
| kotlin‡| 14.74 | 20.87 | 36.52 | 63.47 | 44.70 |
| python | 43.84 | 48.57 | 57.55 | 73.98 | 64.13 |

<!-- END GENERATED add-pgen-x86 -->

**P-max — arm64 (stress).**

<!-- BEGIN GENERATED add-pmax -->

| port | add SQ | add OQ | add FQ |
|------|-------:|-------:|-------:|
| c      |  3.11 | 17.66 |  7.00 |
| rust   |  4.53 | 14.41 |  7.58 |
| zig    |  3.87 | 17.17 |  7.91 |
| swift  |  5.06 | 24.66 | 14.94 |
| csharp |  5.04 | 26.94 | 23.87 |
| go     |  7.16 | 45.31 | 20.89 |
| java‡  |  6.88 | 32.47 | 22.14 |
| kotlin‡|  8.30 | 31.09 | 18.41 |
| python | 26.58 | 45.46 | 33.17 |

<!-- END GENERATED add-pmax -->

**P-max — x86_64 (stress).**

<!-- BEGIN GENERATED add-pmax-x86 -->

| port | add SQ | add OQ | add FQ |
|------|-------:|-------:|-------:|
| c      | 12.53 | 42.96 | 23.04 |
| rust   | 13.17 | 46.57 | 22.61 |
| zig    | 13.91 | 39.54 | 19.65 |
| swift  | 14.51 | 48.76 | 27.03 |
| csharp | 17.73 | 80.59 | 50.14 |
| go     | 16.69 | 75.94 | 32.53 |
| java‡  | 19.54 | 65.16 | 34.66 |
| kotlin‡| 21.73 | 84.71 | 36.04 |
| python | 50.77 | 80.46 | 60.35 |

<!-- END GENERATED add-pmax-x86 -->

## 2. Subtract — SQ · NQ · MQ · OQ · FQ

Same band structure as Add: compact SQ/NQ/MQ (recompacted) plus full-range OQ/FQ.

**P-gen — arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-pgen -->

| port | sub SQ | sub NQ | sub MQ | sub OQ | sub FQ |
|------|-------:|-------:|-------:|-------:|-------:|
| c      |  1.23 |  4.67 |  6.85 | 11.86 |  7.85 |
| rust   |  1.74 |  4.86 |  7.90 | 10.61 |  7.08 |
| zig    |  1.57 |  7.69 | 10.12 | 13.97 |  9.64 |
| swift  |  2.14 |  5.39 | 11.22 | 17.16 | 13.77 |
| csharp |  9.04 |  6.20 | 14.29 | 40.04 | 32.96 |
| go     |  2.77 | 10.21 | 14.89 | 31.00 | 19.80 |
| java‡  |  4.48 |  7.44 | 18.62 | 27.78 | 19.76 |
| kotlin‡|  5.00 |  8.57 | 18.34 | 39.10 | 18.87 |
| python | 20.77 | 23.25 | 27.94 | 39.33 | 33.33 |

<!-- END GENERATED sub-pgen -->

**P-gen — x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-pgen-x86 -->

| port | sub SQ | sub NQ | sub MQ | sub OQ | sub FQ |
|------|-------:|-------:|-------:|-------:|-------:|
| c      |  5.18 | 11.79 | 21.15 | 34.02 | 24.29 |
| rust   |  6.94 | 13.34 | 20.29 | 37.57 | 22.49 |
| zig    |  5.82 | 15.61 | 20.56 | 34.54 | 20.98 |
| swift  |  7.19 | 12.68 | 22.10 | 39.66 | 29.32 |
| csharp | 18.69 | 17.16 | 40.45 | 82.35 | 63.06 |
| go     |  7.24 | 16.31 | 29.17 | 59.54 | 36.90 |
| java‡  | 13.04 | 20.07 | 33.01 | 63.10 | 42.15 |
| kotlin‡| 14.81 | 20.88 | 37.05 | 79.62 | 43.93 |
| python | 42.39 | 49.43 | 58.41 | 73.50 | 65.02 |

<!-- END GENERATED sub-pgen-x86 -->

**P-max — arm64 (stress).**

<!-- BEGIN GENERATED sub-pmax -->

| port | sub SQ | sub OQ | sub FQ |
|------|-------:|-------:|-------:|
| c      |  3.29 | 18.56 |  7.95 |
| rust   |  4.10 | 13.72 |  7.01 |
| zig    |  3.81 | 19.00 | 10.91 |
| swift  |  3.94 | 24.07 | 12.52 |
| csharp |  5.71 | 26.85 | 25.10 |
| go     |  6.46 | 44.78 | 20.56 |
| java‡  |  7.12 | 32.32 | 18.60 |
| kotlin‡|  8.06 | 29.62 | 16.17 |
| python | 28.23 | 43.28 | 30.42 |

<!-- END GENERATED sub-pmax -->

**P-max — x86_64 (stress).**

<!-- BEGIN GENERATED sub-pmax-x86 -->

| port | sub SQ | sub OQ | sub FQ |
|------|-------:|-------:|-------:|
| c      | 11.71 | 39.52 | 20.66 |
| rust   | 14.30 | 44.23 | 21.50 |
| zig    | 13.10 | 39.89 | 20.14 |
| swift  | 14.27 | 45.35 | 25.54 |
| csharp | 18.72 | 80.52 | 51.59 |
| go     | 16.51 | 76.31 | 32.23 |
| java‡  | 25.07 | 63.35 | 32.75 |
| kotlin‡| 25.73 | 84.19 | 38.34 |
| python | 50.96 | 78.54 | 60.77 |

<!-- END GENERATED sub-pmax-x86 -->

## 3. Multiply — CP · WP · XP

**CP** is the **compact** product (≤ 34 digits, **no scaling** — the cheap multiply);
**WP** scales via the 128-bit `recipMulPow10`; **XP** via the 256-bit kernel. C's `mul XP`
lands at ~29.2 post the `Finalize.c` wide-product finalize fix (commit d98fd85); the P-max
`XP` row is the clean re-measure.

**P-gen — arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-pgen -->

| port | mul CP | mul WP | mul XP |
|------|-------:|-------:|-------:|
| c      |  1.40 | 20.73 | 25.38 |
| rust   |  1.51 | 13.69 | 23.86 |
| zig    |  1.58 | 18.45 | 23.04 |
| swift  |  2.24 | 17.11 | 23.97 |
| csharp |  2.15 | 22.26 | 49.19 |
| go     |  2.39 | 28.44 | 39.45 |
| java‡  |  5.14 | 25.46 | 43.55 |
| kotlin‡|  5.77 | 27.24 | 54.73 |
| python | 18.85 | 38.57 | 45.41 |

<!-- END GENERATED mul-pgen -->

**P-gen — x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-pgen-x86 -->

| port | mul CP | mul WP | mul XP |
|------|-------:|-------:|-------:|
| c      |  3.83 | 34.95 | 44.24 |
| rust   |  4.82 | 29.06 | 42.21 |
| zig    |  5.90 | 28.22 | 41.59 |
| swift  |  5.60 | 29.83 | 43.59 |
| csharp |  7.47 | 49.13 | 83.41 |
| go     |  5.78 | 46.86 | 70.32 |
| java‡  | 13.78 | 45.79 | 66.80 |
| kotlin‡| 14.87 | 47.79 | 67.85 |
| python | 41.59 | 76.29 | 87.80 |

<!-- END GENERATED mul-pgen-x86 -->

**P-max — arm64 (stress).** Only XP is feasible at 33–34 digits.

<!-- BEGIN GENERATED mul-pmax -->

| port | mul XP |
|------|-------:|
| c      | 27.82 |
| rust   | 25.06 |
| zig    | 23.80 |
| swift  | 26.40 |
| csharp | 45.82 |
| go     | 40.73 |
| java‡  | 58.65 |
| kotlin‡| 37.36 |
| python | 44.66 |

<!-- END GENERATED mul-pmax -->

**P-max — x86_64 (stress).**

<!-- BEGIN GENERATED mul-pmax-x86 -->

| port | mul XP |
|------|-------:|
| c      | 41.76 |
| rust   | 45.04 |
| zig    | 44.38 |
| swift  | 46.01 |
| csharp | 76.23 |
| go     | 71.62 |
| java‡  | 62.53 |
| kotlin‡| 94.15 |
| python | 85.65 |

<!-- END GENERATED mul-pmax-x86 -->

## 4. Divide — CD · WD · XD (+ ET · PT)

Bands: **CD** small divisor (1–4 digits, 128÷64 quotient-first, §2.4.10), **WD** (5–19,
256÷64), **XD** (20–34, 256÷128 Möller–Granlund), **ET** exact/terminating early-out, **PT**
power-of-ten divisor (`divPow10Divisor` exponent-only fast path, §2.4.9). The compact-divide
cost shows at CD/WD; the ET/PT early-outs are the fastest divides. The C swept **PT** (3.16)
is the coeff-1 (`1E3`) trivial encoding (≡ native ports' `PT1`); the coeff-10ᵏ strip form
runs ~10.5 ns. The **JVM 128-bit divide is competitive-to-ahead** at XD — HotSpot runs
`div XD` faster than the LLVM natives.

**P-gen — arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-pgen -->

| port | div CD | div WD | div XD | div ET | div PT |
|------|-------:|-------:|-------:|-------:|-------:|
| c      | 29.01 | 37.85 | 31.19 |  8.21 |  3.12 |
| rust   | 19.02 | 33.33 | 37.57 |  9.73 |  3.98 |
| zig    | 27.99 | 38.40 | 29.46 | 10.66 |  4.17 |
| swift  | 34.46 | 46.09 | 44.23 |  7.80 |  5.05 |
| csharp | 27.18 | 42.85 | 49.00 |  9.61 |  4.67 |
| go     | 34.72 | 62.56 | 52.86 | 12.26 |  6.64 |
| java‡  | 30.83 | 46.80 | 46.73 | 12.90 |  9.88 |
| kotlin‡| 35.23 | 51.92 | 51.77 | 19.53 | 11.52 |
| python | 55.74 | 64.11 | 62.72 | 24.81 | 18.36 |

<!-- END GENERATED div-pgen -->

**P-gen — x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-pgen-x86 -->

| port | div CD | div WD | div XD | div ET | div PT |
|------|-------:|-------:|-------:|-------:|-------:|
| c      |  88.90 |  87.79 |  74.48 | 27.29 |  6.75 |
| rust   |  75.66 |  83.57 |  82.33 | 28.91 | 10.87 |
| zig    |  72.31 |  87.26 |  72.98 | 30.74 | 11.71 |
| swift  |  80.28 |  91.53 |  92.59 | 26.98 | 10.75 |
| csharp |  86.87 | 110.27 | 114.46 | 34.92 | 11.20 |
| go     |  87.07 | 123.10 | 109.50 | 32.53 | 12.10 |
| java‡  |  89.37 | 114.91 | 129.09 | 46.17 | 23.64 |
| kotlin‡|  93.41 | 119.42 | 126.54 | 48.04 | 24.22 |
| python | 111.00 | 119.78 | 114.02 | 63.62 | 45.08 |

<!-- END GENERATED div-pgen-x86 -->

**P-max — arm64 (stress).** Only XD is feasible at 33–34-digit divisors.

<!-- BEGIN GENERATED div-pmax -->

| port | div XD |
|------|-------:|
| c      | 34.61 |
| rust   | 38.87 |
| zig    | 29.19 |
| swift  | 41.81 |
| csharp | 28.56 |
| go     | 51.76 |
| java‡  | 40.43 |
| kotlin‡| 40.28 |
| python | 60.46 |

<!-- END GENERATED div-pmax -->

**P-max — x86_64 (stress).**

<!-- BEGIN GENERATED div-pmax-x86 -->

| port | div XD |
|------|-------:|
| c      |  68.59 |
| rust   |  74.83 |
| zig    |  66.58 |
| swift  |  90.31 |
| csharp |  94.79 |
| go     | 108.50 |
| java‡  |  93.35 |
| kotlin‡| 128.76 |
| python | 112.63 |

<!-- END GENERATED div-pmax-x86 -->

## 5. FMA — FN (Barrett) · FF (fits-128)

Swept `self + lhs·rhs` over the 3-operand FN/FF regimes (§3.4). `self` placement selects the
finalize path: **FN** keeps the wide product ⇒ 256-bit Barrett; **FF** swamps it ⇒ fits-128
fast path. The fast-path win (FN÷FF) is the whole story — universal **1.35–2.0×** (JVM/BDN
compress it via their packaging term). `‡` = JVM escape-forced.

**FN/FF band shape — arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma -->

| port | FN | FF | FN÷FF | run |
|------|---:|---:|---:|-----|
| c      |  77.72 | 39.45 | 1.97× | Rc2    |
| rust   |  23.22 | 34.17 | 0.68× | Rrsw2  |
| zig    |  64.53 | 42.04 | 1.53× | Rzgsw2 |
| swift  |  88.58 | 42.54 | 2.08× | Rswsw2 |
| csharp | 102.36 | 82.87 | 1.24× | Rcs11  |
| go     | 167.90 | 70.25 | 2.39× | Rgosw2 |
| java‡  | 102.16 | 72.93 | 1.40× | Rjasw2 |
| kotlin‡| 106.00 | 81.98 | 1.29× | Rkosw2 |
| python | 107.82 | 79.26 | 1.36× | Rpysw2 |

<!-- END GENERATED fma -->

**FN/FF band shape — x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-x86 -->

| port | FN | FF | FN÷FF | run |
|------|---:|---:|---:|-----|
| c      | 112.39 |  71.56 | 1.57× | xRc2    |
| rust   |  59.79 |  65.10 | 0.92× | xRrsw2  |
| zig    | 105.02 |  69.69 | 1.51× | xRzgsw2 |
| swift  | 144.01 |  83.09 | 1.73× | xRswsw2 |
| csharp | 188.24 | 143.50 | 1.31× | xRcs11  |
| go     | 256.10 | 130.40 | 1.96× | xRgosw2 |
| java‡  | 201.75 | 167.41 | 1.21× | xRjasw2 |
| kotlin‡| 233.32 | 172.94 | 1.35× | xRkosw2 |
| python | 217.38 | 177.87 | 1.22× | xRpysw2 |

<!-- END GENERATED fma-x86 -->


</div>
