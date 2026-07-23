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
| zig | add | MIX | P-fin | arm64 | thru | 3.09 | libbid | 9.14 | **2.96×** | Rzgsw2 |  |
| zig | sub | MIX | P-fin | arm64 | thru | 2.40 | libbid | 13.48 | **5.62×** | Rzgsw2 |  |
| zig | mul | CP | P-fin | arm64 | thru | 1.43 | libbid | 23.29 | **16.29×** | Rzgsw2 |  |
| zig | mul | WP | P-fin | arm64 | thru | 18.63 | libbid | 32.06 | **1.72×** | Rzgsw2 |  |
| zig | div | CD | P-fin | arm64 | thru | 40.69 | libbid | 34.91 | **0.86×** | Rzgsw2 |  |
| zig | div | WD | P-fin | arm64 | thru | 40.78 | libbid | 39.06 | **0.96×** | Rzgsw2 |  |
| zig | div | ET | P-fin | arm64 | thru | 7.65 | libbid | 5.99 | **0.78×** | Rzgsw2 |  |
| zig | div | PT | P-fin | arm64 | thru | 4.17 | libbid | 5.99 | **1.44×** | Rzgsw2 |  |

<!-- END GENERATED pfin-rel-zig -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-zig-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | add | MIX | P-fin | x86_64 | thru | 12.33 | libbid | 31.03 | **2.52×** | xRzgsw2 |  |
| zig | sub | MIX | P-fin | x86_64 | thru | 10.34 | libbid | 35.45 | **3.43×** | xRzgsw2 |  |
| zig | mul | CP | P-fin | x86_64 | thru | 7.04 | libbid | 47.15 | **6.70×** | xRzgsw2 |  |
| zig | mul | WP | P-fin | x86_64 | thru | 29.29 | libbid | 60.29 | **2.06×** | xRzgsw2 |  |
| zig | div | CD | P-fin | x86_64 | thru | 67.73 | libbid | 77.69 | **1.15×** | xRzgsw2 |  |
| zig | div | WD | P-fin | x86_64 | thru | 92.85 | libbid | 82.71 | **0.89×** | xRzgsw2 |  |
| zig | div | ET | P-fin | x86_64 | thru | 22.82 | libbid | 20.15 | **0.88×** | xRzgsw2 |  |
| zig | div | PT | P-fin | x86_64 | thru | 12.41 | libbid | 19.71 | **1.59×** | xRzgsw2 |  |

<!-- END GENERATED pfin-rel-zig-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-zig -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | add | SQ | P-gen | arm64 | thru | 2.59 | libbid | 8.31 | **3.21×** | Rzgsw2 |  |
| zig | add | NQ | P-gen | arm64 | thru | 5.97 | libbid | 8.28 | **1.39×** | Rzgsw2 |  |
| zig | add | MQ | P-gen | arm64 | thru | 8.46 | libbid | 9.42 | **1.11×** | Rzgsw2 |  |
| zig | add | OQ | P-gen | arm64 | thru | 12.55 | libbid | 13.39 | **1.07×** | Rzgsw2 |  |
| zig | add | FQ | P-gen | arm64 | thru | 8.28 | libbid | 10.65 | **1.29×** | Rzgsw2 |  |

<!-- END GENERATED add-rel-zig -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-zig-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | add | SQ | P-gen | x86_64 | thru | 10.78 | libbid | 30.20 | **2.80×** | xRzgsw2 |  |
| zig | add | NQ | P-gen | x86_64 | thru | 16.34 | libbid | 33.46 | **2.05×** | xRzgsw2 |  |
| zig | add | MQ | P-gen | x86_64 | thru | 25.55 | libbid | 31.52 | **1.23×** | xRzgsw2 |  |
| zig | add | OQ | P-gen | x86_64 | thru | 35.11 | libbid | 51.83 | **1.48×** | xRzgsw2 |  |
| zig | add | FQ | P-gen | x86_64 | thru | 21.19 | libbid | 32.09 | **1.51×** | xRzgsw2 |  |

<!-- END GENERATED add-rel-zig-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-zig -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | sub | SQ | P-gen | arm64 | thru | 1.61 | libbid | 9.05 | **5.62×** | Rzgsw2 |  |
| zig | sub | NQ | P-gen | arm64 | thru | 7.63 | libbid | 11.78 | **1.54×** | Rzgsw2 |  |
| zig | sub | MQ | P-gen | arm64 | thru | 10.17 | libbid | 9.01 | **0.89×** | Rzgsw2 |  |
| zig | sub | OQ | P-gen | arm64 | thru | 13.15 | libbid | 14.26 | **1.08×** | Rzgsw2 |  |
| zig | sub | FQ | P-gen | arm64 | thru | 9.11 | libbid | 10.47 | **1.15×** | Rzgsw2 |  |

<!-- END GENERATED sub-rel-zig -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-zig-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | sub | SQ | P-gen | x86_64 | thru | 7.52 | libbid | 34.25 | **4.55×** | xRzgsw2 |  |
| zig | sub | NQ | P-gen | x86_64 | thru | 17.78 | libbid | 36.66 | **2.06×** | xRzgsw2 |  |
| zig | sub | MQ | P-gen | x86_64 | thru | 26.56 | libbid | 36.66 | **1.38×** | xRzgsw2 |  |
| zig | sub | OQ | P-gen | x86_64 | thru | 36.59 | libbid | 51.52 | **1.41×** | xRzgsw2 |  |
| zig | sub | FQ | P-gen | x86_64 | thru | 24.10 | libbid | 34.71 | **1.44×** | xRzgsw2 |  |

<!-- END GENERATED sub-rel-zig-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-zig -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | mul | CP | P-gen | arm64 | thru | 1.57 | libbid | 22.86 | **14.56×** | Rzgsw2 |  |
| zig | mul | WP | P-gen | arm64 | thru | 18.58 | libbid | 33.01 | **1.78×** | Rzgsw2 |  |
| zig | mul | XP | P-gen | arm64 | thru | 25.31 | libbid | 42.65 | **1.69×** | Rzgsw2 |  |

<!-- END GENERATED mul-rel-zig -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-zig-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | mul | CP | P-gen | x86_64 | thru | 7.72 | libbid | 47.38 | **6.14×** | xRzgsw2 |  |
| zig | mul | WP | P-gen | x86_64 | thru | 28.79 | libbid | 65.94 | **2.29×** | xRzgsw2 |  |
| zig | mul | XP | P-gen | x86_64 | thru | 42.80 | libbid | 96.66 | **2.26×** | xRzgsw2 |  |

<!-- END GENERATED mul-rel-zig-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-zig -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | div | CD | P-gen | arm64 | thru | 37.28 | libbid | 36.61 | **0.98×** | Rzgsw2 |  |
| zig | div | WD | P-gen | arm64 | thru | 41.16 | libbid | 37.48 | **0.91×** | Rzgsw2 |  |
| zig | div | XD | P-gen | arm64 | thru | 31.25 | libbid | 39.15 | **1.25×** | Rzgsw2 |  |
| zig | div | ET | P-gen | arm64 | thru | 10.64 | libbid | 10.86 | **1.02×** | Rzgsw2 |  |
| zig | div | PT | P-gen | arm64 | thru | 4.17 | libbid | 10.64 | **2.55×** | Rzgsw2 |  |

<!-- END GENERATED div-rel-zig -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-zig-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | div | CD | P-gen | x86_64 | thru | 75.13 | libbid | 82.50 | **1.10×** | xRzgsw2 |  |
| zig | div | WD | P-gen | x86_64 | thru | 99.07 | libbid | 84.36 | **0.85×** | xRzgsw2 |  |
| zig | div | XD | P-gen | x86_64 | thru | 77.92 | libbid | 84.37 | **1.08×** | xRzgsw2 |  |
| zig | div | ET | P-gen | x86_64 | thru | 32.73 | libbid | 30.87 | **0.94×** | xRzgsw2 |  |
| zig | div | PT | P-gen | x86_64 | thru | 12.32 | libbid | 31.09 | **2.52×** | xRzgsw2 |  |

<!-- END GENERATED div-rel-zig-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-zig -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | fma | FN | FMA | arm64 | thru | 69.16 | libbid | 81.22 | **1.17×** | Rzgsw2 |  |
| zig | fma | FF | FMA | arm64 | thru | 44.73 | libbid | 57.36 | **1.28×** | Rzgsw2 |  |

<!-- END GENERATED fma-rel-zig -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-zig-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | fma | FN | FMA | x86_64 | thru | 106.84 | libbid | 161.79 | **1.51×** | xRzgsw2 |  |
| zig | fma | FF | FMA | x86_64 | thru | 74.65 | libbid | 124.13 | **1.66×** | xRzgsw2 |  |

<!-- END GENERATED fma-rel-zig-x86 -->

</div>
