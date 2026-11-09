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
| ratio = decimal.Decimal / Miguel | 3× | 2.9× | 1.9× – 3× | 1.8× – 4× |

## FinMix — realistic financial mix (P-fin)

The headline: one realistic 64-bit financial operation mix — a `MIX` add/sub stream, mul `CP`/`WP`, div `CD`/`WD`/`ET`/`PT` — `ratio = alt / Miguel` (&gt; 1 ⇒ d128 faster). This is the profile closest to real financial code.

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED pfin-rel-python -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | add | MIX | P-fin | arm64 | thru | 21.18 | decimal.Decimal | 60.44 | **2.85×** | Rpysw2 | compact idiom peer |
| python | sub | MIX | P-fin | arm64 | thru | 21.14 | decimal.Decimal | 62.80 | **2.97×** | Rpysw2 | compact idiom peer |
| python | mul | CP | P-fin | arm64 | thru | 16.65 | decimal.Decimal | 63.78 | **3.83×** | Rpysw2 | compact idiom peer |
| python | mul | WP | P-fin | arm64 | thru | 38.77 | decimal.Decimal | 69.12 | **1.78×** | Rpysw2 | compact idiom peer |
| python | div | CD | P-fin | arm64 | thru | 54.83 | decimal.Decimal | 96.04 | **1.75×** | Rpysw2 | compact idiom peer |
| python | div | WD | P-fin | arm64 | thru | 58.92 | decimal.Decimal | 99.15 | **1.68×** | Rpysw2 | compact idiom peer |
| python | div | ET | P-fin | arm64 | thru | 21.53 | decimal.Decimal | 86.27 | **4.01×** | Rpysw2 | compact idiom peer |
| python | div | PT | P-fin | arm64 | thru | 18.30 | decimal.Decimal | 85.42 | **4.67×** | Rpysw2 | compact idiom peer |

<!-- END GENERATED pfin-rel-python -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-python-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | add | MIX | P-fin | x86_64 | thru | 47.90 | decimal.Decimal | 152.73 | **3.19×** | xRpysw2 | compact idiom peer |
| python | sub | MIX | P-fin | x86_64 | thru | 55.29 | decimal.Decimal | 160.16 | **2.90×** | xRpysw2 | compact idiom peer |
| python | mul | CP | P-fin | x86_64 | thru | 43.06 | decimal.Decimal | 146.85 | **3.41×** | xRpysw2 | compact idiom peer |
| python | mul | WP | P-fin | x86_64 | thru | 83.45 | decimal.Decimal | 165.82 | **1.99×** | xRpysw2 | compact idiom peer |
| python | div | CD | P-fin | x86_64 | thru | 116.99 | decimal.Decimal | 269.91 | **2.31×** | xRpysw2 | compact idiom peer |
| python | div | WD | P-fin | x86_64 | thru | 146.88 | decimal.Decimal | 269.70 | **1.84×** | xRpysw2 | compact idiom peer |
| python | div | ET | P-fin | x86_64 | thru | 60.27 | decimal.Decimal | 223.53 | **3.71×** | xRpysw2 | compact idiom peer |
| python | div | PT | P-fin | x86_64 | thru | 54.88 | decimal.Decimal | 223.96 | **4.08×** | xRpysw2 | compact idiom peer |

<!-- END GENERATED pfin-rel-python-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-python -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | add | SQss | P-gen | arm64 | thru | 16.12 | decimal.Decimal | 58.45 | **3.63×** | Rpysw2 | compact idiom peer |
| python | add | SQos | P-gen | arm64 | thru | 17.73 | decimal.Decimal | 61.43 | **3.46×** | Rpysw2 | compact idiom peer |
| python | add | NQss | P-gen | arm64 | thru | 19.06 | decimal.Decimal | 68.07 | **3.57×** | Rpysw2 | compact idiom peer |
| python | add | NQos | P-gen | arm64 | thru | 19.56 | decimal.Decimal | 71.26 | **3.64×** | Rpysw2 | compact idiom peer |
| python | add | MQss | P-gen | arm64 | thru | 20.91 | decimal.Decimal | 68.21 | **3.26×** | Rpysw2 | compact idiom peer |
| python | add | MQos | P-gen | arm64 | thru | 28.55 | decimal.Decimal | 70.70 | **2.48×** | Rpysw2 | compact idiom peer |
| python | add | OQss | P-gen | arm64 | thru | 36.65 | decimal.Decimal | 84.88 | **2.32×** | Rpysw2 | compact idiom peer |
| python | add | OQos | P-gen | arm64 | thru | 38.89 | decimal.Decimal | 84.95 | **2.18×** | Rpysw2 | compact idiom peer |
| python | add | FQss | P-gen | arm64 | thru | 30.44 | decimal.Decimal | 75.19 | **2.47×** | Rpysw2 | compact idiom peer |
| python | add | FQos | P-gen | arm64 | thru | 29.86 | decimal.Decimal | 78.95 | **2.64×** | Rpysw2 | compact idiom peer |

<!-- END GENERATED add-rel-python -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-python-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | add | SQss | P-gen | x86_64 | thru | 47.47 | decimal.Decimal | 142.30 | **3.00×** | xRpysw2 | compact idiom peer |
| python | add | SQos | P-gen | x86_64 | thru | 45.53 | decimal.Decimal | 144.47 | **3.17×** | xRpysw2 | compact idiom peer |
| python | add | NQss | P-gen | x86_64 | thru | 49.61 | decimal.Decimal | 174.90 | **3.53×** | xRpysw2 | compact idiom peer |
| python | add | NQos | P-gen | x86_64 | thru | 51.11 | decimal.Decimal | 184.75 | **3.61×** | xRpysw2 | compact idiom peer |
| python | add | MQss | P-gen | x86_64 | thru | 53.89 | decimal.Decimal | 176.98 | **3.28×** | xRpysw2 | compact idiom peer |
| python | add | MQos | P-gen | x86_64 | thru | 67.98 | decimal.Decimal | 184.73 | **2.72×** | xRpysw2 | compact idiom peer |
| python | add | OQss | P-gen | x86_64 | thru | 75.68 | decimal.Decimal | 212.33 | **2.81×** | xRpysw2 | compact idiom peer |
| python | add | OQos | P-gen | x86_64 | thru | 84.52 | decimal.Decimal | 208.48 | **2.47×** | xRpysw2 | compact idiom peer |
| python | add | FQss | P-gen | x86_64 | thru | 69.42 | decimal.Decimal | 195.28 | **2.81×** | xRpysw2 | compact idiom peer |
| python | add | FQos | P-gen | x86_64 | thru | 77.41 | decimal.Decimal | 211.82 | **2.74×** | xRpysw2 | compact idiom peer |

<!-- END GENERATED add-rel-python-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-python -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | sub | SQss | P-gen | arm64 | thru | 16.41 | decimal.Decimal | 60.70 | **3.70×** | Rpysw2 | compact idiom peer |
| python | sub | SQos | P-gen | arm64 | thru | 16.00 | decimal.Decimal | 57.51 | **3.59×** | Rpysw2 | compact idiom peer |
| python | sub | NQss | P-gen | arm64 | thru | 19.17 | decimal.Decimal | 71.18 | **3.71×** | Rpysw2 | compact idiom peer |
| python | sub | NQos | P-gen | arm64 | thru | 18.89 | decimal.Decimal | 66.79 | **3.54×** | Rpysw2 | compact idiom peer |
| python | sub | MQss | P-gen | arm64 | thru | 28.25 | decimal.Decimal | 70.83 | **2.51×** | Rpysw2 | compact idiom peer |
| python | sub | MQos | P-gen | arm64 | thru | 21.04 | decimal.Decimal | 67.87 | **3.23×** | Rpysw2 | compact idiom peer |
| python | sub | OQss | P-gen | arm64 | thru | 38.79 | decimal.Decimal | 85.39 | **2.20×** | Rpysw2 | compact idiom peer |
| python | sub | OQos | P-gen | arm64 | thru | 36.43 | decimal.Decimal | 82.26 | **2.26×** | Rpysw2 | compact idiom peer |
| python | sub | FQss | P-gen | arm64 | thru | 29.33 | decimal.Decimal | 79.73 | **2.72×** | Rpysw2 | compact idiom peer |
| python | sub | FQos | P-gen | arm64 | thru | 30.48 | decimal.Decimal | 74.37 | **2.44×** | Rpysw2 | compact idiom peer |

<!-- END GENERATED sub-rel-python -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-python-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | sub | SQss | P-gen | x86_64 | thru | 44.05 | decimal.Decimal | 154.06 | **3.50×** | xRpysw2 | compact idiom peer |
| python | sub | SQos | P-gen | x86_64 | thru | 42.70 | decimal.Decimal | 146.95 | **3.44×** | xRpysw2 | compact idiom peer |
| python | sub | NQss | P-gen | x86_64 | thru | 53.96 | decimal.Decimal | 186.57 | **3.46×** | xRpysw2 | compact idiom peer |
| python | sub | NQos | P-gen | x86_64 | thru | 51.33 | decimal.Decimal | 170.48 | **3.32×** | xRpysw2 | compact idiom peer |
| python | sub | MQss | P-gen | x86_64 | thru | 68.96 | decimal.Decimal | 184.97 | **2.68×** | xRpysw2 | compact idiom peer |
| python | sub | MQos | P-gen | x86_64 | thru | 59.49 | decimal.Decimal | 174.48 | **2.93×** | xRpysw2 | compact idiom peer |
| python | sub | OQss | P-gen | x86_64 | thru | 83.41 | decimal.Decimal | 208.47 | **2.50×** | xRpysw2 | compact idiom peer |
| python | sub | OQos | P-gen | x86_64 | thru | 84.04 | decimal.Decimal | 206.93 | **2.46×** | xRpysw2 | compact idiom peer |
| python | sub | FQss | P-gen | x86_64 | thru | 73.58 | decimal.Decimal | 205.35 | **2.79×** | xRpysw2 | compact idiom peer |
| python | sub | FQos | P-gen | x86_64 | thru | 64.67 | decimal.Decimal | 196.53 | **3.04×** | xRpysw2 | compact idiom peer |

<!-- END GENERATED sub-rel-python-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-python -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | mul | CP | P-gen | arm64 | thru | 19.33 | decimal.Decimal | 64.36 | **3.33×** | Rpysw2 | compact idiom peer |
| python | mul | WP | P-gen | arm64 | thru | 38.81 | decimal.Decimal | 72.01 | **1.86×** | Rpysw2 | compact idiom peer |
| python | mul | XP | P-gen | arm64 | thru | 45.56 | decimal.Decimal | 92.23 | **2.02×** | Rpysw2 | compact idiom peer |

<!-- END GENERATED mul-rel-python -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-python-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | mul | CP | P-gen | x86_64 | thru | 46.00 | decimal.Decimal | 155.08 | **3.37×** | xRpysw2 | compact idiom peer |
| python | mul | WP | P-gen | x86_64 | thru | 101.93 | decimal.Decimal | 181.19 | **1.78×** | xRpysw2 | compact idiom peer |
| python | mul | XP | P-gen | x86_64 | thru | 104.05 | decimal.Decimal | 201.77 | **1.94×** | xRpysw2 | compact idiom peer |

<!-- END GENERATED mul-rel-python-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-python -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | div | CD | P-gen | arm64 | thru | 56.00 | decimal.Decimal | 98.65 | **1.76×** | Rpysw2 | compact idiom peer |
| python | div | WD | P-gen | arm64 | thru | 58.14 | decimal.Decimal | 103.28 | **1.78×** | Rpysw2 | compact idiom peer |
| python | div | XD | P-gen | arm64 | thru | 62.58 | decimal.Decimal | 165.66 | **2.65×** | Rpysw2 | compact idiom peer |
| python | div | ET | P-gen | arm64 | thru | 25.19 | decimal.Decimal | 93.09 | **3.70×** | Rpysw2 | compact idiom peer |
| python | div | PT | P-gen | arm64 | thru | 18.42 | decimal.Decimal | 90.14 | **4.89×** | Rpysw2 | compact idiom peer |

<!-- END GENERATED div-rel-python -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-python-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | div | CD | P-gen | x86_64 | thru | 127.35 | decimal.Decimal | 255.60 | **2.01×** | xRpysw2 | compact idiom peer |
| python | div | WD | P-gen | x86_64 | thru | 134.79 | decimal.Decimal | 278.60 | **2.07×** | xRpysw2 | compact idiom peer |
| python | div | XD | P-gen | x86_64 | thru | 129.18 | decimal.Decimal | 402.02 | **3.11×** | xRpysw2 | compact idiom peer |
| python | div | ET | P-gen | x86_64 | thru | 70.18 | decimal.Decimal | 251.44 | **3.58×** | xRpysw2 | compact idiom peer |
| python | div | PT | P-gen | x86_64 | thru | 50.32 | decimal.Decimal | 239.37 | **4.76×** | xRpysw2 | compact idiom peer |

<!-- END GENERATED div-rel-python-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-python -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | fma | FN | FMA | arm64 | thru | 78.53 | decimal.Decimal | 142.16 | **1.81×** | Rpysw2 | compact idiom peer |
| python | fma | FF | FMA | arm64 | thru | 79.22 | decimal.Decimal | 163.49 | **2.06×** | Rpysw2 | compact idiom peer |

<!-- END GENERATED fma-rel-python -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-python-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | fma | FN | FMA | x86_64 | thru | 272.39 | decimal.Decimal | 366.67 | **1.35×** | xRpysw2 | compact idiom peer |
| python | fma | FF | FMA | x86_64 | thru | 197.24 | decimal.Decimal | 413.29 | **2.10×** | xRpysw2 | compact idiom peer |

<!-- END GENERATED fma-rel-python-x86 -->

</div>
