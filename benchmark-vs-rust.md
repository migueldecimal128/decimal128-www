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
| ratio = rust_decimal / Miguel | 2.1× | 1.9× | — | 0.6× – 5× |
| ratio = libbid / Miguel | — | — | 2.0× – 13× | — |

## FinMix — realistic financial mix (P-fin)

The headline: one realistic 64-bit financial operation mix — a `MIX` add/sub stream, mul `CP`/`WP`, div `CD`/`WD`/`ET`/`PT` — `ratio = alt / Miguel` (&gt; 1 ⇒ d128 faster). This is the profile closest to real financial code.

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED pfin-rel-rust -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | add | MIX | P-fin | arm64 | thru | 1.97 | rust_decimal | 3.36 | **1.71×** | Rrsw2 | compact idiom peer |
| rust | sub | MIX | P-fin | arm64 | thru | 2.22 | rust_decimal | 3.63 | **1.64×** | Rrsw2 | compact idiom peer |
| rust | div | CD | P-fin | arm64 | thru | 21.38 | rust_decimal | 16.72 | **0.78×** | Rrsw2 | compact idiom peer |
| rust | div | WD | P-fin | arm64 | thru | 34.16 | rust_decimal | 20.29 | **0.59×** | Rrsw2 | compact idiom peer |
| rust | div | ET | P-fin | arm64 | thru | 6.24 | rust_decimal | 3.77 | **0.60×** | Rrsw2 | compact idiom peer |
| rust | div | PT | P-fin | arm64 | thru | 3.97 | rust_decimal | 14.94 | **3.76×** | Rrsw2 | compact idiom peer |
| rust | mul | CP | P-fin | arm64 | thru | 1.11 | libbid | 24.62 | **22.18×** | Rrsw2 |  |
| rust | mul | WP | P-fin | arm64 | thru | 14.91 | libbid | 34.03 | **2.28×** | Rrsw2 |  |

<!-- END GENERATED pfin-rel-rust -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-rust-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | add | MIX | P-fin | x86_64 | thru | 6.85 | rust_decimal | 14.88 | **2.17×** | xRrsw2 | compact idiom peer |
| rust | sub | MIX | P-fin | x86_64 | thru | 8.30 | rust_decimal | 15.96 | **1.92×** | xRrsw2 | compact idiom peer |
| rust | div | CD | P-fin | x86_64 | thru | 77.86 | rust_decimal | 59.10 | **0.76×** | xRrsw2 | compact idiom peer |
| rust | div | WD | P-fin | x86_64 | thru | 93.58 | rust_decimal | 79.71 | **0.85×** | xRrsw2 | compact idiom peer |
| rust | div | ET | P-fin | x86_64 | thru | 25.17 | rust_decimal | 15.46 | **0.61×** | xRrsw2 | compact idiom peer |
| rust | div | PT | P-fin | x86_64 | thru | 10.78 | rust_decimal | 55.19 | **5.12×** | xRrsw2 | compact idiom peer |
| rust | mul | CP | P-fin | x86_64 | thru | 3.85 | libbid | 50.91 | **13.22×** | xRrsw2 |  |
| rust | mul | WP | P-fin | x86_64 | thru | 32.72 | libbid | 66.63 | **2.04×** | xRrsw2 |  |

<!-- END GENERATED pfin-rel-rust-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-rust -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | add | SQss | P-gen | arm64 | thru | 0.81 | rust_decimal | 3.84 | **4.74×** | Rrsw2 | compact idiom peer |
| rust | add | SQos | P-gen | arm64 | thru | 2.14 | rust_decimal | 4.52 | **2.11×** | Rrsw2 | compact idiom peer |
| rust | add | NQss | P-gen | arm64 | thru | 3.45 | rust_decimal | 5.87 | **1.70×** | Rrsw2 | compact idiom peer |
| rust | add | NQos | P-gen | arm64 | thru | 3.77 | rust_decimal | 5.19 | **1.38×** | Rrsw2 | compact idiom peer |
| rust | add | MQss | P-gen | arm64 | thru | 5.17 | rust_decimal | 6.24 | **1.21×** | Rrsw2 | compact idiom peer |
| rust | add | MQos | P-gen | arm64 | thru | 11.38 | rust_decimal | 5.62 | **0.49×** | Rrsw2 | compact idiom peer |
| rust | add | OQss | P-gen | arm64 | thru | 9.41 | - | - | - | Rrsw2 |  |
| rust | add | OQos | P-gen | arm64 | thru | 12.81 | - | - | - | Rrsw2 |  |
| rust | add | FQss | P-gen | arm64 | thru | 8.45 | - | - | - | Rrsw2 |  |
| rust | add | FQos | P-gen | arm64 | thru | 10.03 | - | - | - | Rrsw2 |  |

<!-- END GENERATED add-rel-rust -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-rust-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | add | SQss | P-gen | x86_64 | thru | 2.53 | rust_decimal | 14.21 | **5.62×** | xRrsw2 | compact idiom peer |
| rust | add | SQos | P-gen | x86_64 | thru | 6.59 | rust_decimal | 18.49 | **2.81×** | xRrsw2 | compact idiom peer |
| rust | add | NQss | P-gen | x86_64 | thru | 11.20 | rust_decimal | 21.32 | **1.90×** | xRrsw2 | compact idiom peer |
| rust | add | NQos | P-gen | x86_64 | thru | 11.45 | rust_decimal | 22.93 | **2.00×** | xRrsw2 | compact idiom peer |
| rust | add | MQss | P-gen | x86_64 | thru | 14.54 | rust_decimal | 20.40 | **1.40×** | xRrsw2 | compact idiom peer |
| rust | add | MQos | P-gen | x86_64 | thru | 26.48 | rust_decimal | 20.41 | **0.77×** | xRrsw2 | compact idiom peer |
| rust | add | OQss | P-gen | x86_64 | thru | 32.30 | - | - | - | xRrsw2 |  |
| rust | add | OQos | P-gen | x86_64 | thru | 44.79 | - | - | - | xRrsw2 |  |
| rust | add | FQss | P-gen | x86_64 | thru | 20.10 | - | - | - | xRrsw2 |  |
| rust | add | FQos | P-gen | x86_64 | thru | 24.88 | - | - | - | xRrsw2 |  |

<!-- END GENERATED add-rel-rust-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-rust -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | sub | SQss | P-gen | arm64 | thru | 1.36 | rust_decimal | 3.52 | **2.59×** | Rrsw2 | compact idiom peer |
| rust | sub | SQos | P-gen | arm64 | thru | 1.06 | rust_decimal | 4.34 | **4.09×** | Rrsw2 | compact idiom peer |
| rust | sub | NQss | P-gen | arm64 | thru | 3.73 | rust_decimal | 5.21 | **1.40×** | Rrsw2 | compact idiom peer |
| rust | sub | NQos | P-gen | arm64 | thru | 3.45 | rust_decimal | 5.49 | **1.59×** | Rrsw2 | compact idiom peer |
| rust | sub | MQss | P-gen | arm64 | thru | 11.29 | rust_decimal | 5.53 | **0.49×** | Rrsw2 | compact idiom peer |
| rust | sub | MQos | P-gen | arm64 | thru | 5.13 | rust_decimal | 6.06 | **1.18×** | Rrsw2 | compact idiom peer |
| rust | sub | OQss | P-gen | arm64 | thru | 13.99 | - | - | - | Rrsw2 |  |
| rust | sub | OQos | P-gen | arm64 | thru | 9.20 | - | - | - | Rrsw2 |  |
| rust | sub | FQss | P-gen | arm64 | thru | 9.89 | - | - | - | Rrsw2 |  |
| rust | sub | FQos | P-gen | arm64 | thru | 8.00 | - | - | - | Rrsw2 |  |

<!-- END GENERATED sub-rel-rust -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-rust-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | sub | SQss | P-gen | x86_64 | thru | 5.08 | rust_decimal | 15.58 | **3.07×** | xRrsw2 | compact idiom peer |
| rust | sub | SQos | P-gen | x86_64 | thru | 4.03 | rust_decimal | 15.07 | **3.74×** | xRrsw2 | compact idiom peer |
| rust | sub | NQss | P-gen | x86_64 | thru | 11.41 | rust_decimal | 19.36 | **1.70×** | xRrsw2 | compact idiom peer |
| rust | sub | NQos | P-gen | x86_64 | thru | 10.86 | rust_decimal | 18.69 | **1.72×** | xRrsw2 | compact idiom peer |
| rust | sub | MQss | P-gen | x86_64 | thru | 25.85 | rust_decimal | 19.03 | **0.74×** | xRrsw2 | compact idiom peer |
| rust | sub | MQos | P-gen | x86_64 | thru | 14.91 | rust_decimal | 18.73 | **1.26×** | xRrsw2 | compact idiom peer |
| rust | sub | OQss | P-gen | x86_64 | thru | 43.96 | - | - | - | xRrsw2 |  |
| rust | sub | OQos | P-gen | x86_64 | thru | 32.49 | - | - | - | xRrsw2 |  |
| rust | sub | FQss | P-gen | x86_64 | thru | 24.65 | - | - | - | xRrsw2 |  |
| rust | sub | FQos | P-gen | x86_64 | thru | 19.85 | - | - | - | xRrsw2 |  |

<!-- END GENERATED sub-rel-rust-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-rust -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | mul | CP | P-gen | arm64 | thru | 1.52 | libbid | 24.33 | **16.01×** | Rrsw2 |  |
| rust | mul | WP | P-gen | arm64 | thru | 13.80 | libbid | 34.83 | **2.52×** | Rrsw2 |  |
| rust | mul | XP | P-gen | arm64 | thru | 25.08 | libbid | 45.16 | **1.80×** | Rrsw2 |  |

<!-- END GENERATED mul-rel-rust -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-rust-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | mul | CP | P-gen | x86_64 | thru | 6.07 | libbid | 50.55 | **8.33×** | xRrsw2 |  |
| rust | mul | WP | P-gen | x86_64 | thru | 32.36 | libbid | 73.62 | **2.28×** | xRrsw2 |  |
| rust | mul | XP | P-gen | x86_64 | thru | 46.76 | libbid | 104.96 | **2.24×** | xRrsw2 |  |

<!-- END GENERATED mul-rel-rust-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-rust -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | div | CD | P-gen | arm64 | thru | 21.10 | libbid | 37.59 | **1.78×** | Rrsw2 |  |
| rust | div | WD | P-gen | arm64 | thru | 34.40 | libbid | 37.36 | **1.09×** | Rrsw2 |  |
| rust | div | XD | P-gen | arm64 | thru | 40.43 | libbid | 38.86 | **0.96×** | Rrsw2 |  |
| rust | div | ET | P-gen | arm64 | thru | 9.68 | libbid | 11.94 | **1.23×** | Rrsw2 |  |
| rust | div | PT | P-gen | arm64 | thru | 3.98 | libbid | 11.50 | **2.89×** | Rrsw2 |  |

<!-- END GENERATED div-rel-rust -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-rust-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | div | CD | P-gen | x86_64 | thru | 82.14 | libbid | 86.65 | **1.05×** | xRrsw2 |  |
| rust | div | WD | P-gen | x86_64 | thru | 90.76 | libbid | 88.12 | **0.97×** | xRrsw2 |  |
| rust | div | XD | P-gen | x86_64 | thru | 90.46 | libbid | 88.89 | **0.98×** | xRrsw2 |  |
| rust | div | ET | P-gen | x86_64 | thru | 31.05 | libbid | 31.98 | **1.03×** | xRrsw2 |  |
| rust | div | PT | P-gen | x86_64 | thru | 10.49 | libbid | 32.28 | **3.08×** | xRrsw2 |  |

<!-- END GENERATED div-rel-rust-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-rust -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | fma | FN | FMA | arm64 | thru | 21.52 | - | - | - | Rrsw2 |  |
| rust | fma | FF | FMA | arm64 | thru | 37.93 | - | - | - | Rrsw2 |  |

<!-- END GENERATED fma-rel-rust -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-rust-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | fma | FN | FMA | x86_64 | thru | 67.47 | - | - | - | xRrsw2 |  |
| rust | fma | FF | FMA | x86_64 | thru | 73.82 | - | - | - | xRrsw2 |  |

<!-- END GENERATED fma-rel-rust-x86 -->

</div>
