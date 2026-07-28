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
| python | add | MIX | P-fin | arm64 | thru | 21.48 | decimal.Decimal | 59.65 | **2.78×** | Rpysw2 | compact idiom peer |
| python | sub | MIX | P-fin | arm64 | thru | 20.04 | decimal.Decimal | 60.43 | **3.02×** | Rpysw2 | compact idiom peer |
| python | mul | CP | P-fin | arm64 | thru | 16.57 | decimal.Decimal | 63.25 | **3.82×** | Rpysw2 | compact idiom peer |
| python | mul | WP | P-fin | arm64 | thru | 38.96 | decimal.Decimal | 68.46 | **1.76×** | Rpysw2 | compact idiom peer |
| python | div | CD | P-fin | arm64 | thru | 55.10 | decimal.Decimal | 95.32 | **1.73×** | Rpysw2 | compact idiom peer |
| python | div | WD | P-fin | arm64 | thru | 66.62 | decimal.Decimal | 98.84 | **1.48×** | Rpysw2 | compact idiom peer |
| python | div | ET | P-fin | arm64 | thru | 21.43 | decimal.Decimal | 86.58 | **4.04×** | Rpysw2 | compact idiom peer |
| python | div | PT | P-fin | arm64 | thru | 18.37 | decimal.Decimal | 84.35 | **4.59×** | Rpysw2 | compact idiom peer |

<!-- END GENERATED pfin-rel-python -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-python-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | add | MIX | P-fin | x86_64 | thru | 42.82 | decimal.Decimal | 117.39 | **2.74×** | xRpysw2 | compact idiom peer |
| python | sub | MIX | P-fin | x86_64 | thru | 44.27 | decimal.Decimal | 121.26 | **2.74×** | xRpysw2 | compact idiom peer |
| python | mul | CP | P-fin | x86_64 | thru | 39.57 | decimal.Decimal | 113.47 | **2.87×** | xRpysw2 | compact idiom peer |
| python | mul | WP | P-fin | x86_64 | thru | 76.92 | decimal.Decimal | 130.59 | **1.70×** | xRpysw2 | compact idiom peer |
| python | div | CD | P-fin | x86_64 | thru | 104.83 | decimal.Decimal | 204.74 | **1.95×** | xRpysw2 | compact idiom peer |
| python | div | WD | P-fin | x86_64 | thru | 120.36 | decimal.Decimal | 225.19 | **1.87×** | xRpysw2 | compact idiom peer |
| python | div | ET | P-fin | x86_64 | thru | 53.42 | decimal.Decimal | 186.25 | **3.49×** | xRpysw2 | compact idiom peer |
| python | div | PT | P-fin | x86_64 | thru | 43.79 | decimal.Decimal | 174.98 | **4.00×** | xRpysw2 | compact idiom peer |

<!-- END GENERATED pfin-rel-python-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-python -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | add | SQ | P-gen | arm64 | thru | 21.52 | decimal.Decimal | 60.46 | **2.81×** | Rpysw2 | compact idiom peer |
| python | add | NQ | P-gen | arm64 | thru | 23.12 | decimal.Decimal | 71.77 | **3.10×** | Rpysw2 | compact idiom peer |
| python | add | MQ | P-gen | arm64 | thru | 27.92 | decimal.Decimal | 72.34 | **2.59×** | Rpysw2 | compact idiom peer |
| python | add | OQ | P-gen | arm64 | thru | 39.29 | decimal.Decimal | 85.92 | **2.19×** | Rpysw2 | compact idiom peer |
| python | add | FQ | P-gen | arm64 | thru | 33.75 | decimal.Decimal | 81.94 | **2.43×** | Rpysw2 | compact idiom peer |

<!-- END GENERATED add-rel-python -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-python-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | add | SQ | P-gen | x86_64 | thru | 43.84 | decimal.Decimal | 123.38 | **2.81×** | xRpysw2 | compact idiom peer |
| python | add | NQ | P-gen | x86_64 | thru | 48.57 | decimal.Decimal | 139.79 | **2.88×** | xRpysw2 | compact idiom peer |
| python | add | MQ | P-gen | x86_64 | thru | 57.55 | decimal.Decimal | 149.44 | **2.60×** | xRpysw2 | compact idiom peer |
| python | add | OQ | P-gen | x86_64 | thru | 73.98 | decimal.Decimal | 166.09 | **2.25×** | xRpysw2 | compact idiom peer |
| python | add | FQ | P-gen | x86_64 | thru | 64.13 | decimal.Decimal | 163.26 | **2.55×** | xRpysw2 | compact idiom peer |

<!-- END GENERATED add-rel-python-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-python -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | sub | SQ | P-gen | arm64 | thru | 20.77 | decimal.Decimal | 59.43 | **2.86×** | Rpysw2 | compact idiom peer |
| python | sub | NQ | P-gen | arm64 | thru | 23.25 | decimal.Decimal | 71.64 | **3.08×** | Rpysw2 | compact idiom peer |
| python | sub | MQ | P-gen | arm64 | thru | 27.94 | decimal.Decimal | 71.26 | **2.55×** | Rpysw2 | compact idiom peer |
| python | sub | OQ | P-gen | arm64 | thru | 39.33 | decimal.Decimal | 85.82 | **2.18×** | Rpysw2 | compact idiom peer |
| python | sub | FQ | P-gen | arm64 | thru | 33.33 | decimal.Decimal | 80.48 | **2.41×** | Rpysw2 | compact idiom peer |

<!-- END GENERATED sub-rel-python -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-python-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | sub | SQ | P-gen | x86_64 | thru | 42.39 | decimal.Decimal | 119.51 | **2.82×** | xRpysw2 | compact idiom peer |
| python | sub | NQ | P-gen | x86_64 | thru | 49.43 | decimal.Decimal | 139.91 | **2.83×** | xRpysw2 | compact idiom peer |
| python | sub | MQ | P-gen | x86_64 | thru | 58.41 | decimal.Decimal | 149.30 | **2.56×** | xRpysw2 | compact idiom peer |
| python | sub | OQ | P-gen | x86_64 | thru | 73.50 | decimal.Decimal | 165.69 | **2.25×** | xRpysw2 | compact idiom peer |
| python | sub | FQ | P-gen | x86_64 | thru | 65.02 | decimal.Decimal | 161.97 | **2.49×** | xRpysw2 | compact idiom peer |

<!-- END GENERATED sub-rel-python-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-python -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | mul | CP | P-gen | arm64 | thru | 18.85 | decimal.Decimal | 62.68 | **3.33×** | Rpysw2 | compact idiom peer |
| python | mul | WP | P-gen | arm64 | thru | 38.57 | decimal.Decimal | 73.75 | **1.91×** | Rpysw2 | compact idiom peer |
| python | mul | XP | P-gen | arm64 | thru | 45.41 | decimal.Decimal | 90.87 | **2.00×** | Rpysw2 | compact idiom peer |

<!-- END GENERATED mul-rel-python -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-python-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | mul | CP | P-gen | x86_64 | thru | 41.59 | decimal.Decimal | 113.92 | **2.74×** | xRpysw2 | compact idiom peer |
| python | mul | WP | P-gen | x86_64 | thru | 76.29 | decimal.Decimal | 138.06 | **1.81×** | xRpysw2 | compact idiom peer |
| python | mul | XP | P-gen | x86_64 | thru | 87.80 | decimal.Decimal | 157.91 | **1.80×** | xRpysw2 | compact idiom peer |

<!-- END GENERATED mul-rel-python-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-python -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | div | CD | P-gen | arm64 | thru | 55.74 | decimal.Decimal | 98.68 | **1.77×** | Rpysw2 | compact idiom peer |
| python | div | WD | P-gen | arm64 | thru | 64.11 | decimal.Decimal | 100.99 | **1.58×** | Rpysw2 | compact idiom peer |
| python | div | XD | P-gen | arm64 | thru | 62.72 | decimal.Decimal | 160.38 | **2.56×** | Rpysw2 | compact idiom peer |
| python | div | ET | P-gen | arm64 | thru | 24.81 | decimal.Decimal | 89.85 | **3.62×** | Rpysw2 | compact idiom peer |
| python | div | PT | P-gen | arm64 | thru | 18.36 | decimal.Decimal | 86.96 | **4.74×** | Rpysw2 | compact idiom peer |

<!-- END GENERATED div-rel-python -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-python-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | div | CD | P-gen | x86_64 | thru | 111.00 | decimal.Decimal | 210.73 | **1.90×** | xRpysw2 | compact idiom peer |
| python | div | WD | P-gen | x86_64 | thru | 119.78 | decimal.Decimal | 226.62 | **1.89×** | xRpysw2 | compact idiom peer |
| python | div | XD | P-gen | x86_64 | thru | 114.02 | decimal.Decimal | 336.27 | **2.95×** | xRpysw2 | compact idiom peer |
| python | div | ET | P-gen | x86_64 | thru | 63.62 | decimal.Decimal | 199.19 | **3.13×** | xRpysw2 | compact idiom peer |
| python | div | PT | P-gen | x86_64 | thru | 45.08 | decimal.Decimal | 182.31 | **4.04×** | xRpysw2 | compact idiom peer |

<!-- END GENERATED div-rel-python-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-python -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | fma | FN | FMA | arm64 | thru | 107.82 | decimal.Decimal | 142.31 | **1.32×** | Rpysw2 | compact idiom peer |
| python | fma | FF | FMA | arm64 | thru | 79.26 | decimal.Decimal | 165.21 | **2.08×** | Rpysw2 | compact idiom peer |

<!-- END GENERATED fma-rel-python -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-python-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| python | fma | FN | FMA | x86_64 | thru | 217.38 | decimal.Decimal | 276.78 | **1.27×** | xRpysw2 | compact idiom peer |
| python | fma | FF | FMA | x86_64 | thru | 177.87 | decimal.Decimal | 318.65 | **1.79×** | xRpysw2 | compact idiom peer |

<!-- END GENERATED fma-rel-python-x86 -->

</div>
