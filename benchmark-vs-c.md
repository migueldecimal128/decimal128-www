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

Each row below is the ratio for that reference library on x86_64 (Intel i9-9880H): `ratio = libbid / Miguel`, `ratio = decQuad / Miguel`, or `ratio = mpdecimal / Miguel` (&gt; 1× ⇒ d128 faster), broken out by operation.

| | Add | Subtract | Multiply | Divide |
|---|---|---|---|---|
| ratio = libbid / Miguel | 3× | 4× | 1.3× – 19× | 0.8× – 1.9× |
| ratio = decQuad / Miguel | 6× | 7× | 1.5× – 22× | 1.6× – 7× |
| ratio = mpdecimal / Miguel | 4× | 5× | 1.0× – 13× | 1.8× – 9× |

## FinMix — realistic financial mix (P-fin)

The headline: one realistic 64-bit financial operation mix — a `MIX` add/sub stream, mul `CP`/`WP`, div `CD`/`WD`/`ET`/`PT` — `ratio = alt / Miguel` (&gt; 1 ⇒ d128 faster). This is the profile closest to real financial code.

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED pfin-rel-c -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | add | MIX | P-fin | arm64 | thru | 1.59 | libbid | 10.89 | **6.85×** | Rc2 |  |
| c | sub | MIX | P-fin | arm64 | thru | 2.12 | libbid | 12.78 | **6.03×** | Rc2 |  |
| c | mul | CP | P-fin | arm64 | thru | 1.22 | libbid | 23.91 | **19.60×** | Rc2 |  |
| c | mul | WP | P-fin | arm64 | thru | 20.65 | libbid | 34.44 | **1.67×** | Rc2 |  |
| c | div | CD | P-fin | arm64 | thru | 32.29 | libbid | 36.30 | **1.12×** | Rc2 |  |
| c | div | WD | P-fin | arm64 | thru | 38.59 | libbid | 39.20 | **1.02×** | Rc2 |  |
| c | div | ET | P-fin | arm64 | thru | 6.35 | libbid | 6.11 | **0.96×** | Rc2 |  |
| c | div | PT | P-fin | arm64 | thru | 3.13 | libbid | 6.11 | **1.95×** | Rc2 |  |
| c | add | MIX | P-fin | arm64 | thru | 1.59 | decQuad | 13.91 | **8.75×** | Rc2 |  |
| c | sub | MIX | P-fin | arm64 | thru | 2.12 | decQuad | 32.10 | **15.14×** | Rc2 |  |
| c | mul | CP | P-fin | arm64 | thru | 1.22 | decQuad | 21.65 | **17.75×** | Rc2 |  |
| c | mul | WP | P-fin | arm64 | thru | 20.65 | decQuad | 26.69 | **1.29×** | Rc2 |  |
| c | div | CD | P-fin | arm64 | thru | 32.29 | decQuad | 75.96 | **2.35×** | Rc2 |  |
| c | div | WD | P-fin | arm64 | thru | 38.59 | decQuad | 117.49 | **3.04×** | Rc2 |  |
| c | div | ET | P-fin | arm64 | thru | 6.35 | decQuad | 41.35 | **6.51×** | Rc2 |  |
| c | div | PT | P-fin | arm64 | thru | 3.13 | decQuad | 39.02 | **12.47×** | Rc2 |  |
| c | add | MIX | P-fin | arm64 | thru | 1.59 | mpdecimal | 13.41 | **8.43×** | Rc2 |  |
| c | sub | MIX | P-fin | arm64 | thru | 2.12 | mpdecimal | 13.80 | **6.51×** | Rc2 |  |
| c | mul | CP | P-fin | arm64 | thru | 1.22 | mpdecimal | 13.55 | **11.11×** | Rc2 |  |
| c | mul | WP | P-fin | arm64 | thru | 20.65 | mpdecimal | 30.44 | **1.47×** | Rc2 |  |
| c | div | CD | P-fin | arm64 | thru | 32.29 | mpdecimal | 59.70 | **1.85×** | Rc2 |  |
| c | div | WD | P-fin | arm64 | thru | 38.59 | mpdecimal | 87.26 | **2.26×** | Rc2 |  |
| c | div | ET | P-fin | arm64 | thru | 6.35 | mpdecimal | 57.61 | **9.07×** | Rc2 |  |
| c | div | PT | P-fin | arm64 | thru | 3.13 | mpdecimal | 47.45 | **15.16×** | Rc2 |  |

<!-- END GENERATED pfin-rel-c -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-c-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | add | MIX | P-fin | x86_64 | thru | 5.04 | libbid | 27.25 | **5.41×** | xRc2 |  |
| c | sub | MIX | P-fin | x86_64 | thru | 5.79 | libbid | 29.07 | **5.02×** | xRc2 |  |
| c | mul | CP | P-fin | x86_64 | thru | 2.54 | libbid | 43.66 | **17.19×** | xRc2 |  |
| c | mul | WP | P-fin | x86_64 | thru | 32.89 | libbid | 57.74 | **1.76×** | xRc2 |  |
| c | div | CD | P-fin | x86_64 | thru | 63.00 | libbid | 74.49 | **1.18×** | xRc2 |  |
| c | div | WD | P-fin | x86_64 | thru | 83.65 | libbid | 80.94 | **0.97×** | xRc2 |  |
| c | div | ET | P-fin | x86_64 | thru | 16.87 | libbid | 19.63 | **1.16×** | xRc2 |  |
| c | div | PT | P-fin | x86_64 | thru | 6.81 | libbid | 19.17 | **2.81×** | xRc2 |  |
| c | add | MIX | P-fin | x86_64 | thru | 5.04 | decQuad | 33.61 | **6.67×** | xRc2 |  |
| c | sub | MIX | P-fin | x86_64 | thru | 5.79 | decQuad | 76.00 | **13.13×** | xRc2 |  |
| c | mul | CP | P-fin | x86_64 | thru | 2.54 | decQuad | 57.41 | **22.60×** | xRc2 |  |
| c | mul | WP | P-fin | x86_64 | thru | 32.89 | decQuad | 65.95 | **2.01×** | xRc2 |  |
| c | div | CD | P-fin | x86_64 | thru | 63.00 | decQuad | 129.90 | **2.06×** | xRc2 |  |
| c | div | WD | P-fin | x86_64 | thru | 83.65 | decQuad | 234.55 | **2.80×** | xRc2 |  |
| c | div | ET | P-fin | x86_64 | thru | 16.87 | decQuad | 73.81 | **4.38×** | xRc2 |  |
| c | div | PT | P-fin | x86_64 | thru | 6.81 | decQuad | 66.38 | **9.75×** | xRc2 |  |
| c | add | MIX | P-fin | x86_64 | thru | 5.04 | mpdecimal | 32.61 | **6.47×** | xRc2 |  |
| c | sub | MIX | P-fin | x86_64 | thru | 5.79 | mpdecimal | 37.25 | **6.43×** | xRc2 |  |
| c | mul | CP | P-fin | x86_64 | thru | 2.54 | mpdecimal | 32.11 | **12.64×** | xRc2 |  |
| c | mul | WP | P-fin | x86_64 | thru | 32.89 | mpdecimal | 42.02 | **1.28×** | xRc2 |  |
| c | div | CD | P-fin | x86_64 | thru | 63.00 | mpdecimal | 153.76 | **2.44×** | xRc2 |  |
| c | div | WD | P-fin | x86_64 | thru | 83.65 | mpdecimal | 274.29 | **3.28×** | xRc2 |  |
| c | div | ET | P-fin | x86_64 | thru | 16.87 | mpdecimal | 136.60 | **8.10×** | xRc2 |  |
| c | div | PT | P-fin | x86_64 | thru | 6.81 | mpdecimal | 89.24 | **13.10×** | xRc2 |  |

<!-- END GENERATED pfin-rel-c-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-c -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | add | SQ | P-gen | arm64 | thru | 1.50 | libbid | 7.56 | **5.04×** | Rc2 |  |
| c | add | NQ | P-gen | arm64 | thru | 4.21 | libbid | 8.57 | **2.04×** | Rc2 |  |
| c | add | MQ | P-gen | arm64 | thru | 6.42 | libbid | 8.78 | **1.37×** | Rc2 |  |
| c | add | OQ | P-gen | arm64 | thru | 11.49 | libbid | 14.02 | **1.22×** | Rc2 |  |
| c | add | FQ | P-gen | arm64 | thru | 7.28 | libbid | 9.39 | **1.29×** | Rc2 |  |
| c | add | SQ | P-gen | arm64 | thru | 1.50 | decQuad | 20.48 | **13.65×** | Rc2 |  |
| c | add | NQ | P-gen | arm64 | thru | 4.21 | decQuad | 29.88 | **7.10×** | Rc2 |  |
| c | add | MQ | P-gen | arm64 | thru | 6.42 | decQuad | 28.60 | **4.45×** | Rc2 |  |
| c | add | OQ | P-gen | arm64 | thru | 11.49 | decQuad | 36.02 | **3.13×** | Rc2 |  |
| c | add | FQ | P-gen | arm64 | thru | 7.28 | decQuad | 26.75 | **3.67×** | Rc2 |  |
| c | add | SQ | P-gen | arm64 | thru | 1.50 | mpdecimal | 12.38 | **8.25×** | Rc2 |  |
| c | add | NQ | P-gen | arm64 | thru | 4.21 | mpdecimal | 25.96 | **6.17×** | Rc2 |  |
| c | add | MQ | P-gen | arm64 | thru | 6.42 | mpdecimal | 21.19 | **3.30×** | Rc2 |  |
| c | add | OQ | P-gen | arm64 | thru | 11.49 | mpdecimal | 47.28 | **4.11×** | Rc2 |  |
| c | add | FQ | P-gen | arm64 | thru | 7.28 | mpdecimal | 40.46 | **5.56×** | Rc2 |  |

<!-- END GENERATED add-rel-c -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-c-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | add | SQ | P-gen | x86_64 | thru | 4.60 | libbid | 29.63 | **6.44×** | xRc2 |  |
| c | add | NQ | P-gen | x86_64 | thru | 11.39 | libbid | 31.31 | **2.75×** | xRc2 |  |
| c | add | MQ | P-gen | x86_64 | thru | 20.84 | libbid | 29.79 | **1.43×** | xRc2 |  |
| c | add | OQ | P-gen | x86_64 | thru | 34.55 | libbid | 45.64 | **1.32×** | xRc2 |  |
| c | add | FQ | P-gen | x86_64 | thru | 24.05 | libbid | 29.19 | **1.21×** | xRc2 |  |
| c | add | SQ | P-gen | x86_64 | thru | 4.60 | decQuad | 51.37 | **11.17×** | xRc2 |  |
| c | add | NQ | P-gen | x86_64 | thru | 11.39 | decQuad | 78.46 | **6.89×** | xRc2 |  |
| c | add | MQ | P-gen | x86_64 | thru | 20.84 | decQuad | 75.84 | **3.64×** | xRc2 |  |
| c | add | OQ | P-gen | x86_64 | thru | 34.55 | decQuad | 84.81 | **2.45×** | xRc2 |  |
| c | add | FQ | P-gen | x86_64 | thru | 24.05 | decQuad | 68.94 | **2.87×** | xRc2 |  |
| c | add | SQ | P-gen | x86_64 | thru | 4.60 | mpdecimal | 35.18 | **7.65×** | xRc2 |  |
| c | add | NQ | P-gen | x86_64 | thru | 11.39 | mpdecimal | 53.74 | **4.72×** | xRc2 |  |
| c | add | MQ | P-gen | x86_64 | thru | 20.84 | mpdecimal | 52.60 | **2.52×** | xRc2 |  |
| c | add | OQ | P-gen | x86_64 | thru | 34.55 | mpdecimal | 124.91 | **3.62×** | xRc2 |  |
| c | add | FQ | P-gen | x86_64 | thru | 24.05 | mpdecimal | 82.99 | **3.45×** | xRc2 |  |

<!-- END GENERATED add-rel-c-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-c -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | sub | SQ | P-gen | arm64 | thru | 1.23 | libbid | 9.27 | **7.54×** | Rc2 |  |
| c | sub | NQ | P-gen | arm64 | thru | 4.67 | libbid | 10.26 | **2.20×** | Rc2 |  |
| c | sub | MQ | P-gen | arm64 | thru | 6.85 | libbid | 10.83 | **1.58×** | Rc2 |  |
| c | sub | OQ | P-gen | arm64 | thru | 11.86 | libbid | 14.74 | **1.24×** | Rc2 |  |
| c | sub | FQ | P-gen | arm64 | thru | 7.85 | libbid | 10.55 | **1.34×** | Rc2 |  |
| c | sub | SQ | P-gen | arm64 | thru | 1.23 | decQuad | 22.83 | **18.56×** | Rc2 |  |
| c | sub | NQ | P-gen | arm64 | thru | 4.67 | decQuad | 32.50 | **6.96×** | Rc2 |  |
| c | sub | MQ | P-gen | arm64 | thru | 6.85 | decQuad | 30.71 | **4.48×** | Rc2 |  |
| c | sub | OQ | P-gen | arm64 | thru | 11.86 | decQuad | 38.01 | **3.20×** | Rc2 |  |
| c | sub | FQ | P-gen | arm64 | thru | 7.85 | decQuad | 30.07 | **3.83×** | Rc2 |  |
| c | sub | SQ | P-gen | arm64 | thru | 1.23 | mpdecimal | 12.97 | **10.54×** | Rc2 |  |
| c | sub | NQ | P-gen | arm64 | thru | 4.67 | mpdecimal | 22.16 | **4.75×** | Rc2 |  |
| c | sub | MQ | P-gen | arm64 | thru | 6.85 | mpdecimal | 25.80 | **3.77×** | Rc2 |  |
| c | sub | OQ | P-gen | arm64 | thru | 11.86 | mpdecimal | 47.38 | **3.99×** | Rc2 |  |
| c | sub | FQ | P-gen | arm64 | thru | 7.85 | mpdecimal | 41.75 | **5.32×** | Rc2 |  |

<!-- END GENERATED sub-rel-c -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-c-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | sub | SQ | P-gen | x86_64 | thru | 5.18 | libbid | 32.65 | **6.30×** | xRc2 |  |
| c | sub | NQ | P-gen | x86_64 | thru | 11.79 | libbid | 34.71 | **2.94×** | xRc2 |  |
| c | sub | MQ | P-gen | x86_64 | thru | 21.15 | libbid | 35.56 | **1.68×** | xRc2 |  |
| c | sub | OQ | P-gen | x86_64 | thru | 34.02 | libbid | 52.33 | **1.54×** | xRc2 |  |
| c | sub | FQ | P-gen | x86_64 | thru | 24.29 | libbid | 33.88 | **1.39×** | xRc2 |  |
| c | sub | SQ | P-gen | x86_64 | thru | 5.18 | decQuad | 55.88 | **10.79×** | xRc2 |  |
| c | sub | NQ | P-gen | x86_64 | thru | 11.79 | decQuad | 82.96 | **7.04×** | xRc2 |  |
| c | sub | MQ | P-gen | x86_64 | thru | 21.15 | decQuad | 84.91 | **4.01×** | xRc2 |  |
| c | sub | OQ | P-gen | x86_64 | thru | 34.02 | decQuad | 94.29 | **2.77×** | xRc2 |  |
| c | sub | FQ | P-gen | x86_64 | thru | 24.29 | decQuad | 74.75 | **3.08×** | xRc2 |  |
| c | sub | SQ | P-gen | x86_64 | thru | 5.18 | mpdecimal | 35.32 | **6.82×** | xRc2 |  |
| c | sub | NQ | P-gen | x86_64 | thru | 11.79 | mpdecimal | 57.15 | **4.85×** | xRc2 |  |
| c | sub | MQ | P-gen | x86_64 | thru | 21.15 | mpdecimal | 56.38 | **2.67×** | xRc2 |  |
| c | sub | OQ | P-gen | x86_64 | thru | 34.02 | mpdecimal | 129.77 | **3.81×** | xRc2 |  |
| c | sub | FQ | P-gen | x86_64 | thru | 24.29 | mpdecimal | 83.61 | **3.44×** | xRc2 |  |

<!-- END GENERATED sub-rel-c-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-c -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | mul | CP | P-gen | arm64 | thru | 1.40 | libbid | 24.58 | **17.56×** | Rc2 | **no scaling** — the cheap multiply |
| c | mul | WP | P-gen | arm64 | thru | 20.73 | libbid | 33.28 | **1.61×** | Rc2 | 128-bit recipMulPow10 |
| c | mul | XP | P-gen | arm64 | thru | 25.38 | libbid | 45.22 | **1.78×** | Rc2 | 256-bit recipMulPow10; **1.19× ≈ the recipmul-256 work-order's 1.18–1.54× band** |
| c | mul | CP | P-gen | arm64 | thru | 1.40 | decQuad | 21.54 | **15.39×** | Rc2 | vs DPD |
| c | mul | WP | P-gen | arm64 | thru | 20.73 | decQuad | 27.32 | **1.32×** | Rc2 | vs DPD |
| c | mul | XP | P-gen | arm64 | thru | 25.38 | decQuad | 30.01 | **1.18×** | Rc2 | **decQuad edges d128 on the widest product** (software DPD's flat cost; libbid still slower) |
| c | mul | CP | P-gen | arm64 | thru | 1.40 | mpdecimal | 21.98 | **15.70×** | Rc2 | no-scale multiply vs libmpdec |
| c | mul | WP | P-gen | arm64 | thru | 20.73 | mpdecimal | 53.43 | **2.58×** | Rc2 | 128-bit recipMulPow10 |
| c | mul | XP | P-gen | arm64 | thru | 25.38 | mpdecimal | 72.44 | **2.85×** | Rc2 | **d128 wins the widest product vs libmpdec** (unlike decQuad) |

<!-- END GENERATED mul-rel-c -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-c-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | mul | CP | P-gen | x86_64 | thru | 3.83 | libbid | 49.91 | **13.03×** | xRc2 |  |
| c | mul | WP | P-gen | x86_64 | thru | 34.95 | libbid | 77.04 | **2.20×** | xRc2 |  |
| c | mul | XP | P-gen | x86_64 | thru | 44.24 | libbid | 97.21 | **2.20×** | xRc2 |  |
| c | mul | CP | P-gen | x86_64 | thru | 3.83 | decQuad | 63.21 | **16.50×** | xRc2 |  |
| c | mul | WP | P-gen | x86_64 | thru | 34.95 | decQuad | 73.67 | **2.11×** | xRc2 |  |
| c | mul | XP | P-gen | x86_64 | thru | 44.24 | decQuad | 90.21 | **2.04×** | xRc2 |  |
| c | mul | CP | P-gen | x86_64 | thru | 3.83 | mpdecimal | 67.43 | **17.61×** | xRc2 |  |
| c | mul | WP | P-gen | x86_64 | thru | 34.95 | mpdecimal | 190.27 | **5.44×** | xRc2 |  |
| c | mul | XP | P-gen | x86_64 | thru | 44.24 | mpdecimal | 234.30 | **5.30×** | xRc2 |  |

<!-- END GENERATED mul-rel-c-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-c -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | div | CD | P-gen | arm64 | thru | 29.01 | libbid | 36.64 | **1.26×** | Rc2 | 128÷64 quotient-first (§2.4.10); **libbid wins** — the compact-divide weakness persists |
| c | div | WD | P-gen | arm64 | thru | 37.85 | libbid | 37.56 | **0.99×** | Rc2 | 256÷64; **≈ parity / slight loss** |
| c | div | XD | P-gen | arm64 | thru | 31.19 | libbid | 39.18 | **1.26×** | Rc2 | 256÷128 Möller–Granlund |
| c | div | ET | P-gen | arm64 | thru | 8.21 | libbid | 11.64 | **1.42×** | Rc2 | **quotient-first exact early-out** — beats libbid's exact fast path |
| c | div | PT | P-gen | arm64 | thru | 3.12 | libbid | 11.54 | **3.70×** | Rc2 | `divPow10Divisor` (§2.4.9); **d128's fastest divide** (coeff-1 form) |
| c | div | CD | P-gen | arm64 | thru | 29.01 | decQuad | 74.62 | **2.57×** | Rc2 | vs DPD |
| c | div | WD | P-gen | arm64 | thru | 37.85 | decQuad | 116.59 | **3.08×** | Rc2 | vs DPD |
| c | div | XD | P-gen | arm64 | thru | 31.19 | decQuad | 173.95 | **5.58×** | Rc2 | vs DPD — decNumber divide is slow |
| c | div | ET | P-gen | arm64 | thru | 8.21 | decQuad | 48.13 | **5.86×** | Rc2 | vs DPD |
| c | div | PT | P-gen | arm64 | thru | 3.12 | decQuad | 44.44 | **14.24×** | Rc2 | vs DPD |
| c | div | CD | P-gen | arm64 | thru | 29.01 | mpdecimal | 60.27 | **2.08×** | Rc2 | **narrowest divide gap** (libmpdec's compact divide is its cheapest, like d128's weakness) |
| c | div | WD | P-gen | arm64 | thru | 37.85 | mpdecimal | 90.80 | **2.40×** | Rc2 | 256÷64 |
| c | div | XD | P-gen | arm64 | thru | 31.19 | mpdecimal | 145.79 | **4.67×** | Rc2 | Cowlishaw signature (CD 59 < WD 87 < XD 144) |
| c | div | ET | P-gen | arm64 | thru | 8.21 | mpdecimal | 61.50 | **7.49×** | Rc2 | libmpdec has no exact early-out |
| c | div | PT | P-gen | arm64 | thru | 3.12 | mpdecimal | 51.04 | **16.36×** | Rc2 | **d128's biggest divide win vs libmpdec** |

<!-- END GENERATED div-rel-c -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-c-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | div | CD | P-gen | x86_64 | thru | 88.90 | libbid | 83.35 | **0.94×** | xRc2 |  |
| c | div | WD | P-gen | x86_64 | thru | 87.79 | libbid | 85.72 | **0.98×** | xRc2 |  |
| c | div | XD | P-gen | x86_64 | thru | 74.48 | libbid | 84.67 | **1.14×** | xRc2 |  |
| c | div | ET | P-gen | x86_64 | thru | 27.29 | libbid | 29.45 | **1.08×** | xRc2 |  |
| c | div | PT | P-gen | x86_64 | thru | 6.75 | libbid | 29.43 | **4.36×** | xRc2 |  |
| c | div | CD | P-gen | x86_64 | thru | 88.90 | decQuad | 175.19 | **1.97×** | xRc2 |  |
| c | div | WD | P-gen | x86_64 | thru | 87.79 | decQuad | 242.17 | **2.76×** | xRc2 |  |
| c | div | XD | P-gen | x86_64 | thru | 74.48 | decQuad | 378.15 | **5.08×** | xRc2 |  |
| c | div | ET | P-gen | x86_64 | thru | 27.29 | decQuad | 102.45 | **3.75×** | xRc2 |  |
| c | div | PT | P-gen | x86_64 | thru | 6.75 | decQuad | 81.97 | **12.14×** | xRc2 |  |
| c | div | CD | P-gen | x86_64 | thru | 88.90 | mpdecimal | 191.98 | **2.16×** | xRc2 |  |
| c | div | WD | P-gen | x86_64 | thru | 87.79 | mpdecimal | 302.31 | **3.44×** | xRc2 |  |
| c | div | XD | P-gen | x86_64 | thru | 74.48 | mpdecimal | 350.37 | **4.70×** | xRc2 |  |
| c | div | ET | P-gen | x86_64 | thru | 27.29 | mpdecimal | 150.97 | **5.53×** | xRc2 |  |
| c | div | PT | P-gen | x86_64 | thru | 6.75 | mpdecimal | 97.43 | **14.43×** | xRc2 |  |

<!-- END GENERATED div-rel-c-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-c -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | fma | FN | FMA | arm64 | thru | 77.72 | libbid | 85.21 | **1.10×** | Rc2 |  |
| c | fma | FF | FMA | arm64 | thru | 39.45 | libbid | 57.70 | **1.46×** | Rc2 |  |
| c | fma | FN | FMA | arm64 | thru | 77.72 | decQuad | 63.59 | **0.82×** | Rc2 |  |
| c | fma | FF | FMA | arm64 | thru | 39.45 | decQuad | 70.65 | **1.79×** | Rc2 |  |
| c | fma | FN | FMA | arm64 | thru | 77.72 | mpdecimal | 91.80 | **1.18×** | Rc2 |  |
| c | fma | FF | FMA | arm64 | thru | 39.45 | mpdecimal | 149.25 | **3.78×** | Rc2 |  |

<!-- END GENERATED fma-rel-c -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-c-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | fma | FN | FMA | x86_64 | thru | 112.39 | libbid | 155.00 | **1.38×** | xRc2 |  |
| c | fma | FF | FMA | x86_64 | thru | 71.56 | libbid | 118.50 | **1.66×** | xRc2 |  |
| c | fma | FN | FMA | x86_64 | thru | 112.39 | decQuad | 140.96 | **1.25×** | xRc2 |  |
| c | fma | FF | FMA | x86_64 | thru | 71.56 | decQuad | 145.99 | **2.04×** | xRc2 |  |
| c | fma | FN | FMA | x86_64 | thru | 112.39 | mpdecimal | 252.65 | **2.25×** | xRc2 |  |
| c | fma | FF | FMA | x86_64 | thru | 71.56 | mpdecimal | 329.76 | **4.61×** | xRc2 |  |

<!-- END GENERATED fma-rel-c-x86 -->

</div>
