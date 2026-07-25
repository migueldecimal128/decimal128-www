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
| rust | add | MIX | P-fin | arm64 | thru | 2.22 | rust_decimal | 3.41 | **1.54×** | Rrsw2 | compact idiom peer |
| rust | sub | MIX | P-fin | arm64 | thru | 2.17 | rust_decimal | 3.55 | **1.64×** | Rrsw2 | compact idiom peer |
| rust | div | CD | P-fin | arm64 | thru | 19.10 | rust_decimal | 14.00 | **0.73×** | Rrsw2 | compact idiom peer |
| rust | div | WD | P-fin | arm64 | thru | 33.50 | rust_decimal | 20.38 | **0.61×** | Rrsw2 | compact idiom peer |
| rust | div | ET | P-fin | arm64 | thru | 6.35 | rust_decimal | 3.80 | **0.60×** | Rrsw2 | compact idiom peer |
| rust | div | PT | P-fin | arm64 | thru | 3.98 | rust_decimal | 15.10 | **3.79×** | Rrsw2 | compact idiom peer |
| rust | mul | CP | P-fin | arm64 | thru | 1.12 | libbid | 23.54 | **21.02×** | Rrsw2 |  |
| rust | mul | WP | P-fin | arm64 | thru | 14.33 | libbid | 32.43 | **2.26×** | Rrsw2 |  |

<!-- END GENERATED pfin-rel-rust -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-rust-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | add | MIX | P-fin | x86_64 | thru | 9.65 | rust_decimal | 16.21 | **1.68×** | xRrsw2 | compact idiom peer |
| rust | sub | MIX | P-fin | x86_64 | thru | 8.76 | rust_decimal | 15.56 | **1.78×** | xRrsw2 | compact idiom peer |
| rust | div | CD | P-fin | x86_64 | thru | 71.69 | rust_decimal | 58.25 | **0.81×** | xRrsw2 | compact idiom peer |
| rust | div | WD | P-fin | x86_64 | thru | 89.15 | rust_decimal | 77.37 | **0.87×** | xRrsw2 | compact idiom peer |
| rust | div | ET | P-fin | x86_64 | thru | 23.26 | rust_decimal | 14.43 | **0.62×** | xRrsw2 | compact idiom peer |
| rust | div | PT | P-fin | x86_64 | thru | 10.13 | rust_decimal | 53.05 | **5.24×** | xRrsw2 | compact idiom peer |
| rust | mul | CP | P-fin | x86_64 | thru | 3.42 | libbid | 46.14 | **13.49×** | xRrsw2 |  |
| rust | mul | WP | P-fin | x86_64 | thru | 31.46 | libbid | 60.57 | **1.93×** | xRrsw2 |  |

<!-- END GENERATED pfin-rel-rust-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-rust -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | add | SQ | P-gen | arm64 | thru | 2.76 | rust_decimal | 3.65 | **1.32×** | Rrsw2 | compact idiom peer |
| rust | add | NQ | P-gen | arm64 | thru | 5.14 | rust_decimal | 5.54 | **1.08×** | Rrsw2 | compact idiom peer |
| rust | add | MQ | P-gen | arm64 | thru | 7.38 | rust_decimal | 5.64 | **0.76×** | Rrsw2 | compact idiom peer |
| rust | add | OQ | P-gen | arm64 | thru | 10.40 | - | - | - | Rrsw2 |  |
| rust | add | FQ | P-gen | arm64 | thru | 6.75 | - | - | - | Rrsw2 |  |

<!-- END GENERATED add-rel-rust -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-rust-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | add | SQ | P-gen | x86_64 | thru | 9.18 | rust_decimal | 14.83 | **1.62×** | xRrsw2 | compact idiom peer |
| rust | add | NQ | P-gen | x86_64 | thru | 12.97 | rust_decimal | 20.75 | **1.60×** | xRrsw2 | compact idiom peer |
| rust | add | MQ | P-gen | x86_64 | thru | 20.57 | rust_decimal | 21.03 | **1.02×** | xRrsw2 | compact idiom peer |
| rust | add | OQ | P-gen | x86_64 | thru | 38.33 | - | - | - | xRrsw2 |  |
| rust | add | FQ | P-gen | x86_64 | thru | 24.51 | - | - | - | xRrsw2 |  |

<!-- END GENERATED add-rel-rust-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-rust -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | sub | SQ | P-gen | arm64 | thru | 1.73 | rust_decimal | 3.43 | **1.98×** | Rrsw2 | compact idiom peer |
| rust | sub | NQ | P-gen | arm64 | thru | 4.87 | rust_decimal | 5.64 | **1.16×** | Rrsw2 | compact idiom peer |
| rust | sub | MQ | P-gen | arm64 | thru | 7.84 | rust_decimal | 5.66 | **0.72×** | Rrsw2 | compact idiom peer |
| rust | sub | OQ | P-gen | arm64 | thru | 10.48 | - | - | - | Rrsw2 |  |
| rust | sub | FQ | P-gen | arm64 | thru | 6.94 | - | - | - | Rrsw2 |  |

<!-- END GENERATED sub-rel-rust -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-rust-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | sub | SQ | P-gen | x86_64 | thru | 7.22 | rust_decimal | 14.25 | **1.97×** | xRrsw2 | compact idiom peer |
| rust | sub | NQ | P-gen | x86_64 | thru | 14.40 | rust_decimal | 19.85 | **1.38×** | xRrsw2 | compact idiom peer |
| rust | sub | MQ | P-gen | x86_64 | thru | 21.94 | rust_decimal | 19.82 | **0.90×** | xRrsw2 | compact idiom peer |
| rust | sub | OQ | P-gen | x86_64 | thru | 42.39 | - | - | - | xRrsw2 |  |
| rust | sub | FQ | P-gen | x86_64 | thru | 24.35 | - | - | - | xRrsw2 |  |

<!-- END GENERATED sub-rel-rust-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-rust -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | mul | CP | P-gen | arm64 | thru | 1.59 | libbid | 22.98 | **14.45×** | Rrsw2 |  |
| rust | mul | WP | P-gen | arm64 | thru | 13.87 | libbid | 33.15 | **2.39×** | Rrsw2 |  |
| rust | mul | XP | P-gen | arm64 | thru | 25.13 | libbid | 42.97 | **1.71×** | Rrsw2 |  |

<!-- END GENERATED mul-rel-rust -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-rust-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | mul | CP | P-gen | x86_64 | thru | 5.30 | libbid | 46.33 | **8.74×** | xRrsw2 |  |
| rust | mul | WP | P-gen | x86_64 | thru | 30.15 | libbid | 67.28 | **2.23×** | xRrsw2 |  |
| rust | mul | XP | P-gen | x86_64 | thru | 45.19 | libbid | 95.35 | **2.11×** | xRrsw2 |  |

<!-- END GENERATED mul-rel-rust-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-rust -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | div | CD | P-gen | arm64 | thru | 20.16 | libbid | 37.45 | **1.86×** | Rrsw2 |  |
| rust | div | WD | P-gen | arm64 | thru | 35.66 | libbid | 37.57 | **1.05×** | Rrsw2 |  |
| rust | div | XD | P-gen | arm64 | thru | 38.25 | libbid | 39.17 | **1.02×** | Rrsw2 |  |
| rust | div | ET | P-gen | arm64 | thru | 9.72 | libbid | 11.67 | **1.20×** | Rrsw2 |  |
| rust | div | PT | P-gen | arm64 | thru | 3.97 | libbid | 11.43 | **2.88×** | Rrsw2 |  |

<!-- END GENERATED div-rel-rust -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-rust-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | div | CD | P-gen | x86_64 | thru | 76.14 | libbid | 82.56 | **1.08×** | xRrsw2 |  |
| rust | div | WD | P-gen | x86_64 | thru | 88.14 | libbid | 87.22 | **0.99×** | xRrsw2 |  |
| rust | div | XD | P-gen | x86_64 | thru | 85.94 | libbid | 86.84 | **1.01×** | xRrsw2 |  |
| rust | div | ET | P-gen | x86_64 | thru | 29.61 | libbid | 30.95 | **1.05×** | xRrsw2 |  |
| rust | div | PT | P-gen | x86_64 | thru | 10.19 | libbid | 31.12 | **3.05×** | xRrsw2 |  |

<!-- END GENERATED div-rel-rust-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-rust -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | fma | FN | FMA | arm64 | thru | 21.87 | - | - | - | Rrsw2 |  |
| rust | fma | FF | FMA | arm64 | thru | 33.80 | - | - | - | Rrsw2 |  |

<!-- END GENERATED fma-rel-rust -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-rust-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | fma | FN | FMA | x86_64 | thru | 62.65 | - | - | - | xRrsw2 |  |
| rust | fma | FF | FMA | x86_64 | thru | 69.00 | - | - | - | xRrsw2 |  |

<!-- END GENERATED fma-rel-rust-x86 -->

</div>
