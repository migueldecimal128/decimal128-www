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
| csharp | add | MIX | P-fin | arm64 | thru | 2.72 | System.Decimal | 2.79 | **1.03×** | Rcs11 | compact idiom peer |
| csharp | sub | MIX | P-fin | arm64 | thru | 3.26 | System.Decimal | 3.03 | **0.93×** | Rcs11 | compact idiom peer |
| csharp | div | CD | P-fin | arm64 | thru | 23.57 | System.Decimal | 11.30 | **0.48×** | Rcs11 | compact idiom peer |
| csharp | div | WD | P-fin | arm64 | thru | 32.48 | System.Decimal | 19.19 | **0.59×** | Rcs11 | compact idiom peer |
| csharp | div | ET | P-fin | arm64 | thru | 6.96 | System.Decimal | 5.01 | **0.72×** | Rcs11 | compact idiom peer |
| csharp | div | PT | P-fin | arm64 | thru | 5.15 | System.Decimal | 11.30 | **2.19×** | Rcs11 | compact idiom peer |
| csharp | add | MIX | P-fin | arm64 | thru | 2.72 | Decimal128 (.NET 11) | 9.67 | **3.56×** | Rcs11 |  |
| csharp | sub | MIX | P-fin | arm64 | thru | 3.26 | Decimal128 (.NET 11) | 10.30 | **3.16×** | Rcs11 |  |
| csharp | mul | CP | P-fin | arm64 | thru | 1.62 | Decimal128 (.NET 11) | 8.69 | **5.36×** | Rcs11 |  |
| csharp | mul | WP | P-fin | arm64 | thru | 17.44 | Decimal128 (.NET 11) | 31.13 | **1.78×** | Rcs11 |  |
| csharp | div | CD | P-fin | arm64 | thru | 23.57 | Decimal128 (.NET 11) | 60.35 | **2.56×** | Rcs11 |  |
| csharp | div | WD | P-fin | arm64 | thru | 32.48 | Decimal128 (.NET 11) | 50.50 | **1.55×** | Rcs11 |  |
| csharp | div | ET | P-fin | arm64 | thru | 6.96 | Decimal128 (.NET 11) | 103.42 | **14.86×** | Rcs11 |  |
| csharp | div | PT | P-fin | arm64 | thru | 5.15 | Decimal128 (.NET 11) | 105.00 | **20.39×** | Rcs11 |  |

<!-- END GENERATED pfin-rel-csharp -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-csharp-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | add | MIX | P-fin | x86_64 | thru | 8.62 | System.Decimal | 8.73 | **1.01×** | xRcs11a | compact idiom peer |
| csharp | sub | MIX | P-fin | x86_64 | thru | 12.63 | System.Decimal | 10.09 | **0.80×** | xRcs11 | compact idiom peer |
| csharp | div | CD | P-fin | x86_64 | thru | 87.22 | System.Decimal | 53.38 | **0.61×** | xRcs11 | compact idiom peer |
| csharp | div | WD | P-fin | x86_64 | thru | 94.93 | System.Decimal | 95.33 | **1.00×** | xRcs11 | compact idiom peer |
| csharp | div | ET | P-fin | x86_64 | thru | 23.19 | System.Decimal | 13.84 | **0.60×** | xRcs11 | compact idiom peer |
| csharp | div | PT | P-fin | x86_64 | thru | 12.36 | System.Decimal | 58.43 | **4.73×** | xRcs11 | compact idiom peer |
| csharp | add | MIX | P-fin | x86_64 | thru | 8.62 | Decimal128 (.NET 11) | 23.51 | **2.73×** | xRcs11a |  |
| csharp | sub | MIX | P-fin | x86_64 | thru | 12.63 | Decimal128 (.NET 11) | 27.17 | **2.15×** | xRcs11 |  |
| csharp | mul | CP | P-fin | x86_64 | thru | 4.82 | Decimal128 (.NET 11) | 34.18 | **7.09×** | xRcs11 |  |
| csharp | mul | WP | P-fin | x86_64 | thru | 40.40 | Decimal128 (.NET 11) | 98.75 | **2.44×** | xRcs11 |  |
| csharp | div | CD | P-fin | x86_64 | thru | 87.22 | Decimal128 (.NET 11) | 198.67 | **2.28×** | xRcs11 |  |
| csharp | div | WD | P-fin | x86_64 | thru | 94.93 | Decimal128 (.NET 11) | 161.47 | **1.70×** | xRcs11 |  |
| csharp | div | ET | P-fin | x86_64 | thru | 23.19 | Decimal128 (.NET 11) | 387.07 | **16.69×** | xRcs11 |  |
| csharp | div | PT | P-fin | x86_64 | thru | 12.36 | Decimal128 (.NET 11) | 405.51 | **32.81×** | xRcs11 |  |

<!-- END GENERATED pfin-rel-csharp-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-csharp -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | add | SQss | P-gen | arm64 | thru | 1.41 | System.Decimal | 2.84 | **2.01×** | Rcs11 | compact idiom peer |
| csharp | add | SQos | P-gen | arm64 | thru | 3.40 | System.Decimal | 2.88 | **0.85×** | Rcs11 | compact idiom peer |
| csharp | add | NQss | P-gen | arm64 | thru | 7.04 | System.Decimal | 3.72 | **0.53×** | Rcs11 | compact idiom peer |
| csharp | add | NQos | P-gen | arm64 | thru | 7.02 | System.Decimal | 3.84 | **0.55×** | Rcs11 | compact idiom peer |
| csharp | add | MQss | P-gen | arm64 | thru | 8.68 | System.Decimal | 3.70 | **0.43×** | Rcs11 | compact idiom peer |
| csharp | add | MQos | P-gen | arm64 | thru | 25.44 | System.Decimal | 3.78 | **0.15×** | Rcs11 | compact idiom peer |
| csharp | add | SQss | P-gen | arm64 | thru | 1.41 | Decimal128 (.NET 11) | 11.93 | **8.46×** | Rcs11 |  |
| csharp | add | SQos | P-gen | arm64 | thru | 3.40 | Decimal128 (.NET 11) | 12.68 | **3.73×** | Rcs11 |  |
| csharp | add | NQss | P-gen | arm64 | thru | 7.04 | Decimal128 (.NET 11) | 14.36 | **2.04×** | Rcs11 |  |
| csharp | add | NQos | P-gen | arm64 | thru | 7.02 | Decimal128 (.NET 11) | 14.91 | **2.12×** | Rcs11 |  |
| csharp | add | MQss | P-gen | arm64 | thru | 8.68 | Decimal128 (.NET 11) | 15.85 | **1.83×** | Rcs11 |  |
| csharp | add | MQos | P-gen | arm64 | thru | 25.44 | Decimal128 (.NET 11) | 15.11 | **0.59×** | Rcs11 |  |
| csharp | add | OQss | P-gen | arm64 | thru | 17.29 | Decimal128 (.NET 11) | 99.34 | **5.75×** | Rcs11 |  |
| csharp | add | OQos | P-gen | arm64 | thru | 33.77 | Decimal128 (.NET 11) | 99.39 | **2.94×** | Rcs11 |  |
| csharp | add | FQss | P-gen | arm64 | thru | 13.06 | Decimal128 (.NET 11) | 724.49 | **55.47×** | Rcs11 |  |
| csharp | add | FQos | P-gen | arm64 | thru | 15.90 | Decimal128 (.NET 11) | 765.70 | **48.16×** | Rcs11 |  |

<!-- END GENERATED add-rel-csharp -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-csharp-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | add | SQss | P-gen | x86_64 | thru | 3.61 | System.Decimal | 7.42 | **2.06×** | xRcs11a | compact idiom peer |
| csharp | add | SQos | P-gen | x86_64 | thru | 11.00 | System.Decimal | 10.09 | **0.92×** | xRcs11a | compact idiom peer |
| csharp | add | NQss | P-gen | x86_64 | thru | 14.73 | System.Decimal | 11.55 | **0.78×** | xRcs11a | compact idiom peer |
| csharp | add | NQos | P-gen | x86_64 | thru | 21.06 | System.Decimal | 13.21 | **0.63×** | xRcs11a | compact idiom peer |
| csharp | add | MQss | P-gen | x86_64 | thru | 19.62 | System.Decimal | 11.04 | **0.56×** | xRcs11a | compact idiom peer |
| csharp | add | MQos | P-gen | x86_64 | thru | 44.01 | System.Decimal | 12.55 | **0.29×** | xRcs11a | compact idiom peer |
| csharp | add | SQss | P-gen | x86_64 | thru | 3.61 | Decimal128 (.NET 11) | 45.51 | **12.61×** | xRcs11a |  |
| csharp | add | SQos | P-gen | x86_64 | thru | 11.00 | Decimal128 (.NET 11) | 57.00 | **5.18×** | xRcs11a |  |
| csharp | add | NQss | P-gen | x86_64 | thru | 14.73 | Decimal128 (.NET 11) | 51.06 | **3.47×** | xRcs11a |  |
| csharp | add | NQos | P-gen | x86_64 | thru | 21.06 | Decimal128 (.NET 11) | 55.58 | **2.64×** | xRcs11a |  |
| csharp | add | MQss | P-gen | x86_64 | thru | 19.62 | Decimal128 (.NET 11) | 52.94 | **2.70×** | xRcs11a |  |
| csharp | add | MQos | P-gen | x86_64 | thru | 44.01 | Decimal128 (.NET 11) | 56.15 | **1.28×** | xRcs11a |  |
| csharp | add | OQss | P-gen | x86_64 | thru | 46.94 | Decimal128 (.NET 11) | 264.80 | **5.64×** | xRcs11a |  |
| csharp | add | OQos | P-gen | x86_64 | thru | 75.53 | Decimal128 (.NET 11) | 265.03 | **3.51×** | xRcs11a |  |
| csharp | add | FQss | P-gen | x86_64 | thru | 36.19 | Decimal128 (.NET 11) | 1720.58 | **47.54×** | xRcs11a |  |
| csharp | add | FQos | P-gen | x86_64 | thru | 43.83 | Decimal128 (.NET 11) | 1726.56 | **39.39×** | xRcs11a |  |

<!-- END GENERATED add-rel-csharp-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-csharp -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | sub | SQss | P-gen | arm64 | thru | 2.29 | System.Decimal | 2.36 | **1.03×** | Rcs11 | compact idiom peer |
| csharp | sub | SQos | P-gen | arm64 | thru | 1.52 | System.Decimal | 3.54 | **2.33×** | Rcs11 | compact idiom peer |
| csharp | sub | NQss | P-gen | arm64 | thru | 6.37 | System.Decimal | 3.85 | **0.60×** | Rcs11 | compact idiom peer |
| csharp | sub | NQos | P-gen | arm64 | thru | 5.61 | System.Decimal | 3.76 | **0.67×** | Rcs11 | compact idiom peer |
| csharp | sub | MQss | P-gen | arm64 | thru | 15.91 | System.Decimal | 3.77 | **0.24×** | Rcs11 | compact idiom peer |
| csharp | sub | MQos | P-gen | arm64 | thru | 8.68 | System.Decimal | 3.79 | **0.44×** | Rcs11 | compact idiom peer |
| csharp | sub | SQss | P-gen | arm64 | thru | 2.29 | Decimal128 (.NET 11) | 12.93 | **5.65×** | Rcs11 |  |
| csharp | sub | SQos | P-gen | arm64 | thru | 1.52 | Decimal128 (.NET 11) | 11.97 | **7.88×** | Rcs11 |  |
| csharp | sub | NQss | P-gen | arm64 | thru | 6.37 | Decimal128 (.NET 11) | 14.61 | **2.29×** | Rcs11 |  |
| csharp | sub | NQos | P-gen | arm64 | thru | 5.61 | Decimal128 (.NET 11) | 14.24 | **2.54×** | Rcs11 |  |
| csharp | sub | MQss | P-gen | arm64 | thru | 15.91 | Decimal128 (.NET 11) | 14.88 | **0.94×** | Rcs11 |  |
| csharp | sub | MQos | P-gen | arm64 | thru | 8.68 | Decimal128 (.NET 11) | 15.70 | **1.81×** | Rcs11 |  |
| csharp | sub | OQss | P-gen | arm64 | thru | 31.44 | Decimal128 (.NET 11) | 99.83 | **3.18×** | Rcs11 |  |
| csharp | sub | OQos | P-gen | arm64 | thru | 16.25 | Decimal128 (.NET 11) | 98.54 | **6.06×** | Rcs11 |  |
| csharp | sub | FQss | P-gen | arm64 | thru | 14.63 | Decimal128 (.NET 11) | 735.35 | **50.26×** | Rcs11 |  |
| csharp | sub | FQos | P-gen | arm64 | thru | 12.14 | Decimal128 (.NET 11) | 724.71 | **59.70×** | Rcs11 |  |

<!-- END GENERATED sub-rel-csharp -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-csharp-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | sub | SQss | P-gen | x86_64 | thru | 9.87 | System.Decimal | 9.60 | **0.97×** | xRcs11 | compact idiom peer |
| csharp | sub | SQos | P-gen | x86_64 | thru | 4.52 | System.Decimal | 7.07 | **1.56×** | xRcs11 | compact idiom peer |
| csharp | sub | NQss | P-gen | x86_64 | thru | 18.19 | System.Decimal | 13.53 | **0.74×** | xRcs11 | compact idiom peer |
| csharp | sub | NQos | P-gen | x86_64 | thru | 11.43 | System.Decimal | 12.44 | **1.09×** | xRcs11 | compact idiom peer |
| csharp | sub | MQss | P-gen | x86_64 | thru | 42.52 | System.Decimal | 12.39 | **0.29×** | xRcs11 | compact idiom peer |
| csharp | sub | MQos | P-gen | x86_64 | thru | 21.06 | System.Decimal | 10.84 | **0.51×** | xRcs11 | compact idiom peer |
| csharp | sub | SQss | P-gen | x86_64 | thru | 9.87 | Decimal128 (.NET 11) | 49.93 | **5.06×** | xRcs11 |  |
| csharp | sub | SQos | P-gen | x86_64 | thru | 4.52 | Decimal128 (.NET 11) | 45.39 | **10.04×** | xRcs11 |  |
| csharp | sub | NQss | P-gen | x86_64 | thru | 18.19 | Decimal128 (.NET 11) | 56.03 | **3.08×** | xRcs11 |  |
| csharp | sub | NQos | P-gen | x86_64 | thru | 11.43 | Decimal128 (.NET 11) | 52.06 | **4.55×** | xRcs11 |  |
| csharp | sub | MQss | P-gen | x86_64 | thru | 42.52 | Decimal128 (.NET 11) | 57.68 | **1.36×** | xRcs11 |  |
| csharp | sub | MQos | P-gen | x86_64 | thru | 21.06 | Decimal128 (.NET 11) | 54.67 | **2.60×** | xRcs11 |  |
| csharp | sub | OQss | P-gen | x86_64 | thru | 77.01 | Decimal128 (.NET 11) | 265.54 | **3.45×** | xRcs11 |  |
| csharp | sub | OQos | P-gen | x86_64 | thru | 44.27 | Decimal128 (.NET 11) | 266.68 | **6.02×** | xRcs11 |  |
| csharp | sub | FQss | P-gen | x86_64 | thru | 41.50 | Decimal128 (.NET 11) | 1706.63 | **41.12×** | xRcs11 |  |
| csharp | sub | FQos | P-gen | x86_64 | thru | 35.68 | Decimal128 (.NET 11) | 1722.73 | **48.28×** | xRcs11 |  |

<!-- END GENERATED sub-rel-csharp-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-csharp -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | mul | CP | P-gen | arm64 | thru | 2.07 | Decimal128 (.NET 11) | 9.17 | **4.43×** | Rcs11 |  |
| csharp | mul | WP | P-gen | arm64 | thru | 16.46 | Decimal128 (.NET 11) | 29.79 | **1.81×** | Rcs11 |  |
| csharp | mul | XP | P-gen | arm64 | thru | 43.54 | Decimal128 (.NET 11) | 742.39 | **17.05×** | Rcs11 |  |

<!-- END GENERATED mul-rel-csharp -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-csharp-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | mul | CP | P-gen | x86_64 | thru | 7.59 | Decimal128 (.NET 11) | 36.21 | **4.77×** | xRcs11 |  |
| csharp | mul | WP | P-gen | x86_64 | thru | 43.06 | Decimal128 (.NET 11) | 101.35 | **2.35×** | xRcs11 |  |
| csharp | mul | XP | P-gen | x86_64 | thru | 77.48 | Decimal128 (.NET 11) | 1654.32 | **21.35×** | xRcs11 |  |

<!-- END GENERATED mul-rel-csharp-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-csharp -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | div | CD | P-gen | arm64 | thru | 28.67 | Decimal128 (.NET 11) | 56.63 | **1.98×** | Rcs11 |  |
| csharp | div | WD | P-gen | arm64 | thru | 31.31 | Decimal128 (.NET 11) | 52.06 | **1.66×** | Rcs11 |  |
| csharp | div | XD | P-gen | arm64 | thru | 35.54 | Decimal128 (.NET 11) | 109.37 | **3.08×** | Rcs11 |  |
| csharp | div | ET | P-gen | arm64 | thru | 13.16 | Decimal128 (.NET 11) | 96.04 | **7.30×** | Rcs11 |  |
| csharp | div | PT | P-gen | arm64 | thru | 5.05 | Decimal128 (.NET 11) | 91.45 | **18.11×** | Rcs11 |  |

<!-- END GENERATED div-rel-csharp -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-csharp-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | div | CD | P-gen | x86_64 | thru | 93.04 | Decimal128 (.NET 11) | 198.46 | **2.13×** | xRcs11 |  |
| csharp | div | WD | P-gen | x86_64 | thru | 97.29 | Decimal128 (.NET 11) | 171.65 | **1.76×** | xRcs11 |  |
| csharp | div | XD | P-gen | x86_64 | thru | 105.37 | Decimal128 (.NET 11) | 293.82 | **2.79×** | xRcs11 |  |
| csharp | div | ET | P-gen | x86_64 | thru | 32.85 | Decimal128 (.NET 11) | 352.22 | **10.72×** | xRcs11 |  |
| csharp | div | PT | P-gen | x86_64 | thru | 10.58 | Decimal128 (.NET 11) | 347.94 | **32.89×** | xRcs11 |  |

<!-- END GENERATED div-rel-csharp-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-csharp -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | fma | FN | FMA | arm64 | thru | 103.37 | - | - | - | Rcs11 |  |
| csharp | fma | FF | FMA | arm64 | thru | 76.63 | - | - | - | Rcs11 |  |

<!-- END GENERATED fma-rel-csharp -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-csharp-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | fma | FN | FMA | x86_64 | thru | 186.16 | - | - | - | xRcs11 |  |
| csharp | fma | FF | FMA | x86_64 | thru | 130.74 | - | - | - | xRcs11 |  |

<!-- END GENERATED fma-rel-csharp-x86 -->

</div>
