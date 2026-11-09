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
| ratio = libbid / Miguel | 4× | 3× | 2.1× – 8× | 0.8× – 1.6× |

## FinMix — realistic financial mix (P-fin)

The headline: one realistic 64-bit financial operation mix — a `MIX` add/sub stream, mul `CP`/`WP`, div `CD`/`WD`/`ET`/`PT` — `ratio = alt / Miguel` (&gt; 1 ⇒ d128 faster). This is the profile closest to real financial code.

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED pfin-rel-zig -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | add | MIX | P-fin | arm64 | thru | 2.00 | libbid | 10.39 | **5.20×** | Rzgsw2 |  |
| zig | sub | MIX | P-fin | arm64 | thru | 2.50 | libbid | 11.71 | **4.68×** | Rzgsw2 |  |
| zig | mul | CP | P-fin | arm64 | thru | 1.44 | libbid | 24.62 | **17.10×** | Rzgsw2 |  |
| zig | mul | WP | P-fin | arm64 | thru | 18.66 | libbid | 34.03 | **1.82×** | Rzgsw2 |  |
| zig | div | CD | P-fin | arm64 | thru | 32.04 | libbid | 36.26 | **1.13×** | Rzgsw2 |  |
| zig | div | WD | P-fin | arm64 | thru | 26.20 | libbid | 39.92 | **1.52×** | Rzgsw2 |  |
| zig | div | ET | P-fin | arm64 | thru | 7.61 | libbid | 6.35 | **0.83×** | Rzgsw2 |  |
| zig | div | PT | P-fin | arm64 | thru | 4.17 | libbid | 6.36 | **1.53×** | Rzgsw2 |  |

<!-- END GENERATED pfin-rel-zig -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-zig-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | add | MIX | P-fin | x86_64 | thru | 7.37 | libbid | 30.56 | **4.15×** | xRzgsw2 |  |
| zig | sub | MIX | P-fin | x86_64 | thru | 8.62 | libbid | 31.87 | **3.70×** | xRzgsw2 |  |
| zig | mul | CP | P-fin | x86_64 | thru | 5.96 | libbid | 50.91 | **8.54×** | xRzgsw2 |  |
| zig | mul | WP | P-fin | x86_64 | thru | 31.35 | libbid | 66.63 | **2.13×** | xRzgsw2 |  |
| zig | div | CD | P-fin | x86_64 | thru | 69.14 | libbid | 82.11 | **1.19×** | xRzgsw2 |  |
| zig | div | WD | P-fin | x86_64 | thru | 97.47 | libbid | 86.90 | **0.89×** | xRzgsw2 |  |
| zig | div | ET | P-fin | x86_64 | thru | 21.77 | libbid | 21.25 | **0.98×** | xRzgsw2 |  |
| zig | div | PT | P-fin | x86_64 | thru | 12.99 | libbid | 21.42 | **1.65×** | xRzgsw2 |  |

<!-- END GENERATED pfin-rel-zig-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-zig -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | add | SQss | P-gen | arm64 | thru | 1.31 | libbid | 8.15 | **6.22×** | Rzgsw2 |  |
| zig | add | SQos | P-gen | arm64 | thru | 2.25 | libbid | 8.48 | **3.77×** | Rzgsw2 |  |
| zig | add | NQss | P-gen | arm64 | thru | 4.25 | libbid | 8.57 | **2.02×** | Rzgsw2 |  |
| zig | add | NQos | P-gen | arm64 | thru | 4.89 | libbid | 9.39 | **1.92×** | Rzgsw2 |  |
| zig | add | MQss | P-gen | arm64 | thru | 6.21 | libbid | 8.97 | **1.44×** | Rzgsw2 |  |
| zig | add | MQos | P-gen | arm64 | thru | 12.00 | libbid | 8.33 | **0.69×** | Rzgsw2 |  |
| zig | add | OQss | P-gen | arm64 | thru | 12.28 | libbid | 13.35 | **1.09×** | Rzgsw2 |  |
| zig | add | OQos | P-gen | arm64 | thru | 15.49 | libbid | 15.22 | **0.98×** | Rzgsw2 |  |
| zig | add | FQss | P-gen | arm64 | thru | 8.44 | libbid | 8.61 | **1.02×** | Rzgsw2 |  |
| zig | add | FQos | P-gen | arm64 | thru | 10.93 | libbid | 8.74 | **0.80×** | Rzgsw2 |  |

<!-- END GENERATED add-rel-zig -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-zig-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | add | SQss | P-gen | x86_64 | thru | 5.47 | libbid | 30.12 | **5.51×** | xRzgsw2 |  |
| zig | add | SQos | P-gen | x86_64 | thru | 7.97 | libbid | 27.81 | **3.49×** | xRzgsw2 |  |
| zig | add | NQss | P-gen | x86_64 | thru | 13.50 | libbid | 31.74 | **2.35×** | xRzgsw2 |  |
| zig | add | NQos | P-gen | x86_64 | thru | 14.78 | libbid | 30.17 | **2.04×** | xRzgsw2 |  |
| zig | add | MQss | P-gen | x86_64 | thru | 15.48 | libbid | 29.55 | **1.91×** | xRzgsw2 |  |
| zig | add | MQos | P-gen | x86_64 | thru | 25.00 | libbid | 28.78 | **1.15×** | xRzgsw2 |  |
| zig | add | OQss | P-gen | x86_64 | thru | 30.44 | libbid | 46.76 | **1.54×** | xRzgsw2 |  |
| zig | add | OQos | P-gen | x86_64 | thru | 37.51 | libbid | 47.44 | **1.26×** | xRzgsw2 |  |
| zig | add | FQss | P-gen | x86_64 | thru | 18.61 | libbid | 33.02 | **1.77×** | xRzgsw2 |  |
| zig | add | FQos | P-gen | x86_64 | thru | 23.80 | libbid | 32.54 | **1.37×** | xRzgsw2 |  |

<!-- END GENERATED add-rel-zig-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-zig -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | sub | SQss | P-gen | arm64 | thru | 1.69 | libbid | 8.87 | **5.25×** | Rzgsw2 |  |
| zig | sub | SQos | P-gen | arm64 | thru | 1.31 | libbid | 9.07 | **6.92×** | Rzgsw2 |  |
| zig | sub | NQss | P-gen | arm64 | thru | 4.92 | libbid | 10.70 | **2.17×** | Rzgsw2 |  |
| zig | sub | NQos | P-gen | arm64 | thru | 4.25 | libbid | 8.85 | **2.08×** | Rzgsw2 |  |
| zig | sub | MQss | P-gen | arm64 | thru | 12.39 | libbid | 9.45 | **0.76×** | Rzgsw2 |  |
| zig | sub | MQos | P-gen | arm64 | thru | 6.28 | libbid | 9.14 | **1.46×** | Rzgsw2 |  |
| zig | sub | OQss | P-gen | arm64 | thru | 16.38 | libbid | 16.42 | **1.00×** | Rzgsw2 |  |
| zig | sub | OQos | P-gen | arm64 | thru | 12.90 | libbid | 14.31 | **1.11×** | Rzgsw2 |  |
| zig | sub | FQss | P-gen | arm64 | thru | 10.93 | libbid | 9.74 | **0.89×** | Rzgsw2 |  |
| zig | sub | FQos | P-gen | arm64 | thru | 9.51 | libbid | 9.03 | **0.95×** | Rzgsw2 |  |

<!-- END GENERATED sub-rel-zig -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-zig-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | sub | SQss | P-gen | x86_64 | thru | 7.50 | libbid | 33.73 | **4.50×** | xRzgsw2 |  |
| zig | sub | SQos | P-gen | x86_64 | thru | 5.48 | libbid | 32.99 | **6.02×** | xRzgsw2 |  |
| zig | sub | NQss | P-gen | x86_64 | thru | 14.93 | libbid | 34.85 | **2.33×** | xRzgsw2 |  |
| zig | sub | NQos | P-gen | x86_64 | thru | 13.86 | libbid | 35.61 | **2.57×** | xRzgsw2 |  |
| zig | sub | MQss | P-gen | x86_64 | thru | 25.01 | libbid | 34.98 | **1.40×** | xRzgsw2 |  |
| zig | sub | MQos | P-gen | x86_64 | thru | 15.99 | libbid | 34.66 | **2.17×** | xRzgsw2 |  |
| zig | sub | OQss | P-gen | x86_64 | thru | 38.38 | libbid | 51.72 | **1.35×** | xRzgsw2 |  |
| zig | sub | OQos | P-gen | x86_64 | thru | 31.54 | libbid | 50.81 | **1.61×** | xRzgsw2 |  |
| zig | sub | FQss | P-gen | x86_64 | thru | 23.74 | libbid | 37.25 | **1.57×** | xRzgsw2 |  |
| zig | sub | FQos | P-gen | x86_64 | thru | 20.71 | libbid | 36.53 | **1.76×** | xRzgsw2 |  |

<!-- END GENERATED sub-rel-zig-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-zig -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | mul | CP | P-gen | arm64 | thru | 1.57 | libbid | 24.33 | **15.50×** | Rzgsw2 |  |
| zig | mul | WP | P-gen | arm64 | thru | 18.68 | libbid | 34.83 | **1.86×** | Rzgsw2 |  |
| zig | mul | XP | P-gen | arm64 | thru | 22.87 | libbid | 45.16 | **1.97×** | Rzgsw2 |  |

<!-- END GENERATED mul-rel-zig -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-zig-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | mul | CP | P-gen | x86_64 | thru | 7.46 | libbid | 50.55 | **6.78×** | xRzgsw2 |  |
| zig | mul | WP | P-gen | x86_64 | thru | 36.01 | libbid | 73.62 | **2.04×** | xRzgsw2 |  |
| zig | mul | XP | P-gen | x86_64 | thru | 48.32 | libbid | 104.96 | **2.17×** | xRzgsw2 |  |

<!-- END GENERATED mul-rel-zig-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-zig -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | div | CD | P-gen | arm64 | thru | 29.84 | libbid | 37.59 | **1.26×** | Rzgsw2 |  |
| zig | div | WD | P-gen | arm64 | thru | 26.07 | libbid | 37.36 | **1.43×** | Rzgsw2 |  |
| zig | div | XD | P-gen | arm64 | thru | 33.81 | libbid | 38.86 | **1.15×** | Rzgsw2 |  |
| zig | div | ET | P-gen | arm64 | thru | 10.52 | libbid | 11.94 | **1.13×** | Rzgsw2 |  |
| zig | div | PT | P-gen | arm64 | thru | 4.17 | libbid | 11.50 | **2.76×** | Rzgsw2 |  |

<!-- END GENERATED div-rel-zig -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-zig-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | div | CD | P-gen | x86_64 | thru | 79.70 | libbid | 86.65 | **1.09×** | xRzgsw2 |  |
| zig | div | WD | P-gen | x86_64 | thru | 95.55 | libbid | 88.12 | **0.92×** | xRzgsw2 |  |
| zig | div | XD | P-gen | x86_64 | thru | 80.90 | libbid | 88.89 | **1.10×** | xRzgsw2 |  |
| zig | div | ET | P-gen | x86_64 | thru | 33.46 | libbid | 31.98 | **0.96×** | xRzgsw2 |  |
| zig | div | PT | P-gen | x86_64 | thru | 12.95 | libbid | 32.28 | **2.49×** | xRzgsw2 |  |

<!-- END GENERATED div-rel-zig-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-zig -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | fma | FN | FMA | arm64 | thru | 35.28 | - | - | - | Rzgsw2 |  |
| zig | fma | FF | FMA | arm64 | thru | 42.07 | - | - | - | Rzgsw2 |  |

<!-- END GENERATED fma-rel-zig -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-zig-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | fma | FN | FMA | x86_64 | thru | 119.12 | - | - | - | xRzgsw2 |  |
| zig | fma | FF | FMA | x86_64 | thru | 79.83 | - | - | - | xRzgsw2 |  |

<!-- END GENERATED fma-rel-zig-x86 -->

</div>
