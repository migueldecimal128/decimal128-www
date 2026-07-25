---
layout: default
permalink: /benchmark/vs-kotlin.html
title: "Kotlin Benchmark Results — Decimal128"
description: "decimal128 in Kotlin, measured against the alternatives available to it — a realistic financial mix (P-fin) plus per-operation band characterization, with explicit ratios."
heading: "Kotlin Benchmark Results"
---

<div class="whitepaper" markdown="1">

<p class="whitepaper-meta">Living document — as-measured results. Category codes, profiles, modes &amp; method: <a href="key.html">Benchmark Key</a>.</p>

This is the **Kotlin** view of decimal128 **as-measured**, band by band, with explicit ratios. It opens with the realistic financial-mix (**P-fin**) headline, then the per-operation band characterization (**P-gen**) and FMA. In Kotlin, d128 is measured against its in-language idiom peer **`BigDecimal`**, with the **libbid** universal reference on the full-width bands. It is **data only** — the categories, magnitude profiles, units, and methodology are defined in the [Benchmark Key](key.html) (and, authoritatively, `BenchmarkMatrix.md`). The cross-port d128 band-shape matrices (all ports, no alternatives) live in [Port-Comparison Benchmark Results](port-compare.html); the full index of per-language pages is on the [Benchmarks](/benchmarks.html) hub.

## Summary — Ratio Range by Operation

The ratio for Kotlin's idiom peer on x86_64 (Intel i9-9880H): `ratio = BigDecimal / Miguel` (&gt; 1× ⇒ d128 faster), broken out by operation.

| | Add | Subtract | Multiply | Divide |
|---|---|---|---|---|
| ratio = BigDecimal / Miguel | 2.7× | 4× | 3× – 4× | 1.8× – 55× |

## FinMix — realistic financial mix (P-fin)

The headline: one realistic 64-bit financial operation mix — a `MIX` add/sub stream, mul `CP`/`WP`, div `CD`/`WD`/`ET`/`PT` — `ratio = alt / Miguel` (&gt; 1 ⇒ d128 faster). This is the profile closest to real financial code.

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED pfin-rel-kotlin -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | add | MIX | P-fin | arm64 | thru‡ | 5.34 | BigDecimal | 20.19 | **3.78×** | Rkosw2 | compact idiom peer |
| kotlin | sub | MIX | P-fin | arm64 | thru‡ | 6.31 | BigDecimal | 24.86 | **3.94×** | Rkosw2 | compact idiom peer |
| kotlin | mul | CP | P-fin | arm64 | thru‡ | 5.45 | BigDecimal | 12.46 | **2.29×** | Rkosw2 | compact idiom peer |
| kotlin | mul | WP | P-fin | arm64 | thru‡ | 26.51 | BigDecimal | 64.76 | **2.44×** | Rkosw2 | compact idiom peer |
| kotlin | div | CD | P-fin | arm64 | thru‡ | 38.40 | BigDecimal | 140.29 | **3.65×** | Rkosw2 | compact idiom peer |
| kotlin | div | WD | P-fin | arm64 | thru‡ | 50.04 | BigDecimal | 100.50 | **2.01×** | Rkosw2 | compact idiom peer |
| kotlin | div | ET | P-fin | arm64 | thru‡ | 18.70 | BigDecimal | 507.95 | **27.16×** | Rkosw2 | compact idiom peer |
| kotlin | div | PT | P-fin | arm64 | thru‡ | 15.06 | BigDecimal | 485.55 | **32.24×** | Rkosw2 | compact idiom peer |

<!-- END GENERATED pfin-rel-kotlin -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-kotlin-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | add | MIX | P-fin | x86_64 | thru‡ | 22.78 | BigDecimal | 64.24 | **2.82×** | xRkosw2 | compact idiom peer |
| kotlin | sub | MIX | P-fin | x86_64 | thru‡ | 19.03 | BigDecimal | 75.57 | **3.97×** | xRkosw2 | compact idiom peer |
| kotlin | mul | CP | P-fin | x86_64 | thru‡ | 13.89 | BigDecimal | 43.33 | **3.12×** | xRkosw2 | compact idiom peer |
| kotlin | mul | WP | P-fin | x86_64 | thru‡ | 48.71 | BigDecimal | 164.34 | **3.37×** | xRkosw2 | compact idiom peer |
| kotlin | div | CD | P-fin | x86_64 | thru‡ | 109.38 | BigDecimal | 435.62 | **3.98×** | xRkosw2 | compact idiom peer |
| kotlin | div | WD | P-fin | x86_64 | thru‡ | 132.79 | BigDecimal | 235.28 | **1.77×** | xRkosw2 | compact idiom peer |
| kotlin | div | ET | P-fin | x86_64 | thru‡ | 52.49 | BigDecimal | 1451.36 | **27.65×** | xRkosw2 | compact idiom peer |
| kotlin | div | PT | P-fin | x86_64 | thru‡ | 27.66 | BigDecimal | 1412.66 | **51.07×** | xRkosw2 | compact idiom peer |

<!-- END GENERATED pfin-rel-kotlin-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-kotlin -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | add | SQ | P-gen | arm64 | thru‡ | 5.95 | BigDecimal | 19.25 | **3.24×** | Rkosw2 | compact idiom peer |
| kotlin | add | NQ | P-gen | arm64 | thru‡ | 7.51 | BigDecimal | 30.48 | **4.06×** | Rkosw2 | compact idiom peer |
| kotlin | add | MQ | P-gen | arm64 | thru‡ | 16.99 | BigDecimal | 31.30 | **1.84×** | Rkosw2 | compact idiom peer |
| kotlin | add | OQ | P-gen | arm64 | thru‡ | 30.24 | BigDecimal | 75.47 | **2.50×** | Rkosw2 | compact idiom peer |
| kotlin | add | FQ | P-gen | arm64 | thru‡ | 19.29 | BigDecimal | 89.28 | **4.63×** | Rkosw2 | compact idiom peer |

<!-- END GENERATED add-rel-kotlin -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-kotlin-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | add | SQ | P-gen | x86_64 | thru‡ | 17.29 | BigDecimal | 55.77 | **3.23×** | xRkosw2 | compact idiom peer |
| kotlin | add | NQ | P-gen | x86_64 | thru‡ | 24.21 | BigDecimal | 85.32 | **3.52×** | xRkosw2 | compact idiom peer |
| kotlin | add | MQ | P-gen | x86_64 | thru‡ | 35.78 | BigDecimal | 85.60 | **2.39×** | xRkosw2 | compact idiom peer |
| kotlin | add | OQ | P-gen | x86_64 | thru‡ | 63.53 | BigDecimal | 167.13 | **2.63×** | xRkosw2 | compact idiom peer |
| kotlin | add | FQ | P-gen | x86_64 | thru‡ | 45.87 | BigDecimal | 195.66 | **4.27×** | xRkosw2 | compact idiom peer |

<!-- END GENERATED add-rel-kotlin-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-kotlin -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | sub | SQ | P-gen | arm64 | thru‡ | 5.00 | BigDecimal | 23.36 | **4.67×** | Rkosw2 | compact idiom peer |
| kotlin | sub | NQ | P-gen | arm64 | thru‡ | 7.72 | BigDecimal | 34.64 | **4.49×** | Rkosw2 | compact idiom peer |
| kotlin | sub | MQ | P-gen | arm64 | thru‡ | 17.13 | BigDecimal | 34.69 | **2.03×** | Rkosw2 | compact idiom peer |
| kotlin | sub | OQ | P-gen | arm64 | thru‡ | 31.01 | BigDecimal | 83.45 | **2.69×** | Rkosw2 | compact idiom peer |
| kotlin | sub | FQ | P-gen | arm64 | thru‡ | 17.72 | BigDecimal | 95.69 | **5.40×** | Rkosw2 | compact idiom peer |

<!-- END GENERATED sub-rel-kotlin -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-kotlin-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | sub | SQ | P-gen | x86_64 | thru‡ | 13.61 | BigDecimal | 62.79 | **4.61×** | xRkosw2 | compact idiom peer |
| kotlin | sub | NQ | P-gen | x86_64 | thru‡ | 24.99 | BigDecimal | 92.20 | **3.69×** | xRkosw2 | compact idiom peer |
| kotlin | sub | MQ | P-gen | x86_64 | thru‡ | 36.80 | BigDecimal | 94.55 | **2.57×** | xRkosw2 | compact idiom peer |
| kotlin | sub | OQ | P-gen | x86_64 | thru‡ | 64.91 | BigDecimal | 176.46 | **2.72×** | xRkosw2 | compact idiom peer |
| kotlin | sub | FQ | P-gen | x86_64 | thru‡ | 46.20 | BigDecimal | 203.22 | **4.40×** | xRkosw2 | compact idiom peer |

<!-- END GENERATED sub-rel-kotlin-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-kotlin -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | mul | CP | P-gen | arm64 | thru‡ | 5.52 | BigDecimal | 12.06 | **2.18×** | Rkosw2 | compact idiom peer |
| kotlin | mul | WP | P-gen | arm64 | thru‡ | 29.05 | BigDecimal | 55.58 | **1.91×** | Rkosw2 | compact idiom peer |
| kotlin | mul | XP | P-gen | arm64 | thru‡ | 51.99 | BigDecimal | 161.72 | **3.11×** | Rkosw2 | compact idiom peer |

<!-- END GENERATED mul-rel-kotlin -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-kotlin-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | mul | CP | P-gen | x86_64 | thru‡ | 14.17 | BigDecimal | 41.57 | **2.93×** | xRkosw2 | compact idiom peer |
| kotlin | mul | WP | P-gen | x86_64 | thru‡ | 46.58 | BigDecimal | 152.00 | **3.26×** | xRkosw2 | compact idiom peer |
| kotlin | mul | XP | P-gen | x86_64 | thru‡ | 71.14 | BigDecimal | 273.84 | **3.85×** | xRkosw2 | compact idiom peer |

<!-- END GENERATED mul-rel-kotlin-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-kotlin -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | div | CD | P-gen | arm64 | thru‡ | 35.37 | BigDecimal | 138.12 | **3.91×** | Rkosw2 | compact idiom peer |
| kotlin | div | WD | P-gen | arm64 | thru‡ | 52.56 | BigDecimal | 122.45 | **2.33×** | Rkosw2 | compact idiom peer |
| kotlin | div | XD | P-gen | arm64 | thru‡ | 53.48 | BigDecimal | 216.17 | **4.04×** | Rkosw2 | compact idiom peer |
| kotlin | div | ET | P-gen | arm64 | thru‡ | 19.61 | BigDecimal | 423.69 | **21.61×** | Rkosw2 | compact idiom peer |
| kotlin | div | PT | P-gen | arm64 | thru‡ | 11.54 | BigDecimal | 393.92 | **34.14×** | Rkosw2 | compact idiom peer |

<!-- END GENERATED div-rel-kotlin -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-kotlin-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | div | CD | P-gen | x86_64 | thru‡ | 91.75 | BigDecimal | 365.74 | **3.99×** | xRkosw2 | compact idiom peer |
| kotlin | div | WD | P-gen | x86_64 | thru‡ | 121.40 | BigDecimal | 261.87 | **2.16×** | xRkosw2 | compact idiom peer |
| kotlin | div | XD | P-gen | x86_64 | thru‡ | 138.46 | BigDecimal | 347.22 | **2.51×** | xRkosw2 | compact idiom peer |
| kotlin | div | ET | P-gen | x86_64 | thru‡ | 49.40 | BigDecimal | 1112.78 | **22.53×** | xRkosw2 | compact idiom peer |
| kotlin | div | PT | P-gen | x86_64 | thru‡ | 25.71 | BigDecimal | 1040.78 | **40.48×** | xRkosw2 | compact idiom peer |

<!-- END GENERATED div-rel-kotlin-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-kotlin -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | fma | FN | FMA | arm64 | thru‡ | 114.31 | - | - | - | Rkosw2 |  |
| kotlin | fma | FF | FMA | arm64 | thru‡ | 83.67 | - | - | - | Rkosw2 |  |

<!-- END GENERATED fma-rel-kotlin -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-kotlin-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | fma | FN | FMA | x86_64 | thru‡ | 235.29 | - | - | - | xRkosw2 |  |
| kotlin | fma | FF | FMA | x86_64 | thru‡ | 184.52 | - | - | - | xRkosw2 |  |

<!-- END GENERATED fma-rel-kotlin-x86 -->

</div>
