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
| zig | add | MIX | P-fin | x86_64 | thru | 10.51 | libbid | 32.11 | **3.06×** | xRzgsw2 |  |
| zig | sub | MIX | P-fin | x86_64 | thru | 8.13 | libbid | 36.74 | **4.52×** | xRzgsw2 |  |
| zig | mul | CP | P-fin | x86_64 | thru | 5.52 | libbid | 46.14 | **8.36×** | xRzgsw2 |  |
| zig | mul | WP | P-fin | x86_64 | thru | 30.27 | libbid | 60.57 | **2.00×** | xRzgsw2 |  |
| zig | div | CD | P-fin | x86_64 | thru | 68.19 | libbid | 78.27 | **1.15×** | xRzgsw2 |  |
| zig | div | WD | P-fin | x86_64 | thru | 93.67 | libbid | 82.95 | **0.89×** | xRzgsw2 |  |
| zig | div | ET | P-fin | x86_64 | thru | 21.12 | libbid | 19.44 | **0.92×** | xRzgsw2 |  |
| zig | div | PT | P-fin | x86_64 | thru | 11.82 | libbid | 19.26 | **1.63×** | xRzgsw2 |  |

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
| zig | add | SQ | P-gen | x86_64 | thru | 9.69 | libbid | 30.55 | **3.15×** | xRzgsw2 |  |
| zig | add | NQ | P-gen | x86_64 | thru | 14.88 | libbid | 32.21 | **2.16×** | xRzgsw2 |  |
| zig | add | MQ | P-gen | x86_64 | thru | 19.92 | libbid | 31.68 | **1.59×** | xRzgsw2 |  |
| zig | add | OQ | P-gen | x86_64 | thru | 34.87 | libbid | 47.35 | **1.36×** | xRzgsw2 |  |
| zig | add | FQ | P-gen | x86_64 | thru | 20.60 | libbid | 30.07 | **1.46×** | xRzgsw2 |  |

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
| zig | sub | SQ | P-gen | x86_64 | thru | 6.02 | libbid | 35.44 | **5.89×** | xRzgsw2 |  |
| zig | sub | NQ | P-gen | x86_64 | thru | 16.04 | libbid | 37.04 | **2.31×** | xRzgsw2 |  |
| zig | sub | MQ | P-gen | x86_64 | thru | 22.06 | libbid | 35.97 | **1.63×** | xRzgsw2 |  |
| zig | sub | OQ | P-gen | x86_64 | thru | 37.20 | libbid | 51.86 | **1.39×** | xRzgsw2 |  |
| zig | sub | FQ | P-gen | x86_64 | thru | 23.34 | libbid | 34.95 | **1.50×** | xRzgsw2 |  |

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
| zig | mul | CP | P-gen | x86_64 | thru | 6.14 | libbid | 46.33 | **7.55×** | xRzgsw2 |  |
| zig | mul | WP | P-gen | x86_64 | thru | 29.31 | libbid | 67.28 | **2.30×** | xRzgsw2 |  |
| zig | mul | XP | P-gen | x86_64 | thru | 43.85 | libbid | 95.35 | **2.17×** | xRzgsw2 |  |

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
| zig | div | CD | P-gen | x86_64 | thru | 72.08 | libbid | 82.56 | **1.15×** | xRzgsw2 |  |
| zig | div | WD | P-gen | x86_64 | thru | 91.94 | libbid | 87.22 | **0.95×** | xRzgsw2 |  |
| zig | div | XD | P-gen | x86_64 | thru | 77.11 | libbid | 86.84 | **1.13×** | xRzgsw2 |  |
| zig | div | ET | P-gen | x86_64 | thru | 33.29 | libbid | 30.95 | **0.93×** | xRzgsw2 |  |
| zig | div | PT | P-gen | x86_64 | thru | 11.84 | libbid | 31.12 | **2.63×** | xRzgsw2 |  |

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
| zig | fma | FN | FMA | x86_64 | thru | 116.12 | - | - | - | xRzgsw2 |  |
| zig | fma | FF | FMA | x86_64 | thru | 83.12 | - | - | - | xRzgsw2 |  |

<!-- END GENERATED fma-rel-zig-x86 -->

</div>
