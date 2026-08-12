---
layout: default
permalink: /benchmark/vs-go.html
title: "Go Benchmark Results — Decimal128"
description: "decimal128 in Go, measured against the alternatives available to it — a realistic financial mix (P-fin) plus per-operation band characterization, with explicit ratios."
heading: "Go Benchmark Results"
---

<div class="whitepaper" markdown="1">

<p class="whitepaper-meta">Living document — as-measured results. Category codes, profiles, modes &amp; method: <a href="key.html">Benchmark Key</a>.</p>

This is the **Go** view of decimal128 **as-measured**, band by band, with explicit ratios. It opens with the realistic financial-mix (**P-fin**) headline, then the per-operation band characterization (**P-gen**) and FMA. In Go, d128 is measured against no alternative — Go has neither an in-language decimal peer nor a `libbid` fallback, so its rows are d128-only (`-` in the alt/ratio columns). It is **data only** — the categories, magnitude profiles, units, and methodology are defined in the [Benchmark Key](key.html) (and, authoritatively, `BenchmarkMatrix.md`). The cross-port d128 band-shape matrices (all ports, no alternatives) live in [Port-Comparison Benchmark Results](port-compare.html); the full index of per-language pages is on the [Benchmarks](/benchmarks.html) hub.

## Summary — Ratio Range by Operation

Go has no in-language decimal peer and takes no `libbid` fallback, so every row on this page is d128-only — there is no alternative to compute a ratio against.

## FinMix — realistic financial mix (P-fin)

The headline: one realistic 64-bit financial operation mix — a `MIX` add/sub stream, mul `CP`/`WP`, div `CD`/`WD`/`ET`/`PT` — `ratio = alt / ours` (&gt; 1 ⇒ d128 faster). This is the profile closest to real financial code.

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED pfin-rel-go -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| go | add | MIX | P-fin | arm64 | thru | 3.21 | - | - | - | Rgosw2 |  |
| go | sub | MIX | P-fin | arm64 | thru | 4.13 | - | - | - | Rgosw2 |  |
| go | mul | CP | P-fin | arm64 | thru | 1.98 | - | - | - | Rgosw2 |  |
| go | mul | WP | P-fin | arm64 | thru | 28.48 | - | - | - | Rgosw2 |  |
| go | div | CD | P-fin | arm64 | thru | 37.26 | - | - | - | Rgosw2 |  |
| go | div | WD | P-fin | arm64 | thru | 64.24 | - | - | - | Rgosw2 |  |
| go | div | ET | P-fin | arm64 | thru | 10.65 | - | - | - | Rgosw2 |  |
| go | div | PT | P-fin | arm64 | thru | 6.65 | - | - | - | Rgosw2 |  |

<!-- END GENERATED pfin-rel-go -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-go-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| go | add | MIX | P-fin | x86_64 | thru | 8.87 | - | - | - | xRgosw2 |  |
| go | sub | MIX | P-fin | x86_64 | thru | 11.99 | - | - | - | xRgosw2 |  |
| go | mul | CP | P-fin | x86_64 | thru | 4.42 | - | - | - | xRgosw2 |  |
| go | mul | WP | P-fin | x86_64 | thru | 59.93 | - | - | - | xRgosw2 |  |
| go | div | CD | P-fin | x86_64 | thru | 94.20 | - | - | - | xRgosw2 |  |
| go | div | WD | P-fin | x86_64 | thru | 151.90 | - | - | - | xRgosw2 |  |
| go | div | ET | P-fin | x86_64 | thru | 29.66 | - | - | - | xRgosw2 |  |
| go | div | PT | P-fin | x86_64 | thru | 13.16 | - | - | - | xRgosw2 |  |

<!-- END GENERATED pfin-rel-go-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-go -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| go | add | SQss | P-gen | arm64 | thru | 1.54 | - | - | - | Rgosw2 |  |
| go | add | SQos | P-gen | arm64 | thru | 5.03 | - | - | - | Rgosw2 |  |
| go | add | NQss | P-gen | arm64 | thru | 6.44 | - | - | - | Rgosw2 |  |
| go | add | NQos | P-gen | arm64 | thru | 11.20 | - | - | - | Rgosw2 |  |
| go | add | MQss | P-gen | arm64 | thru | 11.86 | - | - | - | Rgosw2 |  |
| go | add | MQos | P-gen | arm64 | thru | 19.53 | - | - | - | Rgosw2 |  |
| go | add | OQss | P-gen | arm64 | thru | 28.60 | - | - | - | Rgosw2 |  |
| go | add | OQos | P-gen | arm64 | thru | 37.34 | - | - | - | Rgosw2 |  |
| go | add | FQss | P-gen | arm64 | thru | 17.58 | - | - | - | Rgosw2 |  |
| go | add | FQos | P-gen | arm64 | thru | 24.02 | - | - | - | Rgosw2 |  |

<!-- END GENERATED add-rel-go -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-go-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| go | add | SQss | P-gen | x86_64 | thru | 3.47 | - | - | - | xRgosw2 |  |
| go | add | SQos | P-gen | x86_64 | thru | 9.82 | - | - | - | xRgosw2 |  |
| go | add | NQss | P-gen | x86_64 | thru | 12.51 | - | - | - | xRgosw2 |  |
| go | add | NQos | P-gen | x86_64 | thru | 17.40 | - | - | - | xRgosw2 |  |
| go | add | MQss | P-gen | x86_64 | thru | 20.81 | - | - | - | xRgosw2 |  |
| go | add | MQos | P-gen | x86_64 | thru | 34.95 | - | - | - | xRgosw2 |  |
| go | add | OQss | P-gen | x86_64 | thru | 51.43 | - | - | - | xRgosw2 |  |
| go | add | OQos | P-gen | x86_64 | thru | 78.79 | - | - | - | xRgosw2 |  |
| go | add | FQss | P-gen | x86_64 | thru | 32.77 | - | - | - | xRgosw2 |  |
| go | add | FQos | P-gen | x86_64 | thru | 40.59 | - | - | - | xRgosw2 |  |

<!-- END GENERATED add-rel-go-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-go -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| go | sub | SQss | P-gen | arm64 | thru | 2.92 | - | - | - | Rgosw2 |  |
| go | sub | SQos | P-gen | arm64 | thru | 1.62 | - | - | - | Rgosw2 |  |
| go | sub | NQss | P-gen | arm64 | thru | 10.68 | - | - | - | Rgosw2 |  |
| go | sub | NQos | P-gen | arm64 | thru | 5.59 | - | - | - | Rgosw2 |  |
| go | sub | MQss | P-gen | arm64 | thru | 18.11 | - | - | - | Rgosw2 |  |
| go | sub | MQos | P-gen | arm64 | thru | 11.53 | - | - | - | Rgosw2 |  |
| go | sub | OQss | P-gen | arm64 | thru | 36.44 | - | - | - | Rgosw2 |  |
| go | sub | OQos | P-gen | arm64 | thru | 27.58 | - | - | - | Rgosw2 |  |
| go | sub | FQss | P-gen | arm64 | thru | 22.72 | - | - | - | Rgosw2 |  |
| go | sub | FQos | P-gen | arm64 | thru | 16.72 | - | - | - | Rgosw2 |  |

<!-- END GENERATED sub-rel-go -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-go-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| go | sub | SQss | P-gen | x86_64 | thru | 8.78 | - | - | - | xRgosw2 |  |
| go | sub | SQos | P-gen | x86_64 | thru | 3.88 | - | - | - | xRgosw2 |  |
| go | sub | NQss | P-gen | x86_64 | thru | 17.03 | - | - | - | xRgosw2 |  |
| go | sub | NQos | P-gen | x86_64 | thru | 12.17 | - | - | - | xRgosw2 |  |
| go | sub | MQss | P-gen | x86_64 | thru | 34.93 | - | - | - | xRgosw2 |  |
| go | sub | MQos | P-gen | x86_64 | thru | 20.41 | - | - | - | xRgosw2 |  |
| go | sub | OQss | P-gen | x86_64 | thru | 69.12 | - | - | - | xRgosw2 |  |
| go | sub | OQos | P-gen | x86_64 | thru | 50.94 | - | - | - | xRgosw2 |  |
| go | sub | FQss | P-gen | x86_64 | thru | 45.88 | - | - | - | xRgosw2 |  |
| go | sub | FQos | P-gen | x86_64 | thru | 37.08 | - | - | - | xRgosw2 |  |

<!-- END GENERATED sub-rel-go-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-go -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| go | mul | CP | P-gen | arm64 | thru | 2.46 | - | - | - | Rgosw2 |  |
| go | mul | WP | P-gen | arm64 | thru | 28.35 | - | - | - | Rgosw2 |  |
| go | mul | XP | P-gen | arm64 | thru | 39.72 | - | - | - | Rgosw2 |  |

<!-- END GENERATED mul-rel-go -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-go-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| go | mul | CP | P-gen | x86_64 | thru | 6.43 | - | - | - | xRgosw2 |  |
| go | mul | WP | P-gen | x86_64 | thru | 52.28 | - | - | - | xRgosw2 |  |
| go | mul | XP | P-gen | x86_64 | thru | 78.60 | - | - | - | xRgosw2 |  |

<!-- END GENERATED mul-rel-go-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-go -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| go | div | CD | P-gen | arm64 | thru | 35.09 | - | - | - | Rgosw2 |  |
| go | div | WD | P-gen | arm64 | thru | 61.48 | - | - | - | Rgosw2 |  |
| go | div | XD | P-gen | arm64 | thru | 58.03 | - | - | - | Rgosw2 |  |
| go | div | ET | P-gen | arm64 | thru | 12.35 | - | - | - | Rgosw2 |  |
| go | div | PT | P-gen | arm64 | thru | 6.64 | - | - | - | Rgosw2 |  |

<!-- END GENERATED div-rel-go -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-go-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| go | div | CD | P-gen | x86_64 | thru | 92.98 | - | - | - | xRgosw2 |  |
| go | div | WD | P-gen | x86_64 | thru | 157.10 | - | - | - | xRgosw2 |  |
| go | div | XD | P-gen | x86_64 | thru | 117.50 | - | - | - | xRgosw2 |  |
| go | div | ET | P-gen | x86_64 | thru | 35.98 | - | - | - | xRgosw2 |  |
| go | div | PT | P-gen | x86_64 | thru | 15.15 | - | - | - | xRgosw2 |  |

<!-- END GENERATED div-rel-go-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-go -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| go | fma | FN | FMA | arm64 | thru | 159.20 | - | - | - | Rgosw2 |  |
| go | fma | FF | FMA | arm64 | thru | 72.84 | - | - | - | Rgosw2 |  |

<!-- END GENERATED fma-rel-go -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-go-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| go | fma | FN | FMA | x86_64 | thru | 313.30 | - | - | - | xRgosw2 |  |
| go | fma | FF | FMA | x86_64 | thru | 165.00 | - | - | - | xRgosw2 |  |

<!-- END GENERATED fma-rel-go-x86 -->

</div>
