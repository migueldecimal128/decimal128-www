---
layout: default
permalink: /benchmark/vs-c.html
title: "C Benchmark Results — Decimal128"
description: "decimal128 in C, measured against the alternatives available to it — a realistic financial mix (P-fin) plus per-operation band characterization, with explicit ratios."
heading: "C Benchmark Results"
---

<div class="whitepaper" markdown="1">

<p class="whitepaper-meta">Living document — as-measured results. Category codes, profiles, modes &amp; method: <a href="key.html">Benchmark Key</a>.</p>

This is the **C** view of decimal128 **as-measured**, band by band, with explicit ratios. It opens with the realistic financial-mix (**P-fin**) headline, then the per-operation band characterization (**P-gen**) and FMA. In C, d128 is measured against the Intel **libbid** universal reference plus IBM **decQuad** (DPD) and **libmpdecimal**. It is **data only** — the categories, magnitude profiles, units, and methodology are defined in the [Benchmark Key](key.html) (and, authoritatively, `BenchmarkMatrix.md`). The cross-port d128 band-shape matrices (all ports, no alternatives) live in [Port-Comparison Benchmark Results](port-compare.html); the full index of per-language pages is on the [Benchmarks](/benchmarks.html) hub.

## Summary — Ratio Range by Operation

A quick-glance rollup before the detailed tables below: the min–max `ratio = alt / ours` (&gt; 1× ⇒ d128 faster) for each operation, pooled across both architectures (arm64 + x86_64) and all three reference libraries (libbid, decQuad, mpdecimal), split by profile.

| Operation | P-fin range | P-gen range | FMA range |
|---|---|---|---|
| Add | 3.10× – 8.01× | 0.79× – 9.65× | — |
| Subtract | 4.21× – 11.42× | 0.83× – 18.72× | — |
| Multiply | 0.95× – 22.30× | 0.95× – 17.44× | — |
| Divide | 0.81× – 14.52× | 0.81× – 16.24× | — |
| FMA | — | — | 0.77× – 3.64× |

## FinMix — realistic financial mix (P-fin)

The headline: one realistic 64-bit financial operation mix — a `MIX` add/sub stream, mul `CP`/`WP`, div `CD`/`WD`/`ET`/`PT` — `ratio = alt / ours` (&gt; 1 ⇒ d128 faster). This is the profile closest to real financial code.

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED pfin-rel-c -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | add | MIX | P-fin | arm64 | thru | 2.81 | libbid | 10.35 | **3.68×** | Rc2 |  |
| c | sub | MIX | P-fin | arm64 | thru | 2.04 | libbid | 10.65 | **5.22×** | Rc2 |  |
| c | mul | CP | P-fin | arm64 | thru | 1.21 | libbid | 23.69 | **19.58×** | Rc2 |  |
| c | mul | WP | P-fin | arm64 | thru | 20.60 | libbid | 34.45 | **1.67×** | Rc2 |  |
| c | div | CD | P-fin | arm64 | thru | 43.22 | libbid | 35.06 | **0.81×** | Rc2 |  |
| c | div | WD | P-fin | arm64 | thru | 39.24 | libbid | 39.18 | **1.00×** | Rc2 |  |
| c | div | ET | P-fin | arm64 | thru | 6.49 | libbid | 6.11 | **0.94×** | Rc2 |  |
| c | div | PT | P-fin | arm64 | thru | 3.16 | libbid | 6.10 | **1.93×** | Rc2 |  |
| c | add | MIX | P-fin | arm64 | thru | 2.81 | decQuad | 22.51 | **8.01×** | Rc2 |  |
| c | sub | MIX | P-fin | arm64 | thru | 2.04 | decQuad | 23.29 | **11.42×** | Rc2 |  |
| c | mul | CP | P-fin | arm64 | thru | 1.21 | decQuad | 21.41 | **17.69×** | Rc2 |  |
| c | mul | WP | P-fin | arm64 | thru | 20.60 | decQuad | 25.54 | **1.24×** | Rc2 |  |
| c | div | CD | P-fin | arm64 | thru | 43.22 | decQuad | 71.42 | **1.65×** | Rc2 |  |
| c | div | WD | P-fin | arm64 | thru | 39.24 | decQuad | 117.29 | **2.99×** | Rc2 |  |
| c | div | ET | P-fin | arm64 | thru | 6.49 | decQuad | 41.51 | **6.40×** | Rc2 |  |
| c | div | PT | P-fin | arm64 | thru | 3.16 | decQuad | 39.27 | **12.43×** | Rc2 |  |
| c | add | MIX | P-fin | arm64 | thru | 2.81 | mpdecimal | 13.46 | **4.79×** | Rc2 |  |
| c | sub | MIX | P-fin | arm64 | thru | 2.04 | mpdecimal | 14.99 | **7.35×** | Rc2 |  |
| c | mul | CP | P-fin | arm64 | thru | 1.21 | mpdecimal | 9.91 | **8.19×** | Rc2 |  |
| c | mul | WP | P-fin | arm64 | thru | 20.60 | mpdecimal | 29.78 | **1.45×** | Rc2 |  |
| c | div | CD | P-fin | arm64 | thru | 43.22 | mpdecimal | 60.03 | **1.39×** | Rc2 |  |
| c | div | WD | P-fin | arm64 | thru | 39.24 | mpdecimal | 87.72 | **2.24×** | Rc2 |  |
| c | div | ET | P-fin | arm64 | thru | 6.49 | mpdecimal | 56.09 | **8.64×** | Rc2 |  |
| c | div | PT | P-fin | arm64 | thru | 3.16 | mpdecimal | 45.89 | **14.52×** | Rc2 |  |

<!-- END GENERATED pfin-rel-c -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-c-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | add | MIX | P-fin | x86_64 | thru | 10.01 | libbid | 31.03 | **3.10×** | xRc2 |  |
| c | sub | MIX | P-fin | x86_64 | thru | 8.42 | libbid | 35.45 | **4.21×** | xRc2 |  |
| c | mul | CP | P-fin | x86_64 | thru | 2.51 | libbid | 47.15 | **18.78×** | xRc2 |  |
| c | mul | WP | P-fin | x86_64 | thru | 46.77 | libbid | 60.29 | **1.29×** | xRc2 |  |
| c | div | CD | P-fin | x86_64 | thru | 87.44 | libbid | 77.69 | **0.89×** | xRc2 |  |
| c | div | WD | P-fin | x86_64 | thru | 102.32 | libbid | 82.71 | **0.81×** | xRc2 |  |
| c | div | ET | P-fin | x86_64 | thru | 18.22 | libbid | 20.15 | **1.11×** | xRc2 |  |
| c | div | PT | P-fin | x86_64 | thru | 10.21 | libbid | 19.71 | **1.93×** | xRc2 |  |
| c | add | MIX | P-fin | x86_64 | thru | 10.01 | decQuad | 59.43 | **5.94×** | xRc2 |  |
| c | sub | MIX | P-fin | x86_64 | thru | 8.42 | decQuad | 60.69 | **7.21×** | xRc2 |  |
| c | mul | CP | P-fin | x86_64 | thru | 2.51 | decQuad | 55.98 | **22.30×** | xRc2 |  |
| c | mul | WP | P-fin | x86_64 | thru | 46.77 | decQuad | 69.22 | **1.48×** | xRc2 |  |
| c | div | CD | P-fin | x86_64 | thru | 87.44 | decQuad | 137.65 | **1.57×** | xRc2 |  |
| c | div | WD | P-fin | x86_64 | thru | 102.32 | decQuad | 240.81 | **2.35×** | xRc2 |  |
| c | div | ET | P-fin | x86_64 | thru | 18.22 | decQuad | 75.78 | **4.16×** | xRc2 |  |
| c | div | PT | P-fin | x86_64 | thru | 10.21 | decQuad | 67.99 | **6.66×** | xRc2 |  |
| c | add | MIX | P-fin | x86_64 | thru | 10.01 | mpdecimal | 38.13 | **3.81×** | xRc2 |  |
| c | sub | MIX | P-fin | x86_64 | thru | 8.42 | mpdecimal | 38.04 | **4.52×** | xRc2 |  |
| c | mul | CP | P-fin | x86_64 | thru | 2.51 | mpdecimal | 32.81 | **13.07×** | xRc2 |  |
| c | mul | WP | P-fin | x86_64 | thru | 46.77 | mpdecimal | 44.24 | **0.95×** | xRc2 |  |
| c | div | CD | P-fin | x86_64 | thru | 87.44 | mpdecimal | 158.24 | **1.81×** | xRc2 |  |
| c | div | WD | P-fin | x86_64 | thru | 102.32 | mpdecimal | 280.40 | **2.74×** | xRc2 |  |
| c | div | ET | P-fin | x86_64 | thru | 18.22 | mpdecimal | 142.13 | **7.80×** | xRc2 |  |
| c | div | PT | P-fin | x86_64 | thru | 10.21 | mpdecimal | 87.97 | **8.62×** | xRc2 |  |

<!-- END GENERATED pfin-rel-c-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-c -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | add | SQ | P-gen | arm64 | thru | 2.16 | libbid | 7.79 | **3.61×** | Rc2 |  |
| c | add | NQ | P-gen | arm64 | thru | 3.96 | libbid | 8.46 | **2.14×** | Rc2 |  |
| c | add | MQ | P-gen | arm64 | thru | 10.80 | libbid | 8.57 | **0.79×** | Rc2 |  |
| c | add | OQ | P-gen | arm64 | thru | 12.07 | libbid | 13.87 | **1.15×** | Rc2 |  |
| c | add | FQ | P-gen | arm64 | thru | 7.07 | libbid | 9.37 | **1.33×** | Rc2 |  |
| c | add | SQ | P-gen | arm64 | thru | 2.16 | decQuad | 20.84 | **9.65×** | Rc2 |  |
| c | add | NQ | P-gen | arm64 | thru | 3.96 | decQuad | 30.10 | **7.60×** | Rc2 |  |
| c | add | MQ | P-gen | arm64 | thru | 10.80 | decQuad | 28.68 | **2.66×** | Rc2 |  |
| c | add | OQ | P-gen | arm64 | thru | 12.07 | decQuad | 35.77 | **2.96×** | Rc2 |  |
| c | add | FQ | P-gen | arm64 | thru | 7.07 | decQuad | 26.44 | **3.74×** | Rc2 |  |
| c | add | SQ | P-gen | arm64 | thru | 2.16 | mpdecimal | 12.41 | **5.75×** | Rc2 |  |
| c | add | NQ | P-gen | arm64 | thru | 3.96 | mpdecimal | 26.98 | **6.81×** | Rc2 |  |
| c | add | MQ | P-gen | arm64 | thru | 10.80 | mpdecimal | 26.02 | **2.41×** | Rc2 |  |
| c | add | OQ | P-gen | arm64 | thru | 12.07 | mpdecimal | 47.59 | **3.94×** | Rc2 |  |
| c | add | FQ | P-gen | arm64 | thru | 7.07 | mpdecimal | 40.65 | **5.75×** | Rc2 |  |

<!-- END GENERATED add-rel-c -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-c-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | add | SQ | P-gen | x86_64 | thru | 8.93 | libbid | 30.20 | **3.38×** | xRc2 |  |
| c | add | NQ | P-gen | x86_64 | thru | 13.67 | libbid | 33.46 | **2.45×** | xRc2 |  |
| c | add | MQ | P-gen | x86_64 | thru | 35.37 | libbid | 31.52 | **0.89×** | xRc2 |  |
| c | add | OQ | P-gen | x86_64 | thru | 46.17 | libbid | 51.83 | **1.12×** | xRc2 |  |
| c | add | FQ | P-gen | x86_64 | thru | 31.57 | libbid | 32.09 | **1.02×** | xRc2 |  |
| c | add | SQ | P-gen | x86_64 | thru | 8.93 | decQuad | 51.90 | **5.81×** | xRc2 |  |
| c | add | NQ | P-gen | x86_64 | thru | 13.67 | decQuad | 80.55 | **5.89×** | xRc2 |  |
| c | add | MQ | P-gen | x86_64 | thru | 35.37 | decQuad | 77.86 | **2.20×** | xRc2 |  |
| c | add | OQ | P-gen | x86_64 | thru | 46.17 | decQuad | 88.50 | **1.92×** | xRc2 |  |
| c | add | FQ | P-gen | x86_64 | thru | 31.57 | decQuad | 71.35 | **2.26×** | xRc2 |  |
| c | add | SQ | P-gen | x86_64 | thru | 8.93 | mpdecimal | 36.59 | **4.10×** | xRc2 |  |
| c | add | NQ | P-gen | x86_64 | thru | 13.67 | mpdecimal | 56.71 | **4.15×** | xRc2 |  |
| c | add | MQ | P-gen | x86_64 | thru | 35.37 | mpdecimal | 56.80 | **1.61×** | xRc2 |  |
| c | add | OQ | P-gen | x86_64 | thru | 46.17 | mpdecimal | 134.00 | **2.90×** | xRc2 |  |
| c | add | FQ | P-gen | x86_64 | thru | 31.57 | mpdecimal | 85.49 | **2.71×** | xRc2 |  |

<!-- END GENERATED add-rel-c-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-c -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | sub | SQ | P-gen | arm64 | thru | 1.24 | libbid | 9.17 | **7.40×** | Rc2 |  |
| c | sub | NQ | P-gen | arm64 | thru | 4.79 | libbid | 9.60 | **2.00×** | Rc2 |  |
| c | sub | MQ | P-gen | arm64 | thru | 11.35 | libbid | 9.40 | **0.83×** | Rc2 |  |
| c | sub | OQ | P-gen | arm64 | thru | 12.68 | libbid | 14.83 | **1.17×** | Rc2 |  |
| c | sub | FQ | P-gen | arm64 | thru | 7.14 | libbid | 9.37 | **1.31×** | Rc2 |  |
| c | sub | SQ | P-gen | arm64 | thru | 1.24 | decQuad | 23.21 | **18.72×** | Rc2 |  |
| c | sub | NQ | P-gen | arm64 | thru | 4.79 | decQuad | 32.42 | **6.77×** | Rc2 |  |
| c | sub | MQ | P-gen | arm64 | thru | 11.35 | decQuad | 30.13 | **2.65×** | Rc2 |  |
| c | sub | OQ | P-gen | arm64 | thru | 12.68 | decQuad | 36.32 | **2.86×** | Rc2 |  |
| c | sub | FQ | P-gen | arm64 | thru | 7.14 | decQuad | 27.69 | **3.88×** | Rc2 |  |
| c | sub | SQ | P-gen | arm64 | thru | 1.24 | mpdecimal | 12.18 | **9.82×** | Rc2 |  |
| c | sub | NQ | P-gen | arm64 | thru | 4.79 | mpdecimal | 22.26 | **4.65×** | Rc2 |  |
| c | sub | MQ | P-gen | arm64 | thru | 11.35 | mpdecimal | 20.98 | **1.85×** | Rc2 |  |
| c | sub | OQ | P-gen | arm64 | thru | 12.68 | mpdecimal | 46.42 | **3.66×** | Rc2 |  |
| c | sub | FQ | P-gen | arm64 | thru | 7.14 | mpdecimal | 41.10 | **5.76×** | Rc2 |  |

<!-- END GENERATED sub-rel-c -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-c-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | sub | SQ | P-gen | x86_64 | thru | 5.57 | libbid | 34.25 | **6.15×** | xRc2 |  |
| c | sub | NQ | P-gen | x86_64 | thru | 14.00 | libbid | 36.66 | **2.62×** | xRc2 |  |
| c | sub | MQ | P-gen | x86_64 | thru | 35.32 | libbid | 36.66 | **1.04×** | xRc2 |  |
| c | sub | OQ | P-gen | x86_64 | thru | 46.78 | libbid | 51.52 | **1.10×** | xRc2 |  |
| c | sub | FQ | P-gen | x86_64 | thru | 32.92 | libbid | 34.71 | **1.05×** | xRc2 |  |
| c | sub | SQ | P-gen | x86_64 | thru | 5.57 | decQuad | 58.96 | **10.59×** | xRc2 |  |
| c | sub | NQ | P-gen | x86_64 | thru | 14.00 | decQuad | 87.94 | **6.28×** | xRc2 |  |
| c | sub | MQ | P-gen | x86_64 | thru | 35.32 | decQuad | 84.25 | **2.39×** | xRc2 |  |
| c | sub | OQ | P-gen | x86_64 | thru | 46.78 | decQuad | 95.16 | **2.03×** | xRc2 |  |
| c | sub | FQ | P-gen | x86_64 | thru | 32.92 | decQuad | 78.18 | **2.37×** | xRc2 |  |
| c | sub | SQ | P-gen | x86_64 | thru | 5.57 | mpdecimal | 36.59 | **6.57×** | xRc2 |  |
| c | sub | NQ | P-gen | x86_64 | thru | 14.00 | mpdecimal | 55.74 | **3.98×** | xRc2 |  |
| c | sub | MQ | P-gen | x86_64 | thru | 35.32 | mpdecimal | 55.48 | **1.57×** | xRc2 |  |
| c | sub | OQ | P-gen | x86_64 | thru | 46.78 | mpdecimal | 131.30 | **2.81×** | xRc2 |  |
| c | sub | FQ | P-gen | x86_64 | thru | 32.92 | mpdecimal | 84.62 | **2.57×** | xRc2 |  |

<!-- END GENERATED sub-rel-c-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-c -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | mul | CP | P-gen | arm64 | thru | 1.39 | libbid | 24.24 | **17.44×** | Rc2 | **no scaling** — the cheap multiply |
| c | mul | WP | P-gen | arm64 | thru | 20.69 | libbid | 33.43 | **1.62×** | Rc2 | 128-bit recipMulPow10 |
| c | mul | XP | P-gen | arm64 | thru | 29.20 | libbid | 44.63 | **1.53×** | Rc2 | 256-bit recipMulPow10; **1.19× ≈ the recipmul-256 work-order's 1.18–1.54× band** |
| c | mul | CP | P-gen | arm64 | thru | 1.39 | decQuad | 21.74 | **15.64×** | Rc2 | vs DPD |
| c | mul | WP | P-gen | arm64 | thru | 20.69 | decQuad | 26.16 | **1.26×** | Rc2 | vs DPD |
| c | mul | XP | P-gen | arm64 | thru | 29.20 | decQuad | 27.77 | **0.95×** | Rc2 | **decQuad edges d128 on the widest product** (software DPD's flat cost; libbid still slower) |
| c | mul | CP | P-gen | arm64 | thru | 1.39 | mpdecimal | 22.03 | **15.85×** | Rc2 | no-scale multiply vs libmpdec |
| c | mul | WP | P-gen | arm64 | thru | 20.69 | mpdecimal | 53.26 | **2.57×** | Rc2 | 128-bit recipMulPow10 |
| c | mul | XP | P-gen | arm64 | thru | 29.20 | mpdecimal | 72.75 | **2.49×** | Rc2 | **d128 wins the widest product vs libmpdec** (unlike decQuad) |

<!-- END GENERATED mul-rel-c -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-c-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | mul | CP | P-gen | x86_64 | thru | 4.69 | libbid | 47.38 | **10.10×** | xRc2 |  |
| c | mul | WP | P-gen | x86_64 | thru | 46.64 | libbid | 65.94 | **1.41×** | xRc2 |  |
| c | mul | XP | P-gen | x86_64 | thru | 56.37 | libbid | 96.66 | **1.71×** | xRc2 |  |
| c | mul | CP | P-gen | x86_64 | thru | 4.69 | decQuad | 58.68 | **12.51×** | xRc2 |  |
| c | mul | WP | P-gen | x86_64 | thru | 46.64 | decQuad | 74.20 | **1.59×** | xRc2 |  |
| c | mul | XP | P-gen | x86_64 | thru | 56.37 | decQuad | 91.45 | **1.62×** | xRc2 |  |
| c | mul | CP | P-gen | x86_64 | thru | 4.69 | mpdecimal | 63.30 | **13.50×** | xRc2 |  |
| c | mul | WP | P-gen | x86_64 | thru | 46.64 | mpdecimal | 186.07 | **3.99×** | xRc2 |  |
| c | mul | XP | P-gen | x86_64 | thru | 56.37 | mpdecimal | 238.19 | **4.23×** | xRc2 |  |

<!-- END GENERATED mul-rel-c-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-c -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | div | CD | P-gen | arm64 | thru | 42.13 | libbid | 36.61 | **0.87×** | Rc2 | 128÷64 quotient-first (§2.4.10); **libbid wins** — the compact-divide weakness persists |
| c | div | WD | P-gen | arm64 | thru | 38.54 | libbid | 37.71 | **0.98×** | Rc2 | 256÷64; **≈ parity / slight loss** |
| c | div | XD | P-gen | arm64 | thru | 33.72 | libbid | 40.43 | **1.20×** | Rc2 | 256÷128 Möller–Granlund |
| c | div | ET | P-gen | arm64 | thru | 8.40 | libbid | 11.57 | **1.38×** | Rc2 | **quotient-first exact early-out** — beats libbid's exact fast path |
| c | div | PT | P-gen | arm64 | thru | 3.15 | libbid | 11.42 | **3.63×** | Rc2 | `divPow10Divisor` (§2.4.9); **d128's fastest divide** (coeff-1 form) |
| c | div | CD | P-gen | arm64 | thru | 42.13 | decQuad | 71.03 | **1.69×** | Rc2 | vs DPD |
| c | div | WD | P-gen | arm64 | thru | 38.54 | decQuad | 123.03 | **3.19×** | Rc2 | vs DPD |
| c | div | XD | P-gen | arm64 | thru | 33.72 | decQuad | 179.14 | **5.31×** | Rc2 | vs DPD — decNumber divide is slow |
| c | div | ET | P-gen | arm64 | thru | 8.40 | decQuad | 47.96 | **5.71×** | Rc2 | vs DPD |
| c | div | PT | P-gen | arm64 | thru | 3.15 | decQuad | 44.54 | **14.14×** | Rc2 | vs DPD |
| c | div | CD | P-gen | arm64 | thru | 42.13 | mpdecimal | 60.61 | **1.44×** | Rc2 | **narrowest divide gap** (libmpdec's compact divide is its cheapest, like d128's weakness) |
| c | div | WD | P-gen | arm64 | thru | 38.54 | mpdecimal | 92.47 | **2.40×** | Rc2 | 256÷64 |
| c | div | XD | P-gen | arm64 | thru | 33.72 | mpdecimal | 147.57 | **4.38×** | Rc2 | Cowlishaw signature (CD 59 < WD 87 < XD 144) |
| c | div | ET | P-gen | arm64 | thru | 8.40 | mpdecimal | 58.94 | **7.02×** | Rc2 | libmpdec has no exact early-out |
| c | div | PT | P-gen | arm64 | thru | 3.15 | mpdecimal | 51.15 | **16.24×** | Rc2 | **d128's biggest divide win vs libmpdec** |

<!-- END GENERATED div-rel-c -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-c-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | div | CD | P-gen | x86_64 | thru | 88.17 | libbid | 82.50 | **0.94×** | xRc2 |  |
| c | div | WD | P-gen | x86_64 | thru | 103.94 | libbid | 84.36 | **0.81×** | xRc2 |  |
| c | div | XD | P-gen | x86_64 | thru | 92.88 | libbid | 84.37 | **0.91×** | xRc2 |  |
| c | div | ET | P-gen | x86_64 | thru | 29.28 | libbid | 30.87 | **1.05×** | xRc2 |  |
| c | div | PT | P-gen | x86_64 | thru | 10.10 | libbid | 31.09 | **3.08×** | xRc2 |  |
| c | div | CD | P-gen | x86_64 | thru | 88.17 | decQuad | 141.08 | **1.60×** | xRc2 |  |
| c | div | WD | P-gen | x86_64 | thru | 103.94 | decQuad | 250.81 | **2.41×** | xRc2 |  |
| c | div | XD | P-gen | x86_64 | thru | 92.88 | decQuad | 386.79 | **4.16×** | xRc2 |  |
| c | div | ET | P-gen | x86_64 | thru | 29.28 | decQuad | 98.60 | **3.37×** | xRc2 |  |
| c | div | PT | P-gen | x86_64 | thru | 10.10 | decQuad | 84.57 | **8.37×** | xRc2 |  |
| c | div | CD | P-gen | x86_64 | thru | 88.17 | mpdecimal | 161.54 | **1.83×** | xRc2 |  |
| c | div | WD | P-gen | x86_64 | thru | 103.94 | mpdecimal | 284.94 | **2.74×** | xRc2 |  |
| c | div | XD | P-gen | x86_64 | thru | 92.88 | mpdecimal | 363.97 | **3.92×** | xRc2 |  |
| c | div | ET | P-gen | x86_64 | thru | 29.28 | mpdecimal | 157.26 | **5.37×** | xRc2 |  |
| c | div | PT | P-gen | x86_64 | thru | 10.10 | mpdecimal | 105.98 | **10.49×** | xRc2 |  |

<!-- END GENERATED div-rel-c-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-c -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | fma | FN | FMA | arm64 | thru | 79.12 | libbid | 82.34 | **1.04×** | Rc2 |  |
| c | fma | FF | FMA | arm64 | thru | 42.22 | libbid | 59.70 | **1.41×** | Rc2 |  |
| c | fma | FN | FMA | arm64 | thru | 79.12 | decQuad | 61.27 | **0.77×** | Rc2 |  |
| c | fma | FF | FMA | arm64 | thru | 42.22 | decQuad | 71.75 | **1.70×** | Rc2 |  |
| c | fma | FN | FMA | arm64 | thru | 79.12 | mpdecimal | 89.61 | **1.13×** | Rc2 |  |
| c | fma | FF | FMA | arm64 | thru | 42.22 | mpdecimal | 145.83 | **3.45×** | Rc2 |  |

<!-- END GENERATED fma-rel-c -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-c-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | fma | FN | FMA | x86_64 | thru | 151.81 | libbid | 161.79 | **1.07×** | xRc2 |  |
| c | fma | FF | FMA | x86_64 | thru | 93.23 | libbid | 124.13 | **1.33×** | xRc2 |  |
| c | fma | FN | FMA | x86_64 | thru | 151.81 | decQuad | 148.04 | **0.98×** | xRc2 |  |
| c | fma | FF | FMA | x86_64 | thru | 93.23 | decQuad | 155.81 | **1.67×** | xRc2 |  |
| c | fma | FN | FMA | x86_64 | thru | 151.81 | mpdecimal | 261.29 | **1.72×** | xRc2 |  |
| c | fma | FF | FMA | x86_64 | thru | 93.23 | mpdecimal | 339.01 | **3.64×** | xRc2 |  |

<!-- END GENERATED fma-rel-c-x86 -->

</div>
