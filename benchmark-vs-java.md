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
| java | add | MIX | P-fin | arm64 | thru‡ | 4.49 | BigDecimal | 19.61 | **4.37×** | Rjasw2 | compact idiom peer |
| java | sub | MIX | P-fin | arm64 | thru‡ | 5.46 | BigDecimal | 24.01 | **4.40×** | Rjasw2 | compact idiom peer |
| java | mul | CP | P-fin | arm64 | thru‡ | 4.63 | BigDecimal | 12.34 | **2.67×** | Rjasw2 | compact idiom peer |
| java | mul | WP | P-fin | arm64 | thru‡ | 28.59 | BigDecimal | 62.31 | **2.18×** | Rjasw2 | compact idiom peer |
| java | div | CD | P-fin | arm64 | thru‡ | 36.44 | BigDecimal | 138.60 | **3.80×** | Rjasw2 | compact idiom peer |
| java | div | WD | P-fin | arm64 | thru‡ | 43.67 | BigDecimal | 91.31 | **2.09×** | Rjasw2 | compact idiom peer |
| java | div | ET | P-fin | arm64 | thru‡ | 12.52 | BigDecimal | 492.44 | **39.33×** | Rjasw2 | compact idiom peer |
| java | div | PT | P-fin | arm64 | thru‡ | 9.26 | BigDecimal | 472.48 | **51.02×** | Rjasw2 | compact idiom peer |

<!-- END GENERATED pfin-rel-java -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-java-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | add | MIX | P-fin | x86_64 | thru‡ | 8.65 | BigDecimal | 49.08 | **5.67×** | xRjasw2 | compact idiom peer |
| java | sub | MIX | P-fin | x86_64 | thru‡ | 16.32 | BigDecimal | 57.00 | **3.49×** | xRjasw2 | compact idiom peer |
| java | mul | CP | P-fin | x86_64 | thru‡ | 11.93 | BigDecimal | 41.29 | **3.46×** | xRjasw2 | compact idiom peer |
| java | mul | WP | P-fin | x86_64 | thru‡ | 47.91 | BigDecimal | 154.55 | **3.23×** | xRjasw2 | compact idiom peer |
| java | div | CD | P-fin | x86_64 | thru‡ | 99.51 | BigDecimal | 399.43 | **4.01×** | xRjasw2 | compact idiom peer |
| java | div | WD | P-fin | x86_64 | thru‡ | 119.48 | BigDecimal | 214.52 | **1.80×** | xRjasw2 | compact idiom peer |
| java | div | ET | P-fin | x86_64 | thru‡ | 44.66 | BigDecimal | 1386.06 | **31.04×** | xRjasw2 | compact idiom peer |
| java | div | PT | P-fin | x86_64 | thru‡ | 23.25 | BigDecimal | 1337.71 | **57.54×** | xRjasw2 | compact idiom peer |

<!-- END GENERATED pfin-rel-java-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-java -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | add | SQ | P-gen | arm64 | thru‡ | 4.81 | BigDecimal | 19.00 | **3.95×** | Rjasw2 | compact idiom peer |
| java | add | NQ | P-gen | arm64 | thru‡ | 8.07 | BigDecimal | 30.21 | **3.74×** | Rjasw2 | compact idiom peer |
| java | add | MQ | P-gen | arm64 | thru‡ | 19.87 | BigDecimal | 31.65 | **1.59×** | Rjasw2 | compact idiom peer |
| java | add | OQ | P-gen | arm64 | thru‡ | 28.24 | BigDecimal | 69.56 | **2.46×** | Rjasw2 | compact idiom peer |
| java | add | FQ | P-gen | arm64 | thru‡ | 23.23 | BigDecimal | 85.39 | **3.68×** | Rjasw2 | compact idiom peer |

<!-- END GENERATED add-rel-java -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-java-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | add | SQ | P-gen | x86_64 | thru‡ | 13.74 | BigDecimal | 53.35 | **3.88×** | xRjasw2 | compact idiom peer |
| java | add | NQ | P-gen | x86_64 | thru‡ | 20.19 | BigDecimal | 84.09 | **4.16×** | xRjasw2 | compact idiom peer |
| java | add | MQ | P-gen | x86_64 | thru‡ | 33.95 | BigDecimal | 82.50 | **2.43×** | xRjasw2 | compact idiom peer |
| java | add | OQ | P-gen | x86_64 | thru‡ | 61.47 | BigDecimal | 164.39 | **2.67×** | xRjasw2 | compact idiom peer |
| java | add | FQ | P-gen | x86_64 | thru‡ | 43.15 | BigDecimal | 189.49 | **4.39×** | xRjasw2 | compact idiom peer |

<!-- END GENERATED add-rel-java-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-java -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | sub | SQ | P-gen | arm64 | thru‡ | 4.48 | BigDecimal | 23.32 | **5.21×** | Rjasw2 | compact idiom peer |
| java | sub | NQ | P-gen | arm64 | thru‡ | 7.44 | BigDecimal | 33.93 | **4.56×** | Rjasw2 | compact idiom peer |
| java | sub | MQ | P-gen | arm64 | thru‡ | 18.62 | BigDecimal | 34.01 | **1.83×** | Rjasw2 | compact idiom peer |
| java | sub | OQ | P-gen | arm64 | thru‡ | 27.78 | BigDecimal | 77.73 | **2.80×** | Rjasw2 | compact idiom peer |
| java | sub | FQ | P-gen | arm64 | thru‡ | 19.76 | BigDecimal | 90.74 | **4.59×** | Rjasw2 | compact idiom peer |

<!-- END GENERATED sub-rel-java -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-java-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | sub | SQ | P-gen | x86_64 | thru‡ | 13.04 | BigDecimal | 61.72 | **4.73×** | xRjasw2 | compact idiom peer |
| java | sub | NQ | P-gen | x86_64 | thru‡ | 20.07 | BigDecimal | 89.41 | **4.45×** | xRjasw2 | compact idiom peer |
| java | sub | MQ | P-gen | x86_64 | thru‡ | 33.01 | BigDecimal | 91.52 | **2.77×** | xRjasw2 | compact idiom peer |
| java | sub | OQ | P-gen | x86_64 | thru‡ | 63.10 | BigDecimal | 211.69 | **3.35×** | xRjasw2 | compact idiom peer |
| java | sub | FQ | P-gen | x86_64 | thru‡ | 42.15 | BigDecimal | 195.49 | **4.64×** | xRjasw2 | compact idiom peer |

<!-- END GENERATED sub-rel-java-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-java -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | mul | CP | P-gen | arm64 | thru‡ | 5.14 | BigDecimal | 12.09 | **2.35×** | Rjasw2 | compact idiom peer |
| java | mul | WP | P-gen | arm64 | thru‡ | 25.46 | BigDecimal | 54.04 | **2.12×** | Rjasw2 | compact idiom peer |
| java | mul | XP | P-gen | arm64 | thru‡ | 43.55 | BigDecimal | 169.01 | **3.88×** | Rjasw2 | compact idiom peer |

<!-- END GENERATED mul-rel-java -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-java-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | mul | CP | P-gen | x86_64 | thru‡ | 13.78 | BigDecimal | 40.14 | **2.91×** | xRjasw2 | compact idiom peer |
| java | mul | WP | P-gen | x86_64 | thru‡ | 45.79 | BigDecimal | 150.79 | **3.29×** | xRjasw2 | compact idiom peer |
| java | mul | XP | P-gen | x86_64 | thru‡ | 66.80 | BigDecimal | 278.07 | **4.16×** | xRjasw2 | compact idiom peer |

<!-- END GENERATED mul-rel-java-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-java -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | div | CD | P-gen | arm64 | thru‡ | 30.83 | BigDecimal | 133.94 | **4.34×** | Rjasw2 | compact idiom peer |
| java | div | WD | P-gen | arm64 | thru‡ | 46.80 | BigDecimal | 97.30 | **2.08×** | Rjasw2 | compact idiom peer |
| java | div | XD | P-gen | arm64 | thru‡ | 46.73 | BigDecimal | 221.06 | **4.73×** | Rjasw2 | compact idiom peer |
| java | div | ET | P-gen | arm64 | thru‡ | 12.90 | BigDecimal | 411.59 | **31.91×** | Rjasw2 | compact idiom peer |
| java | div | PT | P-gen | arm64 | thru‡ | 9.88 | BigDecimal | 383.58 | **38.82×** | Rjasw2 | compact idiom peer |

<!-- END GENERATED div-rel-java -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-java-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | div | CD | P-gen | x86_64 | thru‡ | 89.37 | BigDecimal | 352.30 | **3.94×** | xRjasw2 | compact idiom peer |
| java | div | WD | P-gen | x86_64 | thru‡ | 114.91 | BigDecimal | 255.81 | **2.23×** | xRjasw2 | compact idiom peer |
| java | div | XD | P-gen | x86_64 | thru‡ | 129.09 | BigDecimal | 343.17 | **2.66×** | xRjasw2 | compact idiom peer |
| java | div | ET | P-gen | x86_64 | thru‡ | 46.17 | BigDecimal | 1106.13 | **23.96×** | xRjasw2 | compact idiom peer |
| java | div | PT | P-gen | x86_64 | thru‡ | 23.64 | BigDecimal | 1026.21 | **43.41×** | xRjasw2 | compact idiom peer |

<!-- END GENERATED div-rel-java-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-java -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | fma | FN | FMA | arm64 | thru‡ | 102.16 | - | - | - | Rjasw2 |  |
| java | fma | FF | FMA | arm64 | thru‡ | 72.93 | - | - | - | Rjasw2 |  |

<!-- END GENERATED fma-rel-java -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-java-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | fma | FN | FMA | x86_64 | thru‡ | 201.75 | - | - | - | xRjasw2 |  |
| java | fma | FF | FMA | x86_64 | thru‡ | 167.41 | - | - | - | xRjasw2 |  |

<!-- END GENERATED fma-rel-java-x86 -->

</div>
