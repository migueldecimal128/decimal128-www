---
layout: default
permalink: /benchmark/vs-python.html
title: "Python Benchmark Results — Decimal128"
description: "decimal128 in Python, measured against the alternatives available to it — a realistic financial mix (P-fin) plus per-operation band characterization, with explicit ratios."
heading: "Python Benchmark Results"
---

<div class="whitepaper" markdown="1">

<p class="whitepaper-meta">Living document — as-measured results. Category codes, profiles, modes &amp; method: <a href="key.html">Benchmark Key</a>.</p>

This is the **Python** view of decimal128 **as-measured**, band by band, with explicit ratios. It opens with the realistic financial-mix (**P-fin**) headline, then the per-operation band characterization (**P-gen**) and FMA. In Python, d128 is measured against its in-language idiom peer **`decimal.Decimal`**, falling back to the **libbid** universal reference where it cannot represent the band. It is **data only** — the categories, magnitude profiles, units, and methodology are defined in the [Benchmark Key](key.html) (and, authoritatively, `BenchmarkMatrix.md`). The cross-port d128 band-shape matrices (all ports, no alternatives) live in [Port-Comparison Benchmark Results](port-compare.html); the full index of per-language pages is on the [Benchmarks](/benchmarks.html) hub.

## Summary — Ratio Range by Operation

The ratio for Python's idiom peer on x86_64 (Intel i9-9880H): `ratio = decimal.Decimal / Miguel` (&gt; 1× ⇒ d128 faster), broken out by operation.

| | Add | Subtract | Multiply | Divide |
|---|---|---|---|---|
| ratio = decimal.Decimal / Miguel | 2.6× | 2.7× | 1.7× – 3× | 1.8× – 4× |

## FinMix — realistic financial mix (P-fin)

The headline: one realistic 64-bit financial operation mix — a `MIX` add/sub stream, mul `CP`/`WP`, div `CD`/`WD`/`ET`/`PT` — `ratio = alt / Miguel` (&gt; 1 ⇒ d128 faster). This is the profile closest to real financial code.

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED pfin-rel-python -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | add | MIX | P-fin | arm64 | thru | 22.31 | decimal.Decimal | 61.44 | **2.75×** | Rpysw2 | compact idiom peer |
| python | sub | MIX | P-fin | arm64 | thru | 20.41 | decimal.Decimal | 63.58 | **3.12×** | Rpysw2 | compact idiom peer |
| python | mul | CP | P-fin | arm64 | thru | 16.69 | decimal.Decimal | 62.70 | **3.76×** | Rpysw2 | compact idiom peer |
| python | mul | WP | P-fin | arm64 | thru | 38.49 | decimal.Decimal | 66.31 | **1.72×** | Rpysw2 | compact idiom peer |
| python | div | CD | P-fin | arm64 | thru | 60.11 | decimal.Decimal | 96.71 | **1.61×** | Rpysw2 | compact idiom peer |
| python | div | WD | P-fin | arm64 | thru | 65.32 | decimal.Decimal | 97.85 | **1.50×** | Rpysw2 | compact idiom peer |
| python | div | ET | P-fin | arm64 | thru | 21.63 | decimal.Decimal | 85.51 | **3.95×** | Rpysw2 | compact idiom peer |
| python | div | PT | P-fin | arm64 | thru | 18.38 | decimal.Decimal | 82.92 | **4.51×** | Rpysw2 | compact idiom peer |

<!-- END GENERATED pfin-rel-python -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-python-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | add | MIX | P-fin | x86_64 | thru | 44.94 | decimal.Decimal | 126.47 | **2.81×** | xRpysw2 | compact idiom peer |
| python | sub | MIX | P-fin | x86_64 | thru | 45.81 | decimal.Decimal | 126.35 | **2.76×** | xRpysw2 | compact idiom peer |
| python | mul | CP | P-fin | x86_64 | thru | 39.10 | decimal.Decimal | 115.66 | **2.96×** | xRpysw2 | compact idiom peer |
| python | mul | WP | P-fin | x86_64 | thru | 76.91 | decimal.Decimal | 132.73 | **1.73×** | xRpysw2 | compact idiom peer |
| python | div | CD | P-fin | x86_64 | thru | 114.23 | decimal.Decimal | 208.07 | **1.82×** | xRpysw2 | compact idiom peer |
| python | div | WD | P-fin | x86_64 | thru | 124.50 | decimal.Decimal | 228.09 | **1.83×** | xRpysw2 | compact idiom peer |
| python | div | ET | P-fin | x86_64 | thru | 54.29 | decimal.Decimal | 186.32 | **3.43×** | xRpysw2 | compact idiom peer |
| python | div | PT | P-fin | x86_64 | thru | 43.37 | decimal.Decimal | 177.04 | **4.08×** | xRpysw2 | compact idiom peer |

<!-- END GENERATED pfin-rel-python-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-python -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | add | SQ | P-gen | arm64 | thru | 23.20 | decimal.Decimal | 61.65 | **2.66×** | Rpysw2 | compact idiom peer |
| python | add | NQ | P-gen | arm64 | thru | 23.02 | decimal.Decimal | 71.74 | **3.12×** | Rpysw2 | compact idiom peer |
| python | add | MQ | P-gen | arm64 | thru | 27.99 | decimal.Decimal | 72.81 | **2.60×** | Rpysw2 | compact idiom peer |
| python | add | OQ | P-gen | arm64 | thru | 39.76 | decimal.Decimal | 87.15 | **2.19×** | Rpysw2 | compact idiom peer |
| python | add | FQ | P-gen | arm64 | thru | 33.32 | decimal.Decimal | 81.80 | **2.45×** | Rpysw2 | compact idiom peer |

<!-- END GENERATED add-rel-python -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-python-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | add | SQ | P-gen | x86_64 | thru | 43.04 | decimal.Decimal | 120.72 | **2.80×** | xRpysw2 | compact idiom peer |
| python | add | NQ | P-gen | x86_64 | thru | 45.08 | decimal.Decimal | 138.56 | **3.07×** | xRpysw2 | compact idiom peer |
| python | add | MQ | P-gen | x86_64 | thru | 54.57 | decimal.Decimal | 141.12 | **2.59×** | xRpysw2 | compact idiom peer |
| python | add | OQ | P-gen | x86_64 | thru | 70.69 | decimal.Decimal | 169.21 | **2.39×** | xRpysw2 | compact idiom peer |
| python | add | FQ | P-gen | x86_64 | thru | 61.73 | decimal.Decimal | 161.05 | **2.61×** | xRpysw2 | compact idiom peer |

<!-- END GENERATED add-rel-python-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-python -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | sub | SQ | P-gen | arm64 | thru | 20.49 | decimal.Decimal | 61.32 | **2.99×** | Rpysw2 | compact idiom peer |
| python | sub | NQ | P-gen | arm64 | thru | 23.50 | decimal.Decimal | 71.65 | **3.05×** | Rpysw2 | compact idiom peer |
| python | sub | MQ | P-gen | arm64 | thru | 28.51 | decimal.Decimal | 71.15 | **2.50×** | Rpysw2 | compact idiom peer |
| python | sub | OQ | P-gen | arm64 | thru | 39.83 | decimal.Decimal | 86.44 | **2.17×** | Rpysw2 | compact idiom peer |
| python | sub | FQ | P-gen | arm64 | thru | 33.67 | decimal.Decimal | 80.25 | **2.38×** | Rpysw2 | compact idiom peer |

<!-- END GENERATED sub-rel-python -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-python-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | sub | SQ | P-gen | x86_64 | thru | 40.72 | decimal.Decimal | 118.37 | **2.91×** | xRpysw2 | compact idiom peer |
| python | sub | NQ | P-gen | x86_64 | thru | 46.69 | decimal.Decimal | 137.99 | **2.96×** | xRpysw2 | compact idiom peer |
| python | sub | MQ | P-gen | x86_64 | thru | 56.16 | decimal.Decimal | 139.95 | **2.49×** | xRpysw2 | compact idiom peer |
| python | sub | OQ | P-gen | x86_64 | thru | 72.58 | decimal.Decimal | 163.88 | **2.26×** | xRpysw2 | compact idiom peer |
| python | sub | FQ | P-gen | x86_64 | thru | 62.54 | decimal.Decimal | 164.32 | **2.63×** | xRpysw2 | compact idiom peer |

<!-- END GENERATED sub-rel-python-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-python -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | mul | CP | P-gen | arm64 | thru | 19.12 | decimal.Decimal | 63.73 | **3.33×** | Rpysw2 | compact idiom peer |
| python | mul | WP | P-gen | arm64 | thru | 38.70 | decimal.Decimal | 74.79 | **1.93×** | Rpysw2 | compact idiom peer |
| python | mul | XP | P-gen | arm64 | thru | 45.06 | decimal.Decimal | 91.48 | **2.03×** | Rpysw2 | compact idiom peer |

<!-- END GENERATED mul-rel-python -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-python-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | mul | CP | P-gen | x86_64 | thru | 40.26 | decimal.Decimal | 112.84 | **2.80×** | xRpysw2 | compact idiom peer |
| python | mul | WP | P-gen | x86_64 | thru | 74.54 | decimal.Decimal | 137.20 | **1.84×** | xRpysw2 | compact idiom peer |
| python | mul | XP | P-gen | x86_64 | thru | 89.62 | decimal.Decimal | 156.37 | **1.74×** | xRpysw2 | compact idiom peer |

<!-- END GENERATED mul-rel-python-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-python -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | div | CD | P-gen | arm64 | thru | 58.85 | decimal.Decimal | 98.45 | **1.67×** | Rpysw2 | compact idiom peer |
| python | div | WD | P-gen | arm64 | thru | 65.52 | decimal.Decimal | 102.90 | **1.57×** | Rpysw2 | compact idiom peer |
| python | div | XD | P-gen | arm64 | thru | 63.22 | decimal.Decimal | 166.68 | **2.64×** | Rpysw2 | compact idiom peer |
| python | div | ET | P-gen | arm64 | thru | 25.16 | decimal.Decimal | 92.01 | **3.66×** | Rpysw2 | compact idiom peer |
| python | div | PT | P-gen | arm64 | thru | 18.55 | decimal.Decimal | 89.00 | **4.80×** | Rpysw2 | compact idiom peer |

<!-- END GENERATED div-rel-python -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-python-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | div | CD | P-gen | x86_64 | thru | 113.16 | decimal.Decimal | 207.04 | **1.83×** | xRpysw2 | compact idiom peer |
| python | div | WD | P-gen | x86_64 | thru | 122.92 | decimal.Decimal | 224.06 | **1.82×** | xRpysw2 | compact idiom peer |
| python | div | XD | P-gen | x86_64 | thru | 113.20 | decimal.Decimal | 330.52 | **2.92×** | xRpysw2 | compact idiom peer |
| python | div | ET | P-gen | x86_64 | thru | 62.56 | decimal.Decimal | 195.34 | **3.12×** | xRpysw2 | compact idiom peer |
| python | div | PT | P-gen | x86_64 | thru | 42.30 | decimal.Decimal | 177.91 | **4.21×** | xRpysw2 | compact idiom peer |

<!-- END GENERATED div-rel-python-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-python -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | fma | FN | FMA | arm64 | thru | 108.28 | decimal.Decimal | 141.46 | **1.31×** | Rpysw2 | compact idiom peer |
| python | fma | FF | FMA | arm64 | thru | 80.05 | decimal.Decimal | 163.28 | **2.04×** | Rpysw2 | compact idiom peer |

<!-- END GENERATED fma-rel-python -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-python-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | fma | FN | FMA | x86_64 | thru | 218.62 | decimal.Decimal | 279.68 | **1.28×** | xRpysw2 | compact idiom peer |
| python | fma | FF | FMA | x86_64 | thru | 178.93 | decimal.Decimal | 319.51 | **1.79×** | xRpysw2 | compact idiom peer |

<!-- END GENERATED fma-rel-python-x86 -->

</div>
