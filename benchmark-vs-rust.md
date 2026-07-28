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
| rust | add | MIX | P-fin | arm64 | thru | 2.03 | rust_decimal | 3.38 | **1.67×** | Rrsw2 | compact idiom peer |
| rust | sub | MIX | P-fin | arm64 | thru | 2.22 | rust_decimal | 3.54 | **1.59×** | Rrsw2 | compact idiom peer |
| rust | div | CD | P-fin | arm64 | thru | 19.05 | rust_decimal | 15.51 | **0.81×** | Rrsw2 | compact idiom peer |
| rust | div | WD | P-fin | arm64 | thru | 35.39 | rust_decimal | 20.57 | **0.58×** | Rrsw2 | compact idiom peer |
| rust | div | ET | P-fin | arm64 | thru | 6.37 | rust_decimal | 3.85 | **0.60×** | Rrsw2 | compact idiom peer |
| rust | div | PT | P-fin | arm64 | thru | 3.98 | rust_decimal | 15.45 | **3.88×** | Rrsw2 | compact idiom peer |
| rust | mul | CP | P-fin | arm64 | thru | 1.12 | libbid | 23.91 | **21.35×** | Rrsw2 |  |
| rust | mul | WP | P-fin | arm64 | thru | 14.23 | libbid | 34.44 | **2.42×** | Rrsw2 |  |

<!-- END GENERATED pfin-rel-rust -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-rust-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | add | MIX | P-fin | x86_64 | thru | 5.67 | rust_decimal | 13.70 | **2.42×** | xRrsw2 | compact idiom peer |
| rust | sub | MIX | P-fin | x86_64 | thru | 7.02 | rust_decimal | 14.33 | **2.04×** | xRrsw2 | compact idiom peer |
| rust | div | CD | P-fin | x86_64 | thru | 71.78 | rust_decimal | 55.18 | **0.77×** | xRrsw2 | compact idiom peer |
| rust | div | WD | P-fin | x86_64 | thru | 85.67 | rust_decimal | 73.47 | **0.86×** | xRrsw2 | compact idiom peer |
| rust | div | ET | P-fin | x86_64 | thru | 23.36 | rust_decimal | 13.73 | **0.59×** | xRrsw2 | compact idiom peer |
| rust | div | PT | P-fin | x86_64 | thru | 10.85 | rust_decimal | 50.20 | **4.63×** | xRrsw2 | compact idiom peer |
| rust | mul | CP | P-fin | x86_64 | thru | 2.84 | libbid | 43.66 | **15.37×** | xRrsw2 |  |
| rust | mul | WP | P-fin | x86_64 | thru | 28.69 | libbid | 57.74 | **2.01×** | xRrsw2 |  |

<!-- END GENERATED pfin-rel-rust-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-rust -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | add | SQ | P-gen | arm64 | thru | 1.82 | rust_decimal | 3.46 | **1.90×** | Rrsw2 | compact idiom peer |
| rust | add | NQ | P-gen | arm64 | thru | 5.69 | rust_decimal | 5.48 | **0.96×** | Rrsw2 | compact idiom peer |
| rust | add | MQ | P-gen | arm64 | thru | 8.54 | rust_decimal | 5.76 | **0.67×** | Rrsw2 | compact idiom peer |
| rust | add | OQ | P-gen | arm64 | thru | 10.82 | - | - | - | Rrsw2 |  |
| rust | add | FQ | P-gen | arm64 | thru | 7.44 | - | - | - | Rrsw2 |  |

<!-- END GENERATED add-rel-rust -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-rust-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | add | SQ | P-gen | x86_64 | thru | 6.93 | rust_decimal | 14.56 | **2.10×** | xRrsw2 | compact idiom peer |
| rust | add | NQ | P-gen | x86_64 | thru | 14.09 | rust_decimal | 20.63 | **1.46×** | xRrsw2 | compact idiom peer |
| rust | add | MQ | P-gen | x86_64 | thru | 20.29 | rust_decimal | 19.77 | **0.97×** | xRrsw2 | compact idiom peer |
| rust | add | OQ | P-gen | x86_64 | thru | 37.60 | - | - | - | xRrsw2 |  |
| rust | add | FQ | P-gen | x86_64 | thru | 22.57 | - | - | - | xRrsw2 |  |

<!-- END GENERATED add-rel-rust-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-rust -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | sub | SQ | P-gen | arm64 | thru | 1.74 | rust_decimal | 3.39 | **1.95×** | Rrsw2 | compact idiom peer |
| rust | sub | NQ | P-gen | arm64 | thru | 4.86 | rust_decimal | 5.54 | **1.14×** | Rrsw2 | compact idiom peer |
| rust | sub | MQ | P-gen | arm64 | thru | 7.90 | rust_decimal | 5.62 | **0.71×** | Rrsw2 | compact idiom peer |
| rust | sub | OQ | P-gen | arm64 | thru | 10.61 | - | - | - | Rrsw2 |  |
| rust | sub | FQ | P-gen | arm64 | thru | 7.08 | - | - | - | Rrsw2 |  |

<!-- END GENERATED sub-rel-rust -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-rust-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | sub | SQ | P-gen | x86_64 | thru | 6.94 | rust_decimal | 14.05 | **2.02×** | xRrsw2 | compact idiom peer |
| rust | sub | NQ | P-gen | x86_64 | thru | 13.34 | rust_decimal | 18.97 | **1.42×** | xRrsw2 | compact idiom peer |
| rust | sub | MQ | P-gen | x86_64 | thru | 20.29 | rust_decimal | 18.91 | **0.93×** | xRrsw2 | compact idiom peer |
| rust | sub | OQ | P-gen | x86_64 | thru | 37.57 | - | - | - | xRrsw2 |  |
| rust | sub | FQ | P-gen | x86_64 | thru | 22.49 | - | - | - | xRrsw2 |  |

<!-- END GENERATED sub-rel-rust-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-rust -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | mul | CP | P-gen | arm64 | thru | 1.51 | libbid | 24.58 | **16.28×** | Rrsw2 |  |
| rust | mul | WP | P-gen | arm64 | thru | 13.69 | libbid | 33.28 | **2.43×** | Rrsw2 |  |
| rust | mul | XP | P-gen | arm64 | thru | 23.86 | libbid | 45.22 | **1.90×** | Rrsw2 |  |

<!-- END GENERATED mul-rel-rust -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-rust-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | mul | CP | P-gen | x86_64 | thru | 4.82 | libbid | 49.91 | **10.35×** | xRrsw2 |  |
| rust | mul | WP | P-gen | x86_64 | thru | 29.06 | libbid | 77.04 | **2.65×** | xRrsw2 |  |
| rust | mul | XP | P-gen | x86_64 | thru | 42.21 | libbid | 97.21 | **2.30×** | xRrsw2 |  |

<!-- END GENERATED mul-rel-rust-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-rust -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | div | CD | P-gen | arm64 | thru | 19.02 | libbid | 36.64 | **1.93×** | Rrsw2 |  |
| rust | div | WD | P-gen | arm64 | thru | 33.33 | libbid | 37.56 | **1.13×** | Rrsw2 |  |
| rust | div | XD | P-gen | arm64 | thru | 37.57 | libbid | 39.18 | **1.04×** | Rrsw2 |  |
| rust | div | ET | P-gen | arm64 | thru | 9.73 | libbid | 11.64 | **1.20×** | Rrsw2 |  |
| rust | div | PT | P-gen | arm64 | thru | 3.98 | libbid | 11.54 | **2.90×** | Rrsw2 |  |

<!-- END GENERATED div-rel-rust -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-rust-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | div | CD | P-gen | x86_64 | thru | 75.66 | libbid | 83.35 | **1.10×** | xRrsw2 |  |
| rust | div | WD | P-gen | x86_64 | thru | 83.57 | libbid | 85.72 | **1.03×** | xRrsw2 |  |
| rust | div | XD | P-gen | x86_64 | thru | 82.33 | libbid | 84.67 | **1.03×** | xRrsw2 |  |
| rust | div | ET | P-gen | x86_64 | thru | 28.91 | libbid | 29.45 | **1.02×** | xRrsw2 |  |
| rust | div | PT | P-gen | x86_64 | thru | 10.87 | libbid | 29.43 | **2.71×** | xRrsw2 |  |

<!-- END GENERATED div-rel-rust-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-rust -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | fma | FN | FMA | arm64 | thru | 23.22 | - | - | - | Rrsw2 |  |
| rust | fma | FF | FMA | arm64 | thru | 34.17 | - | - | - | Rrsw2 |  |

<!-- END GENERATED fma-rel-rust -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-rust-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rust | fma | FN | FMA | x86_64 | thru | 59.79 | - | - | - | xRrsw2 |  |
| rust | fma | FF | FMA | x86_64 | thru | 65.10 | - | - | - | xRrsw2 |  |

<!-- END GENERATED fma-rel-rust-x86 -->

</div>
