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
| kotlin | add | MIX | P-fin | arm64 | thru‡ | 4.91 | BigDecimal | 19.28 | **3.93×** | Rkosw2 | compact idiom peer |
| kotlin | sub | MIX | P-fin | arm64 | thru‡ | 6.34 | BigDecimal | 24.91 | **3.93×** | Rkosw2 | compact idiom peer |
| kotlin | mul | CP | P-fin | arm64 | thru‡ | 5.29 | BigDecimal | 12.49 | **2.36×** | Rkosw2 | compact idiom peer |
| kotlin | mul | WP | P-fin | arm64 | thru‡ | 30.19 | BigDecimal | 65.50 | **2.17×** | Rkosw2 | compact idiom peer |
| kotlin | div | CD | P-fin | arm64 | thru‡ | 40.56 | BigDecimal | 139.88 | **3.45×** | Rkosw2 | compact idiom peer |
| kotlin | div | WD | P-fin | arm64 | thru‡ | 51.73 | BigDecimal | 101.79 | **1.97×** | Rkosw2 | compact idiom peer |
| kotlin | div | ET | P-fin | arm64 | thru‡ | 18.05 | BigDecimal | 502.96 | **27.86×** | Rkosw2 | compact idiom peer |
| kotlin | div | PT | P-fin | arm64 | thru‡ | 15.21 | BigDecimal | 482.55 | **31.73×** | Rkosw2 | compact idiom peer |

<!-- END GENERATED pfin-rel-kotlin -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-kotlin-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | add | MIX | P-fin | x86_64 | thru‡ | 13.42 | BigDecimal | 50.69 | **3.78×** | xRkosw2 | compact idiom peer |
| kotlin | sub | MIX | P-fin | x86_64 | thru‡ | 17.31 | BigDecimal | 63.14 | **3.65×** | xRkosw2 | compact idiom peer |
| kotlin | mul | CP | P-fin | x86_64 | thru‡ | 12.42 | BigDecimal | 42.58 | **3.43×** | xRkosw2 | compact idiom peer |
| kotlin | mul | WP | P-fin | x86_64 | thru‡ | 50.20 | BigDecimal | 157.99 | **3.15×** | xRkosw2 | compact idiom peer |
| kotlin | div | CD | P-fin | x86_64 | thru‡ | 103.64 | BigDecimal | 405.19 | **3.91×** | xRkosw2 | compact idiom peer |
| kotlin | div | WD | P-fin | x86_64 | thru‡ | 127.25 | BigDecimal | 217.09 | **1.71×** | xRkosw2 | compact idiom peer |
| kotlin | div | ET | P-fin | x86_64 | thru‡ | 51.94 | BigDecimal | 1395.56 | **26.87×** | xRkosw2 | compact idiom peer |
| kotlin | div | PT | P-fin | x86_64 | thru‡ | 26.92 | BigDecimal | 1343.69 | **49.91×** | xRkosw2 | compact idiom peer |

<!-- END GENERATED pfin-rel-kotlin-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-kotlin -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | add | SQ | P-gen | arm64 | thru‡ | 4.89 | BigDecimal | 19.34 | **3.96×** | Rkosw2 | compact idiom peer |
| kotlin | add | NQ | P-gen | arm64 | thru‡ | 9.12 | BigDecimal | 30.48 | **3.34×** | Rkosw2 | compact idiom peer |
| kotlin | add | MQ | P-gen | arm64 | thru‡ | 19.04 | BigDecimal | 30.73 | **1.61×** | Rkosw2 | compact idiom peer |
| kotlin | add | OQ | P-gen | arm64 | thru‡ | 39.51 | BigDecimal | 77.47 | **1.96×** | Rkosw2 | compact idiom peer |
| kotlin | add | FQ | P-gen | arm64 | thru‡ | 21.35 | BigDecimal | 89.85 | **4.21×** | Rkosw2 | compact idiom peer |

<!-- END GENERATED add-rel-kotlin -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-kotlin-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | add | SQ | P-gen | x86_64 | thru‡ | 14.74 | BigDecimal | 55.84 | **3.79×** | xRkosw2 | compact idiom peer |
| kotlin | add | NQ | P-gen | x86_64 | thru‡ | 20.87 | BigDecimal | 84.19 | **4.03×** | xRkosw2 | compact idiom peer |
| kotlin | add | MQ | P-gen | x86_64 | thru‡ | 36.52 | BigDecimal | 89.55 | **2.45×** | xRkosw2 | compact idiom peer |
| kotlin | add | OQ | P-gen | x86_64 | thru‡ | 63.47 | BigDecimal | 173.27 | **2.73×** | xRkosw2 | compact idiom peer |
| kotlin | add | FQ | P-gen | x86_64 | thru‡ | 44.70 | BigDecimal | 196.28 | **4.39×** | xRkosw2 | compact idiom peer |

<!-- END GENERATED add-rel-kotlin-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-kotlin -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | sub | SQ | P-gen | arm64 | thru‡ | 5.00 | BigDecimal | 23.35 | **4.67×** | Rkosw2 | compact idiom peer |
| kotlin | sub | NQ | P-gen | arm64 | thru‡ | 8.57 | BigDecimal | 34.67 | **4.05×** | Rkosw2 | compact idiom peer |
| kotlin | sub | MQ | P-gen | arm64 | thru‡ | 18.34 | BigDecimal | 34.83 | **1.90×** | Rkosw2 | compact idiom peer |
| kotlin | sub | OQ | P-gen | arm64 | thru‡ | 39.10 | BigDecimal | 84.69 | **2.17×** | Rkosw2 | compact idiom peer |
| kotlin | sub | FQ | P-gen | arm64 | thru‡ | 18.87 | BigDecimal | 96.17 | **5.10×** | Rkosw2 | compact idiom peer |

<!-- END GENERATED sub-rel-kotlin -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-kotlin-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | sub | SQ | P-gen | x86_64 | thru‡ | 14.81 | BigDecimal | 66.73 | **4.51×** | xRkosw2 | compact idiom peer |
| kotlin | sub | NQ | P-gen | x86_64 | thru‡ | 20.88 | BigDecimal | 90.22 | **4.32×** | xRkosw2 | compact idiom peer |
| kotlin | sub | MQ | P-gen | x86_64 | thru‡ | 37.05 | BigDecimal | 95.44 | **2.58×** | xRkosw2 | compact idiom peer |
| kotlin | sub | OQ | P-gen | x86_64 | thru‡ | 79.62 | BigDecimal | 186.95 | **2.35×** | xRkosw2 | compact idiom peer |
| kotlin | sub | FQ | P-gen | x86_64 | thru‡ | 43.93 | BigDecimal | 206.24 | **4.69×** | xRkosw2 | compact idiom peer |

<!-- END GENERATED sub-rel-kotlin-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-kotlin -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | mul | CP | P-gen | arm64 | thru‡ | 5.77 | BigDecimal | 12.04 | **2.09×** | Rkosw2 | compact idiom peer |
| kotlin | mul | WP | P-gen | arm64 | thru‡ | 27.24 | BigDecimal | 55.00 | **2.02×** | Rkosw2 | compact idiom peer |
| kotlin | mul | XP | P-gen | arm64 | thru‡ | 54.73 | BigDecimal | 161.64 | **2.95×** | Rkosw2 | compact idiom peer |

<!-- END GENERATED mul-rel-kotlin -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-kotlin-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | mul | CP | P-gen | x86_64 | thru‡ | 14.87 | BigDecimal | 39.84 | **2.68×** | xRkosw2 | compact idiom peer |
| kotlin | mul | WP | P-gen | x86_64 | thru‡ | 47.79 | BigDecimal | 153.39 | **3.21×** | xRkosw2 | compact idiom peer |
| kotlin | mul | XP | P-gen | x86_64 | thru‡ | 67.85 | BigDecimal | 282.03 | **4.16×** | xRkosw2 | compact idiom peer |

<!-- END GENERATED mul-rel-kotlin-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-kotlin -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | div | CD | P-gen | arm64 | thru‡ | 35.23 | BigDecimal | 138.76 | **3.94×** | Rkosw2 | compact idiom peer |
| kotlin | div | WD | P-gen | arm64 | thru‡ | 51.92 | BigDecimal | 112.44 | **2.17×** | Rkosw2 | compact idiom peer |
| kotlin | div | XD | P-gen | arm64 | thru‡ | 51.77 | BigDecimal | 222.38 | **4.30×** | Rkosw2 | compact idiom peer |
| kotlin | div | ET | P-gen | arm64 | thru‡ | 19.53 | BigDecimal | 422.56 | **21.64×** | Rkosw2 | compact idiom peer |
| kotlin | div | PT | P-gen | arm64 | thru‡ | 11.52 | BigDecimal | 391.87 | **34.02×** | Rkosw2 | compact idiom peer |

<!-- END GENERATED div-rel-kotlin -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-kotlin-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | div | CD | P-gen | x86_64 | thru‡ | 93.41 | BigDecimal | 359.09 | **3.84×** | xRkosw2 | compact idiom peer |
| kotlin | div | WD | P-gen | x86_64 | thru‡ | 119.42 | BigDecimal | 254.66 | **2.13×** | xRkosw2 | compact idiom peer |
| kotlin | div | XD | P-gen | x86_64 | thru‡ | 126.54 | BigDecimal | 351.65 | **2.78×** | xRkosw2 | compact idiom peer |
| kotlin | div | ET | P-gen | x86_64 | thru‡ | 48.04 | BigDecimal | 1099.23 | **22.88×** | xRkosw2 | compact idiom peer |
| kotlin | div | PT | P-gen | x86_64 | thru‡ | 24.22 | BigDecimal | 1022.51 | **42.22×** | xRkosw2 | compact idiom peer |

<!-- END GENERATED div-rel-kotlin-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-kotlin -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | fma | FN | FMA | arm64 | thru‡ | 106.00 | - | - | - | Rkosw2 |  |
| kotlin | fma | FF | FMA | arm64 | thru‡ | 81.98 | - | - | - | Rkosw2 |  |

<!-- END GENERATED fma-rel-kotlin -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-kotlin-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | fma | FN | FMA | x86_64 | thru‡ | 233.32 | - | - | - | xRkosw2 |  |
| kotlin | fma | FF | FMA | x86_64 | thru‡ | 172.94 | - | - | - | xRkosw2 |  |

<!-- END GENERATED fma-rel-kotlin-x86 -->

</div>
