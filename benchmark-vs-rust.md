---
layout: default
permalink: /benchmark/vs-rust.html
title: "Rust Benchmark Results — Decimal128"
description: "decimal128 in Rust, measured against the alternatives available to it — a realistic financial mix (P-fin) plus per-operation band characterization, with explicit ratios."
heading: "Rust Benchmark Results"
---

<div class="whitepaper" markdown="1">

<p class="whitepaper-meta">Living document — as-measured results. Category codes, profiles, modes &amp; method: <a href="key.html">Benchmark Key</a>.</p>

This is the **Rust** view of decimal128 **as-measured**, band by band, with explicit ratios. It opens with the realistic financial-mix (**P-fin**) headline, then the per-operation band characterization (**P-gen**) and FMA. In Rust, d128 is measured against its in-language idiom peer **`rust_decimal`** on the compact bands it can represent, falling back to the **libbid** universal reference where it cannot (wide products, XD). It is **data only** — the categories, magnitude profiles, units, and methodology are defined in the [Benchmark Key](key.html) (and, authoritatively, `BenchmarkMatrix.md`). The cross-port d128 band-shape matrices (all ports, no alternatives) live in [Port-Comparison Benchmark Results](port-compare.html); the full index of per-language pages is on the [Benchmarks](/benchmarks.html) hub.

## Summary — Ratio Range by Operation

A quick-glance rollup before the detailed tables below: the min–max `ratio = alt / ours` (&gt; 1× ⇒ d128 faster) for each operation on x86_64 (Intel i9-9880H), across both reference/idiom peers measured for Rust (`rust_decimal`, libbid), split by profile.

| Operation | P-fin range | P-gen range | FMA range |
|---|---|---|---|
| Add | 1.55× | 0.81× – 1.88× | — |
| Subtract | 1.87× | 0.74× – 1.87× | — |
| Multiply | 2.02× – 14.97× | 2.15× – 9.04× | — |
| Divide | 0.61× – 5.30× | 0.97× – 3.14× | — |
| FMA | — | — | 1.83× – 2.57× |

## FinMix — realistic financial mix (P-fin)

The headline: one realistic 64-bit financial operation mix — a `MIX` add/sub stream, mul `CP`/`WP`, div `CD`/`WD`/`ET`/`PT` — `ratio = alt / ours` (&gt; 1 ⇒ d128 faster). This is the profile closest to real financial code.

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED pfin-rel-rust -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | add | MIX | P-fin | arm64 | thru | 3.12 | rust_decimal | 3.76 | **1.21×** | Rrsw2 | compact idiom peer |
| rust | sub | MIX | P-fin | arm64 | thru | 2.47 | rust_decimal | 3.71 | **1.50×** | Rrsw2 | compact idiom peer |
| rust | div | CD | P-fin | arm64 | thru | 27.23 | rust_decimal | 14.40 | **0.53×** | Rrsw2 | compact idiom peer |
| rust | div | WD | P-fin | arm64 | thru | 34.43 | rust_decimal | 19.98 | **0.58×** | Rrsw2 | compact idiom peer |
| rust | div | ET | P-fin | arm64 | thru | 6.20 | rust_decimal | 3.85 | **0.62×** | Rrsw2 | compact idiom peer |
| rust | div | PT | P-fin | arm64 | thru | 3.98 | rust_decimal | 15.14 | **3.80×** | Rrsw2 | compact idiom peer |
| rust | mul | CP | P-fin | arm64 | thru | 1.12 | libbid | 23.69 | **21.15×** | Rrsw2 |  |
| rust | mul | WP | P-fin | arm64 | thru | 15.10 | libbid | 34.45 | **2.28×** | Rrsw2 |  |

<!-- END GENERATED pfin-rel-rust -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-rust-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | add | MIX | P-fin | x86_64 | thru | 9.63 | rust_decimal | 14.96 | **1.55×** | xRrsw2 | compact idiom peer |
| rust | sub | MIX | P-fin | x86_64 | thru | 8.01 | rust_decimal | 14.97 | **1.87×** | xRrsw2 | compact idiom peer |
| rust | div | CD | P-fin | x86_64 | thru | 71.07 | rust_decimal | 55.38 | **0.78×** | xRrsw2 | compact idiom peer |
| rust | div | WD | P-fin | x86_64 | thru | 89.09 | rust_decimal | 75.51 | **0.85×** | xRrsw2 | compact idiom peer |
| rust | div | ET | P-fin | x86_64 | thru | 22.70 | rust_decimal | 13.95 | **0.61×** | xRrsw2 | compact idiom peer |
| rust | div | PT | P-fin | x86_64 | thru | 9.77 | rust_decimal | 51.76 | **5.30×** | xRrsw2 | compact idiom peer |
| rust | mul | CP | P-fin | x86_64 | thru | 3.15 | libbid | 47.15 | **14.97×** | xRrsw2 |  |
| rust | mul | WP | P-fin | x86_64 | thru | 29.80 | libbid | 60.29 | **2.02×** | xRrsw2 |  |

<!-- END GENERATED pfin-rel-rust-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-rust -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | add | SQ | P-gen | arm64 | thru | 2.73 | rust_decimal | 3.49 | **1.28×** | Rrsw2 | compact idiom peer |
| rust | add | NQ | P-gen | arm64 | thru | 4.97 | rust_decimal | 5.54 | **1.11×** | Rrsw2 | compact idiom peer |
| rust | add | MQ | P-gen | arm64 | thru | 13.87 | rust_decimal | 5.69 | **0.41×** | Rrsw2 | compact idiom peer |
| rust | add | OQ | P-gen | arm64 | thru | 10.88 | - | - | - | Rrsw2 |  |
| rust | add | FQ | P-gen | arm64 | thru | 6.65 | - | - | - | Rrsw2 |  |

<!-- END GENERATED add-rel-rust -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-rust-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | add | SQ | P-gen | x86_64 | thru | 8.41 | rust_decimal | 15.83 | **1.88×** | xRrsw2 | compact idiom peer |
| rust | add | NQ | P-gen | x86_64 | thru | 12.40 | rust_decimal | 20.60 | **1.66×** | xRrsw2 | compact idiom peer |
| rust | add | MQ | P-gen | x86_64 | thru | 24.95 | rust_decimal | 20.29 | **0.81×** | xRrsw2 | compact idiom peer |
| rust | add | OQ | P-gen | x86_64 | thru | 37.99 | - | - | - | xRrsw2 |  |
| rust | add | FQ | P-gen | x86_64 | thru | 21.35 | - | - | - | xRrsw2 |  |

<!-- END GENERATED add-rel-rust-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-rust -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | sub | SQ | P-gen | arm64 | thru | 1.75 | rust_decimal | 3.52 | **2.01×** | Rrsw2 | compact idiom peer |
| rust | sub | NQ | P-gen | arm64 | thru | 5.14 | rust_decimal | 5.49 | **1.07×** | Rrsw2 | compact idiom peer |
| rust | sub | MQ | P-gen | arm64 | thru | 14.49 | rust_decimal | 5.71 | **0.39×** | Rrsw2 | compact idiom peer |
| rust | sub | OQ | P-gen | arm64 | thru | 10.97 | - | - | - | Rrsw2 |  |
| rust | sub | FQ | P-gen | arm64 | thru | 6.66 | - | - | - | Rrsw2 |  |

<!-- END GENERATED sub-rel-rust -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-rust-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | sub | SQ | P-gen | x86_64 | thru | 7.77 | rust_decimal | 14.52 | **1.87×** | xRrsw2 | compact idiom peer |
| rust | sub | NQ | P-gen | x86_64 | thru | 13.74 | rust_decimal | 19.94 | **1.45×** | xRrsw2 | compact idiom peer |
| rust | sub | MQ | P-gen | x86_64 | thru | 26.44 | rust_decimal | 19.51 | **0.74×** | xRrsw2 | compact idiom peer |
| rust | sub | OQ | P-gen | x86_64 | thru | 39.48 | - | - | - | xRrsw2 |  |
| rust | sub | FQ | P-gen | x86_64 | thru | 24.08 | - | - | - | xRrsw2 |  |

<!-- END GENERATED sub-rel-rust-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-rust -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | mul | CP | P-gen | arm64 | thru | 1.56 | libbid | 24.24 | **15.54×** | Rrsw2 |  |
| rust | mul | WP | P-gen | arm64 | thru | 14.17 | libbid | 33.43 | **2.36×** | Rrsw2 |  |
| rust | mul | XP | P-gen | arm64 | thru | 25.22 | libbid | 44.63 | **1.77×** | Rrsw2 |  |

<!-- END GENERATED mul-rel-rust -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-rust-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | mul | CP | P-gen | x86_64 | thru | 5.24 | libbid | 47.38 | **9.04×** | xRrsw2 |  |
| rust | mul | WP | P-gen | x86_64 | thru | 30.70 | libbid | 65.94 | **2.15×** | xRrsw2 |  |
| rust | mul | XP | P-gen | x86_64 | thru | 44.65 | libbid | 96.66 | **2.16×** | xRrsw2 |  |

<!-- END GENERATED mul-rel-rust-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-rust -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | div | CD | P-gen | arm64 | thru | 26.16 | libbid | 36.61 | **1.40×** | Rrsw2 |  |
| rust | div | WD | P-gen | arm64 | thru | 35.28 | libbid | 37.71 | **1.07×** | Rrsw2 |  |
| rust | div | XD | P-gen | arm64 | thru | 39.49 | libbid | 40.43 | **1.02×** | Rrsw2 |  |
| rust | div | ET | P-gen | arm64 | thru | 9.49 | libbid | 11.57 | **1.22×** | Rrsw2 |  |
| rust | div | PT | P-gen | arm64 | thru | 3.98 | libbid | 11.42 | **2.87×** | Rrsw2 |  |

<!-- END GENERATED div-rel-rust -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-rust-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | div | CD | P-gen | x86_64 | thru | 73.19 | libbid | 82.50 | **1.13×** | xRrsw2 |  |
| rust | div | WD | P-gen | x86_64 | thru | 86.65 | libbid | 84.36 | **0.97×** | xRrsw2 |  |
| rust | div | XD | P-gen | x86_64 | thru | 86.15 | libbid | 84.37 | **0.98×** | xRrsw2 |  |
| rust | div | ET | P-gen | x86_64 | thru | 29.09 | libbid | 30.87 | **1.06×** | xRrsw2 |  |
| rust | div | PT | P-gen | x86_64 | thru | 9.89 | libbid | 31.09 | **3.14×** | xRrsw2 |  |

<!-- END GENERATED div-rel-rust-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-rust -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | fma | FN | FMA | arm64 | thru | 23.03 | libbid | 82.34 | **3.58×** | Rrsw2 |  |
| rust | fma | FF | FMA | arm64 | thru | 33.57 | libbid | 59.70 | **1.78×** | Rrsw2 |  |

<!-- END GENERATED fma-rel-rust -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-rust-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | fma | FN | FMA | x86_64 | thru | 62.90 | libbid | 161.79 | **2.57×** | xRrsw2 |  |
| rust | fma | FF | FMA | x86_64 | thru | 67.82 | libbid | 124.13 | **1.83×** | xRrsw2 |  |

<!-- END GENERATED fma-rel-rust-x86 -->

</div>
