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
| swift | add | MIX | P-fin | arm64 | thru | 5.88 | Foundation.Decimal | 322.48 | **54.84×** | Rswsw2 | compact idiom peer |
| swift | sub | MIX | P-fin | arm64 | thru | 4.88 | Foundation.Decimal | 326.44 | **66.89×** | Rswsw2 | compact idiom peer |
| swift | mul | CP | P-fin | arm64 | thru | 2.16 | Foundation.Decimal | 279.55 | **129.42×** | Rswsw2 | compact idiom peer |
| swift | mul | WP | P-fin | arm64 | thru | 21.02 | Foundation.Decimal | 283.48 | **13.49×** | Rswsw2 | compact idiom peer |
| swift | div | CD | P-fin | arm64 | thru | 36.05 | Foundation.Decimal | 1242.58 | **34.47×** | Rswsw2 | compact idiom peer |
| swift | div | WD | P-fin | arm64 | thru | 48.91 | Foundation.Decimal | 664.99 | **13.60×** | Rswsw2 | compact idiom peer |
| swift | div | ET | P-fin | arm64 | thru | 10.59 | Foundation.Decimal | 3577.28 | **337.80×** | Rswsw2 | compact idiom peer |
| swift | div | PT | P-fin | arm64 | thru | 7.00 | Foundation.Decimal | 3491.84 | **498.83×** | Rswsw2 | compact idiom peer |

<!-- END GENERATED pfin-rel-swift -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-swift-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | add | MIX | P-fin | x86_64 | thru | 13.83 | Foundation.Decimal | 816.55 | **59.04×** | xRswsw2 | compact idiom peer |
| swift | sub | MIX | P-fin | x86_64 | thru | 11.19 | Foundation.Decimal | 809.11 | **72.31×** | xRswsw2 | compact idiom peer |
| swift | mul | CP | P-fin | x86_64 | thru | 4.51 | Foundation.Decimal | 697.00 | **154.55×** | xRswsw2 | compact idiom peer |
| swift | mul | WP | P-fin | x86_64 | thru | 36.27 | Foundation.Decimal | 793.46 | **21.88×** | xRswsw2 | compact idiom peer |
| swift | div | CD | P-fin | x86_64 | thru | 79.58 | Foundation.Decimal | 3004.34 | **37.75×** | xRswsw2 | compact idiom peer |
| swift | div | WD | P-fin | x86_64 | thru | 98.39 | Foundation.Decimal | 1620.20 | **16.47×** | xRswsw2 | compact idiom peer |
| swift | div | ET | P-fin | x86_64 | thru | 26.57 | Foundation.Decimal | 8481.12 | **319.20×** | xRswsw2 | compact idiom peer |
| swift | div | PT | P-fin | x86_64 | thru | 15.90 | Foundation.Decimal | 8433.84 | **530.43×** | xRswsw2 | compact idiom peer |

<!-- END GENERATED pfin-rel-swift-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-swift -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | add | SQ | P-gen | arm64 | thru | 5.82 | Foundation.Decimal | 318.97 | **54.81×** | Rswsw2 | compact idiom peer |
| swift | add | NQ | P-gen | arm64 | thru | 8.14 | Foundation.Decimal | 399.23 | **49.05×** | Rswsw2 | compact idiom peer |
| swift | add | MQ | P-gen | arm64 | thru | 14.79 | Foundation.Decimal | 420.39 | **28.42×** | Rswsw2 | compact idiom peer |
| swift | add | OQ | P-gen | arm64 | thru | 20.41 | Foundation.Decimal | 557.82 | **27.33×** | Rswsw2 | compact idiom peer |
| swift | add | FQ | P-gen | arm64 | thru | 16.37 | Foundation.Decimal | 293.90 | **17.95×** | Rswsw2 | compact idiom peer |

<!-- END GENERATED add-rel-swift -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-swift-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | add | SQ | P-gen | x86_64 | thru | 10.85 | Foundation.Decimal | 839.91 | **77.41×** | xRswsw2 | compact idiom peer |
| swift | add | NQ | P-gen | x86_64 | thru | 16.69 | Foundation.Decimal | 966.03 | **57.88×** | xRswsw2 | compact idiom peer |
| swift | add | MQ | P-gen | x86_64 | thru | 26.77 | Foundation.Decimal | 1011.72 | **37.79×** | xRswsw2 | compact idiom peer |
| swift | add | OQ | P-gen | x86_64 | thru | 47.48 | Foundation.Decimal | 1374.77 | **28.95×** | xRswsw2 | compact idiom peer |
| swift | add | FQ | P-gen | x86_64 | thru | 34.25 | Foundation.Decimal | 680.99 | **19.88×** | xRswsw2 | compact idiom peer |

<!-- END GENERATED add-rel-swift-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-swift -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | sub | SQ | P-gen | arm64 | thru | 5.48 | Foundation.Decimal | 322.24 | **58.80×** | Rswsw2 | compact idiom peer |
| swift | sub | NQ | P-gen | arm64 | thru | 7.78 | Foundation.Decimal | 402.44 | **51.73×** | Rswsw2 | compact idiom peer |
| swift | sub | MQ | P-gen | arm64 | thru | 14.38 | Foundation.Decimal | 423.93 | **29.48×** | Rswsw2 | compact idiom peer |
| swift | sub | OQ | P-gen | arm64 | thru | 19.58 | Foundation.Decimal | 559.63 | **28.58×** | Rswsw2 | compact idiom peer |
| swift | sub | FQ | P-gen | arm64 | thru | 15.62 | Foundation.Decimal | 294.97 | **18.88×** | Rswsw2 | compact idiom peer |

<!-- END GENERATED sub-rel-swift -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-swift-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | sub | SQ | P-gen | x86_64 | thru | 7.90 | Foundation.Decimal | 810.36 | **102.58×** | xRswsw2 | compact idiom peer |
| swift | sub | NQ | P-gen | x86_64 | thru | 16.62 | Foundation.Decimal | 987.26 | **59.40×** | xRswsw2 | compact idiom peer |
| swift | sub | MQ | P-gen | x86_64 | thru | 27.16 | Foundation.Decimal | 1031.76 | **37.99×** | xRswsw2 | compact idiom peer |
| swift | sub | OQ | P-gen | x86_64 | thru | 47.02 | Foundation.Decimal | 1384.46 | **29.44×** | xRswsw2 | compact idiom peer |
| swift | sub | FQ | P-gen | x86_64 | thru | 33.65 | Foundation.Decimal | 663.05 | **19.70×** | xRswsw2 | compact idiom peer |

<!-- END GENERATED sub-rel-swift-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-swift -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | mul | CP | P-gen | arm64 | thru | 3.38 | Foundation.Decimal | 296.40 | **87.69×** | Rswsw2 | compact idiom peer |
| swift | mul | WP | P-gen | arm64 | thru | 20.44 | Foundation.Decimal | 313.64 | **15.34×** | Rswsw2 | compact idiom peer |
| swift | mul | XP | P-gen | arm64 | thru | 25.58 | Foundation.Decimal | 847.96 | **33.15×** | Rswsw2 | compact idiom peer |

<!-- END GENERATED mul-rel-swift -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-swift-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | mul | CP | P-gen | x86_64 | thru | 7.09 | Foundation.Decimal | 709.74 | **100.10×** | xRswsw2 | compact idiom peer |
| swift | mul | WP | P-gen | x86_64 | thru | 35.67 | Foundation.Decimal | 832.41 | **23.34×** | xRswsw2 | compact idiom peer |
| swift | mul | XP | P-gen | x86_64 | thru | 48.41 | Foundation.Decimal | 2062.46 | **42.60×** | xRswsw2 | compact idiom peer |

<!-- END GENERATED mul-rel-swift-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-swift -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | div | CD | P-gen | arm64 | thru | 37.96 | Foundation.Decimal | 1374.10 | **36.20×** | Rswsw2 | compact idiom peer |
| swift | div | WD | P-gen | arm64 | thru | 50.71 | Foundation.Decimal | 902.58 | **17.80×** | Rswsw2 | compact idiom peer |
| swift | div | XD | P-gen | arm64 | thru | 50.45 | Foundation.Decimal | 691.38 | **13.70×** | Rswsw2 | compact idiom peer |
| swift | div | ET | P-gen | arm64 | thru | 10.58 | Foundation.Decimal | 3262.31 | **308.35×** | Rswsw2 | compact idiom peer |
| swift | div | PT | P-gen | arm64 | thru | 7.15 | Foundation.Decimal | 3135.91 | **438.59×** | Rswsw2 | compact idiom peer |

<!-- END GENERATED div-rel-swift -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-swift-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | div | CD | P-gen | x86_64 | thru | 77.86 | Foundation.Decimal | 3200.00 | **41.10×** | xRswsw2 | compact idiom peer |
| swift | div | WD | P-gen | x86_64 | thru | 100.76 | Foundation.Decimal | 2099.23 | **20.83×** | xRswsw2 | compact idiom peer |
| swift | div | XD | P-gen | x86_64 | thru | 104.81 | Foundation.Decimal | 1557.39 | **14.86×** | xRswsw2 | compact idiom peer |
| swift | div | ET | P-gen | x86_64 | thru | 37.72 | Foundation.Decimal | 7467.57 | **197.97×** | xRswsw2 | compact idiom peer |
| swift | div | PT | P-gen | x86_64 | thru | 16.93 | Foundation.Decimal | 7187.12 | **424.52×** | xRswsw2 | compact idiom peer |

<!-- END GENERATED div-rel-swift-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-swift -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | fma | FN | FMA | arm64 | thru | 83.92 | - | - | - | Rswsw2 |  |
| swift | fma | FF | FMA | arm64 | thru | 42.30 | - | - | - | Rswsw2 |  |

<!-- END GENERATED fma-rel-swift -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-swift-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | fma | FN | FMA | x86_64 | thru | 151.25 | - | - | - | xRswsw2 |  |
| swift | fma | FF | FMA | x86_64 | thru | 85.38 | - | - | - | xRswsw2 |  |

<!-- END GENERATED fma-rel-swift-x86 -->

</div>
