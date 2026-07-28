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
| go | sub | MIX | P-fin | arm64 | thru | 4.14 | - | - | - | Rgosw2 |  |
| go | mul | CP | P-fin | arm64 | thru | 1.97 | - | - | - | Rgosw2 |  |
| go | mul | WP | P-fin | arm64 | thru | 28.26 | - | - | - | Rgosw2 |  |
| go | div | CD | P-fin | arm64 | thru | 37.92 | - | - | - | Rgosw2 |  |
| go | div | WD | P-fin | arm64 | thru | 64.46 | - | - | - | Rgosw2 |  |
| go | div | ET | P-fin | arm64 | thru | 10.49 | - | - | - | Rgosw2 |  |
| go | div | PT | P-fin | arm64 | thru | 6.65 | - | - | - | Rgosw2 |  |

<!-- END GENERATED pfin-rel-go -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-go-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| go | add | MIX | P-fin | x86_64 | thru | 7.47 | - | - | - | xRgosw2 |  |
| go | sub | MIX | P-fin | x86_64 | thru | 10.67 | - | - | - | xRgosw2 |  |
| go | mul | CP | P-fin | x86_64 | thru | 3.89 | - | - | - | xRgosw2 |  |
| go | mul | WP | P-fin | x86_64 | thru | 46.99 | - | - | - | xRgosw2 |  |
| go | div | CD | P-fin | x86_64 | thru | 81.83 | - | - | - | xRgosw2 |  |
| go | div | WD | P-fin | x86_64 | thru | 130.80 | - | - | - | xRgosw2 |  |
| go | div | ET | P-fin | x86_64 | thru | 27.39 | - | - | - | xRgosw2 |  |
| go | div | PT | P-fin | x86_64 | thru | 12.04 | - | - | - | xRgosw2 |  |

<!-- END GENERATED pfin-rel-go-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-go -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| go | add | SQ | P-gen | arm64 | thru | 3.17 | - | - | - | Rgosw2 |  |
| go | add | NQ | P-gen | arm64 | thru | 11.28 | - | - | - | Rgosw2 |  |
| go | add | MQ | P-gen | arm64 | thru | 16.04 | - | - | - | Rgosw2 |  |
| go | add | OQ | P-gen | arm64 | thru | 32.24 | - | - | - | Rgosw2 |  |
| go | add | FQ | P-gen | arm64 | thru | 20.50 | - | - | - | Rgosw2 |  |

<!-- END GENERATED add-rel-go -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-go-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| go | add | SQ | P-gen | x86_64 | thru | 8.13 | - | - | - | xRgosw2 |  |
| go | add | NQ | P-gen | x86_64 | thru | 16.58 | - | - | - | xRgosw2 |  |
| go | add | MQ | P-gen | x86_64 | thru | 29.77 | - | - | - | xRgosw2 |  |
| go | add | OQ | P-gen | x86_64 | thru | 59.21 | - | - | - | xRgosw2 |  |
| go | add | FQ | P-gen | x86_64 | thru | 36.86 | - | - | - | xRgosw2 |  |

<!-- END GENERATED add-rel-go-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-go -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| go | sub | SQ | P-gen | arm64 | thru | 2.77 | - | - | - | Rgosw2 |  |
| go | sub | NQ | P-gen | arm64 | thru | 10.21 | - | - | - | Rgosw2 |  |
| go | sub | MQ | P-gen | arm64 | thru | 14.89 | - | - | - | Rgosw2 |  |
| go | sub | OQ | P-gen | arm64 | thru | 31.00 | - | - | - | Rgosw2 |  |
| go | sub | FQ | P-gen | arm64 | thru | 19.80 | - | - | - | Rgosw2 |  |

<!-- END GENERATED sub-rel-go -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-go-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| go | sub | SQ | P-gen | x86_64 | thru | 7.24 | - | - | - | xRgosw2 |  |
| go | sub | NQ | P-gen | x86_64 | thru | 16.31 | - | - | - | xRgosw2 |  |
| go | sub | MQ | P-gen | x86_64 | thru | 29.17 | - | - | - | xRgosw2 |  |
| go | sub | OQ | P-gen | x86_64 | thru | 59.54 | - | - | - | xRgosw2 |  |
| go | sub | FQ | P-gen | x86_64 | thru | 36.90 | - | - | - | xRgosw2 |  |

<!-- END GENERATED sub-rel-go-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-go -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| go | mul | CP | P-gen | arm64 | thru | 2.39 | - | - | - | Rgosw2 |  |
| go | mul | WP | P-gen | arm64 | thru | 28.44 | - | - | - | Rgosw2 |  |
| go | mul | XP | P-gen | arm64 | thru | 39.45 | - | - | - | Rgosw2 |  |

<!-- END GENERATED mul-rel-go -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-go-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| go | mul | CP | P-gen | x86_64 | thru | 5.78 | - | - | - | xRgosw2 |  |
| go | mul | WP | P-gen | x86_64 | thru | 46.86 | - | - | - | xRgosw2 |  |
| go | mul | XP | P-gen | x86_64 | thru | 70.32 | - | - | - | xRgosw2 |  |

<!-- END GENERATED mul-rel-go-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-go -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| go | div | CD | P-gen | arm64 | thru | 34.72 | - | - | - | Rgosw2 |  |
| go | div | WD | P-gen | arm64 | thru | 62.56 | - | - | - | Rgosw2 |  |
| go | div | XD | P-gen | arm64 | thru | 52.86 | - | - | - | Rgosw2 |  |
| go | div | ET | P-gen | arm64 | thru | 12.26 | - | - | - | Rgosw2 |  |
| go | div | PT | P-gen | arm64 | thru | 6.64 | - | - | - | Rgosw2 |  |

<!-- END GENERATED div-rel-go -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-go-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| go | div | CD | P-gen | x86_64 | thru | 87.07 | - | - | - | xRgosw2 |  |
| go | div | WD | P-gen | x86_64 | thru | 123.10 | - | - | - | xRgosw2 |  |
| go | div | XD | P-gen | x86_64 | thru | 109.50 | - | - | - | xRgosw2 |  |
| go | div | ET | P-gen | x86_64 | thru | 32.53 | - | - | - | xRgosw2 |  |
| go | div | PT | P-gen | x86_64 | thru | 12.10 | - | - | - | xRgosw2 |  |

<!-- END GENERATED div-rel-go-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-go -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| go | fma | FN | FMA | arm64 | thru | 167.90 | - | - | - | Rgosw2 |  |
| go | fma | FF | FMA | arm64 | thru | 70.25 | - | - | - | Rgosw2 |  |

<!-- END GENERATED fma-rel-go -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-go-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| go | fma | FN | FMA | x86_64 | thru | 256.10 | - | - | - | xRgosw2 |  |
| go | fma | FF | FMA | x86_64 | thru | 130.40 | - | - | - | xRgosw2 |  |

<!-- END GENERATED fma-rel-go-x86 -->

</div>
