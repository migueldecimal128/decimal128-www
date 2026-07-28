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
| csharp | add | MIX | P-fin | arm64 | thru | 2.70 | System.Decimal | 2.80 | **1.04×** | Rcs11 | compact idiom peer |
| csharp | sub | MIX | P-fin | arm64 | thru | 3.49 | System.Decimal | 2.95 | **0.85×** | Rcs11 | compact idiom peer |
| csharp | div | CD | P-fin | arm64 | thru | 24.10 | System.Decimal | 11.66 | **0.48×** | Rcs11 | compact idiom peer |
| csharp | div | WD | P-fin | arm64 | thru | 44.72 | System.Decimal | 27.96 | **0.63×** | Rcs11 | compact idiom peer |
| csharp | div | ET | P-fin | arm64 | thru | 9.08 | System.Decimal | 5.01 | **0.55×** | Rcs11 | compact idiom peer |
| csharp | div | PT | P-fin | arm64 | thru | 4.61 | System.Decimal | 12.16 | **2.64×** | Rcs11 | compact idiom peer |
| csharp | add | MIX | P-fin | arm64 | thru | 2.70 | Decimal128 (.NET 11) | 9.63 | **3.57×** | Rcs11 |  |
| csharp | sub | MIX | P-fin | arm64 | thru | 3.49 | Decimal128 (.NET 11) | 10.38 | **2.97×** | Rcs11 |  |
| csharp | mul | CP | P-fin | arm64 | thru | 1.70 | Decimal128 (.NET 11) | 9.70 | **5.71×** | Rcs11 |  |
| csharp | mul | WP | P-fin | arm64 | thru | 23.64 | Decimal128 (.NET 11) | 28.44 | **1.20×** | Rcs11 |  |
| csharp | div | CD | P-fin | arm64 | thru | 24.10 | Decimal128 (.NET 11) | 77.69 | **3.22×** | Rcs11 |  |
| csharp | div | WD | P-fin | arm64 | thru | 44.72 | Decimal128 (.NET 11) | 59.12 | **1.32×** | Rcs11 |  |
| csharp | div | ET | P-fin | arm64 | thru | 9.08 | Decimal128 (.NET 11) | 160.34 | **17.66×** | Rcs11 |  |
| csharp | div | PT | P-fin | arm64 | thru | 4.61 | Decimal128 (.NET 11) | 166.05 | **36.02×** | Rcs11 |  |

<!-- END GENERATED pfin-rel-csharp -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-csharp-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | add | MIX | P-fin | x86_64 | thru | 8.59 | System.Decimal | 8.83 | **1.03×** | xRcs11 | compact idiom peer |
| csharp | sub | MIX | P-fin | x86_64 | thru | 12.80 | System.Decimal | 10.44 | **0.82×** | xRcs11 | compact idiom peer |
| csharp | div | CD | P-fin | x86_64 | thru | 83.96 | System.Decimal | 52.63 | **0.63×** | xRcs11 | compact idiom peer |
| csharp | div | WD | P-fin | x86_64 | thru | 108.30 | System.Decimal | 99.60 | **0.92×** | xRcs11 | compact idiom peer |
| csharp | div | ET | P-fin | x86_64 | thru | 23.88 | System.Decimal | 15.94 | **0.67×** | xRcs11 | compact idiom peer |
| csharp | div | PT | P-fin | x86_64 | thru | 11.06 | System.Decimal | 58.55 | **5.29×** | xRcs11 | compact idiom peer |
| csharp | add | MIX | P-fin | x86_64 | thru | 8.59 | Decimal128 (.NET 11) | 23.58 | **2.75×** | xRcs11 |  |
| csharp | sub | MIX | P-fin | x86_64 | thru | 12.80 | Decimal128 (.NET 11) | 27.95 | **2.18×** | xRcs11 |  |
| csharp | mul | CP | P-fin | x86_64 | thru | 5.29 | Decimal128 (.NET 11) | 35.11 | **6.64×** | xRcs11 |  |
| csharp | mul | WP | P-fin | x86_64 | thru | 47.09 | Decimal128 (.NET 11) | 97.07 | **2.06×** | xRcs11 |  |
| csharp | div | CD | P-fin | x86_64 | thru | 83.96 | Decimal128 (.NET 11) | 194.07 | **2.31×** | xRcs11 |  |
| csharp | div | WD | P-fin | x86_64 | thru | 108.30 | Decimal128 (.NET 11) | 159.85 | **1.48×** | xRcs11 |  |
| csharp | div | ET | P-fin | x86_64 | thru | 23.88 | Decimal128 (.NET 11) | 377.61 | **15.81×** | xRcs11 |  |
| csharp | div | PT | P-fin | x86_64 | thru | 11.06 | Decimal128 (.NET 11) | 390.20 | **35.28×** | xRcs11 |  |

<!-- END GENERATED pfin-rel-csharp-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-csharp -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | add | SQ | P-gen | arm64 | thru | 10.69 | System.Decimal | 2.49 | **0.23×** | Rcs11 | compact idiom peer |
| csharp | add | NQ | P-gen | arm64 | thru | 5.46 | System.Decimal | 4.06 | **0.74×** | Rcs11 | compact idiom peer |
| csharp | add | MQ | P-gen | arm64 | thru | 15.70 | System.Decimal | 3.93 | **0.25×** | Rcs11 | compact idiom peer |
| csharp | add | SQ | P-gen | arm64 | thru | 10.69 | Decimal128 (.NET 11) | 13.32 | **1.25×** | Rcs11 |  |
| csharp | add | NQ | P-gen | arm64 | thru | 5.46 | Decimal128 (.NET 11) | 14.55 | **2.66×** | Rcs11 |  |
| csharp | add | MQ | P-gen | arm64 | thru | 15.70 | Decimal128 (.NET 11) | 14.45 | **0.92×** | Rcs11 |  |
| csharp | add | OQ | P-gen | arm64 | thru | 40.82 | Decimal128 (.NET 11) | 98.19 | **2.41×** | Rcs11 |  |
| csharp | add | FQ | P-gen | arm64 | thru | 32.79 | Decimal128 (.NET 11) | 804.95 | **24.55×** | Rcs11 |  |

<!-- END GENERATED add-rel-csharp -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-csharp-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | add | SQ | P-gen | x86_64 | thru | 22.69 | System.Decimal | 11.31 | **0.50×** | xRcs11 | compact idiom peer |
| csharp | add | NQ | P-gen | x86_64 | thru | 17.79 | System.Decimal | 15.62 | **0.88×** | xRcs11 | compact idiom peer |
| csharp | add | MQ | P-gen | x86_64 | thru | 43.75 | System.Decimal | 16.99 | **0.39×** | xRcs11 | compact idiom peer |
| csharp | add | SQ | P-gen | x86_64 | thru | 22.69 | Decimal128 (.NET 11) | 51.73 | **2.28×** | xRcs11 |  |
| csharp | add | NQ | P-gen | x86_64 | thru | 17.79 | Decimal128 (.NET 11) | 57.04 | **3.21×** | xRcs11 |  |
| csharp | add | MQ | P-gen | x86_64 | thru | 43.75 | Decimal128 (.NET 11) | 57.05 | **1.30×** | xRcs11 |  |
| csharp | add | OQ | P-gen | x86_64 | thru | 82.48 | Decimal128 (.NET 11) | 329.80 | **4.00×** | xRcs11 |  |
| csharp | add | FQ | P-gen | x86_64 | thru | 62.87 | Decimal128 (.NET 11) | 2310.54 | **36.75×** | xRcs11 |  |

<!-- END GENERATED add-rel-csharp-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-csharp -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | sub | SQ | P-gen | arm64 | thru | 9.04 | System.Decimal | 2.51 | **0.28×** | Rcs11 | compact idiom peer |
| csharp | sub | NQ | P-gen | arm64 | thru | 6.20 | System.Decimal | 4.11 | **0.66×** | Rcs11 | compact idiom peer |
| csharp | sub | MQ | P-gen | arm64 | thru | 14.29 | System.Decimal | 4.01 | **0.28×** | Rcs11 | compact idiom peer |
| csharp | sub | SQ | P-gen | arm64 | thru | 9.04 | Decimal128 (.NET 11) | 13.31 | **1.47×** | Rcs11 |  |
| csharp | sub | NQ | P-gen | arm64 | thru | 6.20 | Decimal128 (.NET 11) | 14.29 | **2.30×** | Rcs11 |  |
| csharp | sub | MQ | P-gen | arm64 | thru | 14.29 | Decimal128 (.NET 11) | 14.33 | **1.00×** | Rcs11 |  |
| csharp | sub | OQ | P-gen | arm64 | thru | 40.04 | Decimal128 (.NET 11) | 95.25 | **2.38×** | Rcs11 |  |
| csharp | sub | FQ | P-gen | arm64 | thru | 32.96 | Decimal128 (.NET 11) | 806.63 | **24.47×** | Rcs11 |  |

<!-- END GENERATED sub-rel-csharp -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-csharp-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | sub | SQ | P-gen | x86_64 | thru | 18.69 | System.Decimal | 11.73 | **0.63×** | xRcs11 | compact idiom peer |
| csharp | sub | NQ | P-gen | x86_64 | thru | 17.16 | System.Decimal | 15.68 | **0.91×** | xRcs11 | compact idiom peer |
| csharp | sub | MQ | P-gen | x86_64 | thru | 40.45 | System.Decimal | 15.30 | **0.38×** | xRcs11 | compact idiom peer |
| csharp | sub | SQ | P-gen | x86_64 | thru | 18.69 | Decimal128 (.NET 11) | 52.33 | **2.80×** | xRcs11 |  |
| csharp | sub | NQ | P-gen | x86_64 | thru | 17.16 | Decimal128 (.NET 11) | 57.19 | **3.33×** | xRcs11 |  |
| csharp | sub | MQ | P-gen | x86_64 | thru | 40.45 | Decimal128 (.NET 11) | 57.79 | **1.43×** | xRcs11 |  |
| csharp | sub | OQ | P-gen | x86_64 | thru | 82.35 | Decimal128 (.NET 11) | 303.11 | **3.68×** | xRcs11 |  |
| csharp | sub | FQ | P-gen | x86_64 | thru | 63.06 | Decimal128 (.NET 11) | 2294.36 | **36.38×** | xRcs11 |  |

<!-- END GENERATED sub-rel-csharp-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-csharp -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | mul | CP | P-gen | arm64 | thru | 2.15 | Decimal128 (.NET 11) | 9.22 | **4.29×** | Rcs11 |  |
| csharp | mul | WP | P-gen | arm64 | thru | 22.26 | Decimal128 (.NET 11) | 31.85 | **1.43×** | Rcs11 |  |
| csharp | mul | XP | P-gen | arm64 | thru | 49.19 | Decimal128 (.NET 11) | 805.25 | **16.37×** | Rcs11 |  |

<!-- END GENERATED mul-rel-csharp -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-csharp-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | mul | CP | P-gen | x86_64 | thru | 7.47 | Decimal128 (.NET 11) | 34.23 | **4.58×** | xRcs11 |  |
| csharp | mul | WP | P-gen | x86_64 | thru | 49.13 | Decimal128 (.NET 11) | 101.26 | **2.06×** | xRcs11 |  |
| csharp | mul | XP | P-gen | x86_64 | thru | 83.41 | Decimal128 (.NET 11) | 2220.68 | **26.62×** | xRcs11 |  |

<!-- END GENERATED mul-rel-csharp-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-csharp -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | div | CD | P-gen | arm64 | thru | 27.18 | Decimal128 (.NET 11) | 76.87 | **2.83×** | Rcs11 |  |
| csharp | div | WD | P-gen | arm64 | thru | 42.85 | Decimal128 (.NET 11) | 67.95 | **1.59×** | Rcs11 |  |
| csharp | div | XD | P-gen | arm64 | thru | 49.00 | Decimal128 (.NET 11) | 118.33 | **2.41×** | Rcs11 |  |
| csharp | div | ET | P-gen | arm64 | thru | 9.61 | Decimal128 (.NET 11) | 143.12 | **14.89×** | Rcs11 |  |
| csharp | div | PT | P-gen | arm64 | thru | 4.67 | Decimal128 (.NET 11) | 142.50 | **30.51×** | Rcs11 |  |

<!-- END GENERATED div-rel-csharp -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-csharp-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | div | CD | P-gen | x86_64 | thru | 86.87 | Decimal128 (.NET 11) | 226.16 | **2.60×** | xRcs11 |  |
| csharp | div | WD | P-gen | x86_64 | thru | 110.27 | Decimal128 (.NET 11) | 177.83 | **1.61×** | xRcs11 |  |
| csharp | div | XD | P-gen | x86_64 | thru | 114.46 | Decimal128 (.NET 11) | 296.64 | **2.59×** | xRcs11 |  |
| csharp | div | ET | P-gen | x86_64 | thru | 34.92 | Decimal128 (.NET 11) | 470.04 | **13.46×** | xRcs11 |  |
| csharp | div | PT | P-gen | x86_64 | thru | 11.20 | Decimal128 (.NET 11) | 459.91 | **41.06×** | xRcs11 |  |

<!-- END GENERATED div-rel-csharp-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-csharp -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | fma | FN | FMA | arm64 | thru | 102.36 | - | - | - | Rcs11 |  |
| csharp | fma | FF | FMA | arm64 | thru | 82.87 | - | - | - | Rcs11 |  |

<!-- END GENERATED fma-rel-csharp -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-csharp-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | fma | FN | FMA | x86_64 | thru | 188.24 | - | - | - | xRcs11 |  |
| csharp | fma | FF | FMA | x86_64 | thru | 143.50 | - | - | - | xRcs11 |  |

<!-- END GENERATED fma-rel-csharp-x86 -->

</div>
