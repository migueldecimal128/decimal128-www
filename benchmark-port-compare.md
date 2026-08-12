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
| c      |  2.28 |  5.09 | 10.13 | 10.32 | 13.01 | 24.27 | 30.45 |  38.89 | 19.46 | 26.44 |
| rust   |  2.53 |  6.59 | 11.20 | 11.45 | 14.54 | 26.48 | 32.30 |  44.79 | 20.10 | 24.88 |
| zig    |  5.47 |  7.97 | 13.50 | 14.78 | 15.48 | 25.00 | 30.44 |  37.51 | 18.61 | 23.80 |
| swift  |  2.99 |  5.69 | 10.53 | 11.50 | 16.44 | 27.89 | 35.76 |  48.08 | 26.96 | 32.71 |
| csharp |  4.36 | 17.08 | 16.54 | 22.69 | 24.66 | 41.85 | 54.72 |  82.50 | 35.53 | 51.96 |
| go     |  3.47 |  9.82 | 12.51 | 17.40 | 20.81 | 34.95 | 51.43 |  78.79 | 32.77 | 40.59 |
| java‡  |  9.60 | 18.85 | 21.81 | 25.04 | 26.70 | 41.48 | 60.65 |  77.85 | 39.66 | 54.32 |
| kotlin‡| 14.73 | 23.50 | 24.56 | 32.30 | 33.27 | 51.28 | 70.56 | 101.24 | 43.35 | 48.66 |
| python | 47.47 | 45.53 | 49.61 | 51.11 | 53.89 | 67.98 | 75.68 |  84.52 | 69.42 | 77.41 |

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
| c      | 12.96 | 10.95 | 40.38 | 47.13 | 18.24 | 26.71 |
| rust   | 14.69 | 11.67 | 42.55 | 54.22 | 22.44 | 25.79 |
| zig    | 14.15 | 13.48 | 42.83 | 42.64 | 18.36 | 23.13 |
| swift  | 16.97 | 11.97 | 44.39 | 56.50 | 25.26 | 34.53 |
| csharp | 21.43 | 18.21 | 66.64 | 92.07 | 33.51 | 49.18 |
| go     | 19.05 | 15.28 | 66.74 | 87.79 | 29.17 | 36.67 |
| java‡  | 22.96 | 22.19 | 60.74 | 77.64 | 34.65 | 43.25 |
| kotlin‡| 23.21 | 27.14 | 73.31 | 91.18 | 39.20 | 49.10 |
| python | 53.69 | 60.64 | 84.37 | 90.42 | 60.11 | 67.78 |

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
| c      |  4.57 |  2.32 | 10.94 | 10.72 | 24.68 | 13.60 |  38.90 | 30.00 | 26.63 | 20.62 |
| rust   |  5.08 |  4.03 | 11.41 | 10.86 | 25.85 | 14.91 |  43.96 | 32.49 | 24.65 | 19.85 |
| zig    |  7.50 |  5.48 | 14.93 | 13.86 | 25.01 | 15.99 |  38.38 | 31.54 | 23.74 | 20.71 |
| swift  |  5.11 |  3.73 | 11.78 | 10.59 | 28.39 | 16.66 |  45.79 | 35.71 | 32.62 | 26.54 |
| csharp | 11.27 |  5.38 | 24.02 | 12.96 | 40.13 | 24.86 |  76.78 | 52.25 | 47.91 | 35.58 |
| go     |  8.78 |  3.88 | 17.03 | 12.17 | 34.93 | 20.41 |  69.12 | 50.94 | 45.88 | 37.08 |
| java‡  | 15.90 | 13.16 | 23.78 | 19.38 | 39.94 | 24.70 |  83.12 | 62.03 | 52.97 | 41.69 |
| kotlin‡| 18.91 | 13.99 | 31.74 | 27.44 | 47.73 | 33.69 | 106.02 | 73.52 | 54.19 | 41.09 |
| python | 44.05 | 42.70 | 53.96 | 51.33 | 68.96 | 59.49 |  83.41 | 84.04 | 73.58 | 64.67 |

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
| c      | 12.20 | 12.78 |  44.25 | 37.80 | 22.92 | 17.42 |
| rust   | 10.89 | 14.57 |  50.29 | 39.49 | 23.72 | 20.14 |
| zig    | 12.68 | 16.82 |  44.10 | 38.37 | 22.10 | 19.13 |
| swift  | 12.89 | 15.20 |  53.76 | 42.02 | 28.82 | 23.08 |
| csharp | 20.95 | 20.30 |  99.83 | 66.28 | 46.02 | 31.20 |
| go     | 14.11 | 18.48 | 100.90 | 76.59 | 36.08 | 27.83 |
| java‡  | 20.48 | 26.55 |  77.33 | 61.43 | 47.99 | 33.84 |
| kotlin‡| 23.69 | 23.92 |  93.50 | 73.40 | 50.28 | 42.63 |
| python | 51.62 | 55.38 |  86.84 | 92.61 | 67.19 | 59.81 |

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
| c      |  3.86 |  37.34 |  47.91 |
| rust   |  6.07 |  32.36 |  46.76 |
| zig    |  7.46 |  36.01 |  48.32 |
| swift  |  6.41 |  32.66 |  46.99 |
| csharp | 10.44 |  51.48 |  90.48 |
| go     |  6.43 |  52.28 |  78.60 |
| java‡  | 16.20 |  58.63 |  81.20 |
| kotlin‡| 17.36 |  64.37 | 110.91 |
| python | 46.00 | 101.93 | 104.05 |

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
| c      | 48.45 |
| rust   | 51.39 |
| zig    | 50.34 |
| swift  | 50.35 |
| csharp | 93.68 |
| go     | 90.42 |
| java‡  | 69.62 |
| kotlin‡| 84.95 |
| python | 95.08 |

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
| c      |  75.71 |  92.95 |  81.39 | 27.78 |  7.41 |
| rust   |  82.14 |  90.76 |  90.46 | 31.05 | 10.49 |
| zig    |  79.70 |  95.55 |  80.90 | 33.46 | 12.95 |
| swift  |  84.73 | 113.89 | 100.42 | 29.48 | 11.47 |
| csharp | 104.45 | 106.06 | 125.26 | 38.16 | 11.77 |
| go     |  92.98 | 157.10 | 117.50 | 35.98 | 15.15 |
| java‡  | 116.61 | 157.23 | 150.08 | 53.20 | 28.33 |
| kotlin‡| 111.07 | 170.68 | 194.15 | 54.85 | 31.38 |
| python | 127.35 | 134.79 | 129.18 | 70.18 | 50.32 |

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
| c      |  76.98 |
| rust   |  79.98 |
| zig    |  73.84 |
| swift  |  98.60 |
| csharp | 112.32 |
| go     | 110.60 |
| java‡  | 117.49 |
| kotlin‡| 139.41 |
| python | 137.22 |

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
| c      | 130.67 |  83.43 | 1.57× | xRc2    |
| rust   |  67.47 |  73.82 | 0.91× | xRrsw2  |
| zig    | 119.12 |  79.83 | 1.49× | xRzgsw2 |
| swift  | 159.48 |  88.10 | 1.81× | xRswsw2 |
| csharp | 222.38 | 159.26 | 1.40× | xRcs11  |
| go     | 313.30 | 165.00 | 1.90× | xRgosw2 |
| java‡  | 272.76 | 221.71 | 1.23× | xRjasw2 |
| kotlin‡| 290.31 | 229.52 | 1.26× | xRkosw2 |
| python | 272.39 | 197.24 | 1.38× | xRpysw2 |

<!-- END GENERATED fma-x86 -->


</div>
