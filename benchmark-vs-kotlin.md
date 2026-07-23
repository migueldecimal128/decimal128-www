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
| kotlin | add | MIX | P-fin | arm64 | thru‡ | 7.01 | BigDecimal | 20.26 | **2.89×** | Rkosw2 | compact idiom peer |
| kotlin | sub | MIX | P-fin | arm64 | thru‡ | 6.00 | BigDecimal | 23.21 | **3.87×** | Rkosw2 | compact idiom peer |
| kotlin | mul | CP | P-fin | arm64 | thru‡ | 5.58 | BigDecimal | 12.50 | **2.24×** | Rkosw2 | compact idiom peer |
| kotlin | mul | WP | P-fin | arm64 | thru‡ | 25.25 | BigDecimal | 72.62 | **2.88×** | Rkosw2 | compact idiom peer |
| kotlin | div | CD | P-fin | arm64 | thru‡ | 40.00 | BigDecimal | 161.67 | **4.04×** | Rkosw2 | compact idiom peer |
| kotlin | div | WD | P-fin | arm64 | thru‡ | 49.04 | BigDecimal | 98.27 | **2.00×** | Rkosw2 | compact idiom peer |
| kotlin | div | ET | P-fin | arm64 | thru‡ | 18.48 | BigDecimal | 505.15 | **27.33×** | Rkosw2 | compact idiom peer |
| kotlin | div | PT | P-fin | arm64 | thru‡ | 11.00 | BigDecimal | 485.97 | **44.18×** | Rkosw2 | compact idiom peer |

<!-- END GENERATED pfin-rel-kotlin -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-kotlin-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | add | MIX | P-fin | x86_64 | thru‡ | 22.06 | BigDecimal | 58.48 | **2.65×** | xRkosw2 | compact idiom peer |
| kotlin | sub | MIX | P-fin | x86_64 | thru‡ | 18.54 | BigDecimal | 69.77 | **3.76×** | xRkosw2 | compact idiom peer |
| kotlin | mul | CP | P-fin | x86_64 | thru‡ | 13.05 | BigDecimal | 42.42 | **3.25×** | xRkosw2 | compact idiom peer |
| kotlin | mul | WP | P-fin | x86_64 | thru‡ | 45.37 | BigDecimal | 164.99 | **3.64×** | xRkosw2 | compact idiom peer |
| kotlin | div | CD | P-fin | x86_64 | thru‡ | 99.57 | BigDecimal | 430.06 | **4.32×** | xRkosw2 | compact idiom peer |
| kotlin | div | WD | P-fin | x86_64 | thru‡ | 122.28 | BigDecimal | 220.62 | **1.80×** | xRkosw2 | compact idiom peer |
| kotlin | div | ET | P-fin | x86_64 | thru‡ | 49.97 | BigDecimal | 1476.04 | **29.54×** | xRkosw2 | compact idiom peer |
| kotlin | div | PT | P-fin | x86_64 | thru‡ | 25.87 | BigDecimal | 1435.33 | **55.48×** | xRkosw2 | compact idiom peer |

<!-- END GENERATED pfin-rel-kotlin-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-kotlin -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | add | SQ | P-gen | arm64 | thru‡ | 5.94 | BigDecimal | 19.20 | **3.23×** | Rkosw2 | compact idiom peer |
| kotlin | add | NQ | P-gen | arm64 | thru‡ | 8.77 | BigDecimal | 30.41 | **3.47×** | Rkosw2 | compact idiom peer |
| kotlin | add | MQ | P-gen | arm64 | thru‡ | 17.49 | BigDecimal | 30.74 | **1.76×** | Rkosw2 | compact idiom peer |
| kotlin | add | OQ | P-gen | arm64 | thru‡ | 39.85 | BigDecimal | 75.60 | **1.90×** | Rkosw2 | compact idiom peer |
| kotlin | add | FQ | P-gen | arm64 | thru‡ | 19.60 | BigDecimal | 90.16 | **4.60×** | Rkosw2 | compact idiom peer |

<!-- END GENERATED add-rel-kotlin -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-kotlin-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | add | SQ | P-gen | x86_64 | thru‡ | 16.74 | BigDecimal | 56.71 | **3.39×** | xRkosw2 | compact idiom peer |
| kotlin | add | NQ | P-gen | x86_64 | thru‡ | 23.55 | BigDecimal | 87.61 | **3.72×** | xRkosw2 | compact idiom peer |
| kotlin | add | MQ | P-gen | x86_64 | thru‡ | 43.19 | BigDecimal | 86.61 | **2.01×** | xRkosw2 | compact idiom peer |
| kotlin | add | OQ | P-gen | x86_64 | thru‡ | 70.87 | BigDecimal | 168.54 | **2.38×** | xRkosw2 | compact idiom peer |
| kotlin | add | FQ | P-gen | x86_64 | thru‡ | 45.86 | BigDecimal | 210.55 | **4.59×** | xRkosw2 | compact idiom peer |

<!-- END GENERATED add-rel-kotlin-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-kotlin -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | sub | SQ | P-gen | arm64 | thru‡ | 4.90 | BigDecimal | 22.82 | **4.66×** | Rkosw2 | compact idiom peer |
| kotlin | sub | NQ | P-gen | arm64 | thru‡ | 9.06 | BigDecimal | 33.76 | **3.73×** | Rkosw2 | compact idiom peer |
| kotlin | sub | MQ | P-gen | arm64 | thru‡ | 17.61 | BigDecimal | 33.82 | **1.92×** | Rkosw2 | compact idiom peer |
| kotlin | sub | OQ | P-gen | arm64 | thru‡ | 40.76 | BigDecimal | 83.64 | **2.05×** | Rkosw2 | compact idiom peer |
| kotlin | sub | FQ | P-gen | arm64 | thru‡ | 17.84 | BigDecimal | 96.65 | **5.42×** | Rkosw2 | compact idiom peer |

<!-- END GENERATED sub-rel-kotlin -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-kotlin-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | sub | SQ | P-gen | x86_64 | thru‡ | 14.66 | BigDecimal | 65.42 | **4.46×** | xRkosw2 | compact idiom peer |
| kotlin | sub | NQ | P-gen | x86_64 | thru‡ | 24.86 | BigDecimal | 91.38 | **3.68×** | xRkosw2 | compact idiom peer |
| kotlin | sub | MQ | P-gen | x86_64 | thru‡ | 42.31 | BigDecimal | 96.31 | **2.28×** | xRkosw2 | compact idiom peer |
| kotlin | sub | OQ | P-gen | x86_64 | thru‡ | 66.25 | BigDecimal | 180.48 | **2.72×** | xRkosw2 | compact idiom peer |
| kotlin | sub | FQ | P-gen | x86_64 | thru‡ | 45.59 | BigDecimal | 213.83 | **4.69×** | xRkosw2 | compact idiom peer |

<!-- END GENERATED sub-rel-kotlin-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-kotlin -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | mul | CP | P-gen | arm64 | thru‡ | 5.50 | BigDecimal | 11.89 | **2.16×** | Rkosw2 | compact idiom peer |
| kotlin | mul | WP | P-gen | arm64 | thru‡ | 30.01 | BigDecimal | 59.90 | **2.00×** | Rkosw2 | compact idiom peer |
| kotlin | mul | XP | P-gen | arm64 | thru‡ | 59.73 | BigDecimal | 162.25 | **2.72×** | Rkosw2 | compact idiom peer |

<!-- END GENERATED mul-rel-kotlin -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-kotlin-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | mul | CP | P-gen | x86_64 | thru‡ | 14.59 | BigDecimal | 42.30 | **2.90×** | xRkosw2 | compact idiom peer |
| kotlin | mul | WP | P-gen | x86_64 | thru‡ | 46.83 | BigDecimal | 156.51 | **3.34×** | xRkosw2 | compact idiom peer |
| kotlin | mul | XP | P-gen | x86_64 | thru‡ | 85.48 | BigDecimal | 279.37 | **3.27×** | xRkosw2 | compact idiom peer |

<!-- END GENERATED mul-rel-kotlin-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-kotlin -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | div | CD | P-gen | arm64 | thru‡ | 35.92 | BigDecimal | 145.06 | **4.04×** | Rkosw2 | compact idiom peer |
| kotlin | div | WD | P-gen | arm64 | thru‡ | 52.29 | BigDecimal | 118.35 | **2.26×** | Rkosw2 | compact idiom peer |
| kotlin | div | XD | P-gen | arm64 | thru‡ | 53.05 | BigDecimal | 222.14 | **4.19×** | Rkosw2 | compact idiom peer |
| kotlin | div | ET | P-gen | arm64 | thru‡ | 18.98 | BigDecimal | 470.57 | **24.79×** | Rkosw2 | compact idiom peer |
| kotlin | div | PT | P-gen | arm64 | thru‡ | 11.59 | BigDecimal | 436.10 | **37.63×** | Rkosw2 | compact idiom peer |

<!-- END GENERATED div-rel-kotlin -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-kotlin-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | div | CD | P-gen | x86_64 | thru‡ | 94.77 | BigDecimal | 377.00 | **3.98×** | xRkosw2 | compact idiom peer |
| kotlin | div | WD | P-gen | x86_64 | thru‡ | 121.81 | BigDecimal | 268.25 | **2.20×** | xRkosw2 | compact idiom peer |
| kotlin | div | XD | P-gen | x86_64 | thru‡ | 132.68 | BigDecimal | 344.00 | **2.59×** | xRkosw2 | compact idiom peer |
| kotlin | div | ET | P-gen | x86_64 | thru‡ | 49.99 | BigDecimal | 1154.84 | **23.10×** | xRkosw2 | compact idiom peer |
| kotlin | div | PT | P-gen | x86_64 | thru‡ | 27.06 | BigDecimal | 1096.99 | **40.54×** | xRkosw2 | compact idiom peer |

<!-- END GENERATED div-rel-kotlin-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-kotlin -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | fma | FN | FMA | arm64 | thru‡ | 112.22 | libbid | 81.22 | **0.72×** | Rkosw2 |  |
| kotlin | fma | FF | FMA | arm64 | thru‡ | 90.55 | libbid | 57.36 | **0.63×** | Rkosw2 |  |

<!-- END GENERATED fma-rel-kotlin -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-kotlin-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | fma | FN | FMA | x86_64 | thru‡ | 259.22 | libbid | 161.79 | **0.62×** | xRkosw2 |  |
| kotlin | fma | FF | FMA | x86_64 | thru‡ | 225.88 | libbid | 124.13 | **0.55×** | xRkosw2 |  |

<!-- END GENERATED fma-rel-kotlin-x86 -->

</div>
