---
layout: default
permalink: /benchmark/vs-swift.html
title: "Swift Benchmark Results — Decimal128"
description: "decimal128 in Swift, measured against the alternatives available to it — a realistic financial mix (P-fin) plus per-operation band characterization, with explicit ratios."
heading: "Swift Benchmark Results"
---

<div class="whitepaper" markdown="1">

<p class="whitepaper-meta">Living document — as-measured results. Category codes, profiles, modes &amp; method: <a href="key.html">Benchmark Key</a>.</p>

This is the **Swift** view of decimal128 **as-measured**, band by band, with explicit ratios. It opens with the realistic financial-mix (**P-fin**) headline, then the per-operation band characterization (**P-gen**) and FMA. In Swift, d128 is measured against its in-language idiom peer **`Foundation.Decimal`** on the compact bands, falling back to the **libbid** universal reference on the wide paths. It is **data only** — the categories, magnitude profiles, units, and methodology are defined in the [Benchmark Key](key.html) (and, authoritatively, `BenchmarkMatrix.md`). The cross-port d128 band-shape matrices (all ports, no alternatives) live in [Port-Comparison Benchmark Results](port-compare.html); the full index of per-language pages is on the [Benchmarks](/benchmarks.html) hub.

## Summary — Ratio Range by Operation

The ratio for Swift's idiom peer on x86_64 (Intel i9-9880H): `ratio = Foundation.Decimal / Miguel` (&gt; 1× ⇒ d128 faster), broken out by operation.

| | Add | Subtract | Multiply | Divide |
|---|---|---|---|---|
| ratio = Foundation.Decimal / Miguel | 107× | 107× | 25× – 181× | 16× – 775× |

## FinMix — realistic financial mix (P-fin)

The headline: one realistic 64-bit financial operation mix — a `MIX` add/sub stream, mul `CP`/`WP`, div `CD`/`WD`/`ET`/`PT` — `ratio = alt / Miguel` (&gt; 1 ⇒ d128 faster). This is the profile closest to real financial code.

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED pfin-rel-swift -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | add | MIX | P-fin | arm64 | thru | 2.72 | Foundation.Decimal | 316.17 | **116.24×** | Rswsw2 | compact idiom peer |
| swift | sub | MIX | P-fin | arm64 | thru | 2.79 | Foundation.Decimal | 361.44 | **129.55×** | Rswsw2 | compact idiom peer |
| swift | mul | CP | P-fin | arm64 | thru | 1.62 | Foundation.Decimal | 296.13 | **182.80×** | Rswsw2 | compact idiom peer |
| swift | mul | WP | P-fin | arm64 | thru | 17.82 | Foundation.Decimal | 297.10 | **16.67×** | Rswsw2 | compact idiom peer |
| swift | div | CD | P-fin | arm64 | thru | 37.32 | Foundation.Decimal | 1285.67 | **34.45×** | Rswsw2 | compact idiom peer |
| swift | div | WD | P-fin | arm64 | thru | 37.60 | Foundation.Decimal | 688.89 | **18.32×** | Rswsw2 | compact idiom peer |
| swift | div | ET | P-fin | arm64 | thru | 7.75 | Foundation.Decimal | 3694.66 | **476.73×** | Rswsw2 | compact idiom peer |
| swift | div | PT | P-fin | arm64 | thru | 6.85 | Foundation.Decimal | 3590.72 | **524.19×** | Rswsw2 | compact idiom peer |

<!-- END GENERATED pfin-rel-swift -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-swift-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | add | MIX | P-fin | x86_64 | thru | 7.66 | Foundation.Decimal | 825.09 | **107.71×** | xRswsw2 | compact idiom peer |
| swift | sub | MIX | P-fin | x86_64 | thru | 8.46 | Foundation.Decimal | 905.82 | **107.07×** | xRswsw2 | compact idiom peer |
| swift | mul | CP | P-fin | x86_64 | thru | 4.17 | Foundation.Decimal | 756.35 | **181.38×** | xRswsw2 | compact idiom peer |
| swift | mul | WP | P-fin | x86_64 | thru | 32.61 | Foundation.Decimal | 845.70 | **25.93×** | xRswsw2 | compact idiom peer |
| swift | div | CD | P-fin | x86_64 | thru | 76.62 | Foundation.Decimal | 3278.26 | **42.79×** | xRswsw2 | compact idiom peer |
| swift | div | WD | P-fin | x86_64 | thru | 99.80 | Foundation.Decimal | 1676.87 | **16.80×** | xRswsw2 | compact idiom peer |
| swift | div | ET | P-fin | x86_64 | thru | 21.37 | Foundation.Decimal | 9412.21 | **440.44×** | xRswsw2 | compact idiom peer |
| swift | div | PT | P-fin | x86_64 | thru | 11.55 | Foundation.Decimal | 8951.48 | **775.02×** | xRswsw2 | compact idiom peer |

<!-- END GENERATED pfin-rel-swift-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-swift -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | add | SQss | P-gen | arm64 | thru | 1.26 | Foundation.Decimal | 300.96 | **238.86×** | Rswsw2 | compact idiom peer |
| swift | add | SQos | P-gen | arm64 | thru | 2.65 | Foundation.Decimal | 348.20 | **131.40×** | Rswsw2 | compact idiom peer |
| swift | add | NQss | P-gen | arm64 | thru | 4.24 | Foundation.Decimal | 380.68 | **89.78×** | Rswsw2 | compact idiom peer |
| swift | add | NQos | P-gen | arm64 | thru | 4.24 | Foundation.Decimal | 430.58 | **101.55×** | Rswsw2 | compact idiom peer |
| swift | add | MQss | P-gen | arm64 | thru | 5.57 | Foundation.Decimal | 384.99 | **69.12×** | Rswsw2 | compact idiom peer |
| swift | add | MQos | P-gen | arm64 | thru | 12.72 | Foundation.Decimal | 435.10 | **34.21×** | Rswsw2 | compact idiom peer |
| swift | add | OQss | P-gen | arm64 | thru | 15.47 | Foundation.Decimal | 517.24 | **33.44×** | Rswsw2 | compact idiom peer |
| swift | add | OQos | P-gen | arm64 | thru | 22.13 | Foundation.Decimal | 570.94 | **25.80×** | Rswsw2 | compact idiom peer |
| swift | add | FQss | P-gen | arm64 | thru | 10.82 | Foundation.Decimal | 285.37 | **26.37×** | Rswsw2 | compact idiom peer |
| swift | add | FQos | P-gen | arm64 | thru | 14.19 | Foundation.Decimal | 287.02 | **20.23×** | Rswsw2 | compact idiom peer |

<!-- END GENERATED add-rel-swift -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-swift-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | add | SQss | P-gen | x86_64 | thru | 2.99 | Foundation.Decimal | 810.26 | **270.99×** | xRswsw2 | compact idiom peer |
| swift | add | SQos | P-gen | x86_64 | thru | 5.69 | Foundation.Decimal | 923.22 | **162.25×** | xRswsw2 | compact idiom peer |
| swift | add | NQss | P-gen | x86_64 | thru | 10.53 | Foundation.Decimal | 1028.94 | **97.72×** | xRswsw2 | compact idiom peer |
| swift | add | NQos | P-gen | x86_64 | thru | 11.50 | Foundation.Decimal | 1105.30 | **96.11×** | xRswsw2 | compact idiom peer |
| swift | add | MQss | P-gen | x86_64 | thru | 16.44 | Foundation.Decimal | 1001.83 | **60.94×** | xRswsw2 | compact idiom peer |
| swift | add | MQos | P-gen | x86_64 | thru | 27.89 | Foundation.Decimal | 1140.21 | **40.88×** | xRswsw2 | compact idiom peer |
| swift | add | OQss | P-gen | x86_64 | thru | 35.76 | Foundation.Decimal | 1438.33 | **40.22×** | xRswsw2 | compact idiom peer |
| swift | add | OQos | P-gen | x86_64 | thru | 48.08 | Foundation.Decimal | 1548.90 | **32.22×** | xRswsw2 | compact idiom peer |
| swift | add | FQss | P-gen | x86_64 | thru | 26.96 | Foundation.Decimal | 733.83 | **27.22×** | xRswsw2 | compact idiom peer |
| swift | add | FQos | P-gen | x86_64 | thru | 32.71 | Foundation.Decimal | 733.68 | **22.43×** | xRswsw2 | compact idiom peer |

<!-- END GENERATED add-rel-swift-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-swift -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | sub | SQss | P-gen | arm64 | thru | 1.61 | Foundation.Decimal | 353.03 | **219.27×** | Rswsw2 | compact idiom peer |
| swift | sub | SQos | P-gen | arm64 | thru | 1.50 | Foundation.Decimal | 298.31 | **198.87×** | Rswsw2 | compact idiom peer |
| swift | sub | NQss | P-gen | arm64 | thru | 3.45 | Foundation.Decimal | 436.59 | **126.55×** | Rswsw2 | compact idiom peer |
| swift | sub | NQos | P-gen | arm64 | thru | 3.44 | Foundation.Decimal | 383.46 | **111.47×** | Rswsw2 | compact idiom peer |
| swift | sub | MQss | P-gen | arm64 | thru | 11.60 | Foundation.Decimal | 441.24 | **38.04×** | Rswsw2 | compact idiom peer |
| swift | sub | MQos | P-gen | arm64 | thru | 4.78 | Foundation.Decimal | 388.72 | **81.32×** | Rswsw2 | compact idiom peer |
| swift | sub | OQss | P-gen | arm64 | thru | 20.90 | Foundation.Decimal | 578.45 | **27.68×** | Rswsw2 | compact idiom peer |
| swift | sub | OQos | P-gen | arm64 | thru | 14.29 | Foundation.Decimal | 520.08 | **36.39×** | Rswsw2 | compact idiom peer |
| swift | sub | FQss | P-gen | arm64 | thru | 13.41 | Foundation.Decimal | 291.91 | **21.77×** | Rswsw2 | compact idiom peer |
| swift | sub | FQos | P-gen | arm64 | thru | 10.49 | Foundation.Decimal | 287.90 | **27.45×** | Rswsw2 | compact idiom peer |

<!-- END GENERATED sub-rel-swift -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-swift-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | sub | SQss | P-gen | x86_64 | thru | 5.11 | Foundation.Decimal | 1058.46 | **207.14×** | xRswsw2 | compact idiom peer |
| swift | sub | SQos | P-gen | x86_64 | thru | 3.73 | Foundation.Decimal | 788.44 | **211.38×** | xRswsw2 | compact idiom peer |
| swift | sub | NQss | P-gen | x86_64 | thru | 11.78 | Foundation.Decimal | 1175.38 | **99.78×** | xRswsw2 | compact idiom peer |
| swift | sub | NQos | P-gen | x86_64 | thru | 10.59 | Foundation.Decimal | 986.28 | **93.13×** | xRswsw2 | compact idiom peer |
| swift | sub | MQss | P-gen | x86_64 | thru | 28.39 | Foundation.Decimal | 1171.33 | **41.26×** | xRswsw2 | compact idiom peer |
| swift | sub | MQos | P-gen | x86_64 | thru | 16.66 | Foundation.Decimal | 993.04 | **59.61×** | xRswsw2 | compact idiom peer |
| swift | sub | OQss | P-gen | x86_64 | thru | 45.79 | Foundation.Decimal | 1543.20 | **33.70×** | xRswsw2 | compact idiom peer |
| swift | sub | OQos | P-gen | x86_64 | thru | 35.71 | Foundation.Decimal | 1441.99 | **40.38×** | xRswsw2 | compact idiom peer |
| swift | sub | FQss | P-gen | x86_64 | thru | 32.62 | Foundation.Decimal | 729.40 | **22.36×** | xRswsw2 | compact idiom peer |
| swift | sub | FQos | P-gen | x86_64 | thru | 26.54 | Foundation.Decimal | 728.66 | **27.46×** | xRswsw2 | compact idiom peer |

<!-- END GENERATED sub-rel-swift-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-swift -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | mul | CP | P-gen | arm64 | thru | 2.44 | Foundation.Decimal | 293.25 | **120.18×** | Rswsw2 | compact idiom peer |
| swift | mul | WP | P-gen | arm64 | thru | 16.97 | Foundation.Decimal | 316.59 | **18.66×** | Rswsw2 | compact idiom peer |
| swift | mul | XP | P-gen | arm64 | thru | 24.01 | Foundation.Decimal | 842.59 | **35.09×** | Rswsw2 | compact idiom peer |

<!-- END GENERATED mul-rel-swift -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-swift-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | mul | CP | P-gen | x86_64 | thru | 6.41 | Foundation.Decimal | 754.60 | **117.72×** | xRswsw2 | compact idiom peer |
| swift | mul | WP | P-gen | x86_64 | thru | 32.66 | Foundation.Decimal | 845.34 | **25.88×** | xRswsw2 | compact idiom peer |
| swift | mul | XP | P-gen | x86_64 | thru | 46.99 | Foundation.Decimal | 2176.17 | **46.31×** | xRswsw2 | compact idiom peer |

<!-- END GENERATED mul-rel-swift-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-swift -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | div | CD | P-gen | arm64 | thru | 36.97 | Foundation.Decimal | 1356.15 | **36.68×** | Rswsw2 | compact idiom peer |
| swift | div | WD | P-gen | arm64 | thru | 36.20 | Foundation.Decimal | 893.21 | **24.67×** | Rswsw2 | compact idiom peer |
| swift | div | XD | P-gen | arm64 | thru | 45.67 | Foundation.Decimal | 684.13 | **14.98×** | Rswsw2 | compact idiom peer |
| swift | div | ET | P-gen | arm64 | thru | 7.75 | Foundation.Decimal | 3222.17 | **415.76×** | Rswsw2 | compact idiom peer |
| swift | div | PT | P-gen | arm64 | thru | 6.84 | Foundation.Decimal | 3083.81 | **450.85×** | Rswsw2 | compact idiom peer |

<!-- END GENERATED div-rel-swift -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-swift-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | div | CD | P-gen | x86_64 | thru | 84.73 | Foundation.Decimal | 3902.26 | **46.06×** | xRswsw2 | compact idiom peer |
| swift | div | WD | P-gen | x86_64 | thru | 113.89 | Foundation.Decimal | 2538.86 | **22.29×** | xRswsw2 | compact idiom peer |
| swift | div | XD | P-gen | x86_64 | thru | 100.42 | Foundation.Decimal | 1672.94 | **16.66×** | xRswsw2 | compact idiom peer |
| swift | div | ET | P-gen | x86_64 | thru | 29.48 | Foundation.Decimal | 7994.08 | **271.17×** | xRswsw2 | compact idiom peer |
| swift | div | PT | P-gen | x86_64 | thru | 11.47 | Foundation.Decimal | 8289.57 | **722.72×** | xRswsw2 | compact idiom peer |

<!-- END GENERATED div-rel-swift-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-swift -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | fma | FN | FMA | arm64 | thru | 40.39 | - | - | - | Rswsw2 |  |
| swift | fma | FF | FMA | arm64 | thru | 42.07 | - | - | - | Rswsw2 |  |

<!-- END GENERATED fma-rel-swift -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-swift-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | fma | FN | FMA | x86_64 | thru | 159.48 | - | - | - | xRswsw2 |  |
| swift | fma | FF | FMA | x86_64 | thru | 88.10 | - | - | - | xRswsw2 |  |

<!-- END GENERATED fma-rel-swift-x86 -->

</div>
