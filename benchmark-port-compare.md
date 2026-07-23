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
| c      |  2.20 |  4.23 |  6.57 | 11.50 |  7.29 |
| rust   |  2.83 |  4.89 |  7.40 | 10.47 |  6.90 |
| zig    |  2.59 |  6.01 |  8.30 | 12.52 |  8.13 |
| swift  |  5.82 |  8.14 | 14.79 | 20.41 | 16.37 |
| csharp |  5.97 |  4.92 | 15.76 | 39.40 | 34.98 |
| go     |  4.60 | 10.50 | 14.86 | 30.69 | 19.04 |
| java‡  |  5.47 |  7.45 | 18.28 | 28.44 | 22.31 |
| kotlin‡|  5.91 |  8.88 | 17.16 | 40.72 | 20.55 |
| python | 22.10 | 22.41 | 27.33 | 38.42 | 32.98 |

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
| c      |  3.39 | 18.08 |  7.28 |
| rust   |  4.91 | 13.50 |  7.36 |
| zig    |  4.09 | 16.78 |  7.86 |
| swift  |  7.10 | 26.60 | 15.22 |
| csharp |  4.72 | 28.44 | 23.85 |
| go     |  8.24 | 43.48 | 20.70 |
| java‡  |  7.14 | 31.30 | 22.80 |
| kotlin‡|  8.04 | 29.87 | 16.06 |
| python | 25.28 | 43.46 | 31.60 |

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
| c      |  1.22 |  4.74 |  6.85 | 12.00 |  7.45 |
| rust   |  1.74 |  5.05 |  7.58 | 10.50 |  6.97 |
| zig    |  1.58 |  7.56 | 10.23 | 13.17 |  8.98 |
| swift  |  5.48 |  7.78 | 14.38 | 19.58 | 15.62 |
| csharp |  9.06 |  5.83 | 14.81 | 39.87 | 32.31 |
| go     |  2.73 | 10.06 | 14.98 | 31.19 | 19.53 |
| java‡  |  4.39 |  7.22 | 18.40 | 29.75 | 19.59 |
| kotlin‡|  4.89 |  9.29 | 17.70 | 41.65 | 19.16 |
| python | 20.30 | 22.73 | 27.36 | 38.89 | 32.94 |

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
| c      |  3.30 | 18.30 |  8.86 |
| rust   |  4.07 | 13.61 |  6.95 |
| zig    |  3.77 | 18.73 | 10.89 |
| swift  |  6.86 | 26.06 | 14.88 |
| csharp |  5.29 | 27.07 | 24.99 |
| go     |  6.53 | 44.31 | 20.34 |
| java‡  |  6.87 | 31.84 | 23.56 |
| kotlin‡|  7.91 | 29.98 | 17.21 |
| python | 29.50 | 42.87 | 30.04 |

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
| c      |  1.43 | 19.65 | 24.00 |
| rust   |  1.52 | 13.99 | 25.13 |
| zig    |  1.58 | 18.40 | 23.00 |
| swift  |  3.38 | 20.44 | 25.58 |
| csharp |  2.24 | 22.03 | 50.99 |
| go     |  2.60 | 27.76 | 38.68 |
| java‡  |  5.16 | 26.17 | 43.50 |
| kotlin‡|  5.61 | 31.33 | 49.75 |
| python | 18.93 | 38.60 | 44.61 |

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
| c      | 27.40 |
| rust   | 25.06 |
| zig    | 23.76 |
| swift  | 28.00 |
| csharp | 47.03 |
| go     | 39.39 |
| java‡  | 39.88 |
| kotlin‡| 37.96 |
| python | 45.60 |

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
| c      | 41.32 | 39.32 | 32.97 |  8.09 |  3.15 |
| rust   | 25.34 | 32.60 | 36.51 |  9.52 |  3.98 |
| zig    | 37.26 | 40.71 | 32.49 | 10.67 |  4.17 |
| swift  | 37.96 | 50.71 | 50.45 | 10.58 |  7.15 |
| csharp | 29.33 | 48.07 | 48.34 | 19.17 | 10.98 |
| go     | 43.58 | 63.62 | 51.51 | 14.36 |  6.63 |
| java‡  | 31.23 | 47.21 | 47.35 | 13.01 |  9.87 |
| kotlin‡| 36.47 | 47.37 | 51.94 | 19.12 | 11.86 |
| python | 59.36 | 65.13 | 62.48 | 24.41 | 18.34 |

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
| c      | 33.72 |
| rust   | 38.05 |
| zig    | 33.39 |
| swift  | 40.50 |
| csharp | 28.62 |
| go     | 51.75 |
| java‡  | 37.01 |
| kotlin‡| 40.20 |
| python | 61.63 |

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
| c      |  75.77 | 39.42 | 1.92× | Rc2    |
| rust   |  21.90 | 33.92 | 0.65× | Rrsw2  |
| zig    |  67.72 | 42.28 | 1.60× | Rzgsw2 |
| swift  |  83.92 | 42.30 | 1.98× | Rswsw2 |
| csharp | 107.51 | 83.93 | 1.28× | Rcs11  |
| go     | 168.30 | 72.20 | 2.33× | Rgosw2 |
| java‡  |  99.27 | 68.97 | 1.44× | Rjasw2 |
| kotlin‡| 108.72 | 82.63 | 1.32× | Rkosw2 |
| python | 108.32 | 79.75 | 1.36× | Rpysw2 |

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
