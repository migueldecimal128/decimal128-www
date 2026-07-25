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
| c | add | MIX | P-fin | arm64 | thru | 1.72 | libbid | 10.75 | **6.25×** | Rc2 |  |
| c | sub | MIX | P-fin | arm64 | thru | 2.08 | libbid | 13.35 | **6.42×** | Rc2 |  |
| c | mul | CP | P-fin | arm64 | thru | 1.27 | libbid | 23.54 | **18.54×** | Rc2 |  |
| c | mul | WP | P-fin | arm64 | thru | 20.60 | libbid | 32.43 | **1.57×** | Rc2 |  |
| c | div | CD | P-fin | arm64 | thru | 32.33 | libbid | 36.12 | **1.12×** | Rc2 |  |
| c | div | WD | P-fin | arm64 | thru | 38.45 | libbid | 39.16 | **1.02×** | Rc2 |  |
| c | div | ET | P-fin | arm64 | thru | 6.35 | libbid | 6.10 | **0.96×** | Rc2 |  |
| c | div | PT | P-fin | arm64 | thru | 3.13 | libbid | 6.10 | **1.95×** | Rc2 |  |
| c | add | MIX | P-fin | arm64 | thru | 1.72 | decQuad | 13.89 | **8.08×** | Rc2 |  |
| c | sub | MIX | P-fin | arm64 | thru | 2.08 | decQuad | 31.23 | **15.01×** | Rc2 |  |
| c | mul | CP | P-fin | arm64 | thru | 1.27 | decQuad | 21.07 | **16.59×** | Rc2 |  |
| c | mul | WP | P-fin | arm64 | thru | 20.60 | decQuad | 25.61 | **1.24×** | Rc2 |  |
| c | div | CD | P-fin | arm64 | thru | 32.33 | decQuad | 75.67 | **2.34×** | Rc2 |  |
| c | div | WD | P-fin | arm64 | thru | 38.45 | decQuad | 116.99 | **3.04×** | Rc2 |  |
| c | div | ET | P-fin | arm64 | thru | 6.35 | decQuad | 40.83 | **6.43×** | Rc2 |  |
| c | div | PT | P-fin | arm64 | thru | 3.13 | decQuad | 39.43 | **12.60×** | Rc2 |  |
| c | add | MIX | P-fin | arm64 | thru | 1.72 | mpdecimal | 12.85 | **7.47×** | Rc2 |  |
| c | sub | MIX | P-fin | arm64 | thru | 2.08 | mpdecimal | 15.81 | **7.60×** | Rc2 |  |
| c | mul | CP | P-fin | arm64 | thru | 1.27 | mpdecimal | 12.69 | **9.99×** | Rc2 |  |
| c | mul | WP | P-fin | arm64 | thru | 20.60 | mpdecimal | 28.93 | **1.40×** | Rc2 |  |
| c | div | CD | P-fin | arm64 | thru | 32.33 | mpdecimal | 62.76 | **1.94×** | Rc2 |  |
| c | div | WD | P-fin | arm64 | thru | 38.45 | mpdecimal | 86.78 | **2.26×** | Rc2 |  |
| c | div | ET | P-fin | arm64 | thru | 6.35 | mpdecimal | 55.66 | **8.77×** | Rc2 |  |
| c | div | PT | P-fin | arm64 | thru | 3.13 | mpdecimal | 45.61 | **14.57×** | Rc2 |  |

<!-- END GENERATED pfin-rel-c -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-c-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | add | MIX | P-fin | x86_64 | thru | 5.63 | libbid | 28.09 | **4.99×** | xRc2 |  |
| c | sub | MIX | P-fin | x86_64 | thru | 5.70 | libbid | 29.12 | **5.11×** | xRc2 |  |
| c | mul | CP | P-fin | x86_64 | thru | 2.42 | libbid | 44.34 | **18.32×** | xRc2 |  |
| c | mul | WP | P-fin | x86_64 | thru | 40.91 | libbid | 58.84 | **1.44×** | xRc2 |  |
| c | div | CD | P-fin | x86_64 | thru | 72.47 | libbid | 73.35 | **1.01×** | xRc2 |  |
| c | div | WD | P-fin | x86_64 | thru | 99.28 | libbid | 79.45 | **0.80×** | xRc2 |  |
| c | div | ET | P-fin | x86_64 | thru | 18.22 | libbid | 18.93 | **1.04×** | xRc2 |  |
| c | div | PT | P-fin | x86_64 | thru | 9.94 | libbid | 18.69 | **1.88×** | xRc2 |  |
| c | add | MIX | P-fin | x86_64 | thru | 5.63 | decQuad | 32.63 | **5.80×** | xRc2 |  |
| c | sub | MIX | P-fin | x86_64 | thru | 5.70 | decQuad | 77.41 | **13.58×** | xRc2 |  |
| c | mul | CP | P-fin | x86_64 | thru | 2.42 | decQuad | 55.85 | **23.08×** | xRc2 |  |
| c | mul | WP | P-fin | x86_64 | thru | 40.91 | decQuad | 65.79 | **1.61×** | xRc2 |  |
| c | div | CD | P-fin | x86_64 | thru | 72.47 | decQuad | 135.69 | **1.87×** | xRc2 |  |
| c | div | WD | P-fin | x86_64 | thru | 99.28 | decQuad | 233.68 | **2.35×** | xRc2 |  |
| c | div | ET | P-fin | x86_64 | thru | 18.22 | decQuad | 73.36 | **4.03×** | xRc2 |  |
| c | div | PT | P-fin | x86_64 | thru | 9.94 | decQuad | 65.67 | **6.61×** | xRc2 |  |
| c | add | MIX | P-fin | x86_64 | thru | 5.63 | mpdecimal | 33.07 | **5.87×** | xRc2 |  |
| c | sub | MIX | P-fin | x86_64 | thru | 5.70 | mpdecimal | 36.50 | **6.40×** | xRc2 |  |
| c | mul | CP | P-fin | x86_64 | thru | 2.42 | mpdecimal | 30.93 | **12.78×** | xRc2 |  |
| c | mul | WP | P-fin | x86_64 | thru | 40.91 | mpdecimal | 41.63 | **1.02×** | xRc2 |  |
| c | div | CD | P-fin | x86_64 | thru | 72.47 | mpdecimal | 153.54 | **2.12×** | xRc2 |  |
| c | div | WD | P-fin | x86_64 | thru | 99.28 | mpdecimal | 271.44 | **2.73×** | xRc2 |  |
| c | div | ET | P-fin | x86_64 | thru | 18.22 | mpdecimal | 134.79 | **7.40×** | xRc2 |  |
| c | div | PT | P-fin | x86_64 | thru | 9.94 | mpdecimal | 88.80 | **8.93×** | xRc2 |  |

<!-- END GENERATED pfin-rel-c-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-c -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | add | SQ | P-gen | arm64 | thru | 2.19 | libbid | 8.44 | **3.85×** | Rc2 |  |
| c | add | NQ | P-gen | arm64 | thru | 3.93 | libbid | 9.37 | **2.38×** | Rc2 |  |
| c | add | MQ | P-gen | arm64 | thru | 6.31 | libbid | 8.94 | **1.42×** | Rc2 |  |
| c | add | OQ | P-gen | arm64 | thru | 11.31 | libbid | 14.26 | **1.26×** | Rc2 |  |
| c | add | FQ | P-gen | arm64 | thru | 7.01 | libbid | 9.34 | **1.33×** | Rc2 |  |
| c | add | SQ | P-gen | arm64 | thru | 2.19 | decQuad | 19.99 | **9.13×** | Rc2 |  |
| c | add | NQ | P-gen | arm64 | thru | 3.93 | decQuad | 29.53 | **7.51×** | Rc2 |  |
| c | add | MQ | P-gen | arm64 | thru | 6.31 | decQuad | 29.66 | **4.70×** | Rc2 |  |
| c | add | OQ | P-gen | arm64 | thru | 11.31 | decQuad | 33.66 | **2.98×** | Rc2 |  |
| c | add | FQ | P-gen | arm64 | thru | 7.01 | decQuad | 25.52 | **3.64×** | Rc2 |  |
| c | add | SQ | P-gen | arm64 | thru | 2.19 | mpdecimal | 11.35 | **5.18×** | Rc2 |  |
| c | add | NQ | P-gen | arm64 | thru | 3.93 | mpdecimal | 21.69 | **5.52×** | Rc2 |  |
| c | add | MQ | P-gen | arm64 | thru | 6.31 | mpdecimal | 25.11 | **3.98×** | Rc2 |  |
| c | add | OQ | P-gen | arm64 | thru | 11.31 | mpdecimal | 45.18 | **3.99×** | Rc2 |  |
| c | add | FQ | P-gen | arm64 | thru | 7.01 | mpdecimal | 40.14 | **5.73×** | Rc2 |  |

<!-- END GENERATED add-rel-c -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-c-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | add | SQ | P-gen | x86_64 | thru | 7.97 | libbid | 30.49 | **3.83×** | xRc2 |  |
| c | add | NQ | P-gen | x86_64 | thru | 12.22 | libbid | 32.84 | **2.69×** | xRc2 |  |
| c | add | MQ | P-gen | x86_64 | thru | 23.29 | libbid | 31.94 | **1.37×** | xRc2 |  |
| c | add | OQ | P-gen | x86_64 | thru | 42.89 | libbid | 49.07 | **1.14×** | xRc2 |  |
| c | add | FQ | P-gen | x86_64 | thru | 31.37 | libbid | 31.26 | **1.00×** | xRc2 |  |
| c | add | SQ | P-gen | x86_64 | thru | 7.97 | decQuad | 51.90 | **6.51×** | xRc2 |  |
| c | add | NQ | P-gen | x86_64 | thru | 12.22 | decQuad | 82.97 | **6.79×** | xRc2 |  |
| c | add | MQ | P-gen | x86_64 | thru | 23.29 | decQuad | 79.09 | **3.40×** | xRc2 |  |
| c | add | OQ | P-gen | x86_64 | thru | 42.89 | decQuad | 88.03 | **2.05×** | xRc2 |  |
| c | add | FQ | P-gen | x86_64 | thru | 31.37 | decQuad | 71.27 | **2.27×** | xRc2 |  |
| c | add | SQ | P-gen | x86_64 | thru | 7.97 | mpdecimal | 36.43 | **4.57×** | xRc2 |  |
| c | add | NQ | P-gen | x86_64 | thru | 12.22 | mpdecimal | 56.56 | **4.63×** | xRc2 |  |
| c | add | MQ | P-gen | x86_64 | thru | 23.29 | mpdecimal | 56.22 | **2.41×** | xRc2 |  |
| c | add | OQ | P-gen | x86_64 | thru | 42.89 | mpdecimal | 131.21 | **3.06×** | xRc2 |  |
| c | add | FQ | P-gen | x86_64 | thru | 31.37 | mpdecimal | 88.40 | **2.82×** | xRc2 |  |

<!-- END GENERATED add-rel-c-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-c -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | sub | SQ | P-gen | arm64 | thru | 1.22 | libbid | 8.66 | **7.10×** | Rc2 |  |
| c | sub | NQ | P-gen | arm64 | thru | 4.97 | libbid | 9.93 | **2.00×** | Rc2 |  |
| c | sub | MQ | P-gen | arm64 | thru | 6.66 | libbid | 9.08 | **1.36×** | Rc2 |  |
| c | sub | OQ | P-gen | arm64 | thru | 11.99 | libbid | 14.91 | **1.24×** | Rc2 |  |
| c | sub | FQ | P-gen | arm64 | thru | 7.20 | libbid | 10.50 | **1.46×** | Rc2 |  |
| c | sub | SQ | P-gen | arm64 | thru | 1.22 | decQuad | 22.87 | **18.75×** | Rc2 |  |
| c | sub | NQ | P-gen | arm64 | thru | 4.97 | decQuad | 31.49 | **6.34×** | Rc2 |  |
| c | sub | MQ | P-gen | arm64 | thru | 6.66 | decQuad | 30.92 | **4.64×** | Rc2 |  |
| c | sub | OQ | P-gen | arm64 | thru | 11.99 | decQuad | 38.02 | **3.17×** | Rc2 |  |
| c | sub | FQ | P-gen | arm64 | thru | 7.20 | decQuad | 29.00 | **4.03×** | Rc2 |  |
| c | sub | SQ | P-gen | arm64 | thru | 1.22 | mpdecimal | 11.93 | **9.78×** | Rc2 |  |
| c | sub | NQ | P-gen | arm64 | thru | 4.97 | mpdecimal | 21.73 | **4.37×** | Rc2 |  |
| c | sub | MQ | P-gen | arm64 | thru | 6.66 | mpdecimal | 22.10 | **3.32×** | Rc2 |  |
| c | sub | OQ | P-gen | arm64 | thru | 11.99 | mpdecimal | 47.23 | **3.94×** | Rc2 |  |
| c | sub | FQ | P-gen | arm64 | thru | 7.20 | mpdecimal | 39.81 | **5.53×** | Rc2 |  |

<!-- END GENERATED sub-rel-c -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-c-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | sub | SQ | P-gen | x86_64 | thru | 5.06 | libbid | 35.60 | **7.04×** | xRc2 |  |
| c | sub | NQ | P-gen | x86_64 | thru | 13.33 | libbid | 36.06 | **2.71×** | xRc2 |  |
| c | sub | MQ | P-gen | x86_64 | thru | 23.87 | libbid | 34.36 | **1.44×** | xRc2 |  |
| c | sub | OQ | P-gen | x86_64 | thru | 43.39 | libbid | 50.67 | **1.17×** | xRc2 |  |
| c | sub | FQ | P-gen | x86_64 | thru | 31.41 | libbid | 33.98 | **1.08×** | xRc2 |  |
| c | sub | SQ | P-gen | x86_64 | thru | 5.06 | decQuad | 58.82 | **11.62×** | xRc2 |  |
| c | sub | NQ | P-gen | x86_64 | thru | 13.33 | decQuad | 84.85 | **6.37×** | xRc2 |  |
| c | sub | MQ | P-gen | x86_64 | thru | 23.87 | decQuad | 82.42 | **3.45×** | xRc2 |  |
| c | sub | OQ | P-gen | x86_64 | thru | 43.39 | decQuad | 91.52 | **2.11×** | xRc2 |  |
| c | sub | FQ | P-gen | x86_64 | thru | 31.41 | decQuad | 73.64 | **2.34×** | xRc2 |  |
| c | sub | SQ | P-gen | x86_64 | thru | 5.06 | mpdecimal | 35.09 | **6.93×** | xRc2 |  |
| c | sub | NQ | P-gen | x86_64 | thru | 13.33 | mpdecimal | 52.94 | **3.97×** | xRc2 |  |
| c | sub | MQ | P-gen | x86_64 | thru | 23.87 | mpdecimal | 54.97 | **2.30×** | xRc2 |  |
| c | sub | OQ | P-gen | x86_64 | thru | 43.39 | mpdecimal | 124.29 | **2.86×** | xRc2 |  |
| c | sub | FQ | P-gen | x86_64 | thru | 31.41 | mpdecimal | 83.23 | **2.65×** | xRc2 |  |

<!-- END GENERATED sub-rel-c-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-c -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | mul | CP | P-gen | arm64 | thru | 1.40 | libbid | 22.98 | **16.41×** | Rc2 | **no scaling** — the cheap multiply |
| c | mul | WP | P-gen | arm64 | thru | 20.70 | libbid | 33.15 | **1.60×** | Rc2 | 128-bit recipMulPow10 |
| c | mul | XP | P-gen | arm64 | thru | 25.55 | libbid | 42.97 | **1.68×** | Rc2 | 256-bit recipMulPow10; **1.19× ≈ the recipmul-256 work-order's 1.18–1.54× band** |
| c | mul | CP | P-gen | arm64 | thru | 1.40 | decQuad | 21.13 | **15.09×** | Rc2 | vs DPD |
| c | mul | WP | P-gen | arm64 | thru | 20.70 | decQuad | 26.14 | **1.26×** | Rc2 | vs DPD |
| c | mul | XP | P-gen | arm64 | thru | 25.55 | decQuad | 29.82 | **1.17×** | Rc2 | **decQuad edges d128 on the widest product** (software DPD's flat cost; libbid still slower) |
| c | mul | CP | P-gen | arm64 | thru | 1.40 | mpdecimal | 22.01 | **15.72×** | Rc2 | no-scale multiply vs libmpdec |
| c | mul | WP | P-gen | arm64 | thru | 20.70 | mpdecimal | 52.37 | **2.53×** | Rc2 | 128-bit recipMulPow10 |
| c | mul | XP | P-gen | arm64 | thru | 25.55 | mpdecimal | 73.28 | **2.87×** | Rc2 | **d128 wins the widest product vs libmpdec** (unlike decQuad) |

<!-- END GENERATED mul-rel-c -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-c-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | mul | CP | P-gen | x86_64 | thru | 4.39 | libbid | 46.30 | **10.55×** | xRc2 |  |
| c | mul | WP | P-gen | x86_64 | thru | 40.35 | libbid | 64.78 | **1.61×** | xRc2 |  |
| c | mul | XP | P-gen | x86_64 | thru | 48.65 | libbid | 93.04 | **1.91×** | xRc2 |  |
| c | mul | CP | P-gen | x86_64 | thru | 4.39 | decQuad | 56.50 | **12.87×** | xRc2 |  |
| c | mul | WP | P-gen | x86_64 | thru | 40.35 | decQuad | 68.65 | **1.70×** | xRc2 |  |
| c | mul | XP | P-gen | x86_64 | thru | 48.65 | decQuad | 84.39 | **1.73×** | xRc2 |  |
| c | mul | CP | P-gen | x86_64 | thru | 4.39 | mpdecimal | 62.52 | **14.24×** | xRc2 |  |
| c | mul | WP | P-gen | x86_64 | thru | 40.35 | mpdecimal | 184.16 | **4.56×** | xRc2 |  |
| c | mul | XP | P-gen | x86_64 | thru | 48.65 | mpdecimal | 223.01 | **4.58×** | xRc2 |  |

<!-- END GENERATED mul-rel-c-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-c -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | div | CD | P-gen | arm64 | thru | 30.65 | libbid | 37.45 | **1.22×** | Rc2 | 128÷64 quotient-first (§2.4.10); **libbid wins** — the compact-divide weakness persists |
| c | div | WD | P-gen | arm64 | thru | 37.59 | libbid | 37.57 | **1.00×** | Rc2 | 256÷64; **≈ parity / slight loss** |
| c | div | XD | P-gen | arm64 | thru | 29.90 | libbid | 39.17 | **1.31×** | Rc2 | 256÷128 Möller–Granlund |
| c | div | ET | P-gen | arm64 | thru | 8.26 | libbid | 11.67 | **1.41×** | Rc2 | **quotient-first exact early-out** — beats libbid's exact fast path |
| c | div | PT | P-gen | arm64 | thru | 3.12 | libbid | 11.43 | **3.66×** | Rc2 | `divPow10Divisor` (§2.4.9); **d128's fastest divide** (coeff-1 form) |
| c | div | CD | P-gen | arm64 | thru | 30.65 | decQuad | 75.31 | **2.46×** | Rc2 | vs DPD |
| c | div | WD | P-gen | arm64 | thru | 37.59 | decQuad | 115.85 | **3.08×** | Rc2 | vs DPD |
| c | div | XD | P-gen | arm64 | thru | 29.90 | decQuad | 173.54 | **5.80×** | Rc2 | vs DPD — decNumber divide is slow |
| c | div | ET | P-gen | arm64 | thru | 8.26 | decQuad | 47.97 | **5.81×** | Rc2 | vs DPD |
| c | div | PT | P-gen | arm64 | thru | 3.12 | decQuad | 44.05 | **14.12×** | Rc2 | vs DPD |
| c | div | CD | P-gen | arm64 | thru | 30.65 | mpdecimal | 61.56 | **2.01×** | Rc2 | **narrowest divide gap** (libmpdec's compact divide is its cheapest, like d128's weakness) |
| c | div | WD | P-gen | arm64 | thru | 37.59 | mpdecimal | 90.79 | **2.42×** | Rc2 | 256÷64 |
| c | div | XD | P-gen | arm64 | thru | 29.90 | mpdecimal | 154.98 | **5.18×** | Rc2 | Cowlishaw signature (CD 59 < WD 87 < XD 144) |
| c | div | ET | P-gen | arm64 | thru | 8.26 | mpdecimal | 63.32 | **7.67×** | Rc2 | libmpdec has no exact early-out |
| c | div | PT | P-gen | arm64 | thru | 3.12 | mpdecimal | 50.22 | **16.10×** | Rc2 | **d128's biggest divide win vs libmpdec** |

<!-- END GENERATED div-rel-c -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-c-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | div | CD | P-gen | x86_64 | thru | 78.30 | libbid | 80.72 | **1.03×** | xRc2 |  |
| c | div | WD | P-gen | x86_64 | thru | 98.07 | libbid | 80.21 | **0.82×** | xRc2 |  |
| c | div | XD | P-gen | x86_64 | thru | 86.69 | libbid | 81.28 | **0.94×** | xRc2 |  |
| c | div | ET | P-gen | x86_64 | thru | 27.33 | libbid | 29.08 | **1.06×** | xRc2 |  |
| c | div | PT | P-gen | x86_64 | thru | 9.82 | libbid | 29.57 | **3.01×** | xRc2 |  |
| c | div | CD | P-gen | x86_64 | thru | 78.30 | decQuad | 137.28 | **1.75×** | xRc2 |  |
| c | div | WD | P-gen | x86_64 | thru | 98.07 | decQuad | 236.66 | **2.41×** | xRc2 |  |
| c | div | XD | P-gen | x86_64 | thru | 86.69 | decQuad | 371.96 | **4.29×** | xRc2 |  |
| c | div | ET | P-gen | x86_64 | thru | 27.33 | decQuad | 98.98 | **3.62×** | xRc2 |  |
| c | div | PT | P-gen | x86_64 | thru | 9.82 | decQuad | 81.77 | **8.33×** | xRc2 |  |
| c | div | CD | P-gen | x86_64 | thru | 78.30 | mpdecimal | 154.50 | **1.97×** | xRc2 |  |
| c | div | WD | P-gen | x86_64 | thru | 98.07 | mpdecimal | 273.44 | **2.79×** | xRc2 |  |
| c | div | XD | P-gen | x86_64 | thru | 86.69 | mpdecimal | 350.09 | **4.04×** | xRc2 |  |
| c | div | ET | P-gen | x86_64 | thru | 27.33 | mpdecimal | 150.31 | **5.50×** | xRc2 |  |
| c | div | PT | P-gen | x86_64 | thru | 9.82 | mpdecimal | 101.45 | **10.33×** | xRc2 |  |

<!-- END GENERATED div-rel-c-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-c -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | fma | FN | FMA | arm64 | thru | 76.23 | libbid | 81.90 | **1.07×** | Rc2 |  |
| c | fma | FF | FMA | arm64 | thru | 39.38 | libbid | 58.40 | **1.48×** | Rc2 |  |
| c | fma | FN | FMA | arm64 | thru | 76.23 | decQuad | 61.83 | **0.81×** | Rc2 |  |
| c | fma | FF | FMA | arm64 | thru | 39.38 | decQuad | 71.41 | **1.81×** | Rc2 |  |
| c | fma | FN | FMA | arm64 | thru | 76.23 | mpdecimal | 89.73 | **1.18×** | Rc2 |  |
| c | fma | FF | FMA | arm64 | thru | 39.38 | mpdecimal | 147.52 | **3.75×** | Rc2 |  |

<!-- END GENERATED fma-rel-c -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-c-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | fma | FN | FMA | x86_64 | thru | 150.73 | libbid | 156.29 | **1.04×** | xRc2 |  |
| c | fma | FF | FMA | x86_64 | thru | 87.74 | libbid | 117.61 | **1.34×** | xRc2 |  |
| c | fma | FN | FMA | x86_64 | thru | 150.73 | decQuad | 145.89 | **0.97×** | xRc2 |  |
| c | fma | FF | FMA | x86_64 | thru | 87.74 | decQuad | 149.04 | **1.70×** | xRc2 |  |
| c | fma | FN | FMA | x86_64 | thru | 150.73 | mpdecimal | 254.36 | **1.69×** | xRc2 |  |
| c | fma | FF | FMA | x86_64 | thru | 87.74 | mpdecimal | 330.56 | **3.77×** | xRc2 |  |

<!-- END GENERATED fma-rel-c-x86 -->

</div>
