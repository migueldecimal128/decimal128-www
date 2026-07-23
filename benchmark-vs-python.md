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
| python | add | MIX | P-fin | arm64 | thru | 24.86 | decimal.Decimal | 62.00 | **2.49×** | Rpysw2 | compact idiom peer |
| python | sub | MIX | P-fin | arm64 | thru | 22.84 | decimal.Decimal | 62.47 | **2.74×** | Rpysw2 | compact idiom peer |
| python | mul | CP | P-fin | arm64 | thru | 16.55 | decimal.Decimal | 64.07 | **3.87×** | Rpysw2 | compact idiom peer |
| python | mul | WP | P-fin | arm64 | thru | 38.49 | decimal.Decimal | 68.23 | **1.77×** | Rpysw2 | compact idiom peer |
| python | div | CD | P-fin | arm64 | thru | 59.57 | decimal.Decimal | 95.54 | **1.60×** | Rpysw2 | compact idiom peer |
| python | div | WD | P-fin | arm64 | thru | 66.53 | decimal.Decimal | 98.82 | **1.49×** | Rpysw2 | compact idiom peer |
| python | div | ET | P-fin | arm64 | thru | 21.74 | decimal.Decimal | 86.00 | **3.96×** | Rpysw2 | compact idiom peer |
| python | div | PT | P-fin | arm64 | thru | 18.34 | decimal.Decimal | 83.76 | **4.57×** | Rpysw2 | compact idiom peer |

<!-- END GENERATED pfin-rel-python -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-python-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | add | MIX | P-fin | x86_64 | thru | 49.58 | decimal.Decimal | 128.19 | **2.59×** | xRpysw2 | compact idiom peer |
| python | sub | MIX | P-fin | x86_64 | thru | 46.44 | decimal.Decimal | 127.06 | **2.74×** | xRpysw2 | compact idiom peer |
| python | mul | CP | P-fin | x86_64 | thru | 39.38 | decimal.Decimal | 116.11 | **2.95×** | xRpysw2 | compact idiom peer |
| python | mul | WP | P-fin | x86_64 | thru | 77.05 | decimal.Decimal | 136.59 | **1.77×** | xRpysw2 | compact idiom peer |
| python | div | CD | P-fin | x86_64 | thru | 114.36 | decimal.Decimal | 210.13 | **1.84×** | xRpysw2 | compact idiom peer |
| python | div | WD | P-fin | x86_64 | thru | 128.60 | decimal.Decimal | 232.63 | **1.81×** | xRpysw2 | compact idiom peer |
| python | div | ET | P-fin | x86_64 | thru | 55.28 | decimal.Decimal | 189.98 | **3.44×** | xRpysw2 | compact idiom peer |
| python | div | PT | P-fin | x86_64 | thru | 44.19 | decimal.Decimal | 182.85 | **4.14×** | xRpysw2 | compact idiom peer |

<!-- END GENERATED pfin-rel-python-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-python -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | add | SQ | P-gen | arm64 | thru | 22.10 | decimal.Decimal | 62.28 | **2.82×** | Rpysw2 | compact idiom peer |
| python | add | NQ | P-gen | arm64 | thru | 22.41 | decimal.Decimal | 72.80 | **3.25×** | Rpysw2 | compact idiom peer |
| python | add | MQ | P-gen | arm64 | thru | 27.33 | decimal.Decimal | 72.82 | **2.66×** | Rpysw2 | compact idiom peer |
| python | add | OQ | P-gen | arm64 | thru | 38.42 | decimal.Decimal | 86.77 | **2.26×** | Rpysw2 | compact idiom peer |
| python | add | FQ | P-gen | arm64 | thru | 32.98 | decimal.Decimal | 82.11 | **2.49×** | Rpysw2 | compact idiom peer |

<!-- END GENERATED add-rel-python -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-python-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | add | SQ | P-gen | x86_64 | thru | 46.78 | decimal.Decimal | 124.88 | **2.67×** | xRpysw2 | compact idiom peer |
| python | add | NQ | P-gen | x86_64 | thru | 49.80 | decimal.Decimal | 144.98 | **2.91×** | xRpysw2 | compact idiom peer |
| python | add | MQ | P-gen | x86_64 | thru | 64.67 | decimal.Decimal | 148.85 | **2.30×** | xRpysw2 | compact idiom peer |
| python | add | OQ | P-gen | x86_64 | thru | 74.68 | decimal.Decimal | 170.91 | **2.29×** | xRpysw2 | compact idiom peer |
| python | add | FQ | P-gen | x86_64 | thru | 65.32 | decimal.Decimal | 167.26 | **2.56×** | xRpysw2 | compact idiom peer |

<!-- END GENERATED add-rel-python-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-python -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | sub | SQ | P-gen | arm64 | thru | 20.30 | decimal.Decimal | 58.86 | **2.90×** | Rpysw2 | compact idiom peer |
| python | sub | NQ | P-gen | arm64 | thru | 22.73 | decimal.Decimal | 71.20 | **3.13×** | Rpysw2 | compact idiom peer |
| python | sub | MQ | P-gen | arm64 | thru | 27.36 | decimal.Decimal | 72.36 | **2.64×** | Rpysw2 | compact idiom peer |
| python | sub | OQ | P-gen | arm64 | thru | 38.89 | decimal.Decimal | 85.70 | **2.20×** | Rpysw2 | compact idiom peer |
| python | sub | FQ | P-gen | arm64 | thru | 32.94 | decimal.Decimal | 80.52 | **2.44×** | Rpysw2 | compact idiom peer |

<!-- END GENERATED sub-rel-python -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-python-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | sub | SQ | P-gen | x86_64 | thru | 43.28 | decimal.Decimal | 125.79 | **2.91×** | xRpysw2 | compact idiom peer |
| python | sub | NQ | P-gen | x86_64 | thru | 49.32 | decimal.Decimal | 145.23 | **2.94×** | xRpysw2 | compact idiom peer |
| python | sub | MQ | P-gen | x86_64 | thru | 65.98 | decimal.Decimal | 147.79 | **2.24×** | xRpysw2 | compact idiom peer |
| python | sub | OQ | P-gen | x86_64 | thru | 74.12 | decimal.Decimal | 172.99 | **2.33×** | xRpysw2 | compact idiom peer |
| python | sub | FQ | P-gen | x86_64 | thru | 66.69 | decimal.Decimal | 167.99 | **2.52×** | xRpysw2 | compact idiom peer |

<!-- END GENERATED sub-rel-python-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-python -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | mul | CP | P-gen | arm64 | thru | 18.93 | decimal.Decimal | 63.91 | **3.38×** | Rpysw2 | compact idiom peer |
| python | mul | WP | P-gen | arm64 | thru | 38.60 | decimal.Decimal | 73.93 | **1.92×** | Rpysw2 | compact idiom peer |
| python | mul | XP | P-gen | arm64 | thru | 44.61 | decimal.Decimal | 92.32 | **2.07×** | Rpysw2 | compact idiom peer |

<!-- END GENERATED mul-rel-python -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-python-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | mul | CP | P-gen | x86_64 | thru | 42.50 | decimal.Decimal | 118.09 | **2.78×** | xRpysw2 | compact idiom peer |
| python | mul | WP | P-gen | x86_64 | thru | 76.97 | decimal.Decimal | 143.11 | **1.86×** | xRpysw2 | compact idiom peer |
| python | mul | XP | P-gen | x86_64 | thru | 90.70 | decimal.Decimal | 162.30 | **1.79×** | xRpysw2 | compact idiom peer |

<!-- END GENERATED mul-rel-python-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-python -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | div | CD | P-gen | arm64 | thru | 59.36 | decimal.Decimal | 101.28 | **1.71×** | Rpysw2 | compact idiom peer |
| python | div | WD | P-gen | arm64 | thru | 65.13 | decimal.Decimal | 104.28 | **1.60×** | Rpysw2 | compact idiom peer |
| python | div | XD | P-gen | arm64 | thru | 62.48 | decimal.Decimal | 167.48 | **2.68×** | Rpysw2 | compact idiom peer |
| python | div | ET | P-gen | arm64 | thru | 24.41 | decimal.Decimal | 94.46 | **3.87×** | Rpysw2 | compact idiom peer |
| python | div | PT | P-gen | arm64 | thru | 18.34 | decimal.Decimal | 90.30 | **4.92×** | Rpysw2 | compact idiom peer |

<!-- END GENERATED div-rel-python -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-python-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | div | CD | P-gen | x86_64 | thru | 115.87 | decimal.Decimal | 218.17 | **1.88×** | xRpysw2 | compact idiom peer |
| python | div | WD | P-gen | x86_64 | thru | 126.30 | decimal.Decimal | 231.83 | **1.84×** | xRpysw2 | compact idiom peer |
| python | div | XD | P-gen | x86_64 | thru | 119.02 | decimal.Decimal | 350.89 | **2.95×** | xRpysw2 | compact idiom peer |
| python | div | ET | P-gen | x86_64 | thru | 65.54 | decimal.Decimal | 204.19 | **3.12×** | xRpysw2 | compact idiom peer |
| python | div | PT | P-gen | x86_64 | thru | 44.33 | decimal.Decimal | 187.39 | **4.23×** | xRpysw2 | compact idiom peer |

<!-- END GENERATED div-rel-python-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-python -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | fma | FN | FMA | arm64 | thru | 108.32 | decimal.Decimal | 142.29 | **1.31×** | Rpysw2 | compact idiom peer |
| python | fma | FF | FMA | arm64 | thru | 79.75 | decimal.Decimal | 163.28 | **2.05×** | Rpysw2 | compact idiom peer |

<!-- END GENERATED fma-rel-python -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-python-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | fma | FN | FMA | x86_64 | thru | 229.88 | decimal.Decimal | 290.52 | **1.26×** | xRpysw2 | compact idiom peer |
| python | fma | FF | FMA | x86_64 | thru | 190.33 | decimal.Decimal | 337.71 | **1.77×** | xRpysw2 | compact idiom peer |

<!-- END GENERATED fma-rel-python-x86 -->

</div>
