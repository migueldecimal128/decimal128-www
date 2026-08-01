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
| csharp | add | MIX | P-fin | arm64 | thru | 2.78 | System.Decimal | 2.81 | **1.01×** | Rcs12 | compact idiom peer |
| csharp | sub | MIX | P-fin | arm64 | thru | 3.21 | System.Decimal | 2.83 | **0.88×** | Rcs12 | compact idiom peer |
| csharp | div | CD | P-fin | arm64 | thru | 22.88 | System.Decimal | 11.44 | **0.50×** | Rcs12 | compact idiom peer |
| csharp | div | WD | P-fin | arm64 | thru | 30.73 | System.Decimal | 19.10 | **0.62×** | Rcs12 | compact idiom peer |
| csharp | div | ET | P-fin | arm64 | thru | 4.94 | System.Decimal | 4.88 | **0.99×** | Rcs12 | compact idiom peer |
| csharp | div | PT | P-fin | arm64 | thru | 3.69 | System.Decimal | 11.17 | **3.03×** | Rcs12 | compact idiom peer |
| csharp | add | MIX | P-fin | arm64 | thru | 2.78 | Decimal128 (.NET 11) | 9.58 | **3.45×** | Rcs12 |  |
| csharp | sub | MIX | P-fin | arm64 | thru | 3.21 | Decimal128 (.NET 11) | 9.84 | **3.07×** | Rcs12 |  |
| csharp | mul | CP | P-fin | arm64 | thru | 1.72 | Decimal128 (.NET 11) | 8.78 | **5.10×** | Rcs12 |  |
| csharp | mul | WP | P-fin | arm64 | thru | 17.40 | Decimal128 (.NET 11) | 34.26 | **1.97×** | Rcs12 |  |
| csharp | div | CD | P-fin | arm64 | thru | 22.88 | Decimal128 (.NET 11) | 58.40 | **2.55×** | Rcs12 |  |
| csharp | div | WD | P-fin | arm64 | thru | 30.73 | Decimal128 (.NET 11) | 48.46 | **1.58×** | Rcs12 |  |
| csharp | div | ET | P-fin | arm64 | thru | 4.94 | Decimal128 (.NET 11) | 99.41 | **20.12×** | Rcs12 |  |
| csharp | div | PT | P-fin | arm64 | thru | 3.69 | Decimal128 (.NET 11) | 101.79 | **27.59×** | Rcs12 |  |

<!-- END GENERATED pfin-rel-csharp -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-csharp-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | add | MIX | P-fin | x86_64 | thru | 9.38 | System.Decimal | 9.43 | **1.01×** | xRcs12 | compact idiom peer |
| csharp | sub | MIX | P-fin | x86_64 | thru | 12.87 | System.Decimal | 11.33 | **0.88×** | xRcs12 | compact idiom peer |
| csharp | div | CD | P-fin | x86_64 | thru | 87.42 | System.Decimal | 58.21 | **0.67×** | xRcs12 | compact idiom peer |
| csharp | div | WD | P-fin | x86_64 | thru | 104.53 | System.Decimal | 104.34 | **1.00×** | xRcs12 | compact idiom peer |
| csharp | div | ET | P-fin | x86_64 | thru | 31.07 | System.Decimal | 16.63 | **0.54×** | xRcs12 | compact idiom peer |
| csharp | div | PT | P-fin | x86_64 | thru | 10.41 | System.Decimal | 63.55 | **6.10×** | xRcs12 | compact idiom peer |
| csharp | add | MIX | P-fin | x86_64 | thru | 9.38 | Decimal128 (.NET 11) | 25.79 | **2.75×** | xRcs12 |  |
| csharp | sub | MIX | P-fin | x86_64 | thru | 12.87 | Decimal128 (.NET 11) | 30.87 | **2.40×** | xRcs12 |  |
| csharp | mul | CP | P-fin | x86_64 | thru | 5.42 | Decimal128 (.NET 11) | 36.82 | **6.79×** | xRcs12 |  |
| csharp | mul | WP | P-fin | x86_64 | thru | 43.81 | Decimal128 (.NET 11) | 112.48 | **2.57×** | xRcs12 |  |
| csharp | div | CD | P-fin | x86_64 | thru | 87.42 | Decimal128 (.NET 11) | 213.80 | **2.45×** | xRcs12 |  |
| csharp | div | WD | P-fin | x86_64 | thru | 104.53 | Decimal128 (.NET 11) | 171.57 | **1.64×** | xRcs12 |  |
| csharp | div | ET | P-fin | x86_64 | thru | 31.07 | Decimal128 (.NET 11) | 404.35 | **13.01×** | xRcs12 |  |
| csharp | div | PT | P-fin | x86_64 | thru | 10.41 | Decimal128 (.NET 11) | 427.31 | **41.05×** | xRcs12 |  |

<!-- END GENERATED pfin-rel-csharp-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-csharp -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | add | SQss | P-gen | arm64 | thru | 1.44 | System.Decimal | 3.51 | **2.44×** | Rcs12 | compact idiom peer |
| csharp | add | SQos | P-gen | arm64 | thru | 2.92 | System.Decimal | 2.58 | **0.88×** | Rcs12 | compact idiom peer |
| csharp | add | NQss | P-gen | arm64 | thru | 6.20 | System.Decimal | 3.77 | **0.61×** | Rcs12 | compact idiom peer |
| csharp | add | NQos | P-gen | arm64 | thru | 6.98 | System.Decimal | 3.80 | **0.54×** | Rcs12 | compact idiom peer |
| csharp | add | MQss | P-gen | arm64 | thru | 10.27 | System.Decimal | 3.77 | **0.37×** | Rcs12 | compact idiom peer |
| csharp | add | MQos | P-gen | arm64 | thru | 15.46 | System.Decimal | 3.79 | **0.25×** | Rcs12 | compact idiom peer |
| csharp | add | SQss | P-gen | arm64 | thru | 1.44 | Decimal128 (.NET 11) | 11.96 | **8.31×** | Rcs12 |  |
| csharp | add | SQos | P-gen | arm64 | thru | 2.92 | Decimal128 (.NET 11) | 12.92 | **4.42×** | Rcs12 |  |
| csharp | add | NQss | P-gen | arm64 | thru | 6.20 | Decimal128 (.NET 11) | 14.38 | **2.32×** | Rcs12 |  |
| csharp | add | NQos | P-gen | arm64 | thru | 6.98 | Decimal128 (.NET 11) | 14.76 | **2.11×** | Rcs12 |  |
| csharp | add | MQss | P-gen | arm64 | thru | 10.27 | Decimal128 (.NET 11) | 15.77 | **1.54×** | Rcs12 |  |
| csharp | add | MQos | P-gen | arm64 | thru | 15.46 | Decimal128 (.NET 11) | 15.25 | **0.99×** | Rcs12 |  |
| csharp | add | OQss | P-gen | arm64 | thru | 17.35 | Decimal128 (.NET 11) | 94.89 | **5.47×** | Rcs12 |  |
| csharp | add | OQos | P-gen | arm64 | thru | 25.12 | Decimal128 (.NET 11) | 95.25 | **3.79×** | Rcs12 |  |
| csharp | add | FQss | P-gen | arm64 | thru | 10.38 | Decimal128 (.NET 11) | 690.96 | **66.57×** | Rcs12 |  |
| csharp | add | FQos | P-gen | arm64 | thru | 14.92 | Decimal128 (.NET 11) | 709.82 | **47.58×** | Rcs12 |  |

<!-- END GENERATED add-rel-csharp -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-csharp-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | add | SQss | P-gen | x86_64 | thru | 4.12 | System.Decimal | 7.96 | **1.93×** | xRcs12 | compact idiom peer |
| csharp | add | SQos | P-gen | x86_64 | thru | 12.53 | System.Decimal | 11.35 | **0.91×** | xRcs12 | compact idiom peer |
| csharp | add | NQss | P-gen | x86_64 | thru | 16.26 | System.Decimal | 12.25 | **0.75×** | xRcs12 | compact idiom peer |
| csharp | add | NQos | P-gen | x86_64 | thru | 22.84 | System.Decimal | 14.14 | **0.62×** | xRcs12 | compact idiom peer |
| csharp | add | MQss | P-gen | x86_64 | thru | 23.41 | System.Decimal | 12.07 | **0.52×** | xRcs12 | compact idiom peer |
| csharp | add | MQos | P-gen | x86_64 | thru | 45.14 | System.Decimal | 14.35 | **0.32×** | xRcs12 | compact idiom peer |
| csharp | add | SQss | P-gen | x86_64 | thru | 4.12 | Decimal128 (.NET 11) | 49.88 | **12.11×** | xRcs12 |  |
| csharp | add | SQos | P-gen | x86_64 | thru | 12.53 | Decimal128 (.NET 11) | 53.10 | **4.24×** | xRcs12 |  |
| csharp | add | NQss | P-gen | x86_64 | thru | 16.26 | Decimal128 (.NET 11) | 55.62 | **3.42×** | xRcs12 |  |
| csharp | add | NQos | P-gen | x86_64 | thru | 22.84 | Decimal128 (.NET 11) | 60.26 | **2.64×** | xRcs12 |  |
| csharp | add | MQss | P-gen | x86_64 | thru | 23.41 | Decimal128 (.NET 11) | 57.87 | **2.47×** | xRcs12 |  |
| csharp | add | MQos | P-gen | x86_64 | thru | 45.14 | Decimal128 (.NET 11) | 62.82 | **1.39×** | xRcs12 |  |
| csharp | add | OQss | P-gen | x86_64 | thru | 50.70 | Decimal128 (.NET 11) | 290.37 | **5.73×** | xRcs12 |  |
| csharp | add | OQos | P-gen | x86_64 | thru | 73.96 | Decimal128 (.NET 11) | 294.06 | **3.98×** | xRcs12 |  |
| csharp | add | FQss | P-gen | x86_64 | thru | 32.61 | Decimal128 (.NET 11) | 1882.26 | **57.72×** | xRcs12 |  |
| csharp | add | FQos | P-gen | x86_64 | thru | 45.98 | Decimal128 (.NET 11) | 1887.70 | **41.05×** | xRcs12 |  |

<!-- END GENERATED add-rel-csharp-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-csharp -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | sub | SQss | P-gen | arm64 | thru | 2.27 | System.Decimal | 2.45 | **1.08×** | Rcs12 | compact idiom peer |
| csharp | sub | SQos | P-gen | arm64 | thru | 1.68 | System.Decimal | 2.89 | **1.72×** | Rcs12 | compact idiom peer |
| csharp | sub | NQss | P-gen | arm64 | thru | 6.31 | System.Decimal | 3.81 | **0.60×** | Rcs12 | compact idiom peer |
| csharp | sub | NQos | P-gen | arm64 | thru | 5.17 | System.Decimal | 3.85 | **0.74×** | Rcs12 | compact idiom peer |
| csharp | sub | MQss | P-gen | arm64 | thru | 14.38 | System.Decimal | 3.88 | **0.27×** | Rcs12 | compact idiom peer |
| csharp | sub | MQos | P-gen | arm64 | thru | 8.59 | System.Decimal | 4.02 | **0.47×** | Rcs12 | compact idiom peer |
| csharp | sub | SQss | P-gen | arm64 | thru | 2.27 | Decimal128 (.NET 11) | 13.14 | **5.79×** | Rcs12 |  |
| csharp | sub | SQos | P-gen | arm64 | thru | 1.68 | Decimal128 (.NET 11) | 11.84 | **7.05×** | Rcs12 |  |
| csharp | sub | NQss | P-gen | arm64 | thru | 6.31 | Decimal128 (.NET 11) | 14.45 | **2.29×** | Rcs12 |  |
| csharp | sub | NQos | P-gen | arm64 | thru | 5.17 | Decimal128 (.NET 11) | 14.23 | **2.75×** | Rcs12 |  |
| csharp | sub | MQss | P-gen | arm64 | thru | 14.38 | Decimal128 (.NET 11) | 15.02 | **1.04×** | Rcs12 |  |
| csharp | sub | MQos | P-gen | arm64 | thru | 8.59 | Decimal128 (.NET 11) | 15.52 | **1.81×** | Rcs12 |  |
| csharp | sub | OQss | P-gen | arm64 | thru | 23.37 | Decimal128 (.NET 11) | 94.85 | **4.06×** | Rcs12 |  |
| csharp | sub | OQos | P-gen | arm64 | thru | 16.48 | Decimal128 (.NET 11) | 94.14 | **5.71×** | Rcs12 |  |
| csharp | sub | FQss | P-gen | arm64 | thru | 13.44 | Decimal128 (.NET 11) | 710.87 | **52.89×** | Rcs12 |  |
| csharp | sub | FQos | P-gen | arm64 | thru | 9.18 | Decimal128 (.NET 11) | 699.82 | **76.23×** | Rcs12 |  |

<!-- END GENERATED sub-rel-csharp -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-csharp-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | sub | SQss | P-gen | x86_64 | thru | 10.26 | System.Decimal | 10.79 | **1.05×** | xRcs12 | compact idiom peer |
| csharp | sub | SQos | P-gen | x86_64 | thru | 4.94 | System.Decimal | 7.97 | **1.61×** | xRcs12 | compact idiom peer |
| csharp | sub | NQss | P-gen | x86_64 | thru | 19.64 | System.Decimal | 14.77 | **0.75×** | xRcs12 | compact idiom peer |
| csharp | sub | NQos | P-gen | x86_64 | thru | 12.48 | System.Decimal | 12.24 | **0.98×** | xRcs12 | compact idiom peer |
| csharp | sub | MQss | P-gen | x86_64 | thru | 43.08 | System.Decimal | 14.00 | **0.32×** | xRcs12 | compact idiom peer |
| csharp | sub | MQos | P-gen | x86_64 | thru | 20.11 | System.Decimal | 12.83 | **0.64×** | xRcs12 | compact idiom peer |
| csharp | sub | SQss | P-gen | x86_64 | thru | 10.26 | Decimal128 (.NET 11) | 55.03 | **5.36×** | xRcs12 |  |
| csharp | sub | SQos | P-gen | x86_64 | thru | 4.94 | Decimal128 (.NET 11) | 49.63 | **10.05×** | xRcs12 |  |
| csharp | sub | NQss | P-gen | x86_64 | thru | 19.64 | Decimal128 (.NET 11) | 62.03 | **3.16×** | xRcs12 |  |
| csharp | sub | NQos | P-gen | x86_64 | thru | 12.48 | Decimal128 (.NET 11) | 57.17 | **4.58×** | xRcs12 |  |
| csharp | sub | MQss | P-gen | x86_64 | thru | 43.08 | Decimal128 (.NET 11) | 61.83 | **1.44×** | xRcs12 |  |
| csharp | sub | MQos | P-gen | x86_64 | thru | 20.11 | Decimal128 (.NET 11) | 58.67 | **2.92×** | xRcs12 |  |
| csharp | sub | OQss | P-gen | x86_64 | thru | 70.18 | Decimal128 (.NET 11) | 296.22 | **4.22×** | xRcs12 |  |
| csharp | sub | OQos | P-gen | x86_64 | thru | 47.78 | Decimal128 (.NET 11) | 293.50 | **6.14×** | xRcs12 |  |
| csharp | sub | FQss | P-gen | x86_64 | thru | 51.51 | Decimal128 (.NET 11) | 1883.94 | **36.57×** | xRcs12 |  |
| csharp | sub | FQos | P-gen | x86_64 | thru | 29.04 | Decimal128 (.NET 11) | 1882.67 | **64.83×** | xRcs12 |  |

<!-- END GENERATED sub-rel-csharp-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-csharp -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | mul | CP | P-gen | arm64 | thru | 2.15 | Decimal128 (.NET 11) | 8.86 | **4.12×** | Rcs12 |  |
| csharp | mul | WP | P-gen | arm64 | thru | 16.42 | Decimal128 (.NET 11) | 30.13 | **1.83×** | Rcs12 |  |
| csharp | mul | XP | P-gen | arm64 | thru | 43.68 | Decimal128 (.NET 11) | 705.88 | **16.16×** | Rcs12 |  |

<!-- END GENERATED mul-rel-csharp -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-csharp-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | mul | CP | P-gen | x86_64 | thru | 8.09 | Decimal128 (.NET 11) | 38.98 | **4.82×** | xRcs12 |  |
| csharp | mul | WP | P-gen | x86_64 | thru | 46.02 | Decimal128 (.NET 11) | 111.40 | **2.42×** | xRcs12 |  |
| csharp | mul | XP | P-gen | x86_64 | thru | 86.77 | Decimal128 (.NET 11) | 1814.36 | **20.91×** | xRcs12 |  |

<!-- END GENERATED mul-rel-csharp-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-csharp -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | div | CD | P-gen | arm64 | thru | 23.76 | Decimal128 (.NET 11) | 53.22 | **2.24×** | Rcs12 |  |
| csharp | div | WD | P-gen | arm64 | thru | 30.64 | Decimal128 (.NET 11) | 49.30 | **1.61×** | Rcs12 |  |
| csharp | div | XD | P-gen | arm64 | thru | 31.84 | Decimal128 (.NET 11) | 108.17 | **3.40×** | Rcs12 |  |
| csharp | div | ET | P-gen | arm64 | thru | 6.91 | Decimal128 (.NET 11) | 90.94 | **13.16×** | Rcs12 |  |
| csharp | div | PT | P-gen | arm64 | thru | 3.54 | Decimal128 (.NET 11) | 88.90 | **25.11×** | Rcs12 |  |

<!-- END GENERATED div-rel-csharp -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-csharp-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | div | CD | P-gen | x86_64 | thru | 92.95 | Decimal128 (.NET 11) | 216.70 | **2.33×** | xRcs12 |  |
| csharp | div | WD | P-gen | x86_64 | thru | 106.44 | Decimal128 (.NET 11) | 187.58 | **1.76×** | xRcs12 |  |
| csharp | div | XD | P-gen | x86_64 | thru | 108.38 | Decimal128 (.NET 11) | 322.83 | **2.98×** | xRcs12 |  |
| csharp | div | ET | P-gen | x86_64 | thru | 37.68 | Decimal128 (.NET 11) | 385.60 | **10.23×** | xRcs12 |  |
| csharp | div | PT | P-gen | x86_64 | thru | 10.22 | Decimal128 (.NET 11) | 376.73 | **36.86×** | xRcs12 |  |

<!-- END GENERATED div-rel-csharp-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-csharp -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | fma | FN | FMA | arm64 | thru | 103.04 | - | - | - | Rcs12 |  |
| csharp | fma | FF | FMA | arm64 | thru | 74.62 | - | - | - | Rcs12 |  |

<!-- END GENERATED fma-rel-csharp -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-csharp-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | fma | FN | FMA | x86_64 | thru | 207.75 | - | - | - | xRcs12 |  |
| csharp | fma | FF | FMA | x86_64 | thru | 148.05 | - | - | - | xRcs12 |  |

<!-- END GENERATED fma-rel-csharp-x86 -->

</div>
