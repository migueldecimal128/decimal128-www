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
| c      |  0.84 |  2.05 |  3.54 |  4.07 |  5.69 |  9.54 | 11.45 | 16.81 |  7.85 | 10.12 |
| rust   |  0.81 |  2.14 |  3.45 |  3.77 |  5.17 | 11.38 |  9.41 | 12.81 |  8.45 | 10.03 |
| zig    |  1.31 |  2.25 |  4.25 |  4.89 |  6.21 | 12.00 | 12.28 | 15.49 |  8.44 | 10.93 |
| swift  |  1.26 |  2.65 |  4.24 |  4.24 |  5.57 | 12.72 | 15.47 | 22.13 | 10.82 | 14.19 |
| csharp |  1.26 |  2.89 |  6.32 |  7.01 | 10.68 | 14.70 | 17.25 | 25.33 | 10.38 | 14.75 |
| go     |  1.53 |  5.06 |  6.37 | 11.32 | 11.79 | 19.40 | 28.50 | 37.24 | 17.74 | 25.46 |
| java‡  |  3.84 |  4.89 |  7.61 | 10.31 | 11.46 | 28.55 | 22.60 | 45.44 | 16.01 | 33.74 |
| kotlin‡|  4.32 |  6.14 |  8.69 | 10.86 | 13.50 | 25.76 | 26.86 | 43.03 | 18.53 | 26.91 |
| python | 16.12 | 17.73 | 19.06 | 19.56 | 20.91 | 28.55 | 36.65 | 38.89 | 30.44 | 29.86 |

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
| c      |  3.21 |  2.92 | 18.68 | 26.93 |  9.41 | 12.35 |
| rust   |  3.50 |  3.42 | 13.81 | 21.01 | 10.31 | 12.63 |
| zig    |  3.63 |  3.60 | 17.68 | 20.62 |  9.92 | 11.70 |
| swift  |  5.67 |  5.14 | 21.90 | 29.35 | 11.88 | 17.83 |
| csharp |  5.15 |  4.43 | 22.23 | 32.44 |  8.78 | 13.21 |
| go     |  8.59 |  6.46 | 39.62 | 50.63 | 18.58 | 24.06 |
| java‡  |  6.82 |  6.63 | 22.16 | 41.21 | 20.24 | 30.33 |
| kotlin‡|  8.61 |  7.76 | 24.60 | 35.89 | 29.18 | 28.79 |
| python | 28.54 | 24.58 | 41.91 | 45.46 | 31.56 | 29.23 |

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
| c      |  1.51 |  0.92 |  4.06 |  3.45 |  9.67 |  5.58 | 17.31 | 11.88 | 10.52 |  9.01 |
| rust   |  1.36 |  1.06 |  3.73 |  3.45 | 11.29 |  5.13 | 13.99 |  9.20 |  9.89 |  8.00 |
| zig    |  1.69 |  1.31 |  4.92 |  4.25 | 12.39 |  6.28 | 16.38 | 12.90 | 10.93 |  9.51 |
| swift  |  1.61 |  1.50 |  3.45 |  3.44 | 11.60 |  4.78 | 20.90 | 14.29 | 13.41 | 10.49 |
| csharp |  2.18 |  1.52 |  6.24 |  5.06 | 14.40 |  8.56 | 23.44 | 16.39 | 13.38 |  9.20 |
| go     |  2.92 |  1.62 | 10.74 |  5.58 | 18.57 | 11.50 | 36.54 | 27.66 | 24.01 | 16.81 |
| java‡  |  4.82 |  4.01 |  9.70 |  7.40 | 27.76 | 10.72 | 44.93 | 22.12 | 33.29 | 15.82 |
| kotlin‡|  5.19 |  4.31 | 10.78 |  8.44 | 25.95 | 13.20 | 41.62 | 25.84 | 24.82 | 16.89 |
| python | 16.41 | 16.00 | 19.17 | 18.89 | 28.25 | 21.04 | 38.79 | 36.43 | 29.33 | 30.48 |

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
| c      |  2.63 |  3.62 | 24.74 | 19.39 | 10.42 | 10.27 |
| rust   |  2.62 |  3.60 | 20.01 | 12.65 | 11.38 |  9.72 |
| zig    |  3.54 |  3.96 | 21.17 | 18.80 | 11.89 | 12.07 |
| swift  |  3.77 |  4.44 | 26.04 | 20.28 | 14.97 | 11.32 |
| csharp |  4.97 |  5.14 | 29.51 | 21.33 | 12.25 |  7.77 |
| go     |  5.13 |  8.03 | 50.12 | 39.05 | 22.69 | 17.40 |
| java‡  |  6.33 |  6.86 | 40.23 | 22.29 | 30.07 | 19.05 |
| kotlin‡|  7.14 |  7.80 | 35.21 | 23.21 | 27.60 | 32.29 |
| python | 22.67 | 28.07 | 42.13 | 40.99 | 27.04 | 27.56 |

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
| c      |  1.40 | 20.71 | 25.37 |
| rust   |  1.52 | 13.80 | 25.08 |
| zig    |  1.57 | 18.68 | 22.87 |
| swift  |  2.44 | 16.97 | 24.01 |
| csharp |  2.19 | 16.36 | 45.33 |
| go     |  2.43 | 28.05 | 40.52 |
| java‡  |  5.28 | 30.22 | 43.02 |
| kotlin‡|  5.54 | 32.99 | 42.70 |
| python | 19.33 | 38.81 | 45.56 |

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
| c      | 27.80 |
| rust   | 26.34 |
| zig    | 23.87 |
| swift  | 26.11 |
| csharp | 45.48 |
| go     | 41.46 |
| java‡  | 48.64 |
| kotlin‡| 38.09 |
| python | 45.52 |

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
192÷64 with a 128-bit quotient, §2.4.15), **XD** (20–34, 256÷128 Möller–Granlund), **ET** exact/terminating early-out, **PT**
power-of-ten divisor (`divPow10Divisor` exponent-only fast path, §2.4.9). The compact-divide
cost shows at CD/WD; the ET/PT early-outs are the fastest divides. The C swept **PT** (3.16)
is the coeff-1 (`1E3`) trivial encoding (≡ native ports' `PT1`); the coeff-10ᵏ strip form
runs ~10.5 ns. The **JVM 128-bit divide is competitive-to-ahead** at XD — HotSpot runs
`div XD` faster than the LLVM natives.

**P-gen — arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-pgen -->

| port | div CD | div WD | div XD | div ET | div PT |
|------|-------:|-------:|-------:|-------:|-------:|
| c      | 30.10 | 32.45 | 33.69 |  8.23 |  3.12 |
| rust   | 21.10 | 34.40 | 40.43 |  9.68 |  3.98 |
| zig    | 29.84 | 26.07 | 33.81 | 10.52 |  4.17 |
| swift  | 36.97 | 36.20 | 45.67 |  7.75 |  6.84 |
| csharp | 24.73 | 24.21 | 32.78 |  6.91 |  3.42 |
| go     | 36.28 | 42.58 | 52.23 | 12.42 |  6.64 |
| java‡  | 33.17 | 44.43 | 53.63 | 12.39 | 10.76 |
| kotlin‡| 41.69 | 47.34 | 56.57 | 17.68 | 11.84 |
| python | 56.00 | 58.14 | 62.58 | 25.19 | 18.42 |

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
| c      | 32.78 |
| rust   | 41.96 |
| zig    | 31.99 |
| swift  | 43.12 |
| csharp | 29.62 |
| go     | 53.65 |
| java‡  | 39.89 |
| kotlin‡| 40.01 |
| python | 60.84 |

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
| c      | 39.18 | 39.45 | 0.99× | Rc2    |
| rust   | 21.52 | 37.93 | 0.57× | Rrsw2  |
| zig    | 35.28 | 42.07 | 0.84× | Rzgsw2 |
| swift  | 40.39 | 42.07 | 0.96× | Rswsw2 |
| csharp | 75.31 | 79.37 | 0.95× | Rcs11  |
| go     | 61.48 | 72.25 | 0.85× | Rgosw2 |
| java‡  | 46.36 | 58.30 | 0.80× | Rjasw2 |
| kotlin‡| 54.49 | 65.42 | 0.83× | Rkosw2 |
| python | 78.53 | 79.22 | 0.99× | Rpysw2 |

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
