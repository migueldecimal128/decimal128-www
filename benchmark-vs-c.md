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
| c | add | MIX | P-fin | x86_64 | thru | 4.40 | libbid | 27.35 | **6.22×** | xRc2 |  |
| c | sub | MIX | P-fin | x86_64 | thru | 5.21 | libbid | 28.89 | **5.55×** | xRc2 |  |
| c | mul | CP | P-fin | x86_64 | thru | 2.39 | libbid | 44.35 | **18.56×** | xRc2 |  |
| c | mul | WP | P-fin | x86_64 | thru | 33.35 | libbid | 57.75 | **1.73×** | xRc2 |  |
| c | div | CD | P-fin | x86_64 | thru | 60.89 | libbid | 74.27 | **1.22×** | xRc2 |  |
| c | div | WD | P-fin | x86_64 | thru | 83.16 | libbid | 79.07 | **0.95×** | xRc2 |  |
| c | div | ET | P-fin | x86_64 | thru | 15.68 | libbid | 18.88 | **1.20×** | xRc2 |  |
| c | div | PT | P-fin | x86_64 | thru | 6.64 | libbid | 19.10 | **2.88×** | xRc2 |  |
| c | add | MIX | P-fin | x86_64 | thru | 4.40 | decQuad | 34.70 | **7.89×** | xRc2 |  |
| c | sub | MIX | P-fin | x86_64 | thru | 5.21 | decQuad | 75.53 | **14.50×** | xRc2 |  |
| c | mul | CP | P-fin | x86_64 | thru | 2.39 | decQuad | 54.38 | **22.75×** | xRc2 |  |
| c | mul | WP | P-fin | x86_64 | thru | 33.35 | decQuad | 68.77 | **2.06×** | xRc2 |  |
| c | div | CD | P-fin | x86_64 | thru | 60.89 | decQuad | 128.03 | **2.10×** | xRc2 |  |
| c | div | WD | P-fin | x86_64 | thru | 83.16 | decQuad | 233.67 | **2.81×** | xRc2 |  |
| c | div | ET | P-fin | x86_64 | thru | 15.68 | decQuad | 70.53 | **4.50×** | xRc2 |  |
| c | div | PT | P-fin | x86_64 | thru | 6.64 | decQuad | 63.46 | **9.56×** | xRc2 |  |
| c | add | MIX | P-fin | x86_64 | thru | 4.40 | mpdecimal | 32.01 | **7.27×** | xRc2 |  |
| c | sub | MIX | P-fin | x86_64 | thru | 5.21 | mpdecimal | 35.57 | **6.83×** | xRc2 |  |
| c | mul | CP | P-fin | x86_64 | thru | 2.39 | mpdecimal | 30.73 | **12.86×** | xRc2 |  |
| c | mul | WP | P-fin | x86_64 | thru | 33.35 | mpdecimal | 42.62 | **1.28×** | xRc2 |  |
| c | div | CD | P-fin | x86_64 | thru | 60.89 | mpdecimal | 150.65 | **2.47×** | xRc2 |  |
| c | div | WD | P-fin | x86_64 | thru | 83.16 | mpdecimal | 267.35 | **3.21×** | xRc2 |  |
| c | div | ET | P-fin | x86_64 | thru | 15.68 | mpdecimal | 132.52 | **8.45×** | xRc2 |  |
| c | div | PT | P-fin | x86_64 | thru | 6.64 | mpdecimal | 88.93 | **13.39×** | xRc2 |  |

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
| c | add | SQss | P-gen | x86_64 | thru | 2.03 | libbid | 27.04 | **13.32×** | xRc2 |  |
| c | add | SQos | P-gen | x86_64 | thru | 4.47 | libbid | 25.59 | **5.72×** | xRc2 |  |
| c | add | NQss | P-gen | x86_64 | thru | 9.00 | libbid | 29.04 | **3.23×** | xRc2 |  |
| c | add | NQos | P-gen | x86_64 | thru | 9.18 | libbid | 28.25 | **3.08×** | xRc2 |  |
| c | add | MQss | P-gen | x86_64 | thru | 11.72 | libbid | 27.26 | **2.33×** | xRc2 |  |
| c | add | MQos | P-gen | x86_64 | thru | 22.04 | libbid | 27.12 | **1.23×** | xRc2 |  |
| c | add | OQss | P-gen | x86_64 | thru | 27.31 | libbid | 42.96 | **1.57×** | xRc2 |  |
| c | add | OQos | P-gen | x86_64 | thru | 35.26 | libbid | 43.17 | **1.22×** | xRc2 |  |
| c | add | FQss | P-gen | x86_64 | thru | 17.65 | libbid | 29.28 | **1.66×** | xRc2 |  |
| c | add | FQos | P-gen | x86_64 | thru | 23.89 | libbid | 29.32 | **1.23×** | xRc2 |  |
| c | add | SQss | P-gen | x86_64 | thru | 2.03 | decQuad | 19.24 | **9.48×** | xRc2 |  |
| c | add | SQos | P-gen | x86_64 | thru | 4.47 | decQuad | 78.00 | **17.45×** | xRc2 |  |
| c | add | NQss | P-gen | x86_64 | thru | 9.00 | decQuad | 69.17 | **7.69×** | xRc2 |  |
| c | add | NQos | P-gen | x86_64 | thru | 9.18 | decQuad | 80.87 | **8.81×** | xRc2 |  |
| c | add | MQss | P-gen | x86_64 | thru | 11.72 | decQuad | 68.21 | **5.82×** | xRc2 |  |
| c | add | MQos | P-gen | x86_64 | thru | 22.04 | decQuad | 77.00 | **3.49×** | xRc2 |  |
| c | add | OQss | P-gen | x86_64 | thru | 27.31 | decQuad | 79.30 | **2.90×** | xRc2 |  |
| c | add | OQos | P-gen | x86_64 | thru | 35.26 | decQuad | 87.50 | **2.48×** | xRc2 |  |
| c | add | FQss | P-gen | x86_64 | thru | 17.65 | decQuad | 64.20 | **3.64×** | xRc2 |  |
| c | add | FQos | P-gen | x86_64 | thru | 23.89 | decQuad | 65.66 | **2.75×** | xRc2 |  |
| c | add | SQss | P-gen | x86_64 | thru | 2.03 | mpdecimal | 28.14 | **13.86×** | xRc2 |  |
| c | add | SQos | P-gen | x86_64 | thru | 4.47 | mpdecimal | 32.52 | **7.28×** | xRc2 |  |
| c | add | NQss | P-gen | x86_64 | thru | 9.00 | mpdecimal | 47.60 | **5.29×** | xRc2 |  |
| c | add | NQos | P-gen | x86_64 | thru | 9.18 | mpdecimal | 50.11 | **5.46×** | xRc2 |  |
| c | add | MQss | P-gen | x86_64 | thru | 11.72 | mpdecimal | 48.01 | **4.10×** | xRc2 |  |
| c | add | MQos | P-gen | x86_64 | thru | 22.04 | mpdecimal | 49.40 | **2.24×** | xRc2 |  |
| c | add | OQss | P-gen | x86_64 | thru | 27.31 | mpdecimal | 122.30 | **4.48×** | xRc2 |  |
| c | add | OQos | P-gen | x86_64 | thru | 35.26 | mpdecimal | 123.98 | **3.52×** | xRc2 |  |
| c | add | FQss | P-gen | x86_64 | thru | 17.65 | mpdecimal | 79.13 | **4.48×** | xRc2 |  |
| c | add | FQos | P-gen | x86_64 | thru | 23.89 | mpdecimal | 83.49 | **3.49×** | xRc2 |  |

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
| c | sub | SQss | P-gen | x86_64 | thru | 4.05 | libbid | 30.07 | **7.42×** | xRc2 |  |
| c | sub | SQos | P-gen | x86_64 | thru | 2.02 | libbid | 30.04 | **14.87×** | xRc2 |  |
| c | sub | NQss | P-gen | x86_64 | thru | 9.87 | libbid | 31.79 | **3.22×** | xRc2 |  |
| c | sub | NQos | P-gen | x86_64 | thru | 9.59 | libbid | 32.49 | **3.39×** | xRc2 |  |
| c | sub | MQss | P-gen | x86_64 | thru | 22.44 | libbid | 30.94 | **1.38×** | xRc2 |  |
| c | sub | MQos | P-gen | x86_64 | thru | 12.16 | libbid | 30.85 | **2.54×** | xRc2 |  |
| c | sub | OQss | P-gen | x86_64 | thru | 34.57 | libbid | 46.20 | **1.34×** | xRc2 |  |
| c | sub | OQos | P-gen | x86_64 | thru | 26.66 | libbid | 45.86 | **1.72×** | xRc2 |  |
| c | sub | FQss | P-gen | x86_64 | thru | 23.82 | libbid | 33.24 | **1.40×** | xRc2 |  |
| c | sub | FQos | P-gen | x86_64 | thru | 17.66 | libbid | 32.74 | **1.85×** | xRc2 |  |
| c | sub | SQss | P-gen | x86_64 | thru | 4.05 | decQuad | 82.49 | **20.37×** | xRc2 |  |
| c | sub | SQos | P-gen | x86_64 | thru | 2.02 | decQuad | 20.68 | **10.24×** | xRc2 |  |
| c | sub | NQss | P-gen | x86_64 | thru | 9.87 | decQuad | 87.15 | **8.83×** | xRc2 |  |
| c | sub | NQos | P-gen | x86_64 | thru | 9.59 | decQuad | 74.22 | **7.74×** | xRc2 |  |
| c | sub | MQss | P-gen | x86_64 | thru | 22.44 | decQuad | 81.12 | **3.61×** | xRc2 |  |
| c | sub | MQos | P-gen | x86_64 | thru | 12.16 | decQuad | 69.84 | **5.74×** | xRc2 |  |
| c | sub | OQss | P-gen | x86_64 | thru | 34.57 | decQuad | 90.98 | **2.63×** | xRc2 |  |
| c | sub | OQos | P-gen | x86_64 | thru | 26.66 | decQuad | 82.99 | **3.11×** | xRc2 |  |
| c | sub | FQss | P-gen | x86_64 | thru | 23.82 | decQuad | 69.34 | **2.91×** | xRc2 |  |
| c | sub | FQos | P-gen | x86_64 | thru | 17.66 | decQuad | 68.94 | **3.90×** | xRc2 |  |
| c | sub | SQss | P-gen | x86_64 | thru | 4.05 | mpdecimal | 32.75 | **8.09×** | xRc2 |  |
| c | sub | SQos | P-gen | x86_64 | thru | 2.02 | mpdecimal | 28.26 | **13.99×** | xRc2 |  |
| c | sub | NQss | P-gen | x86_64 | thru | 9.87 | mpdecimal | 49.51 | **5.02×** | xRc2 |  |
| c | sub | NQos | P-gen | x86_64 | thru | 9.59 | mpdecimal | 47.19 | **4.92×** | xRc2 |  |
| c | sub | MQss | P-gen | x86_64 | thru | 22.44 | mpdecimal | 48.37 | **2.16×** | xRc2 |  |
| c | sub | MQos | P-gen | x86_64 | thru | 12.16 | mpdecimal | 46.82 | **3.85×** | xRc2 |  |
| c | sub | OQss | P-gen | x86_64 | thru | 34.57 | mpdecimal | 122.76 | **3.55×** | xRc2 |  |
| c | sub | OQos | P-gen | x86_64 | thru | 26.66 | mpdecimal | 121.11 | **4.54×** | xRc2 |  |
| c | sub | FQss | P-gen | x86_64 | thru | 23.82 | mpdecimal | 82.01 | **3.44×** | xRc2 |  |
| c | sub | FQos | P-gen | x86_64 | thru | 17.66 | mpdecimal | 77.86 | **4.41×** | xRc2 |  |

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
| c | mul | CP | P-gen | x86_64 | thru | 3.34 | libbid | 44.79 | **13.41×** | xRc2 |  |
| c | mul | WP | P-gen | x86_64 | thru | 33.09 | libbid | 63.43 | **1.92×** | xRc2 |  |
| c | mul | XP | P-gen | x86_64 | thru | 42.43 | libbid | 92.23 | **2.17×** | xRc2 |  |
| c | mul | CP | P-gen | x86_64 | thru | 3.34 | decQuad | 55.11 | **16.50×** | xRc2 |  |
| c | mul | WP | P-gen | x86_64 | thru | 33.09 | decQuad | 71.62 | **2.16×** | xRc2 |  |
| c | mul | XP | P-gen | x86_64 | thru | 42.43 | decQuad | 87.13 | **2.05×** | xRc2 |  |
| c | mul | CP | P-gen | x86_64 | thru | 3.34 | mpdecimal | 60.59 | **18.14×** | xRc2 |  |
| c | mul | WP | P-gen | x86_64 | thru | 33.09 | mpdecimal | 180.17 | **5.44×** | xRc2 |  |
| c | mul | XP | P-gen | x86_64 | thru | 42.43 | mpdecimal | 221.59 | **5.22×** | xRc2 |  |

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
| c | div | CD | P-gen | x86_64 | thru | 70.52 | libbid | 79.67 | **1.13×** | xRc2 |  |
| c | div | WD | P-gen | x86_64 | thru | 84.35 | libbid | 81.86 | **0.97×** | xRc2 |  |
| c | div | XD | P-gen | x86_64 | thru | 73.79 | libbid | 82.43 | **1.12×** | xRc2 |  |
| c | div | ET | P-gen | x86_64 | thru | 25.84 | libbid | 29.82 | **1.15×** | xRc2 |  |
| c | div | PT | P-gen | x86_64 | thru | 6.71 | libbid | 29.73 | **4.43×** | xRc2 |  |
| c | div | CD | P-gen | x86_64 | thru | 70.52 | decQuad | 135.67 | **1.92×** | xRc2 |  |
| c | div | WD | P-gen | x86_64 | thru | 84.35 | decQuad | 240.68 | **2.85×** | xRc2 |  |
| c | div | XD | P-gen | x86_64 | thru | 73.79 | decQuad | 389.33 | **5.28×** | xRc2 |  |
| c | div | ET | P-gen | x86_64 | thru | 25.84 | decQuad | 94.82 | **3.67×** | xRc2 |  |
| c | div | PT | P-gen | x86_64 | thru | 6.71 | decQuad | 79.72 | **11.88×** | xRc2 |  |
| c | div | CD | P-gen | x86_64 | thru | 70.52 | mpdecimal | 157.83 | **2.24×** | xRc2 |  |
| c | div | WD | P-gen | x86_64 | thru | 84.35 | mpdecimal | 274.38 | **3.25×** | xRc2 |  |
| c | div | XD | P-gen | x86_64 | thru | 73.79 | mpdecimal | 352.70 | **4.78×** | xRc2 |  |
| c | div | ET | P-gen | x86_64 | thru | 25.84 | mpdecimal | 152.49 | **5.90×** | xRc2 |  |
| c | div | PT | P-gen | x86_64 | thru | 6.71 | mpdecimal | 100.94 | **15.04×** | xRc2 |  |

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
| c | fma | FN | FMA | x86_64 | thru | 114.54 | libbid | 154.43 | **1.35×** | xRc2 |  |
| c | fma | FF | FMA | x86_64 | thru | 72.55 | libbid | 118.36 | **1.63×** | xRc2 |  |
| c | fma | FN | FMA | x86_64 | thru | 114.54 | decQuad | 141.54 | **1.24×** | xRc2 |  |
| c | fma | FF | FMA | x86_64 | thru | 72.55 | decQuad | 149.10 | **2.06×** | xRc2 |  |
| c | fma | FN | FMA | x86_64 | thru | 114.54 | mpdecimal | 251.34 | **2.19×** | xRc2 |  |
| c | fma | FF | FMA | x86_64 | thru | 72.55 | mpdecimal | 328.26 | **4.52×** | xRc2 |  |

<!-- END GENERATED fma-rel-c-x86 -->

</div>
