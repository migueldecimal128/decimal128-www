---
layout: default
permalink: /benchmark/vs-c.html
title: "C Benchmark Results — Decimal128"
description: "decimal128 in C, measured against the alternatives available to it — a realistic financial mix (P-fin) plus per-operation band characterization, with explicit ratios."
heading: "C Benchmark Results"
---

<div class="whitepaper" markdown="1">

<p class="whitepaper-meta">Living document — as-measured results. Category codes, profiles, modes &amp; method: <a href="key.html">Benchmark Key</a>.</p>

This is the **C** view of decimal128 **as-measured**, band by band, with explicit ratios. It opens with the realistic financial-mix (**P-fin**) headline, then the per-operation band characterization (**P-gen**) and FMA. In C, d128 is measured against the Intel **libbid** universal reference plus IBM **decQuad** (DPD) and **libmpdecimal**. It is **data only** — the categories, magnitude profiles, units, and methodology are defined in the [Benchmark Key](key.html) (and, authoritatively, `BenchmarkMatrix.md`). The cross-port d128 band-shape matrices (all ports, no alternatives) live in [Port-Comparison Benchmark Results](port-compare.html); the full index of per-language pages is on the [Benchmarks](/benchmarks.html) hub.

## Summary — Ratio Range by Operation

Each row below is the ratio for that reference library on x86_64 (Intel i9-9880H): `ratio = libbid / Miguel`, `ratio = decQuad / Miguel`, or `ratio = mpdecimal / Miguel` (&gt; 1× ⇒ d128 faster), broken out by operation.

| | Add | Subtract | Multiply | Divide |
|---|---|---|---|---|
| ratio = libbid / Miguel | 3× | 4× | 1.3× – 19× | 0.8× – 1.9× |
| ratio = decQuad / Miguel | 6× | 7× | 1.5× – 22× | 1.6× – 7× |
| ratio = mpdecimal / Miguel | 4× | 5× | 1.0× – 13× | 1.8× – 9× |

## FinMix — realistic financial mix (P-fin)

The headline: one realistic 64-bit financial operation mix — a `MIX` add/sub stream, mul `CP`/`WP`, div `CD`/`WD`/`ET`/`PT` — `ratio = alt / Miguel` (&gt; 1 ⇒ d128 faster). This is the profile closest to real financial code.

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED pfin-rel-c -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | add | MIX | P-fin | arm64 | thru | 2.76 | libbid | 11.37 | **4.12×** | Rc2 |  |
| c | sub | MIX | P-fin | arm64 | thru | 2.08 | libbid | 13.38 | **6.43×** | Rc2 |  |
| c | mul | CP | P-fin | arm64 | thru | 1.25 | libbid | 23.54 | **18.83×** | Rc2 |  |
| c | mul | WP | P-fin | arm64 | thru | 19.99 | libbid | 32.10 | **1.61×** | Rc2 |  |
| c | div | CD | P-fin | arm64 | thru | 43.31 | libbid | 37.72 | **0.87×** | Rc2 |  |
| c | div | WD | P-fin | arm64 | thru | 38.91 | libbid | 39.06 | **1.00×** | Rc2 |  |
| c | div | ET | P-fin | arm64 | thru | 6.48 | libbid | 5.96 | **0.92×** | Rc2 |  |
| c | div | PT | P-fin | arm64 | thru | 3.15 | libbid | 6.06 | **1.92×** | Rc2 |  |
| c | add | MIX | P-fin | arm64 | thru | 2.76 | decQuad | 21.90 | **7.93×** | Rc2 |  |
| c | sub | MIX | P-fin | arm64 | thru | 2.08 | decQuad | 22.86 | **10.99×** | Rc2 |  |
| c | mul | CP | P-fin | arm64 | thru | 1.25 | decQuad | 22.09 | **17.67×** | Rc2 |  |
| c | mul | WP | P-fin | arm64 | thru | 19.99 | decQuad | 25.94 | **1.30×** | Rc2 |  |
| c | div | CD | P-fin | arm64 | thru | 43.31 | decQuad | 71.40 | **1.65×** | Rc2 |  |
| c | div | WD | P-fin | arm64 | thru | 38.91 | decQuad | 117.16 | **3.01×** | Rc2 |  |
| c | div | ET | P-fin | arm64 | thru | 6.48 | decQuad | 39.86 | **6.15×** | Rc2 |  |
| c | div | PT | P-fin | arm64 | thru | 3.15 | decQuad | 38.05 | **12.08×** | Rc2 |  |
| c | add | MIX | P-fin | arm64 | thru | 2.76 | mpdecimal | 15.58 | **5.64×** | Rc2 |  |
| c | sub | MIX | P-fin | arm64 | thru | 2.08 | mpdecimal | 13.02 | **6.26×** | Rc2 |  |
| c | mul | CP | P-fin | arm64 | thru | 1.25 | mpdecimal | 14.52 | **11.62×** | Rc2 |  |
| c | mul | WP | P-fin | arm64 | thru | 19.99 | mpdecimal | 28.71 | **1.44×** | Rc2 |  |
| c | div | CD | P-fin | arm64 | thru | 43.31 | mpdecimal | 58.52 | **1.35×** | Rc2 |  |
| c | div | WD | P-fin | arm64 | thru | 38.91 | mpdecimal | 85.40 | **2.19×** | Rc2 |  |
| c | div | ET | P-fin | arm64 | thru | 6.48 | mpdecimal | 57.34 | **8.85×** | Rc2 |  |
| c | div | PT | P-fin | arm64 | thru | 3.15 | mpdecimal | 46.34 | **14.71×** | Rc2 |  |

<!-- END GENERATED pfin-rel-c -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-c-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | add | MIX | P-fin | x86_64 | thru | 10.44 | libbid | 32.11 | **3.08×** | xRc2 |  |
| c | sub | MIX | P-fin | x86_64 | thru | 6.72 | libbid | 36.74 | **5.47×** | xRc2 |  |
| c | mul | CP | P-fin | x86_64 | thru | 2.55 | libbid | 46.14 | **18.09×** | xRc2 |  |
| c | mul | WP | P-fin | x86_64 | thru | 42.64 | libbid | 60.57 | **1.42×** | xRc2 |  |
| c | div | CD | P-fin | x86_64 | thru | 88.20 | libbid | 78.27 | **0.89×** | xRc2 |  |
| c | div | WD | P-fin | x86_64 | thru | 102.49 | libbid | 82.95 | **0.81×** | xRc2 |  |
| c | div | ET | P-fin | x86_64 | thru | 18.48 | libbid | 19.44 | **1.05×** | xRc2 |  |
| c | div | PT | P-fin | x86_64 | thru | 10.11 | libbid | 19.26 | **1.91×** | xRc2 |  |
| c | add | MIX | P-fin | x86_64 | thru | 10.44 | decQuad | 56.19 | **5.38×** | xRc2 |  |
| c | sub | MIX | P-fin | x86_64 | thru | 6.72 | decQuad | 63.02 | **9.38×** | xRc2 |  |
| c | mul | CP | P-fin | x86_64 | thru | 2.55 | decQuad | 58.79 | **23.05×** | xRc2 |  |
| c | mul | WP | P-fin | x86_64 | thru | 42.64 | decQuad | 69.11 | **1.62×** | xRc2 |  |
| c | div | CD | P-fin | x86_64 | thru | 88.20 | decQuad | 136.82 | **1.55×** | xRc2 |  |
| c | div | WD | P-fin | x86_64 | thru | 102.49 | decQuad | 241.68 | **2.36×** | xRc2 |  |
| c | div | ET | P-fin | x86_64 | thru | 18.48 | decQuad | 76.25 | **4.13×** | xRc2 |  |
| c | div | PT | P-fin | x86_64 | thru | 10.11 | decQuad | 69.21 | **6.85×** | xRc2 |  |
| c | add | MIX | P-fin | x86_64 | thru | 10.44 | mpdecimal | 39.01 | **3.74×** | xRc2 |  |
| c | sub | MIX | P-fin | x86_64 | thru | 6.72 | mpdecimal | 38.11 | **5.67×** | xRc2 |  |
| c | mul | CP | P-fin | x86_64 | thru | 2.55 | mpdecimal | 32.79 | **12.86×** | xRc2 |  |
| c | mul | WP | P-fin | x86_64 | thru | 42.64 | mpdecimal | 43.78 | **1.03×** | xRc2 |  |
| c | div | CD | P-fin | x86_64 | thru | 88.20 | mpdecimal | 155.55 | **1.76×** | xRc2 |  |
| c | div | WD | P-fin | x86_64 | thru | 102.49 | mpdecimal | 278.12 | **2.71×** | xRc2 |  |
| c | div | ET | P-fin | x86_64 | thru | 18.48 | mpdecimal | 137.16 | **7.42×** | xRc2 |  |
| c | div | PT | P-fin | x86_64 | thru | 10.11 | mpdecimal | 91.16 | **9.02×** | xRc2 |  |

<!-- END GENERATED pfin-rel-c-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-c -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | add | SQ | P-gen | arm64 | thru | 2.20 | libbid | 8.63 | **3.92×** | Rc2 |  |
| c | add | NQ | P-gen | arm64 | thru | 4.23 | libbid | 8.34 | **1.97×** | Rc2 |  |
| c | add | MQ | P-gen | arm64 | thru | 6.57 | libbid | 8.63 | **1.31×** | Rc2 |  |
| c | add | OQ | P-gen | arm64 | thru | 11.50 | libbid | 13.40 | **1.17×** | Rc2 |  |
| c | add | FQ | P-gen | arm64 | thru | 7.29 | libbid | 9.21 | **1.26×** | Rc2 |  |
| c | add | SQ | P-gen | arm64 | thru | 2.20 | decQuad | 19.86 | **9.03×** | Rc2 |  |
| c | add | NQ | P-gen | arm64 | thru | 4.23 | decQuad | 30.02 | **7.10×** | Rc2 |  |
| c | add | MQ | P-gen | arm64 | thru | 6.57 | decQuad | 30.95 | **4.71×** | Rc2 |  |
| c | add | OQ | P-gen | arm64 | thru | 11.50 | decQuad | 33.45 | **2.91×** | Rc2 |  |
| c | add | FQ | P-gen | arm64 | thru | 7.29 | decQuad | 25.43 | **3.49×** | Rc2 |  |
| c | add | SQ | P-gen | arm64 | thru | 2.20 | mpdecimal | 12.09 | **5.50×** | Rc2 |  |
| c | add | NQ | P-gen | arm64 | thru | 4.23 | mpdecimal | 26.38 | **6.24×** | Rc2 |  |
| c | add | MQ | P-gen | arm64 | thru | 6.57 | mpdecimal | 24.11 | **3.67×** | Rc2 |  |
| c | add | OQ | P-gen | arm64 | thru | 11.50 | mpdecimal | 47.35 | **4.12×** | Rc2 |  |
| c | add | FQ | P-gen | arm64 | thru | 7.29 | mpdecimal | 39.01 | **5.35×** | Rc2 |  |

<!-- END GENERATED add-rel-c -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-c-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | add | SQ | P-gen | x86_64 | thru | 8.99 | libbid | 30.55 | **3.40×** | xRc2 |  |
| c | add | NQ | P-gen | x86_64 | thru | 13.01 | libbid | 32.21 | **2.48×** | xRc2 |  |
| c | add | MQ | P-gen | x86_64 | thru | 24.99 | libbid | 31.68 | **1.27×** | xRc2 |  |
| c | add | OQ | P-gen | x86_64 | thru | 46.65 | libbid | 47.35 | **1.02×** | xRc2 |  |
| c | add | FQ | P-gen | x86_64 | thru | 32.83 | libbid | 30.07 | **0.92×** | xRc2 |  |
| c | add | SQ | P-gen | x86_64 | thru | 8.99 | decQuad | 52.08 | **5.79×** | xRc2 |  |
| c | add | NQ | P-gen | x86_64 | thru | 13.01 | decQuad | 105.97 | **8.15×** | xRc2 |  |
| c | add | MQ | P-gen | x86_64 | thru | 24.99 | decQuad | 78.42 | **3.14×** | xRc2 |  |
| c | add | OQ | P-gen | x86_64 | thru | 46.65 | decQuad | 88.54 | **1.90×** | xRc2 |  |
| c | add | FQ | P-gen | x86_64 | thru | 32.83 | decQuad | 71.69 | **2.18×** | xRc2 |  |
| c | add | SQ | P-gen | x86_64 | thru | 8.99 | mpdecimal | 37.15 | **4.13×** | xRc2 |  |
| c | add | NQ | P-gen | x86_64 | thru | 13.01 | mpdecimal | 63.41 | **4.87×** | xRc2 |  |
| c | add | MQ | P-gen | x86_64 | thru | 24.99 | mpdecimal | 54.74 | **2.19×** | xRc2 |  |
| c | add | OQ | P-gen | x86_64 | thru | 46.65 | mpdecimal | 128.03 | **2.74×** | xRc2 |  |
| c | add | FQ | P-gen | x86_64 | thru | 32.83 | mpdecimal | 88.62 | **2.70×** | xRc2 |  |

<!-- END GENERATED add-rel-c-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-c -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | sub | SQ | P-gen | arm64 | thru | 1.22 | libbid | 9.06 | **7.43×** | Rc2 |  |
| c | sub | NQ | P-gen | arm64 | thru | 4.74 | libbid | 10.86 | **2.29×** | Rc2 |  |
| c | sub | MQ | P-gen | arm64 | thru | 6.85 | libbid | 8.85 | **1.29×** | Rc2 |  |
| c | sub | OQ | P-gen | arm64 | thru | 12.00 | libbid | 16.89 | **1.41×** | Rc2 |  |
| c | sub | FQ | P-gen | arm64 | thru | 7.45 | libbid | 10.25 | **1.38×** | Rc2 |  |
| c | sub | SQ | P-gen | arm64 | thru | 1.22 | decQuad | 22.30 | **18.28×** | Rc2 |  |
| c | sub | NQ | P-gen | arm64 | thru | 4.74 | decQuad | 31.35 | **6.61×** | Rc2 |  |
| c | sub | MQ | P-gen | arm64 | thru | 6.85 | decQuad | 31.30 | **4.57×** | Rc2 |  |
| c | sub | OQ | P-gen | arm64 | thru | 12.00 | decQuad | 35.50 | **2.96×** | Rc2 |  |
| c | sub | FQ | P-gen | arm64 | thru | 7.45 | decQuad | 29.30 | **3.93×** | Rc2 |  |
| c | sub | SQ | P-gen | arm64 | thru | 1.22 | mpdecimal | 12.28 | **10.07×** | Rc2 |  |
| c | sub | NQ | P-gen | arm64 | thru | 4.74 | mpdecimal | 26.14 | **5.51×** | Rc2 |  |
| c | sub | MQ | P-gen | arm64 | thru | 6.85 | mpdecimal | 20.64 | **3.01×** | Rc2 |  |
| c | sub | OQ | P-gen | arm64 | thru | 12.00 | mpdecimal | 48.73 | **4.06×** | Rc2 |  |
| c | sub | FQ | P-gen | arm64 | thru | 7.45 | mpdecimal | 39.92 | **5.36×** | Rc2 |  |

<!-- END GENERATED sub-rel-c -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-c-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | sub | SQ | P-gen | x86_64 | thru | 5.38 | libbid | 35.44 | **6.59×** | xRc2 |  |
| c | sub | NQ | P-gen | x86_64 | thru | 13.42 | libbid | 37.04 | **2.76×** | xRc2 |  |
| c | sub | MQ | P-gen | x86_64 | thru | 24.60 | libbid | 35.97 | **1.46×** | xRc2 |  |
| c | sub | OQ | P-gen | x86_64 | thru | 45.68 | libbid | 51.86 | **1.14×** | xRc2 |  |
| c | sub | FQ | P-gen | x86_64 | thru | 33.35 | libbid | 34.95 | **1.05×** | xRc2 |  |
| c | sub | SQ | P-gen | x86_64 | thru | 5.38 | decQuad | 58.61 | **10.89×** | xRc2 |  |
| c | sub | NQ | P-gen | x86_64 | thru | 13.42 | decQuad | 87.22 | **6.50×** | xRc2 |  |
| c | sub | MQ | P-gen | x86_64 | thru | 24.60 | decQuad | 84.37 | **3.43×** | xRc2 |  |
| c | sub | OQ | P-gen | x86_64 | thru | 45.68 | decQuad | 93.20 | **2.04×** | xRc2 |  |
| c | sub | FQ | P-gen | x86_64 | thru | 33.35 | decQuad | 74.36 | **2.23×** | xRc2 |  |
| c | sub | SQ | P-gen | x86_64 | thru | 5.38 | mpdecimal | 37.38 | **6.95×** | xRc2 |  |
| c | sub | NQ | P-gen | x86_64 | thru | 13.42 | mpdecimal | 54.46 | **4.06×** | xRc2 |  |
| c | sub | MQ | P-gen | x86_64 | thru | 24.60 | mpdecimal | 54.08 | **2.20×** | xRc2 |  |
| c | sub | OQ | P-gen | x86_64 | thru | 45.68 | mpdecimal | 126.94 | **2.78×** | xRc2 |  |
| c | sub | FQ | P-gen | x86_64 | thru | 33.35 | mpdecimal | 84.08 | **2.52×** | xRc2 |  |

<!-- END GENERATED sub-rel-c-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-c -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | mul | CP | P-gen | arm64 | thru | 1.43 | libbid | 23.10 | **16.15×** | Rc2 | **no scaling** — the cheap multiply |
| c | mul | WP | P-gen | arm64 | thru | 19.65 | libbid | 33.19 | **1.69×** | Rc2 | 128-bit recipMulPow10 |
| c | mul | XP | P-gen | arm64 | thru | 24.00 | libbid | 42.29 | **1.76×** | Rc2 | 256-bit recipMulPow10; **1.19× ≈ the recipmul-256 work-order's 1.18–1.54× band** |
| c | mul | CP | P-gen | arm64 | thru | 1.43 | decQuad | 21.96 | **15.36×** | Rc2 | vs DPD |
| c | mul | WP | P-gen | arm64 | thru | 19.65 | decQuad | 26.27 | **1.34×** | Rc2 | vs DPD |
| c | mul | XP | P-gen | arm64 | thru | 24.00 | decQuad | 30.26 | **1.26×** | Rc2 | **decQuad edges d128 on the widest product** (software DPD's flat cost; libbid still slower) |
| c | mul | CP | P-gen | arm64 | thru | 1.43 | mpdecimal | 21.25 | **14.86×** | Rc2 | no-scale multiply vs libmpdec |
| c | mul | WP | P-gen | arm64 | thru | 19.65 | mpdecimal | 50.37 | **2.56×** | Rc2 | 128-bit recipMulPow10 |
| c | mul | XP | P-gen | arm64 | thru | 24.00 | mpdecimal | 68.36 | **2.85×** | Rc2 | **d128 wins the widest product vs libmpdec** (unlike decQuad) |

<!-- END GENERATED mul-rel-c -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-c-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | mul | CP | P-gen | x86_64 | thru | 4.39 | libbid | 46.33 | **10.55×** | xRc2 |  |
| c | mul | WP | P-gen | x86_64 | thru | 42.60 | libbid | 67.28 | **1.58×** | xRc2 |  |
| c | mul | XP | P-gen | x86_64 | thru | 51.91 | libbid | 95.35 | **1.84×** | xRc2 |  |
| c | mul | CP | P-gen | x86_64 | thru | 4.39 | decQuad | 57.65 | **13.13×** | xRc2 |  |
| c | mul | WP | P-gen | x86_64 | thru | 42.60 | decQuad | 70.59 | **1.66×** | xRc2 |  |
| c | mul | XP | P-gen | x86_64 | thru | 51.91 | decQuad | 87.63 | **1.69×** | xRc2 |  |
| c | mul | CP | P-gen | x86_64 | thru | 4.39 | mpdecimal | 65.40 | **14.90×** | xRc2 |  |
| c | mul | WP | P-gen | x86_64 | thru | 42.60 | mpdecimal | 185.44 | **4.35×** | xRc2 |  |
| c | mul | XP | P-gen | x86_64 | thru | 51.91 | mpdecimal | 229.09 | **4.41×** | xRc2 |  |

<!-- END GENERATED mul-rel-c-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-c -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | div | CD | P-gen | arm64 | thru | 41.32 | libbid | 36.52 | **0.88×** | Rc2 | 128÷64 quotient-first (§2.4.10); **libbid wins** — the compact-divide weakness persists |
| c | div | WD | P-gen | arm64 | thru | 39.32 | libbid | 37.53 | **0.95×** | Rc2 | 256÷64; **≈ parity / slight loss** |
| c | div | XD | P-gen | arm64 | thru | 32.97 | libbid | 39.01 | **1.18×** | Rc2 | 256÷128 Möller–Granlund |
| c | div | ET | P-gen | arm64 | thru | 8.09 | libbid | 10.87 | **1.34×** | Rc2 | **quotient-first exact early-out** — beats libbid's exact fast path |
| c | div | PT | P-gen | arm64 | thru | 3.15 | libbid | 10.76 | **3.42×** | Rc2 | `divPow10Divisor` (§2.4.9); **d128's fastest divide** (coeff-1 form) |
| c | div | CD | P-gen | arm64 | thru | 41.32 | decQuad | 71.20 | **1.72×** | Rc2 | vs DPD |
| c | div | WD | P-gen | arm64 | thru | 39.32 | decQuad | 116.24 | **2.96×** | Rc2 | vs DPD |
| c | div | XD | P-gen | arm64 | thru | 32.97 | decQuad | 173.28 | **5.26×** | Rc2 | vs DPD — decNumber divide is slow |
| c | div | ET | P-gen | arm64 | thru | 8.09 | decQuad | 45.03 | **5.57×** | Rc2 | vs DPD |
| c | div | PT | P-gen | arm64 | thru | 3.15 | decQuad | 42.41 | **13.46×** | Rc2 | vs DPD |
| c | div | CD | P-gen | arm64 | thru | 41.32 | mpdecimal | 59.40 | **1.44×** | Rc2 | **narrowest divide gap** (libmpdec's compact divide is its cheapest, like d128's weakness) |
| c | div | WD | P-gen | arm64 | thru | 39.32 | mpdecimal | 88.72 | **2.26×** | Rc2 | 256÷64 |
| c | div | XD | P-gen | arm64 | thru | 32.97 | mpdecimal | 141.59 | **4.29×** | Rc2 | Cowlishaw signature (CD 59 < WD 87 < XD 144) |
| c | div | ET | P-gen | arm64 | thru | 8.09 | mpdecimal | 57.55 | **7.11×** | Rc2 | libmpdec has no exact early-out |
| c | div | PT | P-gen | arm64 | thru | 3.15 | mpdecimal | 47.88 | **15.20×** | Rc2 | **d128's biggest divide win vs libmpdec** |

<!-- END GENERATED div-rel-c -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-c-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | div | CD | P-gen | x86_64 | thru | 91.83 | libbid | 82.56 | **0.90×** | xRc2 |  |
| c | div | WD | P-gen | x86_64 | thru | 103.64 | libbid | 87.22 | **0.84×** | xRc2 |  |
| c | div | XD | P-gen | x86_64 | thru | 96.37 | libbid | 86.84 | **0.90×** | xRc2 |  |
| c | div | ET | P-gen | x86_64 | thru | 29.93 | libbid | 30.95 | **1.03×** | xRc2 |  |
| c | div | PT | P-gen | x86_64 | thru | 10.39 | libbid | 31.12 | **3.00×** | xRc2 |  |
| c | div | CD | P-gen | x86_64 | thru | 91.83 | decQuad | 149.17 | **1.62×** | xRc2 |  |
| c | div | WD | P-gen | x86_64 | thru | 103.64 | decQuad | 253.49 | **2.45×** | xRc2 |  |
| c | div | XD | P-gen | x86_64 | thru | 96.37 | decQuad | 396.69 | **4.12×** | xRc2 |  |
| c | div | ET | P-gen | x86_64 | thru | 29.93 | decQuad | 102.90 | **3.44×** | xRc2 |  |
| c | div | PT | P-gen | x86_64 | thru | 10.39 | decQuad | 86.11 | **8.29×** | xRc2 |  |
| c | div | CD | P-gen | x86_64 | thru | 91.83 | mpdecimal | 167.13 | **1.82×** | xRc2 |  |
| c | div | WD | P-gen | x86_64 | thru | 103.64 | mpdecimal | 290.07 | **2.80×** | xRc2 |  |
| c | div | XD | P-gen | x86_64 | thru | 96.37 | mpdecimal | 377.07 | **3.91×** | xRc2 |  |
| c | div | ET | P-gen | x86_64 | thru | 29.93 | mpdecimal | 156.43 | **5.23×** | xRc2 |  |
| c | div | PT | P-gen | x86_64 | thru | 10.39 | mpdecimal | 103.10 | **9.92×** | xRc2 |  |

<!-- END GENERATED div-rel-c-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-c -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | fma | FN | FMA | arm64 | thru | 75.77 | libbid | 84.00 | **1.11×** | Rc2 |  |
| c | fma | FF | FMA | arm64 | thru | 39.42 | libbid | 57.07 | **1.45×** | Rc2 |  |
| c | fma | FN | FMA | arm64 | thru | 75.77 | decQuad | 65.32 | **0.86×** | Rc2 |  |
| c | fma | FF | FMA | arm64 | thru | 39.42 | decQuad | 70.53 | **1.79×** | Rc2 |  |
| c | fma | FN | FMA | arm64 | thru | 75.77 | mpdecimal | 92.11 | **1.22×** | Rc2 |  |
| c | fma | FF | FMA | arm64 | thru | 39.42 | mpdecimal | 146.66 | **3.72×** | Rc2 |  |

<!-- END GENERATED fma-rel-c -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-c-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | fma | FN | FMA | x86_64 | thru | 154.12 | libbid | 160.41 | **1.04×** | xRc2 |  |
| c | fma | FF | FMA | x86_64 | thru | 91.07 | libbid | 123.46 | **1.36×** | xRc2 |  |
| c | fma | FN | FMA | x86_64 | thru | 154.12 | decQuad | 147.86 | **0.96×** | xRc2 |  |
| c | fma | FF | FMA | x86_64 | thru | 91.07 | decQuad | 154.38 | **1.70×** | xRc2 |  |
| c | fma | FN | FMA | x86_64 | thru | 154.12 | mpdecimal | 265.43 | **1.72×** | xRc2 |  |
| c | fma | FF | FMA | x86_64 | thru | 91.07 | mpdecimal | 342.56 | **3.76×** | xRc2 |  |

<!-- END GENERATED fma-rel-c-x86 -->

</div>
