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
| java | add | MIX | P-fin | arm64 | thru‡ | 6.35 | BigDecimal | 20.37 | **3.21×** | Rjasw2 | compact idiom peer |
| java | sub | MIX | P-fin | arm64 | thru‡ | 5.62 | BigDecimal | 24.03 | **4.28×** | Rjasw2 | compact idiom peer |
| java | mul | CP | P-fin | arm64 | thru‡ | 5.29 | BigDecimal | 12.97 | **2.45×** | Rjasw2 | compact idiom peer |
| java | mul | WP | P-fin | arm64 | thru‡ | 28.00 | BigDecimal | 72.87 | **2.60×** | Rjasw2 | compact idiom peer |
| java | div | CD | P-fin | arm64 | thru‡ | 36.96 | BigDecimal | 157.62 | **4.26×** | Rjasw2 | compact idiom peer |
| java | div | WD | P-fin | arm64 | thru‡ | 49.51 | BigDecimal | 89.46 | **1.81×** | Rjasw2 | compact idiom peer |
| java | div | ET | P-fin | arm64 | thru‡ | 12.86 | BigDecimal | 498.81 | **38.79×** | Rjasw2 | compact idiom peer |
| java | div | PT | P-fin | arm64 | thru‡ | 9.88 | BigDecimal | 479.82 | **48.56×** | Rjasw2 | compact idiom peer |

<!-- END GENERATED pfin-rel-java -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-java-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | add | MIX | P-fin | x86_64 | thru‡ | 16.43 | BigDecimal | 55.19 | **3.36×** | xRjasw2 | compact idiom peer |
| java | sub | MIX | P-fin | x86_64 | thru‡ | 16.23 | BigDecimal | 66.31 | **4.09×** | xRjasw2 | compact idiom peer |
| java | mul | CP | P-fin | x86_64 | thru‡ | 12.37 | BigDecimal | 41.73 | **3.37×** | xRjasw2 | compact idiom peer |
| java | mul | WP | P-fin | x86_64 | thru‡ | 49.39 | BigDecimal | 150.91 | **3.06×** | xRjasw2 | compact idiom peer |
| java | div | CD | P-fin | x86_64 | thru‡ | 97.03 | BigDecimal | 408.57 | **4.21×** | xRjasw2 | compact idiom peer |
| java | div | WD | P-fin | x86_64 | thru‡ | 122.89 | BigDecimal | 218.12 | **1.77×** | xRjasw2 | compact idiom peer |
| java | div | ET | P-fin | x86_64 | thru‡ | 44.76 | BigDecimal | 1472.00 | **32.89×** | xRjasw2 | compact idiom peer |
| java | div | PT | P-fin | x86_64 | thru‡ | 23.41 | BigDecimal | 1405.87 | **60.05×** | xRjasw2 | compact idiom peer |

<!-- END GENERATED pfin-rel-java-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-java -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | add | SQ | P-gen | arm64 | thru‡ | 5.45 | BigDecimal | 18.86 | **3.46×** | Rjasw2 | compact idiom peer |
| java | add | NQ | P-gen | arm64 | thru‡ | 7.30 | BigDecimal | 29.87 | **4.09×** | Rjasw2 | compact idiom peer |
| java | add | MQ | P-gen | arm64 | thru‡ | 18.58 | BigDecimal | 30.10 | **1.62×** | Rjasw2 | compact idiom peer |
| java | add | OQ | P-gen | arm64 | thru‡ | 29.30 | BigDecimal | 72.88 | **2.49×** | Rjasw2 | compact idiom peer |
| java | add | FQ | P-gen | arm64 | thru‡ | 21.54 | BigDecimal | 86.96 | **4.04×** | Rjasw2 | compact idiom peer |

<!-- END GENERATED add-rel-java -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-java-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | add | SQ | P-gen | x86_64 | thru‡ | 13.52 | BigDecimal | 53.06 | **3.92×** | xRjasw2 | compact idiom peer |
| java | add | NQ | P-gen | x86_64 | thru‡ | 18.92 | BigDecimal | 82.51 | **4.36×** | xRjasw2 | compact idiom peer |
| java | add | MQ | P-gen | x86_64 | thru‡ | 37.06 | BigDecimal | 85.05 | **2.29×** | xRjasw2 | compact idiom peer |
| java | add | OQ | P-gen | x86_64 | thru‡ | 59.75 | BigDecimal | 173.14 | **2.90×** | xRjasw2 | compact idiom peer |
| java | add | FQ | P-gen | x86_64 | thru‡ | 40.06 | BigDecimal | 238.95 | **5.96×** | xRjasw2 | compact idiom peer |

<!-- END GENERATED add-rel-java-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-java -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | sub | SQ | P-gen | arm64 | thru‡ | 4.37 | BigDecimal | 22.39 | **5.12×** | Rjasw2 | compact idiom peer |
| java | sub | NQ | P-gen | arm64 | thru‡ | 7.68 | BigDecimal | 33.18 | **4.32×** | Rjasw2 | compact idiom peer |
| java | sub | MQ | P-gen | arm64 | thru‡ | 18.61 | BigDecimal | 33.07 | **1.78×** | Rjasw2 | compact idiom peer |
| java | sub | OQ | P-gen | arm64 | thru‡ | 28.68 | BigDecimal | 78.38 | **2.73×** | Rjasw2 | compact idiom peer |
| java | sub | FQ | P-gen | arm64 | thru‡ | 21.56 | BigDecimal | 97.41 | **4.52×** | Rjasw2 | compact idiom peer |

<!-- END GENERATED sub-rel-java -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-java-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | sub | SQ | P-gen | x86_64 | thru‡ | 12.56 | BigDecimal | 61.14 | **4.87×** | xRjasw2 | compact idiom peer |
| java | sub | NQ | P-gen | x86_64 | thru‡ | 20.46 | BigDecimal | 88.35 | **4.32×** | xRjasw2 | compact idiom peer |
| java | sub | MQ | P-gen | x86_64 | thru‡ | 42.84 | BigDecimal | 99.92 | **2.33×** | xRjasw2 | compact idiom peer |
| java | sub | OQ | P-gen | x86_64 | thru‡ | 61.25 | BigDecimal | 180.86 | **2.95×** | xRjasw2 | compact idiom peer |
| java | sub | FQ | P-gen | x86_64 | thru‡ | 42.44 | BigDecimal | 208.92 | **4.92×** | xRjasw2 | compact idiom peer |

<!-- END GENERATED sub-rel-java-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-java -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | mul | CP | P-gen | arm64 | thru‡ | 5.01 | BigDecimal | 11.94 | **2.38×** | Rjasw2 | compact idiom peer |
| java | mul | WP | P-gen | arm64 | thru‡ | 24.29 | BigDecimal | 55.86 | **2.30×** | Rjasw2 | compact idiom peer |
| java | mul | XP | P-gen | arm64 | thru‡ | 50.45 | BigDecimal | 158.40 | **3.14×** | Rjasw2 | compact idiom peer |

<!-- END GENERATED mul-rel-java -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-java-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | mul | CP | P-gen | x86_64 | thru‡ | 14.13 | BigDecimal | 38.76 | **2.74×** | xRjasw2 | compact idiom peer |
| java | mul | WP | P-gen | x86_64 | thru‡ | 52.55 | BigDecimal | 151.33 | **2.88×** | xRjasw2 | compact idiom peer |
| java | mul | XP | P-gen | x86_64 | thru‡ | 78.46 | BigDecimal | 281.91 | **3.59×** | xRjasw2 | compact idiom peer |

<!-- END GENERATED mul-rel-java-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-java -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | div | CD | P-gen | arm64 | thru‡ | 31.79 | BigDecimal | 142.39 | **4.48×** | Rjasw2 | compact idiom peer |
| java | div | WD | P-gen | arm64 | thru‡ | 50.12 | BigDecimal | 95.63 | **1.91×** | Rjasw2 | compact idiom peer |
| java | div | XD | P-gen | arm64 | thru‡ | 47.34 | BigDecimal | 224.93 | **4.75×** | Rjasw2 | compact idiom peer |
| java | div | ET | P-gen | arm64 | thru‡ | 12.96 | BigDecimal | 492.33 | **37.99×** | Rjasw2 | compact idiom peer |
| java | div | PT | P-gen | arm64 | thru‡ | 9.83 | BigDecimal | 454.87 | **46.27×** | Rjasw2 | compact idiom peer |

<!-- END GENERATED div-rel-java -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-java-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | div | CD | P-gen | x86_64 | thru‡ | 88.03 | BigDecimal | 369.63 | **4.20×** | xRjasw2 | compact idiom peer |
| java | div | WD | P-gen | x86_64 | thru‡ | 117.29 | BigDecimal | 251.05 | **2.14×** | xRjasw2 | compact idiom peer |
| java | div | XD | P-gen | x86_64 | thru‡ | 124.42 | BigDecimal | 347.70 | **2.79×** | xRjasw2 | compact idiom peer |
| java | div | ET | P-gen | x86_64 | thru‡ | 44.96 | BigDecimal | 1151.20 | **25.60×** | xRjasw2 | compact idiom peer |
| java | div | PT | P-gen | x86_64 | thru‡ | 23.94 | BigDecimal | 1050.40 | **43.88×** | xRjasw2 | compact idiom peer |

<!-- END GENERATED div-rel-java-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-java -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | fma | FN | FMA | arm64 | thru‡ | 105.85 | libbid | 81.22 | **0.77×** | Rjasw2 |  |
| java | fma | FF | FMA | arm64 | thru‡ | 74.85 | libbid | 57.36 | **0.77×** | Rjasw2 |  |

<!-- END GENERATED fma-rel-java -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-java-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | fma | FN | FMA | x86_64 | thru‡ | 220.62 | libbid | 161.79 | **0.73×** | xRjasw2 |  |
| java | fma | FF | FMA | x86_64 | thru‡ | 198.30 | libbid | 124.13 | **0.63×** | xRjasw2 |  |

<!-- END GENERATED fma-rel-java-x86 -->

</div>
