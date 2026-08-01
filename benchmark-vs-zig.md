---
layout: default
permalink: /benchmark/vs-zig.html
title: "Zig Benchmark Results — Decimal128"
description: "decimal128 in Zig, measured against the alternatives available to it — a realistic financial mix (P-fin) plus per-operation band characterization, with explicit ratios."
heading: "Zig Benchmark Results"
---

<div class="whitepaper" markdown="1">

<p class="whitepaper-meta">Living document — as-measured results. Category codes, profiles, modes &amp; method: <a href="key.html">Benchmark Key</a>.</p>

This is the **Zig** view of decimal128 **as-measured**, band by band, with explicit ratios. It opens with the realistic financial-mix (**P-fin**) headline, then the per-operation band characterization (**P-gen**) and FMA. In Zig, d128 is measured against the **libbid** universal reference (Zig has no in-language decimal peer). It is **data only** — the categories, magnitude profiles, units, and methodology are defined in the [Benchmark Key](key.html) (and, authoritatively, `BenchmarkMatrix.md`). The cross-port d128 band-shape matrices (all ports, no alternatives) live in [Port-Comparison Benchmark Results](port-compare.html); the full index of per-language pages is on the [Benchmarks](/benchmarks.html) hub.

## Summary — Ratio Range by Operation

The ratio for Zig's reference library on x86_64 (Intel i9-9880H): `ratio = libbid / Miguel` (&gt; 1× ⇒ d128 faster), broken out by operation. Zig has no in-language decimal peer.

| | Add | Subtract | Multiply | Divide |
|---|---|---|---|---|
| ratio = libbid / Miguel | 2.5× | 3× | 2.1× – 7× | 0.9× – 1.6× |

## FinMix — realistic financial mix (P-fin)

The headline: one realistic 64-bit financial operation mix — a `MIX` add/sub stream, mul `CP`/`WP`, div `CD`/`WD`/`ET`/`PT` — `ratio = alt / Miguel` (&gt; 1 ⇒ d128 faster). This is the profile closest to real financial code.

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED pfin-rel-zig -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | add | MIX | P-fin | arm64 | thru | 2.02 | libbid | 10.72 | **5.31×** | Rzgsw2 |  |
| zig | sub | MIX | P-fin | arm64 | thru | 2.50 | libbid | 11.80 | **4.72×** | Rzgsw2 |  |
| zig | mul | CP | P-fin | arm64 | thru | 1.43 | libbid | 23.57 | **16.48×** | Rzgsw2 |  |
| zig | mul | WP | P-fin | arm64 | thru | 18.64 | libbid | 34.52 | **1.85×** | Rzgsw2 |  |
| zig | div | CD | P-fin | arm64 | thru | 30.44 | libbid | 35.07 | **1.15×** | Rzgsw2 |  |
| zig | div | WD | P-fin | arm64 | thru | 38.09 | libbid | 40.37 | **1.06×** | Rzgsw2 |  |
| zig | div | ET | P-fin | arm64 | thru | 7.59 | libbid | 6.09 | **0.80×** | Rzgsw2 |  |
| zig | div | PT | P-fin | arm64 | thru | 4.13 | libbid | 6.09 | **1.47×** | Rzgsw2 |  |

<!-- END GENERATED pfin-rel-zig -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-zig-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | add | MIX | P-fin | x86_64 | thru | 6.77 | libbid | 27.35 | **4.04×** | xRzgsw2 |  |
| zig | sub | MIX | P-fin | x86_64 | thru | 7.84 | libbid | 28.89 | **3.68×** | xRzgsw2 |  |
| zig | mul | CP | P-fin | x86_64 | thru | 5.34 | libbid | 44.35 | **8.31×** | xRzgsw2 |  |
| zig | mul | WP | P-fin | x86_64 | thru | 28.35 | libbid | 57.75 | **2.04×** | xRzgsw2 |  |
| zig | div | CD | P-fin | x86_64 | thru | 63.30 | libbid | 74.27 | **1.17×** | xRzgsw2 |  |
| zig | div | WD | P-fin | x86_64 | thru | 112.06 | libbid | 79.07 | **0.71×** | xRzgsw2 |  |
| zig | div | ET | P-fin | x86_64 | thru | 19.93 | libbid | 18.88 | **0.95×** | xRzgsw2 |  |
| zig | div | PT | P-fin | x86_64 | thru | 11.76 | libbid | 19.10 | **1.62×** | xRzgsw2 |  |

<!-- END GENERATED pfin-rel-zig-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-zig -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | add | SQss | P-gen | arm64 | thru | 1.27 | libbid | 7.96 | **6.27×** | Rzgsw2 |  |
| zig | add | SQos | P-gen | arm64 | thru | 2.26 | libbid | 8.69 | **3.85×** | Rzgsw2 |  |
| zig | add | NQss | P-gen | arm64 | thru | 4.25 | libbid | 9.36 | **2.20×** | Rzgsw2 |  |
| zig | add | NQos | P-gen | arm64 | thru | 4.88 | libbid | 9.78 | **2.00×** | Rzgsw2 |  |
| zig | add | MQss | P-gen | arm64 | thru | 6.21 | libbid | 9.75 | **1.57×** | Rzgsw2 |  |
| zig | add | MQos | P-gen | arm64 | thru | 12.26 | libbid | 9.71 | **0.79×** | Rzgsw2 |  |
| zig | add | OQss | P-gen | arm64 | thru | 12.00 | libbid | 13.66 | **1.14×** | Rzgsw2 |  |
| zig | add | OQos | P-gen | arm64 | thru | 15.68 | libbid | 15.31 | **0.98×** | Rzgsw2 |  |
| zig | add | FQss | P-gen | arm64 | thru | 8.44 | libbid | 9.32 | **1.10×** | Rzgsw2 |  |
| zig | add | FQos | P-gen | arm64 | thru | 10.88 | libbid | 10.38 | **0.95×** | Rzgsw2 |  |

<!-- END GENERATED add-rel-zig -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-zig-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | add | SQss | P-gen | x86_64 | thru | 4.92 | libbid | 27.04 | **5.50×** | xRzgsw2 |  |
| zig | add | SQos | P-gen | x86_64 | thru | 7.28 | libbid | 25.59 | **3.52×** | xRzgsw2 |  |
| zig | add | NQss | P-gen | x86_64 | thru | 12.12 | libbid | 29.04 | **2.40×** | xRzgsw2 |  |
| zig | add | NQos | P-gen | x86_64 | thru | 13.15 | libbid | 28.25 | **2.15×** | xRzgsw2 |  |
| zig | add | MQss | P-gen | x86_64 | thru | 14.25 | libbid | 27.26 | **1.91×** | xRzgsw2 |  |
| zig | add | MQos | P-gen | x86_64 | thru | 22.63 | libbid | 27.12 | **1.20×** | xRzgsw2 |  |
| zig | add | OQss | P-gen | x86_64 | thru | 27.93 | libbid | 42.96 | **1.54×** | xRzgsw2 |  |
| zig | add | OQos | P-gen | x86_64 | thru | 34.21 | libbid | 43.17 | **1.26×** | xRzgsw2 |  |
| zig | add | FQss | P-gen | x86_64 | thru | 16.55 | libbid | 29.28 | **1.77×** | xRzgsw2 |  |
| zig | add | FQos | P-gen | x86_64 | thru | 21.07 | libbid | 29.32 | **1.39×** | xRzgsw2 |  |

<!-- END GENERATED add-rel-zig-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-zig -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | sub | SQss | P-gen | arm64 | thru | 1.69 | libbid | 9.68 | **5.73×** | Rzgsw2 |  |
| zig | sub | SQos | P-gen | arm64 | thru | 1.32 | libbid | 10.04 | **7.61×** | Rzgsw2 |  |
| zig | sub | NQss | P-gen | arm64 | thru | 4.93 | libbid | 10.87 | **2.20×** | Rzgsw2 |  |
| zig | sub | NQos | P-gen | arm64 | thru | 4.29 | libbid | 11.42 | **2.66×** | Rzgsw2 |  |
| zig | sub | MQss | P-gen | arm64 | thru | 12.78 | libbid | 9.94 | **0.78×** | Rzgsw2 |  |
| zig | sub | MQos | P-gen | arm64 | thru | 6.23 | libbid | 9.78 | **1.57×** | Rzgsw2 |  |
| zig | sub | OQss | P-gen | arm64 | thru | 16.28 | libbid | 15.79 | **0.97×** | Rzgsw2 |  |
| zig | sub | OQos | P-gen | arm64 | thru | 12.95 | libbid | 14.84 | **1.15×** | Rzgsw2 |  |
| zig | sub | FQss | P-gen | arm64 | thru | 11.10 | libbid | 9.39 | **0.85×** | Rzgsw2 |  |
| zig | sub | FQos | P-gen | arm64 | thru | 9.44 | libbid | 9.48 | **1.00×** | Rzgsw2 |  |

<!-- END GENERATED sub-rel-zig -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-zig-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | sub | SQss | P-gen | x86_64 | thru | 6.62 | libbid | 30.07 | **4.54×** | xRzgsw2 |  |
| zig | sub | SQos | P-gen | x86_64 | thru | 5.07 | libbid | 30.04 | **5.93×** | xRzgsw2 |  |
| zig | sub | NQss | P-gen | x86_64 | thru | 14.10 | libbid | 31.79 | **2.25×** | xRzgsw2 |  |
| zig | sub | NQos | P-gen | x86_64 | thru | 12.56 | libbid | 32.49 | **2.59×** | xRzgsw2 |  |
| zig | sub | MQss | P-gen | x86_64 | thru | 22.85 | libbid | 30.94 | **1.35×** | xRzgsw2 |  |
| zig | sub | MQos | P-gen | x86_64 | thru | 14.54 | libbid | 30.85 | **2.12×** | xRzgsw2 |  |
| zig | sub | OQss | P-gen | x86_64 | thru | 34.14 | libbid | 46.20 | **1.35×** | xRzgsw2 |  |
| zig | sub | OQos | P-gen | x86_64 | thru | 28.25 | libbid | 45.86 | **1.62×** | xRzgsw2 |  |
| zig | sub | FQss | P-gen | x86_64 | thru | 21.29 | libbid | 33.24 | **1.56×** | xRzgsw2 |  |
| zig | sub | FQos | P-gen | x86_64 | thru | 16.98 | libbid | 32.74 | **1.93×** | xRzgsw2 |  |

<!-- END GENERATED sub-rel-zig-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-zig -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | mul | CP | P-gen | arm64 | thru | 1.58 | libbid | 23.13 | **14.64×** | Rzgsw2 |  |
| zig | mul | WP | P-gen | arm64 | thru | 18.69 | libbid | 35.06 | **1.88×** | Rzgsw2 |  |
| zig | mul | XP | P-gen | arm64 | thru | 22.90 | libbid | 45.24 | **1.98×** | Rzgsw2 |  |

<!-- END GENERATED mul-rel-zig -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-zig-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | mul | CP | P-gen | x86_64 | thru | 6.06 | libbid | 44.79 | **7.39×** | xRzgsw2 |  |
| zig | mul | WP | P-gen | x86_64 | thru | 28.06 | libbid | 63.43 | **2.26×** | xRzgsw2 |  |
| zig | mul | XP | P-gen | x86_64 | thru | 41.73 | libbid | 92.23 | **2.21×** | xRzgsw2 |  |

<!-- END GENERATED mul-rel-zig-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-zig -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | div | CD | P-gen | arm64 | thru | 30.28 | libbid | 36.77 | **1.21×** | Rzgsw2 |  |
| zig | div | WD | P-gen | arm64 | thru | 40.30 | libbid | 37.54 | **0.93×** | Rzgsw2 |  |
| zig | div | XD | P-gen | arm64 | thru | 32.08 | libbid | 38.97 | **1.21×** | Rzgsw2 |  |
| zig | div | ET | P-gen | arm64 | thru | 10.70 | libbid | 11.68 | **1.09×** | Rzgsw2 |  |
| zig | div | PT | P-gen | arm64 | thru | 4.13 | libbid | 11.45 | **2.77×** | Rzgsw2 |  |

<!-- END GENERATED div-rel-zig -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-zig-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | div | CD | P-gen | x86_64 | thru | 73.17 | libbid | 79.67 | **1.09×** | xRzgsw2 |  |
| zig | div | WD | P-gen | x86_64 | thru | 88.27 | libbid | 81.86 | **0.93×** | xRzgsw2 |  |
| zig | div | XD | P-gen | x86_64 | thru | 73.48 | libbid | 82.43 | **1.12×** | xRzgsw2 |  |
| zig | div | ET | P-gen | x86_64 | thru | 31.04 | libbid | 29.82 | **0.96×** | xRzgsw2 |  |
| zig | div | PT | P-gen | x86_64 | thru | 11.76 | libbid | 29.73 | **2.53×** | xRzgsw2 |  |

<!-- END GENERATED div-rel-zig-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-zig -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | fma | FN | FMA | arm64 | thru | 64.07 | - | - | - | Rzgsw2 |  |
| zig | fma | FF | FMA | arm64 | thru | 41.72 | - | - | - | Rzgsw2 |  |

<!-- END GENERATED fma-rel-zig -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-zig-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | fma | FN | FMA | x86_64 | thru | 105.20 | - | - | - | xRzgsw2 |  |
| zig | fma | FF | FMA | x86_64 | thru | 69.56 | - | - | - | xRzgsw2 |  |

<!-- END GENERATED fma-rel-zig-x86 -->

</div>
