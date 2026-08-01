---
layout: default
permalink: /benchmark/vs-java.html
title: "Java Benchmark Results — Decimal128"
description: "decimal128 in Java, measured against the alternatives available to it — a realistic financial mix (P-fin) plus per-operation band characterization, with explicit ratios."
heading: "Java Benchmark Results"
---

<div class="whitepaper" markdown="1">

<p class="whitepaper-meta">Living document — as-measured results. Category codes, profiles, modes &amp; method: <a href="key.html">Benchmark Key</a>.</p>

This is the **Java** view of decimal128 **as-measured**, band by band, with explicit ratios. It opens with the realistic financial-mix (**P-fin**) headline, then the per-operation band characterization (**P-gen**) and FMA. In Java, d128 is measured against its in-language idiom peer **`BigDecimal`**, with the **libbid** universal reference on the full-width bands. It is **data only** — the categories, magnitude profiles, units, and methodology are defined in the [Benchmark Key](key.html) (and, authoritatively, `BenchmarkMatrix.md`). The cross-port d128 band-shape matrices (all ports, no alternatives) live in [Port-Comparison Benchmark Results](port-compare.html); the full index of per-language pages is on the [Benchmarks](/benchmarks.html) hub.

## Summary — Ratio Range by Operation

The ratio for Java's idiom peer on x86_64 (Intel i9-9880H): `ratio = BigDecimal / Miguel` (&gt; 1× ⇒ d128 faster), broken out by operation.

| | Add | Subtract | Multiply | Divide |
|---|---|---|---|---|
| ratio = BigDecimal / Miguel | 3× | 4× | 3× | 1.8× – 60× |

## FinMix — realistic financial mix (P-fin)

The headline: one realistic 64-bit financial operation mix — a `MIX` add/sub stream, mul `CP`/`WP`, div `CD`/`WD`/`ET`/`PT` — `ratio = alt / Miguel` (&gt; 1 ⇒ d128 faster). This is the profile closest to real financial code.

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED pfin-rel-java -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | add | MIX | P-fin | arm64 | thru‡ | 4.44 | BigDecimal | 19.56 | **4.41×** | Rjasw2 | compact idiom peer |
| java | sub | MIX | P-fin | arm64 | thru‡ | 5.40 | BigDecimal | 22.61 | **4.19×** | Rjasw2 | compact idiom peer |
| java | mul | CP | P-fin | arm64 | thru‡ | 4.99 | BigDecimal | 12.39 | **2.48×** | Rjasw2 | compact idiom peer |
| java | mul | WP | P-fin | arm64 | thru‡ | 30.91 | BigDecimal | 60.23 | **1.95×** | Rjasw2 | compact idiom peer |
| java | div | CD | P-fin | arm64 | thru‡ | 36.75 | BigDecimal | 141.22 | **3.84×** | Rjasw2 | compact idiom peer |
| java | div | WD | P-fin | arm64 | thru‡ | 46.50 | BigDecimal | 91.87 | **1.98×** | Rjasw2 | compact idiom peer |
| java | div | ET | P-fin | arm64 | thru‡ | 13.36 | BigDecimal | 498.45 | **37.31×** | Rjasw2 | compact idiom peer |
| java | div | PT | P-fin | arm64 | thru‡ | 9.98 | BigDecimal | 476.14 | **47.71×** | Rjasw2 | compact idiom peer |

<!-- END GENERATED pfin-rel-java -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-java-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | add | MIX | P-fin | x86_64 | thru‡ | 9.31 | BigDecimal | 47.78 | **5.13×** | xRjasw2 | compact idiom peer |
| java | sub | MIX | P-fin | x86_64 | thru‡ | 15.79 | BigDecimal | 58.50 | **3.70×** | xRjasw2 | compact idiom peer |
| java | mul | CP | P-fin | x86_64 | thru‡ | 11.55 | BigDecimal | 41.58 | **3.60×** | xRjasw2 | compact idiom peer |
| java | mul | WP | P-fin | x86_64 | thru‡ | 47.84 | BigDecimal | 151.76 | **3.17×** | xRjasw2 | compact idiom peer |
| java | div | CD | P-fin | x86_64 | thru‡ | 96.97 | BigDecimal | 392.22 | **4.04×** | xRjasw2 | compact idiom peer |
| java | div | WD | P-fin | x86_64 | thru‡ | 120.32 | BigDecimal | 210.18 | **1.75×** | xRjasw2 | compact idiom peer |
| java | div | ET | P-fin | x86_64 | thru‡ | 47.29 | BigDecimal | 1374.24 | **29.06×** | xRjasw2 | compact idiom peer |
| java | div | PT | P-fin | x86_64 | thru‡ | 23.06 | BigDecimal | 1318.70 | **57.19×** | xRjasw2 | compact idiom peer |

<!-- END GENERATED pfin-rel-java-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-java -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | add | SQss | P-gen | arm64 | thru‡ | 3.98 | BigDecimal | 18.22 | **4.58×** | Rjasw2 | compact idiom peer |
| java | add | SQos | P-gen | arm64 | thru‡ | 4.93 | BigDecimal | 21.58 | **4.38×** | Rjasw2 | compact idiom peer |
| java | add | NQss | P-gen | arm64 | thru‡ | 8.04 | BigDecimal | 29.94 | **3.72×** | Rjasw2 | compact idiom peer |
| java | add | NQos | P-gen | arm64 | thru‡ | 9.32 | BigDecimal | 35.34 | **3.79×** | Rjasw2 | compact idiom peer |
| java | add | MQss | P-gen | arm64 | thru‡ | 11.88 | BigDecimal | 29.66 | **2.50×** | Rjasw2 | compact idiom peer |
| java | add | MQos | P-gen | arm64 | thru‡ | 30.02 | BigDecimal | 36.31 | **1.21×** | Rjasw2 | compact idiom peer |
| java | add | OQss | P-gen | arm64 | thru‡ | 21.61 | BigDecimal | 78.91 | **3.65×** | Rjasw2 | compact idiom peer |
| java | add | OQos | P-gen | arm64 | thru‡ | 46.52 | BigDecimal | 81.39 | **1.75×** | Rjasw2 | compact idiom peer |
| java | add | FQss | P-gen | arm64 | thru‡ | 17.72 | BigDecimal | 76.90 | **4.34×** | Rjasw2 | compact idiom peer |
| java | add | FQos | P-gen | arm64 | thru‡ | 33.72 | BigDecimal | 91.30 | **2.71×** | Rjasw2 | compact idiom peer |

<!-- END GENERATED add-rel-java -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-java-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | add | SQss | P-gen | x86_64 | thru‡ | 6.74 | BigDecimal | 46.21 | **6.86×** | xRjasw2 | compact idiom peer |
| java | add | SQos | P-gen | x86_64 | thru‡ | 15.83 | BigDecimal | 55.32 | **3.49×** | xRjasw2 | compact idiom peer |
| java | add | NQss | P-gen | x86_64 | thru‡ | 18.42 | BigDecimal | 72.20 | **3.92×** | xRjasw2 | compact idiom peer |
| java | add | NQos | P-gen | x86_64 | thru‡ | 26.10 | BigDecimal | 81.16 | **3.11×** | xRjasw2 | compact idiom peer |
| java | add | MQss | P-gen | x86_64 | thru‡ | 23.64 | BigDecimal | 74.76 | **3.16×** | xRjasw2 | compact idiom peer |
| java | add | MQos | P-gen | x86_64 | thru‡ | 37.61 | BigDecimal | 85.60 | **2.28×** | xRjasw2 | compact idiom peer |
| java | add | OQss | P-gen | x86_64 | thru‡ | 52.12 | BigDecimal | 161.01 | **3.09×** | xRjasw2 | compact idiom peer |
| java | add | OQos | P-gen | x86_64 | thru‡ | 67.21 | BigDecimal | 165.22 | **2.46×** | xRjasw2 | compact idiom peer |
| java | add | FQss | P-gen | x86_64 | thru‡ | 34.70 | BigDecimal | 176.68 | **5.09×** | xRjasw2 | compact idiom peer |
| java | add | FQos | P-gen | x86_64 | thru‡ | 44.10 | BigDecimal | 203.74 | **4.62×** | xRjasw2 | compact idiom peer |

<!-- END GENERATED add-rel-java-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-java -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | sub | SQss | P-gen | arm64 | thru‡ | 4.90 | BigDecimal | 25.19 | **5.14×** | Rjasw2 | compact idiom peer |
| java | sub | SQos | P-gen | arm64 | thru‡ | 4.18 | BigDecimal | 22.35 | **5.35×** | Rjasw2 | compact idiom peer |
| java | sub | NQss | P-gen | arm64 | thru‡ | 8.35 | BigDecimal | 39.36 | **4.71×** | Rjasw2 | compact idiom peer |
| java | sub | NQos | P-gen | arm64 | thru‡ | 7.65 | BigDecimal | 34.07 | **4.45×** | Rjasw2 | compact idiom peer |
| java | sub | MQss | P-gen | arm64 | thru‡ | 29.21 | BigDecimal | 39.69 | **1.36×** | Rjasw2 | compact idiom peer |
| java | sub | MQos | P-gen | arm64 | thru‡ | 10.91 | BigDecimal | 33.83 | **3.10×** | Rjasw2 | compact idiom peer |
| java | sub | OQss | P-gen | arm64 | thru‡ | 45.72 | BigDecimal | 87.62 | **1.92×** | Rjasw2 | compact idiom peer |
| java | sub | OQos | P-gen | arm64 | thru‡ | 21.31 | BigDecimal | 82.51 | **3.87×** | Rjasw2 | compact idiom peer |
| java | sub | FQss | P-gen | arm64 | thru‡ | 33.14 | BigDecimal | 98.95 | **2.99×** | Rjasw2 | compact idiom peer |
| java | sub | FQos | P-gen | arm64 | thru‡ | 17.28 | BigDecimal | 84.54 | **4.89×** | Rjasw2 | compact idiom peer |

<!-- END GENERATED sub-rel-java -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-java-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | sub | SQss | P-gen | x86_64 | thru‡ | 14.09 | BigDecimal | 62.35 | **4.43×** | xRjasw2 | compact idiom peer |
| java | sub | SQos | P-gen | x86_64 | thru‡ | 9.64 | BigDecimal | 52.31 | **5.43×** | xRjasw2 | compact idiom peer |
| java | sub | NQss | P-gen | x86_64 | thru‡ | 26.87 | BigDecimal | 86.92 | **3.23×** | xRjasw2 | compact idiom peer |
| java | sub | NQos | P-gen | x86_64 | thru‡ | 18.22 | BigDecimal | 78.73 | **4.32×** | xRjasw2 | compact idiom peer |
| java | sub | MQss | P-gen | x86_64 | thru‡ | 37.16 | BigDecimal | 91.44 | **2.46×** | xRjasw2 | compact idiom peer |
| java | sub | MQos | P-gen | x86_64 | thru‡ | 23.42 | BigDecimal | 83.46 | **3.56×** | xRjasw2 | compact idiom peer |
| java | sub | OQss | P-gen | x86_64 | thru‡ | 66.52 | BigDecimal | 173.44 | **2.61×** | xRjasw2 | compact idiom peer |
| java | sub | OQos | P-gen | x86_64 | thru‡ | 51.03 | BigDecimal | 166.75 | **3.27×** | xRjasw2 | compact idiom peer |
| java | sub | FQss | P-gen | x86_64 | thru‡ | 43.00 | BigDecimal | 209.57 | **4.87×** | xRjasw2 | compact idiom peer |
| java | sub | FQos | P-gen | x86_64 | thru‡ | 33.92 | BigDecimal | 183.87 | **5.42×** | xRjasw2 | compact idiom peer |

<!-- END GENERATED sub-rel-java-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-java -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | mul | CP | P-gen | arm64 | thru‡ | 5.46 | BigDecimal | 12.31 | **2.25×** | Rjasw2 | compact idiom peer |
| java | mul | WP | P-gen | arm64 | thru‡ | 30.42 | BigDecimal | 58.01 | **1.91×** | Rjasw2 | compact idiom peer |
| java | mul | XP | P-gen | arm64 | thru‡ | 45.83 | BigDecimal | 165.43 | **3.61×** | Rjasw2 | compact idiom peer |

<!-- END GENERATED mul-rel-java -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-java-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | mul | CP | P-gen | x86_64 | thru‡ | 13.18 | BigDecimal | 39.29 | **2.98×** | xRjasw2 | compact idiom peer |
| java | mul | WP | P-gen | x86_64 | thru‡ | 43.99 | BigDecimal | 146.94 | **3.34×** | xRjasw2 | compact idiom peer |
| java | mul | XP | P-gen | x86_64 | thru‡ | 63.42 | BigDecimal | 267.06 | **4.21×** | xRjasw2 | compact idiom peer |

<!-- END GENERATED mul-rel-java-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-java -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | div | CD | P-gen | arm64 | thru‡ | 31.73 | BigDecimal | 141.36 | **4.46×** | Rjasw2 | compact idiom peer |
| java | div | WD | P-gen | arm64 | thru‡ | 48.72 | BigDecimal | 102.98 | **2.11×** | Rjasw2 | compact idiom peer |
| java | div | XD | P-gen | arm64 | thru‡ | 50.17 | BigDecimal | 234.08 | **4.67×** | Rjasw2 | compact idiom peer |
| java | div | ET | P-gen | arm64 | thru‡ | 14.21 | BigDecimal | 426.20 | **29.99×** | Rjasw2 | compact idiom peer |
| java | div | PT | P-gen | arm64 | thru‡ | 11.33 | BigDecimal | 393.58 | **34.74×** | Rjasw2 | compact idiom peer |

<!-- END GENERATED div-rel-java -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-java-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | div | CD | P-gen | x86_64 | thru‡ | 88.17 | BigDecimal | 372.47 | **4.22×** | xRjasw2 | compact idiom peer |
| java | div | WD | P-gen | x86_64 | thru‡ | 115.91 | BigDecimal | 254.76 | **2.20×** | xRjasw2 | compact idiom peer |
| java | div | XD | P-gen | x86_64 | thru‡ | 124.04 | BigDecimal | 336.06 | **2.71×** | xRjasw2 | compact idiom peer |
| java | div | ET | P-gen | x86_64 | thru‡ | 45.41 | BigDecimal | 1086.24 | **23.92×** | xRjasw2 | compact idiom peer |
| java | div | PT | P-gen | x86_64 | thru‡ | 23.34 | BigDecimal | 1087.55 | **46.60×** | xRjasw2 | compact idiom peer |

<!-- END GENERATED div-rel-java-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-java -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | fma | FN | FMA | arm64 | thru‡ | 100.71 | - | - | - | Rjasw2 |  |
| java | fma | FF | FMA | arm64 | thru‡ | 71.66 | - | - | - | Rjasw2 |  |

<!-- END GENERATED fma-rel-java -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-java-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | fma | FN | FMA | x86_64 | thru‡ | 200.34 | - | - | - | xRjasw2 |  |
| java | fma | FF | FMA | x86_64 | thru‡ | 168.33 | - | - | - | xRjasw2 |  |

<!-- END GENERATED fma-rel-java-x86 -->

</div>
