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
| java | add | MIX | P-fin | x86_64 | thru‡ | 11.81 | BigDecimal | 63.63 | **5.39×** | xRjasw2 | compact idiom peer |
| java | sub | MIX | P-fin | x86_64 | thru‡ | 19.36 | BigDecimal | 80.62 | **4.16×** | xRjasw2 | compact idiom peer |
| java | mul | CP | P-fin | x86_64 | thru‡ | 13.75 | BigDecimal | 49.56 | **3.60×** | xRjasw2 | compact idiom peer |
| java | mul | WP | P-fin | x86_64 | thru‡ | 53.01 | BigDecimal | 207.41 | **3.91×** | xRjasw2 | compact idiom peer |
| java | div | CD | P-fin | x86_64 | thru‡ | 108.15 | BigDecimal | 512.67 | **4.74×** | xRjasw2 | compact idiom peer |
| java | div | WD | P-fin | x86_64 | thru‡ | 144.96 | BigDecimal | 289.27 | **2.00×** | xRjasw2 | compact idiom peer |
| java | div | ET | P-fin | x86_64 | thru‡ | 53.15 | BigDecimal | 1792.64 | **33.73×** | xRjasw2 | compact idiom peer |
| java | div | PT | P-fin | x86_64 | thru‡ | 31.45 | BigDecimal | 1725.38 | **54.86×** | xRjasw2 | compact idiom peer |

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
| java | add | SQss | P-gen | x86_64 | thru‡ | 9.60 | BigDecimal | 60.35 | **6.29×** | xRjasw2 | compact idiom peer |
| java | add | SQos | P-gen | x86_64 | thru‡ | 18.85 | BigDecimal | 76.59 | **4.06×** | xRjasw2 | compact idiom peer |
| java | add | NQss | P-gen | x86_64 | thru‡ | 21.81 | BigDecimal | 102.12 | **4.68×** | xRjasw2 | compact idiom peer |
| java | add | NQos | P-gen | x86_64 | thru‡ | 25.04 | BigDecimal | 111.77 | **4.46×** | xRjasw2 | compact idiom peer |
| java | add | MQss | P-gen | x86_64 | thru‡ | 26.70 | BigDecimal | 101.81 | **3.81×** | xRjasw2 | compact idiom peer |
| java | add | MQos | P-gen | x86_64 | thru‡ | 41.48 | BigDecimal | 115.93 | **2.79×** | xRjasw2 | compact idiom peer |
| java | add | OQss | P-gen | x86_64 | thru‡ | 60.65 | BigDecimal | 212.97 | **3.51×** | xRjasw2 | compact idiom peer |
| java | add | OQos | P-gen | x86_64 | thru‡ | 77.85 | BigDecimal | 222.66 | **2.86×** | xRjasw2 | compact idiom peer |
| java | add | FQss | P-gen | x86_64 | thru‡ | 39.66 | BigDecimal | 239.07 | **6.03×** | xRjasw2 | compact idiom peer |
| java | add | FQos | P-gen | x86_64 | thru‡ | 54.32 | BigDecimal | 266.59 | **4.91×** | xRjasw2 | compact idiom peer |

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
| java | sub | SQss | P-gen | x86_64 | thru‡ | 15.90 | BigDecimal | 85.93 | **5.40×** | xRjasw2 | compact idiom peer |
| java | sub | SQos | P-gen | x86_64 | thru‡ | 13.16 | BigDecimal | 74.12 | **5.63×** | xRjasw2 | compact idiom peer |
| java | sub | NQss | P-gen | x86_64 | thru‡ | 23.78 | BigDecimal | 118.65 | **4.99×** | xRjasw2 | compact idiom peer |
| java | sub | NQos | P-gen | x86_64 | thru‡ | 19.38 | BigDecimal | 115.04 | **5.94×** | xRjasw2 | compact idiom peer |
| java | sub | MQss | P-gen | x86_64 | thru‡ | 39.94 | BigDecimal | 123.32 | **3.09×** | xRjasw2 | compact idiom peer |
| java | sub | MQos | P-gen | x86_64 | thru‡ | 24.70 | BigDecimal | 118.46 | **4.80×** | xRjasw2 | compact idiom peer |
| java | sub | OQss | P-gen | x86_64 | thru‡ | 83.12 | BigDecimal | 235.29 | **2.83×** | xRjasw2 | compact idiom peer |
| java | sub | OQos | P-gen | x86_64 | thru‡ | 62.03 | BigDecimal | 223.94 | **3.61×** | xRjasw2 | compact idiom peer |
| java | sub | FQss | P-gen | x86_64 | thru‡ | 52.97 | BigDecimal | 280.61 | **5.30×** | xRjasw2 | compact idiom peer |
| java | sub | FQos | P-gen | x86_64 | thru‡ | 41.69 | BigDecimal | 243.12 | **5.83×** | xRjasw2 | compact idiom peer |

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
| java | mul | CP | P-gen | x86_64 | thru‡ | 16.20 | BigDecimal | 47.72 | **2.95×** | xRjasw2 | compact idiom peer |
| java | mul | WP | P-gen | x86_64 | thru‡ | 58.63 | BigDecimal | 208.62 | **3.56×** | xRjasw2 | compact idiom peer |
| java | mul | XP | P-gen | x86_64 | thru‡ | 81.20 | BigDecimal | 361.61 | **4.45×** | xRjasw2 | compact idiom peer |

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
| java | div | CD | P-gen | x86_64 | thru‡ | 116.61 | BigDecimal | 503.35 | **4.32×** | xRjasw2 | compact idiom peer |
| java | div | WD | P-gen | x86_64 | thru‡ | 157.23 | BigDecimal | 341.38 | **2.17×** | xRjasw2 | compact idiom peer |
| java | div | XD | P-gen | x86_64 | thru‡ | 150.08 | BigDecimal | 448.11 | **2.99×** | xRjasw2 | compact idiom peer |
| java | div | ET | P-gen | x86_64 | thru‡ | 53.20 | BigDecimal | 1671.77 | **31.42×** | xRjasw2 | compact idiom peer |
| java | div | PT | P-gen | x86_64 | thru‡ | 28.33 | BigDecimal | 1556.18 | **54.93×** | xRjasw2 | compact idiom peer |

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
| java | fma | FN | FMA | x86_64 | thru‡ | 272.76 | - | - | - | xRjasw2 |  |
| java | fma | FF | FMA | x86_64 | thru‡ | 221.71 | - | - | - | xRjasw2 |  |

<!-- END GENERATED fma-rel-java-x86 -->

</div>
