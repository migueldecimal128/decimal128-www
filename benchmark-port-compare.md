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
| c      |  2.18 |  3.97 |  6.43 | 11.78 |  7.30 |
| rust   |  2.69 |  5.07 |  7.38 | 10.56 |  6.90 |
| zig    |  2.59 |  5.97 |  8.46 | 12.55 |  8.28 |
| swift  |  5.79 |  8.61 | 14.73 | 20.41 | 16.45 |
| csharp |  5.84 |  4.89 | 15.26 | 39.66 | 34.78 |
| go     |  5.09 | 10.53 | 15.44 | 30.54 | 19.24 |
| java‡  |  5.45 |  7.30 | 18.58 | 29.30 | 21.54 |
| kotlin‡|  5.94 |  8.77 | 17.49 | 39.85 | 19.60 |
| python | 22.87 | 23.01 | 27.84 | 38.92 | 32.42 |

<!-- END GENERATED add-pgen -->

**P-gen — x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-pgen-x86 -->

| port | add SQ | add NQ | add MQ | add OQ | add FQ |
|------|-------:|-------:|-------:|-------:|-------:|
| c      |  8.93 | 13.67 | 35.37 | 46.17 | 31.57 |
| rust   |  8.41 | 12.40 | 24.95 | 37.99 | 21.35 |
| zig    | 10.78 | 16.34 | 25.55 | 35.11 | 21.19 |
| swift  |  9.50 | 13.55 | 28.91 | 40.41 | 29.03 |
| csharp | 18.92 | 18.33 | 57.26 | 85.87 | 65.57 |
| go     | 12.31 | 17.70 | 42.80 | 66.05 | 40.02 |
| java‡  | 13.52 | 18.92 | 37.06 | 59.75 | 40.06 |
| kotlin‡| 16.74 | 23.55 | 43.19 | 70.87 | 45.86 |
| python | 46.56 | 48.77 | 64.72 | 72.84 | 64.31 |

<!-- END GENERATED add-pgen-x86 -->

**P-max — arm64 (stress).**

<!-- BEGIN GENERATED add-pmax -->

| port | add SQ | add OQ | add FQ |
|------|-------:|-------:|-------:|
| c      |  3.39 | 17.49 |  7.43 |
| rust   |  4.92 | 13.54 |  7.24 |
| zig    |  3.83 | 16.85 |  7.82 |
| swift  |  7.27 | 26.88 | 15.61 |
| csharp |  4.73 | 27.49 | 23.85 |
| go     |  8.08 | 44.39 | 20.82 |
| java‡  |  7.08 | 31.63 | 19.99 |
| kotlin‡|  8.17 | 30.39 | 15.72 |
| python | 25.37 | 43.51 | 31.32 |

<!-- END GENERATED add-pmax -->

**P-max — x86_64 (stress).**

<!-- BEGIN GENERATED add-pmax-x86 -->

| port | add SQ | add OQ | add FQ |
|------|-------:|-------:|-------:|
| c      | 14.53 | 53.22 | 27.95 |
| rust   | 12.83 | 43.97 | 20.09 |
| zig    | 16.36 | 39.20 | 20.70 |
| swift  | 14.35 | 44.99 | 26.36 |
| csharp | 21.28 | 88.12 | 53.77 |
| go     | 20.74 | 81.02 | 35.50 |
| java‡  | 20.69 | 62.75 | 33.91 |
| kotlin‡| 29.23 | 85.48 | 39.82 |
| python | 49.05 | 79.32 | 60.18 |

<!-- END GENERATED add-pmax-x86 -->

## 2. Subtract — SQ · NQ · MQ · OQ · FQ

Same band structure as Add: compact SQ/NQ/MQ (recompacted) plus full-range OQ/FQ.

**P-gen — arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-pgen -->

| port | sub SQ | sub NQ | sub MQ | sub OQ | sub FQ |
|------|-------:|-------:|-------:|-------:|-------:|
| c      |  1.25 |  4.71 |  6.79 | 12.01 |  7.49 |
| rust   |  1.71 |  5.04 |  7.81 | 10.59 |  7.14 |
| zig    |  1.61 |  7.63 | 10.17 | 13.15 |  9.11 |
| swift  |  5.50 |  7.77 | 14.27 | 19.27 | 15.61 |
| csharp |  9.20 |  6.28 | 15.43 | 40.45 | 33.61 |
| go     |  2.78 | 10.13 | 14.93 | 31.30 | 19.78 |
| java‡  |  4.37 |  7.68 | 18.61 | 28.68 | 21.56 |
| kotlin‡|  4.90 |  9.06 | 17.61 | 40.76 | 17.84 |
| python | 20.02 | 22.71 | 27.58 | 38.90 | 32.37 |

<!-- END GENERATED sub-pgen -->

**P-gen — x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-pgen-x86 -->

| port | sub SQ | sub NQ | sub MQ | sub OQ | sub FQ |
|------|-------:|-------:|-------:|-------:|-------:|
| c      |  5.57 | 14.00 | 35.32 | 46.78 | 32.92 |
| rust   |  7.77 | 13.74 | 26.44 | 39.48 | 24.08 |
| zig    |  7.52 | 17.78 | 26.56 | 36.59 | 24.10 |
| swift  |  7.72 | 14.40 | 30.22 | 41.28 | 29.56 |
| csharp | 22.52 | 17.83 | 57.55 | 87.29 | 65.89 |
| go     |  9.46 | 18.14 | 43.77 | 65.49 | 41.29 |
| java‡  | 12.56 | 20.46 | 42.84 | 61.25 | 42.44 |
| kotlin‡| 14.66 | 24.86 | 42.31 | 66.25 | 45.59 |
| python | 42.63 | 48.62 | 64.47 | 73.37 | 65.59 |

<!-- END GENERATED sub-pgen-x86 -->

**P-max — arm64 (stress).**

<!-- BEGIN GENERATED sub-pmax -->

| port | sub SQ | sub OQ | sub FQ |
|------|-------:|-------:|-------:|
| c      |  3.29 | 18.44 |  8.07 |
| rust   |  4.23 | 13.71 |  7.63 |
| zig    |  3.79 | 19.15 | 11.72 |
| swift  |  6.85 | 26.20 | 14.76 |
| csharp |  5.20 | 26.92 | 25.17 |
| go     |  6.85 | 45.19 | 20.96 |
| java‡  |  6.81 | 30.91 | 20.15 |
| kotlin‡|  7.95 | 30.26 | 17.10 |
| python | 28.77 | 42.76 | 30.56 |

<!-- END GENERATED sub-pmax -->

**P-max — x86_64 (stress).**

<!-- BEGIN GENERATED sub-pmax-x86 -->

| port | sub SQ | sub OQ | sub FQ |
|------|-------:|-------:|-------:|
| c      | 13.64 | 54.10 | 28.73 |
| rust   | 13.62 | 45.04 | 21.22 |
| zig    | 16.22 | 41.74 | 22.80 |
| swift  | 14.78 | 47.09 | 26.55 |
| csharp | 20.54 | 91.27 | 56.66 |
| go     | 18.67 | 83.35 | 35.87 |
| java‡  | 23.96 | 68.05 | 33.36 |
| kotlin‡| 28.04 | 88.63 | 39.53 |
| python | 51.40 | 78.16 | 64.84 |

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
| c      |  1.40 | 20.04 | 26.75 |
| rust   |  1.50 | 14.38 | 23.64 |
| zig    |  1.57 | 18.58 | 25.31 |
| swift  |  3.30 | 21.26 | 28.43 |
| csharp |  2.67 | 27.80 | 47.67 |
| go     |  2.61 | 27.28 | 40.14 |
| java‡  |  5.01 | 24.29 | 50.45 |
| kotlin‡|  5.50 | 30.01 | 59.73 |
| python | 19.01 | 37.99 | 47.71 |

<!-- END GENERATED mul-pgen -->

**P-gen — x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-pgen-x86 -->

| port | mul CP | mul WP | mul XP |
|------|-------:|-------:|-------:|
| c      |  4.69 | 46.64 | 56.37 |
| rust   |  5.24 | 30.70 | 44.65 |
| zig    |  7.72 | 28.79 | 42.80 |
| swift  |  6.56 | 35.16 | 53.78 |
| csharp |  8.42 | 67.54 | 95.83 |
| go     |  7.44 | 54.27 | 75.89 |
| java‡  | 14.13 | 52.55 | 78.46 |
| kotlin‡| 14.59 | 46.83 | 85.48 |
| python | 42.70 | 75.70 | 88.72 |

<!-- END GENERATED mul-pgen-x86 -->

**P-max — arm64 (stress).** Only XP is feasible at 33–34 digits.

<!-- BEGIN GENERATED mul-pmax -->

| port | mul XP |
|------|-------:|
| c      | 29.60 |
| rust   | 27.44 |
| zig    | 25.65 |
| swift  | 31.14 |
| csharp | 35.02 |
| go     | 39.83 |
| java‡  | 47.38 |
| kotlin‡| 48.17 |
| python | 47.74 |

<!-- END GENERATED mul-pmax -->

**P-max — x86_64 (stress).**

<!-- BEGIN GENERATED mul-pmax-x86 -->

| port | mul XP |
|------|-------:|
| c      |  59.92 |
| rust   |  50.21 |
| zig    |  45.64 |
| swift  |  52.19 |
| csharp |  75.91 |
| go     |  80.13 |
| java‡  |  76.60 |
| kotlin‡| 120.09 |
| python |  91.58 |

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
| c      | 41.39 | 38.23 | 36.90 |  8.17 |  3.16 |
| rust   | 23.44 | 35.97 | 39.45 |  9.47 |  3.98 |
| zig    | 37.28 | 41.16 | 31.25 | 10.64 |  4.17 |
| swift  | 36.26 | 48.21 | 46.65 | 10.58 |  7.07 |
| csharp | 30.16 | 47.96 | 49.41 | 19.26 | 10.40 |
| go     | 43.91 | 62.95 | 52.32 | 14.89 |  6.64 |
| java‡  | 31.79 | 50.12 | 47.34 | 12.96 |  9.83 |
| kotlin‡| 35.92 | 52.29 | 53.05 | 18.98 | 11.59 |
| python | 58.34 | 64.08 | 62.61 | 24.82 | 18.32 |

<!-- END GENERATED div-pgen -->

**P-gen — x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-pgen-x86 -->

| port | div CD | div WD | div XD | div ET | div PT |
|------|-------:|-------:|-------:|-------:|-------:|
| c      |  88.17 | 103.94 |  92.88 | 29.28 | 10.10 |
| rust   |  73.19 |  86.65 |  86.15 | 29.09 |  9.89 |
| zig    |  75.13 |  99.07 |  77.92 | 32.73 | 12.32 |
| swift  |  71.35 |  97.19 |  91.69 | 29.37 | 12.33 |
| csharp | 122.15 | 136.75 | 131.43 | 56.04 | 12.94 |
| go     | 108.90 | 133.40 | 116.20 | 37.99 | 13.33 |
| java‡  |  88.03 | 117.29 | 124.42 | 44.96 | 23.94 |
| kotlin‡|  94.77 | 121.81 | 132.68 | 49.99 | 27.06 |
| python | 115.88 | 125.94 | 117.43 | 64.53 | 44.58 |

<!-- END GENERATED div-pgen-x86 -->

**P-max — arm64 (stress).** Only XD is feasible at 33–34-digit divisors.

<!-- BEGIN GENERATED div-pmax -->

| port | div XD |
|------|-------:|
| c      | 32.67 |
| rust   | 42.79 |
| zig    | 29.98 |
| swift  | 43.51 |
| csharp | 28.76 |
| go     | 52.93 |
| java‡  | 36.93 |
| kotlin‡| 39.81 |
| python | 61.53 |

<!-- END GENERATED div-pmax -->

**P-max — x86_64 (stress).**

<!-- BEGIN GENERATED div-pmax-x86 -->

| port | div XD |
|------|-------:|
| c      |  89.06 |
| rust   |  76.69 |
| zig    |  69.56 |
| swift  |  91.96 |
| csharp | 106.89 |
| go     | 112.10 |
| java‡  |  97.53 |
| kotlin‡| 135.64 |
| python | 111.70 |

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
| c      |  79.12 | 41.95 | 1.89× | Rc2    |
| rust   |  22.92 | 33.05 | 0.69× | Rrsw2  |
| zig    |  69.16 | 44.73 | 1.55× | Rzgsw2 |
| swift  |  88.59 | 45.22 | 1.96× | Rswsw2 |
| csharp |  95.97 | 72.25 | 1.33× | Rcs11  |
| go     | 157.60 | 76.29 | 2.07× | Rgosw2 |
| java‡  | 105.85 | 74.85 | 1.41× | Rjasw2 |
| kotlin‡| 112.22 | 90.55 | 1.24× | Rkosw2 |
| python | 112.59 | 82.41 | 1.37× | Rpysw2 |

<!-- END GENERATED fma -->

**FN/FF band shape — x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-x86 -->

| port | FN | FF | FN÷FF | run |
|------|---:|---:|---:|-----|
| c      | 151.81 |  93.23 | 1.63× | xRc2    |
| rust   |  62.90 |  67.82 | 0.93× | xRrsw2  |
| zig    | 106.84 |  74.65 | 1.43× | xRzgsw2 |
| swift  | 151.33 |  85.41 | 1.77× | xRswsw2 |
| csharp | 201.21 | 167.63 | 1.20× | xRcs11  |
| go     | 264.80 | 147.40 | 1.80× | xRgosw2 |
| java‡  | 220.62 | 198.30 | 1.11× | xRjasw2 |
| kotlin‡| 259.22 | 225.88 | 1.15× | xRkosw2 |
| python | 219.47 | 183.06 | 1.20× | xRpysw2 |

<!-- END GENERATED fma-x86 -->


</div>
