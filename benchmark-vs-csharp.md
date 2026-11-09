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
| ratio = System.Decimal / Miguel | 0.9× | 0.7× | — | 0.6× – 5× |
| ratio = Decimal128 (.NET 11) / Miguel | 2.2× | 2.2× | 2.4× – 5× | 1.6× – 36× |

## FinMix — realistic financial mix (P-fin)

The headline: one realistic 64-bit financial operation mix — a `MIX` add/sub stream, mul `CP`/`WP`, div `CD`/`WD`/`ET`/`PT` — `ratio = alt / Miguel` (&gt; 1 ⇒ d128 faster). This is the profile closest to real financial code.

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED pfin-rel-csharp -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | add | MIX | P-fin | arm64 | thru | 2.79 | System.Decimal | 2.84 | **1.02×** | Rcs11 | compact idiom peer |
| csharp | sub | MIX | P-fin | arm64 | thru | 3.17 | System.Decimal | 2.75 | **0.87×** | Rcs11 | compact idiom peer |
| csharp | div | CD | P-fin | arm64 | thru | 21.45 | System.Decimal | 11.38 | **0.53×** | Rcs11 | compact idiom peer |
| csharp | div | WD | P-fin | arm64 | thru | 24.81 | System.Decimal | 19.05 | **0.77×** | Rcs11 | compact idiom peer |
| csharp | div | ET | P-fin | arm64 | thru | 4.90 | System.Decimal | 5.22 | **1.07×** | Rcs11 | compact idiom peer |
| csharp | div | PT | P-fin | arm64 | thru | 3.45 | System.Decimal | 11.04 | **3.20×** | Rcs11 | compact idiom peer |
| csharp | add | MIX | P-fin | arm64 | thru | 2.79 | Decimal128 (.NET 11) | 9.18 | **3.29×** | Rcs11 |  |
| csharp | sub | MIX | P-fin | arm64 | thru | 3.17 | Decimal128 (.NET 11) | 9.04 | **2.85×** | Rcs11 |  |
| csharp | mul | CP | P-fin | arm64 | thru | 1.69 | Decimal128 (.NET 11) | 8.78 | **5.20×** | Rcs11 |  |
| csharp | mul | WP | P-fin | arm64 | thru | 17.45 | Decimal128 (.NET 11) | 30.00 | **1.72×** | Rcs11 |  |
| csharp | div | CD | P-fin | arm64 | thru | 21.45 | Decimal128 (.NET 11) | 58.85 | **2.74×** | Rcs11 |  |
| csharp | div | WD | P-fin | arm64 | thru | 24.81 | Decimal128 (.NET 11) | 49.18 | **1.98×** | Rcs11 |  |
| csharp | div | ET | P-fin | arm64 | thru | 4.90 | Decimal128 (.NET 11) | 102.24 | **20.87×** | Rcs11 |  |
| csharp | div | PT | P-fin | arm64 | thru | 3.45 | Decimal128 (.NET 11) | 103.17 | **29.90×** | Rcs11 |  |

<!-- END GENERATED pfin-rel-csharp -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-csharp-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | add | MIX | P-fin | x86_64 | thru | 11.49 | System.Decimal | 11.35 | **0.99×** | xRcs11 | compact idiom peer |
| csharp | sub | MIX | P-fin | x86_64 | thru | 14.98 | System.Decimal | 11.51 | **0.77×** | xRcs11 | compact idiom peer |
| csharp | div | CD | P-fin | x86_64 | thru | 90.03 | System.Decimal | 59.00 | **0.66×** | xRcs11 | compact idiom peer |
| csharp | div | WD | P-fin | x86_64 | thru | 104.10 | System.Decimal | 116.65 | **1.12×** | xRcs11 | compact idiom peer |
| csharp | div | ET | P-fin | x86_64 | thru | 29.23 | System.Decimal | 20.69 | **0.71×** | xRcs11 | compact idiom peer |
| csharp | div | PT | P-fin | x86_64 | thru | 12.00 | System.Decimal | 65.24 | **5.44×** | xRcs11 | compact idiom peer |
| csharp | add | MIX | P-fin | x86_64 | thru | 11.49 | Decimal128 (.NET 11) | 26.19 | **2.28×** | xRcs11 |  |
| csharp | sub | MIX | P-fin | x86_64 | thru | 14.98 | Decimal128 (.NET 11) | 32.89 | **2.20×** | xRcs11 |  |
| csharp | mul | CP | P-fin | x86_64 | thru | 6.74 | Decimal128 (.NET 11) | 37.15 | **5.51×** | xRcs11 |  |
| csharp | mul | WP | P-fin | x86_64 | thru | 44.97 | Decimal128 (.NET 11) | 110.69 | **2.46×** | xRcs11 |  |
| csharp | div | CD | P-fin | x86_64 | thru | 90.03 | Decimal128 (.NET 11) | 213.19 | **2.37×** | xRcs11 |  |
| csharp | div | WD | P-fin | x86_64 | thru | 104.10 | Decimal128 (.NET 11) | 171.07 | **1.64×** | xRcs11 |  |
| csharp | div | ET | P-fin | x86_64 | thru | 29.23 | Decimal128 (.NET 11) | 419.91 | **14.37×** | xRcs11 |  |
| csharp | div | PT | P-fin | x86_64 | thru | 12.00 | Decimal128 (.NET 11) | 433.44 | **36.12×** | xRcs11 |  |

<!-- END GENERATED pfin-rel-csharp-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-csharp -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | add | SQss | P-gen | arm64 | thru | 1.26 | System.Decimal | 2.92 | **2.32×** | Rcs11 | compact idiom peer |
| csharp | add | SQos | P-gen | arm64 | thru | 2.89 | System.Decimal | 2.91 | **1.01×** | Rcs11 | compact idiom peer |
| csharp | add | NQss | P-gen | arm64 | thru | 6.32 | System.Decimal | 3.91 | **0.62×** | Rcs11 | compact idiom peer |
| csharp | add | NQos | P-gen | arm64 | thru | 7.01 | System.Decimal | 3.81 | **0.54×** | Rcs11 | compact idiom peer |
| csharp | add | MQss | P-gen | arm64 | thru | 10.68 | System.Decimal | 3.72 | **0.35×** | Rcs11 | compact idiom peer |
| csharp | add | MQos | P-gen | arm64 | thru | 14.70 | System.Decimal | 3.78 | **0.26×** | Rcs11 | compact idiom peer |
| csharp | add | SQss | P-gen | arm64 | thru | 1.26 | Decimal128 (.NET 11) | 11.08 | **8.79×** | Rcs11 |  |
| csharp | add | SQos | P-gen | arm64 | thru | 2.89 | Decimal128 (.NET 11) | 12.29 | **4.25×** | Rcs11 |  |
| csharp | add | NQss | P-gen | arm64 | thru | 6.32 | Decimal128 (.NET 11) | 13.43 | **2.12×** | Rcs11 |  |
| csharp | add | NQos | P-gen | arm64 | thru | 7.01 | Decimal128 (.NET 11) | 13.82 | **1.97×** | Rcs11 |  |
| csharp | add | MQss | P-gen | arm64 | thru | 10.68 | Decimal128 (.NET 11) | 14.93 | **1.40×** | Rcs11 |  |
| csharp | add | MQos | P-gen | arm64 | thru | 14.70 | Decimal128 (.NET 11) | 14.07 | **0.96×** | Rcs11 |  |
| csharp | add | OQss | P-gen | arm64 | thru | 17.25 | Decimal128 (.NET 11) | 98.49 | **5.71×** | Rcs11 |  |
| csharp | add | OQos | P-gen | arm64 | thru | 25.33 | Decimal128 (.NET 11) | 98.17 | **3.88×** | Rcs11 |  |
| csharp | add | FQss | P-gen | arm64 | thru | 10.38 | Decimal128 (.NET 11) | 727.85 | **70.12×** | Rcs11 |  |
| csharp | add | FQos | P-gen | arm64 | thru | 14.75 | Decimal128 (.NET 11) | 732.57 | **49.67×** | Rcs11 |  |

<!-- END GENERATED add-rel-csharp -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-csharp-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | add | SQss | P-gen | x86_64 | thru | 4.36 | System.Decimal | 9.48 | **2.17×** | xRcs11 | compact idiom peer |
| csharp | add | SQos | P-gen | x86_64 | thru | 17.08 | System.Decimal | 10.46 | **0.61×** | xRcs11 | compact idiom peer |
| csharp | add | NQss | P-gen | x86_64 | thru | 16.54 | System.Decimal | 14.36 | **0.87×** | xRcs11 | compact idiom peer |
| csharp | add | NQos | P-gen | x86_64 | thru | 22.69 | System.Decimal | 15.89 | **0.70×** | xRcs11 | compact idiom peer |
| csharp | add | MQss | P-gen | x86_64 | thru | 24.66 | System.Decimal | 12.17 | **0.49×** | xRcs11 | compact idiom peer |
| csharp | add | MQos | P-gen | x86_64 | thru | 41.85 | System.Decimal | 13.12 | **0.31×** | xRcs11 | compact idiom peer |
| csharp | add | SQss | P-gen | x86_64 | thru | 4.36 | Decimal128 (.NET 11) | 48.48 | **11.12×** | xRcs11 |  |
| csharp | add | SQos | P-gen | x86_64 | thru | 17.08 | Decimal128 (.NET 11) | 52.65 | **3.08×** | xRcs11 |  |
| csharp | add | NQss | P-gen | x86_64 | thru | 16.54 | Decimal128 (.NET 11) | 55.51 | **3.36×** | xRcs11 |  |
| csharp | add | NQos | P-gen | x86_64 | thru | 22.69 | Decimal128 (.NET 11) | 67.11 | **2.96×** | xRcs11 |  |
| csharp | add | MQss | P-gen | x86_64 | thru | 24.66 | Decimal128 (.NET 11) | 56.72 | **2.30×** | xRcs11 |  |
| csharp | add | MQos | P-gen | x86_64 | thru | 41.85 | Decimal128 (.NET 11) | 58.11 | **1.39×** | xRcs11 |  |
| csharp | add | OQss | P-gen | x86_64 | thru | 54.72 | Decimal128 (.NET 11) | 285.69 | **5.22×** | xRcs11 |  |
| csharp | add | OQos | P-gen | x86_64 | thru | 82.50 | Decimal128 (.NET 11) | 315.57 | **3.83×** | xRcs11 |  |
| csharp | add | FQss | P-gen | x86_64 | thru | 35.53 | Decimal128 (.NET 11) | 1866.16 | **52.52×** | xRcs11 |  |
| csharp | add | FQos | P-gen | x86_64 | thru | 51.96 | Decimal128 (.NET 11) | 1858.15 | **35.76×** | xRcs11 |  |

<!-- END GENERATED add-rel-csharp-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-csharp -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | sub | SQss | P-gen | arm64 | thru | 2.18 | System.Decimal | 2.47 | **1.13×** | Rcs11 | compact idiom peer |
| csharp | sub | SQos | P-gen | arm64 | thru | 1.52 | System.Decimal | 3.54 | **2.33×** | Rcs11 | compact idiom peer |
| csharp | sub | NQss | P-gen | arm64 | thru | 6.24 | System.Decimal | 3.73 | **0.60×** | Rcs11 | compact idiom peer |
| csharp | sub | NQos | P-gen | arm64 | thru | 5.06 | System.Decimal | 3.75 | **0.74×** | Rcs11 | compact idiom peer |
| csharp | sub | MQss | P-gen | arm64 | thru | 14.40 | System.Decimal | 3.79 | **0.26×** | Rcs11 | compact idiom peer |
| csharp | sub | MQos | P-gen | arm64 | thru | 8.56 | System.Decimal | 3.80 | **0.44×** | Rcs11 | compact idiom peer |
| csharp | sub | SQss | P-gen | arm64 | thru | 2.18 | Decimal128 (.NET 11) | 12.52 | **5.74×** | Rcs11 |  |
| csharp | sub | SQos | P-gen | arm64 | thru | 1.52 | Decimal128 (.NET 11) | 11.25 | **7.40×** | Rcs11 |  |
| csharp | sub | NQss | P-gen | arm64 | thru | 6.24 | Decimal128 (.NET 11) | 14.08 | **2.26×** | Rcs11 |  |
| csharp | sub | NQos | P-gen | arm64 | thru | 5.06 | Decimal128 (.NET 11) | 13.54 | **2.68×** | Rcs11 |  |
| csharp | sub | MQss | P-gen | arm64 | thru | 14.40 | Decimal128 (.NET 11) | 14.17 | **0.98×** | Rcs11 |  |
| csharp | sub | MQos | P-gen | arm64 | thru | 8.56 | Decimal128 (.NET 11) | 15.23 | **1.78×** | Rcs11 |  |
| csharp | sub | OQss | P-gen | arm64 | thru | 23.44 | Decimal128 (.NET 11) | 96.45 | **4.11×** | Rcs11 |  |
| csharp | sub | OQos | P-gen | arm64 | thru | 16.39 | Decimal128 (.NET 11) | 98.50 | **6.01×** | Rcs11 |  |
| csharp | sub | FQss | P-gen | arm64 | thru | 13.38 | Decimal128 (.NET 11) | 733.07 | **54.79×** | Rcs11 |  |
| csharp | sub | FQos | P-gen | arm64 | thru | 9.20 | Decimal128 (.NET 11) | 724.42 | **78.74×** | Rcs11 |  |

<!-- END GENERATED sub-rel-csharp -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-csharp-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | sub | SQss | P-gen | x86_64 | thru | 11.27 | System.Decimal | 11.25 | **1.00×** | xRcs11 | compact idiom peer |
| csharp | sub | SQos | P-gen | x86_64 | thru | 5.38 | System.Decimal | 9.24 | **1.72×** | xRcs11 | compact idiom peer |
| csharp | sub | NQss | P-gen | x86_64 | thru | 24.02 | System.Decimal | 15.77 | **0.66×** | xRcs11 | compact idiom peer |
| csharp | sub | NQos | P-gen | x86_64 | thru | 12.96 | System.Decimal | 12.04 | **0.93×** | xRcs11 | compact idiom peer |
| csharp | sub | MQss | P-gen | x86_64 | thru | 40.13 | System.Decimal | 16.20 | **0.40×** | xRcs11 | compact idiom peer |
| csharp | sub | MQos | P-gen | x86_64 | thru | 24.86 | System.Decimal | 13.28 | **0.53×** | xRcs11 | compact idiom peer |
| csharp | sub | SQss | P-gen | x86_64 | thru | 11.27 | Decimal128 (.NET 11) | 53.20 | **4.72×** | xRcs11 |  |
| csharp | sub | SQos | P-gen | x86_64 | thru | 5.38 | Decimal128 (.NET 11) | 49.11 | **9.13×** | xRcs11 |  |
| csharp | sub | NQss | P-gen | x86_64 | thru | 24.02 | Decimal128 (.NET 11) | 68.45 | **2.85×** | xRcs11 |  |
| csharp | sub | NQos | P-gen | x86_64 | thru | 12.96 | Decimal128 (.NET 11) | 57.55 | **4.44×** | xRcs11 |  |
| csharp | sub | MQss | P-gen | x86_64 | thru | 40.13 | Decimal128 (.NET 11) | 61.17 | **1.52×** | xRcs11 |  |
| csharp | sub | MQos | P-gen | x86_64 | thru | 24.86 | Decimal128 (.NET 11) | 65.67 | **2.64×** | xRcs11 |  |
| csharp | sub | OQss | P-gen | x86_64 | thru | 76.78 | Decimal128 (.NET 11) | 287.51 | **3.74×** | xRcs11 |  |
| csharp | sub | OQos | P-gen | x86_64 | thru | 52.25 | Decimal128 (.NET 11) | 314.72 | **6.02×** | xRcs11 |  |
| csharp | sub | FQss | P-gen | x86_64 | thru | 47.91 | Decimal128 (.NET 11) | 1900.18 | **39.66×** | xRcs11 |  |
| csharp | sub | FQos | P-gen | x86_64 | thru | 35.58 | Decimal128 (.NET 11) | 1892.73 | **53.20×** | xRcs11 |  |

<!-- END GENERATED sub-rel-csharp-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-csharp -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | mul | CP | P-gen | arm64 | thru | 2.19 | Decimal128 (.NET 11) | 8.97 | **4.10×** | Rcs11 |  |
| csharp | mul | WP | P-gen | arm64 | thru | 16.36 | Decimal128 (.NET 11) | 30.29 | **1.85×** | Rcs11 |  |
| csharp | mul | XP | P-gen | arm64 | thru | 45.33 | Decimal128 (.NET 11) | 730.70 | **16.12×** | Rcs11 |  |

<!-- END GENERATED mul-rel-csharp -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-csharp-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | mul | CP | P-gen | x86_64 | thru | 10.44 | Decimal128 (.NET 11) | 36.64 | **3.51×** | xRcs11 |  |
| csharp | mul | WP | P-gen | x86_64 | thru | 51.48 | Decimal128 (.NET 11) | 111.54 | **2.17×** | xRcs11 |  |
| csharp | mul | XP | P-gen | x86_64 | thru | 90.48 | Decimal128 (.NET 11) | 1812.05 | **20.03×** | xRcs11 |  |

<!-- END GENERATED mul-rel-csharp-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-csharp -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | div | CD | P-gen | arm64 | thru | 24.73 | Decimal128 (.NET 11) | 55.10 | **2.23×** | Rcs11 |  |
| csharp | div | WD | P-gen | arm64 | thru | 24.21 | Decimal128 (.NET 11) | 52.07 | **2.15×** | Rcs11 |  |
| csharp | div | XD | P-gen | arm64 | thru | 32.78 | Decimal128 (.NET 11) | 110.69 | **3.38×** | Rcs11 |  |
| csharp | div | ET | P-gen | arm64 | thru | 6.91 | Decimal128 (.NET 11) | 92.00 | **13.31×** | Rcs11 |  |
| csharp | div | PT | P-gen | arm64 | thru | 3.42 | Decimal128 (.NET 11) | 91.63 | **26.79×** | Rcs11 |  |

<!-- END GENERATED div-rel-csharp -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-csharp-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | div | CD | P-gen | x86_64 | thru | 104.45 | Decimal128 (.NET 11) | 214.73 | **2.06×** | xRcs11 |  |
| csharp | div | WD | P-gen | x86_64 | thru | 106.06 | Decimal128 (.NET 11) | 189.86 | **1.79×** | xRcs11 |  |
| csharp | div | XD | P-gen | x86_64 | thru | 125.26 | Decimal128 (.NET 11) | 317.10 | **2.53×** | xRcs11 |  |
| csharp | div | ET | P-gen | x86_64 | thru | 38.16 | Decimal128 (.NET 11) | 381.76 | **10.00×** | xRcs11 |  |
| csharp | div | PT | P-gen | x86_64 | thru | 11.77 | Decimal128 (.NET 11) | 385.40 | **32.74×** | xRcs11 |  |

<!-- END GENERATED div-rel-csharp-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-csharp -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | fma | FN | FMA | arm64 | thru | 75.31 | - | - | - | Rcs11 |  |
| csharp | fma | FF | FMA | arm64 | thru | 79.37 | - | - | - | Rcs11 |  |

<!-- END GENERATED fma-rel-csharp -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-csharp-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | fma | FN | FMA | x86_64 | thru | 222.38 | - | - | - | xRcs11 |  |
| csharp | fma | FF | FMA | x86_64 | thru | 159.26 | - | - | - | xRcs11 |  |

<!-- END GENERATED fma-rel-csharp-x86 -->

</div>
