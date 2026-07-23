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
| swift | add | MIX | P-fin | arm64 | thru | 6.15 | Foundation.Decimal | 338.09 | **54.97×** | Rswsw2 | compact idiom peer |
| swift | sub | MIX | P-fin | arm64 | thru | 4.89 | Foundation.Decimal | 341.45 | **69.83×** | Rswsw2 | compact idiom peer |
| swift | mul | CP | P-fin | arm64 | thru | 2.17 | Foundation.Decimal | 293.92 | **135.45×** | Rswsw2 | compact idiom peer |
| swift | mul | WP | P-fin | arm64 | thru | 21.77 | Foundation.Decimal | 288.46 | **13.25×** | Rswsw2 | compact idiom peer |
| swift | div | CD | P-fin | arm64 | thru | 36.12 | Foundation.Decimal | 1242.99 | **34.41×** | Rswsw2 | compact idiom peer |
| swift | div | WD | P-fin | arm64 | thru | 48.93 | Foundation.Decimal | 666.00 | **13.61×** | Rswsw2 | compact idiom peer |
| swift | div | ET | P-fin | arm64 | thru | 10.58 | Foundation.Decimal | 3568.14 | **337.25×** | Rswsw2 | compact idiom peer |
| swift | div | PT | P-fin | arm64 | thru | 7.07 | Foundation.Decimal | 3488.89 | **493.48×** | Rswsw2 | compact idiom peer |

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
| swift | add | SQ | P-gen | arm64 | thru | 5.79 | Foundation.Decimal | 317.15 | **54.78×** | Rswsw2 | compact idiom peer |
| swift | add | NQ | P-gen | arm64 | thru | 8.61 | Foundation.Decimal | 397.93 | **46.22×** | Rswsw2 | compact idiom peer |
| swift | add | MQ | P-gen | arm64 | thru | 14.73 | Foundation.Decimal | 401.87 | **27.28×** | Rswsw2 | compact idiom peer |
| swift | add | OQ | P-gen | arm64 | thru | 20.41 | Foundation.Decimal | 532.08 | **26.07×** | Rswsw2 | compact idiom peer |
| swift | add | FQ | P-gen | arm64 | thru | 16.45 | Foundation.Decimal | 278.72 | **16.94×** | Rswsw2 | compact idiom peer |

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
| swift | sub | SQ | P-gen | arm64 | thru | 5.50 | Foundation.Decimal | 321.49 | **58.45×** | Rswsw2 | compact idiom peer |
| swift | sub | NQ | P-gen | arm64 | thru | 7.77 | Foundation.Decimal | 402.23 | **51.77×** | Rswsw2 | compact idiom peer |
| swift | sub | MQ | P-gen | arm64 | thru | 14.27 | Foundation.Decimal | 406.03 | **28.45×** | Rswsw2 | compact idiom peer |
| swift | sub | OQ | P-gen | arm64 | thru | 19.27 | Foundation.Decimal | 533.93 | **27.71×** | Rswsw2 | compact idiom peer |
| swift | sub | FQ | P-gen | arm64 | thru | 15.61 | Foundation.Decimal | 281.96 | **18.06×** | Rswsw2 | compact idiom peer |

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
| swift | mul | CP | P-gen | arm64 | thru | 3.30 | Foundation.Decimal | 284.13 | **86.10×** | Rswsw2 | compact idiom peer |
| swift | mul | WP | P-gen | arm64 | thru | 21.26 | Foundation.Decimal | 303.20 | **14.26×** | Rswsw2 | compact idiom peer |
| swift | mul | XP | P-gen | arm64 | thru | 28.43 | Foundation.Decimal | 815.48 | **28.68×** | Rswsw2 | compact idiom peer |

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
| swift | div | CD | P-gen | arm64 | thru | 36.26 | Foundation.Decimal | 1308.06 | **36.07×** | Rswsw2 | compact idiom peer |
| swift | div | WD | P-gen | arm64 | thru | 48.21 | Foundation.Decimal | 860.87 | **17.86×** | Rswsw2 | compact idiom peer |
| swift | div | XD | P-gen | arm64 | thru | 46.65 | Foundation.Decimal | 659.74 | **14.14×** | Rswsw2 | compact idiom peer |
| swift | div | ET | P-gen | arm64 | thru | 10.58 | Foundation.Decimal | 3094.90 | **292.52×** | Rswsw2 | compact idiom peer |
| swift | div | PT | P-gen | arm64 | thru | 7.07 | Foundation.Decimal | 2994.41 | **423.54×** | Rswsw2 | compact idiom peer |

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
| swift | fma | FN | FMA | arm64 | thru | 88.59 | libbid | 81.22 | **0.92×** | Rswsw2 |  |
| swift | fma | FF | FMA | arm64 | thru | 45.22 | libbid | 57.36 | **1.27×** | Rswsw2 |  |

<!-- END GENERATED fma-rel-swift -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-swift-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | fma | FN | FMA | x86_64 | thru | 151.33 | libbid | 161.79 | **1.07×** | xRswsw2 |  |
| swift | fma | FF | FMA | x86_64 | thru | 85.41 | libbid | 124.13 | **1.45×** | xRswsw2 |  |

<!-- END GENERATED fma-rel-swift-x86 -->

</div>
