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
| ratio = BigDecimal / Miguel | 5× | 4× | 3× | 2.0× – 54× |

## FinMix — realistic financial mix (P-fin)

The headline: one realistic 64-bit financial operation mix — a `MIX` add/sub stream, mul `CP`/`WP`, div `CD`/`WD`/`ET`/`PT` — `ratio = alt / Miguel` (&gt; 1 ⇒ d128 faster). This is the profile closest to real financial code.

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED pfin-rel-java -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | add | MIX | P-fin | arm64 | thru‡ | 5.11 | BigDecimal | 18.95 | **3.71×** | Rjasw2 | compact idiom peer |
| java | sub | MIX | P-fin | arm64 | thru‡ | 6.07 | BigDecimal | 22.74 | **3.75×** | Rjasw2 | compact idiom peer |
| java | mul | CP | P-fin | arm64 | thru‡ | 4.89 | BigDecimal | 12.61 | **2.58×** | Rjasw2 | compact idiom peer |
| java | mul | WP | P-fin | arm64 | thru‡ | 29.46 | BigDecimal | 68.17 | **2.31×** | Rjasw2 | compact idiom peer |
| java | div | CD | P-fin | arm64 | thru‡ | 36.26 | BigDecimal | 144.25 | **3.98×** | Rjasw2 | compact idiom peer |
| java | div | WD | P-fin | arm64 | thru‡ | 38.79 | BigDecimal | 95.63 | **2.47×** | Rjasw2 | compact idiom peer |
| java | div | ET | P-fin | arm64 | thru‡ | 13.31 | BigDecimal | 504.36 | **37.89×** | Rjasw2 | compact idiom peer |
| java | div | PT | P-fin | arm64 | thru‡ | 10.69 | BigDecimal | 483.51 | **45.23×** | Rjasw2 | compact idiom peer |

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
| java | add | SQss | P-gen | arm64 | thru‡ | 3.84 | BigDecimal | 17.88 | **4.66×** | Rjasw2 | compact idiom peer |
| java | add | SQos | P-gen | arm64 | thru‡ | 4.89 | BigDecimal | 20.96 | **4.29×** | Rjasw2 | compact idiom peer |
| java | add | NQss | P-gen | arm64 | thru‡ | 7.61 | BigDecimal | 29.36 | **3.86×** | Rjasw2 | compact idiom peer |
| java | add | NQos | P-gen | arm64 | thru‡ | 10.31 | BigDecimal | 30.10 | **2.92×** | Rjasw2 | compact idiom peer |
| java | add | MQss | P-gen | arm64 | thru‡ | 11.46 | BigDecimal | 29.67 | **2.59×** | Rjasw2 | compact idiom peer |
| java | add | MQos | P-gen | arm64 | thru‡ | 28.55 | BigDecimal | 30.59 | **1.07×** | Rjasw2 | compact idiom peer |
| java | add | OQss | P-gen | arm64 | thru‡ | 22.60 | BigDecimal | 68.69 | **3.04×** | Rjasw2 | compact idiom peer |
| java | add | OQos | P-gen | arm64 | thru‡ | 45.44 | BigDecimal | 71.03 | **1.56×** | Rjasw2 | compact idiom peer |
| java | add | FQss | P-gen | arm64 | thru‡ | 16.01 | BigDecimal | 71.80 | **4.48×** | Rjasw2 | compact idiom peer |
| java | add | FQos | P-gen | arm64 | thru‡ | 33.74 | BigDecimal | 83.68 | **2.48×** | Rjasw2 | compact idiom peer |

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
| java | sub | SQss | P-gen | arm64 | thru‡ | 4.82 | BigDecimal | 22.20 | **4.61×** | Rjasw2 | compact idiom peer |
| java | sub | SQos | P-gen | arm64 | thru‡ | 4.01 | BigDecimal | 21.42 | **5.34×** | Rjasw2 | compact idiom peer |
| java | sub | NQss | P-gen | arm64 | thru‡ | 9.70 | BigDecimal | 33.74 | **3.48×** | Rjasw2 | compact idiom peer |
| java | sub | NQos | P-gen | arm64 | thru‡ | 7.40 | BigDecimal | 33.42 | **4.52×** | Rjasw2 | compact idiom peer |
| java | sub | MQss | P-gen | arm64 | thru‡ | 27.76 | BigDecimal | 33.89 | **1.22×** | Rjasw2 | compact idiom peer |
| java | sub | MQos | P-gen | arm64 | thru‡ | 10.72 | BigDecimal | 33.32 | **3.11×** | Rjasw2 | compact idiom peer |
| java | sub | OQss | P-gen | arm64 | thru‡ | 44.93 | BigDecimal | 77.26 | **1.72×** | Rjasw2 | compact idiom peer |
| java | sub | OQos | P-gen | arm64 | thru‡ | 22.12 | BigDecimal | 75.15 | **3.40×** | Rjasw2 | compact idiom peer |
| java | sub | FQss | P-gen | arm64 | thru‡ | 33.29 | BigDecimal | 85.83 | **2.58×** | Rjasw2 | compact idiom peer |
| java | sub | FQos | P-gen | arm64 | thru‡ | 15.82 | BigDecimal | 77.04 | **4.87×** | Rjasw2 | compact idiom peer |

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
| java | mul | CP | P-gen | arm64 | thru‡ | 5.28 | BigDecimal | 11.79 | **2.23×** | Rjasw2 | compact idiom peer |
| java | mul | WP | P-gen | arm64 | thru‡ | 30.22 | BigDecimal | 59.99 | **1.99×** | Rjasw2 | compact idiom peer |
| java | mul | XP | P-gen | arm64 | thru‡ | 43.02 | BigDecimal | 164.23 | **3.82×** | Rjasw2 | compact idiom peer |

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
| java | div | CD | P-gen | arm64 | thru‡ | 33.17 | BigDecimal | 138.38 | **4.17×** | Rjasw2 | compact idiom peer |
| java | div | WD | P-gen | arm64 | thru‡ | 44.43 | BigDecimal | 104.94 | **2.36×** | Rjasw2 | compact idiom peer |
| java | div | XD | P-gen | arm64 | thru‡ | 53.63 | BigDecimal | 225.18 | **4.20×** | Rjasw2 | compact idiom peer |
| java | div | ET | P-gen | arm64 | thru‡ | 12.39 | BigDecimal | 425.83 | **34.37×** | Rjasw2 | compact idiom peer |
| java | div | PT | P-gen | arm64 | thru‡ | 10.76 | BigDecimal | 394.25 | **36.64×** | Rjasw2 | compact idiom peer |

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
| java | fma | FN | FMA | arm64 | thru‡ | 46.36 | - | - | - | Rjasw2 |  |
| java | fma | FF | FMA | arm64 | thru‡ | 58.30 | - | - | - | Rjasw2 |  |

<!-- END GENERATED fma-rel-java -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-java-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | fma | FN | FMA | x86_64 | thru‡ | 272.76 | - | - | - | xRjasw2 |  |
| java | fma | FF | FMA | x86_64 | thru‡ | 221.71 | - | - | - | xRjasw2 |  |

<!-- END GENERATED fma-rel-java-x86 -->

</div>
