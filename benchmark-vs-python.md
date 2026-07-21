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

A quick-glance rollup before the detailed tables below: the min–max `ratio = alt / ours` (&gt; 1× ⇒ d128 faster) for each operation on x86_64 (Intel i9-9880H) for Python's idiom peer (`decimal.Decimal`), split by profile.

| Operation | P-fin range | P-gen range |
|---|---|---|
| Add | 2.6× | 2.2× – 3× |
| Subtract | 2.7× | 2.2× – 2.9× |
| Multiply | 1.7× – 3× | 1.9× – 2.8× |
| Divide | 1.8× – 4× | 1.8× – 4× |

## FinMix — realistic financial mix (P-fin)

The headline: one realistic 64-bit financial operation mix — a `MIX` add/sub stream, mul `CP`/`WP`, div `CD`/`WD`/`ET`/`PT` — `ratio = alt / ours` (&gt; 1 ⇒ d128 faster). This is the profile closest to real financial code.

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED pfin-rel-python -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | add | MIX | P-fin | arm64 | thru | 24.44 | decimal.Decimal | 64.71 | **2.65×** | Rpysw2 | compact idiom peer |
| python | sub | MIX | P-fin | arm64 | thru | 22.99 | decimal.Decimal | 62.23 | **2.71×** | Rpysw2 | compact idiom peer |
| python | mul | CP | P-fin | arm64 | thru | 16.65 | decimal.Decimal | 62.76 | **3.77×** | Rpysw2 | compact idiom peer |
| python | mul | WP | P-fin | arm64 | thru | 38.17 | decimal.Decimal | 67.45 | **1.77×** | Rpysw2 | compact idiom peer |
| python | div | CD | P-fin | arm64 | thru | 60.00 | decimal.Decimal | 96.43 | **1.61×** | Rpysw2 | compact idiom peer |
| python | div | WD | P-fin | arm64 | thru | 66.13 | decimal.Decimal | 100.24 | **1.52×** | Rpysw2 | compact idiom peer |
| python | div | ET | P-fin | arm64 | thru | 22.11 | decimal.Decimal | 85.68 | **3.88×** | Rpysw2 | compact idiom peer |
| python | div | PT | P-fin | arm64 | thru | 18.32 | decimal.Decimal | 83.53 | **4.56×** | Rpysw2 | compact idiom peer |

<!-- END GENERATED pfin-rel-python -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-python-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | add | MIX | P-fin | x86_64 | thru | 48.66 | decimal.Decimal | 125.37 | **2.58×** | xRpysw2 | compact idiom peer |
| python | sub | MIX | P-fin | x86_64 | thru | 46.33 | decimal.Decimal | 125.50 | **2.71×** | xRpysw2 | compact idiom peer |
| python | mul | CP | P-fin | x86_64 | thru | 38.95 | decimal.Decimal | 119.69 | **3.07×** | xRpysw2 | compact idiom peer |
| python | mul | WP | P-fin | x86_64 | thru | 76.53 | decimal.Decimal | 133.20 | **1.74×** | xRpysw2 | compact idiom peer |
| python | div | CD | P-fin | x86_64 | thru | 113.68 | decimal.Decimal | 209.71 | **1.84×** | xRpysw2 | compact idiom peer |
| python | div | WD | P-fin | x86_64 | thru | 126.57 | decimal.Decimal | 230.16 | **1.82×** | xRpysw2 | compact idiom peer |
| python | div | ET | P-fin | x86_64 | thru | 55.53 | decimal.Decimal | 186.48 | **3.36×** | xRpysw2 | compact idiom peer |
| python | div | PT | P-fin | x86_64 | thru | 43.66 | decimal.Decimal | 179.55 | **4.11×** | xRpysw2 | compact idiom peer |

<!-- END GENERATED pfin-rel-python-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-python -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | add | SQ | P-gen | arm64 | thru | 24.02 | decimal.Decimal | 61.64 | **2.57×** | Rpysw2 | compact idiom peer |
| python | add | NQ | P-gen | arm64 | thru | 22.34 | decimal.Decimal | 71.62 | **3.21×** | Rpysw2 | compact idiom peer |
| python | add | MQ | P-gen | arm64 | thru | 29.81 | decimal.Decimal | 71.71 | **2.41×** | Rpysw2 | compact idiom peer |
| python | add | OQ | P-gen | arm64 | thru | 39.74 | decimal.Decimal | 85.75 | **2.16×** | Rpysw2 | compact idiom peer |
| python | add | FQ | P-gen | arm64 | thru | 32.73 | decimal.Decimal | 80.83 | **2.47×** | Rpysw2 | compact idiom peer |

<!-- END GENERATED add-rel-python -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-python-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | add | SQ | P-gen | x86_64 | thru | 46.56 | decimal.Decimal | 122.06 | **2.62×** | xRpysw2 | compact idiom peer |
| python | add | NQ | P-gen | x86_64 | thru | 48.77 | decimal.Decimal | 146.11 | **3.00×** | xRpysw2 | compact idiom peer |
| python | add | MQ | P-gen | x86_64 | thru | 64.72 | decimal.Decimal | 142.40 | **2.20×** | xRpysw2 | compact idiom peer |
| python | add | OQ | P-gen | x86_64 | thru | 72.84 | decimal.Decimal | 170.96 | **2.35×** | xRpysw2 | compact idiom peer |
| python | add | FQ | P-gen | x86_64 | thru | 64.31 | decimal.Decimal | 167.15 | **2.60×** | xRpysw2 | compact idiom peer |

<!-- END GENERATED add-rel-python-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-python -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | sub | SQ | P-gen | arm64 | thru | 21.12 | decimal.Decimal | 63.46 | **3.00×** | Rpysw2 | compact idiom peer |
| python | sub | NQ | P-gen | arm64 | thru | 22.47 | decimal.Decimal | 73.16 | **3.26×** | Rpysw2 | compact idiom peer |
| python | sub | MQ | P-gen | arm64 | thru | 29.81 | decimal.Decimal | 72.65 | **2.44×** | Rpysw2 | compact idiom peer |
| python | sub | OQ | P-gen | arm64 | thru | 39.48 | decimal.Decimal | 86.03 | **2.18×** | Rpysw2 | compact idiom peer |
| python | sub | FQ | P-gen | arm64 | thru | 32.58 | decimal.Decimal | 81.53 | **2.50×** | Rpysw2 | compact idiom peer |

<!-- END GENERATED sub-rel-python -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-python-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | sub | SQ | P-gen | x86_64 | thru | 42.63 | decimal.Decimal | 121.05 | **2.84×** | xRpysw2 | compact idiom peer |
| python | sub | NQ | P-gen | x86_64 | thru | 48.62 | decimal.Decimal | 142.87 | **2.94×** | xRpysw2 | compact idiom peer |
| python | sub | MQ | P-gen | x86_64 | thru | 64.47 | decimal.Decimal | 143.60 | **2.23×** | xRpysw2 | compact idiom peer |
| python | sub | OQ | P-gen | x86_64 | thru | 73.37 | decimal.Decimal | 171.05 | **2.33×** | xRpysw2 | compact idiom peer |
| python | sub | FQ | P-gen | x86_64 | thru | 65.59 | decimal.Decimal | 168.41 | **2.57×** | xRpysw2 | compact idiom peer |

<!-- END GENERATED sub-rel-python-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-python -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | mul | CP | P-gen | arm64 | thru | 19.12 | decimal.Decimal | 63.55 | **3.32×** | Rpysw2 | compact idiom peer |
| python | mul | WP | P-gen | arm64 | thru | 38.31 | decimal.Decimal | 73.27 | **1.91×** | Rpysw2 | compact idiom peer |
| python | mul | XP | P-gen | arm64 | thru | 47.89 | decimal.Decimal | 91.68 | **1.91×** | Rpysw2 | compact idiom peer |

<!-- END GENERATED mul-rel-python -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-python-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | mul | CP | P-gen | x86_64 | thru | 42.70 | decimal.Decimal | 118.82 | **2.78×** | xRpysw2 | compact idiom peer |
| python | mul | WP | P-gen | x86_64 | thru | 75.70 | decimal.Decimal | 141.21 | **1.87×** | xRpysw2 | compact idiom peer |
| python | mul | XP | P-gen | x86_64 | thru | 88.72 | decimal.Decimal | 164.32 | **1.85×** | xRpysw2 | compact idiom peer |

<!-- END GENERATED mul-rel-python-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-python -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | div | CD | P-gen | arm64 | thru | 58.75 | decimal.Decimal | 98.62 | **1.68×** | Rpysw2 | compact idiom peer |
| python | div | WD | P-gen | arm64 | thru | 65.11 | decimal.Decimal | 100.54 | **1.54×** | Rpysw2 | compact idiom peer |
| python | div | XD | P-gen | arm64 | thru | 63.27 | decimal.Decimal | 163.86 | **2.59×** | Rpysw2 | compact idiom peer |
| python | div | ET | P-gen | arm64 | thru | 24.44 | decimal.Decimal | 91.88 | **3.76×** | Rpysw2 | compact idiom peer |
| python | div | PT | P-gen | arm64 | thru | 18.25 | decimal.Decimal | 90.38 | **4.95×** | Rpysw2 | compact idiom peer |

<!-- END GENERATED div-rel-python -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-python-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | div | CD | P-gen | x86_64 | thru | 115.88 | decimal.Decimal | 213.03 | **1.84×** | xRpysw2 | compact idiom peer |
| python | div | WD | P-gen | x86_64 | thru | 125.94 | decimal.Decimal | 235.91 | **1.87×** | xRpysw2 | compact idiom peer |
| python | div | XD | P-gen | x86_64 | thru | 117.43 | decimal.Decimal | 345.32 | **2.94×** | xRpysw2 | compact idiom peer |
| python | div | ET | P-gen | x86_64 | thru | 64.53 | decimal.Decimal | 205.85 | **3.19×** | xRpysw2 | compact idiom peer |
| python | div | PT | P-gen | x86_64 | thru | 44.58 | decimal.Decimal | 187.65 | **4.21×** | xRpysw2 | compact idiom peer |

<!-- END GENERATED div-rel-python-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-python -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | fma | FN | FMA | arm64 | thru | 112.13 | decimal.Decimal | 142.15 | **1.27×** | Rpysw2 | compact idiom peer |
| python | fma | FF | FMA | arm64 | thru | 81.48 | decimal.Decimal | 164.49 | **2.02×** | Rpysw2 | compact idiom peer |

<!-- END GENERATED fma-rel-python -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-python-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | fma | FN | FMA | x86_64 | thru | 219.47 | decimal.Decimal | 280.07 | **1.28×** | xRpysw2 | compact idiom peer |
| python | fma | FF | FMA | x86_64 | thru | 183.06 | decimal.Decimal | 332.59 | **1.82×** | xRpysw2 | compact idiom peer |

<!-- END GENERATED fma-rel-python-x86 -->

</div>
