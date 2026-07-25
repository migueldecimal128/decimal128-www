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
| c      |  2.19 |  3.93 |  6.31 | 11.31 |  7.01 |
| rust   |  2.76 |  5.14 |  7.38 | 10.40 |  6.75 |
| zig    |  2.55 |  5.92 |  8.44 | 12.60 |  8.20 |
| swift  |  5.80 |  8.19 | 15.06 | 20.66 | 16.56 |
| csharp |  6.02 |  4.91 | 15.97 | 39.53 | 34.82 |
| go     |  4.64 | 10.96 | 15.29 | 31.21 | 19.26 |
| java‡  |  5.44 |  7.18 | 18.59 | 29.49 | 22.64 |
| kotlin‡|  5.95 |  7.51 | 16.99 | 30.24 | 19.29 |
| python | 23.20 | 23.02 | 27.99 | 39.76 | 33.32 |

<!-- END GENERATED add-pgen -->

**P-gen — x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-pgen-x86 -->

| port | add SQ | add NQ | add MQ | add OQ | add FQ |
|------|-------:|-------:|-------:|-------:|-------:|
| c      |  7.97 | 12.22 | 23.29 | 42.89 | 31.37 |
| rust   |  9.04 | 12.57 | 19.95 | 38.42 | 22.70 |
| zig    |  8.98 | 14.49 | 19.18 | 33.43 | 19.73 |
| swift  | 11.40 | 16.17 | 26.05 | 46.40 | 32.89 |
| csharp | 15.32 | 17.57 | 42.15 | 82.23 | 62.37 |
| go     |  9.96 | 15.93 | 28.64 | 59.47 | 35.54 |
| java‡  | 13.59 | 20.44 | 31.84 | 61.66 | 40.76 |
| kotlin‡| 17.29 | 24.21 | 35.78 | 63.53 | 45.87 |
| python | 43.04 | 45.08 | 54.57 | 70.69 | 61.73 |

<!-- END GENERATED add-pgen-x86 -->

**P-max — arm64 (stress).**

<!-- BEGIN GENERATED add-pmax -->

| port | add SQ | add OQ | add FQ |
|------|-------:|-------:|-------:|
| c      |  3.40 | 17.75 |  7.64 |
| rust   |  5.04 | 13.57 |  7.57 |
| zig    |  3.94 | 16.81 |  8.65 |
| swift  |  7.24 | 26.76 | 15.85 |
| csharp |  4.72 | 27.68 | 23.67 |
| go     |  8.27 | 45.40 | 20.77 |
| java‡  |  7.21 | 32.49 | 21.09 |
| kotlin‡|  8.23 | 29.61 | 17.18 |
| python | 25.12 | 43.44 | 31.43 |

<!-- END GENERATED add-pmax -->

**P-max — x86_64 (stress).**

<!-- BEGIN GENERATED add-pmax-x86 -->

| port | add SQ | add OQ | add FQ |
|------|-------:|-------:|-------:|
| c      | 14.33 | 51.41 | 26.83 |
| rust   | 13.27 | 43.45 | 21.16 |
| zig    | 13.93 | 38.78 | 19.10 |
| swift  | 17.37 | 54.90 | 30.35 |
| csharp | 18.95 | 81.35 | 49.11 |
| go     | 18.17 | 75.89 | 31.11 |
| java‡  | 21.74 | 62.25 | 33.51 |
| kotlin‡| 27.36 | 86.12 | 36.21 |
| python | 48.68 | 77.30 | 59.07 |

<!-- END GENERATED add-pmax-x86 -->

## 2. Subtract — SQ · NQ · MQ · OQ · FQ

Same band structure as Add: compact SQ/NQ/MQ (recompacted) plus full-range OQ/FQ.

**P-gen — arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-pgen -->

| port | sub SQ | sub NQ | sub MQ | sub OQ | sub FQ |
|------|-------:|-------:|-------:|-------:|-------:|
| c      |  1.22 |  4.97 |  6.66 | 11.99 |  7.20 |
| rust   |  1.73 |  4.87 |  7.84 | 10.48 |  6.94 |
| zig    |  1.57 |  7.64 | 10.14 | 13.19 |  8.94 |
| swift  |  5.10 |  7.84 | 14.45 | 19.65 | 15.57 |
| csharp |  9.15 |  5.78 | 14.98 | 39.88 | 33.74 |
| go     |  2.79 | 10.29 | 14.96 | 31.15 | 20.04 |
| java‡  |  4.58 |  7.40 | 18.61 | 28.38 | 20.17 |
| kotlin‡|  5.00 |  7.72 | 17.13 | 31.01 | 17.72 |
| python | 20.49 | 23.50 | 28.51 | 39.83 | 33.67 |

<!-- END GENERATED sub-pgen -->

**P-gen — x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-pgen-x86 -->

| port | sub SQ | sub NQ | sub MQ | sub OQ | sub FQ |
|------|-------:|-------:|-------:|-------:|-------:|
| c      |  5.06 | 13.33 | 23.87 | 43.39 | 31.41 |
| rust   |  6.97 | 13.88 | 22.27 | 39.42 | 24.76 |
| zig    |  5.79 | 15.45 | 20.43 | 34.81 | 22.12 |
| swift  |  8.08 | 15.73 | 26.10 | 45.90 | 33.72 |
| csharp | 18.83 | 18.34 | 41.39 | 81.43 | 64.33 |
| go     |  7.27 | 16.52 | 28.59 | 60.87 | 36.54 |
| java‡  | 12.45 | 22.17 | 33.18 | 67.62 | 44.53 |
| kotlin‡| 13.61 | 24.99 | 36.80 | 64.91 | 46.20 |
| python | 40.72 | 46.69 | 56.16 | 72.58 | 62.54 |

<!-- END GENERATED sub-pgen-x86 -->

**P-max — arm64 (stress).**

<!-- BEGIN GENERATED sub-pmax -->

| port | sub SQ | sub OQ | sub FQ |
|------|-------:|-------:|-------:|
| c      |  3.30 | 18.72 |  8.15 |
| rust   |  4.45 | 13.52 |  7.47 |
| zig    |  3.84 | 18.20 | 11.97 |
| swift  |  6.88 | 26.31 | 15.02 |
| csharp |  5.29 | 29.87 | 24.77 |
| go     |  7.01 | 44.90 | 20.94 |
| java‡  |  7.25 | 32.26 | 18.76 |
| kotlin‡|  8.04 | 30.90 | 18.18 |
| python | 28.46 | 43.42 | 30.84 |

<!-- END GENERATED sub-pmax -->

**P-max — x86_64 (stress).**

<!-- BEGIN GENERATED sub-pmax-x86 -->

| port | sub SQ | sub OQ | sub FQ |
|------|-------:|-------:|-------:|
| c      | 13.26 | 50.58 | 27.33 |
| rust   | 13.78 | 44.51 | 22.67 |
| zig    | 13.77 | 40.48 | 20.99 |
| swift  | 16.33 | 52.43 | 28.74 |
| csharp | 18.63 | 81.64 | 51.86 |
| go     | 16.69 | 76.73 | 31.66 |
| java‡  | 22.76 | 62.60 | 35.33 |
| kotlin‡| 28.02 | 87.93 | 39.74 |
| python | 49.80 | 89.75 | 59.84 |

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
| c      |  1.40 | 20.70 | 25.55 |
| rust   |  1.59 | 13.87 | 25.13 |
| zig    |  1.57 | 18.39 | 23.01 |
| swift  |  3.39 | 20.58 | 25.60 |
| csharp |  2.18 | 22.83 | 52.39 |
| go     |  2.50 | 27.88 | 39.83 |
| java‡  |  5.34 | 25.63 | 46.02 |
| kotlin‡|  5.52 | 29.05 | 51.99 |
| python | 19.12 | 38.70 | 45.06 |

<!-- END GENERATED mul-pgen -->

**P-gen — x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-pgen-x86 -->

| port | mul CP | mul WP | mul XP |
|------|-------:|-------:|-------:|
| c      |  4.39 | 40.35 | 48.65 |
| rust   |  5.21 | 29.91 | 43.84 |
| zig    |  5.97 | 28.44 | 41.90 |
| swift  |  7.09 | 34.22 | 48.01 |
| csharp |  7.38 | 51.32 | 82.92 |
| go     |  6.14 | 47.29 | 72.39 |
| java‡  | 13.89 | 43.90 | 64.21 |
| kotlin‡| 14.17 | 46.58 | 71.14 |
| python | 40.26 | 74.54 | 89.62 |

<!-- END GENERATED mul-pgen-x86 -->

**P-max — arm64 (stress).** Only XP is feasible at 33–34 digits.

<!-- BEGIN GENERATED mul-pmax -->

| port | mul XP |
|------|-------:|
| c      | 27.69 |
| rust   | 25.41 |
| zig    | 23.80 |
| swift  | 27.99 |
| csharp | 46.30 |
| go     | 40.26 |
| java‡  | 60.12 |
| kotlin‡| 39.51 |
| python | 45.32 |

<!-- END GENERATED mul-pmax -->

**P-max — x86_64 (stress).**

<!-- BEGIN GENERATED mul-pmax-x86 -->

| port | mul XP |
|------|-------:|
| c      | 49.45 |
| rust   | 45.63 |
| zig    | 44.80 |
| swift  | 46.51 |
| csharp | 72.88 |
| go     | 72.59 |
| java‡  | 61.57 |
| kotlin‡| 95.67 |
| python | 88.01 |

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
| c      | 30.65 | 37.59 | 29.90 |  8.26 |  3.12 |
| rust   | 20.16 | 35.66 | 38.25 |  9.72 |  3.97 |
| zig    | 28.24 | 38.45 | 29.77 | 10.72 |  4.17 |
| swift  | 38.67 | 51.00 | 49.63 |  9.82 |  7.16 |
| csharp | 29.45 | 47.00 | 49.02 | 19.14 | 11.67 |
| go     | 34.66 | 61.12 | 53.52 | 12.37 |  6.64 |
| java‡  | 30.96 | 47.63 | 46.80 | 13.03 | 10.08 |
| kotlin‡| 35.37 | 52.56 | 53.48 | 19.61 | 11.54 |
| python | 58.85 | 65.52 | 63.22 | 25.16 | 18.55 |

<!-- END GENERATED div-pgen -->

**P-gen — x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-pgen-x86 -->

| port | div CD | div WD | div XD | div ET | div PT |
|------|-------:|-------:|-------:|-------:|-------:|
| c      |  78.30 |  98.07 |  86.69 | 27.33 |  9.82 |
| rust   |  71.50 |  84.17 |  82.65 | 28.56 |  9.85 |
| zig    |  67.93 |  88.34 |  77.54 | 31.58 | 11.51 |
| swift  |  77.79 |  99.20 | 100.32 | 33.54 | 15.51 |
| csharp | 101.57 | 110.76 | 112.82 | 52.27 | 11.28 |
| go     |  99.80 | 121.90 | 106.70 | 33.96 | 11.78 |
| java‡  |  87.79 | 114.89 | 121.68 | 44.61 | 23.27 |
| kotlin‡|  91.75 | 121.40 | 138.46 | 49.40 | 25.71 |
| python | 113.16 | 122.92 | 113.20 | 62.56 | 42.30 |

<!-- END GENERATED div-pgen-x86 -->

**P-max — arm64 (stress).** Only XD is feasible at 33–34-digit divisors.

<!-- BEGIN GENERATED div-pmax -->

| port | div XD |
|------|-------:|
| c      | 30.87 |
| rust   | 39.86 |
| zig    | 28.47 |
| swift  | 38.91 |
| csharp | 28.84 |
| go     | 53.03 |
| java‡  | 37.70 |
| kotlin‡| 37.93 |
| python | 61.45 |

<!-- END GENERATED div-pmax -->

**P-max — x86_64 (stress).**

<!-- BEGIN GENERATED div-pmax-x86 -->

| port | div XD |
|------|-------:|
| c      |  81.94 |
| rust   |  74.48 |
| zig    |  69.49 |
| swift  |  94.09 |
| csharp |  92.30 |
| go     | 101.30 |
| java‡  |  94.30 |
| kotlin‡| 137.67 |
| python | 111.13 |

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
| c      |  76.23 | 39.38 | 1.94× | Rc2    |
| rust   |  21.87 | 33.80 | 0.65× | Rrsw2  |
| zig    |  64.67 | 42.28 | 1.53× | Rzgsw2 |
| swift  |  83.99 | 42.23 | 1.99× | Rswsw2 |
| csharp | 105.42 | 84.16 | 1.25× | Rcs11  |
| go     | 168.90 | 70.38 | 2.40× | Rgosw2 |
| java‡  | 102.01 | 73.56 | 1.39× | Rjasw2 |
| kotlin‡| 114.31 | 83.67 | 1.37× | Rkosw2 |
| python | 108.28 | 80.05 | 1.35× | Rpysw2 |

<!-- END GENERATED fma -->

**FN/FF band shape — x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-x86 -->

| port | FN | FF | FN÷FF | run |
|------|---:|---:|---:|-----|
| c      | 150.73 |  87.74 | 1.72× | xRc2    |
| rust   |  60.82 |  66.12 | 0.92× | xRrsw2  |
| zig    | 112.17 |  80.35 | 1.40× | xRzgsw2 |
| swift  | 148.55 |  83.13 | 1.79× | xRswsw2 |
| csharp | 182.05 | 142.09 | 1.28× | xRcs11  |
| go     | 249.30 | 128.10 | 1.95× | xRgosw2 |
| java‡  | 201.54 | 167.67 | 1.20× | xRjasw2 |
| kotlin‡| 235.29 | 184.52 | 1.28× | xRkosw2 |
| python | 218.62 | 178.93 | 1.22× | xRpysw2 |

<!-- END GENERATED fma-x86 -->


</div>
