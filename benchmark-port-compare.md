---
layout: default
permalink: /benchmark/port-compare.html
title: "Port-Comparison Benchmark Results — Decimal128"
description: "Cross-port decimal128 band-shape matrices — each port's own ns/op per operation band on identical operands, with no comparison against alternatives."
heading: "Port-Comparison Benchmark Results"
---

<div class="whitepaper" markdown="1">

<p class="whitepaper-meta">Split out of `benchmark-op-results.md` 2026-07-17. Living document — as-measured results.</p>

This document is the **cross-port d128 band-shape** tier: compact matrices of decimal128's
own ns/op per operation band, every port on the **same** swept operands. It **does not
compare against alternatives** — no libbid / idiom-peer / ratio columns. Those live in the
companion reports:

- **`benchmark-port-compare.md`** (this doc) — d128-only band matrices, port × band.
  "How does each port's kernel shape up across the input bands, fast path vs slow path?"
- **`benchmark-op-results.md`** — the same bands **vs alternatives** (libbid / decQuad /
  mpdecimal / idiom peers), with explicit ratios. "How fast is d128 against the field?"
- **`benchmark-finmix.md`** — the realistic financial operation mix (P-fin), vs peers.

**Method.** Swept 4096-input average per band (bare `thru`; ns/op = `Time/4096` over the
shared `decimal128-resources/swept/<profile>/` corpus, byte-identical operands every port).
arm64 (M3 Pro) and x86_64 (Intel i9-9880H); JVM verify-off, `‡` = escape-forced
alloc-inclusive. `P-gen` = general digit-length-uniform widths; `P-max` = 34-digit stress.
Band/category codes (`SQ`/`NQ`/`MQ`/`OQ`/`FQ`, `CP`/`WP`/`XP`, `CD`/`WD`/`XD`/`ET`/`PT`,
`FN`/`FF`) are defined in `BenchmarkMatrix.md` §3 (authoritative) and glossed in
`benchmark-op-results.md`'s Key.

## 1. Add — SQ · NQ · MQ · OQ · FQ

SQ/NQ/MQ are the **compact** regime (qExp ∈ [0,−8], result < 10²⁸) — recompacted so the
28-digit peers can run on the same operands in the relational report; OQ/FQ keep the full
range. **MQ (Δ>4, the `qAlignDelta>4` no-round path) is the alignment-slope column** — 2–3×
the pack-direct NQ, the one add/sub band where d128's alignment cost shows.

**P-gen — arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-pgen -->

| port | add SQ | add NQ | add MQ | add OQ | add FQ |
|------|-------:|-------:|-------:|-------:|-------:|
| c      |  2.16 |  3.96 | 10.80 | 12.07 |  7.07 |
| rust   |  2.73 |  4.97 | 13.87 | 10.88 |  6.65 |
| zig    |  2.54 |  6.07 | 12.18 | 12.83 |  7.58 |
| swift  |  4.15 |  5.99 | 15.93 | 17.68 | 12.84 |
| csharp |  6.06 |  5.04 | 19.04 | 36.36 | 30.60 |
| go     |  5.07 | 10.38 | 21.83 | 32.50 | 19.99 |
| java‡  |  5.47 |  7.32 | 22.11 | 30.33 | 22.14 |
| kotlin‡|  6.02 |  7.43 | 21.91 | 38.01 | 18.26 |
| python | 24.02 | 22.34 | 29.81 | 39.74 | 32.73 |

<!-- END GENERATED add-pgen -->

**P-gen — x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-pgen-x86 -->

| port | add SQ | add NQ | add MQ | add OQ | add FQ |
|------|-------:|-------:|-------:|-------:|-------:|
| c      |  8.93 | 13.67 | 35.37 | 46.17 | 31.57 |
| rust   |  8.41 | 12.40 | 24.95 | 37.99 | 21.35 |
| zig    | 10.78 | 16.34 | 25.55 | 35.11 | 21.19 |
| swift  |  9.50 | 13.55 | 28.91 | 40.41 | 29.03 |
| csharp | 13.59 | 18.16 | 50.25 | 71.58 | 42.58 |
| go     | 12.31 | 17.70 | 42.80 | 66.05 | 40.02 |
| java‡  | 13.52 | 18.92 | 37.06 | 59.75 | 40.06 |
| kotlin‡| 16.74 | 23.55 | 43.19 | 70.87 | 45.86 |
| python | 46.56 | 48.77 | 64.72 | 72.84 | 64.31 |

<!-- END GENERATED add-pgen-x86 -->

**P-max — arm64 (stress).**

<!-- BEGIN GENERATED add-pmax -->

| port | add SQ | add OQ | add FQ |
|------|-------:|-------:|-------:|
| c      |  3.34 | 17.61 |  6.81 |
| rust   |  5.27 | 13.45 |  7.87 |
| zig    |  3.85 | 16.86 |  7.66 |
| swift  |  6.02 | 22.79 | 12.87 |
| csharp |  4.72 | 28.58 | 25.17 |
| go     | 11.02 | 42.83 | 20.67 |
| java‡  |  7.08 | 31.06 | 23.20 |
| kotlin‡|  8.10 | 29.87 | 16.93 |
| python | 27.17 | 43.17 | 30.49 |

<!-- END GENERATED add-pmax -->

**P-max — x86_64 (stress).**

<!-- BEGIN GENERATED add-pmax-x86 -->

| port | add SQ | add OQ | add FQ |
|------|-------:|-------:|-------:|
| c      | 14.53 | 53.22 | 27.95 |
| rust   | 12.83 | 43.97 | 20.09 |
| zig    | 16.36 | 39.20 | 20.70 |
| swift  | 14.35 | 44.99 | 26.36 |
| csharp | 21.58 | 93.22 | 40.16 |
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
| c      |  1.24 |  4.79 | 11.35 | 12.68 |  7.14 |
| rust   |  1.75 |  5.14 | 14.49 | 10.97 |  6.66 |
| zig    |  1.56 |  7.64 | 13.51 | 14.44 |  9.31 |
| swift  |  2.58 |  5.61 | 15.39 | 17.42 | 12.97 |
| csharp |  9.34 |  5.82 | 18.80 | 35.73 | 28.91 |
| go     |  2.69 | 10.09 | 22.03 | 32.21 | 19.60 |
| java‡  |  4.41 |  7.15 | 22.10 | 29.43 | 20.77 |
| kotlin‡|  5.01 |  7.74 | 22.09 | 39.16 | 18.04 |
| python | 21.12 | 22.47 | 29.81 | 39.48 | 32.58 |

<!-- END GENERATED sub-pgen -->

**P-gen — x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-pgen-x86 -->

| port | sub SQ | sub NQ | sub MQ | sub OQ | sub FQ |
|------|-------:|-------:|-------:|-------:|-------:|
| c      |  5.57 | 14.00 | 35.32 | 46.78 | 32.92 |
| rust   |  7.77 | 13.74 | 26.44 | 39.48 | 24.08 |
| zig    |  7.52 | 17.78 | 26.56 | 36.59 | 24.10 |
| swift  |  7.72 | 14.40 | 30.22 | 41.28 | 29.56 |
| csharp | 10.77 | 22.60 | 49.51 | 70.90 | 41.26 |
| go     |  9.46 | 18.14 | 43.77 | 65.49 | 41.29 |
| java‡  | 12.56 | 20.46 | 42.84 | 61.25 | 42.44 |
| kotlin‡| 14.66 | 24.86 | 42.31 | 66.25 | 45.59 |
| python | 42.63 | 48.62 | 64.47 | 73.37 | 65.59 |

<!-- END GENERATED sub-pgen-x86 -->

**P-max — arm64 (stress).**

<!-- BEGIN GENERATED sub-pmax -->

| port | sub SQ | sub OQ | sub FQ |
|------|-------:|-------:|-------:|
| c      |  3.26 | 18.31 |  8.92 |
| rust   |  4.22 | 13.36 |  7.85 |
| zig    |  3.75 | 19.00 | 10.28 |
| swift  |  4.36 | 23.20 | 12.46 |
| csharp |  5.25 | 29.36 | 26.52 |
| go     |  6.50 | 44.44 | 20.02 |
| java‡  |  6.95 | 30.98 | 23.77 |
| kotlin‡|  7.92 | 30.02 | 18.15 |
| python | 28.53 | 43.43 | 30.21 |

<!-- END GENERATED sub-pmax -->

**P-max — x86_64 (stress).**

<!-- BEGIN GENERATED sub-pmax-x86 -->

| port | sub SQ | sub OQ | sub FQ |
|------|-------:|-------:|-------:|
| c      | 13.64 | 54.10 | 28.73 |
| rust   | 13.62 | 45.04 | 21.22 |
| zig    | 16.22 | 41.74 | 22.80 |
| swift  | 14.78 | 47.09 | 26.55 |
| csharp | 24.73 | 92.58 | 38.64 |
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
| c      |  1.39 | 20.69 | 29.20 |
| rust   |  1.56 | 14.17 | 25.22 |
| zig    |  1.58 | 18.57 | 25.44 |
| swift  |  4.06 | 20.99 | 27.65 |
| csharp |  2.54 | 33.22 | 52.65 |
| go     |  2.50 | 27.04 | 37.51 |
| java‡  |  4.95 | 26.03 | 52.40 |
| kotlin‡|  5.32 | 31.21 | 61.49 |
| python | 19.12 | 38.31 | 47.89 |

<!-- END GENERATED mul-pgen -->

**P-gen — x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-pgen-x86 -->

| port | mul CP | mul WP | mul XP |
|------|-------:|-------:|-------:|
| c      |  4.69 | 46.64 | 56.37 |
| rust   |  5.24 | 30.70 | 44.65 |
| zig    |  7.72 | 28.79 | 42.80 |
| swift  |  6.56 | 35.16 | 53.78 |
| csharp |  9.59 | 50.34 | 77.47 |
| go     |  7.44 | 54.27 | 75.89 |
| java‡  | 14.13 | 52.55 | 78.46 |
| kotlin‡| 14.59 | 46.83 | 85.48 |
| python | 42.70 | 75.70 | 88.72 |

<!-- END GENERATED mul-pgen-x86 -->

**P-max — arm64 (stress).** Only XP is feasible at 33–34 digits.

<!-- BEGIN GENERATED mul-pmax -->

| port | mul XP |
|------|-------:|
| c      | 30.10 |
| rust   | 29.26 |
| zig    | 25.52 |
| swift  | 30.21 |
| csharp | 35.14 |
| go     | 41.06 |
| java‡  | 55.08 |
| kotlin‡| 51.60 |
| python | 47.60 |

<!-- END GENERATED mul-pmax -->

**P-max — x86_64 (stress).**

<!-- BEGIN GENERATED mul-pmax-x86 -->

| port | mul XP |
|------|-------:|
| c      |  59.92 |
| rust   |  50.21 |
| zig    |  45.64 |
| swift  |  52.19 |
| csharp |  87.60 |
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
| c      | 42.13 | 38.54 | 33.72 |  8.40 |  3.15 |
| rust   | 26.16 | 35.28 | 39.49 |  9.49 |  3.98 |
| zig    | 39.04 | 42.29 | 34.46 | 10.69 |  4.23 |
| swift  | 33.87 | 44.84 | 44.18 |  8.53 |  7.63 |
| csharp | 34.65 | 56.44 | 60.06 | 18.92 |  9.36 |
| go     | 46.91 | 59.31 | 60.13 | 14.92 |  6.56 |
| java‡  | 30.35 | 51.05 | 48.29 | 12.73 |  9.78 |
| kotlin‡| 34.96 | 50.90 | 52.77 | 19.44 | 11.48 |
| python | 58.75 | 65.11 | 63.27 | 24.44 | 18.25 |

<!-- END GENERATED div-pgen -->

**P-gen — x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-pgen-x86 -->

| port | div CD | div WD | div XD | div ET | div PT |
|------|-------:|-------:|-------:|-------:|-------:|
| c      |  88.17 | 103.94 |  92.88 | 29.28 | 10.10 |
| rust   |  73.19 |  86.65 |  86.15 | 29.09 |  9.89 |
| zig    |  75.13 |  99.07 |  77.92 | 32.73 | 12.32 |
| swift  |  71.35 |  97.19 |  91.69 | 29.37 | 12.33 |
| csharp |  96.82 | 113.00 | 121.06 | 44.04 | 12.21 |
| go     | 108.90 | 133.40 | 116.20 | 37.99 | 13.33 |
| java‡  |  88.03 | 117.29 | 124.42 | 44.96 | 23.94 |
| kotlin‡|  94.77 | 121.81 | 132.68 | 49.99 | 27.06 |
| python | 115.88 | 125.94 | 117.43 | 64.53 | 44.58 |

<!-- END GENERATED div-pgen-x86 -->

**P-max — arm64 (stress).** Only XD is feasible at 33–34-digit divisors.

<!-- BEGIN GENERATED div-pmax -->

| port | div XD |
|------|-------:|
| c      | 32.31 |
| rust   | 41.87 |
| zig    | 31.25 |
| swift  | 39.80 |
| csharp | 28.73 |
| go     | 53.62 |
| java‡  | 39.81 |
| kotlin‡| 39.60 |
| python | 62.11 |

<!-- END GENERATED div-pmax -->

**P-max — x86_64 (stress).**

<!-- BEGIN GENERATED div-pmax-x86 -->

| port | div XD |
|------|-------:|
| c      |  89.06 |
| rust   |  76.69 |
| zig    |  69.56 |
| swift  |  91.96 |
| csharp | 128.42 |
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
| c      |  79.12 | 42.22 | 1.87× | Rc2    |
| rust   |  23.03 | 33.57 | 0.69× | Rrsw2  |
| zig    |  66.93 | 44.61 | 1.50× | Rzgsw2 |
| swift  |  85.36 | 44.53 | 1.92× | Rswsw2 |
| csharp |  93.71 | 71.25 | 1.32× | Rcs11  |
| go     | 157.70 | 76.56 | 2.06× | Rgosw2 |
| java‡  | 104.26 | 75.19 | 1.39× | Rjasw2 |
| kotlin‡| 111.02 | 88.17 | 1.26× | Rkosw2 |
| python | 112.13 | 81.48 | 1.38× | Rpysw2 |

<!-- END GENERATED fma -->

**FN/FF band shape — x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-x86 -->

| port | FN | FF | FN÷FF | run |
|------|---:|---:|---:|-----|
| c      | 151.81 |  93.23 | 1.63× | xRc2    |
| rust   |  62.90 |  67.82 | 0.93× | xRrsw2  |
| zig    | 106.84 |  74.65 | 1.43× | xRzgsw2 |
| swift  | 151.33 |  85.41 | 1.77× | xRswsw2 |
| csharp | 195.58 | 138.44 | 1.41× | xRcssw2 |
| go     | 264.80 | 147.40 | 1.80× | xRgosw2 |
| java‡  | 220.62 | 198.30 | 1.11× | xRjasw2 |
| kotlin‡| 259.22 | 225.88 | 1.15× | xRkosw2 |
| python | 219.47 | 183.06 | 1.20× | xRpysw2 |

<!-- END GENERATED fma-x86 -->


</div>
