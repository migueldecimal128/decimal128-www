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
| kotlin | add | MIX | P-fin | arm64 | thru‡ | 7.14 | BigDecimal | 20.60 | **2.89×** | Rkosw2 | compact idiom peer |
| kotlin | sub | MIX | P-fin | arm64 | thru‡ | 6.05 | BigDecimal | 23.44 | **3.87×** | Rkosw2 | compact idiom peer |
| kotlin | mul | CP | P-fin | arm64 | thru‡ | 5.35 | BigDecimal | 12.57 | **2.35×** | Rkosw2 | compact idiom peer |
| kotlin | mul | WP | P-fin | arm64 | thru‡ | 26.31 | BigDecimal | 72.71 | **2.76×** | Rkosw2 | compact idiom peer |
| kotlin | div | CD | P-fin | arm64 | thru‡ | 39.81 | BigDecimal | 161.56 | **4.06×** | Rkosw2 | compact idiom peer |
| kotlin | div | WD | P-fin | arm64 | thru‡ | 48.83 | BigDecimal | 95.38 | **1.95×** | Rkosw2 | compact idiom peer |
| kotlin | div | ET | P-fin | arm64 | thru‡ | 18.31 | BigDecimal | 504.68 | **27.56×** | Rkosw2 | compact idiom peer |
| kotlin | div | PT | P-fin | arm64 | thru‡ | 12.60 | BigDecimal | 483.62 | **38.38×** | Rkosw2 | compact idiom peer |

<!-- END GENERATED pfin-rel-kotlin -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-kotlin-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | add | MIX | P-fin | x86_64 | thru‡ | 21.49 | BigDecimal | 63.99 | **2.98×** | xRkosw2 | compact idiom peer |
| kotlin | sub | MIX | P-fin | x86_64 | thru‡ | 18.65 | BigDecimal | 69.53 | **3.73×** | xRkosw2 | compact idiom peer |
| kotlin | mul | CP | P-fin | x86_64 | thru‡ | 13.25 | BigDecimal | 43.10 | **3.25×** | xRkosw2 | compact idiom peer |
| kotlin | mul | WP | P-fin | x86_64 | thru‡ | 45.84 | BigDecimal | 164.06 | **3.58×** | xRkosw2 | compact idiom peer |
| kotlin | div | CD | P-fin | x86_64 | thru‡ | 103.14 | BigDecimal | 420.53 | **4.08×** | xRkosw2 | compact idiom peer |
| kotlin | div | WD | P-fin | x86_64 | thru‡ | 121.24 | BigDecimal | 226.40 | **1.87×** | xRkosw2 | compact idiom peer |
| kotlin | div | ET | P-fin | x86_64 | thru‡ | 50.24 | BigDecimal | 1457.70 | **29.01×** | xRkosw2 | compact idiom peer |
| kotlin | div | PT | P-fin | x86_64 | thru‡ | 26.23 | BigDecimal | 1401.76 | **53.44×** | xRkosw2 | compact idiom peer |

<!-- END GENERATED pfin-rel-kotlin-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-kotlin -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | add | SQ | P-gen | arm64 | thru‡ | 5.91 | BigDecimal | 19.29 | **3.26×** | Rkosw2 | compact idiom peer |
| kotlin | add | NQ | P-gen | arm64 | thru‡ | 8.88 | BigDecimal | 30.48 | **3.43×** | Rkosw2 | compact idiom peer |
| kotlin | add | MQ | P-gen | arm64 | thru‡ | 17.16 | BigDecimal | 30.70 | **1.79×** | Rkosw2 | compact idiom peer |
| kotlin | add | OQ | P-gen | arm64 | thru‡ | 40.72 | BigDecimal | 74.82 | **1.84×** | Rkosw2 | compact idiom peer |
| kotlin | add | FQ | P-gen | arm64 | thru‡ | 20.55 | BigDecimal | 83.49 | **4.06×** | Rkosw2 | compact idiom peer |

<!-- END GENERATED add-rel-kotlin -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-kotlin-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | add | SQ | P-gen | x86_64 | thru‡ | 17.88 | BigDecimal | 57.85 | **3.24×** | xRkosw2 | compact idiom peer |
| kotlin | add | NQ | P-gen | x86_64 | thru‡ | 25.19 | BigDecimal | 95.03 | **3.77×** | xRkosw2 | compact idiom peer |
| kotlin | add | MQ | P-gen | x86_64 | thru‡ | 35.49 | BigDecimal | 86.60 | **2.44×** | xRkosw2 | compact idiom peer |
| kotlin | add | OQ | P-gen | x86_64 | thru‡ | 65.43 | BigDecimal | 175.16 | **2.68×** | xRkosw2 | compact idiom peer |
| kotlin | add | FQ | P-gen | x86_64 | thru‡ | 45.96 | BigDecimal | 194.54 | **4.23×** | xRkosw2 | compact idiom peer |

<!-- END GENERATED add-rel-kotlin-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-kotlin -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | sub | SQ | P-gen | arm64 | thru‡ | 4.89 | BigDecimal | 22.80 | **4.66×** | Rkosw2 | compact idiom peer |
| kotlin | sub | NQ | P-gen | arm64 | thru‡ | 9.29 | BigDecimal | 34.00 | **3.66×** | Rkosw2 | compact idiom peer |
| kotlin | sub | MQ | P-gen | arm64 | thru‡ | 17.70 | BigDecimal | 33.86 | **1.91×** | Rkosw2 | compact idiom peer |
| kotlin | sub | OQ | P-gen | arm64 | thru‡ | 41.65 | BigDecimal | 81.55 | **1.96×** | Rkosw2 | compact idiom peer |
| kotlin | sub | FQ | P-gen | arm64 | thru‡ | 19.16 | BigDecimal | 86.60 | **4.52×** | Rkosw2 | compact idiom peer |

<!-- END GENERATED sub-rel-kotlin -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-kotlin-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | sub | SQ | P-gen | x86_64 | thru‡ | 13.58 | BigDecimal | 64.22 | **4.73×** | xRkosw2 | compact idiom peer |
| kotlin | sub | NQ | P-gen | x86_64 | thru‡ | 26.78 | BigDecimal | 94.22 | **3.52×** | xRkosw2 | compact idiom peer |
| kotlin | sub | MQ | P-gen | x86_64 | thru‡ | 36.46 | BigDecimal | 100.45 | **2.76×** | xRkosw2 | compact idiom peer |
| kotlin | sub | OQ | P-gen | x86_64 | thru‡ | 64.82 | BigDecimal | 182.92 | **2.82×** | xRkosw2 | compact idiom peer |
| kotlin | sub | FQ | P-gen | x86_64 | thru‡ | 46.98 | BigDecimal | 209.86 | **4.47×** | xRkosw2 | compact idiom peer |

<!-- END GENERATED sub-rel-kotlin-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-kotlin -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | mul | CP | P-gen | arm64 | thru‡ | 5.61 | BigDecimal | 14.08 | **2.51×** | Rkosw2 | compact idiom peer |
| kotlin | mul | WP | P-gen | arm64 | thru‡ | 31.33 | BigDecimal | 55.16 | **1.76×** | Rkosw2 | compact idiom peer |
| kotlin | mul | XP | P-gen | arm64 | thru‡ | 49.75 | BigDecimal | 163.41 | **3.28×** | Rkosw2 | compact idiom peer |

<!-- END GENERATED mul-rel-kotlin -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-kotlin-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | mul | CP | P-gen | x86_64 | thru‡ | 14.93 | BigDecimal | 41.73 | **2.80×** | xRkosw2 | compact idiom peer |
| kotlin | mul | WP | P-gen | x86_64 | thru‡ | 50.69 | BigDecimal | 154.68 | **3.05×** | xRkosw2 | compact idiom peer |
| kotlin | mul | XP | P-gen | x86_64 | thru‡ | 72.70 | BigDecimal | 281.73 | **3.88×** | xRkosw2 | compact idiom peer |

<!-- END GENERATED mul-rel-kotlin-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-kotlin -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | div | CD | P-gen | arm64 | thru‡ | 36.47 | BigDecimal | 154.13 | **4.23×** | Rkosw2 | compact idiom peer |
| kotlin | div | WD | P-gen | arm64 | thru‡ | 47.37 | BigDecimal | 127.89 | **2.70×** | Rkosw2 | compact idiom peer |
| kotlin | div | XD | P-gen | arm64 | thru‡ | 51.94 | BigDecimal | 224.12 | **4.31×** | Rkosw2 | compact idiom peer |
| kotlin | div | ET | P-gen | arm64 | thru‡ | 19.12 | BigDecimal | 513.55 | **26.86×** | Rkosw2 | compact idiom peer |
| kotlin | div | PT | P-gen | arm64 | thru‡ | 11.86 | BigDecimal | 470.46 | **39.67×** | Rkosw2 | compact idiom peer |

<!-- END GENERATED div-rel-kotlin -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-kotlin-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | div | CD | P-gen | x86_64 | thru‡ | 96.06 | BigDecimal | 367.29 | **3.82×** | xRkosw2 | compact idiom peer |
| kotlin | div | WD | P-gen | x86_64 | thru‡ | 122.82 | BigDecimal | 265.12 | **2.16×** | xRkosw2 | compact idiom peer |
| kotlin | div | XD | P-gen | x86_64 | thru‡ | 132.51 | BigDecimal | 344.43 | **2.60×** | xRkosw2 | compact idiom peer |
| kotlin | div | ET | P-gen | x86_64 | thru‡ | 51.56 | BigDecimal | 1152.96 | **22.36×** | xRkosw2 | compact idiom peer |
| kotlin | div | PT | P-gen | x86_64 | thru‡ | 25.70 | BigDecimal | 1061.98 | **41.32×** | xRkosw2 | compact idiom peer |

<!-- END GENERATED div-rel-kotlin-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-kotlin -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | fma | FN | FMA | arm64 | thru‡ | 108.72 | libbid | 84.00 | **0.77×** | Rkosw2 |  |
| kotlin | fma | FF | FMA | arm64 | thru‡ | 82.63 | libbid | 57.07 | **0.69×** | Rkosw2 |  |

<!-- END GENERATED fma-rel-kotlin -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-kotlin-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kotlin | fma | FN | FMA | x86_64 | thru‡ | 233.51 | libbid | 160.41 | **0.69×** | xRkosw2 |  |
| kotlin | fma | FF | FMA | x86_64 | thru‡ | 178.64 | libbid | 123.46 | **0.69×** | xRkosw2 |  |

<!-- END GENERATED fma-rel-kotlin-x86 -->

</div>
