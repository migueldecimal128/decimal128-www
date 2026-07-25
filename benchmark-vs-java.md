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
| java | add | MIX | P-fin | arm64 | thru‡ | 4.48 | BigDecimal | 18.84 | **4.21×** | Rjasw2 | compact idiom peer |
| java | sub | MIX | P-fin | arm64 | thru‡ | 5.42 | BigDecimal | 23.91 | **4.41×** | Rjasw2 | compact idiom peer |
| java | mul | CP | P-fin | arm64 | thru‡ | 4.76 | BigDecimal | 12.32 | **2.59×** | Rjasw2 | compact idiom peer |
| java | mul | WP | P-fin | arm64 | thru‡ | 28.19 | BigDecimal | 63.32 | **2.25×** | Rjasw2 | compact idiom peer |
| java | div | CD | P-fin | arm64 | thru‡ | 36.26 | BigDecimal | 139.32 | **3.84×** | Rjasw2 | compact idiom peer |
| java | div | WD | P-fin | arm64 | thru‡ | 44.12 | BigDecimal | 91.10 | **2.06×** | Rjasw2 | compact idiom peer |
| java | div | ET | P-fin | arm64 | thru‡ | 12.42 | BigDecimal | 499.90 | **40.25×** | Rjasw2 | compact idiom peer |
| java | div | PT | P-fin | arm64 | thru‡ | 9.56 | BigDecimal | 477.30 | **49.93×** | Rjasw2 | compact idiom peer |

<!-- END GENERATED pfin-rel-java -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-java-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | add | MIX | P-fin | x86_64 | thru‡ | 17.92 | BigDecimal | 64.57 | **3.60×** | xRjasw2 | compact idiom peer |
| java | sub | MIX | P-fin | x86_64 | thru‡ | 18.54 | BigDecimal | 75.01 | **4.05×** | xRjasw2 | compact idiom peer |
| java | mul | CP | P-fin | x86_64 | thru‡ | 12.15 | BigDecimal | 40.74 | **3.35×** | xRjasw2 | compact idiom peer |
| java | mul | WP | P-fin | x86_64 | thru‡ | 49.13 | BigDecimal | 153.58 | **3.13×** | xRjasw2 | compact idiom peer |
| java | div | CD | P-fin | x86_64 | thru‡ | 96.84 | BigDecimal | 400.68 | **4.14×** | xRjasw2 | compact idiom peer |
| java | div | WD | P-fin | x86_64 | thru‡ | 121.69 | BigDecimal | 216.89 | **1.78×** | xRjasw2 | compact idiom peer |
| java | div | ET | P-fin | x86_64 | thru‡ | 44.62 | BigDecimal | 1385.89 | **31.06×** | xRjasw2 | compact idiom peer |
| java | div | PT | P-fin | x86_64 | thru‡ | 23.27 | BigDecimal | 1333.78 | **57.32×** | xRjasw2 | compact idiom peer |

<!-- END GENERATED pfin-rel-java-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-java -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | add | SQ | P-gen | arm64 | thru‡ | 5.44 | BigDecimal | 19.21 | **3.53×** | Rjasw2 | compact idiom peer |
| java | add | NQ | P-gen | arm64 | thru‡ | 7.18 | BigDecimal | 31.01 | **4.32×** | Rjasw2 | compact idiom peer |
| java | add | MQ | P-gen | arm64 | thru‡ | 18.59 | BigDecimal | 31.95 | **1.72×** | Rjasw2 | compact idiom peer |
| java | add | OQ | P-gen | arm64 | thru‡ | 29.49 | BigDecimal | 72.93 | **2.47×** | Rjasw2 | compact idiom peer |
| java | add | FQ | P-gen | arm64 | thru‡ | 22.64 | BigDecimal | 87.57 | **3.87×** | Rjasw2 | compact idiom peer |

<!-- END GENERATED add-rel-java -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-java-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | add | SQ | P-gen | x86_64 | thru‡ | 13.59 | BigDecimal | 52.53 | **3.87×** | xRjasw2 | compact idiom peer |
| java | add | NQ | P-gen | x86_64 | thru‡ | 20.44 | BigDecimal | 82.25 | **4.02×** | xRjasw2 | compact idiom peer |
| java | add | MQ | P-gen | x86_64 | thru‡ | 31.84 | BigDecimal | 85.04 | **2.67×** | xRjasw2 | compact idiom peer |
| java | add | OQ | P-gen | x86_64 | thru‡ | 61.66 | BigDecimal | 169.32 | **2.75×** | xRjasw2 | compact idiom peer |
| java | add | FQ | P-gen | x86_64 | thru‡ | 40.76 | BigDecimal | 192.12 | **4.71×** | xRjasw2 | compact idiom peer |

<!-- END GENERATED add-rel-java-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-java -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | sub | SQ | P-gen | arm64 | thru‡ | 4.58 | BigDecimal | 23.47 | **5.12×** | Rjasw2 | compact idiom peer |
| java | sub | NQ | P-gen | arm64 | thru‡ | 7.40 | BigDecimal | 35.40 | **4.78×** | Rjasw2 | compact idiom peer |
| java | sub | MQ | P-gen | arm64 | thru‡ | 18.61 | BigDecimal | 34.41 | **1.85×** | Rjasw2 | compact idiom peer |
| java | sub | OQ | P-gen | arm64 | thru‡ | 28.38 | BigDecimal | 79.52 | **2.80×** | Rjasw2 | compact idiom peer |
| java | sub | FQ | P-gen | arm64 | thru‡ | 20.17 | BigDecimal | 93.47 | **4.63×** | Rjasw2 | compact idiom peer |

<!-- END GENERATED sub-rel-java -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-java-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | sub | SQ | P-gen | x86_64 | thru‡ | 12.45 | BigDecimal | 62.73 | **5.04×** | xRjasw2 | compact idiom peer |
| java | sub | NQ | P-gen | x86_64 | thru‡ | 22.17 | BigDecimal | 89.86 | **4.05×** | xRjasw2 | compact idiom peer |
| java | sub | MQ | P-gen | x86_64 | thru‡ | 33.18 | BigDecimal | 93.98 | **2.83×** | xRjasw2 | compact idiom peer |
| java | sub | OQ | P-gen | x86_64 | thru‡ | 67.62 | BigDecimal | 178.45 | **2.64×** | xRjasw2 | compact idiom peer |
| java | sub | FQ | P-gen | x86_64 | thru‡ | 44.53 | BigDecimal | 197.03 | **4.42×** | xRjasw2 | compact idiom peer |

<!-- END GENERATED sub-rel-java-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-java -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | mul | CP | P-gen | arm64 | thru‡ | 5.34 | BigDecimal | 12.30 | **2.30×** | Rjasw2 | compact idiom peer |
| java | mul | WP | P-gen | arm64 | thru‡ | 25.63 | BigDecimal | 57.65 | **2.25×** | Rjasw2 | compact idiom peer |
| java | mul | XP | P-gen | arm64 | thru‡ | 46.02 | BigDecimal | 155.22 | **3.37×** | Rjasw2 | compact idiom peer |

<!-- END GENERATED mul-rel-java -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-java-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | mul | CP | P-gen | x86_64 | thru‡ | 13.89 | BigDecimal | 40.60 | **2.92×** | xRjasw2 | compact idiom peer |
| java | mul | WP | P-gen | x86_64 | thru‡ | 43.90 | BigDecimal | 147.95 | **3.37×** | xRjasw2 | compact idiom peer |
| java | mul | XP | P-gen | x86_64 | thru‡ | 64.21 | BigDecimal | 267.11 | **4.16×** | xRjasw2 | compact idiom peer |

<!-- END GENERATED mul-rel-java-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-java -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | div | CD | P-gen | arm64 | thru‡ | 30.96 | BigDecimal | 143.62 | **4.64×** | Rjasw2 | compact idiom peer |
| java | div | WD | P-gen | arm64 | thru‡ | 47.63 | BigDecimal | 96.33 | **2.02×** | Rjasw2 | compact idiom peer |
| java | div | XD | P-gen | arm64 | thru‡ | 46.80 | BigDecimal | 222.73 | **4.76×** | Rjasw2 | compact idiom peer |
| java | div | ET | P-gen | arm64 | thru‡ | 13.03 | BigDecimal | 430.04 | **33.00×** | Rjasw2 | compact idiom peer |
| java | div | PT | P-gen | arm64 | thru‡ | 10.08 | BigDecimal | 398.74 | **39.56×** | Rjasw2 | compact idiom peer |

<!-- END GENERATED div-rel-java -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-java-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | div | CD | P-gen | x86_64 | thru‡ | 87.79 | BigDecimal | 352.22 | **4.01×** | xRjasw2 | compact idiom peer |
| java | div | WD | P-gen | x86_64 | thru‡ | 114.89 | BigDecimal | 253.68 | **2.21×** | xRjasw2 | compact idiom peer |
| java | div | XD | P-gen | x86_64 | thru‡ | 121.68 | BigDecimal | 337.33 | **2.77×** | xRjasw2 | compact idiom peer |
| java | div | ET | P-gen | x86_64 | thru‡ | 44.61 | BigDecimal | 1092.65 | **24.49×** | xRjasw2 | compact idiom peer |
| java | div | PT | P-gen | x86_64 | thru‡ | 23.27 | BigDecimal | 1011.76 | **43.48×** | xRjasw2 | compact idiom peer |

<!-- END GENERATED div-rel-java-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-java -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | fma | FN | FMA | arm64 | thru‡ | 102.01 | - | - | - | Rjasw2 |  |
| java | fma | FF | FMA | arm64 | thru‡ | 73.56 | - | - | - | Rjasw2 |  |

<!-- END GENERATED fma-rel-java -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-java-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| java | fma | FN | FMA | x86_64 | thru‡ | 201.54 | - | - | - | xRjasw2 |  |
| java | fma | FF | FMA | x86_64 | thru‡ | 167.67 | - | - | - | xRjasw2 |  |

<!-- END GENERATED fma-rel-java-x86 -->

</div>
