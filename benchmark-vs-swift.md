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
| ratio = Foundation.Decimal / Miguel | 69× | 78× | 21× – 177× | 17× – 644× |

## FinMix — realistic financial mix (P-fin)

The headline: one realistic 64-bit financial operation mix — a `MIX` add/sub stream, mul `CP`/`WP`, div `CD`/`WD`/`ET`/`PT` — `ratio = alt / Miguel` (&gt; 1 ⇒ d128 faster). This is the profile closest to real financial code.

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED pfin-rel-swift -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | add | MIX | P-fin | arm64 | thru | 2.59 | Foundation.Decimal | 302.75 | **116.89×** | Rswsw2 | compact idiom peer |
| swift | sub | MIX | P-fin | arm64 | thru | 2.70 | Foundation.Decimal | 346.72 | **128.41×** | Rswsw2 | compact idiom peer |
| swift | mul | CP | P-fin | arm64 | thru | 1.61 | Foundation.Decimal | 282.88 | **175.70×** | Rswsw2 | compact idiom peer |
| swift | mul | WP | P-fin | arm64 | thru | 17.93 | Foundation.Decimal | 286.10 | **15.96×** | Rswsw2 | compact idiom peer |
| swift | div | CD | P-fin | arm64 | thru | 35.66 | Foundation.Decimal | 1258.70 | **35.30×** | Rswsw2 | compact idiom peer |
| swift | div | WD | P-fin | arm64 | thru | 47.31 | Foundation.Decimal | 675.11 | **14.27×** | Rswsw2 | compact idiom peer |
| swift | div | ET | P-fin | arm64 | thru | 7.77 | Foundation.Decimal | 3631.00 | **467.31×** | Rswsw2 | compact idiom peer |
| swift | div | PT | P-fin | arm64 | thru | 5.04 | Foundation.Decimal | 3549.25 | **704.22×** | Rswsw2 | compact idiom peer |

<!-- END GENERATED pfin-rel-swift -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-swift-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | add | MIX | P-fin | x86_64 | thru | 6.92 | Foundation.Decimal | 755.07 | **109.11×** | xRswsw2 | compact idiom peer |
| swift | sub | MIX | P-fin | x86_64 | thru | 7.65 | Foundation.Decimal | 850.55 | **111.18×** | xRswsw2 | compact idiom peer |
| swift | mul | CP | P-fin | x86_64 | thru | 3.60 | Foundation.Decimal | 689.64 | **191.57×** | xRswsw2 | compact idiom peer |
| swift | mul | WP | P-fin | x86_64 | thru | 29.77 | Foundation.Decimal | 769.68 | **25.85×** | xRswsw2 | compact idiom peer |
| swift | div | CD | P-fin | x86_64 | thru | 70.74 | Foundation.Decimal | 2940.93 | **41.57×** | xRswsw2 | compact idiom peer |
| swift | div | WD | P-fin | x86_64 | thru | 91.17 | Foundation.Decimal | 1542.41 | **16.92×** | xRswsw2 | compact idiom peer |
| swift | div | ET | P-fin | x86_64 | thru | 19.73 | Foundation.Decimal | 8244.88 | **417.89×** | xRswsw2 | compact idiom peer |
| swift | div | PT | P-fin | x86_64 | thru | 10.37 | Foundation.Decimal | 7983.64 | **769.88×** | xRswsw2 | compact idiom peer |

<!-- END GENERATED pfin-rel-swift-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-swift -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | add | SQss | P-gen | arm64 | thru | 1.24 | Foundation.Decimal | 290.46 | **234.24×** | Rswsw2 | compact idiom peer |
| swift | add | SQos | P-gen | arm64 | thru | 2.62 | Foundation.Decimal | 341.77 | **130.45×** | Rswsw2 | compact idiom peer |
| swift | add | NQss | P-gen | arm64 | thru | 4.24 | Foundation.Decimal | 371.45 | **87.61×** | Rswsw2 | compact idiom peer |
| swift | add | NQos | P-gen | arm64 | thru | 4.24 | Foundation.Decimal | 421.21 | **99.34×** | Rswsw2 | compact idiom peer |
| swift | add | MQss | P-gen | arm64 | thru | 5.57 | Foundation.Decimal | 376.68 | **67.63×** | Rswsw2 | compact idiom peer |
| swift | add | MQos | P-gen | arm64 | thru | 12.89 | Foundation.Decimal | 425.67 | **33.02×** | Rswsw2 | compact idiom peer |
| swift | add | OQss | P-gen | arm64 | thru | 15.04 | Foundation.Decimal | 510.43 | **33.94×** | Rswsw2 | compact idiom peer |
| swift | add | OQos | P-gen | arm64 | thru | 22.33 | Foundation.Decimal | 560.76 | **25.11×** | Rswsw2 | compact idiom peer |
| swift | add | FQss | P-gen | arm64 | thru | 11.71 | Foundation.Decimal | 280.97 | **23.99×** | Rswsw2 | compact idiom peer |
| swift | add | FQos | P-gen | arm64 | thru | 13.99 | Foundation.Decimal | 281.07 | **20.09×** | Rswsw2 | compact idiom peer |

<!-- END GENERATED add-rel-swift -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-swift-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | add | SQss | P-gen | x86_64 | thru | 2.44 | Foundation.Decimal | 724.34 | **296.86×** | xRswsw2 | compact idiom peer |
| swift | add | SQos | P-gen | x86_64 | thru | 5.08 | Foundation.Decimal | 828.27 | **163.05×** | xRswsw2 | compact idiom peer |
| swift | add | NQss | P-gen | x86_64 | thru | 9.29 | Foundation.Decimal | 894.64 | **96.30×** | xRswsw2 | compact idiom peer |
| swift | add | NQos | P-gen | x86_64 | thru | 10.03 | Foundation.Decimal | 1010.95 | **100.79×** | xRswsw2 | compact idiom peer |
| swift | add | MQss | P-gen | x86_64 | thru | 15.04 | Foundation.Decimal | 892.55 | **59.35×** | xRswsw2 | compact idiom peer |
| swift | add | MQos | P-gen | x86_64 | thru | 27.79 | Foundation.Decimal | 1068.52 | **38.45×** | xRswsw2 | compact idiom peer |
| swift | add | OQss | P-gen | x86_64 | thru | 32.04 | Foundation.Decimal | 1225.87 | **38.26×** | xRswsw2 | compact idiom peer |
| swift | add | OQos | P-gen | x86_64 | thru | 43.23 | Foundation.Decimal | 1344.02 | **31.09×** | xRswsw2 | compact idiom peer |
| swift | add | FQss | P-gen | x86_64 | thru | 24.54 | Foundation.Decimal | 634.89 | **25.87×** | xRswsw2 | compact idiom peer |
| swift | add | FQos | P-gen | x86_64 | thru | 29.73 | Foundation.Decimal | 645.81 | **21.72×** | xRswsw2 | compact idiom peer |

<!-- END GENERATED add-rel-swift-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-swift -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | sub | SQss | P-gen | arm64 | thru | 1.61 | Foundation.Decimal | 346.89 | **215.46×** | Rswsw2 | compact idiom peer |
| swift | sub | SQos | P-gen | arm64 | thru | 1.48 | Foundation.Decimal | 292.73 | **197.79×** | Rswsw2 | compact idiom peer |
| swift | sub | NQss | P-gen | arm64 | thru | 3.46 | Foundation.Decimal | 428.44 | **123.83×** | Rswsw2 | compact idiom peer |
| swift | sub | NQos | P-gen | arm64 | thru | 3.44 | Foundation.Decimal | 374.06 | **108.74×** | Rswsw2 | compact idiom peer |
| swift | sub | MQss | P-gen | arm64 | thru | 11.62 | Foundation.Decimal | 431.62 | **37.14×** | Rswsw2 | compact idiom peer |
| swift | sub | MQos | P-gen | arm64 | thru | 4.79 | Foundation.Decimal | 379.21 | **79.17×** | Rswsw2 | compact idiom peer |
| swift | sub | OQss | P-gen | arm64 | thru | 20.94 | Foundation.Decimal | 565.54 | **27.01×** | Rswsw2 | compact idiom peer |
| swift | sub | OQos | P-gen | arm64 | thru | 14.10 | Foundation.Decimal | 511.24 | **36.26×** | Rswsw2 | compact idiom peer |
| swift | sub | FQss | P-gen | arm64 | thru | 13.25 | Foundation.Decimal | 284.39 | **21.46×** | Rswsw2 | compact idiom peer |
| swift | sub | FQos | P-gen | arm64 | thru | 10.24 | Foundation.Decimal | 280.36 | **27.38×** | Rswsw2 | compact idiom peer |

<!-- END GENERATED sub-rel-swift -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-swift-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | sub | SQss | P-gen | x86_64 | thru | 4.40 | Foundation.Decimal | 844.21 | **191.87×** | xRswsw2 | compact idiom peer |
| swift | sub | SQos | P-gen | x86_64 | thru | 3.09 | Foundation.Decimal | 715.24 | **231.47×** | xRswsw2 | compact idiom peer |
| swift | sub | NQss | P-gen | x86_64 | thru | 10.16 | Foundation.Decimal | 1011.63 | **99.57×** | xRswsw2 | compact idiom peer |
| swift | sub | NQos | P-gen | x86_64 | thru | 9.46 | Foundation.Decimal | 877.86 | **92.80×** | xRswsw2 | compact idiom peer |
| swift | sub | MQss | P-gen | x86_64 | thru | 25.09 | Foundation.Decimal | 1007.16 | **40.14×** | xRswsw2 | compact idiom peer |
| swift | sub | MQos | P-gen | x86_64 | thru | 15.08 | Foundation.Decimal | 900.10 | **59.69×** | xRswsw2 | compact idiom peer |
| swift | sub | OQss | P-gen | x86_64 | thru | 42.03 | Foundation.Decimal | 1332.53 | **31.70×** | xRswsw2 | compact idiom peer |
| swift | sub | OQos | P-gen | x86_64 | thru | 31.78 | Foundation.Decimal | 1223.11 | **38.49×** | xRswsw2 | compact idiom peer |
| swift | sub | FQss | P-gen | x86_64 | thru | 29.58 | Foundation.Decimal | 637.76 | **21.56×** | xRswsw2 | compact idiom peer |
| swift | sub | FQos | P-gen | x86_64 | thru | 23.95 | Foundation.Decimal | 632.91 | **26.43×** | xRswsw2 | compact idiom peer |

<!-- END GENERATED sub-rel-swift-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-swift -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | mul | CP | P-gen | arm64 | thru | 2.28 | Foundation.Decimal | 286.00 | **125.44×** | Rswsw2 | compact idiom peer |
| swift | mul | WP | P-gen | arm64 | thru | 17.01 | Foundation.Decimal | 303.68 | **17.85×** | Rswsw2 | compact idiom peer |
| swift | mul | XP | P-gen | arm64 | thru | 24.01 | Foundation.Decimal | 825.85 | **34.40×** | Rswsw2 | compact idiom peer |

<!-- END GENERATED mul-rel-swift -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-swift-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | mul | CP | P-gen | x86_64 | thru | 5.66 | Foundation.Decimal | 673.38 | **118.97×** | xRswsw2 | compact idiom peer |
| swift | mul | WP | P-gen | x86_64 | thru | 29.66 | Foundation.Decimal | 769.46 | **25.94×** | xRswsw2 | compact idiom peer |
| swift | mul | XP | P-gen | x86_64 | thru | 42.94 | Foundation.Decimal | 1961.85 | **45.69×** | xRswsw2 | compact idiom peer |

<!-- END GENERATED mul-rel-swift-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-swift -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | div | CD | P-gen | arm64 | thru | 35.31 | Foundation.Decimal | 1322.98 | **37.47×** | Rswsw2 | compact idiom peer |
| swift | div | WD | P-gen | arm64 | thru | 46.90 | Foundation.Decimal | 873.28 | **18.62×** | Rswsw2 | compact idiom peer |
| swift | div | XD | P-gen | arm64 | thru | 44.89 | Foundation.Decimal | 664.61 | **14.81×** | Rswsw2 | compact idiom peer |
| swift | div | ET | P-gen | arm64 | thru | 7.77 | Foundation.Decimal | 3115.42 | **400.95×** | Rswsw2 | compact idiom peer |
| swift | div | PT | P-gen | arm64 | thru | 5.02 | Foundation.Decimal | 3013.94 | **600.39×** | Rswsw2 | compact idiom peer |

<!-- END GENERATED div-rel-swift -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-swift-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | div | CD | P-gen | x86_64 | thru | 78.30 | Foundation.Decimal | 3095.28 | **39.53×** | xRswsw2 | compact idiom peer |
| swift | div | WD | P-gen | x86_64 | thru | 91.05 | Foundation.Decimal | 1979.46 | **21.74×** | xRswsw2 | compact idiom peer |
| swift | div | XD | P-gen | x86_64 | thru | 92.84 | Foundation.Decimal | 1476.69 | **15.91×** | xRswsw2 | compact idiom peer |
| swift | div | ET | P-gen | x86_64 | thru | 26.92 | Foundation.Decimal | 7078.23 | **262.94×** | xRswsw2 | compact idiom peer |
| swift | div | PT | P-gen | x86_64 | thru | 10.55 | Foundation.Decimal | 6961.89 | **659.89×** | xRswsw2 | compact idiom peer |

<!-- END GENERATED div-rel-swift-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-swift -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | fma | FN | FMA | arm64 | thru | 89.90 | - | - | - | Rswsw2 |  |
| swift | fma | FF | FMA | arm64 | thru | 42.70 | - | - | - | Rswsw2 |  |

<!-- END GENERATED fma-rel-swift -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-swift-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | fma | FN | FMA | x86_64 | thru | 145.47 | - | - | - | xRswsw2 |  |
| swift | fma | FF | FMA | x86_64 | thru | 81.06 | - | - | - | xRswsw2 |  |

<!-- END GENERATED fma-rel-swift-x86 -->

</div>
