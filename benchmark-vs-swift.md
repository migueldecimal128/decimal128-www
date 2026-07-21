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

The ratio for Swift's idiom peer on x86_64 (Intel i9-9880H): `ratio = Foundation.Decimal / ours` (&gt; 1× ⇒ d128 faster), broken out by operation.

| | Add | Subtract | Multiply | Divide |
|---|---|---|---|---|
| ratio = Foundation.Decimal / Miguel | 69× | 78× | 21× – 177× | 17× – 644× |

## FinMix — realistic financial mix (P-fin)

The headline: one realistic 64-bit financial operation mix — a `MIX` add/sub stream, mul `CP`/`WP`, div `CD`/`WD`/`ET`/`PT` — `ratio = alt / ours` (&gt; 1 ⇒ d128 faster). This is the profile closest to real financial code.

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED pfin-rel-swift -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | add | MIX | P-fin | arm64 | thru | 4.16 | Foundation.Decimal | 337.29 | **81.08×** | Rswsw2 | compact idiom peer |
| swift | sub | MIX | P-fin | arm64 | thru | 3.07 | Foundation.Decimal | 341.16 | **111.13×** | Rswsw2 | compact idiom peer |
| swift | mul | CP | P-fin | arm64 | thru | 1.78 | Foundation.Decimal | 293.46 | **164.87×** | Rswsw2 | compact idiom peer |
| swift | mul | WP | P-fin | arm64 | thru | 22.01 | Foundation.Decimal | 294.61 | **13.39×** | Rswsw2 | compact idiom peer |
| swift | div | CD | P-fin | arm64 | thru | 35.90 | Foundation.Decimal | 1291.90 | **35.99×** | Rswsw2 | compact idiom peer |
| swift | div | WD | P-fin | arm64 | thru | 48.13 | Foundation.Decimal | 693.33 | **14.41×** | Rswsw2 | compact idiom peer |
| swift | div | ET | P-fin | arm64 | thru | 8.53 | Foundation.Decimal | 3720.17 | **436.13×** | Rswsw2 | compact idiom peer |
| swift | div | PT | P-fin | arm64 | thru | 7.62 | Foundation.Decimal | 3623.83 | **475.57×** | Rswsw2 | compact idiom peer |

<!-- END GENERATED pfin-rel-swift -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-swift-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | add | MIX | P-fin | x86_64 | thru | 11.60 | Foundation.Decimal | 804.37 | **69.34×** | xRswsw2 | compact idiom peer |
| swift | sub | MIX | P-fin | x86_64 | thru | 9.91 | Foundation.Decimal | 771.75 | **77.88×** | xRswsw2 | compact idiom peer |
| swift | mul | CP | P-fin | x86_64 | thru | 3.90 | Foundation.Decimal | 689.76 | **176.86×** | xRswsw2 | compact idiom peer |
| swift | mul | WP | P-fin | x86_64 | thru | 35.41 | Foundation.Decimal | 752.01 | **21.24×** | xRswsw2 | compact idiom peer |
| swift | div | CD | P-fin | x86_64 | thru | 70.24 | Foundation.Decimal | 2939.77 | **41.85×** | xRswsw2 | compact idiom peer |
| swift | div | WD | P-fin | x86_64 | thru | 91.35 | Foundation.Decimal | 1512.92 | **16.56×** | xRswsw2 | compact idiom peer |
| swift | div | ET | P-fin | x86_64 | thru | 21.86 | Foundation.Decimal | 8453.28 | **386.70×** | xRswsw2 | compact idiom peer |
| swift | div | PT | P-fin | x86_64 | thru | 12.72 | Foundation.Decimal | 8190.50 | **643.91×** | xRswsw2 | compact idiom peer |

<!-- END GENERATED pfin-rel-swift-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-swift -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | add | SQ | P-gen | arm64 | thru | 4.15 | Foundation.Decimal | 306.15 | **73.77×** | Rswsw2 | compact idiom peer |
| swift | add | NQ | P-gen | arm64 | thru | 5.99 | Foundation.Decimal | 386.53 | **64.53×** | Rswsw2 | compact idiom peer |
| swift | add | MQ | P-gen | arm64 | thru | 15.93 | Foundation.Decimal | 392.09 | **24.61×** | Rswsw2 | compact idiom peer |
| swift | add | OQ | P-gen | arm64 | thru | 17.68 | Foundation.Decimal | 522.39 | **29.55×** | Rswsw2 | compact idiom peer |
| swift | add | FQ | P-gen | arm64 | thru | 12.84 | Foundation.Decimal | 271.65 | **21.16×** | Rswsw2 | compact idiom peer |

<!-- END GENERATED add-rel-swift -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-swift-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | add | SQ | P-gen | x86_64 | thru | 9.50 | Foundation.Decimal | 789.25 | **83.08×** | xRswsw2 | compact idiom peer |
| swift | add | NQ | P-gen | x86_64 | thru | 13.55 | Foundation.Decimal | 949.79 | **70.10×** | xRswsw2 | compact idiom peer |
| swift | add | MQ | P-gen | x86_64 | thru | 28.91 | Foundation.Decimal | 959.17 | **33.18×** | xRswsw2 | compact idiom peer |
| swift | add | OQ | P-gen | x86_64 | thru | 40.41 | Foundation.Decimal | 1286.86 | **31.85×** | xRswsw2 | compact idiom peer |
| swift | add | FQ | P-gen | x86_64 | thru | 29.03 | Foundation.Decimal | 626.53 | **21.58×** | xRswsw2 | compact idiom peer |

<!-- END GENERATED add-rel-swift-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-swift -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | sub | SQ | P-gen | arm64 | thru | 2.58 | Foundation.Decimal | 312.74 | **121.22×** | Rswsw2 | compact idiom peer |
| swift | sub | NQ | P-gen | arm64 | thru | 5.61 | Foundation.Decimal | 388.64 | **69.28×** | Rswsw2 | compact idiom peer |
| swift | sub | MQ | P-gen | arm64 | thru | 15.39 | Foundation.Decimal | 396.68 | **25.78×** | Rswsw2 | compact idiom peer |
| swift | sub | OQ | P-gen | arm64 | thru | 17.42 | Foundation.Decimal | 522.49 | **29.99×** | Rswsw2 | compact idiom peer |
| swift | sub | FQ | P-gen | arm64 | thru | 12.97 | Foundation.Decimal | 274.32 | **21.15×** | Rswsw2 | compact idiom peer |

<!-- END GENERATED sub-rel-swift -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-swift-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | sub | SQ | P-gen | x86_64 | thru | 7.72 | Foundation.Decimal | 775.21 | **100.42×** | xRswsw2 | compact idiom peer |
| swift | sub | NQ | P-gen | x86_64 | thru | 14.40 | Foundation.Decimal | 1002.85 | **69.64×** | xRswsw2 | compact idiom peer |
| swift | sub | MQ | P-gen | x86_64 | thru | 30.22 | Foundation.Decimal | 976.20 | **32.30×** | xRswsw2 | compact idiom peer |
| swift | sub | OQ | P-gen | x86_64 | thru | 41.28 | Foundation.Decimal | 1360.36 | **32.95×** | xRswsw2 | compact idiom peer |
| swift | sub | FQ | P-gen | x86_64 | thru | 29.56 | Foundation.Decimal | 634.49 | **21.46×** | xRswsw2 | compact idiom peer |

<!-- END GENERATED sub-rel-swift-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-swift -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | mul | CP | P-gen | arm64 | thru | 4.06 | Foundation.Decimal | 277.54 | **68.36×** | Rswsw2 | compact idiom peer |
| swift | mul | WP | P-gen | arm64 | thru | 20.99 | Foundation.Decimal | 294.38 | **14.02×** | Rswsw2 | compact idiom peer |
| swift | mul | XP | P-gen | arm64 | thru | 27.65 | Foundation.Decimal | 798.35 | **28.87×** | Rswsw2 | compact idiom peer |

<!-- END GENERATED mul-rel-swift -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-swift-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | mul | CP | P-gen | x86_64 | thru | 6.56 | Foundation.Decimal | 674.34 | **102.80×** | xRswsw2 | compact idiom peer |
| swift | mul | WP | P-gen | x86_64 | thru | 35.16 | Foundation.Decimal | 772.76 | **21.98×** | xRswsw2 | compact idiom peer |
| swift | mul | XP | P-gen | x86_64 | thru | 53.78 | Foundation.Decimal | 1998.35 | **37.16×** | xRswsw2 | compact idiom peer |

<!-- END GENERATED mul-rel-swift-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-swift -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | div | CD | P-gen | arm64 | thru | 33.87 | Foundation.Decimal | 1289.57 | **38.07×** | Rswsw2 | compact idiom peer |
| swift | div | WD | P-gen | arm64 | thru | 44.84 | Foundation.Decimal | 846.47 | **18.88×** | Rswsw2 | compact idiom peer |
| swift | div | XD | P-gen | arm64 | thru | 44.18 | Foundation.Decimal | 681.51 | **15.43×** | Rswsw2 | compact idiom peer |
| swift | div | ET | P-gen | arm64 | thru | 8.53 | Foundation.Decimal | 3204.05 | **375.62×** | Rswsw2 | compact idiom peer |
| swift | div | PT | P-gen | arm64 | thru | 7.63 | Foundation.Decimal | 3093.81 | **405.48×** | Rswsw2 | compact idiom peer |

<!-- END GENERATED div-rel-swift -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-swift-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | div | CD | P-gen | x86_64 | thru | 71.35 | Foundation.Decimal | 3051.77 | **42.77×** | xRswsw2 | compact idiom peer |
| swift | div | WD | P-gen | x86_64 | thru | 97.19 | Foundation.Decimal | 2064.40 | **21.24×** | xRswsw2 | compact idiom peer |
| swift | div | XD | P-gen | x86_64 | thru | 91.69 | Foundation.Decimal | 1485.98 | **16.21×** | xRswsw2 | compact idiom peer |
| swift | div | ET | P-gen | x86_64 | thru | 29.37 | Foundation.Decimal | 7272.49 | **247.62×** | xRswsw2 | compact idiom peer |
| swift | div | PT | P-gen | x86_64 | thru | 12.33 | Foundation.Decimal | 6794.60 | **551.06×** | xRswsw2 | compact idiom peer |

<!-- END GENERATED div-rel-swift-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-swift -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | fma | FN | FMA | arm64 | thru | 85.36 | libbid | 82.34 | **0.96×** | Rswsw2 |  |
| swift | fma | FF | FMA | arm64 | thru | 44.53 | libbid | 59.70 | **1.34×** | Rswsw2 |  |

<!-- END GENERATED fma-rel-swift -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-swift-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | fma | FN | FMA | x86_64 | thru | 151.33 | libbid | 161.79 | **1.07×** | xRswsw2 |  |
| swift | fma | FF | FMA | x86_64 | thru | 85.41 | libbid | 124.13 | **1.45×** | xRswsw2 |  |

<!-- END GENERATED fma-rel-swift-x86 -->

</div>
