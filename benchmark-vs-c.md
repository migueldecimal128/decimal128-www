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
| c | add | MIX | P-fin | x86_64 | thru | 4.96 | libbid | 30.56 | **6.16×** | xRc2 |  |
| c | sub | MIX | P-fin | x86_64 | thru | 5.92 | libbid | 31.87 | **5.38×** | xRc2 |  |
| c | mul | CP | P-fin | x86_64 | thru | 2.82 | libbid | 50.91 | **18.05×** | xRc2 |  |
| c | mul | WP | P-fin | x86_64 | thru | 38.05 | libbid | 66.63 | **1.75×** | xRc2 |  |
| c | div | CD | P-fin | x86_64 | thru | 66.61 | libbid | 82.11 | **1.23×** | xRc2 |  |
| c | div | WD | P-fin | x86_64 | thru | 94.04 | libbid | 86.90 | **0.92×** | xRc2 |  |
| c | div | ET | P-fin | x86_64 | thru | 17.24 | libbid | 21.25 | **1.23×** | xRc2 |  |
| c | div | PT | P-fin | x86_64 | thru | 7.51 | libbid | 21.42 | **2.85×** | xRc2 |  |
| c | add | MIX | P-fin | x86_64 | thru | 4.96 | decQuad | 39.88 | **8.04×** | xRc2 |  |
| c | sub | MIX | P-fin | x86_64 | thru | 5.92 | decQuad | 86.38 | **14.59×** | xRc2 |  |
| c | mul | CP | P-fin | x86_64 | thru | 2.82 | decQuad | 61.25 | **21.72×** | xRc2 |  |
| c | mul | WP | P-fin | x86_64 | thru | 38.05 | decQuad | 76.73 | **2.02×** | xRc2 |  |
| c | div | CD | P-fin | x86_64 | thru | 66.61 | decQuad | 147.02 | **2.21×** | xRc2 |  |
| c | div | WD | P-fin | x86_64 | thru | 94.04 | decQuad | 265.55 | **2.82×** | xRc2 |  |
| c | div | ET | P-fin | x86_64 | thru | 17.24 | decQuad | 81.75 | **4.74×** | xRc2 |  |
| c | div | PT | P-fin | x86_64 | thru | 7.51 | decQuad | 73.24 | **9.75×** | xRc2 |  |
| c | add | MIX | P-fin | x86_64 | thru | 4.96 | mpdecimal | 35.65 | **7.19×** | xRc2 |  |
| c | sub | MIX | P-fin | x86_64 | thru | 5.92 | mpdecimal | 40.06 | **6.77×** | xRc2 |  |
| c | mul | CP | P-fin | x86_64 | thru | 2.82 | mpdecimal | 34.58 | **12.26×** | xRc2 |  |
| c | mul | WP | P-fin | x86_64 | thru | 38.05 | mpdecimal | 47.63 | **1.25×** | xRc2 |  |
| c | div | CD | P-fin | x86_64 | thru | 66.61 | mpdecimal | 169.56 | **2.55×** | xRc2 |  |
| c | div | WD | P-fin | x86_64 | thru | 94.04 | mpdecimal | 297.68 | **3.17×** | xRc2 |  |
| c | div | ET | P-fin | x86_64 | thru | 17.24 | mpdecimal | 151.08 | **8.76×** | xRc2 |  |
| c | div | PT | P-fin | x86_64 | thru | 7.51 | mpdecimal | 105.39 | **14.03×** | xRc2 |  |

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
| c | add | SQss | P-gen | x86_64 | thru | 2.28 | libbid | 30.12 | **13.21×** | xRc2 |  |
| c | add | SQos | P-gen | x86_64 | thru | 5.09 | libbid | 27.81 | **5.46×** | xRc2 |  |
| c | add | NQss | P-gen | x86_64 | thru | 10.13 | libbid | 31.74 | **3.13×** | xRc2 |  |
| c | add | NQos | P-gen | x86_64 | thru | 10.32 | libbid | 30.17 | **2.92×** | xRc2 |  |
| c | add | MQss | P-gen | x86_64 | thru | 13.01 | libbid | 29.55 | **2.27×** | xRc2 |  |
| c | add | MQos | P-gen | x86_64 | thru | 24.27 | libbid | 28.78 | **1.19×** | xRc2 |  |
| c | add | OQss | P-gen | x86_64 | thru | 30.45 | libbid | 46.76 | **1.54×** | xRc2 |  |
| c | add | OQos | P-gen | x86_64 | thru | 38.89 | libbid | 47.44 | **1.22×** | xRc2 |  |
| c | add | FQss | P-gen | x86_64 | thru | 19.46 | libbid | 33.02 | **1.70×** | xRc2 |  |
| c | add | FQos | P-gen | x86_64 | thru | 26.44 | libbid | 32.54 | **1.23×** | xRc2 |  |
| c | add | SQss | P-gen | x86_64 | thru | 2.28 | decQuad | 21.23 | **9.31×** | xRc2 |  |
| c | add | SQos | P-gen | x86_64 | thru | 5.09 | decQuad | 87.00 | **17.09×** | xRc2 |  |
| c | add | NQss | P-gen | x86_64 | thru | 10.13 | decQuad | 75.37 | **7.44×** | xRc2 |  |
| c | add | NQos | P-gen | x86_64 | thru | 10.32 | decQuad | 91.17 | **8.83×** | xRc2 |  |
| c | add | MQss | P-gen | x86_64 | thru | 13.01 | decQuad | 71.37 | **5.49×** | xRc2 |  |
| c | add | MQos | P-gen | x86_64 | thru | 24.27 | decQuad | 85.48 | **3.52×** | xRc2 |  |
| c | add | OQss | P-gen | x86_64 | thru | 30.45 | decQuad | 87.09 | **2.86×** | xRc2 |  |
| c | add | OQos | P-gen | x86_64 | thru | 38.89 | decQuad | 100.65 | **2.59×** | xRc2 |  |
| c | add | FQss | P-gen | x86_64 | thru | 19.46 | decQuad | 71.68 | **3.68×** | xRc2 |  |
| c | add | FQos | P-gen | x86_64 | thru | 26.44 | decQuad | 76.01 | **2.87×** | xRc2 |  |
| c | add | SQss | P-gen | x86_64 | thru | 2.28 | mpdecimal | 31.16 | **13.67×** | xRc2 |  |
| c | add | SQos | P-gen | x86_64 | thru | 5.09 | mpdecimal | 35.74 | **7.02×** | xRc2 |  |
| c | add | NQss | P-gen | x86_64 | thru | 10.13 | mpdecimal | 52.39 | **5.17×** | xRc2 |  |
| c | add | NQos | P-gen | x86_64 | thru | 10.32 | mpdecimal | 54.55 | **5.29×** | xRc2 |  |
| c | add | MQss | P-gen | x86_64 | thru | 13.01 | mpdecimal | 52.10 | **4.00×** | xRc2 |  |
| c | add | MQos | P-gen | x86_64 | thru | 24.27 | mpdecimal | 53.88 | **2.22×** | xRc2 |  |
| c | add | OQss | P-gen | x86_64 | thru | 30.45 | mpdecimal | 136.07 | **4.47×** | xRc2 |  |
| c | add | OQos | P-gen | x86_64 | thru | 38.89 | mpdecimal | 144.17 | **3.71×** | xRc2 |  |
| c | add | FQss | P-gen | x86_64 | thru | 19.46 | mpdecimal | 92.14 | **4.73×** | xRc2 |  |
| c | add | FQos | P-gen | x86_64 | thru | 26.44 | mpdecimal | 96.21 | **3.64×** | xRc2 |  |

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
| c | sub | SQss | P-gen | x86_64 | thru | 4.57 | libbid | 33.73 | **7.38×** | xRc2 |  |
| c | sub | SQos | P-gen | x86_64 | thru | 2.32 | libbid | 32.99 | **14.22×** | xRc2 |  |
| c | sub | NQss | P-gen | x86_64 | thru | 10.94 | libbid | 34.85 | **3.19×** | xRc2 |  |
| c | sub | NQos | P-gen | x86_64 | thru | 10.72 | libbid | 35.61 | **3.32×** | xRc2 |  |
| c | sub | MQss | P-gen | x86_64 | thru | 24.68 | libbid | 34.98 | **1.42×** | xRc2 |  |
| c | sub | MQos | P-gen | x86_64 | thru | 13.60 | libbid | 34.66 | **2.55×** | xRc2 |  |
| c | sub | OQss | P-gen | x86_64 | thru | 38.90 | libbid | 51.72 | **1.33×** | xRc2 |  |
| c | sub | OQos | P-gen | x86_64 | thru | 30.00 | libbid | 50.81 | **1.69×** | xRc2 |  |
| c | sub | FQss | P-gen | x86_64 | thru | 26.63 | libbid | 37.25 | **1.40×** | xRc2 |  |
| c | sub | FQos | P-gen | x86_64 | thru | 20.62 | libbid | 36.53 | **1.77×** | xRc2 |  |
| c | sub | SQss | P-gen | x86_64 | thru | 4.57 | decQuad | 92.66 | **20.28×** | xRc2 |  |
| c | sub | SQos | P-gen | x86_64 | thru | 2.32 | decQuad | 23.06 | **9.94×** | xRc2 |  |
| c | sub | NQss | P-gen | x86_64 | thru | 10.94 | decQuad | 95.80 | **8.76×** | xRc2 |  |
| c | sub | NQos | P-gen | x86_64 | thru | 10.72 | decQuad | 81.60 | **7.61×** | xRc2 |  |
| c | sub | MQss | P-gen | x86_64 | thru | 24.68 | decQuad | 92.74 | **3.76×** | xRc2 |  |
| c | sub | MQos | P-gen | x86_64 | thru | 13.60 | decQuad | 78.14 | **5.75×** | xRc2 |  |
| c | sub | OQss | P-gen | x86_64 | thru | 38.90 | decQuad | 103.86 | **2.67×** | xRc2 |  |
| c | sub | OQos | P-gen | x86_64 | thru | 30.00 | decQuad | 92.53 | **3.08×** | xRc2 |  |
| c | sub | FQss | P-gen | x86_64 | thru | 26.63 | decQuad | 79.07 | **2.97×** | xRc2 |  |
| c | sub | FQos | P-gen | x86_64 | thru | 20.62 | decQuad | 76.85 | **3.73×** | xRc2 |  |
| c | sub | SQss | P-gen | x86_64 | thru | 4.57 | mpdecimal | 36.53 | **7.99×** | xRc2 |  |
| c | sub | SQos | P-gen | x86_64 | thru | 2.32 | mpdecimal | 31.62 | **13.63×** | xRc2 |  |
| c | sub | NQss | P-gen | x86_64 | thru | 10.94 | mpdecimal | 55.56 | **5.08×** | xRc2 |  |
| c | sub | NQos | P-gen | x86_64 | thru | 10.72 | mpdecimal | 52.92 | **4.94×** | xRc2 |  |
| c | sub | MQss | P-gen | x86_64 | thru | 24.68 | mpdecimal | 55.14 | **2.23×** | xRc2 |  |
| c | sub | MQos | P-gen | x86_64 | thru | 13.60 | mpdecimal | 53.58 | **3.94×** | xRc2 |  |
| c | sub | OQss | P-gen | x86_64 | thru | 38.90 | mpdecimal | 139.81 | **3.59×** | xRc2 |  |
| c | sub | OQos | P-gen | x86_64 | thru | 30.00 | mpdecimal | 138.05 | **4.60×** | xRc2 |  |
| c | sub | FQss | P-gen | x86_64 | thru | 26.63 | mpdecimal | 94.19 | **3.54×** | xRc2 |  |
| c | sub | FQos | P-gen | x86_64 | thru | 20.62 | mpdecimal | 90.62 | **4.39×** | xRc2 |  |

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
| c | mul | CP | P-gen | x86_64 | thru | 3.86 | libbid | 50.55 | **13.10×** | xRc2 |  |
| c | mul | WP | P-gen | x86_64 | thru | 37.34 | libbid | 73.62 | **1.97×** | xRc2 |  |
| c | mul | XP | P-gen | x86_64 | thru | 47.91 | libbid | 104.96 | **2.19×** | xRc2 |  |
| c | mul | CP | P-gen | x86_64 | thru | 3.86 | decQuad | 61.15 | **15.84×** | xRc2 |  |
| c | mul | WP | P-gen | x86_64 | thru | 37.34 | decQuad | 80.41 | **2.15×** | xRc2 |  |
| c | mul | XP | P-gen | x86_64 | thru | 47.91 | decQuad | 96.83 | **2.02×** | xRc2 |  |
| c | mul | CP | P-gen | x86_64 | thru | 3.86 | mpdecimal | 68.97 | **17.87×** | xRc2 |  |
| c | mul | WP | P-gen | x86_64 | thru | 37.34 | mpdecimal | 201.04 | **5.38×** | xRc2 |  |
| c | mul | XP | P-gen | x86_64 | thru | 47.91 | mpdecimal | 244.70 | **5.11×** | xRc2 |  |

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
| c | div | CD | P-gen | x86_64 | thru | 75.71 | libbid | 86.65 | **1.14×** | xRc2 |  |
| c | div | WD | P-gen | x86_64 | thru | 92.95 | libbid | 88.12 | **0.95×** | xRc2 |  |
| c | div | XD | P-gen | x86_64 | thru | 81.39 | libbid | 88.89 | **1.09×** | xRc2 |  |
| c | div | ET | P-gen | x86_64 | thru | 27.78 | libbid | 31.98 | **1.15×** | xRc2 |  |
| c | div | PT | P-gen | x86_64 | thru | 7.41 | libbid | 32.28 | **4.36×** | xRc2 |  |
| c | div | CD | P-gen | x86_64 | thru | 75.71 | decQuad | 152.28 | **2.01×** | xRc2 |  |
| c | div | WD | P-gen | x86_64 | thru | 92.95 | decQuad | 268.83 | **2.89×** | xRc2 |  |
| c | div | XD | P-gen | x86_64 | thru | 81.39 | decQuad | 432.16 | **5.31×** | xRc2 |  |
| c | div | ET | P-gen | x86_64 | thru | 27.78 | decQuad | 107.02 | **3.85×** | xRc2 |  |
| c | div | PT | P-gen | x86_64 | thru | 7.41 | decQuad | 90.81 | **12.26×** | xRc2 |  |
| c | div | CD | P-gen | x86_64 | thru | 75.71 | mpdecimal | 173.43 | **2.29×** | xRc2 |  |
| c | div | WD | P-gen | x86_64 | thru | 92.95 | mpdecimal | 301.84 | **3.25×** | xRc2 |  |
| c | div | XD | P-gen | x86_64 | thru | 81.39 | mpdecimal | 384.11 | **4.72×** | xRc2 |  |
| c | div | ET | P-gen | x86_64 | thru | 27.78 | mpdecimal | 171.97 | **6.19×** | xRc2 |  |
| c | div | PT | P-gen | x86_64 | thru | 7.41 | mpdecimal | 113.34 | **15.30×** | xRc2 |  |

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
| c | fma | FN | FMA | x86_64 | thru | 130.67 | libbid | 176.51 | **1.35×** | xRc2 |  |
| c | fma | FF | FMA | x86_64 | thru | 83.43 | libbid | 135.93 | **1.63×** | xRc2 |  |
| c | fma | FN | FMA | x86_64 | thru | 130.67 | decQuad | 159.73 | **1.22×** | xRc2 |  |
| c | fma | FF | FMA | x86_64 | thru | 83.43 | decQuad | 168.32 | **2.02×** | xRc2 |  |
| c | fma | FN | FMA | x86_64 | thru | 130.67 | mpdecimal | 285.81 | **2.19×** | xRc2 |  |
| c | fma | FF | FMA | x86_64 | thru | 83.43 | mpdecimal | 372.25 | **4.46×** | xRc2 |  |

<!-- END GENERATED fma-rel-c-x86 -->

</div>
