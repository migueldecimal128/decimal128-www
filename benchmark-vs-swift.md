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
| swift | add | MIX | P-fin | arm64 | thru | 4.33 | Foundation.Decimal | 316.91 | **73.19×** | Rswsw2 | compact idiom peer |
| swift | sub | MIX | P-fin | arm64 | thru | 4.72 | Foundation.Decimal | 363.01 | **76.91×** | Rswsw2 | compact idiom peer |
| swift | mul | CP | P-fin | arm64 | thru | 2.16 | Foundation.Decimal | 294.62 | **136.40×** | Rswsw2 | compact idiom peer |
| swift | mul | WP | P-fin | arm64 | thru | 20.96 | Foundation.Decimal | 296.43 | **14.14×** | Rswsw2 | compact idiom peer |
| swift | div | CD | P-fin | arm64 | thru | 39.23 | Foundation.Decimal | 1295.88 | **33.03×** | Rswsw2 | compact idiom peer |
| swift | div | WD | P-fin | arm64 | thru | 52.34 | Foundation.Decimal | 697.65 | **13.33×** | Rswsw2 | compact idiom peer |
| swift | div | ET | P-fin | arm64 | thru | 9.82 | Foundation.Decimal | 3738.33 | **380.69×** | Rswsw2 | compact idiom peer |
| swift | div | PT | P-fin | arm64 | thru | 7.15 | Foundation.Decimal | 3637.84 | **508.79×** | Rswsw2 | compact idiom peer |

<!-- END GENERATED pfin-rel-swift -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-swift-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | add | MIX | P-fin | x86_64 | thru | 12.76 | Foundation.Decimal | 791.38 | **62.02×** | xRswsw2 | compact idiom peer |
| swift | sub | MIX | P-fin | x86_64 | thru | 10.78 | Foundation.Decimal | 798.28 | **74.05×** | xRswsw2 | compact idiom peer |
| swift | mul | CP | P-fin | x86_64 | thru | 4.29 | Foundation.Decimal | 685.24 | **159.73×** | xRswsw2 | compact idiom peer |
| swift | mul | WP | P-fin | x86_64 | thru | 34.14 | Foundation.Decimal | 764.86 | **22.40×** | xRswsw2 | compact idiom peer |
| swift | div | CD | P-fin | x86_64 | thru | 74.97 | Foundation.Decimal | 2917.12 | **38.91×** | xRswsw2 | compact idiom peer |
| swift | div | WD | P-fin | x86_64 | thru | 97.81 | Foundation.Decimal | 1549.20 | **15.84×** | xRswsw2 | compact idiom peer |
| swift | div | ET | P-fin | x86_64 | thru | 25.91 | Foundation.Decimal | 8202.38 | **316.57×** | xRswsw2 | compact idiom peer |
| swift | div | PT | P-fin | x86_64 | thru | 15.76 | Foundation.Decimal | 8023.77 | **509.12×** | xRswsw2 | compact idiom peer |

<!-- END GENERATED pfin-rel-swift-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-swift -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | add | SQ | P-gen | arm64 | thru | 5.80 | Foundation.Decimal | 317.31 | **54.71×** | Rswsw2 | compact idiom peer |
| swift | add | NQ | P-gen | arm64 | thru | 8.19 | Foundation.Decimal | 399.50 | **48.78×** | Rswsw2 | compact idiom peer |
| swift | add | MQ | P-gen | arm64 | thru | 15.06 | Foundation.Decimal | 403.37 | **26.78×** | Rswsw2 | compact idiom peer |
| swift | add | OQ | P-gen | arm64 | thru | 20.66 | Foundation.Decimal | 536.95 | **25.99×** | Rswsw2 | compact idiom peer |
| swift | add | FQ | P-gen | arm64 | thru | 16.56 | Foundation.Decimal | 280.00 | **16.91×** | Rswsw2 | compact idiom peer |

<!-- END GENERATED add-rel-swift -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-swift-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | add | SQ | P-gen | x86_64 | thru | 11.40 | Foundation.Decimal | 808.46 | **70.92×** | xRswsw2 | compact idiom peer |
| swift | add | NQ | P-gen | x86_64 | thru | 16.17 | Foundation.Decimal | 942.09 | **58.26×** | xRswsw2 | compact idiom peer |
| swift | add | MQ | P-gen | x86_64 | thru | 26.05 | Foundation.Decimal | 964.27 | **37.02×** | xRswsw2 | compact idiom peer |
| swift | add | OQ | P-gen | x86_64 | thru | 46.40 | Foundation.Decimal | 1313.95 | **28.32×** | xRswsw2 | compact idiom peer |
| swift | add | FQ | P-gen | x86_64 | thru | 32.89 | Foundation.Decimal | 642.72 | **19.54×** | xRswsw2 | compact idiom peer |

<!-- END GENERATED add-rel-swift-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-swift -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | sub | SQ | P-gen | arm64 | thru | 5.10 | Foundation.Decimal | 323.80 | **63.49×** | Rswsw2 | compact idiom peer |
| swift | sub | NQ | P-gen | arm64 | thru | 7.84 | Foundation.Decimal | 403.41 | **51.46×** | Rswsw2 | compact idiom peer |
| swift | sub | MQ | P-gen | arm64 | thru | 14.45 | Foundation.Decimal | 406.16 | **28.11×** | Rswsw2 | compact idiom peer |
| swift | sub | OQ | P-gen | arm64 | thru | 19.65 | Foundation.Decimal | 538.40 | **27.40×** | Rswsw2 | compact idiom peer |
| swift | sub | FQ | P-gen | arm64 | thru | 15.57 | Foundation.Decimal | 281.04 | **18.05×** | Rswsw2 | compact idiom peer |

<!-- END GENERATED sub-rel-swift -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-swift-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | sub | SQ | P-gen | x86_64 | thru | 8.08 | Foundation.Decimal | 778.88 | **96.40×** | xRswsw2 | compact idiom peer |
| swift | sub | NQ | P-gen | x86_64 | thru | 15.73 | Foundation.Decimal | 966.59 | **61.45×** | xRswsw2 | compact idiom peer |
| swift | sub | MQ | P-gen | x86_64 | thru | 26.10 | Foundation.Decimal | 972.38 | **37.26×** | xRswsw2 | compact idiom peer |
| swift | sub | OQ | P-gen | x86_64 | thru | 45.90 | Foundation.Decimal | 1329.08 | **28.96×** | xRswsw2 | compact idiom peer |
| swift | sub | FQ | P-gen | x86_64 | thru | 33.72 | Foundation.Decimal | 638.67 | **18.94×** | xRswsw2 | compact idiom peer |

<!-- END GENERATED sub-rel-swift-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-swift -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | mul | CP | P-gen | arm64 | thru | 3.39 | Foundation.Decimal | 296.13 | **87.35×** | Rswsw2 | compact idiom peer |
| swift | mul | WP | P-gen | arm64 | thru | 20.58 | Foundation.Decimal | 316.01 | **15.36×** | Rswsw2 | compact idiom peer |
| swift | mul | XP | P-gen | arm64 | thru | 25.60 | Foundation.Decimal | 850.83 | **33.24×** | Rswsw2 | compact idiom peer |

<!-- END GENERATED mul-rel-swift -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-swift-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | mul | CP | P-gen | x86_64 | thru | 7.09 | Foundation.Decimal | 680.52 | **95.98×** | xRswsw2 | compact idiom peer |
| swift | mul | WP | P-gen | x86_64 | thru | 34.22 | Foundation.Decimal | 803.29 | **23.47×** | xRswsw2 | compact idiom peer |
| swift | mul | XP | P-gen | x86_64 | thru | 48.01 | Foundation.Decimal | 1986.61 | **41.38×** | xRswsw2 | compact idiom peer |

<!-- END GENERATED mul-rel-swift-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-swift -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | div | CD | P-gen | arm64 | thru | 38.67 | Foundation.Decimal | 1367.93 | **35.37×** | Rswsw2 | compact idiom peer |
| swift | div | WD | P-gen | arm64 | thru | 51.00 | Foundation.Decimal | 899.89 | **17.64×** | Rswsw2 | compact idiom peer |
| swift | div | XD | P-gen | arm64 | thru | 49.63 | Foundation.Decimal | 686.71 | **13.84×** | Rswsw2 | compact idiom peer |
| swift | div | ET | P-gen | arm64 | thru | 9.82 | Foundation.Decimal | 3202.04 | **326.07×** | Rswsw2 | compact idiom peer |
| swift | div | PT | P-gen | arm64 | thru | 7.16 | Foundation.Decimal | 3095.19 | **432.29×** | Rswsw2 | compact idiom peer |

<!-- END GENERATED div-rel-swift -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-swift-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | div | CD | P-gen | x86_64 | thru | 77.79 | Foundation.Decimal | 3123.84 | **40.16×** | xRswsw2 | compact idiom peer |
| swift | div | WD | P-gen | x86_64 | thru | 99.20 | Foundation.Decimal | 2008.21 | **20.24×** | xRswsw2 | compact idiom peer |
| swift | div | XD | P-gen | x86_64 | thru | 100.32 | Foundation.Decimal | 1511.36 | **15.07×** | xRswsw2 | compact idiom peer |
| swift | div | ET | P-gen | x86_64 | thru | 33.54 | Foundation.Decimal | 7177.29 | **213.99×** | xRswsw2 | compact idiom peer |
| swift | div | PT | P-gen | x86_64 | thru | 15.51 | Foundation.Decimal | 6837.99 | **440.88×** | xRswsw2 | compact idiom peer |

<!-- END GENERATED div-rel-swift-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-swift -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | fma | FN | FMA | arm64 | thru | 83.99 | - | - | - | Rswsw2 |  |
| swift | fma | FF | FMA | arm64 | thru | 42.23 | - | - | - | Rswsw2 |  |

<!-- END GENERATED fma-rel-swift -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-swift-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| swift | fma | FN | FMA | x86_64 | thru | 148.55 | - | - | - | xRswsw2 |  |
| swift | fma | FF | FMA | x86_64 | thru | 83.13 | - | - | - | xRswsw2 |  |

<!-- END GENERATED fma-rel-swift-x86 -->

</div>
