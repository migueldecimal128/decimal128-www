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
| csharp |  1.44 |  2.92 |  6.20 |  6.98 | 10.27 | 15.46 | 17.35 | 25.12 | 10.38 | 14.92 |
| go     |  1.54 |  5.03 |  6.44 | 11.20 | 11.86 | 19.53 | 28.60 | 37.34 | 17.58 | 24.02 |
| java‡  |  3.98 |  4.93 |  8.04 |  9.32 | 11.88 | 30.02 | 21.61 | 46.52 | 17.72 | 33.72 |
| kotlin‡|  4.35 |  6.19 |  8.88 |  9.92 | 13.86 | 27.28 | 24.97 | 44.47 | 16.52 | 28.76 |
| python | 16.24 | 17.76 | 19.19 | 19.53 | 21.25 | 29.40 | 37.80 | 39.87 | 31.21 | 29.96 |

<!-- END GENERATED add-pgen -->

**P-gen — x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-pgen-x86 -->

| port | add SQss | add SQos | add NQss | add NQos | add MQss | add MQos | add OQss | add OQos | add FQss | add FQos |
|------|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|
| c      |  2.03 |  4.47 |  9.00 |  9.18 | 11.72 | 22.04 | 27.31 | 35.26 | 17.65 | 23.89 |
| rust   |  2.41 |  5.40 | 10.25 | 10.47 | 13.51 | 24.66 | 30.35 | 41.67 | 18.09 | 22.24 |
| zig    |  4.92 |  7.28 | 12.12 | 13.15 | 14.25 | 22.63 | 27.93 | 34.21 | 16.55 | 21.07 |
| swift  |  2.44 |  5.08 |  9.29 | 10.03 | 15.04 | 27.79 | 32.04 | 43.23 | 24.54 | 29.73 |
| csharp |  4.12 | 12.53 | 16.26 | 22.84 | 23.41 | 45.14 | 50.70 | 73.96 | 32.61 | 45.98 |
| go     |  3.13 |  9.01 | 11.40 | 16.91 | 19.04 | 32.59 | 46.99 | 62.47 | 29.44 | 37.04 |
| java‡  |  6.74 | 15.83 | 18.42 | 26.10 | 23.64 | 37.61 | 52.12 | 67.21 | 34.70 | 44.10 |
| kotlin‡| 10.84 | 15.53 | 16.79 | 23.28 | 24.03 | 36.95 | 52.95 | 81.88 | 35.62 | 44.75 |
| python | 38.55 | 41.46 | 44.13 | 45.77 | 47.51 | 60.92 | 66.58 | 73.91 | 57.27 | 64.60 |

<!-- END GENERATED add-pgen-x86 -->

**P-max — arm64 (stress).**

<!-- BEGIN GENERATED add-pmax -->

| port | add SQss | add SQos | add OQss | add OQos | add FQss | add FQos |
|------|-------:|-------:|-------:|-------:|-------:|-------:|
| c      |  3.23 |  2.93 | 18.26 | 26.88 |  9.42 | 12.26 |
| rust   |  5.17 |  4.05 | 12.51 | 23.06 | 10.39 | 12.61 |
| zig    |  3.59 |  3.77 | 17.31 | 20.76 |  9.93 | 11.80 |
| swift  |  4.86 |  4.87 | 21.79 | 29.40 | 11.58 | 17.21 |
| csharp |  5.20 |  4.51 | 21.99 | 32.17 |  8.59 | 13.33 |
| go     |  8.74 |  6.64 | 39.79 | 51.10 | 18.64 | 22.81 |
| java‡  |  6.84 |  9.07 | 22.26 | 41.27 | 21.05 | 30.26 |
| kotlin‡|  8.71 |  7.91 | 24.98 | 37.82 | 28.77 | 29.17 |
| python | 29.04 | 25.50 | 43.42 | 44.83 | 30.97 | 29.29 |

<!-- END GENERATED add-pmax -->

**P-max — x86_64 (stress).**

<!-- BEGIN GENERATED add-pmax-x86 -->

| port | add SQss | add SQos | add OQss | add OQos | add FQss | add FQos |
|------|-------:|-------:|-------:|-------:|-------:|-------:|
| c      | 11.92 |  9.75 | 35.98 | 42.46 | 16.19 | 22.54 |
| rust   | 12.49 | 10.65 | 37.91 | 48.77 | 20.33 | 23.27 |
| zig    | 12.94 | 12.10 | 33.63 | 38.41 | 16.78 | 20.20 |
| swift  | 13.70 | 11.10 | 40.04 | 51.87 | 22.67 | 27.74 |
| csharp | 18.27 | 16.37 | 69.35 | 90.41 | 32.30 | 43.31 |
| go     | 15.08 | 13.98 | 61.25 | 80.76 | 25.87 | 33.20 |
| java‡  | 18.32 | 20.47 | 52.94 | 63.56 | 27.58 | 33.58 |
| kotlin‡| 24.20 | 21.20 | 64.77 | 86.96 | 32.32 | 36.89 |
| python | 48.63 | 45.57 | 71.99 | 80.05 | 53.39 | 59.28 |

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
| csharp |  2.27 |  1.68 |  6.31 |  5.17 | 14.38 |  8.59 | 23.37 | 16.48 | 13.44 |  9.18 |
| go     |  2.92 |  1.62 | 10.68 |  5.59 | 18.11 | 11.53 | 36.44 | 27.58 | 22.72 | 16.72 |
| java‡  |  4.90 |  4.18 |  8.35 |  7.65 | 29.21 | 10.91 | 45.72 | 21.31 | 33.14 | 17.28 |
| kotlin‡|  5.20 |  3.66 |  9.35 |  8.70 | 27.38 | 13.23 | 43.18 | 25.00 | 28.39 | 18.11 |
| python | 16.44 | 16.05 | 19.34 | 18.91 | 28.38 | 20.76 | 38.91 | 36.73 | 29.49 | 30.99 |

<!-- END GENERATED sub-pgen -->

**P-gen — x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-pgen-x86 -->

| port | sub SQss | sub SQos | sub NQss | sub NQos | sub MQss | sub MQos | sub OQss | sub OQos | sub FQss | sub FQos |
|------|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|
| c      |  4.05 |  2.02 |  9.87 |  9.59 | 22.44 | 12.16 | 34.57 | 26.66 | 23.82 | 17.66 |
| rust   |  4.43 |  3.28 | 10.51 |  9.97 | 23.73 | 13.85 | 41.61 | 29.13 | 22.17 | 17.12 |
| zig    |  6.62 |  5.07 | 14.10 | 12.56 | 22.85 | 14.54 | 34.14 | 28.25 | 21.29 | 16.98 |
| swift  |  4.40 |  3.09 | 10.16 |  9.46 | 25.09 | 15.08 | 42.03 | 31.78 | 29.58 | 23.95 |
| csharp | 10.26 |  4.94 | 19.64 | 12.48 | 43.08 | 20.11 | 70.18 | 47.78 | 51.51 | 29.04 |
| go     |  8.08 |  3.31 | 16.32 | 11.45 | 32.15 | 18.76 | 61.83 | 46.20 | 36.45 | 29.27 |
| java‡  | 14.09 |  9.64 | 26.87 | 18.22 | 37.16 | 23.42 | 66.52 | 51.03 | 43.00 | 33.92 |
| kotlin‡| 15.06 |  9.69 | 24.62 | 17.95 | 38.25 | 25.55 | 83.63 | 54.07 | 47.19 | 35.50 |
| python | 40.02 | 38.44 | 46.63 | 45.32 | 61.19 | 48.14 | 73.42 | 66.22 | 64.83 | 57.36 |

<!-- END GENERATED sub-pgen-x86 -->

**P-max — arm64 (stress).**

<!-- BEGIN GENERATED sub-pmax -->

| port | sub SQss | sub SQos | sub OQss | sub OQos | sub FQss | sub FQos |
|------|-------:|-------:|-------:|-------:|-------:|-------:|
| c      |  2.65 |  3.54 | 24.68 | 19.47 | 10.45 | 10.28 |
| rust   |  2.88 |  4.98 | 22.32 | 12.52 | 10.85 |  9.92 |
| zig    |  3.48 |  3.85 | 20.95 | 18.86 | 11.99 | 12.11 |
| swift  |  3.69 |  4.69 | 27.14 | 20.24 | 14.06 | 10.80 |
| csharp |  4.99 |  5.19 | 31.14 | 21.32 | 12.25 |  7.94 |
| go     |  5.06 |  8.03 | 50.38 | 39.26 | 22.29 | 17.44 |
| java‡  |  6.15 |  6.98 | 40.73 | 22.23 | 30.11 | 30.25 |
| kotlin‡|  7.34 |  8.05 | 36.05 | 23.85 | 28.30 | 25.90 |
| python | 25.84 | 29.52 | 43.00 | 41.08 | 26.88 | 27.43 |

<!-- END GENERATED sub-pmax -->

**P-max — x86_64 (stress).**

<!-- BEGIN GENERATED sub-pmax-x86 -->

| port | sub SQss | sub SQos | sub OQss | sub OQos | sub FQss | sub FQos |
|------|-------:|-------:|-------:|-------:|-------:|-------:|
| c      | 10.93 | 11.37 | 39.02 | 33.95 | 20.50 | 15.74 |
| rust   | 10.09 | 13.09 | 45.27 | 35.70 | 21.01 | 18.15 |
| zig    | 11.57 | 13.27 | 38.47 | 34.64 | 20.00 | 17.26 |
| swift  | 10.30 | 14.05 | 47.57 | 38.58 | 25.20 | 20.69 |
| csharp | 16.61 | 17.02 | 88.09 | 65.22 | 40.63 | 25.70 |
| go     | 12.74 | 14.71 | 79.94 | 60.83 | 32.50 | 25.56 |
| java‡  | 17.45 | 21.27 | 62.77 | 51.11 | 32.63 | 29.19 |
| kotlin‡| 21.35 | 25.25 | 91.89 | 68.02 | 38.69 | 32.69 |
| python | 46.11 | 48.04 | 77.42 | 71.07 | 59.33 | 53.00 |

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
| csharp |  2.15 | 16.42 | 43.68 |
| go     |  2.46 | 28.35 | 39.72 |
| java‡  |  5.46 | 30.42 | 45.83 |
| kotlin‡|  5.54 | 29.88 | 42.63 |
| python | 19.07 | 39.25 | 46.47 |

<!-- END GENERATED mul-pgen -->

**P-gen — x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-pgen-x86 -->

| port | mul CP | mul WP | mul XP |
|------|-------:|-------:|-------:|
| c      |  3.34 | 33.09 | 42.43 |
| rust   |  5.20 | 29.08 | 42.34 |
| zig    |  6.06 | 28.06 | 41.73 |
| swift  |  5.66 | 29.66 | 42.94 |
| csharp |  8.09 | 46.02 | 86.77 |
| go     |  5.78 | 47.84 | 71.93 |
| java‡  | 13.18 | 43.99 | 63.42 |
| kotlin‡| 14.27 | 53.27 | 92.36 |
| python | 40.91 | 78.97 | 86.96 |

<!-- END GENERATED mul-pgen-x86 -->

**P-max — arm64 (stress).** Only XP is feasible at 33–34 digits.

<!-- BEGIN GENERATED mul-pmax -->

| port | mul XP |
|------|-------:|
| c      | 27.82 |
| rust   | 26.31 |
| zig    | 23.88 |
| swift  | 26.46 |
| csharp | 44.65 |
| go     | 41.26 |
| java‡  | 47.64 |
| kotlin‡| 38.80 |
| python | 45.32 |

<!-- END GENERATED mul-pmax -->

**P-max — x86_64 (stress).**

<!-- BEGIN GENERATED mul-pmax-x86 -->

| port | mul XP |
|------|-------:|
| c      | 42.45 |
| rust   | 45.89 |
| zig    | 44.52 |
| swift  | 45.69 |
| csharp | 82.55 |
| go     | 72.78 |
| java‡  | 61.99 |
| kotlin‡| 93.27 |
| python | 83.30 |

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
| csharp | 23.76 | 30.64 | 31.84 |  6.91 |  3.54 |
| go     | 35.09 | 61.48 | 58.03 | 12.35 |  6.64 |
| java‡  | 31.73 | 48.72 | 50.17 | 14.21 | 11.33 |
| kotlin‡| 34.17 | 49.78 | 52.47 | 19.76 | 11.71 |
| python | 56.20 | 65.65 | 63.05 | 25.33 | 18.52 |

<!-- END GENERATED div-pgen -->

**P-gen — x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-pgen-x86 -->

| port | div CD | div WD | div XD | div ET | div PT |
|------|-------:|-------:|-------:|-------:|-------:|
| c      |  70.52 |  84.35 |  73.79 | 25.84 |  6.71 |
| rust   |  75.94 |  82.73 |  82.60 | 28.45 |  9.32 |
| zig    |  73.17 |  88.27 |  73.48 | 31.04 | 11.76 |
| swift  |  78.30 |  91.05 |  92.84 | 26.92 | 10.55 |
| csharp |  92.95 | 106.44 | 108.38 | 37.68 | 10.22 |
| go     |  87.21 | 123.00 | 107.80 | 32.82 | 12.03 |
| java‡  |  88.17 | 115.91 | 124.04 | 45.41 | 23.34 |
| kotlin‡|  93.05 | 124.85 | 145.96 | 49.48 | 24.17 |
| python | 111.15 | 119.58 | 112.15 | 61.75 | 42.96 |

<!-- END GENERATED div-pgen-x86 -->

**P-max — arm64 (stress).** Only XD is feasible at 33–34-digit divisors.

<!-- BEGIN GENERATED div-pmax -->

| port | div XD |
|------|-------:|
| c      | 32.06 |
| rust   | 41.04 |
| zig    | 30.38 |
| swift  | 42.03 |
| csharp | 29.49 |
| go     | 52.02 |
| java‡  | 36.78 |
| kotlin‡| 41.52 |
| python | 61.27 |

<!-- END GENERATED div-pmax -->

**P-max — x86_64 (stress).**

<!-- BEGIN GENERATED div-pmax-x86 -->

| port | div XD |
|------|-------:|
| c      |  69.08 |
| rust   |  73.40 |
| zig    |  66.51 |
| swift  |  92.88 |
| csharp |  98.83 |
| go     | 104.30 |
| java‡  |  90.39 |
| kotlin‡| 136.17 |
| python | 107.00 |

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
| csharp | 103.04 | 74.62 | 1.38× | Rcs12  |
| go     | 159.20 | 72.84 | 2.19× | Rgosw2 |
| java‡  | 100.71 | 71.66 | 1.41× | Rjasw2 |
| kotlin‡| 110.65 | 89.52 | 1.24× | Rkosw2 |
| python | 110.01 | 79.92 | 1.38× | Rpysw2 |

<!-- END GENERATED fma -->

**FN/FF band shape — x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-x86 -->

| port | FN | FF | FN÷FF | run |
|------|---:|---:|---:|-----|
| c      | 114.54 |  72.55 | 1.58× | xRc2    |
| rust   |  59.85 |  65.75 | 0.91× | xRrsw2  |
| zig    | 105.20 |  69.56 | 1.51× | xRzgsw2 |
| swift  | 145.47 |  81.06 | 1.79× | xRswsw2 |
| csharp | 207.75 | 148.05 | 1.40× | xRcs12  |
| go     | 249.80 | 130.70 | 1.91× | xRgosw2 |
| java‡  | 200.34 | 168.33 | 1.19× | xRjasw2 |
| kotlin‡| 235.31 | 179.42 | 1.31× | xRkosw2 |
| python | 213.95 | 174.56 | 1.23× | xRpysw2 |

<!-- END GENERATED fma-x86 -->


</div>
