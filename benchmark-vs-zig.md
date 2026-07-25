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
| zig | add | MIX | P-fin | arm64 | thru | 2.12 | libbid | 10.75 | **5.07×** | Rzgsw2 |  |
| zig | sub | MIX | P-fin | arm64 | thru | 2.50 | libbid | 13.35 | **5.34×** | Rzgsw2 |  |
| zig | mul | CP | P-fin | arm64 | thru | 1.43 | libbid | 23.54 | **16.46×** | Rzgsw2 |  |
| zig | mul | WP | P-fin | arm64 | thru | 18.55 | libbid | 32.43 | **1.75×** | Rzgsw2 |  |
| zig | div | CD | P-fin | arm64 | thru | 30.12 | libbid | 36.12 | **1.20×** | Rzgsw2 |  |
| zig | div | WD | P-fin | arm64 | thru | 38.22 | libbid | 39.16 | **1.02×** | Rzgsw2 |  |
| zig | div | ET | P-fin | arm64 | thru | 7.59 | libbid | 6.10 | **0.80×** | Rzgsw2 |  |
| zig | div | PT | P-fin | arm64 | thru | 4.17 | libbid | 6.10 | **1.46×** | Rzgsw2 |  |

<!-- END GENERATED pfin-rel-zig -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-zig-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | add | MIX | P-fin | x86_64 | thru | 9.94 | libbid | 28.09 | **2.83×** | xRzgsw2 |  |
| zig | sub | MIX | P-fin | x86_64 | thru | 7.67 | libbid | 29.12 | **3.80×** | xRzgsw2 |  |
| zig | mul | CP | P-fin | x86_64 | thru | 5.25 | libbid | 44.34 | **8.45×** | xRzgsw2 |  |
| zig | mul | WP | P-fin | x86_64 | thru | 29.29 | libbid | 58.84 | **2.01×** | xRzgsw2 |  |
| zig | div | CD | P-fin | x86_64 | thru | 65.19 | libbid | 73.35 | **1.13×** | xRzgsw2 |  |
| zig | div | WD | P-fin | x86_64 | thru | 90.38 | libbid | 79.45 | **0.88×** | xRzgsw2 |  |
| zig | div | ET | P-fin | x86_64 | thru | 20.19 | libbid | 18.93 | **0.94×** | xRzgsw2 |  |
| zig | div | PT | P-fin | x86_64 | thru | 11.71 | libbid | 18.69 | **1.60×** | xRzgsw2 |  |

<!-- END GENERATED pfin-rel-zig-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-zig -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | add | SQ | P-gen | arm64 | thru | 2.55 | libbid | 8.44 | **3.31×** | Rzgsw2 |  |
| zig | add | NQ | P-gen | arm64 | thru | 5.92 | libbid | 9.37 | **1.58×** | Rzgsw2 |  |
| zig | add | MQ | P-gen | arm64 | thru | 8.44 | libbid | 8.94 | **1.06×** | Rzgsw2 |  |
| zig | add | OQ | P-gen | arm64 | thru | 12.60 | libbid | 14.26 | **1.13×** | Rzgsw2 |  |
| zig | add | FQ | P-gen | arm64 | thru | 8.20 | libbid | 9.34 | **1.14×** | Rzgsw2 |  |

<!-- END GENERATED add-rel-zig -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-zig-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | add | SQ | P-gen | x86_64 | thru | 8.98 | libbid | 30.49 | **3.40×** | xRzgsw2 |  |
| zig | add | NQ | P-gen | x86_64 | thru | 14.49 | libbid | 32.84 | **2.27×** | xRzgsw2 |  |
| zig | add | MQ | P-gen | x86_64 | thru | 19.18 | libbid | 31.94 | **1.67×** | xRzgsw2 |  |
| zig | add | OQ | P-gen | x86_64 | thru | 33.43 | libbid | 49.07 | **1.47×** | xRzgsw2 |  |
| zig | add | FQ | P-gen | x86_64 | thru | 19.73 | libbid | 31.26 | **1.58×** | xRzgsw2 |  |

<!-- END GENERATED add-rel-zig-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-zig -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | sub | SQ | P-gen | arm64 | thru | 1.57 | libbid | 8.66 | **5.52×** | Rzgsw2 |  |
| zig | sub | NQ | P-gen | arm64 | thru | 7.64 | libbid | 9.93 | **1.30×** | Rzgsw2 |  |
| zig | sub | MQ | P-gen | arm64 | thru | 10.14 | libbid | 9.08 | **0.90×** | Rzgsw2 |  |
| zig | sub | OQ | P-gen | arm64 | thru | 13.19 | libbid | 14.91 | **1.13×** | Rzgsw2 |  |
| zig | sub | FQ | P-gen | arm64 | thru | 8.94 | libbid | 10.50 | **1.17×** | Rzgsw2 |  |

<!-- END GENERATED sub-rel-zig -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-zig-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | sub | SQ | P-gen | x86_64 | thru | 5.79 | libbid | 35.60 | **6.15×** | xRzgsw2 |  |
| zig | sub | NQ | P-gen | x86_64 | thru | 15.45 | libbid | 36.06 | **2.33×** | xRzgsw2 |  |
| zig | sub | MQ | P-gen | x86_64 | thru | 20.43 | libbid | 34.36 | **1.68×** | xRzgsw2 |  |
| zig | sub | OQ | P-gen | x86_64 | thru | 34.81 | libbid | 50.67 | **1.46×** | xRzgsw2 |  |
| zig | sub | FQ | P-gen | x86_64 | thru | 22.12 | libbid | 33.98 | **1.54×** | xRzgsw2 |  |

<!-- END GENERATED sub-rel-zig-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-zig -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | mul | CP | P-gen | arm64 | thru | 1.57 | libbid | 22.98 | **14.64×** | Rzgsw2 |  |
| zig | mul | WP | P-gen | arm64 | thru | 18.39 | libbid | 33.15 | **1.80×** | Rzgsw2 |  |
| zig | mul | XP | P-gen | arm64 | thru | 23.01 | libbid | 42.97 | **1.87×** | Rzgsw2 |  |

<!-- END GENERATED mul-rel-zig -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-zig-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | mul | CP | P-gen | x86_64 | thru | 5.97 | libbid | 46.30 | **7.76×** | xRzgsw2 |  |
| zig | mul | WP | P-gen | x86_64 | thru | 28.44 | libbid | 64.78 | **2.28×** | xRzgsw2 |  |
| zig | mul | XP | P-gen | x86_64 | thru | 41.90 | libbid | 93.04 | **2.22×** | xRzgsw2 |  |

<!-- END GENERATED mul-rel-zig-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-zig -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | div | CD | P-gen | arm64 | thru | 28.24 | libbid | 37.45 | **1.33×** | Rzgsw2 |  |
| zig | div | WD | P-gen | arm64 | thru | 38.45 | libbid | 37.57 | **0.98×** | Rzgsw2 |  |
| zig | div | XD | P-gen | arm64 | thru | 29.77 | libbid | 39.17 | **1.32×** | Rzgsw2 |  |
| zig | div | ET | P-gen | arm64 | thru | 10.72 | libbid | 11.67 | **1.09×** | Rzgsw2 |  |
| zig | div | PT | P-gen | arm64 | thru | 4.17 | libbid | 11.43 | **2.74×** | Rzgsw2 |  |

<!-- END GENERATED div-rel-zig -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-zig-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | div | CD | P-gen | x86_64 | thru | 67.93 | libbid | 80.72 | **1.19×** | xRzgsw2 |  |
| zig | div | WD | P-gen | x86_64 | thru | 88.34 | libbid | 80.21 | **0.91×** | xRzgsw2 |  |
| zig | div | XD | P-gen | x86_64 | thru | 77.54 | libbid | 81.28 | **1.05×** | xRzgsw2 |  |
| zig | div | ET | P-gen | x86_64 | thru | 31.58 | libbid | 29.08 | **0.92×** | xRzgsw2 |  |
| zig | div | PT | P-gen | x86_64 | thru | 11.51 | libbid | 29.57 | **2.57×** | xRzgsw2 |  |

<!-- END GENERATED div-rel-zig-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-zig -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | fma | FN | FMA | arm64 | thru | 64.67 | - | - | - | Rzgsw2 |  |
| zig | fma | FF | FMA | arm64 | thru | 42.28 | - | - | - | Rzgsw2 |  |

<!-- END GENERATED fma-rel-zig -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-zig-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | fma | FN | FMA | x86_64 | thru | 112.17 | - | - | - | xRzgsw2 |  |
| zig | fma | FF | FMA | x86_64 | thru | 80.35 | - | - | - | xRzgsw2 |  |

<!-- END GENERATED fma-rel-zig-x86 -->

</div>
