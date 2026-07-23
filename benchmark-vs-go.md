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
| go | add | MIX | P-fin | arm64 | thru | 5.38 | - | - | - | Rgosw2 |  |
| go | sub | MIX | P-fin | arm64 | thru | 3.99 | - | - | - | Rgosw2 |  |
| go | mul | CP | P-fin | arm64 | thru | 2.14 | - | - | - | Rgosw2 |  |
| go | mul | WP | P-fin | arm64 | thru | 27.96 | - | - | - | Rgosw2 |  |
| go | div | CD | P-fin | arm64 | thru | 47.24 | - | - | - | Rgosw2 |  |
| go | div | WD | P-fin | arm64 | thru | 64.37 | - | - | - | Rgosw2 |  |
| go | div | ET | P-fin | arm64 | thru | 11.44 | - | - | - | Rgosw2 |  |
| go | div | PT | P-fin | arm64 | thru | 6.64 | - | - | - | Rgosw2 |  |

<!-- END GENERATED pfin-rel-go -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-go-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| go | add | MIX | P-fin | x86_64 | thru | 13.04 | - | - | - | xRgosw2 |  |
| go | sub | MIX | P-fin | x86_64 | thru | 10.37 | - | - | - | xRgosw2 |  |
| go | mul | CP | P-fin | x86_64 | thru | 4.48 | - | - | - | xRgosw2 |  |
| go | mul | WP | P-fin | x86_64 | thru | 50.38 | - | - | - | xRgosw2 |  |
| go | div | CD | P-fin | x86_64 | thru | 107.30 | - | - | - | xRgosw2 |  |
| go | div | WD | P-fin | x86_64 | thru | 127.50 | - | - | - | xRgosw2 |  |
| go | div | ET | P-fin | x86_64 | thru | 29.75 | - | - | - | xRgosw2 |  |
| go | div | PT | P-fin | x86_64 | thru | 12.15 | - | - | - | xRgosw2 |  |

<!-- END GENERATED pfin-rel-go-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-go -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| go | add | SQ | P-gen | arm64 | thru | 4.60 | - | - | - | Rgosw2 |  |
| go | add | NQ | P-gen | arm64 | thru | 10.50 | - | - | - | Rgosw2 |  |
| go | add | MQ | P-gen | arm64 | thru | 14.86 | - | - | - | Rgosw2 |  |
| go | add | OQ | P-gen | arm64 | thru | 30.69 | - | - | - | Rgosw2 |  |
| go | add | FQ | P-gen | arm64 | thru | 19.04 | - | - | - | Rgosw2 |  |

<!-- END GENERATED add-rel-go -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-go-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| go | add | SQ | P-gen | x86_64 | thru | 10.26 | - | - | - | xRgosw2 |  |
| go | add | NQ | P-gen | x86_64 | thru | 16.18 | - | - | - | xRgosw2 |  |
| go | add | MQ | P-gen | x86_64 | thru | 29.47 | - | - | - | xRgosw2 |  |
| go | add | OQ | P-gen | x86_64 | thru | 61.41 | - | - | - | xRgosw2 |  |
| go | add | FQ | P-gen | x86_64 | thru | 37.57 | - | - | - | xRgosw2 |  |

<!-- END GENERATED add-rel-go-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-go -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| go | sub | SQ | P-gen | arm64 | thru | 2.73 | - | - | - | Rgosw2 |  |
| go | sub | NQ | P-gen | arm64 | thru | 10.06 | - | - | - | Rgosw2 |  |
| go | sub | MQ | P-gen | arm64 | thru | 14.98 | - | - | - | Rgosw2 |  |
| go | sub | OQ | P-gen | arm64 | thru | 31.19 | - | - | - | Rgosw2 |  |
| go | sub | FQ | P-gen | arm64 | thru | 19.53 | - | - | - | Rgosw2 |  |

<!-- END GENERATED sub-rel-go -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-go-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| go | sub | SQ | P-gen | x86_64 | thru | 7.21 | - | - | - | xRgosw2 |  |
| go | sub | NQ | P-gen | x86_64 | thru | 16.47 | - | - | - | xRgosw2 |  |
| go | sub | MQ | P-gen | x86_64 | thru | 29.40 | - | - | - | xRgosw2 |  |
| go | sub | OQ | P-gen | x86_64 | thru | 63.28 | - | - | - | xRgosw2 |  |
| go | sub | FQ | P-gen | x86_64 | thru | 37.58 | - | - | - | xRgosw2 |  |

<!-- END GENERATED sub-rel-go-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-go -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| go | mul | CP | P-gen | arm64 | thru | 2.60 | - | - | - | Rgosw2 |  |
| go | mul | WP | P-gen | arm64 | thru | 27.76 | - | - | - | Rgosw2 |  |
| go | mul | XP | P-gen | arm64 | thru | 38.68 | - | - | - | Rgosw2 |  |

<!-- END GENERATED mul-rel-go -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-go-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| go | mul | CP | P-gen | x86_64 | thru | 6.23 | - | - | - | xRgosw2 |  |
| go | mul | WP | P-gen | x86_64 | thru | 48.97 | - | - | - | xRgosw2 |  |
| go | mul | XP | P-gen | x86_64 | thru | 74.16 | - | - | - | xRgosw2 |  |

<!-- END GENERATED mul-rel-go-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-go -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| go | div | CD | P-gen | arm64 | thru | 43.58 | - | - | - | Rgosw2 |  |
| go | div | WD | P-gen | arm64 | thru | 63.62 | - | - | - | Rgosw2 |  |
| go | div | XD | P-gen | arm64 | thru | 51.51 | - | - | - | Rgosw2 |  |
| go | div | ET | P-gen | arm64 | thru | 14.36 | - | - | - | Rgosw2 |  |
| go | div | PT | P-gen | arm64 | thru | 6.63 | - | - | - | Rgosw2 |  |

<!-- END GENERATED div-rel-go -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-go-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| go | div | CD | P-gen | x86_64 | thru | 106.30 | - | - | - | xRgosw2 |  |
| go | div | WD | P-gen | x86_64 | thru | 126.10 | - | - | - | xRgosw2 |  |
| go | div | XD | P-gen | x86_64 | thru | 110.10 | - | - | - | xRgosw2 |  |
| go | div | ET | P-gen | x86_64 | thru | 35.17 | - | - | - | xRgosw2 |  |
| go | div | PT | P-gen | x86_64 | thru | 12.18 | - | - | - | xRgosw2 |  |

<!-- END GENERATED div-rel-go-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-go -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| go | fma | FN | FMA | arm64 | thru | 168.30 | - | - | - | Rgosw2 |  |
| go | fma | FF | FMA | arm64 | thru | 72.20 | - | - | - | Rgosw2 |  |

<!-- END GENERATED fma-rel-go -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-go-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| go | fma | FN | FMA | x86_64 | thru | 259.10 | - | - | - | xRgosw2 |  |
| go | fma | FF | FMA | x86_64 | thru | 131.50 | - | - | - | xRgosw2 |  |

<!-- END GENERATED fma-rel-go-x86 -->

</div>
