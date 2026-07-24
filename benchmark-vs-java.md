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
| java | add | MIX | P-fin | arm64 | thru‡ | 6.17 | BigDecimal | 19.54 | **3.17×** | Rjasw2 | compact idiom peer |
| java | sub | MIX | P-fin | arm64 | thru‡ | 5.61 | BigDecimal | 22.23 | **3.96×** | Rjasw2 | compact idiom peer |
| java | mul | CP | P-fin | arm64 | thru‡ | 4.83 | BigDecimal | 12.61 | **2.61×** | Rjasw2 | compact idiom peer |
| java | mul | WP | P-fin | arm64 | thru‡ | 27.65 | BigDecimal | 74.06 | **2.68×** | Rjasw2 | compact idiom peer |
| java | div | CD | P-fin | arm64 | thru‡ | 35.74 | BigDecimal | 154.42 | **4.32×** | Rjasw2 | compact idiom peer |
| java | div | WD | P-fin | arm64 | thru‡ | 43.97 | BigDecimal | 90.11 | **2.05×** | Rjasw2 | compact idiom peer |
| java | div | ET | P-fin | arm64 | thru‡ | 12.91 | BigDecimal | 501.54 | **38.85×** | Rjasw2 | compact idiom peer |
| java | div | PT | P-fin | arm64 | thru‡ | 9.50 | BigDecimal | 482.39 | **50.78×** | Rjasw2 | compact idiom peer |

<!-- END GENERATED pfin-rel-java -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-java-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | add | MIX | P-fin | x86_64 | thru‡ | 16.11 | BigDecimal | 58.92 | **3.66×** | xRjasw2 | compact idiom peer |
| java | sub | MIX | P-fin | x86_64 | thru‡ | 16.77 | BigDecimal | 67.45 | **4.02×** | xRjasw2 | compact idiom peer |
| java | mul | CP | P-fin | x86_64 | thru‡ | 13.17 | BigDecimal | 41.25 | **3.13×** | xRjasw2 | compact idiom peer |
| java | mul | WP | P-fin | x86_64 | thru‡ | 51.99 | BigDecimal | 164.70 | **3.17×** | xRjasw2 | compact idiom peer |
| java | div | CD | P-fin | x86_64 | thru‡ | 99.59 | BigDecimal | 417.97 | **4.20×** | xRjasw2 | compact idiom peer |
| java | div | WD | P-fin | x86_64 | thru‡ | 128.71 | BigDecimal | 224.53 | **1.74×** | xRjasw2 | compact idiom peer |
| java | div | ET | P-fin | x86_64 | thru‡ | 47.28 | BigDecimal | 1469.52 | **31.08×** | xRjasw2 | compact idiom peer |
| java | div | PT | P-fin | x86_64 | thru‡ | 24.29 | BigDecimal | 1393.50 | **57.37×** | xRjasw2 | compact idiom peer |

<!-- END GENERATED pfin-rel-java-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-java -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | add | SQ | P-gen | arm64 | thru‡ | 5.47 | BigDecimal | 19.00 | **3.47×** | Rjasw2 | compact idiom peer |
| java | add | NQ | P-gen | arm64 | thru‡ | 7.45 | BigDecimal | 30.63 | **4.11×** | Rjasw2 | compact idiom peer |
| java | add | MQ | P-gen | arm64 | thru‡ | 18.28 | BigDecimal | 31.03 | **1.70×** | Rjasw2 | compact idiom peer |
| java | add | OQ | P-gen | arm64 | thru‡ | 28.44 | BigDecimal | 71.59 | **2.52×** | Rjasw2 | compact idiom peer |
| java | add | FQ | P-gen | arm64 | thru‡ | 22.31 | BigDecimal | 86.85 | **3.89×** | Rjasw2 | compact idiom peer |

<!-- END GENERATED add-rel-java -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-java-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | add | SQ | P-gen | x86_64 | thru‡ | 13.69 | BigDecimal | 54.47 | **3.98×** | xRjasw2 | compact idiom peer |
| java | add | NQ | P-gen | x86_64 | thru‡ | 20.24 | BigDecimal | 85.69 | **4.23×** | xRjasw2 | compact idiom peer |
| java | add | MQ | P-gen | x86_64 | thru‡ | 34.23 | BigDecimal | 88.92 | **2.60×** | xRjasw2 | compact idiom peer |
| java | add | OQ | P-gen | x86_64 | thru‡ | 66.83 | BigDecimal | 181.89 | **2.72×** | xRjasw2 | compact idiom peer |
| java | add | FQ | P-gen | x86_64 | thru‡ | 59.37 | BigDecimal | 341.30 | **5.75×** | xRjasw2 | compact idiom peer |

<!-- END GENERATED add-rel-java-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-java -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | sub | SQ | P-gen | arm64 | thru‡ | 4.39 | BigDecimal | 23.20 | **5.28×** | Rjasw2 | compact idiom peer |
| java | sub | NQ | P-gen | arm64 | thru‡ | 7.22 | BigDecimal | 33.91 | **4.70×** | Rjasw2 | compact idiom peer |
| java | sub | MQ | P-gen | arm64 | thru‡ | 18.40 | BigDecimal | 35.12 | **1.91×** | Rjasw2 | compact idiom peer |
| java | sub | OQ | P-gen | arm64 | thru‡ | 29.75 | BigDecimal | 78.14 | **2.63×** | Rjasw2 | compact idiom peer |
| java | sub | FQ | P-gen | arm64 | thru‡ | 19.59 | BigDecimal | 91.57 | **4.67×** | Rjasw2 | compact idiom peer |

<!-- END GENERATED sub-rel-java -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-java-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | sub | SQ | P-gen | x86_64 | thru‡ | 13.14 | BigDecimal | 69.47 | **5.29×** | xRjasw2 | compact idiom peer |
| java | sub | NQ | P-gen | x86_64 | thru‡ | 23.39 | BigDecimal | 93.43 | **3.99×** | xRjasw2 | compact idiom peer |
| java | sub | MQ | P-gen | x86_64 | thru‡ | 36.06 | BigDecimal | 103.59 | **2.87×** | xRjasw2 | compact idiom peer |
| java | sub | OQ | P-gen | x86_64 | thru‡ | 80.64 | BigDecimal | 243.86 | **3.02×** | xRjasw2 | compact idiom peer |
| java | sub | FQ | P-gen | x86_64 | thru‡ | 45.21 | BigDecimal | 217.82 | **4.82×** | xRjasw2 | compact idiom peer |

<!-- END GENERATED sub-rel-java-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-java -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | mul | CP | P-gen | arm64 | thru‡ | 5.16 | BigDecimal | 11.89 | **2.30×** | Rjasw2 | compact idiom peer |
| java | mul | WP | P-gen | arm64 | thru‡ | 26.17 | BigDecimal | 55.24 | **2.11×** | Rjasw2 | compact idiom peer |
| java | mul | XP | P-gen | arm64 | thru‡ | 43.50 | BigDecimal | 155.85 | **3.58×** | Rjasw2 | compact idiom peer |

<!-- END GENERATED mul-rel-java -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-java-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | mul | CP | P-gen | x86_64 | thru‡ | 14.36 | BigDecimal | 42.56 | **2.96×** | xRjasw2 | compact idiom peer |
| java | mul | WP | P-gen | x86_64 | thru‡ | 49.29 | BigDecimal | 156.42 | **3.17×** | xRjasw2 | compact idiom peer |
| java | mul | XP | P-gen | x86_64 | thru‡ | 69.74 | BigDecimal | 279.82 | **4.01×** | xRjasw2 | compact idiom peer |

<!-- END GENERATED mul-rel-java-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-java -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | div | CD | P-gen | arm64 | thru‡ | 31.23 | BigDecimal | 136.68 | **4.38×** | Rjasw2 | compact idiom peer |
| java | div | WD | P-gen | arm64 | thru‡ | 47.21 | BigDecimal | 104.15 | **2.21×** | Rjasw2 | compact idiom peer |
| java | div | XD | P-gen | arm64 | thru‡ | 47.35 | BigDecimal | 217.88 | **4.60×** | Rjasw2 | compact idiom peer |
| java | div | ET | P-gen | arm64 | thru‡ | 13.01 | BigDecimal | 412.83 | **31.73×** | Rjasw2 | compact idiom peer |
| java | div | PT | P-gen | arm64 | thru‡ | 9.87 | BigDecimal | 382.06 | **38.71×** | Rjasw2 | compact idiom peer |

<!-- END GENERATED div-rel-java -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-java-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | div | CD | P-gen | x86_64 | thru‡ | 92.50 | BigDecimal | 372.26 | **4.02×** | xRjasw2 | compact idiom peer |
| java | div | WD | P-gen | x86_64 | thru‡ | 119.89 | BigDecimal | 264.02 | **2.20×** | xRjasw2 | compact idiom peer |
| java | div | XD | P-gen | x86_64 | thru‡ | 129.20 | BigDecimal | 358.32 | **2.77×** | xRjasw2 | compact idiom peer |
| java | div | ET | P-gen | x86_64 | thru‡ | 49.83 | BigDecimal | 1152.56 | **23.13×** | xRjasw2 | compact idiom peer |
| java | div | PT | P-gen | x86_64 | thru‡ | 24.48 | BigDecimal | 1055.59 | **43.12×** | xRjasw2 | compact idiom peer |

<!-- END GENERATED div-rel-java-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-java -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | fma | FN | FMA | arm64 | thru‡ | 99.27 | - | - | - | Rjasw2 |  |
| java | fma | FF | FMA | arm64 | thru‡ | 68.97 | - | - | - | Rjasw2 |  |

<!-- END GENERATED fma-rel-java -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-java-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | fma | FN | FMA | x86_64 | thru‡ | 219.34 | - | - | - | xRjasw2 |  |
| java | fma | FF | FMA | x86_64 | thru‡ | 179.09 | - | - | - | xRjasw2 |  |

<!-- END GENERATED fma-rel-java-x86 -->

</div>
