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

Each row below is the ratio for that reference/idiom peer on x86_64 (Intel i9-9880H): `ratio = rust_decimal / Miguel` or `ratio = libbid / Miguel` (&gt; 1× ⇒ d128 faster), broken out by operation. `rust_decimal` has no wide-product multiply band (that falls back to libbid), and libbid isn't used for add/subtract/divide, so those cells are blank.

| | Add | Subtract | Multiply | Divide |
|---|---|---|---|---|
| ratio = rust_decimal / Miguel | 1.6× | 1.9× | — | 0.6× – 5× |
| ratio = libbid / Miguel | — | — | 2.0× – 15× | — |

## FinMix — realistic financial mix (P-fin)

The headline: one realistic 64-bit financial operation mix — a `MIX` add/sub stream, mul `CP`/`WP`, div `CD`/`WD`/`ET`/`PT` — `ratio = alt / Miguel` (&gt; 1 ⇒ d128 faster). This is the profile closest to real financial code.

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED pfin-rel-rust -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | add | MIX | P-fin | arm64 | thru | 2.01 | rust_decimal | 3.36 | **1.67×** | Rrsw2 | compact idiom peer |
| rust | sub | MIX | P-fin | arm64 | thru | 2.20 | rust_decimal | 3.55 | **1.61×** | Rrsw2 | compact idiom peer |
| rust | div | CD | P-fin | arm64 | thru | 20.82 | rust_decimal | 13.90 | **0.67×** | Rrsw2 | compact idiom peer |
| rust | div | WD | P-fin | arm64 | thru | 38.54 | rust_decimal | 20.09 | **0.52×** | Rrsw2 | compact idiom peer |
| rust | div | ET | P-fin | arm64 | thru | 6.27 | rust_decimal | 3.84 | **0.61×** | Rrsw2 | compact idiom peer |
| rust | div | PT | P-fin | arm64 | thru | 4.00 | rust_decimal | 15.34 | **3.83×** | Rrsw2 | compact idiom peer |
| rust | mul | CP | P-fin | arm64 | thru | 1.13 | libbid | 23.57 | **20.86×** | Rrsw2 |  |
| rust | mul | WP | P-fin | arm64 | thru | 14.43 | libbid | 34.52 | **2.39×** | Rrsw2 |  |

<!-- END GENERATED pfin-rel-rust -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-rust-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | add | MIX | P-fin | x86_64 | thru | 6.33 | rust_decimal | 13.42 | **2.12×** | xRrsw2 | compact idiom peer |
| rust | sub | MIX | P-fin | x86_64 | thru | 7.46 | rust_decimal | 14.60 | **1.96×** | xRrsw2 | compact idiom peer |
| rust | div | CD | P-fin | x86_64 | thru | 72.57 | rust_decimal | 55.28 | **0.76×** | xRrsw2 | compact idiom peer |
| rust | div | WD | P-fin | x86_64 | thru | 86.93 | rust_decimal | 74.22 | **0.85×** | xRrsw2 | compact idiom peer |
| rust | div | ET | P-fin | x86_64 | thru | 23.12 | rust_decimal | 14.30 | **0.62×** | xRrsw2 | compact idiom peer |
| rust | div | PT | P-fin | x86_64 | thru | 9.73 | rust_decimal | 50.79 | **5.22×** | xRrsw2 | compact idiom peer |
| rust | mul | CP | P-fin | x86_64 | thru | 3.40 | libbid | 44.36 | **13.05×** | xRrsw2 |  |
| rust | mul | WP | P-fin | x86_64 | thru | 29.54 | libbid | 57.85 | **1.96×** | xRrsw2 |  |

<!-- END GENERATED pfin-rel-rust-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-rust -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | add | SQss | P-gen | arm64 | thru | 0.81 | rust_decimal | 3.82 | **4.72×** | Rrsw2 | compact idiom peer |
| rust | add | SQos | P-gen | arm64 | thru | 2.00 | rust_decimal | 3.41 | **1.71×** | Rrsw2 | compact idiom peer |
| rust | add | NQss | P-gen | arm64 | thru | 3.37 | rust_decimal | 5.67 | **1.68×** | Rrsw2 | compact idiom peer |
| rust | add | NQos | P-gen | arm64 | thru | 3.76 | rust_decimal | 5.11 | **1.36×** | Rrsw2 | compact idiom peer |
| rust | add | MQss | P-gen | arm64 | thru | 5.22 | rust_decimal | 6.11 | **1.17×** | Rrsw2 | compact idiom peer |
| rust | add | MQos | P-gen | arm64 | thru | 11.25 | rust_decimal | 5.52 | **0.49×** | Rrsw2 | compact idiom peer |
| rust | add | OQss | P-gen | arm64 | thru | 9.06 | - | - | - | Rrsw2 |  |
| rust | add | OQos | P-gen | arm64 | thru | 13.78 | - | - | - | Rrsw2 |  |
| rust | add | FQss | P-gen | arm64 | thru | 8.41 | - | - | - | Rrsw2 |  |
| rust | add | FQos | P-gen | arm64 | thru | 10.25 | - | - | - | Rrsw2 |  |

<!-- END GENERATED add-rel-rust -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-rust-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | add | SQss | P-gen | x86_64 | thru | 2.01 | rust_decimal | 12.66 | **6.30×** | xRrsw2 | compact idiom peer |
| rust | add | SQos | P-gen | x86_64 | thru | 5.22 | rust_decimal | 15.50 | **2.97×** | xRrsw2 | compact idiom peer |
| rust | add | NQss | P-gen | x86_64 | thru | 10.75 | rust_decimal | 18.18 | **1.69×** | xRrsw2 | compact idiom peer |
| rust | add | NQos | P-gen | x86_64 | thru | 10.67 | rust_decimal | 18.95 | **1.78×** | xRrsw2 | compact idiom peer |
| rust | add | MQss | P-gen | x86_64 | thru | 13.32 | rust_decimal | 18.79 | **1.41×** | xRrsw2 | compact idiom peer |
| rust | add | MQos | P-gen | x86_64 | thru | 24.87 | rust_decimal | 19.29 | **0.78×** | xRrsw2 | compact idiom peer |
| rust | add | OQss | P-gen | x86_64 | thru | 29.93 | - | - | - | xRrsw2 |  |
| rust | add | OQos | P-gen | x86_64 | thru | 41.69 | - | - | - | xRrsw2 |  |
| rust | add | FQss | P-gen | x86_64 | thru | 18.73 | - | - | - | xRrsw2 |  |
| rust | add | FQos | P-gen | x86_64 | thru | 22.87 | - | - | - | xRrsw2 |  |

<!-- END GENERATED add-rel-rust-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-rust -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | sub | SQss | P-gen | arm64 | thru | 1.36 | rust_decimal | 3.27 | **2.40×** | Rrsw2 | compact idiom peer |
| rust | sub | SQos | P-gen | arm64 | thru | 1.06 | rust_decimal | 4.39 | **4.14×** | Rrsw2 | compact idiom peer |
| rust | sub | NQss | P-gen | arm64 | thru | 3.74 | rust_decimal | 5.10 | **1.36×** | Rrsw2 | compact idiom peer |
| rust | sub | NQos | P-gen | arm64 | thru | 3.45 | rust_decimal | 5.52 | **1.60×** | Rrsw2 | compact idiom peer |
| rust | sub | MQss | P-gen | arm64 | thru | 11.32 | rust_decimal | 5.48 | **0.48×** | Rrsw2 | compact idiom peer |
| rust | sub | MQos | P-gen | arm64 | thru | 5.08 | rust_decimal | 6.16 | **1.21×** | Rrsw2 | compact idiom peer |
| rust | sub | OQss | P-gen | arm64 | thru | 13.44 | - | - | - | Rrsw2 |  |
| rust | sub | OQos | P-gen | arm64 | thru | 9.05 | - | - | - | Rrsw2 |  |
| rust | sub | FQss | P-gen | arm64 | thru | 9.95 | - | - | - | Rrsw2 |  |
| rust | sub | FQos | P-gen | arm64 | thru | 8.06 | - | - | - | Rrsw2 |  |

<!-- END GENERATED sub-rel-rust -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-rust-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | sub | SQss | P-gen | x86_64 | thru | 4.47 | rust_decimal | 14.06 | **3.15×** | xRrsw2 | compact idiom peer |
| rust | sub | SQos | P-gen | x86_64 | thru | 3.25 | rust_decimal | 13.52 | **4.16×** | xRrsw2 | compact idiom peer |
| rust | sub | NQss | P-gen | x86_64 | thru | 10.67 | rust_decimal | 17.95 | **1.68×** | xRrsw2 | compact idiom peer |
| rust | sub | NQos | P-gen | x86_64 | thru | 9.86 | rust_decimal | 16.40 | **1.66×** | xRrsw2 | compact idiom peer |
| rust | sub | MQss | P-gen | x86_64 | thru | 23.60 | rust_decimal | 17.36 | **0.74×** | xRrsw2 | compact idiom peer |
| rust | sub | MQos | P-gen | x86_64 | thru | 13.66 | rust_decimal | 16.93 | **1.24×** | xRrsw2 | compact idiom peer |
| rust | sub | OQss | P-gen | x86_64 | thru | 41.21 | - | - | - | xRrsw2 |  |
| rust | sub | OQos | P-gen | x86_64 | thru | 30.02 | - | - | - | xRrsw2 |  |
| rust | sub | FQss | P-gen | x86_64 | thru | 23.13 | - | - | - | xRrsw2 |  |
| rust | sub | FQos | P-gen | x86_64 | thru | 17.91 | - | - | - | xRrsw2 |  |

<!-- END GENERATED sub-rel-rust-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-rust -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | mul | CP | P-gen | arm64 | thru | 1.52 | libbid | 23.13 | **15.22×** | Rrsw2 |  |
| rust | mul | WP | P-gen | arm64 | thru | 13.81 | libbid | 35.06 | **2.54×** | Rrsw2 |  |
| rust | mul | XP | P-gen | arm64 | thru | 25.03 | libbid | 45.24 | **1.81×** | Rrsw2 |  |

<!-- END GENERATED mul-rel-rust -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-rust-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | mul | CP | P-gen | x86_64 | thru | 5.46 | libbid | 45.57 | **8.35×** | xRrsw2 |  |
| rust | mul | WP | P-gen | x86_64 | thru | 29.98 | libbid | 64.59 | **2.15×** | xRrsw2 |  |
| rust | mul | XP | P-gen | x86_64 | thru | 43.70 | libbid | 93.63 | **2.14×** | xRrsw2 |  |

<!-- END GENERATED mul-rel-rust-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-rust -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | div | CD | P-gen | arm64 | thru | 20.04 | libbid | 36.77 | **1.83×** | Rrsw2 |  |
| rust | div | WD | P-gen | arm64 | thru | 37.80 | libbid | 37.54 | **0.99×** | Rrsw2 |  |
| rust | div | XD | P-gen | arm64 | thru | 37.84 | libbid | 38.97 | **1.03×** | Rrsw2 |  |
| rust | div | ET | P-gen | arm64 | thru | 9.60 | libbid | 11.68 | **1.22×** | Rrsw2 |  |
| rust | div | PT | P-gen | arm64 | thru | 3.99 | libbid | 11.45 | **2.87×** | Rrsw2 |  |

<!-- END GENERATED div-rel-rust -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-rust-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | div | CD | P-gen | x86_64 | thru | 77.73 | libbid | 81.20 | **1.04×** | xRrsw2 |  |
| rust | div | WD | P-gen | x86_64 | thru | 84.82 | libbid | 82.98 | **0.98×** | xRrsw2 |  |
| rust | div | XD | P-gen | x86_64 | thru | 84.40 | libbid | 82.60 | **0.98×** | xRrsw2 |  |
| rust | div | ET | P-gen | x86_64 | thru | 28.97 | libbid | 29.87 | **1.03×** | xRrsw2 |  |
| rust | div | PT | P-gen | x86_64 | thru | 9.49 | libbid | 30.17 | **3.18×** | xRrsw2 |  |

<!-- END GENERATED div-rel-rust-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-rust -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | fma | FN | FMA | arm64 | thru | 22.84 | - | - | - | Rrsw2 |  |
| rust | fma | FF | FMA | arm64 | thru | 35.77 | - | - | - | Rrsw2 |  |

<!-- END GENERATED fma-rel-rust -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-rust-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | fma | FN | FMA | x86_64 | thru | 60.95 | - | - | - | xRrsw2 |  |
| rust | fma | FF | FMA | x86_64 | thru | 68.80 | - | - | - | xRrsw2 |  |

<!-- END GENERATED fma-rel-rust-x86 -->

</div>
