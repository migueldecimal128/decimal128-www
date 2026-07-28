---
layout: default
permalink: /benchmark/vs-csharp.html
title: "C# Benchmark Results — Decimal128"
description: "decimal128 in C#, measured against the alternatives available to it — a realistic financial mix (P-fin) plus per-operation band characterization, with explicit ratios."
heading: "C# Benchmark Results"
---

<div class="whitepaper" markdown="1">

<p class="whitepaper-meta">Living document — as-measured results. Category codes, profiles, modes &amp; method: <a href="key.html">Benchmark Key</a>.</p>

This is the **C#** view of decimal128 **as-measured**, band by band, with explicit ratios. It opens with the realistic financial-mix (**P-fin**) headline, then the per-operation band characterization (**P-gen**) and FMA. In C#, d128 is measured against its in-language idiom peer **`System.Decimal`** on the compact bands it can represent, and the conformant **.NET 11 `System.Numerics.Decimal128`** (arm64 only for now). C# takes no `libbid` fallback, so bands neither .NET type can represent show `-`. It is **data only** — the categories, magnitude profiles, units, and methodology are defined in the [Benchmark Key](key.html) (and, authoritatively, `BenchmarkMatrix.md`). The cross-port d128 band-shape matrices (all ports, no alternatives) live in [Port-Comparison Benchmark Results](port-compare.html); the full index of per-language pages is on the [Benchmarks](/benchmarks.html) hub.

## Summary — Ratio Range by Operation

Each row below is the ratio for that reference/idiom peer on x86_64 (Intel i9-9880H): `ratio = System.Decimal / Miguel` or `ratio = Decimal128 (.NET 11) / Miguel` (&gt; 1× ⇒ d128 faster), broken out by operation. `System.Decimal` has no wide-product multiply band, so that cell is blank.

| | Add | Subtract | Multiply | Divide |
|---|---|---|---|---|
| ratio = System.Decimal / Miguel | 0.8× | 0.9× | — | 0.5× – 5× |
| ratio = Decimal128 (.NET 11) / Miguel | 2.5× | 2.9× | 2.2× – 8× | 4× – 54× |

## FinMix — realistic financial mix (P-fin)

The headline: one realistic 64-bit financial operation mix — a `MIX` add/sub stream, mul `CP`/`WP`, div `CD`/`WD`/`ET`/`PT` — `ratio = alt / Miguel` (&gt; 1 ⇒ d128 faster). This is the profile closest to real financial code.

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED pfin-rel-csharp -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | add | MIX | P-fin | arm64 | thru | 2.70 | System.Decimal | 2.79 | **1.03×** | Rcs11 | compact idiom peer |
| csharp | sub | MIX | P-fin | arm64 | thru | 17.60 | System.Decimal | 2.94 | **0.17×** | Rcs11 | compact idiom peer |
| csharp | div | CD | P-fin | arm64 | thru | 24.25 | System.Decimal | 11.91 | **0.49×** | Rcs11 | compact idiom peer |
| csharp | div | WD | P-fin | arm64 | thru | 42.44 | System.Decimal | 26.87 | **0.63×** | Rcs11 | compact idiom peer |
| csharp | div | ET | P-fin | arm64 | thru | 9.15 | System.Decimal | 4.94 | **0.54×** | Rcs11 | compact idiom peer |
| csharp | div | PT | P-fin | arm64 | thru | 4.66 | System.Decimal | 11.96 | **2.57×** | Rcs11 | compact idiom peer |
| csharp | add | MIX | P-fin | arm64 | thru | 2.70 | Decimal128 (.NET 11) | 9.59 | **3.55×** | Rcs11 |  |
| csharp | sub | MIX | P-fin | arm64 | thru | 17.60 | Decimal128 (.NET 11) | 10.36 | **0.59×** | Rcs11 |  |
| csharp | mul | CP | P-fin | arm64 | thru | 1.64 | Decimal128 (.NET 11) | 9.64 | **5.88×** | Rcs11 |  |
| csharp | mul | WP | P-fin | arm64 | thru | 24.09 | Decimal128 (.NET 11) | 28.31 | **1.18×** | Rcs11 |  |
| csharp | div | CD | P-fin | arm64 | thru | 24.25 | Decimal128 (.NET 11) | 77.37 | **3.19×** | Rcs11 |  |
| csharp | div | WD | P-fin | arm64 | thru | 42.44 | Decimal128 (.NET 11) | 56.53 | **1.33×** | Rcs11 |  |
| csharp | div | ET | P-fin | arm64 | thru | 9.15 | Decimal128 (.NET 11) | 160.47 | **17.54×** | Rcs11 |  |
| csharp | div | PT | P-fin | arm64 | thru | 4.66 | Decimal128 (.NET 11) | 166.08 | **35.64×** | Rcs11 |  |

<!-- END GENERATED pfin-rel-csharp -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-csharp-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | add | MIX | P-fin | x86_64 | thru | 7.94 | System.Decimal | 10.85 | **1.37×** | xRcs11 | compact idiom peer |
| csharp | sub | MIX | P-fin | x86_64 | thru | 12.99 | System.Decimal | 13.54 | **1.04×** | xRcs11 | compact idiom peer |
| csharp | div | CD | P-fin | x86_64 | thru | 91.07 | System.Decimal | 61.30 | **0.67×** | xRcs11 | compact idiom peer |
| csharp | div | WD | P-fin | x86_64 | thru | 125.38 | System.Decimal | 111.18 | **0.89×** | xRcs11 | compact idiom peer |
| csharp | div | ET | P-fin | x86_64 | thru | 23.59 | System.Decimal | 15.46 | **0.66×** | xRcs11 | compact idiom peer |
| csharp | div | PT | P-fin | x86_64 | thru | 11.67 | System.Decimal | 67.63 | **5.80×** | xRcs11 | compact idiom peer |
| csharp | add | MIX | P-fin | x86_64 | thru | 7.94 | Decimal128 (.NET 11) | 36.59 | **4.61×** | xRcs11 |  |
| csharp | sub | MIX | P-fin | x86_64 | thru | 12.99 | Decimal128 (.NET 11) | 41.82 | **3.22×** | xRcs11 |  |
| csharp | mul | CP | P-fin | x86_64 | thru | 5.49 | Decimal128 (.NET 11) | 43.29 | **7.89×** | xRcs11 |  |
| csharp | mul | WP | P-fin | x86_64 | thru | 56.17 | Decimal128 (.NET 11) | 138.46 | **2.47×** | xRcs11 |  |
| csharp | div | CD | P-fin | x86_64 | thru | 91.07 | Decimal128 (.NET 11) | 434.48 | **4.77×** | xRcs11 |  |
| csharp | div | WD | P-fin | x86_64 | thru | 125.38 | Decimal128 (.NET 11) | 481.02 | **3.84×** | xRcs11 |  |
| csharp | div | ET | P-fin | x86_64 | thru | 23.59 | Decimal128 (.NET 11) | 620.08 | **26.29×** | xRcs11 |  |
| csharp | div | PT | P-fin | x86_64 | thru | 11.67 | Decimal128 (.NET 11) | 630.77 | **54.05×** | xRcs11 |  |

<!-- END GENERATED pfin-rel-csharp-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-csharp -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | add | SQ | P-gen | arm64 | thru | 10.20 | System.Decimal | 2.54 | **0.25×** | Rcs11 | compact idiom peer |
| csharp | add | NQ | P-gen | arm64 | thru | 5.58 | System.Decimal | 4.08 | **0.73×** | Rcs11 | compact idiom peer |
| csharp | add | MQ | P-gen | arm64 | thru | 16.33 | System.Decimal | 4.01 | **0.25×** | Rcs11 | compact idiom peer |
| csharp | add | SQ | P-gen | arm64 | thru | 10.20 | Decimal128 (.NET 11) | 13.10 | **1.28×** | Rcs11 |  |
| csharp | add | NQ | P-gen | arm64 | thru | 5.58 | Decimal128 (.NET 11) | 14.50 | **2.60×** | Rcs11 |  |
| csharp | add | MQ | P-gen | arm64 | thru | 16.33 | Decimal128 (.NET 11) | 14.17 | **0.87×** | Rcs11 |  |
| csharp | add | OQ | P-gen | arm64 | thru | 40.62 | Decimal128 (.NET 11) | 99.53 | **2.45×** | Rcs11 |  |
| csharp | add | FQ | P-gen | arm64 | thru | 33.18 | Decimal128 (.NET 11) | 853.77 | **25.73×** | Rcs11 |  |

<!-- END GENERATED add-rel-csharp -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-csharp-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | add | SQ | P-gen | x86_64 | thru | 20.90 | System.Decimal | 11.67 | **0.56×** | xRcs11 | compact idiom peer |
| csharp | add | NQ | P-gen | x86_64 | thru | 17.05 | System.Decimal | 16.09 | **0.94×** | xRcs11 | compact idiom peer |
| csharp | add | MQ | P-gen | x86_64 | thru | 41.60 | System.Decimal | 17.99 | **0.43×** | xRcs11 | compact idiom peer |
| csharp | add | SQ | P-gen | x86_64 | thru | 20.90 | Decimal128 (.NET 11) | 62.54 | **2.99×** | xRcs11 |  |
| csharp | add | NQ | P-gen | x86_64 | thru | 17.05 | Decimal128 (.NET 11) | 64.76 | **3.80×** | xRcs11 |  |
| csharp | add | MQ | P-gen | x86_64 | thru | 41.60 | Decimal128 (.NET 11) | 65.55 | **1.58×** | xRcs11 |  |
| csharp | add | OQ | P-gen | x86_64 | thru | 84.43 | Decimal128 (.NET 11) | 359.83 | **4.26×** | xRcs11 |  |
| csharp | add | FQ | P-gen | x86_64 | thru | 63.64 | Decimal128 (.NET 11) | 3093.38 | **48.61×** | xRcs11 |  |

<!-- END GENERATED add-rel-csharp-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-csharp -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | sub | SQ | P-gen | arm64 | thru | 9.38 | System.Decimal | 2.84 | **0.30×** | Rcs11 | compact idiom peer |
| csharp | sub | NQ | P-gen | arm64 | thru | 6.15 | System.Decimal | 4.16 | **0.68×** | Rcs11 | compact idiom peer |
| csharp | sub | MQ | P-gen | arm64 | thru | 15.05 | System.Decimal | 4.00 | **0.27×** | Rcs11 | compact idiom peer |
| csharp | sub | SQ | P-gen | arm64 | thru | 9.38 | Decimal128 (.NET 11) | 13.34 | **1.42×** | Rcs11 |  |
| csharp | sub | NQ | P-gen | arm64 | thru | 6.15 | Decimal128 (.NET 11) | 14.16 | **2.30×** | Rcs11 |  |
| csharp | sub | MQ | P-gen | arm64 | thru | 15.05 | Decimal128 (.NET 11) | 14.25 | **0.95×** | Rcs11 |  |
| csharp | sub | OQ | P-gen | arm64 | thru | 39.89 | Decimal128 (.NET 11) | 101.83 | **2.55×** | Rcs11 |  |
| csharp | sub | FQ | P-gen | arm64 | thru | 33.67 | Decimal128 (.NET 11) | 822.16 | **24.42×** | Rcs11 |  |

<!-- END GENERATED sub-rel-csharp -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-csharp-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | sub | SQ | P-gen | x86_64 | thru | 19.44 | System.Decimal | 11.35 | **0.58×** | xRcs11 | compact idiom peer |
| csharp | sub | NQ | P-gen | x86_64 | thru | 16.24 | System.Decimal | 15.90 | **0.98×** | xRcs11 | compact idiom peer |
| csharp | sub | MQ | P-gen | x86_64 | thru | 40.31 | System.Decimal | 15.40 | **0.38×** | xRcs11 | compact idiom peer |
| csharp | sub | SQ | P-gen | x86_64 | thru | 19.44 | Decimal128 (.NET 11) | 64.93 | **3.34×** | xRcs11 |  |
| csharp | sub | NQ | P-gen | x86_64 | thru | 16.24 | Decimal128 (.NET 11) | 63.90 | **3.93×** | xRcs11 |  |
| csharp | sub | MQ | P-gen | x86_64 | thru | 40.31 | Decimal128 (.NET 11) | 66.83 | **1.66×** | xRcs11 |  |
| csharp | sub | OQ | P-gen | x86_64 | thru | 83.00 | Decimal128 (.NET 11) | 359.89 | **4.34×** | xRcs11 |  |
| csharp | sub | FQ | P-gen | x86_64 | thru | 63.84 | Decimal128 (.NET 11) | 3062.27 | **47.97×** | xRcs11 |  |

<!-- END GENERATED sub-rel-csharp-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-csharp -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | mul | CP | P-gen | arm64 | thru | 2.11 | Decimal128 (.NET 11) | 9.09 | **4.31×** | Rcs11 |  |
| csharp | mul | WP | P-gen | arm64 | thru | 22.27 | Decimal128 (.NET 11) | 30.48 | **1.37×** | Rcs11 |  |
| csharp | mul | XP | P-gen | arm64 | thru | 49.99 | Decimal128 (.NET 11) | 792.86 | **15.86×** | Rcs11 |  |

<!-- END GENERATED mul-rel-csharp -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-csharp-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | mul | CP | P-gen | x86_64 | thru | 7.30 | Decimal128 (.NET 11) | 38.28 | **5.24×** | xRcs11 |  |
| csharp | mul | WP | P-gen | x86_64 | thru | 49.87 | Decimal128 (.NET 11) | 141.35 | **2.83×** | xRcs11 |  |
| csharp | mul | XP | P-gen | x86_64 | thru | 84.32 | Decimal128 (.NET 11) | 2984.92 | **35.40×** | xRcs11 |  |

<!-- END GENERATED mul-rel-csharp-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-csharp -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | div | CD | P-gen | arm64 | thru | 27.65 | Decimal128 (.NET 11) | 70.76 | **2.56×** | Rcs11 |  |
| csharp | div | WD | P-gen | arm64 | thru | 46.43 | Decimal128 (.NET 11) | 57.85 | **1.25×** | Rcs11 |  |
| csharp | div | XD | P-gen | arm64 | thru | 45.98 | Decimal128 (.NET 11) | 110.00 | **2.39×** | Rcs11 |  |
| csharp | div | ET | P-gen | arm64 | thru | 9.60 | Decimal128 (.NET 11) | 143.94 | **14.99×** | Rcs11 |  |
| csharp | div | PT | P-gen | arm64 | thru | 4.76 | Decimal128 (.NET 11) | 142.65 | **29.97×** | Rcs11 |  |

<!-- END GENERATED div-rel-csharp -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-csharp-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | div | CD | P-gen | x86_64 | thru | 87.46 | Decimal128 (.NET 11) | 380.52 | **4.35×** | xRcs11 |  |
| csharp | div | WD | P-gen | x86_64 | thru | 110.23 | Decimal128 (.NET 11) | 453.55 | **4.11×** | xRcs11 |  |
| csharp | div | XD | P-gen | x86_64 | thru | 116.72 | Decimal128 (.NET 11) | 1205.03 | **10.32×** | xRcs11 |  |
| csharp | div | ET | P-gen | x86_64 | thru | 34.14 | Decimal128 (.NET 11) | 522.77 | **15.31×** | xRcs11 |  |
| csharp | div | PT | P-gen | x86_64 | thru | 11.64 | Decimal128 (.NET 11) | 525.07 | **45.11×** | xRcs11 |  |

<!-- END GENERATED div-rel-csharp-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-csharp -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | fma | FN | FMA | arm64 | thru | 105.25 | - | - | - | Rcs11 |  |
| csharp | fma | FF | FMA | arm64 | thru | 83.32 | - | - | - | Rcs11 |  |

<!-- END GENERATED fma-rel-csharp -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-csharp-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | fma | FN | FMA | x86_64 | thru | 187.32 | - | - | - | xRcs11 |  |
| csharp | fma | FF | FMA | x86_64 | thru | 140.98 | - | - | - | xRcs11 |  |

<!-- END GENERATED fma-rel-csharp-x86 -->

</div>
