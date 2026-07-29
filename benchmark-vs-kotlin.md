---
layout: default
permalink: /benchmark/vs-kotlin.html
title: "Kotlin Benchmark Results — Decimal128"
description: "decimal128 in Kotlin, measured against the alternatives available to it — a realistic financial mix (P-fin) plus per-operation band characterization, with explicit ratios."
heading: "Kotlin Benchmark Results"
---

<div class="whitepaper" markdown="1">

<p class="whitepaper-meta">Living document — as-measured results. Category codes, profiles, modes &amp; method: <a href="key.html">Benchmark Key</a>.</p>

This is the **Kotlin** view of decimal128 **as-measured**, band by band, with explicit ratios. It opens with the realistic financial-mix (**P-fin**) headline, then the per-operation band characterization (**P-gen**) and FMA. In Kotlin, d128 is measured against its in-language idiom peer **`BigDecimal`**, with the **libbid** universal reference on the full-width bands. It is **data only** — the categories, magnitude profiles, units, and methodology are defined in the [Benchmark Key](key.html) (and, authoritatively, `BenchmarkMatrix.md`). The cross-port d128 band-shape matrices (all ports, no alternatives) live in [Port-Comparison Benchmark Results](port-compare.html); the full index of per-language pages is on the [Benchmarks](/benchmarks.html) hub.

## Summary — Ratio Range by Operation

The ratio for Kotlin's idiom peer on x86_64 (Intel i9-9880H): `ratio = BigDecimal / Miguel` (&gt; 1× ⇒ d128 faster), broken out by operation.

| | Add | Subtract | Multiply | Divide |
|---|---|---|---|---|
| ratio = BigDecimal / Miguel | 2.7× | 4× | 3× – 4× | 1.8× – 55× |

## FinMix — realistic financial mix (P-fin)

The headline: one realistic 64-bit financial operation mix — a `MIX` add/sub stream, mul `CP`/`WP`, div `CD`/`WD`/`ET`/`PT` — `ratio = alt / Miguel` (&gt; 1 ⇒ d128 faster). This is the profile closest to real financial code.

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED pfin-rel-kotlin -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | add | MIX | P-fin | arm64 | thru‡ | 4.89 | BigDecimal | 20.24 | **4.14×** | Rkosw2 | compact idiom peer |
| kotlin | sub | MIX | P-fin | arm64 | thru‡ | 6.38 | BigDecimal | 24.81 | **3.89×** | Rkosw2 | compact idiom peer |
| kotlin | mul | CP | P-fin | arm64 | thru‡ | 5.40 | BigDecimal | 12.56 | **2.33×** | Rkosw2 | compact idiom peer |
| kotlin | mul | WP | P-fin | arm64 | thru‡ | 30.03 | BigDecimal | 67.12 | **2.24×** | Rkosw2 | compact idiom peer |
| kotlin | div | CD | P-fin | arm64 | thru‡ | 39.46 | BigDecimal | 140.61 | **3.56×** | Rkosw2 | compact idiom peer |
| kotlin | div | WD | P-fin | arm64 | thru‡ | 52.20 | BigDecimal | 111.89 | **2.14×** | Rkosw2 | compact idiom peer |
| kotlin | div | ET | P-fin | arm64 | thru‡ | 18.24 | BigDecimal | 507.64 | **27.83×** | Rkosw2 | compact idiom peer |
| kotlin | div | PT | P-fin | arm64 | thru‡ | 15.15 | BigDecimal | 488.01 | **32.21×** | Rkosw2 | compact idiom peer |

<!-- END GENERATED pfin-rel-kotlin -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-kotlin-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | add | MIX | P-fin | x86_64 | thru‡ | 13.62 | BigDecimal | 52.70 | **3.87×** | xRkosw2 | compact idiom peer |
| kotlin | sub | MIX | P-fin | x86_64 | thru‡ | 18.47 | BigDecimal | 62.54 | **3.39×** | xRkosw2 | compact idiom peer |
| kotlin | mul | CP | P-fin | x86_64 | thru‡ | 12.98 | BigDecimal | 44.19 | **3.40×** | xRkosw2 | compact idiom peer |
| kotlin | mul | WP | P-fin | x86_64 | thru‡ | 48.50 | BigDecimal | 155.52 | **3.21×** | xRkosw2 | compact idiom peer |
| kotlin | div | CD | P-fin | x86_64 | thru‡ | 115.81 | BigDecimal | 431.06 | **3.72×** | xRkosw2 | compact idiom peer |
| kotlin | div | WD | P-fin | x86_64 | thru‡ | 130.47 | BigDecimal | 227.82 | **1.75×** | xRkosw2 | compact idiom peer |
| kotlin | div | ET | P-fin | x86_64 | thru‡ | 52.79 | BigDecimal | 1483.00 | **28.09×** | xRkosw2 | compact idiom peer |
| kotlin | div | PT | P-fin | x86_64 | thru‡ | 27.48 | BigDecimal | 1412.19 | **51.39×** | xRkosw2 | compact idiom peer |

<!-- END GENERATED pfin-rel-kotlin-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-kotlin -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | add | SQss | P-gen | arm64 | thru‡ | 4.35 | BigDecimal | 18.63 | **4.28×** | Rkosw2 | compact idiom peer |
| kotlin | add | SQos | P-gen | arm64 | thru‡ | 6.19 | BigDecimal | 21.41 | **3.46×** | Rkosw2 | compact idiom peer |
| kotlin | add | NQss | P-gen | arm64 | thru‡ | 8.88 | BigDecimal | 29.82 | **3.36×** | Rkosw2 | compact idiom peer |
| kotlin | add | NQos | P-gen | arm64 | thru‡ | 9.92 | BigDecimal | 30.52 | **3.08×** | Rkosw2 | compact idiom peer |
| kotlin | add | MQss | P-gen | arm64 | thru‡ | 13.86 | BigDecimal | 29.88 | **2.16×** | Rkosw2 | compact idiom peer |
| kotlin | add | MQos | P-gen | arm64 | thru‡ | 27.28 | BigDecimal | 30.51 | **1.12×** | Rkosw2 | compact idiom peer |
| kotlin | add | OQss | P-gen | arm64 | thru‡ | 24.97 | BigDecimal | 72.04 | **2.89×** | Rkosw2 | compact idiom peer |
| kotlin | add | OQos | P-gen | arm64 | thru‡ | 44.47 | BigDecimal | 75.38 | **1.70×** | Rkosw2 | compact idiom peer |
| kotlin | add | FQss | P-gen | arm64 | thru‡ | 16.52 | BigDecimal | 75.55 | **4.57×** | Rkosw2 | compact idiom peer |
| kotlin | add | FQos | P-gen | arm64 | thru‡ | 28.76 | BigDecimal | 84.90 | **2.95×** | Rkosw2 | compact idiom peer |

<!-- END GENERATED add-rel-kotlin -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-kotlin-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | add | SQss | P-gen | x86_64 | thru‡ | 10.67 | BigDecimal | 49.59 | **4.65×** | xRkosw2 | compact idiom peer |
| kotlin | add | SQos | P-gen | x86_64 | thru‡ | 16.00 | BigDecimal | 57.16 | **3.57×** | xRkosw2 | compact idiom peer |
| kotlin | add | NQss | P-gen | x86_64 | thru‡ | 16.64 | BigDecimal | 73.83 | **4.44×** | xRkosw2 | compact idiom peer |
| kotlin | add | NQos | P-gen | x86_64 | thru‡ | 23.28 | BigDecimal | 83.34 | **3.58×** | xRkosw2 | compact idiom peer |
| kotlin | add | MQss | P-gen | x86_64 | thru‡ | 23.78 | BigDecimal | 76.89 | **3.23×** | xRkosw2 | compact idiom peer |
| kotlin | add | MQos | P-gen | x86_64 | thru‡ | 38.78 | BigDecimal | 83.90 | **2.16×** | xRkosw2 | compact idiom peer |
| kotlin | add | OQss | P-gen | x86_64 | thru‡ | 57.57 | BigDecimal | 173.17 | **3.01×** | xRkosw2 | compact idiom peer |
| kotlin | add | OQos | P-gen | x86_64 | thru‡ | 82.83 | BigDecimal | 169.07 | **2.04×** | xRkosw2 | compact idiom peer |
| kotlin | add | FQss | P-gen | x86_64 | thru‡ | 34.24 | BigDecimal | 174.95 | **5.11×** | xRkosw2 | compact idiom peer |
| kotlin | add | FQos | P-gen | x86_64 | thru‡ | 41.62 | BigDecimal | 199.60 | **4.80×** | xRkosw2 | compact idiom peer |

<!-- END GENERATED add-rel-kotlin-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-kotlin -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | sub | SQss | P-gen | arm64 | thru‡ | 5.20 | BigDecimal | 22.48 | **4.32×** | Rkosw2 | compact idiom peer |
| kotlin | sub | SQos | P-gen | arm64 | thru‡ | 3.66 | BigDecimal | 22.28 | **6.09×** | Rkosw2 | compact idiom peer |
| kotlin | sub | NQss | P-gen | arm64 | thru‡ | 9.35 | BigDecimal | 34.26 | **3.66×** | Rkosw2 | compact idiom peer |
| kotlin | sub | NQos | P-gen | arm64 | thru‡ | 8.70 | BigDecimal | 34.24 | **3.94×** | Rkosw2 | compact idiom peer |
| kotlin | sub | MQss | P-gen | arm64 | thru‡ | 27.38 | BigDecimal | 33.52 | **1.22×** | Rkosw2 | compact idiom peer |
| kotlin | sub | MQos | P-gen | arm64 | thru‡ | 13.23 | BigDecimal | 33.62 | **2.54×** | Rkosw2 | compact idiom peer |
| kotlin | sub | OQss | P-gen | arm64 | thru‡ | 43.18 | BigDecimal | 83.36 | **1.93×** | Rkosw2 | compact idiom peer |
| kotlin | sub | OQos | P-gen | arm64 | thru‡ | 25.00 | BigDecimal | 80.21 | **3.21×** | Rkosw2 | compact idiom peer |
| kotlin | sub | FQss | P-gen | arm64 | thru‡ | 28.39 | BigDecimal | 89.90 | **3.17×** | Rkosw2 | compact idiom peer |
| kotlin | sub | FQos | P-gen | arm64 | thru‡ | 18.11 | BigDecimal | 81.90 | **4.52×** | Rkosw2 | compact idiom peer |

<!-- END GENERATED sub-rel-kotlin -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-kotlin-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | sub | SQss | P-gen | x86_64 | thru‡ | 14.89 | BigDecimal | 66.75 | **4.48×** | xRkosw2 | compact idiom peer |
| kotlin | sub | SQos | P-gen | x86_64 | thru‡ | 10.03 | BigDecimal | 56.12 | **5.60×** | xRkosw2 | compact idiom peer |
| kotlin | sub | NQss | P-gen | x86_64 | thru‡ | 25.07 | BigDecimal | 95.07 | **3.79×** | xRkosw2 | compact idiom peer |
| kotlin | sub | NQos | P-gen | x86_64 | thru‡ | 17.45 | BigDecimal | 83.35 | **4.78×** | xRkosw2 | compact idiom peer |
| kotlin | sub | MQss | P-gen | x86_64 | thru‡ | 41.05 | BigDecimal | 98.85 | **2.41×** | xRkosw2 | compact idiom peer |
| kotlin | sub | MQos | P-gen | x86_64 | thru‡ | 25.73 | BigDecimal | 88.19 | **3.43×** | xRkosw2 | compact idiom peer |
| kotlin | sub | OQss | P-gen | x86_64 | thru‡ | 82.85 | BigDecimal | 175.29 | **2.12×** | xRkosw2 | compact idiom peer |
| kotlin | sub | OQos | P-gen | x86_64 | thru‡ | 62.21 | BigDecimal | 176.50 | **2.84×** | xRkosw2 | compact idiom peer |
| kotlin | sub | FQss | P-gen | x86_64 | thru‡ | 42.91 | BigDecimal | 205.24 | **4.78×** | xRkosw2 | compact idiom peer |
| kotlin | sub | FQos | P-gen | x86_64 | thru‡ | 35.15 | BigDecimal | 178.29 | **5.07×** | xRkosw2 | compact idiom peer |

<!-- END GENERATED sub-rel-kotlin-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-kotlin -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | mul | CP | P-gen | arm64 | thru‡ | 5.54 | BigDecimal | 11.88 | **2.14×** | Rkosw2 | compact idiom peer |
| kotlin | mul | WP | P-gen | arm64 | thru‡ | 29.88 | BigDecimal | 64.15 | **2.15×** | Rkosw2 | compact idiom peer |
| kotlin | mul | XP | P-gen | arm64 | thru‡ | 42.63 | BigDecimal | 160.46 | **3.76×** | Rkosw2 | compact idiom peer |

<!-- END GENERATED mul-rel-kotlin -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-kotlin-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | mul | CP | P-gen | x86_64 | thru‡ | 13.34 | BigDecimal | 40.62 | **3.04×** | xRkosw2 | compact idiom peer |
| kotlin | mul | WP | P-gen | x86_64 | thru‡ | 51.92 | BigDecimal | 163.59 | **3.15×** | xRkosw2 | compact idiom peer |
| kotlin | mul | XP | P-gen | x86_64 | thru‡ | 96.56 | BigDecimal | 286.05 | **2.96×** | xRkosw2 | compact idiom peer |

<!-- END GENERATED mul-rel-kotlin-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-kotlin -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | div | CD | P-gen | arm64 | thru‡ | 34.17 | BigDecimal | 144.51 | **4.23×** | Rkosw2 | compact idiom peer |
| kotlin | div | WD | P-gen | arm64 | thru‡ | 49.78 | BigDecimal | 124.07 | **2.49×** | Rkosw2 | compact idiom peer |
| kotlin | div | XD | P-gen | arm64 | thru‡ | 52.47 | BigDecimal | 220.19 | **4.20×** | Rkosw2 | compact idiom peer |
| kotlin | div | ET | P-gen | arm64 | thru‡ | 19.76 | BigDecimal | 435.10 | **22.02×** | Rkosw2 | compact idiom peer |
| kotlin | div | PT | P-gen | arm64 | thru‡ | 11.71 | BigDecimal | 404.25 | **34.52×** | Rkosw2 | compact idiom peer |

<!-- END GENERATED div-rel-kotlin -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-kotlin-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | div | CD | P-gen | x86_64 | thru‡ | 97.97 | BigDecimal | 379.91 | **3.88×** | xRkosw2 | compact idiom peer |
| kotlin | div | WD | P-gen | x86_64 | thru‡ | 135.59 | BigDecimal | 259.82 | **1.92×** | xRkosw2 | compact idiom peer |
| kotlin | div | XD | P-gen | x86_64 | thru‡ | 153.35 | BigDecimal | 353.35 | **2.30×** | xRkosw2 | compact idiom peer |
| kotlin | div | ET | P-gen | x86_64 | thru‡ | 49.06 | BigDecimal | 1173.97 | **23.93×** | xRkosw2 | compact idiom peer |
| kotlin | div | PT | P-gen | x86_64 | thru‡ | 26.00 | BigDecimal | 1075.63 | **41.37×** | xRkosw2 | compact idiom peer |

<!-- END GENERATED div-rel-kotlin-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-kotlin -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | fma | FN | FMA | arm64 | thru‡ | 110.65 | - | - | - | Rkosw2 |  |
| kotlin | fma | FF | FMA | arm64 | thru‡ | 89.52 | - | - | - | Rkosw2 |  |

<!-- END GENERATED fma-rel-kotlin -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-kotlin-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | fma | FN | FMA | x86_64 | thru‡ | 235.97 | - | - | - | xRkosw2 |  |
| kotlin | fma | FF | FMA | x86_64 | thru‡ | 178.28 | - | - | - | xRkosw2 |  |

<!-- END GENERATED fma-rel-kotlin-x86 -->

</div>
