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
| java | add | MIX | P-fin | x86_64 | thru‡ | 10.00 | BigDecimal | 49.28 | **4.93×** | xRjasw2 | compact idiom peer |
| java | sub | MIX | P-fin | x86_64 | thru‡ | 18.04 | BigDecimal | 60.49 | **3.35×** | xRjasw2 | compact idiom peer |
| java | mul | CP | P-fin | x86_64 | thru‡ | 12.28 | BigDecimal | 44.24 | **3.60×** | xRjasw2 | compact idiom peer |
| java | mul | WP | P-fin | x86_64 | thru‡ | 49.41 | BigDecimal | 155.36 | **3.14×** | xRjasw2 | compact idiom peer |
| java | div | CD | P-fin | x86_64 | thru‡ | 99.77 | BigDecimal | 417.32 | **4.18×** | xRjasw2 | compact idiom peer |
| java | div | WD | P-fin | x86_64 | thru‡ | 125.83 | BigDecimal | 222.29 | **1.77×** | xRjasw2 | compact idiom peer |
| java | div | ET | P-fin | x86_64 | thru‡ | 50.37 | BigDecimal | 1459.72 | **28.98×** | xRjasw2 | compact idiom peer |
| java | div | PT | P-fin | x86_64 | thru‡ | 24.18 | BigDecimal | 1379.38 | **57.05×** | xRjasw2 | compact idiom peer |

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
| java | add | SQss | P-gen | x86_64 | thru‡ | 7.22 | BigDecimal | 49.09 | **6.80×** | xRjasw2 | compact idiom peer |
| java | add | SQos | P-gen | x86_64 | thru‡ | 16.04 | BigDecimal | 61.53 | **3.84×** | xRjasw2 | compact idiom peer |
| java | add | NQss | P-gen | x86_64 | thru‡ | 18.53 | BigDecimal | 77.11 | **4.16×** | xRjasw2 | compact idiom peer |
| java | add | NQos | P-gen | x86_64 | thru‡ | 27.36 | BigDecimal | 89.10 | **3.26×** | xRjasw2 | compact idiom peer |
| java | add | MQss | P-gen | x86_64 | thru‡ | 25.59 | BigDecimal | 78.37 | **3.06×** | xRjasw2 | compact idiom peer |
| java | add | MQos | P-gen | x86_64 | thru‡ | 40.08 | BigDecimal | 87.93 | **2.19×** | xRjasw2 | compact idiom peer |
| java | add | OQss | P-gen | x86_64 | thru‡ | 55.34 | BigDecimal | 172.40 | **3.12×** | xRjasw2 | compact idiom peer |
| java | add | OQos | P-gen | x86_64 | thru‡ | 73.65 | BigDecimal | 170.75 | **2.32×** | xRjasw2 | compact idiom peer |
| java | add | FQss | P-gen | x86_64 | thru‡ | 34.89 | BigDecimal | 181.05 | **5.19×** | xRjasw2 | compact idiom peer |
| java | add | FQos | P-gen | x86_64 | thru‡ | 45.29 | BigDecimal | 208.98 | **4.61×** | xRjasw2 | compact idiom peer |

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
| java | sub | SQss | P-gen | x86_64 | thru‡ | 14.29 | BigDecimal | 65.42 | **4.58×** | xRjasw2 | compact idiom peer |
| java | sub | SQos | P-gen | x86_64 | thru‡ | 10.57 | BigDecimal | 56.75 | **5.37×** | xRjasw2 | compact idiom peer |
| java | sub | NQss | P-gen | x86_64 | thru‡ | 28.64 | BigDecimal | 95.07 | **3.32×** | xRjasw2 | compact idiom peer |
| java | sub | NQos | P-gen | x86_64 | thru‡ | 20.03 | BigDecimal | 89.49 | **4.47×** | xRjasw2 | compact idiom peer |
| java | sub | MQss | P-gen | x86_64 | thru‡ | 39.76 | BigDecimal | 95.68 | **2.41×** | xRjasw2 | compact idiom peer |
| java | sub | MQos | P-gen | x86_64 | thru‡ | 25.05 | BigDecimal | 87.45 | **3.49×** | xRjasw2 | compact idiom peer |
| java | sub | OQss | P-gen | x86_64 | thru‡ | 70.87 | BigDecimal | 184.26 | **2.60×** | xRjasw2 | compact idiom peer |
| java | sub | OQos | P-gen | x86_64 | thru‡ | 59.94 | BigDecimal | 194.04 | **3.24×** | xRjasw2 | compact idiom peer |
| java | sub | FQss | P-gen | x86_64 | thru‡ | 47.92 | BigDecimal | 216.07 | **4.51×** | xRjasw2 | compact idiom peer |
| java | sub | FQos | P-gen | x86_64 | thru‡ | 36.63 | BigDecimal | 187.60 | **5.12×** | xRjasw2 | compact idiom peer |

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
| java | mul | CP | P-gen | x86_64 | thru‡ | 13.96 | BigDecimal | 42.12 | **3.02×** | xRjasw2 | compact idiom peer |
| java | mul | WP | P-gen | x86_64 | thru‡ | 46.25 | BigDecimal | 160.94 | **3.48×** | xRjasw2 | compact idiom peer |
| java | mul | XP | P-gen | x86_64 | thru‡ | 67.77 | BigDecimal | 282.93 | **4.17×** | xRjasw2 | compact idiom peer |

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
| java | div | CD | P-gen | x86_64 | thru‡ | 93.35 | BigDecimal | 367.19 | **3.93×** | xRjasw2 | compact idiom peer |
| java | div | WD | P-gen | x86_64 | thru‡ | 119.04 | BigDecimal | 263.98 | **2.22×** | xRjasw2 | compact idiom peer |
| java | div | XD | P-gen | x86_64 | thru‡ | 131.80 | BigDecimal | 355.97 | **2.70×** | xRjasw2 | compact idiom peer |
| java | div | ET | P-gen | x86_64 | thru‡ | 47.14 | BigDecimal | 1159.93 | **24.61×** | xRjasw2 | compact idiom peer |
| java | div | PT | P-gen | x86_64 | thru‡ | 23.57 | BigDecimal | 1117.22 | **47.40×** | xRjasw2 | compact idiom peer |

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
| java | fma | FN | FMA | x86_64 | thru‡ | 199.38 | - | - | - | xRjasw2 |  |
| java | fma | FF | FMA | x86_64 | thru‡ | 167.29 | - | - | - | xRjasw2 |  |

<!-- END GENERATED fma-rel-java-x86 -->

</div>
