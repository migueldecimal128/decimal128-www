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
| c      |  8.99 | 13.01 | 24.99 | 46.65 | 32.83 |
| rust   |  9.18 | 12.97 | 20.57 | 38.33 | 24.51 |
| zig    |  9.69 | 14.88 | 19.92 | 34.87 | 20.60 |
| swift  | 10.85 | 16.69 | 26.77 | 47.48 | 34.25 |
| csharp | 16.85 | 16.65 | 42.58 | 84.60 | 65.20 |
| go     | 10.26 | 16.18 | 29.47 | 61.41 | 37.57 |
| java‡  | 13.69 | 20.24 | 34.23 | 66.83 | 59.37 |
| kotlin‡| 17.88 | 25.19 | 35.49 | 65.43 | 45.96 |
| python | 46.78 | 49.80 | 64.67 | 74.68 | 65.32 |

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
| c      | 15.41 | 52.33 | 27.93 |
| rust   | 13.77 | 45.29 | 22.04 |
| zig    | 14.19 | 39.24 | 19.46 |
| swift  | 18.04 | 56.17 | 30.78 |
| csharp | 18.28 | 79.92 | 49.45 |
| go     | 17.92 | 77.64 | 33.13 |
| java‡  | 21.86 | 65.94 | 34.94 |
| kotlin‡| 26.52 | 84.94 | 37.58 |
| python | 49.89 | 78.84 | 61.69 |

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
| c      |  5.38 | 13.42 | 24.60 | 45.68 | 33.35 |
| rust   |  7.22 | 14.40 | 21.94 | 42.39 | 24.35 |
| zig    |  6.02 | 16.04 | 22.06 | 37.20 | 23.34 |
| swift  |  7.90 | 16.62 | 27.16 | 47.02 | 33.65 |
| csharp | 19.32 | 19.00 | 41.83 | 85.34 | 63.64 |
| go     |  7.21 | 16.47 | 29.40 | 63.28 | 37.58 |
| java‡  | 13.14 | 23.39 | 36.06 | 80.64 | 45.21 |
| kotlin‡| 13.58 | 26.78 | 36.46 | 64.82 | 46.98 |
| python | 43.28 | 49.32 | 65.98 | 74.12 | 66.69 |

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
| c      | 13.50 | 56.30 | 28.46 |
| rust   | 14.24 | 46.58 | 23.52 |
| zig    | 14.25 | 43.41 | 21.91 |
| swift  | 17.08 | 53.31 | 29.84 |
| csharp | 21.05 | 80.05 | 51.58 |
| go     | 16.74 | 80.05 | 32.89 |
| java‡  | 24.20 | 65.18 | 34.91 |
| kotlin‡| 27.60 | 87.11 | 39.47 |
| python | 51.58 | 80.17 | 62.33 |

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
| c      |  4.39 | 42.60 | 51.91 |
| rust   |  5.30 | 30.15 | 45.19 |
| zig    |  6.14 | 29.31 | 43.85 |
| swift  |  7.09 | 35.67 | 48.41 |
| csharp |  7.59 | 52.80 | 84.97 |
| go     |  6.23 | 48.97 | 74.16 |
| java‡  | 14.36 | 49.29 | 69.74 |
| kotlin‡| 14.93 | 50.69 | 72.70 |
| python | 42.50 | 76.97 | 90.70 |

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
| c      | 54.81 |
| rust   | 47.11 |
| zig    | 45.76 |
| swift  | 47.60 |
| csharp | 77.71 |
| go     | 77.22 |
| java‡  | 65.06 |
| kotlin‡| 98.17 |
| python | 90.86 |

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
| c      |  91.83 | 103.64 |  96.37 | 29.93 | 10.39 |
| rust   |  76.14 |  88.14 |  85.94 | 29.61 | 10.19 |
| zig    |  72.08 |  91.94 |  77.11 | 33.29 | 11.84 |
| swift  |  77.86 | 100.76 | 104.81 | 37.72 | 16.93 |
| csharp | 104.79 | 116.41 | 115.59 | 52.30 | 11.85 |
| go     | 106.30 | 126.10 | 110.10 | 35.17 | 12.18 |
| java‡  |  92.50 | 119.89 | 129.20 | 49.83 | 24.48 |
| kotlin‡|  96.06 | 122.82 | 132.51 | 51.56 | 25.70 |
| python | 115.87 | 126.30 | 119.02 | 65.54 | 44.33 |

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
| c      |  90.02 |
| rust   |  77.53 |
| zig    |  71.13 |
| swift  |  95.28 |
| csharp |  98.01 |
| go     | 105.60 |
| java‡  |  98.54 |
| kotlin‡| 136.57 |
| python | 119.07 |

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
| c      | 154.12 |  91.07 | 1.69× | xRc2    |
| rust   |  62.65 |  69.00 | 0.91× | xRrsw2  |
| zig    | 116.12 |  83.12 | 1.40× | xRzgsw2 |
| swift  | 151.25 |  85.38 | 1.77× | xRswsw2 |
| csharp | 187.99 | 146.06 | 1.29× | xRcs11  |
| go     | 259.10 | 131.50 | 1.97× | xRgosw2 |
| java‡  | 219.34 | 179.09 | 1.22× | xRjasw2 |
| kotlin‡| 233.51 | 178.64 | 1.31× | xRkosw2 |
| python | 229.88 | 190.33 | 1.21× | xRpysw2 |

<!-- END GENERATED fma-x86 -->


</div>
