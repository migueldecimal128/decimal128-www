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
| ratio = BigDecimal / Miguel | 4× | 4× | 3× | 1.9× – 51× |

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
| kotlin | add | MIX | P-fin | x86_64 | thru‡ | 17.01 | BigDecimal | 68.32 | **4.02×** | xRkosw2 | compact idiom peer |
| kotlin | sub | MIX | P-fin | x86_64 | thru‡ | 22.95 | BigDecimal | 87.69 | **3.82×** | xRkosw2 | compact idiom peer |
| kotlin | mul | CP | P-fin | x86_64 | thru‡ | 15.82 | BigDecimal | 53.95 | **3.41×** | xRkosw2 | compact idiom peer |
| kotlin | mul | WP | P-fin | x86_64 | thru‡ | 65.20 | BigDecimal | 209.30 | **3.21×** | xRkosw2 | compact idiom peer |
| kotlin | div | CD | P-fin | x86_64 | thru‡ | 131.31 | BigDecimal | 527.45 | **4.02×** | xRkosw2 | compact idiom peer |
| kotlin | div | WD | P-fin | x86_64 | thru‡ | 162.38 | BigDecimal | 300.21 | **1.85×** | xRkosw2 | compact idiom peer |
| kotlin | div | ET | P-fin | x86_64 | thru‡ | 66.93 | BigDecimal | 1822.78 | **27.23×** | xRkosw2 | compact idiom peer |
| kotlin | div | PT | P-fin | x86_64 | thru‡ | 34.67 | BigDecimal | 1757.49 | **50.69×** | xRkosw2 | compact idiom peer |

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
| kotlin | add | SQss | P-gen | x86_64 | thru‡ | 14.73 | BigDecimal | 63.75 | **4.33×** | xRkosw2 | compact idiom peer |
| kotlin | add | SQos | P-gen | x86_64 | thru‡ | 23.50 | BigDecimal | 75.59 | **3.22×** | xRkosw2 | compact idiom peer |
| kotlin | add | NQss | P-gen | x86_64 | thru‡ | 24.56 | BigDecimal | 102.39 | **4.17×** | xRkosw2 | compact idiom peer |
| kotlin | add | NQos | P-gen | x86_64 | thru‡ | 32.30 | BigDecimal | 112.49 | **3.48×** | xRkosw2 | compact idiom peer |
| kotlin | add | MQss | P-gen | x86_64 | thru‡ | 33.27 | BigDecimal | 108.23 | **3.25×** | xRkosw2 | compact idiom peer |
| kotlin | add | MQos | P-gen | x86_64 | thru‡ | 51.28 | BigDecimal | 120.87 | **2.36×** | xRkosw2 | compact idiom peer |
| kotlin | add | OQss | P-gen | x86_64 | thru‡ | 70.56 | BigDecimal | 216.17 | **3.06×** | xRkosw2 | compact idiom peer |
| kotlin | add | OQos | P-gen | x86_64 | thru‡ | 101.24 | BigDecimal | 215.61 | **2.13×** | xRkosw2 | compact idiom peer |
| kotlin | add | FQss | P-gen | x86_64 | thru‡ | 43.35 | BigDecimal | 242.44 | **5.59×** | xRkosw2 | compact idiom peer |
| kotlin | add | FQos | P-gen | x86_64 | thru‡ | 48.66 | BigDecimal | 265.04 | **5.45×** | xRkosw2 | compact idiom peer |

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
| kotlin | sub | SQss | P-gen | x86_64 | thru‡ | 18.91 | BigDecimal | 89.09 | **4.71×** | xRkosw2 | compact idiom peer |
| kotlin | sub | SQos | P-gen | x86_64 | thru‡ | 13.99 | BigDecimal | 76.44 | **5.46×** | xRkosw2 | compact idiom peer |
| kotlin | sub | NQss | P-gen | x86_64 | thru‡ | 31.74 | BigDecimal | 121.25 | **3.82×** | xRkosw2 | compact idiom peer |
| kotlin | sub | NQos | P-gen | x86_64 | thru‡ | 27.44 | BigDecimal | 121.76 | **4.44×** | xRkosw2 | compact idiom peer |
| kotlin | sub | MQss | P-gen | x86_64 | thru‡ | 47.73 | BigDecimal | 127.70 | **2.68×** | xRkosw2 | compact idiom peer |
| kotlin | sub | MQos | P-gen | x86_64 | thru‡ | 33.69 | BigDecimal | 120.10 | **3.56×** | xRkosw2 | compact idiom peer |
| kotlin | sub | OQss | P-gen | x86_64 | thru‡ | 106.02 | BigDecimal | 236.51 | **2.23×** | xRkosw2 | compact idiom peer |
| kotlin | sub | OQos | P-gen | x86_64 | thru‡ | 73.52 | BigDecimal | 225.62 | **3.07×** | xRkosw2 | compact idiom peer |
| kotlin | sub | FQss | P-gen | x86_64 | thru‡ | 54.19 | BigDecimal | 273.80 | **5.05×** | xRkosw2 | compact idiom peer |
| kotlin | sub | FQos | P-gen | x86_64 | thru‡ | 41.09 | BigDecimal | 248.74 | **6.05×** | xRkosw2 | compact idiom peer |

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
| kotlin | mul | CP | P-gen | x86_64 | thru‡ | 17.36 | BigDecimal | 51.64 | **2.97×** | xRkosw2 | compact idiom peer |
| kotlin | mul | WP | P-gen | x86_64 | thru‡ | 64.37 | BigDecimal | 210.28 | **3.27×** | xRkosw2 | compact idiom peer |
| kotlin | mul | XP | P-gen | x86_64 | thru‡ | 110.91 | BigDecimal | 372.11 | **3.36×** | xRkosw2 | compact idiom peer |

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
| kotlin | div | CD | P-gen | x86_64 | thru‡ | 111.07 | BigDecimal | 505.28 | **4.55×** | xRkosw2 | compact idiom peer |
| kotlin | div | WD | P-gen | x86_64 | thru‡ | 170.68 | BigDecimal | 338.13 | **1.98×** | xRkosw2 | compact idiom peer |
| kotlin | div | XD | P-gen | x86_64 | thru‡ | 194.15 | BigDecimal | 452.63 | **2.33×** | xRkosw2 | compact idiom peer |
| kotlin | div | ET | P-gen | x86_64 | thru‡ | 54.85 | BigDecimal | 1710.40 | **31.18×** | xRkosw2 | compact idiom peer |
| kotlin | div | PT | P-gen | x86_64 | thru‡ | 31.38 | BigDecimal | 1584.28 | **50.49×** | xRkosw2 | compact idiom peer |

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
| kotlin | fma | FN | FMA | x86_64 | thru‡ | 290.31 | - | - | - | xRkosw2 |  |
| kotlin | fma | FF | FMA | x86_64 | thru‡ | 229.52 | - | - | - | xRkosw2 |  |

<!-- END GENERATED fma-rel-kotlin-x86 -->

</div>
