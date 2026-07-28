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
| zig | add | MIX | P-fin | arm64 | thru | 2.02 | libbid | 10.89 | **5.39×** | Rzgsw2 |  |
| zig | sub | MIX | P-fin | arm64 | thru | 2.52 | libbid | 12.78 | **5.07×** | Rzgsw2 |  |
| zig | mul | CP | P-fin | arm64 | thru | 1.44 | libbid | 23.91 | **16.60×** | Rzgsw2 |  |
| zig | mul | WP | P-fin | arm64 | thru | 18.69 | libbid | 34.44 | **1.84×** | Rzgsw2 |  |
| zig | div | CD | P-fin | arm64 | thru | 32.09 | libbid | 36.30 | **1.13×** | Rzgsw2 |  |
| zig | div | WD | P-fin | arm64 | thru | 40.07 | libbid | 39.20 | **0.98×** | Rzgsw2 |  |
| zig | div | ET | P-fin | arm64 | thru | 7.59 | libbid | 6.11 | **0.81×** | Rzgsw2 |  |
| zig | div | PT | P-fin | arm64 | thru | 4.17 | libbid | 6.11 | **1.47×** | Rzgsw2 |  |

<!-- END GENERATED pfin-rel-zig -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-zig-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | add | MIX | P-fin | x86_64 | thru | 6.74 | libbid | 27.25 | **4.04×** | xRzgsw2 |  |
| zig | sub | MIX | P-fin | x86_64 | thru | 7.83 | libbid | 29.07 | **3.71×** | xRzgsw2 |  |
| zig | mul | CP | P-fin | x86_64 | thru | 5.33 | libbid | 43.66 | **8.19×** | xRzgsw2 |  |
| zig | mul | WP | P-fin | x86_64 | thru | 29.00 | libbid | 57.74 | **1.99×** | xRzgsw2 |  |
| zig | div | CD | P-fin | x86_64 | thru | 64.14 | libbid | 74.49 | **1.16×** | xRzgsw2 |  |
| zig | div | WD | P-fin | x86_64 | thru | 88.54 | libbid | 80.94 | **0.91×** | xRzgsw2 |  |
| zig | div | ET | P-fin | x86_64 | thru | 19.73 | libbid | 19.63 | **0.99×** | xRzgsw2 |  |
| zig | div | PT | P-fin | x86_64 | thru | 11.73 | libbid | 19.17 | **1.63×** | xRzgsw2 |  |

<!-- END GENERATED pfin-rel-zig-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-zig -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | add | SQ | P-gen | arm64 | thru | 1.79 | libbid | 7.56 | **4.22×** | Rzgsw2 |  |
| zig | add | NQ | P-gen | arm64 | thru | 6.66 | libbid | 8.57 | **1.29×** | Rzgsw2 |  |
| zig | add | MQ | P-gen | arm64 | thru | 8.54 | libbid | 8.78 | **1.03×** | Rzgsw2 |  |
| zig | add | OQ | P-gen | arm64 | thru | 12.92 | libbid | 14.02 | **1.09×** | Rzgsw2 |  |
| zig | add | FQ | P-gen | arm64 | thru | 8.09 | libbid | 9.39 | **1.16×** | Rzgsw2 |  |

<!-- END GENERATED add-rel-zig -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-zig-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | add | SQ | P-gen | x86_64 | thru | 6.23 | libbid | 29.63 | **4.76×** | xRzgsw2 |  |
| zig | add | NQ | P-gen | x86_64 | thru | 15.14 | libbid | 31.31 | **2.07×** | xRzgsw2 |  |
| zig | add | MQ | P-gen | x86_64 | thru | 20.24 | libbid | 29.79 | **1.47×** | xRzgsw2 |  |
| zig | add | OQ | P-gen | x86_64 | thru | 34.44 | libbid | 45.64 | **1.33×** | xRzgsw2 |  |
| zig | add | FQ | P-gen | x86_64 | thru | 20.52 | libbid | 29.19 | **1.42×** | xRzgsw2 |  |

<!-- END GENERATED add-rel-zig-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-zig -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | sub | SQ | P-gen | arm64 | thru | 1.57 | libbid | 9.27 | **5.90×** | Rzgsw2 |  |
| zig | sub | NQ | P-gen | arm64 | thru | 7.69 | libbid | 10.26 | **1.33×** | Rzgsw2 |  |
| zig | sub | MQ | P-gen | arm64 | thru | 10.12 | libbid | 10.83 | **1.07×** | Rzgsw2 |  |
| zig | sub | OQ | P-gen | arm64 | thru | 13.97 | libbid | 14.74 | **1.06×** | Rzgsw2 |  |
| zig | sub | FQ | P-gen | arm64 | thru | 9.64 | libbid | 10.55 | **1.09×** | Rzgsw2 |  |

<!-- END GENERATED sub-rel-zig -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-zig-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | sub | SQ | P-gen | x86_64 | thru | 5.82 | libbid | 32.65 | **5.61×** | xRzgsw2 |  |
| zig | sub | NQ | P-gen | x86_64 | thru | 15.61 | libbid | 34.71 | **2.22×** | xRzgsw2 |  |
| zig | sub | MQ | P-gen | x86_64 | thru | 20.56 | libbid | 35.56 | **1.73×** | xRzgsw2 |  |
| zig | sub | OQ | P-gen | x86_64 | thru | 34.54 | libbid | 52.33 | **1.52×** | xRzgsw2 |  |
| zig | sub | FQ | P-gen | x86_64 | thru | 20.98 | libbid | 33.88 | **1.61×** | xRzgsw2 |  |

<!-- END GENERATED sub-rel-zig-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-zig -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | mul | CP | P-gen | arm64 | thru | 1.58 | libbid | 24.58 | **15.56×** | Rzgsw2 |  |
| zig | mul | WP | P-gen | arm64 | thru | 18.45 | libbid | 33.28 | **1.80×** | Rzgsw2 |  |
| zig | mul | XP | P-gen | arm64 | thru | 23.04 | libbid | 45.22 | **1.96×** | Rzgsw2 |  |

<!-- END GENERATED mul-rel-zig -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-zig-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | mul | CP | P-gen | x86_64 | thru | 5.90 | libbid | 49.91 | **8.46×** | xRzgsw2 |  |
| zig | mul | WP | P-gen | x86_64 | thru | 28.22 | libbid | 77.04 | **2.73×** | xRzgsw2 |  |
| zig | mul | XP | P-gen | x86_64 | thru | 41.59 | libbid | 97.21 | **2.34×** | xRzgsw2 |  |

<!-- END GENERATED mul-rel-zig-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-zig -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | div | CD | P-gen | arm64 | thru | 27.99 | libbid | 36.64 | **1.31×** | Rzgsw2 |  |
| zig | div | WD | P-gen | arm64 | thru | 38.40 | libbid | 37.56 | **0.98×** | Rzgsw2 |  |
| zig | div | XD | P-gen | arm64 | thru | 29.46 | libbid | 39.18 | **1.33×** | Rzgsw2 |  |
| zig | div | ET | P-gen | arm64 | thru | 10.66 | libbid | 11.64 | **1.09×** | Rzgsw2 |  |
| zig | div | PT | P-gen | arm64 | thru | 4.17 | libbid | 11.54 | **2.77×** | Rzgsw2 |  |

<!-- END GENERATED div-rel-zig -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-zig-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | div | CD | P-gen | x86_64 | thru | 72.31 | libbid | 83.35 | **1.15×** | xRzgsw2 |  |
| zig | div | WD | P-gen | x86_64 | thru | 87.26 | libbid | 85.72 | **0.98×** | xRzgsw2 |  |
| zig | div | XD | P-gen | x86_64 | thru | 72.98 | libbid | 84.67 | **1.16×** | xRzgsw2 |  |
| zig | div | ET | P-gen | x86_64 | thru | 30.74 | libbid | 29.45 | **0.96×** | xRzgsw2 |  |
| zig | div | PT | P-gen | x86_64 | thru | 11.71 | libbid | 29.43 | **2.51×** | xRzgsw2 |  |

<!-- END GENERATED div-rel-zig-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-zig -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | fma | FN | FMA | arm64 | thru | 64.53 | - | - | - | Rzgsw2 |  |
| zig | fma | FF | FMA | arm64 | thru | 42.04 | - | - | - | Rzgsw2 |  |

<!-- END GENERATED fma-rel-zig -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-zig-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zig | fma | FN | FMA | x86_64 | thru | 105.02 | - | - | - | xRzgsw2 |  |
| zig | fma | FF | FMA | x86_64 | thru | 69.69 | - | - | - | xRzgsw2 |  |

<!-- END GENERATED fma-rel-zig-x86 -->

</div>
