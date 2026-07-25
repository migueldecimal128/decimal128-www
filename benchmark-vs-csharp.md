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
| csharp | add | MIX | P-fin | arm64 | thru | 2.69 | System.Decimal | 2.79 | **1.04×** | Rcs11 | compact idiom peer |
| csharp | sub | MIX | P-fin | arm64 | thru | 3.15 | System.Decimal | 3.00 | **0.95×** | Rcs11 | compact idiom peer |
| csharp | div | CD | P-fin | arm64 | thru | 27.24 | System.Decimal | 11.15 | **0.41×** | Rcs11 | compact idiom peer |
| csharp | div | WD | P-fin | arm64 | thru | 41.73 | System.Decimal | 26.96 | **0.65×** | Rcs11 | compact idiom peer |
| csharp | div | ET | P-fin | arm64 | thru | 14.03 | System.Decimal | 5.17 | **0.37×** | Rcs11 | compact idiom peer |
| csharp | div | PT | P-fin | arm64 | thru | 5.30 | System.Decimal | 12.53 | **2.36×** | Rcs11 | compact idiom peer |
| csharp | add | MIX | P-fin | arm64 | thru | 2.69 | Decimal128 (.NET 11) | 17.07 | **6.35×** | Rcs11 |  |
| csharp | sub | MIX | P-fin | arm64 | thru | 3.15 | Decimal128 (.NET 11) | 17.14 | **5.44×** | Rcs11 |  |
| csharp | mul | CP | P-fin | arm64 | thru | 1.77 | Decimal128 (.NET 11) | 11.12 | **6.28×** | Rcs11 |  |
| csharp | mul | WP | P-fin | arm64 | thru | 23.87 | Decimal128 (.NET 11) | 47.54 | **1.99×** | Rcs11 |  |
| csharp | div | CD | P-fin | arm64 | thru | 27.24 | Decimal128 (.NET 11) | 154.95 | **5.69×** | Rcs11 |  |
| csharp | div | WD | P-fin | arm64 | thru | 41.73 | Decimal128 (.NET 11) | 181.82 | **4.36×** | Rcs11 |  |
| csharp | div | ET | P-fin | arm64 | thru | 14.03 | Decimal128 (.NET 11) | 237.56 | **16.93×** | Rcs11 |  |
| csharp | div | PT | P-fin | arm64 | thru | 5.30 | Decimal128 (.NET 11) | 242.05 | **45.67×** | Rcs11 |  |

<!-- END GENERATED pfin-rel-csharp -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-csharp-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | add | MIX | P-fin | x86_64 | thru | 8.73 | System.Decimal | 8.84 | **1.01×** | xRcs11 | compact idiom peer |
| csharp | sub | MIX | P-fin | x86_64 | thru | 12.92 | System.Decimal | 10.74 | **0.83×** | xRcs11 | compact idiom peer |
| csharp | div | CD | P-fin | x86_64 | thru | 99.01 | System.Decimal | 52.53 | **0.53×** | xRcs11 | compact idiom peer |
| csharp | div | WD | P-fin | x86_64 | thru | 117.28 | System.Decimal | 101.76 | **0.87×** | xRcs11 | compact idiom peer |
| csharp | div | ET | P-fin | x86_64 | thru | 27.36 | System.Decimal | 15.59 | **0.57×** | xRcs11 | compact idiom peer |
| csharp | div | PT | P-fin | x86_64 | thru | 11.93 | System.Decimal | 59.05 | **4.95×** | xRcs11 | compact idiom peer |
| csharp | add | MIX | P-fin | x86_64 | thru | 8.73 | Decimal128 (.NET 11) | 33.88 | **3.88×** | xRcs11 |  |
| csharp | sub | MIX | P-fin | x86_64 | thru | 12.92 | Decimal128 (.NET 11) | 37.11 | **2.87×** | xRcs11 |  |
| csharp | mul | CP | P-fin | x86_64 | thru | 5.81 | Decimal128 (.NET 11) | 39.88 | **6.86×** | xRcs11 |  |
| csharp | mul | WP | P-fin | x86_64 | thru | 46.74 | Decimal128 (.NET 11) | 125.92 | **2.69×** | xRcs11 |  |
| csharp | div | CD | P-fin | x86_64 | thru | 99.01 | Decimal128 (.NET 11) | 425.02 | **4.29×** | xRcs11 |  |
| csharp | div | WD | P-fin | x86_64 | thru | 117.28 | Decimal128 (.NET 11) | 473.24 | **4.04×** | xRcs11 |  |
| csharp | div | ET | P-fin | x86_64 | thru | 27.36 | Decimal128 (.NET 11) | 619.39 | **22.64×** | xRcs11 |  |
| csharp | div | PT | P-fin | x86_64 | thru | 11.93 | Decimal128 (.NET 11) | 629.83 | **52.79×** | xRcs11 |  |

<!-- END GENERATED pfin-rel-csharp-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-csharp -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | add | SQ | P-gen | arm64 | thru | 6.02 | System.Decimal | 2.52 | **0.42×** | Rcs11 | compact idiom peer |
| csharp | add | NQ | P-gen | arm64 | thru | 4.91 | System.Decimal | 4.15 | **0.85×** | Rcs11 | compact idiom peer |
| csharp | add | MQ | P-gen | arm64 | thru | 15.97 | System.Decimal | 3.99 | **0.25×** | Rcs11 | compact idiom peer |
| csharp | add | SQ | P-gen | arm64 | thru | 6.02 | Decimal128 (.NET 11) | 19.82 | **3.29×** | Rcs11 |  |
| csharp | add | NQ | P-gen | arm64 | thru | 4.91 | Decimal128 (.NET 11) | 18.97 | **3.86×** | Rcs11 |  |
| csharp | add | MQ | P-gen | arm64 | thru | 15.97 | Decimal128 (.NET 11) | 19.64 | **1.23×** | Rcs11 |  |
| csharp | add | OQ | P-gen | arm64 | thru | 39.53 | Decimal128 (.NET 11) | 143.67 | **3.63×** | Rcs11 |  |
| csharp | add | FQ | P-gen | arm64 | thru | 34.82 | Decimal128 (.NET 11) | 1251.36 | **35.94×** | Rcs11 |  |

<!-- END GENERATED add-rel-csharp -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-csharp-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | add | SQ | P-gen | x86_64 | thru | 15.32 | System.Decimal | 11.86 | **0.77×** | xRcs11 | compact idiom peer |
| csharp | add | NQ | P-gen | x86_64 | thru | 17.57 | System.Decimal | 16.64 | **0.95×** | xRcs11 | compact idiom peer |
| csharp | add | MQ | P-gen | x86_64 | thru | 42.15 | System.Decimal | 17.36 | **0.41×** | xRcs11 | compact idiom peer |
| csharp | add | SQ | P-gen | x86_64 | thru | 15.32 | Decimal128 (.NET 11) | 61.70 | **4.03×** | xRcs11 |  |
| csharp | add | NQ | P-gen | x86_64 | thru | 17.57 | Decimal128 (.NET 11) | 65.57 | **3.73×** | xRcs11 |  |
| csharp | add | MQ | P-gen | x86_64 | thru | 42.15 | Decimal128 (.NET 11) | 65.65 | **1.56×** | xRcs11 |  |
| csharp | add | OQ | P-gen | x86_64 | thru | 82.23 | Decimal128 (.NET 11) | 340.59 | **4.14×** | xRcs11 |  |
| csharp | add | FQ | P-gen | x86_64 | thru | 62.37 | Decimal128 (.NET 11) | 3044.09 | **48.81×** | xRcs11 |  |

<!-- END GENERATED add-rel-csharp-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-csharp -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | sub | SQ | P-gen | arm64 | thru | 9.15 | System.Decimal | 2.56 | **0.28×** | Rcs11 | compact idiom peer |
| csharp | sub | NQ | P-gen | arm64 | thru | 5.78 | System.Decimal | 4.15 | **0.72×** | Rcs11 | compact idiom peer |
| csharp | sub | MQ | P-gen | arm64 | thru | 14.98 | System.Decimal | 4.08 | **0.27×** | Rcs11 | compact idiom peer |
| csharp | sub | SQ | P-gen | arm64 | thru | 9.15 | Decimal128 (.NET 11) | 19.58 | **2.14×** | Rcs11 |  |
| csharp | sub | NQ | P-gen | arm64 | thru | 5.78 | Decimal128 (.NET 11) | 19.09 | **3.30×** | Rcs11 |  |
| csharp | sub | MQ | P-gen | arm64 | thru | 14.98 | Decimal128 (.NET 11) | 19.27 | **1.29×** | Rcs11 |  |
| csharp | sub | OQ | P-gen | arm64 | thru | 39.88 | Decimal128 (.NET 11) | 143.85 | **3.61×** | Rcs11 |  |
| csharp | sub | FQ | P-gen | arm64 | thru | 33.74 | Decimal128 (.NET 11) | 1251.64 | **37.10×** | Rcs11 |  |

<!-- END GENERATED sub-rel-csharp -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-csharp-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | sub | SQ | P-gen | x86_64 | thru | 18.83 | System.Decimal | 11.48 | **0.61×** | xRcs11 | compact idiom peer |
| csharp | sub | NQ | P-gen | x86_64 | thru | 18.34 | System.Decimal | 16.47 | **0.90×** | xRcs11 | compact idiom peer |
| csharp | sub | MQ | P-gen | x86_64 | thru | 41.39 | System.Decimal | 15.64 | **0.38×** | xRcs11 | compact idiom peer |
| csharp | sub | SQ | P-gen | x86_64 | thru | 18.83 | Decimal128 (.NET 11) | 62.10 | **3.30×** | xRcs11 |  |
| csharp | sub | NQ | P-gen | x86_64 | thru | 18.34 | Decimal128 (.NET 11) | 64.81 | **3.53×** | xRcs11 |  |
| csharp | sub | MQ | P-gen | x86_64 | thru | 41.39 | Decimal128 (.NET 11) | 66.56 | **1.61×** | xRcs11 |  |
| csharp | sub | OQ | P-gen | x86_64 | thru | 81.43 | Decimal128 (.NET 11) | 358.81 | **4.41×** | xRcs11 |  |
| csharp | sub | FQ | P-gen | x86_64 | thru | 64.33 | Decimal128 (.NET 11) | 3094.16 | **48.10×** | xRcs11 |  |

<!-- END GENERATED sub-rel-csharp-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-csharp -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | mul | CP | P-gen | arm64 | thru | 2.18 | Decimal128 (.NET 11) | 10.95 | **5.02×** | Rcs11 |  |
| csharp | mul | WP | P-gen | arm64 | thru | 22.83 | Decimal128 (.NET 11) | 54.22 | **2.37×** | Rcs11 |  |
| csharp | mul | XP | P-gen | arm64 | thru | 52.39 | Decimal128 (.NET 11) | 1222.02 | **23.33×** | Rcs11 |  |

<!-- END GENERATED mul-rel-csharp -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-csharp-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | mul | CP | P-gen | x86_64 | thru | 7.38 | Decimal128 (.NET 11) | 37.33 | **5.06×** | xRcs11 |  |
| csharp | mul | WP | P-gen | x86_64 | thru | 51.32 | Decimal128 (.NET 11) | 121.90 | **2.38×** | xRcs11 |  |
| csharp | mul | XP | P-gen | x86_64 | thru | 82.92 | Decimal128 (.NET 11) | 2968.36 | **35.80×** | xRcs11 |  |

<!-- END GENERATED mul-rel-csharp-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-csharp -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | div | CD | P-gen | arm64 | thru | 29.45 | Decimal128 (.NET 11) | 113.46 | **3.85×** | Rcs11 |  |
| csharp | div | WD | P-gen | arm64 | thru | 47.00 | Decimal128 (.NET 11) | 158.00 | **3.36×** | Rcs11 |  |
| csharp | div | XD | P-gen | arm64 | thru | 49.02 | Decimal128 (.NET 11) | 561.63 | **11.46×** | Rcs11 |  |
| csharp | div | ET | P-gen | arm64 | thru | 19.14 | Decimal128 (.NET 11) | 153.02 | **7.99×** | Rcs11 |  |
| csharp | div | PT | P-gen | arm64 | thru | 11.67 | Decimal128 (.NET 11) | 151.10 | **12.95×** | Rcs11 |  |

<!-- END GENERATED div-rel-csharp -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-csharp-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | div | CD | P-gen | x86_64 | thru | 101.57 | Decimal128 (.NET 11) | 361.56 | **3.56×** | xRcs11 |  |
| csharp | div | WD | P-gen | x86_64 | thru | 110.76 | Decimal128 (.NET 11) | 428.13 | **3.87×** | xRcs11 |  |
| csharp | div | XD | P-gen | x86_64 | thru | 112.82 | Decimal128 (.NET 11) | 1160.87 | **10.29×** | xRcs11 |  |
| csharp | div | ET | P-gen | x86_64 | thru | 52.27 | Decimal128 (.NET 11) | 516.67 | **9.88×** | xRcs11 |  |
| csharp | div | PT | P-gen | x86_64 | thru | 11.28 | Decimal128 (.NET 11) | 501.95 | **44.50×** | xRcs11 |  |

<!-- END GENERATED div-rel-csharp-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-csharp -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | fma | FN | FMA | arm64 | thru | 105.42 | - | - | - | Rcs11 |  |
| csharp | fma | FF | FMA | arm64 | thru | 84.16 | - | - | - | Rcs11 |  |

<!-- END GENERATED fma-rel-csharp -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-csharp-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| csharp | fma | FN | FMA | x86_64 | thru | 182.05 | - | - | - | xRcs11 |  |
| csharp | fma | FF | FMA | x86_64 | thru | 142.09 | - | - | - | xRcs11 |  |

<!-- END GENERATED fma-rel-csharp-x86 -->

</div>
