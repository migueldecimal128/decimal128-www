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

| port | add SQss | add SQos | add NQss | add NQos | add MQss | add MQos | add OQss | add OQos | add FQss | add FQos |
|------|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|
| c      |  0.84 |  2.05 |  3.54 |  4.07 |  5.68 |  9.34 | 11.45 | 16.60 |  8.03 | 10.10 |
| rust   |  0.81 |  2.00 |  3.37 |  3.76 |  5.22 | 11.25 |  9.06 | 13.78 |  8.41 | 10.25 |
| zig    |  1.27 |  2.26 |  4.25 |  4.88 |  6.21 | 12.26 | 12.00 | 15.68 |  8.44 | 10.88 |
| swift  |  1.24 |  2.62 |  4.24 |  4.24 |  5.57 | 12.89 | 15.04 | 22.33 | 11.71 | 13.99 |
| csharp |  1.41 |  3.40 |  7.04 |  7.02 |  8.68 | 25.44 | 17.29 | 33.77 | 13.06 | 15.90 |
| go     |  1.54 |  5.03 |  6.44 | 11.20 | 11.86 | 19.53 | 28.60 | 37.34 | 17.58 | 24.02 |
| java‡  |  3.98 |  4.93 |  8.04 |  9.32 | 11.88 | 30.02 | 21.61 | 46.52 | 17.72 | 33.72 |
| kotlin‡|  4.35 |  6.19 |  8.88 |  9.92 | 13.86 | 27.28 | 24.97 | 44.47 | 16.52 | 28.76 |
| python | 16.24 | 17.76 | 19.19 | 19.53 | 21.25 | 29.40 | 37.80 | 39.87 | 31.21 | 29.96 |

<!-- END GENERATED add-pgen -->

**P-gen — x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-pgen-x86 -->

| port | add SQss | add SQos | add NQss | add NQos | add MQss | add MQos | add OQss | add OQos | add FQss | add FQos |
|------|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|
| c      |  1.58 |  4.51 |  9.07 |  9.15 | 11.71 | 22.07 | 27.08 | 34.84 | 17.46 | 23.49 |
| rust   |  2.01 |  5.22 | 10.75 | 10.67 | 13.32 | 24.87 | 29.93 | 41.69 | 18.73 | 22.87 |
| zig    |  5.00 |  7.47 | 12.34 | 13.18 | 14.23 | 22.72 | 28.07 | 35.28 | 16.77 | 21.26 |
| swift  |  2.56 |  5.32 |  9.44 | 10.65 | 15.83 | 26.44 | 33.12 | 48.10 | 25.33 | 30.82 |
| csharp |  3.61 | 11.00 | 14.73 | 21.06 | 19.62 | 44.01 | 46.94 | 75.53 | 36.19 | 43.83 |
| go     |  3.19 |  9.10 | 11.33 | 16.58 | 19.01 | 32.50 | 46.99 | 62.84 | 30.34 | 36.96 |
| java‡  |  7.22 | 16.04 | 18.53 | 27.36 | 25.59 | 40.08 | 55.34 | 73.65 | 34.89 | 45.29 |
| kotlin‡| 10.67 | 16.00 | 16.64 | 23.28 | 23.78 | 38.78 | 57.57 | 82.83 | 34.24 | 41.62 |
| python | 39.01 | 43.90 | 44.75 | 45.94 | 47.53 | 58.98 | 65.23 | 73.44 | 56.29 | 63.93 |

<!-- END GENERATED add-pgen-x86 -->

**P-max — arm64 (stress).**

<!-- BEGIN GENERATED add-pmax -->

| port | add SQss | add SQos | add OQss | add OQos | add FQss | add FQos |
|------|-------:|-------:|-------:|-------:|-------:|-------:|
| c      |  3.23 |  2.93 | 18.26 | 26.88 |  9.42 | 12.26 |
| rust   |  5.17 |  4.05 | 12.51 | 23.06 | 10.39 | 12.61 |
| zig    |  3.59 |  3.77 | 17.31 | 20.76 |  9.93 | 11.80 |
| swift  |  4.86 |  4.87 | 21.79 | 29.40 | 11.58 | 17.21 |
| csharp |  5.45 |  4.43 | 22.93 | 31.38 | 16.03 | 21.23 |
| go     |  8.74 |  6.64 | 39.79 | 51.10 | 18.64 | 22.81 |
| java‡  |  6.84 |  9.07 | 22.26 | 41.27 | 21.05 | 30.26 |
| kotlin‡|  8.71 |  7.91 | 24.98 | 37.82 | 28.77 | 29.17 |
| python | 29.04 | 25.50 | 43.42 | 44.83 | 30.97 | 29.29 |

<!-- END GENERATED add-pmax -->

**P-max — x86_64 (stress).**

<!-- BEGIN GENERATED add-pmax-x86 -->

| port | add SQss | add SQos | add OQss | add OQos | add FQss | add FQos |
|------|-------:|-------:|-------:|-------:|-------:|-------:|
| c      | 10.75 |  9.82 | 35.99 | 42.27 | 16.27 | 22.68 |
| rust   | 12.61 | 10.82 | 38.60 | 48.91 | 20.44 | 23.72 |
| zig    | 13.10 | 12.29 | 34.49 | 39.78 | 17.45 | 20.52 |
| swift  | 13.90 | 10.97 | 40.44 | 54.13 | 22.97 | 27.66 |
| csharp | 17.42 | 15.85 | 61.73 | 82.61 | 34.63 | 41.40 |
| go     | 15.26 | 14.05 | 61.37 | 79.30 | 26.15 | 33.44 |
| java‡  | 18.94 | 20.71 | 53.61 | 64.04 | 28.11 | 34.83 |
| kotlin‡| 19.91 | 26.21 | 64.63 | 91.49 | 30.19 | 36.79 |
| python | 49.52 | 48.71 | 74.60 | 81.17 | 54.76 | 62.60 |

<!-- END GENERATED add-pmax-x86 -->

## 2. Subtract — SQ · NQ · MQ · OQ · FQ

Same band structure as Add: compact SQ/NQ/MQ (recompacted) plus full-range OQ/FQ.

**P-gen — arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-pgen -->

| port | sub SQss | sub SQos | sub NQss | sub NQos | sub MQss | sub MQos | sub OQss | sub OQos | sub FQss | sub FQos |
|------|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|
| c      |  1.51 |  0.93 |  4.06 |  3.46 |  9.73 |  5.59 | 17.20 | 11.85 | 10.70 |  8.95 |
| rust   |  1.36 |  1.06 |  3.74 |  3.45 | 11.32 |  5.08 | 13.44 |  9.05 |  9.95 |  8.06 |
| zig    |  1.69 |  1.32 |  4.93 |  4.29 | 12.78 |  6.23 | 16.28 | 12.95 | 11.10 |  9.44 |
| swift  |  1.61 |  1.48 |  3.46 |  3.44 | 11.62 |  4.79 | 20.94 | 14.10 | 13.25 | 10.24 |
| csharp |  2.29 |  1.52 |  6.37 |  5.61 | 15.91 |  8.68 | 31.44 | 16.25 | 14.63 | 12.14 |
| go     |  2.92 |  1.62 | 10.68 |  5.59 | 18.11 | 11.53 | 36.44 | 27.58 | 22.72 | 16.72 |
| java‡  |  4.90 |  4.18 |  8.35 |  7.65 | 29.21 | 10.91 | 45.72 | 21.31 | 33.14 | 17.28 |
| kotlin‡|  5.20 |  3.66 |  9.35 |  8.70 | 27.38 | 13.23 | 43.18 | 25.00 | 28.39 | 18.11 |
| python | 16.44 | 16.05 | 19.34 | 18.91 | 28.38 | 20.76 | 38.91 | 36.73 | 29.49 | 30.99 |

<!-- END GENERATED sub-pgen -->

**P-gen — x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-pgen-x86 -->

| port | sub SQss | sub SQos | sub NQss | sub NQos | sub MQss | sub MQos | sub OQss | sub OQos | sub FQss | sub FQos |
|------|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|
| c      |  3.99 |  2.20 |  9.81 |  9.55 | 22.29 | 12.03 | 34.35 | 26.67 | 23.86 | 17.63 |
| rust   |  4.47 |  3.25 | 10.67 |  9.86 | 23.60 | 13.66 | 41.21 | 30.02 | 23.13 | 17.91 |
| zig    |  6.74 |  5.11 | 13.52 | 12.79 | 22.66 | 14.56 | 34.51 | 28.49 | 21.60 | 17.26 |
| swift  |  4.71 |  3.12 | 10.64 | 10.07 | 28.07 | 15.40 | 44.93 | 34.17 | 31.44 | 25.55 |
| csharp |  9.87 |  4.52 | 18.19 | 11.43 | 42.52 | 21.06 | 77.01 | 44.27 | 41.50 | 35.68 |
| go     |  7.68 |  3.32 | 16.58 | 11.16 | 32.76 | 18.75 | 62.41 | 46.21 | 36.72 | 29.16 |
| java‡  | 14.29 | 10.57 | 28.64 | 20.03 | 39.76 | 25.05 | 70.87 | 59.94 | 47.92 | 36.63 |
| kotlin‡| 14.89 | 10.03 | 25.07 | 17.45 | 41.05 | 25.73 | 82.85 | 62.21 | 42.91 | 35.15 |
| python | 41.92 | 39.67 | 47.07 | 45.14 | 59.81 | 48.12 | 74.08 | 65.32 | 65.14 | 58.49 |

<!-- END GENERATED sub-pgen-x86 -->

**P-max — arm64 (stress).**

<!-- BEGIN GENERATED sub-pmax -->

| port | sub SQss | sub SQos | sub OQss | sub OQos | sub FQss | sub FQos |
|------|-------:|-------:|-------:|-------:|-------:|-------:|
| c      |  2.65 |  3.54 | 24.68 | 19.47 | 10.45 | 10.28 |
| rust   |  2.88 |  4.98 | 22.32 | 12.52 | 10.85 |  9.92 |
| zig    |  3.48 |  3.85 | 20.95 | 18.86 | 11.99 | 12.11 |
| swift  |  3.69 |  4.69 | 27.14 | 20.24 | 14.06 | 10.80 |
| csharp |  4.67 |  5.11 | 28.98 | 21.26 | 19.86 | 10.49 |
| go     |  5.06 |  8.03 | 50.38 | 39.26 | 22.29 | 17.44 |
| java‡  |  6.15 |  6.98 | 40.73 | 22.23 | 30.11 | 30.25 |
| kotlin‡|  7.34 |  8.05 | 36.05 | 23.85 | 28.30 | 25.90 |
| python | 25.84 | 29.52 | 43.00 | 41.08 | 26.88 | 27.43 |

<!-- END GENERATED sub-pmax -->

**P-max — x86_64 (stress).**

<!-- BEGIN GENERATED sub-pmax-x86 -->

| port | sub SQss | sub SQos | sub OQss | sub OQos | sub FQss | sub FQos |
|------|-------:|-------:|-------:|-------:|-------:|-------:|
| c      | 10.12 | 11.53 | 39.13 | 34.10 | 20.68 | 15.80 |
| rust   | 10.04 | 13.14 | 45.83 | 36.09 | 21.24 | 18.80 |
| zig    | 11.76 | 13.50 | 38.67 | 35.20 | 20.39 | 17.23 |
| swift  | 10.72 | 14.35 | 49.03 | 39.01 | 25.63 | 20.75 |
| csharp | 17.51 | 15.89 | 81.67 | 59.71 | 41.01 | 32.86 |
| go     | 12.93 | 14.90 | 80.25 | 60.51 | 32.41 | 25.62 |
| java‡  | 18.13 | 22.19 | 62.75 | 52.24 | 33.94 | 26.61 |
| kotlin‡| 23.65 | 22.98 | 93.83 | 65.91 | 38.99 | 31.87 |
| python | 46.99 | 51.05 | 78.92 | 72.68 | 61.21 | 57.04 |

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
| c      |  1.50 | 20.65 | 25.47 |
| rust   |  1.52 | 13.81 | 25.03 |
| zig    |  1.58 | 18.69 | 22.90 |
| swift  |  2.28 | 17.01 | 24.01 |
| csharp |  2.07 | 16.46 | 43.54 |
| go     |  2.46 | 28.35 | 39.72 |
| java‡  |  5.46 | 30.42 | 45.83 |
| kotlin‡|  5.54 | 29.88 | 42.63 |
| python | 19.07 | 39.25 | 46.47 |

<!-- END GENERATED mul-pgen -->

**P-gen — x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-pgen-x86 -->

| port | mul CP | mul WP | mul XP |
|------|-------:|-------:|-------:|
| c      |  3.36 | 33.58 | 43.09 |
| rust   |  5.46 | 29.98 | 43.70 |
| zig    |  6.07 | 28.44 | 41.98 |
| swift  |  6.13 | 30.01 | 45.67 |
| csharp |  7.59 | 43.06 | 77.48 |
| go     |  5.76 | 47.91 | 71.81 |
| java‡  | 13.96 | 46.25 | 67.77 |
| kotlin‡| 13.34 | 51.92 | 96.56 |
| python | 42.76 | 78.71 | 88.01 |

<!-- END GENERATED mul-pgen-x86 -->

**P-max — arm64 (stress).** Only XP is feasible at 33–34 digits.

<!-- BEGIN GENERATED mul-pmax -->

| port | mul XP |
|------|-------:|
| c      | 27.82 |
| rust   | 26.31 |
| zig    | 23.88 |
| swift  | 26.46 |
| csharp | 45.16 |
| go     | 41.26 |
| java‡  | 47.64 |
| kotlin‡| 38.80 |
| python | 45.32 |

<!-- END GENERATED mul-pmax -->

**P-max — x86_64 (stress).**

<!-- BEGIN GENERATED mul-pmax-x86 -->

| port | mul XP |
|------|-------:|
| c      |  42.12 |
| rust   |  46.47 |
| zig    |  44.78 |
| swift  |  50.40 |
| csharp | 128.27 |
| go     |  72.20 |
| java‡  |  64.71 |
| kotlin‡|  93.74 |
| python |  85.91 |

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
| c      | 28.50 | 37.47 | 32.73 |  8.24 |  3.12 |
| rust   | 20.04 | 37.80 | 37.84 |  9.60 |  3.99 |
| zig    | 30.28 | 40.30 | 32.08 | 10.70 |  4.13 |
| swift  | 35.31 | 46.90 | 44.89 |  7.77 |  5.02 |
| csharp | 28.67 | 31.31 | 35.54 | 13.16 |  5.05 |
| go     | 35.09 | 61.48 | 58.03 | 12.35 |  6.64 |
| java‡  | 31.73 | 48.72 | 50.17 | 14.21 | 11.33 |
| kotlin‡| 34.17 | 49.78 | 52.47 | 19.76 | 11.71 |
| python | 56.20 | 65.65 | 63.05 | 25.33 | 18.52 |

<!-- END GENERATED div-pgen -->

**P-gen — x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-pgen-x86 -->

| port | div CD | div WD | div XD | div ET | div PT |
|------|-------:|-------:|-------:|-------:|-------:|
| c      |  72.13 |  85.25 |  74.22 | 25.89 |  6.75 |
| rust   |  77.73 |  84.82 |  84.40 | 28.97 |  9.49 |
| zig    |  73.67 |  89.09 |  74.79 | 31.62 | 11.95 |
| swift  |  83.15 |  94.28 |  99.44 | 29.40 | 10.82 |
| csharp |  93.04 |  97.29 | 105.37 | 32.85 | 10.58 |
| go     |  87.33 | 122.90 | 107.50 | 32.44 | 12.07 |
| java‡  |  93.35 | 119.04 | 131.80 | 47.14 | 23.57 |
| kotlin‡|  97.97 | 135.59 | 153.35 | 49.06 | 26.00 |
| python | 111.49 | 120.52 | 116.64 | 68.24 | 44.72 |

<!-- END GENERATED div-pgen-x86 -->

**P-max — arm64 (stress).** Only XD is feasible at 33–34-digit divisors.

<!-- BEGIN GENERATED div-pmax -->

| port | div XD |
|------|-------:|
| c      | 32.06 |
| rust   | 41.04 |
| zig    | 30.38 |
| swift  | 42.03 |
| csharp | 29.13 |
| go     | 52.02 |
| java‡  | 36.78 |
| kotlin‡| 41.52 |
| python | 61.27 |

<!-- END GENERATED div-pmax -->

**P-max — x86_64 (stress).**

<!-- BEGIN GENERATED div-pmax-x86 -->

| port | div XD |
|------|-------:|
| c      |  68.96 |
| rust   |  74.44 |
| zig    |  67.81 |
| swift  |  97.07 |
| csharp | 163.42 |
| go     | 102.10 |
| java‡  |  92.09 |
| kotlin‡| 138.84 |
| python | 116.96 |

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
| c      |  76.24 | 39.70 | 1.92× | Rc2    |
| rust   |  22.84 | 35.77 | 0.64× | Rrsw2  |
| zig    |  64.07 | 41.72 | 1.54× | Rzgsw2 |
| swift  |  89.90 | 42.70 | 2.11× | Rswsw2 |
| csharp | 103.37 | 76.63 | 1.35× | Rcs11  |
| go     | 159.20 | 72.84 | 2.19× | Rgosw2 |
| java‡  | 100.71 | 71.66 | 1.41× | Rjasw2 |
| kotlin‡| 110.65 | 89.52 | 1.24× | Rkosw2 |
| python | 110.01 | 79.92 | 1.38× | Rpysw2 |

<!-- END GENERATED fma -->

**FN/FF band shape — x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-x86 -->

| port | FN | FF | FN÷FF | run |
|------|---:|---:|---:|-----|
| c      | 114.77 |  72.99 | 1.57× | xRc2    |
| rust   |  60.95 |  68.80 | 0.89× | xRrsw2  |
| zig    | 110.44 |  70.08 | 1.58× | xRzgsw2 |
| swift  | 145.85 |  82.19 | 1.77× | xRswsw2 |
| csharp | 186.16 | 130.74 | 1.42× | xRcs11  |
| go     | 250.30 | 130.30 | 1.92× | xRgosw2 |
| java‡  | 199.38 | 167.29 | 1.19× | xRjasw2 |
| kotlin‡| 235.97 | 178.28 | 1.32× | xRkosw2 |
| python | 228.93 | 185.09 | 1.24× | xRpysw2 |

<!-- END GENERATED fma-x86 -->


</div>
