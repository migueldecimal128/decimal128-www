---
layout: default
permalink: /benchmark/vs-python.html
title: "Python Benchmark Results — Decimal128"
description: "decimal128 in Python, measured against the alternatives available to it — a realistic financial mix (P-fin) plus per-operation band characterization, with explicit ratios."
heading: "Python Benchmark Results"
---

<div class="whitepaper" markdown="1">

<p class="whitepaper-meta">Living document — as-measured results. Category codes, profiles, modes &amp; method: <a href="key.html">Benchmark Key</a>.</p>

This is the **Python** view of decimal128 **as-measured**, band by band, with explicit ratios. It opens with the realistic financial-mix (**P-fin**) headline, then the per-operation band characterization (**P-gen**) and FMA. In Python, d128 is measured against its in-language idiom peer **`decimal.Decimal`**, falling back to the **libbid** universal reference where it cannot represent the band. It is **data only** — the categories, magnitude profiles, units, and methodology are defined in the [Benchmark Key](key.html) (and, authoritatively, `BenchmarkMatrix.md`). The cross-port d128 band-shape matrices (all ports, no alternatives) live in [Port-Comparison Benchmark Results](port-compare.html); the full index of per-language pages is on the [Benchmarks](/benchmarks.html) hub.

## Summary — Ratio Range by Operation

The ratio for Python's idiom peer on x86_64 (Intel i9-9880H): `ratio = decimal.Decimal / Miguel` (&gt; 1× ⇒ d128 faster), broken out by operation.

| | Add | Subtract | Multiply | Divide |
|---|---|---|---|---|
| ratio = decimal.Decimal / Miguel | 2.6× | 2.7× | 1.7× – 3× | 1.8× – 4× |

## FinMix — realistic financial mix (P-fin)

The headline: one realistic 64-bit financial operation mix — a `MIX` add/sub stream, mul `CP`/`WP`, div `CD`/`WD`/`ET`/`PT` — `ratio = alt / Miguel` (&gt; 1 ⇒ d128 faster). This is the profile closest to real financial code.

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED pfin-rel-python -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | add | MIX | P-fin | arm64 | thru | 21.39 | decimal.Decimal | 60.73 | **2.84×** | Rpysw2 | compact idiom peer |
| python | sub | MIX | P-fin | arm64 | thru | 20.30 | decimal.Decimal | 62.53 | **3.08×** | Rpysw2 | compact idiom peer |
| python | mul | CP | P-fin | arm64 | thru | 16.56 | decimal.Decimal | 62.70 | **3.79×** | Rpysw2 | compact idiom peer |
| python | mul | WP | P-fin | arm64 | thru | 38.68 | decimal.Decimal | 67.60 | **1.75×** | Rpysw2 | compact idiom peer |
| python | div | CD | P-fin | arm64 | thru | 55.59 | decimal.Decimal | 97.57 | **1.76×** | Rpysw2 | compact idiom peer |
| python | div | WD | P-fin | arm64 | thru | 66.68 | decimal.Decimal | 100.36 | **1.51×** | Rpysw2 | compact idiom peer |
| python | div | ET | P-fin | arm64 | thru | 21.73 | decimal.Decimal | 87.85 | **4.04×** | Rpysw2 | compact idiom peer |
| python | div | PT | P-fin | arm64 | thru | 18.40 | decimal.Decimal | 86.40 | **4.70×** | Rpysw2 | compact idiom peer |

<!-- END GENERATED pfin-rel-python -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-python-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | add | MIX | P-fin | x86_64 | thru | 42.96 | decimal.Decimal | 118.15 | **2.75×** | xRpysw2 | compact idiom peer |
| python | sub | MIX | P-fin | x86_64 | thru | 44.37 | decimal.Decimal | 122.03 | **2.75×** | xRpysw2 | compact idiom peer |
| python | mul | CP | P-fin | x86_64 | thru | 39.80 | decimal.Decimal | 113.35 | **2.85×** | xRpysw2 | compact idiom peer |
| python | mul | WP | P-fin | x86_64 | thru | 76.74 | decimal.Decimal | 129.82 | **1.69×** | xRpysw2 | compact idiom peer |
| python | div | CD | P-fin | x86_64 | thru | 104.89 | decimal.Decimal | 204.75 | **1.95×** | xRpysw2 | compact idiom peer |
| python | div | WD | P-fin | x86_64 | thru | 120.57 | decimal.Decimal | 226.14 | **1.88×** | xRpysw2 | compact idiom peer |
| python | div | ET | P-fin | x86_64 | thru | 53.75 | decimal.Decimal | 184.04 | **3.42×** | xRpysw2 | compact idiom peer |
| python | div | PT | P-fin | x86_64 | thru | 44.76 | decimal.Decimal | 178.34 | **3.98×** | xRpysw2 | compact idiom peer |

<!-- END GENERATED pfin-rel-python-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-python -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | add | SQss | P-gen | arm64 | thru | 16.24 | decimal.Decimal | 57.93 | **3.57×** | Rpysw2 | compact idiom peer |
| python | add | SQos | P-gen | arm64 | thru | 17.76 | decimal.Decimal | 62.64 | **3.53×** | Rpysw2 | compact idiom peer |
| python | add | NQss | P-gen | arm64 | thru | 19.19 | decimal.Decimal | 69.37 | **3.61×** | Rpysw2 | compact idiom peer |
| python | add | NQos | P-gen | arm64 | thru | 19.53 | decimal.Decimal | 72.89 | **3.73×** | Rpysw2 | compact idiom peer |
| python | add | MQss | P-gen | arm64 | thru | 21.25 | decimal.Decimal | 68.97 | **3.25×** | Rpysw2 | compact idiom peer |
| python | add | MQos | P-gen | arm64 | thru | 29.40 | decimal.Decimal | 72.68 | **2.47×** | Rpysw2 | compact idiom peer |
| python | add | OQss | P-gen | arm64 | thru | 37.80 | decimal.Decimal | 84.43 | **2.23×** | Rpysw2 | compact idiom peer |
| python | add | OQos | P-gen | arm64 | thru | 39.87 | decimal.Decimal | 85.87 | **2.15×** | Rpysw2 | compact idiom peer |
| python | add | FQss | P-gen | arm64 | thru | 31.21 | decimal.Decimal | 76.71 | **2.46×** | Rpysw2 | compact idiom peer |
| python | add | FQos | P-gen | arm64 | thru | 29.96 | decimal.Decimal | 79.36 | **2.65×** | Rpysw2 | compact idiom peer |

<!-- END GENERATED add-rel-python -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-python-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | add | SQss | P-gen | x86_64 | thru | 39.01 | decimal.Decimal | 113.84 | **2.92×** | xRpysw2 | compact idiom peer |
| python | add | SQos | P-gen | x86_64 | thru | 43.90 | decimal.Decimal | 120.65 | **2.75×** | xRpysw2 | compact idiom peer |
| python | add | NQss | P-gen | x86_64 | thru | 44.75 | decimal.Decimal | 134.19 | **3.00×** | xRpysw2 | compact idiom peer |
| python | add | NQos | P-gen | x86_64 | thru | 45.94 | decimal.Decimal | 136.21 | **2.96×** | xRpysw2 | compact idiom peer |
| python | add | MQss | P-gen | x86_64 | thru | 47.53 | decimal.Decimal | 131.85 | **2.77×** | xRpysw2 | compact idiom peer |
| python | add | MQos | P-gen | x86_64 | thru | 58.98 | decimal.Decimal | 136.60 | **2.32×** | xRpysw2 | compact idiom peer |
| python | add | OQss | P-gen | x86_64 | thru | 65.23 | decimal.Decimal | 160.78 | **2.46×** | xRpysw2 | compact idiom peer |
| python | add | OQos | P-gen | x86_64 | thru | 73.44 | decimal.Decimal | 161.49 | **2.20×** | xRpysw2 | compact idiom peer |
| python | add | FQss | P-gen | x86_64 | thru | 56.29 | decimal.Decimal | 154.24 | **2.74×** | xRpysw2 | compact idiom peer |
| python | add | FQos | P-gen | x86_64 | thru | 63.93 | decimal.Decimal | 162.39 | **2.54×** | xRpysw2 | compact idiom peer |

<!-- END GENERATED add-rel-python-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-python -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | sub | SQss | P-gen | arm64 | thru | 16.44 | decimal.Decimal | 60.91 | **3.70×** | Rpysw2 | compact idiom peer |
| python | sub | SQos | P-gen | arm64 | thru | 16.05 | decimal.Decimal | 57.15 | **3.56×** | Rpysw2 | compact idiom peer |
| python | sub | NQss | P-gen | arm64 | thru | 19.34 | decimal.Decimal | 72.94 | **3.77×** | Rpysw2 | compact idiom peer |
| python | sub | NQos | P-gen | arm64 | thru | 18.91 | decimal.Decimal | 68.08 | **3.60×** | Rpysw2 | compact idiom peer |
| python | sub | MQss | P-gen | arm64 | thru | 28.38 | decimal.Decimal | 73.15 | **2.58×** | Rpysw2 | compact idiom peer |
| python | sub | MQos | P-gen | arm64 | thru | 20.76 | decimal.Decimal | 68.17 | **3.28×** | Rpysw2 | compact idiom peer |
| python | sub | OQss | P-gen | arm64 | thru | 38.91 | decimal.Decimal | 85.33 | **2.19×** | Rpysw2 | compact idiom peer |
| python | sub | OQos | P-gen | arm64 | thru | 36.73 | decimal.Decimal | 83.55 | **2.27×** | Rpysw2 | compact idiom peer |
| python | sub | FQss | P-gen | arm64 | thru | 29.49 | decimal.Decimal | 79.68 | **2.70×** | Rpysw2 | compact idiom peer |
| python | sub | FQos | P-gen | arm64 | thru | 30.99 | decimal.Decimal | 75.78 | **2.45×** | Rpysw2 | compact idiom peer |

<!-- END GENERATED sub-rel-python -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-python-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | sub | SQss | P-gen | x86_64 | thru | 41.92 | decimal.Decimal | 120.38 | **2.87×** | xRpysw2 | compact idiom peer |
| python | sub | SQos | P-gen | x86_64 | thru | 39.67 | decimal.Decimal | 110.11 | **2.78×** | xRpysw2 | compact idiom peer |
| python | sub | NQss | P-gen | x86_64 | thru | 47.07 | decimal.Decimal | 136.66 | **2.90×** | xRpysw2 | compact idiom peer |
| python | sub | NQos | P-gen | x86_64 | thru | 45.14 | decimal.Decimal | 130.13 | **2.88×** | xRpysw2 | compact idiom peer |
| python | sub | MQss | P-gen | x86_64 | thru | 59.81 | decimal.Decimal | 136.77 | **2.29×** | xRpysw2 | compact idiom peer |
| python | sub | MQos | P-gen | x86_64 | thru | 48.12 | decimal.Decimal | 130.32 | **2.71×** | xRpysw2 | compact idiom peer |
| python | sub | OQss | P-gen | x86_64 | thru | 74.08 | decimal.Decimal | 162.20 | **2.19×** | xRpysw2 | compact idiom peer |
| python | sub | OQos | P-gen | x86_64 | thru | 65.32 | decimal.Decimal | 158.88 | **2.43×** | xRpysw2 | compact idiom peer |
| python | sub | FQss | P-gen | x86_64 | thru | 65.14 | decimal.Decimal | 160.39 | **2.46×** | xRpysw2 | compact idiom peer |
| python | sub | FQos | P-gen | x86_64 | thru | 58.49 | decimal.Decimal | 157.86 | **2.70×** | xRpysw2 | compact idiom peer |

<!-- END GENERATED sub-rel-python-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-python -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | mul | CP | P-gen | arm64 | thru | 19.07 | decimal.Decimal | 63.14 | **3.31×** | Rpysw2 | compact idiom peer |
| python | mul | WP | P-gen | arm64 | thru | 39.25 | decimal.Decimal | 73.30 | **1.87×** | Rpysw2 | compact idiom peer |
| python | mul | XP | P-gen | arm64 | thru | 46.47 | decimal.Decimal | 91.74 | **1.97×** | Rpysw2 | compact idiom peer |

<!-- END GENERATED mul-rel-python -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-python-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | mul | CP | P-gen | x86_64 | thru | 42.76 | decimal.Decimal | 115.04 | **2.69×** | xRpysw2 | compact idiom peer |
| python | mul | WP | P-gen | x86_64 | thru | 78.71 | decimal.Decimal | 137.26 | **1.74×** | xRpysw2 | compact idiom peer |
| python | mul | XP | P-gen | x86_64 | thru | 88.01 | decimal.Decimal | 159.75 | **1.82×** | xRpysw2 | compact idiom peer |

<!-- END GENERATED mul-rel-python-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-python -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | div | CD | P-gen | arm64 | thru | 56.20 | decimal.Decimal | 100.33 | **1.79×** | Rpysw2 | compact idiom peer |
| python | div | WD | P-gen | arm64 | thru | 65.65 | decimal.Decimal | 103.99 | **1.58×** | Rpysw2 | compact idiom peer |
| python | div | XD | P-gen | arm64 | thru | 63.05 | decimal.Decimal | 168.00 | **2.66×** | Rpysw2 | compact idiom peer |
| python | div | ET | P-gen | arm64 | thru | 25.33 | decimal.Decimal | 93.95 | **3.71×** | Rpysw2 | compact idiom peer |
| python | div | PT | P-gen | arm64 | thru | 18.52 | decimal.Decimal | 90.32 | **4.88×** | Rpysw2 | compact idiom peer |

<!-- END GENERATED div-rel-python -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-python-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | div | CD | P-gen | x86_64 | thru | 111.49 | decimal.Decimal | 210.15 | **1.88×** | xRpysw2 | compact idiom peer |
| python | div | WD | P-gen | x86_64 | thru | 120.52 | decimal.Decimal | 229.34 | **1.90×** | xRpysw2 | compact idiom peer |
| python | div | XD | P-gen | x86_64 | thru | 116.64 | decimal.Decimal | 361.51 | **3.10×** | xRpysw2 | compact idiom peer |
| python | div | ET | P-gen | x86_64 | thru | 68.24 | decimal.Decimal | 201.68 | **2.96×** | xRpysw2 | compact idiom peer |
| python | div | PT | P-gen | x86_64 | thru | 44.72 | decimal.Decimal | 181.50 | **4.06×** | xRpysw2 | compact idiom peer |

<!-- END GENERATED div-rel-python-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-python -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | fma | FN | FMA | arm64 | thru | 110.01 | decimal.Decimal | 142.58 | **1.30×** | Rpysw2 | compact idiom peer |
| python | fma | FF | FMA | arm64 | thru | 79.92 | decimal.Decimal | 164.27 | **2.06×** | Rpysw2 | compact idiom peer |

<!-- END GENERATED fma-rel-python -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-python-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | fma | FN | FMA | x86_64 | thru | 228.93 | decimal.Decimal | 301.24 | **1.32×** | xRpysw2 | compact idiom peer |
| python | fma | FF | FMA | x86_64 | thru | 185.09 | decimal.Decimal | 343.91 | **1.86×** | xRpysw2 | compact idiom peer |

<!-- END GENERATED fma-rel-python-x86 -->

</div>
