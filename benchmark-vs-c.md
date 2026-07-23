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
| c | add | MIX | P-fin | arm64 | thru | 2.75 | libbid | 9.14 | **3.32×** | Rc2 |  |
| c | sub | MIX | P-fin | arm64 | thru | 2.04 | libbid | 13.48 | **6.61×** | Rc2 |  |
| c | mul | CP | P-fin | arm64 | thru | 1.29 | libbid | 23.29 | **18.05×** | Rc2 |  |
| c | mul | WP | P-fin | arm64 | thru | 20.07 | libbid | 32.06 | **1.60×** | Rc2 |  |
| c | div | CD | P-fin | arm64 | thru | 43.27 | libbid | 34.91 | **0.81×** | Rc2 |  |
| c | div | WD | P-fin | arm64 | thru | 39.37 | libbid | 39.06 | **0.99×** | Rc2 |  |
| c | div | ET | P-fin | arm64 | thru | 6.48 | libbid | 5.99 | **0.92×** | Rc2 |  |
| c | div | PT | P-fin | arm64 | thru | 3.16 | libbid | 5.99 | **1.90×** | Rc2 |  |
| c | add | MIX | P-fin | arm64 | thru | 2.75 | decQuad | 21.68 | **7.88×** | Rc2 |  |
| c | sub | MIX | P-fin | arm64 | thru | 2.04 | decQuad | 22.31 | **10.94×** | Rc2 |  |
| c | mul | CP | P-fin | arm64 | thru | 1.29 | decQuad | 22.67 | **17.57×** | Rc2 |  |
| c | mul | WP | P-fin | arm64 | thru | 20.07 | decQuad | 26.01 | **1.30×** | Rc2 |  |
| c | div | CD | P-fin | arm64 | thru | 43.27 | decQuad | 71.41 | **1.65×** | Rc2 |  |
| c | div | WD | P-fin | arm64 | thru | 39.37 | decQuad | 117.33 | **2.98×** | Rc2 |  |
| c | div | ET | P-fin | arm64 | thru | 6.48 | decQuad | 39.75 | **6.13×** | Rc2 |  |
| c | div | PT | P-fin | arm64 | thru | 3.16 | decQuad | 38.13 | **12.07×** | Rc2 |  |
| c | add | MIX | P-fin | arm64 | thru | 2.75 | mpdecimal | 14.07 | **5.12×** | Rc2 |  |
| c | sub | MIX | P-fin | arm64 | thru | 2.04 | mpdecimal | 14.41 | **7.06×** | Rc2 |  |
| c | mul | CP | P-fin | arm64 | thru | 1.29 | mpdecimal | 14.37 | **11.14×** | Rc2 |  |
| c | mul | WP | P-fin | arm64 | thru | 20.07 | mpdecimal | 28.86 | **1.44×** | Rc2 |  |
| c | div | CD | P-fin | arm64 | thru | 43.27 | mpdecimal | 58.07 | **1.34×** | Rc2 |  |
| c | div | WD | P-fin | arm64 | thru | 39.37 | mpdecimal | 84.84 | **2.15×** | Rc2 |  |
| c | div | ET | P-fin | arm64 | thru | 6.48 | mpdecimal | 54.04 | **8.34×** | Rc2 |  |
| c | div | PT | P-fin | arm64 | thru | 3.16 | mpdecimal | 44.26 | **14.01×** | Rc2 |  |

<!-- END GENERATED pfin-rel-c -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-c-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | add | MIX | P-fin | x86_64 | thru | 10.01 | libbid | 31.03 | **3.10×** | xRc2 |  |
| c | sub | MIX | P-fin | x86_64 | thru | 8.42 | libbid | 35.45 | **4.21×** | xRc2 |  |
| c | mul | CP | P-fin | x86_64 | thru | 2.51 | libbid | 47.15 | **18.78×** | xRc2 |  |
| c | mul | WP | P-fin | x86_64 | thru | 46.77 | libbid | 60.29 | **1.29×** | xRc2 |  |
| c | div | CD | P-fin | x86_64 | thru | 87.44 | libbid | 77.69 | **0.89×** | xRc2 |  |
| c | div | WD | P-fin | x86_64 | thru | 102.32 | libbid | 82.71 | **0.81×** | xRc2 |  |
| c | div | ET | P-fin | x86_64 | thru | 18.22 | libbid | 20.15 | **1.11×** | xRc2 |  |
| c | div | PT | P-fin | x86_64 | thru | 10.21 | libbid | 19.71 | **1.93×** | xRc2 |  |
| c | add | MIX | P-fin | x86_64 | thru | 10.01 | decQuad | 59.43 | **5.94×** | xRc2 |  |
| c | sub | MIX | P-fin | x86_64 | thru | 8.42 | decQuad | 60.69 | **7.21×** | xRc2 |  |
| c | mul | CP | P-fin | x86_64 | thru | 2.51 | decQuad | 55.98 | **22.30×** | xRc2 |  |
| c | mul | WP | P-fin | x86_64 | thru | 46.77 | decQuad | 69.22 | **1.48×** | xRc2 |  |
| c | div | CD | P-fin | x86_64 | thru | 87.44 | decQuad | 137.65 | **1.57×** | xRc2 |  |
| c | div | WD | P-fin | x86_64 | thru | 102.32 | decQuad | 240.81 | **2.35×** | xRc2 |  |
| c | div | ET | P-fin | x86_64 | thru | 18.22 | decQuad | 75.78 | **4.16×** | xRc2 |  |
| c | div | PT | P-fin | x86_64 | thru | 10.21 | decQuad | 67.99 | **6.66×** | xRc2 |  |
| c | add | MIX | P-fin | x86_64 | thru | 10.01 | mpdecimal | 38.13 | **3.81×** | xRc2 |  |
| c | sub | MIX | P-fin | x86_64 | thru | 8.42 | mpdecimal | 38.04 | **4.52×** | xRc2 |  |
| c | mul | CP | P-fin | x86_64 | thru | 2.51 | mpdecimal | 32.81 | **13.07×** | xRc2 |  |
| c | mul | WP | P-fin | x86_64 | thru | 46.77 | mpdecimal | 44.24 | **0.95×** | xRc2 |  |
| c | div | CD | P-fin | x86_64 | thru | 87.44 | mpdecimal | 158.24 | **1.81×** | xRc2 |  |
| c | div | WD | P-fin | x86_64 | thru | 102.32 | mpdecimal | 280.40 | **2.74×** | xRc2 |  |
| c | div | ET | P-fin | x86_64 | thru | 18.22 | mpdecimal | 142.13 | **7.80×** | xRc2 |  |
| c | div | PT | P-fin | x86_64 | thru | 10.21 | mpdecimal | 87.97 | **8.62×** | xRc2 |  |

<!-- END GENERATED pfin-rel-c-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-c -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | add | SQ | P-gen | arm64 | thru | 2.18 | libbid | 8.31 | **3.81×** | Rc2 |  |
| c | add | NQ | P-gen | arm64 | thru | 3.97 | libbid | 8.28 | **2.09×** | Rc2 |  |
| c | add | MQ | P-gen | arm64 | thru | 6.43 | libbid | 9.42 | **1.47×** | Rc2 |  |
| c | add | OQ | P-gen | arm64 | thru | 11.78 | libbid | 13.39 | **1.14×** | Rc2 |  |
| c | add | FQ | P-gen | arm64 | thru | 7.30 | libbid | 10.65 | **1.46×** | Rc2 |  |
| c | add | SQ | P-gen | arm64 | thru | 2.18 | decQuad | 20.06 | **9.20×** | Rc2 |  |
| c | add | NQ | P-gen | arm64 | thru | 3.97 | decQuad | 29.40 | **7.41×** | Rc2 |  |
| c | add | MQ | P-gen | arm64 | thru | 6.43 | decQuad | 28.09 | **4.37×** | Rc2 |  |
| c | add | OQ | P-gen | arm64 | thru | 11.78 | decQuad | 33.57 | **2.85×** | Rc2 |  |
| c | add | FQ | P-gen | arm64 | thru | 7.30 | decQuad | 26.79 | **3.67×** | Rc2 |  |
| c | add | SQ | P-gen | arm64 | thru | 2.18 | mpdecimal | 12.29 | **5.64×** | Rc2 |  |
| c | add | NQ | P-gen | arm64 | thru | 3.97 | mpdecimal | 26.26 | **6.61×** | Rc2 |  |
| c | add | MQ | P-gen | arm64 | thru | 6.43 | mpdecimal | 22.09 | **3.44×** | Rc2 |  |
| c | add | OQ | P-gen | arm64 | thru | 11.78 | mpdecimal | 44.46 | **3.77×** | Rc2 |  |
| c | add | FQ | P-gen | arm64 | thru | 7.30 | mpdecimal | 39.27 | **5.38×** | Rc2 |  |

<!-- END GENERATED add-rel-c -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-c-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | add | SQ | P-gen | x86_64 | thru | 8.93 | libbid | 30.20 | **3.38×** | xRc2 |  |
| c | add | NQ | P-gen | x86_64 | thru | 13.67 | libbid | 33.46 | **2.45×** | xRc2 |  |
| c | add | MQ | P-gen | x86_64 | thru | 35.37 | libbid | 31.52 | **0.89×** | xRc2 |  |
| c | add | OQ | P-gen | x86_64 | thru | 46.17 | libbid | 51.83 | **1.12×** | xRc2 |  |
| c | add | FQ | P-gen | x86_64 | thru | 31.57 | libbid | 32.09 | **1.02×** | xRc2 |  |
| c | add | SQ | P-gen | x86_64 | thru | 8.93 | decQuad | 51.90 | **5.81×** | xRc2 |  |
| c | add | NQ | P-gen | x86_64 | thru | 13.67 | decQuad | 80.55 | **5.89×** | xRc2 |  |
| c | add | MQ | P-gen | x86_64 | thru | 35.37 | decQuad | 77.86 | **2.20×** | xRc2 |  |
| c | add | OQ | P-gen | x86_64 | thru | 46.17 | decQuad | 88.50 | **1.92×** | xRc2 |  |
| c | add | FQ | P-gen | x86_64 | thru | 31.57 | decQuad | 71.35 | **2.26×** | xRc2 |  |
| c | add | SQ | P-gen | x86_64 | thru | 8.93 | mpdecimal | 36.59 | **4.10×** | xRc2 |  |
| c | add | NQ | P-gen | x86_64 | thru | 13.67 | mpdecimal | 56.71 | **4.15×** | xRc2 |  |
| c | add | MQ | P-gen | x86_64 | thru | 35.37 | mpdecimal | 56.80 | **1.61×** | xRc2 |  |
| c | add | OQ | P-gen | x86_64 | thru | 46.17 | mpdecimal | 134.00 | **2.90×** | xRc2 |  |
| c | add | FQ | P-gen | x86_64 | thru | 31.57 | mpdecimal | 85.49 | **2.71×** | xRc2 |  |

<!-- END GENERATED add-rel-c-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-c -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | sub | SQ | P-gen | arm64 | thru | 1.25 | libbid | 9.05 | **7.24×** | Rc2 |  |
| c | sub | NQ | P-gen | arm64 | thru | 4.71 | libbid | 11.78 | **2.50×** | Rc2 |  |
| c | sub | MQ | P-gen | arm64 | thru | 6.79 | libbid | 9.01 | **1.33×** | Rc2 |  |
| c | sub | OQ | P-gen | arm64 | thru | 12.01 | libbid | 14.26 | **1.19×** | Rc2 |  |
| c | sub | FQ | P-gen | arm64 | thru | 7.49 | libbid | 10.47 | **1.40×** | Rc2 |  |
| c | sub | SQ | P-gen | arm64 | thru | 1.25 | decQuad | 22.32 | **17.86×** | Rc2 |  |
| c | sub | NQ | P-gen | arm64 | thru | 4.71 | decQuad | 31.22 | **6.63×** | Rc2 |  |
| c | sub | MQ | P-gen | arm64 | thru | 6.79 | decQuad | 30.69 | **4.52×** | Rc2 |  |
| c | sub | OQ | P-gen | arm64 | thru | 12.01 | decQuad | 35.98 | **3.00×** | Rc2 |  |
| c | sub | FQ | P-gen | arm64 | thru | 7.49 | decQuad | 29.01 | **3.87×** | Rc2 |  |
| c | sub | SQ | P-gen | arm64 | thru | 1.25 | mpdecimal | 12.64 | **10.11×** | Rc2 |  |
| c | sub | NQ | P-gen | arm64 | thru | 4.71 | mpdecimal | 26.08 | **5.54×** | Rc2 |  |
| c | sub | MQ | P-gen | arm64 | thru | 6.79 | mpdecimal | 24.11 | **3.55×** | Rc2 |  |
| c | sub | OQ | P-gen | arm64 | thru | 12.01 | mpdecimal | 45.81 | **3.81×** | Rc2 |  |
| c | sub | FQ | P-gen | arm64 | thru | 7.49 | mpdecimal | 39.20 | **5.23×** | Rc2 |  |

<!-- END GENERATED sub-rel-c -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-c-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | sub | SQ | P-gen | x86_64 | thru | 5.57 | libbid | 34.25 | **6.15×** | xRc2 |  |
| c | sub | NQ | P-gen | x86_64 | thru | 14.00 | libbid | 36.66 | **2.62×** | xRc2 |  |
| c | sub | MQ | P-gen | x86_64 | thru | 35.32 | libbid | 36.66 | **1.04×** | xRc2 |  |
| c | sub | OQ | P-gen | x86_64 | thru | 46.78 | libbid | 51.52 | **1.10×** | xRc2 |  |
| c | sub | FQ | P-gen | x86_64 | thru | 32.92 | libbid | 34.71 | **1.05×** | xRc2 |  |
| c | sub | SQ | P-gen | x86_64 | thru | 5.57 | decQuad | 58.96 | **10.59×** | xRc2 |  |
| c | sub | NQ | P-gen | x86_64 | thru | 14.00 | decQuad | 87.94 | **6.28×** | xRc2 |  |
| c | sub | MQ | P-gen | x86_64 | thru | 35.32 | decQuad | 84.25 | **2.39×** | xRc2 |  |
| c | sub | OQ | P-gen | x86_64 | thru | 46.78 | decQuad | 95.16 | **2.03×** | xRc2 |  |
| c | sub | FQ | P-gen | x86_64 | thru | 32.92 | decQuad | 78.18 | **2.37×** | xRc2 |  |
| c | sub | SQ | P-gen | x86_64 | thru | 5.57 | mpdecimal | 36.59 | **6.57×** | xRc2 |  |
| c | sub | NQ | P-gen | x86_64 | thru | 14.00 | mpdecimal | 55.74 | **3.98×** | xRc2 |  |
| c | sub | MQ | P-gen | x86_64 | thru | 35.32 | mpdecimal | 55.48 | **1.57×** | xRc2 |  |
| c | sub | OQ | P-gen | x86_64 | thru | 46.78 | mpdecimal | 131.30 | **2.81×** | xRc2 |  |
| c | sub | FQ | P-gen | x86_64 | thru | 32.92 | mpdecimal | 84.62 | **2.57×** | xRc2 |  |

<!-- END GENERATED sub-rel-c-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-c -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | mul | CP | P-gen | arm64 | thru | 1.40 | libbid | 22.86 | **16.33×** | Rc2 | **no scaling** — the cheap multiply |
| c | mul | WP | P-gen | arm64 | thru | 20.04 | libbid | 33.01 | **1.65×** | Rc2 | 128-bit recipMulPow10 |
| c | mul | XP | P-gen | arm64 | thru | 26.75 | libbid | 42.65 | **1.59×** | Rc2 | 256-bit recipMulPow10; **1.19× ≈ the recipmul-256 work-order's 1.18–1.54× band** |
| c | mul | CP | P-gen | arm64 | thru | 1.40 | decQuad | 22.18 | **15.84×** | Rc2 | vs DPD |
| c | mul | WP | P-gen | arm64 | thru | 20.04 | decQuad | 27.52 | **1.37×** | Rc2 | vs DPD |
| c | mul | XP | P-gen | arm64 | thru | 26.75 | decQuad | 30.50 | **1.14×** | Rc2 | **decQuad edges d128 on the widest product** (software DPD's flat cost; libbid still slower) |
| c | mul | CP | P-gen | arm64 | thru | 1.40 | mpdecimal | 21.28 | **15.20×** | Rc2 | no-scale multiply vs libmpdec |
| c | mul | WP | P-gen | arm64 | thru | 20.04 | mpdecimal | 51.84 | **2.59×** | Rc2 | 128-bit recipMulPow10 |
| c | mul | XP | P-gen | arm64 | thru | 26.75 | mpdecimal | 69.02 | **2.58×** | Rc2 | **d128 wins the widest product vs libmpdec** (unlike decQuad) |

<!-- END GENERATED mul-rel-c -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-c-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | mul | CP | P-gen | x86_64 | thru | 4.69 | libbid | 47.38 | **10.10×** | xRc2 |  |
| c | mul | WP | P-gen | x86_64 | thru | 46.64 | libbid | 65.94 | **1.41×** | xRc2 |  |
| c | mul | XP | P-gen | x86_64 | thru | 56.37 | libbid | 96.66 | **1.71×** | xRc2 |  |
| c | mul | CP | P-gen | x86_64 | thru | 4.69 | decQuad | 58.68 | **12.51×** | xRc2 |  |
| c | mul | WP | P-gen | x86_64 | thru | 46.64 | decQuad | 74.20 | **1.59×** | xRc2 |  |
| c | mul | XP | P-gen | x86_64 | thru | 56.37 | decQuad | 91.45 | **1.62×** | xRc2 |  |
| c | mul | CP | P-gen | x86_64 | thru | 4.69 | mpdecimal | 63.30 | **13.50×** | xRc2 |  |
| c | mul | WP | P-gen | x86_64 | thru | 46.64 | mpdecimal | 186.07 | **3.99×** | xRc2 |  |
| c | mul | XP | P-gen | x86_64 | thru | 56.37 | mpdecimal | 238.19 | **4.23×** | xRc2 |  |

<!-- END GENERATED mul-rel-c-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-c -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | div | CD | P-gen | arm64 | thru | 41.39 | libbid | 36.61 | **0.88×** | Rc2 | 128÷64 quotient-first (§2.4.10); **libbid wins** — the compact-divide weakness persists |
| c | div | WD | P-gen | arm64 | thru | 38.23 | libbid | 37.48 | **0.98×** | Rc2 | 256÷64; **≈ parity / slight loss** |
| c | div | XD | P-gen | arm64 | thru | 36.90 | libbid | 39.15 | **1.06×** | Rc2 | 256÷128 Möller–Granlund |
| c | div | ET | P-gen | arm64 | thru | 8.17 | libbid | 10.86 | **1.33×** | Rc2 | **quotient-first exact early-out** — beats libbid's exact fast path |
| c | div | PT | P-gen | arm64 | thru | 3.16 | libbid | 10.64 | **3.37×** | Rc2 | `divPow10Divisor` (§2.4.9); **d128's fastest divide** (coeff-1 form) |
| c | div | CD | P-gen | arm64 | thru | 41.39 | decQuad | 71.11 | **1.72×** | Rc2 | vs DPD |
| c | div | WD | P-gen | arm64 | thru | 38.23 | decQuad | 116.08 | **3.04×** | Rc2 | vs DPD |
| c | div | XD | P-gen | arm64 | thru | 36.90 | decQuad | 173.77 | **4.71×** | Rc2 | vs DPD — decNumber divide is slow |
| c | div | ET | P-gen | arm64 | thru | 8.17 | decQuad | 45.54 | **5.57×** | Rc2 | vs DPD |
| c | div | PT | P-gen | arm64 | thru | 3.16 | decQuad | 43.17 | **13.66×** | Rc2 | vs DPD |
| c | div | CD | P-gen | arm64 | thru | 41.39 | mpdecimal | 58.75 | **1.42×** | Rc2 | **narrowest divide gap** (libmpdec's compact divide is its cheapest, like d128's weakness) |
| c | div | WD | P-gen | arm64 | thru | 38.23 | mpdecimal | 87.45 | **2.29×** | Rc2 | 256÷64 |
| c | div | XD | P-gen | arm64 | thru | 36.90 | mpdecimal | 137.38 | **3.72×** | Rc2 | Cowlishaw signature (CD 59 < WD 87 < XD 144) |
| c | div | ET | P-gen | arm64 | thru | 8.17 | mpdecimal | 57.44 | **7.03×** | Rc2 | libmpdec has no exact early-out |
| c | div | PT | P-gen | arm64 | thru | 3.16 | mpdecimal | 49.40 | **15.63×** | Rc2 | **d128's biggest divide win vs libmpdec** |

<!-- END GENERATED div-rel-c -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-c-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | div | CD | P-gen | x86_64 | thru | 88.17 | libbid | 82.50 | **0.94×** | xRc2 |  |
| c | div | WD | P-gen | x86_64 | thru | 103.94 | libbid | 84.36 | **0.81×** | xRc2 |  |
| c | div | XD | P-gen | x86_64 | thru | 92.88 | libbid | 84.37 | **0.91×** | xRc2 |  |
| c | div | ET | P-gen | x86_64 | thru | 29.28 | libbid | 30.87 | **1.05×** | xRc2 |  |
| c | div | PT | P-gen | x86_64 | thru | 10.10 | libbid | 31.09 | **3.08×** | xRc2 |  |
| c | div | CD | P-gen | x86_64 | thru | 88.17 | decQuad | 141.08 | **1.60×** | xRc2 |  |
| c | div | WD | P-gen | x86_64 | thru | 103.94 | decQuad | 250.81 | **2.41×** | xRc2 |  |
| c | div | XD | P-gen | x86_64 | thru | 92.88 | decQuad | 386.79 | **4.16×** | xRc2 |  |
| c | div | ET | P-gen | x86_64 | thru | 29.28 | decQuad | 98.60 | **3.37×** | xRc2 |  |
| c | div | PT | P-gen | x86_64 | thru | 10.10 | decQuad | 84.57 | **8.37×** | xRc2 |  |
| c | div | CD | P-gen | x86_64 | thru | 88.17 | mpdecimal | 161.54 | **1.83×** | xRc2 |  |
| c | div | WD | P-gen | x86_64 | thru | 103.94 | mpdecimal | 284.94 | **2.74×** | xRc2 |  |
| c | div | XD | P-gen | x86_64 | thru | 92.88 | mpdecimal | 363.97 | **3.92×** | xRc2 |  |
| c | div | ET | P-gen | x86_64 | thru | 29.28 | mpdecimal | 157.26 | **5.37×** | xRc2 |  |
| c | div | PT | P-gen | x86_64 | thru | 10.10 | mpdecimal | 105.98 | **10.49×** | xRc2 |  |

<!-- END GENERATED div-rel-c-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-c -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | fma | FN | FMA | arm64 | thru | 79.12 | libbid | 81.22 | **1.03×** | Rc2 |  |
| c | fma | FF | FMA | arm64 | thru | 41.95 | libbid | 57.36 | **1.37×** | Rc2 |  |
| c | fma | FN | FMA | arm64 | thru | 79.12 | decQuad | 62.68 | **0.79×** | Rc2 |  |
| c | fma | FF | FMA | arm64 | thru | 41.95 | decQuad | 69.96 | **1.67×** | Rc2 |  |
| c | fma | FN | FMA | arm64 | thru | 79.12 | mpdecimal | 88.83 | **1.12×** | Rc2 |  |
| c | fma | FF | FMA | arm64 | thru | 41.95 | mpdecimal | 144.71 | **3.45×** | Rc2 |  |

<!-- END GENERATED fma-rel-c -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-c-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | fma | FN | FMA | x86_64 | thru | 151.81 | libbid | 161.79 | **1.07×** | xRc2 |  |
| c | fma | FF | FMA | x86_64 | thru | 93.23 | libbid | 124.13 | **1.33×** | xRc2 |  |
| c | fma | FN | FMA | x86_64 | thru | 151.81 | decQuad | 148.04 | **0.98×** | xRc2 |  |
| c | fma | FF | FMA | x86_64 | thru | 93.23 | decQuad | 155.81 | **1.67×** | xRc2 |  |
| c | fma | FN | FMA | x86_64 | thru | 151.81 | mpdecimal | 261.29 | **1.72×** | xRc2 |  |
| c | fma | FF | FMA | x86_64 | thru | 93.23 | mpdecimal | 339.01 | **3.64×** | xRc2 |  |

<!-- END GENERATED fma-rel-c-x86 -->

</div>
