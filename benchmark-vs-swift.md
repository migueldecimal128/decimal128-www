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
| swift | add | MIX | P-fin | arm64 | thru | 2.52 | Foundation.Decimal | 304.31 | **120.76×** | Rswsw2 | compact idiom peer |
| swift | sub | MIX | P-fin | arm64 | thru | 2.67 | Foundation.Decimal | 349.15 | **130.77×** | Rswsw2 | compact idiom peer |
| swift | mul | CP | P-fin | arm64 | thru | 1.60 | Foundation.Decimal | 284.88 | **178.05×** | Rswsw2 | compact idiom peer |
| swift | mul | WP | P-fin | arm64 | thru | 18.00 | Foundation.Decimal | 284.84 | **15.82×** | Rswsw2 | compact idiom peer |
| swift | div | CD | P-fin | arm64 | thru | 35.11 | Foundation.Decimal | 1248.71 | **35.57×** | Rswsw2 | compact idiom peer |
| swift | div | WD | P-fin | arm64 | thru | 47.30 | Foundation.Decimal | 670.22 | **14.17×** | Rswsw2 | compact idiom peer |
| swift | div | ET | P-fin | arm64 | thru | 7.77 | Foundation.Decimal | 3608.80 | **464.45×** | Rswsw2 | compact idiom peer |
| swift | div | PT | P-fin | arm64 | thru | 5.02 | Foundation.Decimal | 3525.30 | **702.25×** | Rswsw2 | compact idiom peer |

<!-- END GENERATED pfin-rel-swift -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-swift-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | add | MIX | P-fin | x86_64 | thru | 7.75 | Foundation.Decimal | 754.43 | **97.35×** | xRswsw2 | compact idiom peer |
| swift | sub | MIX | P-fin | x86_64 | thru | 9.67 | Foundation.Decimal | 896.02 | **92.66×** | xRswsw2 | compact idiom peer |
| swift | mul | CP | P-fin | x86_64 | thru | 3.58 | Foundation.Decimal | 698.92 | **195.23×** | xRswsw2 | compact idiom peer |
| swift | mul | WP | P-fin | x86_64 | thru | 29.83 | Foundation.Decimal | 778.37 | **26.09×** | xRswsw2 | compact idiom peer |
| swift | div | CD | P-fin | x86_64 | thru | 71.10 | Foundation.Decimal | 2961.28 | **41.65×** | xRswsw2 | compact idiom peer |
| swift | div | WD | P-fin | x86_64 | thru | 90.74 | Foundation.Decimal | 1555.19 | **17.14×** | xRswsw2 | compact idiom peer |
| swift | div | ET | P-fin | x86_64 | thru | 19.98 | Foundation.Decimal | 8370.93 | **418.97×** | xRswsw2 | compact idiom peer |
| swift | div | PT | P-fin | x86_64 | thru | 10.76 | Foundation.Decimal | 8161.97 | **758.55×** | xRswsw2 | compact idiom peer |

<!-- END GENERATED pfin-rel-swift-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-swift -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | add | SQ | P-gen | arm64 | thru | 2.41 | Foundation.Decimal | 315.53 | **130.93×** | Rswsw2 | compact idiom peer |
| swift | add | NQ | P-gen | arm64 | thru | 6.20 | Foundation.Decimal | 396.67 | **63.98×** | Rswsw2 | compact idiom peer |
| swift | add | MQ | P-gen | arm64 | thru | 12.41 | Foundation.Decimal | 401.75 | **32.37×** | Rswsw2 | compact idiom peer |
| swift | add | OQ | P-gen | arm64 | thru | 18.92 | Foundation.Decimal | 530.58 | **28.04×** | Rswsw2 | compact idiom peer |
| swift | add | FQ | P-gen | arm64 | thru | 14.35 | Foundation.Decimal | 277.71 | **19.35×** | Rswsw2 | compact idiom peer |

<!-- END GENERATED add-rel-swift -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-swift-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | add | SQ | P-gen | x86_64 | thru | 6.85 | Foundation.Decimal | 772.99 | **112.85×** | xRswsw2 | compact idiom peer |
| swift | add | NQ | P-gen | x86_64 | thru | 12.42 | Foundation.Decimal | 943.19 | **75.94×** | xRswsw2 | compact idiom peer |
| swift | add | MQ | P-gen | x86_64 | thru | 22.72 | Foundation.Decimal | 958.66 | **42.19×** | xRswsw2 | compact idiom peer |
| swift | add | OQ | P-gen | x86_64 | thru | 40.54 | Foundation.Decimal | 1298.26 | **32.02×** | xRswsw2 | compact idiom peer |
| swift | add | FQ | P-gen | x86_64 | thru | 29.56 | Foundation.Decimal | 630.52 | **21.33×** | xRswsw2 | compact idiom peer |

<!-- END GENERATED add-rel-swift-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-swift -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | sub | SQ | P-gen | arm64 | thru | 2.14 | Foundation.Decimal | 320.90 | **149.95×** | Rswsw2 | compact idiom peer |
| swift | sub | NQ | P-gen | arm64 | thru | 5.39 | Foundation.Decimal | 400.99 | **74.40×** | Rswsw2 | compact idiom peer |
| swift | sub | MQ | P-gen | arm64 | thru | 11.22 | Foundation.Decimal | 403.66 | **35.98×** | Rswsw2 | compact idiom peer |
| swift | sub | OQ | P-gen | arm64 | thru | 17.16 | Foundation.Decimal | 531.65 | **30.98×** | Rswsw2 | compact idiom peer |
| swift | sub | FQ | P-gen | arm64 | thru | 13.77 | Foundation.Decimal | 280.37 | **20.36×** | Rswsw2 | compact idiom peer |

<!-- END GENERATED sub-rel-swift -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-swift-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | sub | SQ | P-gen | x86_64 | thru | 7.19 | Foundation.Decimal | 783.44 | **108.96×** | xRswsw2 | compact idiom peer |
| swift | sub | NQ | P-gen | x86_64 | thru | 12.68 | Foundation.Decimal | 951.48 | **75.04×** | xRswsw2 | compact idiom peer |
| swift | sub | MQ | P-gen | x86_64 | thru | 22.10 | Foundation.Decimal | 964.03 | **43.62×** | xRswsw2 | compact idiom peer |
| swift | sub | OQ | P-gen | x86_64 | thru | 39.66 | Foundation.Decimal | 1293.62 | **32.62×** | xRswsw2 | compact idiom peer |
| swift | sub | FQ | P-gen | x86_64 | thru | 29.32 | Foundation.Decimal | 630.12 | **21.49×** | xRswsw2 | compact idiom peer |

<!-- END GENERATED sub-rel-swift-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-swift -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | mul | CP | P-gen | arm64 | thru | 2.24 | Foundation.Decimal | 284.21 | **126.88×** | Rswsw2 | compact idiom peer |
| swift | mul | WP | P-gen | arm64 | thru | 17.11 | Foundation.Decimal | 300.85 | **17.58×** | Rswsw2 | compact idiom peer |
| swift | mul | XP | P-gen | arm64 | thru | 23.97 | Foundation.Decimal | 812.82 | **33.91×** | Rswsw2 | compact idiom peer |

<!-- END GENERATED mul-rel-swift -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-swift-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | mul | CP | P-gen | x86_64 | thru | 5.60 | Foundation.Decimal | 681.56 | **121.71×** | xRswsw2 | compact idiom peer |
| swift | mul | WP | P-gen | x86_64 | thru | 29.83 | Foundation.Decimal | 767.20 | **25.72×** | xRswsw2 | compact idiom peer |
| swift | mul | XP | P-gen | x86_64 | thru | 43.59 | Foundation.Decimal | 2088.27 | **47.91×** | xRswsw2 | compact idiom peer |

<!-- END GENERATED mul-rel-swift-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-swift -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | div | CD | P-gen | arm64 | thru | 34.46 | Foundation.Decimal | 1311.52 | **38.06×** | Rswsw2 | compact idiom peer |
| swift | div | WD | P-gen | arm64 | thru | 46.09 | Foundation.Decimal | 861.69 | **18.70×** | Rswsw2 | compact idiom peer |
| swift | div | XD | P-gen | arm64 | thru | 44.23 | Foundation.Decimal | 657.88 | **14.87×** | Rswsw2 | compact idiom peer |
| swift | div | ET | P-gen | arm64 | thru | 7.80 | Foundation.Decimal | 3084.38 | **395.43×** | Rswsw2 | compact idiom peer |
| swift | div | PT | P-gen | arm64 | thru | 5.05 | Foundation.Decimal | 2982.27 | **590.55×** | Rswsw2 | compact idiom peer |

<!-- END GENERATED div-rel-swift -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-swift-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | div | CD | P-gen | x86_64 | thru | 80.28 | Foundation.Decimal | 3102.71 | **38.65×** | xRswsw2 | compact idiom peer |
| swift | div | WD | P-gen | x86_64 | thru | 91.53 | Foundation.Decimal | 1999.14 | **21.84×** | xRswsw2 | compact idiom peer |
| swift | div | XD | P-gen | x86_64 | thru | 92.59 | Foundation.Decimal | 1489.90 | **16.09×** | xRswsw2 | compact idiom peer |
| swift | div | ET | P-gen | x86_64 | thru | 26.98 | Foundation.Decimal | 7103.88 | **263.30×** | xRswsw2 | compact idiom peer |
| swift | div | PT | P-gen | x86_64 | thru | 10.75 | Foundation.Decimal | 7269.86 | **676.27×** | xRswsw2 | compact idiom peer |

<!-- END GENERATED div-rel-swift-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-swift -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | fma | FN | FMA | arm64 | thru | 88.58 | - | - | - | Rswsw2 |  |
| swift | fma | FF | FMA | arm64 | thru | 42.54 | - | - | - | Rswsw2 |  |

<!-- END GENERATED fma-rel-swift -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-swift-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | fma | FN | FMA | x86_64 | thru | 144.01 | - | - | - | xRswsw2 |  |
| swift | fma | FF | FMA | x86_64 | thru | 83.09 | - | - | - | xRswsw2 |  |

<!-- END GENERATED fma-rel-swift-x86 -->

</div>
