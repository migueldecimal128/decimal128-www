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
| swift | add | MIX | P-fin | x86_64 | thru | 7.23 | Foundation.Decimal | 741.13 | **102.51×** | xRswsw2 | compact idiom peer |
| swift | sub | MIX | P-fin | x86_64 | thru | 7.96 | Foundation.Decimal | 849.75 | **106.75×** | xRswsw2 | compact idiom peer |
| swift | mul | CP | P-fin | x86_64 | thru | 3.62 | Foundation.Decimal | 731.34 | **202.03×** | xRswsw2 | compact idiom peer |
| swift | mul | WP | P-fin | x86_64 | thru | 37.20 | Foundation.Decimal | 838.29 | **22.53×** | xRswsw2 | compact idiom peer |
| swift | div | CD | P-fin | x86_64 | thru | 75.33 | Foundation.Decimal | 3103.36 | **41.20×** | xRswsw2 | compact idiom peer |
| swift | div | WD | P-fin | x86_64 | thru | 93.55 | Foundation.Decimal | 1554.43 | **16.62×** | xRswsw2 | compact idiom peer |
| swift | div | ET | P-fin | x86_64 | thru | 20.51 | Foundation.Decimal | 8662.66 | **422.36×** | xRswsw2 | compact idiom peer |
| swift | div | PT | P-fin | x86_64 | thru | 11.01 | Foundation.Decimal | 8181.90 | **743.13×** | xRswsw2 | compact idiom peer |

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
| swift | add | SQss | P-gen | x86_64 | thru | 2.56 | Foundation.Decimal | 741.31 | **289.57×** | xRswsw2 | compact idiom peer |
| swift | add | SQos | P-gen | x86_64 | thru | 5.32 | Foundation.Decimal | 832.90 | **156.56×** | xRswsw2 | compact idiom peer |
| swift | add | NQss | P-gen | x86_64 | thru | 9.44 | Foundation.Decimal | 926.06 | **98.10×** | xRswsw2 | compact idiom peer |
| swift | add | NQos | P-gen | x86_64 | thru | 10.65 | Foundation.Decimal | 1034.81 | **97.17×** | xRswsw2 | compact idiom peer |
| swift | add | MQss | P-gen | x86_64 | thru | 15.83 | Foundation.Decimal | 986.75 | **62.33×** | xRswsw2 | compact idiom peer |
| swift | add | MQos | P-gen | x86_64 | thru | 26.44 | Foundation.Decimal | 1077.93 | **40.77×** | xRswsw2 | compact idiom peer |
| swift | add | OQss | P-gen | x86_64 | thru | 33.12 | Foundation.Decimal | 1321.25 | **39.89×** | xRswsw2 | compact idiom peer |
| swift | add | OQos | P-gen | x86_64 | thru | 48.10 | Foundation.Decimal | 1460.39 | **30.36×** | xRswsw2 | compact idiom peer |
| swift | add | FQss | P-gen | x86_64 | thru | 25.33 | Foundation.Decimal | 676.71 | **26.72×** | xRswsw2 | compact idiom peer |
| swift | add | FQos | P-gen | x86_64 | thru | 30.82 | Foundation.Decimal | 642.13 | **20.83×** | xRswsw2 | compact idiom peer |

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
| swift | sub | SQss | P-gen | x86_64 | thru | 4.71 | Foundation.Decimal | 881.14 | **187.08×** | xRswsw2 | compact idiom peer |
| swift | sub | SQos | P-gen | x86_64 | thru | 3.12 | Foundation.Decimal | 742.69 | **238.04×** | xRswsw2 | compact idiom peer |
| swift | sub | NQss | P-gen | x86_64 | thru | 10.64 | Foundation.Decimal | 1052.92 | **98.96×** | xRswsw2 | compact idiom peer |
| swift | sub | NQos | P-gen | x86_64 | thru | 10.07 | Foundation.Decimal | 982.93 | **97.61×** | xRswsw2 | compact idiom peer |
| swift | sub | MQss | P-gen | x86_64 | thru | 28.07 | Foundation.Decimal | 1067.03 | **38.01×** | xRswsw2 | compact idiom peer |
| swift | sub | MQos | P-gen | x86_64 | thru | 15.40 | Foundation.Decimal | 938.93 | **60.97×** | xRswsw2 | compact idiom peer |
| swift | sub | OQss | P-gen | x86_64 | thru | 44.93 | Foundation.Decimal | 1447.86 | **32.22×** | xRswsw2 | compact idiom peer |
| swift | sub | OQos | P-gen | x86_64 | thru | 34.17 | Foundation.Decimal | 1332.28 | **38.99×** | xRswsw2 | compact idiom peer |
| swift | sub | FQss | P-gen | x86_64 | thru | 31.44 | Foundation.Decimal | 680.71 | **21.65×** | xRswsw2 | compact idiom peer |
| swift | sub | FQos | P-gen | x86_64 | thru | 25.55 | Foundation.Decimal | 657.92 | **25.75×** | xRswsw2 | compact idiom peer |

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
| swift | mul | CP | P-gen | x86_64 | thru | 6.13 | Foundation.Decimal | 722.72 | **117.90×** | xRswsw2 | compact idiom peer |
| swift | mul | WP | P-gen | x86_64 | thru | 30.01 | Foundation.Decimal | 817.84 | **27.25×** | xRswsw2 | compact idiom peer |
| swift | mul | XP | P-gen | x86_64 | thru | 45.67 | Foundation.Decimal | 2001.85 | **43.83×** | xRswsw2 | compact idiom peer |

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
| swift | div | CD | P-gen | x86_64 | thru | 83.15 | Foundation.Decimal | 3307.56 | **39.78×** | xRswsw2 | compact idiom peer |
| swift | div | WD | P-gen | x86_64 | thru | 94.28 | Foundation.Decimal | 2130.40 | **22.60×** | xRswsw2 | compact idiom peer |
| swift | div | XD | P-gen | x86_64 | thru | 99.44 | Foundation.Decimal | 1619.23 | **16.28×** | xRswsw2 | compact idiom peer |
| swift | div | ET | P-gen | x86_64 | thru | 29.40 | Foundation.Decimal | 7409.24 | **252.01×** | xRswsw2 | compact idiom peer |
| swift | div | PT | P-gen | x86_64 | thru | 10.82 | Foundation.Decimal | 7238.86 | **669.03×** | xRswsw2 | compact idiom peer |

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
| swift | fma | FN | FMA | x86_64 | thru | 145.85 | - | - | - | xRswsw2 |  |
| swift | fma | FF | FMA | x86_64 | thru | 82.19 | - | - | - | xRswsw2 |  |

<!-- END GENERATED fma-rel-swift-x86 -->

</div>
