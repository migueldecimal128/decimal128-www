---
layout: default
permalink: /benchmark/vs-c.html
title: "C Benchmark Results — Decimal128"
description: "decimal128 in C, measured against the alternatives available to it — a realistic financial mix (P-fin) plus per-operation band characterization, with explicit ratios."
heading: "C Benchmark Results"
---

<div class="whitepaper" markdown="1">

<p class="whitepaper-meta">Living document — as-measured results. Category codes, profiles, modes &amp; method: <a href="key.html">Benchmark Key</a>.</p>

This is the **C** view of decimal128 **as-measured**, band by band, with explicit ratios. It opens with the realistic financial-mix (**P-fin**) headline, then the per-operation band characterization (**P-gen**) and FMA. In C, d128 is measured against the Intel **libbid** universal reference plus IBM **decQuad** (DPD) and **libmpdecimal**. It is **data only** — the categories, magnitude profiles, units, and methodology are defined in the [Benchmark Key](key.html) (and, authoritatively, `BenchmarkMatrix.md`). The cross-port d128 band-shape matrices (all ports, no alternatives) live in [Port-Comparison Benchmark Results](port-compare.html); the full index of per-language pages is on the [Benchmarks](/benchmarks.html) hub.

## Summary — Ratio Range by Operation

Each row below is the ratio for that reference library on x86_64 (Intel i9-9880H): `ratio = libbid / Miguel`, `ratio = decQuad / Miguel`, or `ratio = mpdecimal / Miguel` (&gt; 1× ⇒ d128 faster), broken out by operation.

| | Add | Subtract | Multiply | Divide |
|---|---|---|---|---|
| ratio = libbid / Miguel | 3× | 4× | 1.3× – 19× | 0.8× – 1.9× |
| ratio = decQuad / Miguel | 6× | 7× | 1.5× – 22× | 1.6× – 7× |
| ratio = mpdecimal / Miguel | 4× | 5× | 1.0× – 13× | 1.8× – 9× |

## FinMix — realistic financial mix (P-fin)

The headline: one realistic 64-bit financial operation mix — a `MIX` add/sub stream, mul `CP`/`WP`, div `CD`/`WD`/`ET`/`PT` — `ratio = alt / Miguel` (&gt; 1 ⇒ d128 faster). This is the profile closest to real financial code.

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED pfin-rel-c -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | add | MIX | P-fin | arm64 | thru | 1.58 | libbid | 10.72 | **6.78×** | Rc2 |  |
| c | sub | MIX | P-fin | arm64 | thru | 2.07 | libbid | 11.80 | **5.70×** | Rc2 |  |
| c | mul | CP | P-fin | arm64 | thru | 1.33 | libbid | 23.57 | **17.72×** | Rc2 |  |
| c | mul | WP | P-fin | arm64 | thru | 20.54 | libbid | 34.52 | **1.68×** | Rc2 |  |
| c | div | CD | P-fin | arm64 | thru | 30.56 | libbid | 35.07 | **1.15×** | Rc2 |  |
| c | div | WD | P-fin | arm64 | thru | 41.05 | libbid | 40.37 | **0.98×** | Rc2 |  |
| c | div | ET | P-fin | arm64 | thru | 6.34 | libbid | 6.09 | **0.96×** | Rc2 |  |
| c | div | PT | P-fin | arm64 | thru | 3.13 | libbid | 6.09 | **1.95×** | Rc2 |  |
| c | add | MIX | P-fin | arm64 | thru | 1.58 | decQuad | 13.90 | **8.80×** | Rc2 |  |
| c | sub | MIX | P-fin | arm64 | thru | 2.07 | decQuad | 30.55 | **14.76×** | Rc2 |  |
| c | mul | CP | P-fin | arm64 | thru | 1.33 | decQuad | 21.42 | **16.11×** | Rc2 |  |
| c | mul | WP | P-fin | arm64 | thru | 20.54 | decQuad | 26.06 | **1.27×** | Rc2 |  |
| c | div | CD | P-fin | arm64 | thru | 30.56 | decQuad | 73.26 | **2.40×** | Rc2 |  |
| c | div | WD | P-fin | arm64 | thru | 41.05 | decQuad | 122.46 | **2.98×** | Rc2 |  |
| c | div | ET | P-fin | arm64 | thru | 6.34 | decQuad | 41.42 | **6.53×** | Rc2 |  |
| c | div | PT | P-fin | arm64 | thru | 3.13 | decQuad | 39.32 | **12.56×** | Rc2 |  |
| c | add | MIX | P-fin | arm64 | thru | 1.58 | mpdecimal | 13.03 | **8.25×** | Rc2 |  |
| c | sub | MIX | P-fin | arm64 | thru | 2.07 | mpdecimal | 14.20 | **6.86×** | Rc2 |  |
| c | mul | CP | P-fin | arm64 | thru | 1.33 | mpdecimal | 10.35 | **7.78×** | Rc2 |  |
| c | mul | WP | P-fin | arm64 | thru | 20.54 | mpdecimal | 30.01 | **1.46×** | Rc2 |  |
| c | div | CD | P-fin | arm64 | thru | 30.56 | mpdecimal | 62.34 | **2.04×** | Rc2 |  |
| c | div | WD | P-fin | arm64 | thru | 41.05 | mpdecimal | 90.11 | **2.20×** | Rc2 |  |
| c | div | ET | P-fin | arm64 | thru | 6.34 | mpdecimal | 57.78 | **9.11×** | Rc2 |  |
| c | div | PT | P-fin | arm64 | thru | 3.13 | mpdecimal | 45.93 | **14.67×** | Rc2 |  |

<!-- END GENERATED pfin-rel-c -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-c-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | add | MIX | P-fin | x86_64 | thru | 4.46 | libbid | 27.49 | **6.16×** | xRc2 |  |
| c | sub | MIX | P-fin | x86_64 | thru | 5.35 | libbid | 28.61 | **5.35×** | xRc2 |  |
| c | mul | CP | P-fin | x86_64 | thru | 2.38 | libbid | 44.36 | **18.64×** | xRc2 |  |
| c | mul | WP | P-fin | x86_64 | thru | 33.39 | libbid | 57.85 | **1.73×** | xRc2 |  |
| c | div | CD | P-fin | x86_64 | thru | 61.10 | libbid | 74.56 | **1.22×** | xRc2 |  |
| c | div | WD | P-fin | x86_64 | thru | 84.20 | libbid | 80.65 | **0.96×** | xRc2 |  |
| c | div | ET | P-fin | x86_64 | thru | 15.96 | libbid | 19.63 | **1.23×** | xRc2 |  |
| c | div | PT | P-fin | x86_64 | thru | 6.72 | libbid | 19.55 | **2.91×** | xRc2 |  |
| c | add | MIX | P-fin | x86_64 | thru | 4.46 | decQuad | 35.06 | **7.86×** | xRc2 |  |
| c | sub | MIX | P-fin | x86_64 | thru | 5.35 | decQuad | 75.67 | **14.14×** | xRc2 |  |
| c | mul | CP | P-fin | x86_64 | thru | 2.38 | decQuad | 54.63 | **22.95×** | xRc2 |  |
| c | mul | WP | P-fin | x86_64 | thru | 33.39 | decQuad | 68.84 | **2.06×** | xRc2 |  |
| c | div | CD | P-fin | x86_64 | thru | 61.10 | decQuad | 128.79 | **2.11×** | xRc2 |  |
| c | div | WD | P-fin | x86_64 | thru | 84.20 | decQuad | 236.75 | **2.81×** | xRc2 |  |
| c | div | ET | P-fin | x86_64 | thru | 15.96 | decQuad | 71.49 | **4.48×** | xRc2 |  |
| c | div | PT | P-fin | x86_64 | thru | 6.72 | decQuad | 64.31 | **9.57×** | xRc2 |  |
| c | add | MIX | P-fin | x86_64 | thru | 4.46 | mpdecimal | 31.71 | **7.11×** | xRc2 |  |
| c | sub | MIX | P-fin | x86_64 | thru | 5.35 | mpdecimal | 36.64 | **6.85×** | xRc2 |  |
| c | mul | CP | P-fin | x86_64 | thru | 2.38 | mpdecimal | 30.99 | **13.02×** | xRc2 |  |
| c | mul | WP | P-fin | x86_64 | thru | 33.39 | mpdecimal | 42.80 | **1.28×** | xRc2 |  |
| c | div | CD | P-fin | x86_64 | thru | 61.10 | mpdecimal | 152.49 | **2.50×** | xRc2 |  |
| c | div | WD | P-fin | x86_64 | thru | 84.20 | mpdecimal | 272.57 | **3.24×** | xRc2 |  |
| c | div | ET | P-fin | x86_64 | thru | 15.96 | mpdecimal | 134.77 | **8.44×** | xRc2 |  |
| c | div | PT | P-fin | x86_64 | thru | 6.72 | mpdecimal | 90.20 | **13.42×** | xRc2 |  |

<!-- END GENERATED pfin-rel-c-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-c -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | add | SQss | P-gen | arm64 | thru | 0.84 | libbid | 7.96 | **9.48×** | Rc2 |  |
| c | add | SQos | P-gen | arm64 | thru | 2.05 | libbid | 8.69 | **4.24×** | Rc2 |  |
| c | add | NQss | P-gen | arm64 | thru | 3.54 | libbid | 9.36 | **2.64×** | Rc2 |  |
| c | add | NQos | P-gen | arm64 | thru | 4.07 | libbid | 9.78 | **2.40×** | Rc2 |  |
| c | add | MQss | P-gen | arm64 | thru | 5.68 | libbid | 9.75 | **1.72×** | Rc2 |  |
| c | add | MQos | P-gen | arm64 | thru | 9.34 | libbid | 9.71 | **1.04×** | Rc2 |  |
| c | add | OQss | P-gen | arm64 | thru | 11.45 | libbid | 13.66 | **1.19×** | Rc2 |  |
| c | add | OQos | P-gen | arm64 | thru | 16.60 | libbid | 15.31 | **0.92×** | Rc2 |  |
| c | add | FQss | P-gen | arm64 | thru | 8.03 | libbid | 9.32 | **1.16×** | Rc2 |  |
| c | add | FQos | P-gen | arm64 | thru | 10.10 | libbid | 10.38 | **1.03×** | Rc2 |  |
| c | add | SQss | P-gen | arm64 | thru | 0.84 | decQuad | 7.64 | **9.10×** | Rc2 |  |
| c | add | SQos | P-gen | arm64 | thru | 2.05 | decQuad | 33.13 | **16.16×** | Rc2 |  |
| c | add | NQss | P-gen | arm64 | thru | 3.54 | decQuad | 27.01 | **7.63×** | Rc2 |  |
| c | add | NQos | P-gen | arm64 | thru | 4.07 | decQuad | 35.59 | **8.74×** | Rc2 |  |
| c | add | MQss | P-gen | arm64 | thru | 5.68 | decQuad | 24.73 | **4.35×** | Rc2 |  |
| c | add | MQos | P-gen | arm64 | thru | 9.34 | decQuad | 31.37 | **3.36×** | Rc2 |  |
| c | add | OQss | P-gen | arm64 | thru | 11.45 | decQuad | 33.69 | **2.94×** | Rc2 |  |
| c | add | OQos | P-gen | arm64 | thru | 16.60 | decQuad | 37.34 | **2.25×** | Rc2 |  |
| c | add | FQss | P-gen | arm64 | thru | 8.03 | decQuad | 27.06 | **3.37×** | Rc2 |  |
| c | add | FQos | P-gen | arm64 | thru | 10.10 | decQuad | 26.86 | **2.66×** | Rc2 |  |
| c | add | SQss | P-gen | arm64 | thru | 0.84 | mpdecimal | 11.83 | **14.08×** | Rc2 |  |
| c | add | SQos | P-gen | arm64 | thru | 2.05 | mpdecimal | 13.58 | **6.62×** | Rc2 |  |
| c | add | NQss | P-gen | arm64 | thru | 3.54 | mpdecimal | 24.24 | **6.85×** | Rc2 |  |
| c | add | NQos | P-gen | arm64 | thru | 4.07 | mpdecimal | 28.27 | **6.95×** | Rc2 |  |
| c | add | MQss | P-gen | arm64 | thru | 5.68 | mpdecimal | 20.03 | **3.53×** | Rc2 |  |
| c | add | MQos | P-gen | arm64 | thru | 9.34 | mpdecimal | 25.96 | **2.78×** | Rc2 |  |
| c | add | OQss | P-gen | arm64 | thru | 11.45 | mpdecimal | 46.76 | **4.08×** | Rc2 |  |
| c | add | OQos | P-gen | arm64 | thru | 16.60 | mpdecimal | 48.72 | **2.93×** | Rc2 |  |
| c | add | FQss | P-gen | arm64 | thru | 8.03 | mpdecimal | 39.81 | **4.96×** | Rc2 |  |
| c | add | FQos | P-gen | arm64 | thru | 10.10 | mpdecimal | 42.48 | **4.21×** | Rc2 |  |

<!-- END GENERATED add-rel-c -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-c-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | add | SQss | P-gen | x86_64 | thru | 1.58 | libbid | 27.16 | **17.19×** | xRc2 |  |
| c | add | SQos | P-gen | x86_64 | thru | 4.51 | libbid | 25.75 | **5.71×** | xRc2 |  |
| c | add | NQss | P-gen | x86_64 | thru | 9.07 | libbid | 29.03 | **3.20×** | xRc2 |  |
| c | add | NQos | P-gen | x86_64 | thru | 9.15 | libbid | 28.31 | **3.09×** | xRc2 |  |
| c | add | MQss | P-gen | x86_64 | thru | 11.71 | libbid | 27.10 | **2.31×** | xRc2 |  |
| c | add | MQos | P-gen | x86_64 | thru | 22.07 | libbid | 26.84 | **1.22×** | xRc2 |  |
| c | add | OQss | P-gen | x86_64 | thru | 27.08 | libbid | 43.08 | **1.59×** | xRc2 |  |
| c | add | OQos | P-gen | x86_64 | thru | 34.84 | libbid | 43.29 | **1.24×** | xRc2 |  |
| c | add | FQss | P-gen | x86_64 | thru | 17.46 | libbid | 28.98 | **1.66×** | xRc2 |  |
| c | add | FQos | P-gen | x86_64 | thru | 23.49 | libbid | 29.89 | **1.27×** | xRc2 |  |
| c | add | SQss | P-gen | x86_64 | thru | 1.58 | decQuad | 19.50 | **12.34×** | xRc2 |  |
| c | add | SQos | P-gen | x86_64 | thru | 4.51 | decQuad | 78.05 | **17.31×** | xRc2 |  |
| c | add | NQss | P-gen | x86_64 | thru | 9.07 | decQuad | 69.32 | **7.64×** | xRc2 |  |
| c | add | NQos | P-gen | x86_64 | thru | 9.15 | decQuad | 81.43 | **8.90×** | xRc2 |  |
| c | add | MQss | P-gen | x86_64 | thru | 11.71 | decQuad | 66.01 | **5.64×** | xRc2 |  |
| c | add | MQos | P-gen | x86_64 | thru | 22.07 | decQuad | 77.54 | **3.51×** | xRc2 |  |
| c | add | OQss | P-gen | x86_64 | thru | 27.08 | decQuad | 79.84 | **2.95×** | xRc2 |  |
| c | add | OQos | P-gen | x86_64 | thru | 34.84 | decQuad | 86.66 | **2.49×** | xRc2 |  |
| c | add | FQss | P-gen | x86_64 | thru | 17.46 | decQuad | 63.79 | **3.65×** | xRc2 |  |
| c | add | FQos | P-gen | x86_64 | thru | 23.49 | decQuad | 68.62 | **2.92×** | xRc2 |  |
| c | add | SQss | P-gen | x86_64 | thru | 1.58 | mpdecimal | 29.02 | **18.37×** | xRc2 |  |
| c | add | SQos | P-gen | x86_64 | thru | 4.51 | mpdecimal | 33.13 | **7.35×** | xRc2 |  |
| c | add | NQss | P-gen | x86_64 | thru | 9.07 | mpdecimal | 47.48 | **5.23×** | xRc2 |  |
| c | add | NQos | P-gen | x86_64 | thru | 9.15 | mpdecimal | 49.90 | **5.45×** | xRc2 |  |
| c | add | MQss | P-gen | x86_64 | thru | 11.71 | mpdecimal | 47.68 | **4.07×** | xRc2 |  |
| c | add | MQos | P-gen | x86_64 | thru | 22.07 | mpdecimal | 49.54 | **2.24×** | xRc2 |  |
| c | add | OQss | P-gen | x86_64 | thru | 27.08 | mpdecimal | 122.32 | **4.52×** | xRc2 |  |
| c | add | OQos | P-gen | x86_64 | thru | 34.84 | mpdecimal | 123.82 | **3.55×** | xRc2 |  |
| c | add | FQss | P-gen | x86_64 | thru | 17.46 | mpdecimal | 78.83 | **4.51×** | xRc2 |  |
| c | add | FQos | P-gen | x86_64 | thru | 23.49 | mpdecimal | 86.24 | **3.67×** | xRc2 |  |

<!-- END GENERATED add-rel-c-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-c -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | sub | SQss | P-gen | arm64 | thru | 1.51 | libbid | 9.68 | **6.41×** | Rc2 |  |
| c | sub | SQos | P-gen | arm64 | thru | 0.93 | libbid | 10.04 | **10.80×** | Rc2 |  |
| c | sub | NQss | P-gen | arm64 | thru | 4.06 | libbid | 10.87 | **2.68×** | Rc2 |  |
| c | sub | NQos | P-gen | arm64 | thru | 3.46 | libbid | 11.42 | **3.30×** | Rc2 |  |
| c | sub | MQss | P-gen | arm64 | thru | 9.73 | libbid | 9.94 | **1.02×** | Rc2 |  |
| c | sub | MQos | P-gen | arm64 | thru | 5.59 | libbid | 9.78 | **1.75×** | Rc2 |  |
| c | sub | OQss | P-gen | arm64 | thru | 17.20 | libbid | 15.79 | **0.92×** | Rc2 |  |
| c | sub | OQos | P-gen | arm64 | thru | 11.85 | libbid | 14.84 | **1.25×** | Rc2 |  |
| c | sub | FQss | P-gen | arm64 | thru | 10.70 | libbid | 9.39 | **0.88×** | Rc2 |  |
| c | sub | FQos | P-gen | arm64 | thru | 8.95 | libbid | 9.48 | **1.06×** | Rc2 |  |
| c | sub | SQss | P-gen | arm64 | thru | 1.51 | decQuad | 34.54 | **22.87×** | Rc2 |  |
| c | sub | SQos | P-gen | arm64 | thru | 0.93 | decQuad | 8.17 | **8.78×** | Rc2 |  |
| c | sub | NQss | P-gen | arm64 | thru | 4.06 | decQuad | 36.03 | **8.87×** | Rc2 |  |
| c | sub | NQos | P-gen | arm64 | thru | 3.46 | decQuad | 28.26 | **8.17×** | Rc2 |  |
| c | sub | MQss | P-gen | arm64 | thru | 9.73 | decQuad | 33.32 | **3.42×** | Rc2 |  |
| c | sub | MQos | P-gen | arm64 | thru | 5.59 | decQuad | 26.46 | **4.73×** | Rc2 |  |
| c | sub | OQss | P-gen | arm64 | thru | 17.20 | decQuad | 39.30 | **2.28×** | Rc2 |  |
| c | sub | OQos | P-gen | arm64 | thru | 11.85 | decQuad | 34.31 | **2.90×** | Rc2 |  |
| c | sub | FQss | P-gen | arm64 | thru | 10.70 | decQuad | 27.74 | **2.59×** | Rc2 |  |
| c | sub | FQos | P-gen | arm64 | thru | 8.95 | decQuad | 28.82 | **3.22×** | Rc2 |  |
| c | sub | SQss | P-gen | arm64 | thru | 1.51 | mpdecimal | 13.58 | **8.99×** | Rc2 |  |
| c | sub | SQos | P-gen | arm64 | thru | 0.93 | mpdecimal | 11.71 | **12.59×** | Rc2 |  |
| c | sub | NQss | P-gen | arm64 | thru | 4.06 | mpdecimal | 24.31 | **5.99×** | Rc2 |  |
| c | sub | NQos | P-gen | arm64 | thru | 3.46 | mpdecimal | 21.78 | **6.29×** | Rc2 |  |
| c | sub | MQss | P-gen | arm64 | thru | 9.73 | mpdecimal | 25.56 | **2.63×** | Rc2 |  |
| c | sub | MQos | P-gen | arm64 | thru | 5.59 | mpdecimal | 21.03 | **3.76×** | Rc2 |  |
| c | sub | OQss | P-gen | arm64 | thru | 17.20 | mpdecimal | 46.84 | **2.72×** | Rc2 |  |
| c | sub | OQos | P-gen | arm64 | thru | 11.85 | mpdecimal | 45.29 | **3.82×** | Rc2 |  |
| c | sub | FQss | P-gen | arm64 | thru | 10.70 | mpdecimal | 41.97 | **3.92×** | Rc2 |  |
| c | sub | FQos | P-gen | arm64 | thru | 8.95 | mpdecimal | 40.85 | **4.56×** | Rc2 |  |

<!-- END GENERATED sub-rel-c -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-c-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | sub | SQss | P-gen | x86_64 | thru | 3.99 | libbid | 31.21 | **7.82×** | xRc2 |  |
| c | sub | SQos | P-gen | x86_64 | thru | 2.20 | libbid | 29.85 | **13.57×** | xRc2 |  |
| c | sub | NQss | P-gen | x86_64 | thru | 9.81 | libbid | 31.57 | **3.22×** | xRc2 |  |
| c | sub | NQos | P-gen | x86_64 | thru | 9.55 | libbid | 32.24 | **3.38×** | xRc2 |  |
| c | sub | MQss | P-gen | x86_64 | thru | 22.29 | libbid | 30.59 | **1.37×** | xRc2 |  |
| c | sub | MQos | P-gen | x86_64 | thru | 12.03 | libbid | 30.70 | **2.55×** | xRc2 |  |
| c | sub | OQss | P-gen | x86_64 | thru | 34.35 | libbid | 46.61 | **1.36×** | xRc2 |  |
| c | sub | OQos | P-gen | x86_64 | thru | 26.67 | libbid | 46.07 | **1.73×** | xRc2 |  |
| c | sub | FQss | P-gen | x86_64 | thru | 23.86 | libbid | 33.80 | **1.42×** | xRc2 |  |
| c | sub | FQos | P-gen | x86_64 | thru | 17.63 | libbid | 32.91 | **1.87×** | xRc2 |  |
| c | sub | SQss | P-gen | x86_64 | thru | 3.99 | decQuad | 81.91 | **20.53×** | xRc2 |  |
| c | sub | SQos | P-gen | x86_64 | thru | 2.20 | decQuad | 20.49 | **9.31×** | xRc2 |  |
| c | sub | NQss | P-gen | x86_64 | thru | 9.81 | decQuad | 84.72 | **8.64×** | xRc2 |  |
| c | sub | NQos | P-gen | x86_64 | thru | 9.55 | decQuad | 74.00 | **7.75×** | xRc2 |  |
| c | sub | MQss | P-gen | x86_64 | thru | 22.29 | decQuad | 80.90 | **3.63×** | xRc2 |  |
| c | sub | MQos | P-gen | x86_64 | thru | 12.03 | decQuad | 69.86 | **5.81×** | xRc2 |  |
| c | sub | OQss | P-gen | x86_64 | thru | 34.35 | decQuad | 91.64 | **2.67×** | xRc2 |  |
| c | sub | OQos | P-gen | x86_64 | thru | 26.67 | decQuad | 85.82 | **3.22×** | xRc2 |  |
| c | sub | FQss | P-gen | x86_64 | thru | 23.86 | decQuad | 70.83 | **2.97×** | xRc2 |  |
| c | sub | FQos | P-gen | x86_64 | thru | 17.63 | decQuad | 68.83 | **3.90×** | xRc2 |  |
| c | sub | SQss | P-gen | x86_64 | thru | 3.99 | mpdecimal | 32.45 | **8.13×** | xRc2 |  |
| c | sub | SQos | P-gen | x86_64 | thru | 2.20 | mpdecimal | 28.05 | **12.75×** | xRc2 |  |
| c | sub | NQss | P-gen | x86_64 | thru | 9.81 | mpdecimal | 49.40 | **5.04×** | xRc2 |  |
| c | sub | NQos | P-gen | x86_64 | thru | 9.55 | mpdecimal | 47.31 | **4.95×** | xRc2 |  |
| c | sub | MQss | P-gen | x86_64 | thru | 22.29 | mpdecimal | 48.63 | **2.18×** | xRc2 |  |
| c | sub | MQos | P-gen | x86_64 | thru | 12.03 | mpdecimal | 46.51 | **3.87×** | xRc2 |  |
| c | sub | OQss | P-gen | x86_64 | thru | 34.35 | mpdecimal | 122.91 | **3.58×** | xRc2 |  |
| c | sub | OQos | P-gen | x86_64 | thru | 26.67 | mpdecimal | 122.81 | **4.60×** | xRc2 |  |
| c | sub | FQss | P-gen | x86_64 | thru | 23.86 | mpdecimal | 82.93 | **3.48×** | xRc2 |  |
| c | sub | FQos | P-gen | x86_64 | thru | 17.63 | mpdecimal | 78.25 | **4.44×** | xRc2 |  |

<!-- END GENERATED sub-rel-c-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-c -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | mul | CP | P-gen | arm64 | thru | 1.50 | libbid | 23.13 | **15.42×** | Rc2 | **no scaling** — the cheap multiply |
| c | mul | WP | P-gen | arm64 | thru | 20.65 | libbid | 35.06 | **1.70×** | Rc2 | 128-bit recipMulPow10 |
| c | mul | XP | P-gen | arm64 | thru | 25.47 | libbid | 45.24 | **1.78×** | Rc2 | 256-bit recipMulPow10; **1.19× ≈ the recipmul-256 work-order's 1.18–1.54× band** |
| c | mul | CP | P-gen | arm64 | thru | 1.50 | decQuad | 21.33 | **14.22×** | Rc2 | vs DPD |
| c | mul | WP | P-gen | arm64 | thru | 20.65 | decQuad | 27.37 | **1.33×** | Rc2 | vs DPD |
| c | mul | XP | P-gen | arm64 | thru | 25.47 | decQuad | 30.17 | **1.18×** | Rc2 | **decQuad edges d128 on the widest product** (software DPD's flat cost; libbid still slower) |
| c | mul | CP | P-gen | arm64 | thru | 1.50 | mpdecimal | 21.77 | **14.51×** | Rc2 | no-scale multiply vs libmpdec |
| c | mul | WP | P-gen | arm64 | thru | 20.65 | mpdecimal | 53.31 | **2.58×** | Rc2 | 128-bit recipMulPow10 |
| c | mul | XP | P-gen | arm64 | thru | 25.47 | mpdecimal | 73.49 | **2.89×** | Rc2 | **d128 wins the widest product vs libmpdec** (unlike decQuad) |

<!-- END GENERATED mul-rel-c -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-c-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | mul | CP | P-gen | x86_64 | thru | 3.36 | libbid | 45.57 | **13.56×** | xRc2 |  |
| c | mul | WP | P-gen | x86_64 | thru | 33.58 | libbid | 64.59 | **1.92×** | xRc2 |  |
| c | mul | XP | P-gen | x86_64 | thru | 43.09 | libbid | 93.63 | **2.17×** | xRc2 |  |
| c | mul | CP | P-gen | x86_64 | thru | 3.36 | decQuad | 56.46 | **16.80×** | xRc2 |  |
| c | mul | WP | P-gen | x86_64 | thru | 33.58 | decQuad | 72.86 | **2.17×** | xRc2 |  |
| c | mul | XP | P-gen | x86_64 | thru | 43.09 | decQuad | 88.62 | **2.06×** | xRc2 |  |
| c | mul | CP | P-gen | x86_64 | thru | 3.36 | mpdecimal | 61.42 | **18.28×** | xRc2 |  |
| c | mul | WP | P-gen | x86_64 | thru | 33.58 | mpdecimal | 180.93 | **5.39×** | xRc2 |  |
| c | mul | XP | P-gen | x86_64 | thru | 43.09 | mpdecimal | 227.84 | **5.29×** | xRc2 |  |

<!-- END GENERATED mul-rel-c-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-c -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | div | CD | P-gen | arm64 | thru | 28.50 | libbid | 36.77 | **1.29×** | Rc2 | 128÷64 quotient-first (§2.4.10); **libbid wins** — the compact-divide weakness persists |
| c | div | WD | P-gen | arm64 | thru | 37.47 | libbid | 37.54 | **1.00×** | Rc2 | 256÷64; **≈ parity / slight loss** |
| c | div | XD | P-gen | arm64 | thru | 32.73 | libbid | 38.97 | **1.19×** | Rc2 | 256÷128 Möller–Granlund |
| c | div | ET | P-gen | arm64 | thru | 8.24 | libbid | 11.68 | **1.42×** | Rc2 | **quotient-first exact early-out** — beats libbid's exact fast path |
| c | div | PT | P-gen | arm64 | thru | 3.12 | libbid | 11.45 | **3.67×** | Rc2 | `divPow10Divisor` (§2.4.9); **d128's fastest divide** (coeff-1 form) |
| c | div | CD | P-gen | arm64 | thru | 28.50 | decQuad | 71.29 | **2.50×** | Rc2 | vs DPD |
| c | div | WD | P-gen | arm64 | thru | 37.47 | decQuad | 116.34 | **3.10×** | Rc2 | vs DPD |
| c | div | XD | P-gen | arm64 | thru | 32.73 | decQuad | 173.67 | **5.31×** | Rc2 | vs DPD — decNumber divide is slow |
| c | div | ET | P-gen | arm64 | thru | 8.24 | decQuad | 48.44 | **5.88×** | Rc2 | vs DPD |
| c | div | PT | P-gen | arm64 | thru | 3.12 | decQuad | 44.50 | **14.26×** | Rc2 | vs DPD |
| c | div | CD | P-gen | arm64 | thru | 28.50 | mpdecimal | 61.20 | **2.15×** | Rc2 | **narrowest divide gap** (libmpdec's compact divide is its cheapest, like d128's weakness) |
| c | div | WD | P-gen | arm64 | thru | 37.47 | mpdecimal | 90.34 | **2.41×** | Rc2 | 256÷64 |
| c | div | XD | P-gen | arm64 | thru | 32.73 | mpdecimal | 141.26 | **4.32×** | Rc2 | Cowlishaw signature (CD 59 < WD 87 < XD 144) |
| c | div | ET | P-gen | arm64 | thru | 8.24 | mpdecimal | 61.67 | **7.48×** | Rc2 | libmpdec has no exact early-out |
| c | div | PT | P-gen | arm64 | thru | 3.12 | mpdecimal | 51.52 | **16.51×** | Rc2 | **d128's biggest divide win vs libmpdec** |

<!-- END GENERATED div-rel-c -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-c-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | div | CD | P-gen | x86_64 | thru | 72.13 | libbid | 81.20 | **1.13×** | xRc2 |  |
| c | div | WD | P-gen | x86_64 | thru | 85.25 | libbid | 82.98 | **0.97×** | xRc2 |  |
| c | div | XD | P-gen | x86_64 | thru | 74.22 | libbid | 82.60 | **1.11×** | xRc2 |  |
| c | div | ET | P-gen | x86_64 | thru | 25.89 | libbid | 29.87 | **1.15×** | xRc2 |  |
| c | div | PT | P-gen | x86_64 | thru | 6.75 | libbid | 30.17 | **4.47×** | xRc2 |  |
| c | div | CD | P-gen | x86_64 | thru | 72.13 | decQuad | 137.73 | **1.91×** | xRc2 |  |
| c | div | WD | P-gen | x86_64 | thru | 85.25 | decQuad | 241.90 | **2.84×** | xRc2 |  |
| c | div | XD | P-gen | x86_64 | thru | 74.22 | decQuad | 390.12 | **5.26×** | xRc2 |  |
| c | div | ET | P-gen | x86_64 | thru | 25.89 | decQuad | 95.47 | **3.69×** | xRc2 |  |
| c | div | PT | P-gen | x86_64 | thru | 6.75 | decQuad | 82.40 | **12.21×** | xRc2 |  |
| c | div | CD | P-gen | x86_64 | thru | 72.13 | mpdecimal | 160.39 | **2.22×** | xRc2 |  |
| c | div | WD | P-gen | x86_64 | thru | 85.25 | mpdecimal | 276.46 | **3.24×** | xRc2 |  |
| c | div | XD | P-gen | x86_64 | thru | 74.22 | mpdecimal | 353.54 | **4.76×** | xRc2 |  |
| c | div | ET | P-gen | x86_64 | thru | 25.89 | mpdecimal | 154.18 | **5.96×** | xRc2 |  |
| c | div | PT | P-gen | x86_64 | thru | 6.75 | mpdecimal | 101.13 | **14.98×** | xRc2 |  |

<!-- END GENERATED div-rel-c-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-c -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | fma | FN | FMA | arm64 | thru | 76.24 | libbid | 82.83 | **1.09×** | Rc2 |  |
| c | fma | FF | FMA | arm64 | thru | 39.70 | libbid | 58.46 | **1.47×** | Rc2 |  |
| c | fma | FN | FMA | arm64 | thru | 76.24 | decQuad | 61.70 | **0.81×** | Rc2 |  |
| c | fma | FF | FMA | arm64 | thru | 39.70 | decQuad | 72.91 | **1.84×** | Rc2 |  |
| c | fma | FN | FMA | arm64 | thru | 76.24 | mpdecimal | 89.49 | **1.17×** | Rc2 |  |
| c | fma | FF | FMA | arm64 | thru | 39.70 | mpdecimal | 154.27 | **3.89×** | Rc2 |  |

<!-- END GENERATED fma-rel-c -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-c-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | fma | FN | FMA | x86_64 | thru | 114.77 | libbid | 155.17 | **1.35×** | xRc2 |  |
| c | fma | FF | FMA | x86_64 | thru | 72.99 | libbid | 119.14 | **1.63×** | xRc2 |  |
| c | fma | FN | FMA | x86_64 | thru | 114.77 | decQuad | 141.79 | **1.24×** | xRc2 |  |
| c | fma | FF | FMA | x86_64 | thru | 72.99 | decQuad | 149.72 | **2.05×** | xRc2 |  |
| c | fma | FN | FMA | x86_64 | thru | 114.77 | mpdecimal | 253.96 | **2.21×** | xRc2 |  |
| c | fma | FF | FMA | x86_64 | thru | 72.99 | mpdecimal | 331.53 | **4.54×** | xRc2 |  |

<!-- END GENERATED fma-rel-c-x86 -->

</div>
