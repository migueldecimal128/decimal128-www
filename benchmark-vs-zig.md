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

## FinMix — realistic financial mix (P-fin)

The headline: one realistic 64-bit financial operation mix — a `MIX` add/sub stream, mul `CP`/`WP`, div `CD`/`WD`/`ET`/`PT` — `ratio = alt / ours` (&gt; 1 ⇒ d128 faster). This is the profile closest to real financial code.

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED pfin-rel-zig -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | add | MIX | P-fin | arm64 | thru | 3.14 | libbid | 10.35 | **3.30×** | Rzgsw2 |  |
| zig | sub | MIX | P-fin | arm64 | thru | 2.48 | libbid | 10.65 | **4.29×** | Rzgsw2 |  |
| zig | mul | CP | P-fin | arm64 | thru | 1.44 | libbid | 23.69 | **16.45×** | Rzgsw2 |  |
| zig | mul | WP | P-fin | arm64 | thru | 18.64 | libbid | 34.45 | **1.85×** | Rzgsw2 |  |
| zig | div | CD | P-fin | arm64 | thru | 40.61 | libbid | 35.06 | **0.86×** | Rzgsw2 |  |
| zig | div | WD | P-fin | arm64 | thru | 41.25 | libbid | 39.18 | **0.95×** | Rzgsw2 |  |
| zig | div | ET | P-fin | arm64 | thru | 7.65 | libbid | 6.11 | **0.80×** | Rzgsw2 |  |
| zig | div | PT | P-fin | arm64 | thru | 4.23 | libbid | 6.10 | **1.44×** | Rzgsw2 |  |

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
| zig | add | SQ | P-gen | arm64 | thru | 2.54 | libbid | 7.79 | **3.07×** | Rzgsw2 |  |
| zig | add | NQ | P-gen | arm64 | thru | 6.07 | libbid | 8.46 | **1.39×** | Rzgsw2 |  |
| zig | add | MQ | P-gen | arm64 | thru | 12.18 | libbid | 8.57 | **0.70×** | Rzgsw2 |  |
| zig | add | OQ | P-gen | arm64 | thru | 12.83 | libbid | 13.87 | **1.08×** | Rzgsw2 |  |
| zig | add | FQ | P-gen | arm64 | thru | 7.58 | libbid | 9.37 | **1.24×** | Rzgsw2 |  |

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
| zig | sub | SQ | P-gen | arm64 | thru | 1.56 | libbid | 9.17 | **5.88×** | Rzgsw2 |  |
| zig | sub | NQ | P-gen | arm64 | thru | 7.64 | libbid | 9.60 | **1.26×** | Rzgsw2 |  |
| zig | sub | MQ | P-gen | arm64 | thru | 13.51 | libbid | 9.40 | **0.70×** | Rzgsw2 |  |
| zig | sub | OQ | P-gen | arm64 | thru | 14.44 | libbid | 14.83 | **1.03×** | Rzgsw2 |  |
| zig | sub | FQ | P-gen | arm64 | thru | 9.31 | libbid | 9.37 | **1.01×** | Rzgsw2 |  |

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
| zig | mul | CP | P-gen | arm64 | thru | 1.58 | libbid | 24.24 | **15.34×** | Rzgsw2 |  |
| zig | mul | WP | P-gen | arm64 | thru | 18.57 | libbid | 33.43 | **1.80×** | Rzgsw2 |  |
| zig | mul | XP | P-gen | arm64 | thru | 25.44 | libbid | 44.63 | **1.75×** | Rzgsw2 |  |

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
| zig | div | CD | P-gen | arm64 | thru | 39.04 | libbid | 36.61 | **0.94×** | Rzgsw2 |  |
| zig | div | WD | P-gen | arm64 | thru | 42.29 | libbid | 37.71 | **0.89×** | Rzgsw2 |  |
| zig | div | XD | P-gen | arm64 | thru | 34.46 | libbid | 40.43 | **1.17×** | Rzgsw2 |  |
| zig | div | ET | P-gen | arm64 | thru | 10.69 | libbid | 11.57 | **1.08×** | Rzgsw2 |  |
| zig | div | PT | P-gen | arm64 | thru | 4.23 | libbid | 11.42 | **2.70×** | Rzgsw2 |  |

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
| zig | fma | FN | FMA | arm64 | thru | 66.93 | libbid | 82.34 | **1.23×** | Rzgsw2 |  |
| zig | fma | FF | FMA | arm64 | thru | 44.61 | libbid | 59.70 | **1.34×** | Rzgsw2 |  |

<!-- END GENERATED fma-rel-zig -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-zig-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | fma | FN | FMA | x86_64 | thru | 106.84 | libbid | 161.79 | **1.51×** | xRzgsw2 |  |
| zig | fma | FF | FMA | x86_64 | thru | 74.65 | libbid | 124.13 | **1.66×** | xRzgsw2 |  |

<!-- END GENERATED fma-rel-zig-x86 -->

</div>
