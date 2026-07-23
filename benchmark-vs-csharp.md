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
| csharp | add | MIX | P-fin | arm64 | thru | 3.98 | System.Decimal | 2.96 | **0.74×** | Rcs11 | compact idiom peer |
| csharp | sub | MIX | P-fin | arm64 | thru | 3.11 | System.Decimal | 2.96 | **0.95×** | Rcs11 | compact idiom peer |
| csharp | div | CD | P-fin | arm64 | thru | 26.08 | System.Decimal | 11.16 | **0.43×** | Rcs11 | compact idiom peer |
| csharp | div | WD | P-fin | arm64 | thru | 45.99 | System.Decimal | 27.22 | **0.59×** | Rcs11 | compact idiom peer |
| csharp | div | ET | P-fin | arm64 | thru | 14.15 | System.Decimal | 5.16 | **0.36×** | Rcs11 | compact idiom peer |
| csharp | div | PT | P-fin | arm64 | thru | 5.22 | System.Decimal | 12.34 | **2.36×** | Rcs11 | compact idiom peer |
| csharp | add | MIX | P-fin | arm64 | thru | 3.98 | Decimal128 (.NET 11) | 16.44 | **4.13×** | Rcs11 |  |
| csharp | sub | MIX | P-fin | arm64 | thru | 3.11 | Decimal128 (.NET 11) | 15.49 | **4.98×** | Rcs11 |  |
| csharp | mul | CP | P-fin | arm64 | thru | 1.87 | Decimal128 (.NET 11) | 11.01 | **5.89×** | Rcs11 |  |
| csharp | mul | WP | P-fin | arm64 | thru | 23.86 | Decimal128 (.NET 11) | 51.33 | **2.15×** | Rcs11 |  |
| csharp | div | CD | P-fin | arm64 | thru | 26.08 | Decimal128 (.NET 11) | 151.29 | **5.80×** | Rcs11 |  |
| csharp | div | WD | P-fin | arm64 | thru | 45.99 | Decimal128 (.NET 11) | 188.46 | **4.10×** | Rcs11 |  |
| csharp | div | ET | P-fin | arm64 | thru | 14.15 | Decimal128 (.NET 11) | 235.56 | **16.65×** | Rcs11 |  |
| csharp | div | PT | P-fin | arm64 | thru | 5.22 | Decimal128 (.NET 11) | 240.20 | **46.02×** | Rcs11 |  |

<!-- END GENERATED pfin-rel-csharp -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-csharp-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | add | MIX | P-fin | x86_64 | thru | 17.85 | System.Decimal | 15.99 | **0.90×** | xRcs11 | compact idiom peer |
| csharp | sub | MIX | P-fin | x86_64 | thru | 15.06 | System.Decimal | 15.71 | **1.04×** | xRcs11 | compact idiom peer |
| csharp | div | CD | P-fin | x86_64 | thru | 109.87 | System.Decimal | 61.56 | **0.56×** | xRcs11 | compact idiom peer |
| csharp | div | WD | P-fin | x86_64 | thru | 124.96 | System.Decimal | 111.77 | **0.89×** | xRcs11 | compact idiom peer |
| csharp | div | ET | P-fin | x86_64 | thru | 28.79 | System.Decimal | 16.06 | **0.56×** | xRcs11 | compact idiom peer |
| csharp | div | PT | P-fin | x86_64 | thru | 11.77 | System.Decimal | 67.56 | **5.74×** | xRcs11 | compact idiom peer |
| csharp | add | MIX | P-fin | x86_64 | thru | 17.85 | Decimal128 (.NET 11) | 47.17 | **2.64×** | xRcs11 |  |
| csharp | sub | MIX | P-fin | x86_64 | thru | 15.06 | Decimal128 (.NET 11) | 47.96 | **3.18×** | xRcs11 |  |
| csharp | mul | CP | P-fin | x86_64 | thru | 5.34 | Decimal128 (.NET 11) | 43.43 | **8.13×** | xRcs11 |  |
| csharp | mul | WP | P-fin | x86_64 | thru | 55.80 | Decimal128 (.NET 11) | 137.73 | **2.47×** | xRcs11 |  |
| csharp | div | CD | P-fin | x86_64 | thru | 109.87 | Decimal128 (.NET 11) | 439.54 | **4.00×** | xRcs11 |  |
| csharp | div | WD | P-fin | x86_64 | thru | 124.96 | Decimal128 (.NET 11) | 488.51 | **3.91×** | xRcs11 |  |
| csharp | div | ET | P-fin | x86_64 | thru | 28.79 | Decimal128 (.NET 11) | 621.48 | **21.59×** | xRcs11 |  |
| csharp | div | PT | P-fin | x86_64 | thru | 11.77 | Decimal128 (.NET 11) | 636.05 | **54.04×** | xRcs11 |  |

<!-- END GENERATED pfin-rel-csharp-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-csharp -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | add | SQ | P-gen | arm64 | thru | 5.97 | System.Decimal | 2.49 | **0.42×** | Rcs11 | compact idiom peer |
| csharp | add | NQ | P-gen | arm64 | thru | 4.92 | System.Decimal | 4.11 | **0.84×** | Rcs11 | compact idiom peer |
| csharp | add | MQ | P-gen | arm64 | thru | 15.76 | System.Decimal | 4.18 | **0.27×** | Rcs11 | compact idiom peer |
| csharp | add | SQ | P-gen | arm64 | thru | 5.97 | Decimal128 (.NET 11) | 19.35 | **3.24×** | Rcs11 |  |
| csharp | add | NQ | P-gen | arm64 | thru | 4.92 | Decimal128 (.NET 11) | 19.49 | **3.96×** | Rcs11 |  |
| csharp | add | MQ | P-gen | arm64 | thru | 15.76 | Decimal128 (.NET 11) | 20.15 | **1.28×** | Rcs11 |  |
| csharp | add | OQ | P-gen | arm64 | thru | 39.40 | Decimal128 (.NET 11) | 142.85 | **3.63×** | Rcs11 |  |
| csharp | add | FQ | P-gen | arm64 | thru | 34.98 | Decimal128 (.NET 11) | 1245.45 | **35.60×** | Rcs11 |  |

<!-- END GENERATED add-rel-csharp -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-csharp-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | add | SQ | P-gen | x86_64 | thru | 16.85 | System.Decimal | 11.85 | **0.70×** | xRcs11 | compact idiom peer |
| csharp | add | NQ | P-gen | x86_64 | thru | 16.65 | System.Decimal | 16.67 | **1.00×** | xRcs11 | compact idiom peer |
| csharp | add | MQ | P-gen | x86_64 | thru | 42.58 | System.Decimal | 17.57 | **0.41×** | xRcs11 | compact idiom peer |
| csharp | add | SQ | P-gen | x86_64 | thru | 16.85 | Decimal128 (.NET 11) | 64.42 | **3.82×** | xRcs11 |  |
| csharp | add | NQ | P-gen | x86_64 | thru | 16.65 | Decimal128 (.NET 11) | 67.34 | **4.04×** | xRcs11 |  |
| csharp | add | MQ | P-gen | x86_64 | thru | 42.58 | Decimal128 (.NET 11) | 67.92 | **1.60×** | xRcs11 |  |
| csharp | add | OQ | P-gen | x86_64 | thru | 84.60 | Decimal128 (.NET 11) | 353.25 | **4.18×** | xRcs11 |  |
| csharp | add | FQ | P-gen | x86_64 | thru | 65.20 | Decimal128 (.NET 11) | 3162.13 | **48.50×** | xRcs11 |  |

<!-- END GENERATED add-rel-csharp-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-csharp -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | sub | SQ | P-gen | arm64 | thru | 9.06 | System.Decimal | 2.66 | **0.29×** | Rcs11 | compact idiom peer |
| csharp | sub | NQ | P-gen | arm64 | thru | 5.83 | System.Decimal | 4.16 | **0.71×** | Rcs11 | compact idiom peer |
| csharp | sub | MQ | P-gen | arm64 | thru | 14.81 | System.Decimal | 4.11 | **0.28×** | Rcs11 | compact idiom peer |
| csharp | sub | SQ | P-gen | arm64 | thru | 9.06 | Decimal128 (.NET 11) | 19.50 | **2.15×** | Rcs11 |  |
| csharp | sub | NQ | P-gen | arm64 | thru | 5.83 | Decimal128 (.NET 11) | 19.21 | **3.30×** | Rcs11 |  |
| csharp | sub | MQ | P-gen | arm64 | thru | 14.81 | Decimal128 (.NET 11) | 19.17 | **1.29×** | Rcs11 |  |
| csharp | sub | OQ | P-gen | arm64 | thru | 39.87 | Decimal128 (.NET 11) | 142.13 | **3.56×** | Rcs11 |  |
| csharp | sub | FQ | P-gen | arm64 | thru | 32.31 | Decimal128 (.NET 11) | 1244.61 | **38.52×** | Rcs11 |  |

<!-- END GENERATED sub-rel-csharp -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-csharp-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | sub | SQ | P-gen | x86_64 | thru | 19.32 | System.Decimal | 12.03 | **0.62×** | xRcs11 | compact idiom peer |
| csharp | sub | NQ | P-gen | x86_64 | thru | 19.00 | System.Decimal | 16.70 | **0.88×** | xRcs11 | compact idiom peer |
| csharp | sub | MQ | P-gen | x86_64 | thru | 41.83 | System.Decimal | 16.02 | **0.38×** | xRcs11 | compact idiom peer |
| csharp | sub | SQ | P-gen | x86_64 | thru | 19.32 | Decimal128 (.NET 11) | 64.83 | **3.36×** | xRcs11 |  |
| csharp | sub | NQ | P-gen | x86_64 | thru | 19.00 | Decimal128 (.NET 11) | 66.44 | **3.50×** | xRcs11 |  |
| csharp | sub | MQ | P-gen | x86_64 | thru | 41.83 | Decimal128 (.NET 11) | 68.44 | **1.64×** | xRcs11 |  |
| csharp | sub | OQ | P-gen | x86_64 | thru | 85.34 | Decimal128 (.NET 11) | 356.31 | **4.18×** | xRcs11 |  |
| csharp | sub | FQ | P-gen | x86_64 | thru | 63.64 | Decimal128 (.NET 11) | 3150.05 | **49.50×** | xRcs11 |  |

<!-- END GENERATED sub-rel-csharp-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-csharp -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | mul | CP | P-gen | arm64 | thru | 2.24 | Decimal128 (.NET 11) | 10.93 | **4.88×** | Rcs11 |  |
| csharp | mul | WP | P-gen | arm64 | thru | 22.03 | Decimal128 (.NET 11) | 47.85 | **2.17×** | Rcs11 |  |
| csharp | mul | XP | P-gen | arm64 | thru | 50.99 | Decimal128 (.NET 11) | 1217.57 | **23.88×** | Rcs11 |  |

<!-- END GENERATED mul-rel-csharp -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-csharp-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | mul | CP | P-gen | x86_64 | thru | 7.59 | Decimal128 (.NET 11) | 41.41 | **5.46×** | xRcs11 |  |
| csharp | mul | WP | P-gen | x86_64 | thru | 52.80 | Decimal128 (.NET 11) | 130.07 | **2.46×** | xRcs11 |  |
| csharp | mul | XP | P-gen | x86_64 | thru | 84.97 | Decimal128 (.NET 11) | 2986.32 | **35.15×** | xRcs11 |  |

<!-- END GENERATED mul-rel-csharp-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-csharp -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | div | CD | P-gen | arm64 | thru | 29.33 | Decimal128 (.NET 11) | 118.44 | **4.04×** | Rcs11 |  |
| csharp | div | WD | P-gen | arm64 | thru | 48.07 | Decimal128 (.NET 11) | 157.80 | **3.28×** | Rcs11 |  |
| csharp | div | XD | P-gen | arm64 | thru | 48.34 | Decimal128 (.NET 11) | 560.19 | **11.59×** | Rcs11 |  |
| csharp | div | ET | P-gen | arm64 | thru | 19.17 | Decimal128 (.NET 11) | 152.48 | **7.95×** | Rcs11 |  |
| csharp | div | PT | P-gen | arm64 | thru | 10.98 | Decimal128 (.NET 11) | 148.50 | **13.52×** | Rcs11 |  |

<!-- END GENERATED div-rel-csharp -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-csharp-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | div | CD | P-gen | x86_64 | thru | 104.79 | Decimal128 (.NET 11) | 379.53 | **3.62×** | xRcs11 |  |
| csharp | div | WD | P-gen | x86_64 | thru | 116.41 | Decimal128 (.NET 11) | 442.40 | **3.80×** | xRcs11 |  |
| csharp | div | XD | P-gen | x86_64 | thru | 115.59 | Decimal128 (.NET 11) | 1189.40 | **10.29×** | xRcs11 |  |
| csharp | div | ET | P-gen | x86_64 | thru | 52.30 | Decimal128 (.NET 11) | 540.04 | **10.33×** | xRcs11 |  |
| csharp | div | PT | P-gen | x86_64 | thru | 11.85 | Decimal128 (.NET 11) | 525.23 | **44.32×** | xRcs11 |  |

<!-- END GENERATED div-rel-csharp-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-csharp -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | fma | FN | FMA | arm64 | thru | 107.51 | - | - | - | Rcs11 |  |
| csharp | fma | FF | FMA | arm64 | thru | 83.93 | - | - | - | Rcs11 |  |

<!-- END GENERATED fma-rel-csharp -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-csharp-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | fma | FN | FMA | x86_64 | thru | 187.99 | - | - | - | xRcs11 |  |
| csharp | fma | FF | FMA | x86_64 | thru | 146.06 | - | - | - | xRcs11 |  |

<!-- END GENERATED fma-rel-csharp-x86 -->

</div>
