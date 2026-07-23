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
| csharp | add | MIX | P-fin | arm64 | thru | 3.93 | System.Decimal | 3.00 | **0.76×** | Rcs11 | compact idiom peer |
| csharp | sub | MIX | P-fin | arm64 | thru | 2.97 | System.Decimal | 2.99 | **1.01×** | Rcs11 | compact idiom peer |
| csharp | div | CD | P-fin | arm64 | thru | 25.93 | System.Decimal | 11.26 | **0.43×** | Rcs11 | compact idiom peer |
| csharp | div | WD | P-fin | arm64 | thru | 44.58 | System.Decimal | 28.00 | **0.63×** | Rcs11 | compact idiom peer |
| csharp | div | ET | P-fin | arm64 | thru | 14.15 | System.Decimal | 4.91 | **0.35×** | Rcs11 | compact idiom peer |
| csharp | div | PT | P-fin | arm64 | thru | 5.32 | System.Decimal | 12.49 | **2.35×** | Rcs11 | compact idiom peer |
| csharp | add | MIX | P-fin | arm64 | thru | 3.93 | Decimal128 (.NET 11) | 16.24 | **4.13×** | Rcs11 |  |
| csharp | sub | MIX | P-fin | arm64 | thru | 2.97 | Decimal128 (.NET 11) | 15.66 | **5.27×** | Rcs11 |  |
| csharp | mul | CP | P-fin | arm64 | thru | 1.76 | Decimal128 (.NET 11) | 11.00 | **6.25×** | Rcs11 |  |
| csharp | mul | WP | P-fin | arm64 | thru | 24.54 | Decimal128 (.NET 11) | 48.89 | **1.99×** | Rcs11 |  |
| csharp | div | CD | P-fin | arm64 | thru | 25.93 | Decimal128 (.NET 11) | 160.70 | **6.20×** | Rcs11 |  |
| csharp | div | WD | P-fin | arm64 | thru | 44.58 | Decimal128 (.NET 11) | 185.48 | **4.16×** | Rcs11 |  |
| csharp | div | ET | P-fin | arm64 | thru | 14.15 | Decimal128 (.NET 11) | 237.57 | **16.79×** | Rcs11 |  |
| csharp | div | PT | P-fin | arm64 | thru | 5.32 | Decimal128 (.NET 11) | 243.46 | **45.76×** | Rcs11 |  |

<!-- END GENERATED pfin-rel-csharp -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-csharp-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | add | MIX | P-fin | x86_64 | thru | 17.25 | System.Decimal | 13.57 | **0.79×** | xRcs11 | compact idiom peer |
| csharp | sub | MIX | P-fin | x86_64 | thru | 15.03 | System.Decimal | 13.00 | **0.86×** | xRcs11 | compact idiom peer |
| csharp | div | CD | P-fin | x86_64 | thru | 113.08 | System.Decimal | 59.82 | **0.53×** | xRcs11 | compact idiom peer |
| csharp | div | WD | P-fin | x86_64 | thru | 135.01 | System.Decimal | 116.11 | **0.86×** | xRcs11 | compact idiom peer |
| csharp | div | ET | P-fin | x86_64 | thru | 30.32 | System.Decimal | 17.09 | **0.56×** | xRcs11 | compact idiom peer |
| csharp | div | PT | P-fin | x86_64 | thru | 12.62 | System.Decimal | 66.66 | **5.28×** | xRcs11 | compact idiom peer |
| csharp | add | MIX | P-fin | x86_64 | thru | 17.25 | Decimal128 (.NET 11) | 43.78 | **2.54×** | xRcs11 |  |
| csharp | sub | MIX | P-fin | x86_64 | thru | 15.03 | Decimal128 (.NET 11) | 44.07 | **2.93×** | xRcs11 |  |
| csharp | mul | CP | P-fin | x86_64 | thru | 5.61 | Decimal128 (.NET 11) | 42.53 | **7.58×** | xRcs11 |  |
| csharp | mul | WP | P-fin | x86_64 | thru | 62.00 | Decimal128 (.NET 11) | 137.25 | **2.21×** | xRcs11 |  |
| csharp | div | CD | P-fin | x86_64 | thru | 113.08 | Decimal128 (.NET 11) | 460.60 | **4.07×** | xRcs11 |  |
| csharp | div | WD | P-fin | x86_64 | thru | 135.01 | Decimal128 (.NET 11) | 514.48 | **3.81×** | xRcs11 |  |
| csharp | div | ET | P-fin | x86_64 | thru | 30.32 | Decimal128 (.NET 11) | 666.38 | **21.98×** | xRcs11 |  |
| csharp | div | PT | P-fin | x86_64 | thru | 12.62 | Decimal128 (.NET 11) | 683.01 | **54.12×** | xRcs11 |  |

<!-- END GENERATED pfin-rel-csharp-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-csharp -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | add | SQ | P-gen | arm64 | thru | 5.84 | System.Decimal | 2.50 | **0.43×** | Rcs11 | compact idiom peer |
| csharp | add | NQ | P-gen | arm64 | thru | 4.89 | System.Decimal | 4.15 | **0.85×** | Rcs11 | compact idiom peer |
| csharp | add | MQ | P-gen | arm64 | thru | 15.26 | System.Decimal | 4.12 | **0.27×** | Rcs11 | compact idiom peer |
| csharp | add | SQ | P-gen | arm64 | thru | 5.84 | Decimal128 (.NET 11) | 20.16 | **3.45×** | Rcs11 |  |
| csharp | add | NQ | P-gen | arm64 | thru | 4.89 | Decimal128 (.NET 11) | 19.91 | **4.07×** | Rcs11 |  |
| csharp | add | MQ | P-gen | arm64 | thru | 15.26 | Decimal128 (.NET 11) | 20.12 | **1.32×** | Rcs11 |  |
| csharp | add | OQ | P-gen | arm64 | thru | 39.66 | Decimal128 (.NET 11) | 143.74 | **3.62×** | Rcs11 |  |
| csharp | add | FQ | P-gen | arm64 | thru | 34.78 | Decimal128 (.NET 11) | 1253.19 | **36.03×** | Rcs11 |  |

<!-- END GENERATED add-rel-csharp -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-csharp-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | add | SQ | P-gen | x86_64 | thru | 18.92 | System.Decimal | 13.91 | **0.74×** | xRcs11 | compact idiom peer |
| csharp | add | NQ | P-gen | x86_64 | thru | 18.33 | System.Decimal | 18.59 | **1.01×** | xRcs11 | compact idiom peer |
| csharp | add | MQ | P-gen | x86_64 | thru | 57.26 | System.Decimal | 20.10 | **0.35×** | xRcs11 | compact idiom peer |
| csharp | add | SQ | P-gen | x86_64 | thru | 18.92 | Decimal128 (.NET 11) | 68.08 | **3.60×** | xRcs11 |  |
| csharp | add | NQ | P-gen | x86_64 | thru | 18.33 | Decimal128 (.NET 11) | 71.79 | **3.92×** | xRcs11 |  |
| csharp | add | MQ | P-gen | x86_64 | thru | 57.26 | Decimal128 (.NET 11) | 73.29 | **1.28×** | xRcs11 |  |
| csharp | add | OQ | P-gen | x86_64 | thru | 85.87 | Decimal128 (.NET 11) | 374.11 | **4.36×** | xRcs11 |  |
| csharp | add | FQ | P-gen | x86_64 | thru | 65.57 | Decimal128 (.NET 11) | 3333.93 | **50.85×** | xRcs11 |  |

<!-- END GENERATED add-rel-csharp-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-csharp -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | sub | SQ | P-gen | arm64 | thru | 9.20 | System.Decimal | 2.50 | **0.27×** | Rcs11 | compact idiom peer |
| csharp | sub | NQ | P-gen | arm64 | thru | 6.28 | System.Decimal | 4.13 | **0.66×** | Rcs11 | compact idiom peer |
| csharp | sub | MQ | P-gen | arm64 | thru | 15.43 | System.Decimal | 4.11 | **0.27×** | Rcs11 | compact idiom peer |
| csharp | sub | SQ | P-gen | arm64 | thru | 9.20 | Decimal128 (.NET 11) | 19.56 | **2.13×** | Rcs11 |  |
| csharp | sub | NQ | P-gen | arm64 | thru | 6.28 | Decimal128 (.NET 11) | 19.44 | **3.10×** | Rcs11 |  |
| csharp | sub | MQ | P-gen | arm64 | thru | 15.43 | Decimal128 (.NET 11) | 20.42 | **1.32×** | Rcs11 |  |
| csharp | sub | OQ | P-gen | arm64 | thru | 40.45 | Decimal128 (.NET 11) | 143.87 | **3.56×** | Rcs11 |  |
| csharp | sub | FQ | P-gen | arm64 | thru | 33.61 | Decimal128 (.NET 11) | 1259.90 | **37.49×** | Rcs11 |  |

<!-- END GENERATED sub-rel-csharp -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-csharp-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | sub | SQ | P-gen | x86_64 | thru | 22.52 | System.Decimal | 12.93 | **0.57×** | xRcs11 | compact idiom peer |
| csharp | sub | NQ | P-gen | x86_64 | thru | 17.83 | System.Decimal | 18.20 | **1.02×** | xRcs11 | compact idiom peer |
| csharp | sub | MQ | P-gen | x86_64 | thru | 57.55 | System.Decimal | 17.61 | **0.31×** | xRcs11 | compact idiom peer |
| csharp | sub | SQ | P-gen | x86_64 | thru | 22.52 | Decimal128 (.NET 11) | 68.70 | **3.05×** | xRcs11 |  |
| csharp | sub | NQ | P-gen | x86_64 | thru | 17.83 | Decimal128 (.NET 11) | 71.25 | **4.00×** | xRcs11 |  |
| csharp | sub | MQ | P-gen | x86_64 | thru | 57.55 | Decimal128 (.NET 11) | 73.98 | **1.29×** | xRcs11 |  |
| csharp | sub | OQ | P-gen | x86_64 | thru | 87.29 | Decimal128 (.NET 11) | 373.76 | **4.28×** | xRcs11 |  |
| csharp | sub | FQ | P-gen | x86_64 | thru | 65.89 | Decimal128 (.NET 11) | 3310.77 | **50.25×** | xRcs11 |  |

<!-- END GENERATED sub-rel-csharp-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-csharp -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | mul | CP | P-gen | arm64 | thru | 2.67 | Decimal128 (.NET 11) | 10.99 | **4.12×** | Rcs11 |  |
| csharp | mul | WP | P-gen | arm64 | thru | 27.80 | Decimal128 (.NET 11) | 51.66 | **1.86×** | Rcs11 |  |
| csharp | mul | XP | P-gen | arm64 | thru | 47.67 | Decimal128 (.NET 11) | 1221.77 | **25.63×** | Rcs11 |  |

<!-- END GENERATED mul-rel-csharp -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-csharp-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | mul | CP | P-gen | x86_64 | thru | 8.42 | Decimal128 (.NET 11) | 41.94 | **4.98×** | xRcs11 |  |
| csharp | mul | WP | P-gen | x86_64 | thru | 67.54 | Decimal128 (.NET 11) | 138.43 | **2.05×** | xRcs11 |  |
| csharp | mul | XP | P-gen | x86_64 | thru | 95.83 | Decimal128 (.NET 11) | 3222.82 | **33.63×** | xRcs11 |  |

<!-- END GENERATED mul-rel-csharp-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-csharp -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | div | CD | P-gen | arm64 | thru | 30.16 | Decimal128 (.NET 11) | 121.16 | **4.02×** | Rcs11 |  |
| csharp | div | WD | P-gen | arm64 | thru | 47.96 | Decimal128 (.NET 11) | 158.68 | **3.31×** | Rcs11 |  |
| csharp | div | XD | P-gen | arm64 | thru | 49.41 | Decimal128 (.NET 11) | 563.13 | **11.40×** | Rcs11 |  |
| csharp | div | ET | P-gen | arm64 | thru | 19.26 | Decimal128 (.NET 11) | 155.59 | **8.08×** | Rcs11 |  |
| csharp | div | PT | P-gen | arm64 | thru | 10.40 | Decimal128 (.NET 11) | 153.04 | **14.72×** | Rcs11 |  |

<!-- END GENERATED div-rel-csharp -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-csharp-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | div | CD | P-gen | x86_64 | thru | 122.15 | Decimal128 (.NET 11) | 408.72 | **3.35×** | xRcs11 |  |
| csharp | div | WD | P-gen | x86_64 | thru | 136.75 | Decimal128 (.NET 11) | 483.97 | **3.54×** | xRcs11 |  |
| csharp | div | XD | P-gen | x86_64 | thru | 131.43 | Decimal128 (.NET 11) | 1301.82 | **9.91×** | xRcs11 |  |
| csharp | div | ET | P-gen | x86_64 | thru | 56.04 | Decimal128 (.NET 11) | 598.66 | **10.68×** | xRcs11 |  |
| csharp | div | PT | P-gen | x86_64 | thru | 12.94 | Decimal128 (.NET 11) | 564.60 | **43.63×** | xRcs11 |  |

<!-- END GENERATED div-rel-csharp-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-csharp -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | fma | FN | FMA | arm64 | thru | 95.97 | - | - | - | Rcs11 |  |
| csharp | fma | FF | FMA | arm64 | thru | 72.25 | - | - | - | Rcs11 |  |

<!-- END GENERATED fma-rel-csharp -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-csharp-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | fma | FN | FMA | x86_64 | thru | 201.21 | - | - | - | xRcs11 |  |
| csharp | fma | FF | FMA | x86_64 | thru | 167.63 | - | - | - | xRcs11 |  |

<!-- END GENERATED fma-rel-csharp-x86 -->

</div>
