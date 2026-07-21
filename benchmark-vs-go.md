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

Go has no in-language decimal peer and takes no `libbid` fallback, so every row on this page is d128-only — there is no alternative to compute a ratio against. The rollup below is included for consistency with the other language pages, but every cell is blank.

| Operation | P-fin range | P-gen range |
|---|---|---|
| Add | — | — |
| Subtract | — | — |
| Multiply | — | — |
| Divide | — | — |

## FinMix — realistic financial mix (P-fin)

The headline: one realistic 64-bit financial operation mix — a `MIX` add/sub stream, mul `CP`/`WP`, div `CD`/`WD`/`ET`/`PT` — `ratio = alt / ours` (&gt; 1 ⇒ d128 faster). This is the profile closest to real financial code.

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED pfin-rel-go -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| go | add | MIX | P-fin | arm64 | thru | 8.51 | - | - | - | Rgosw2 |  |
| go | sub | MIX | P-fin | arm64 | thru | 4.17 | - | - | - | Rgosw2 |  |
| go | mul | CP | P-fin | arm64 | thru | 2.14 | - | - | - | Rgosw2 |  |
| go | mul | WP | P-fin | arm64 | thru | 28.31 | - | - | - | Rgosw2 |  |
| go | div | CD | P-fin | arm64 | thru | 47.17 | - | - | - | Rgosw2 |  |
| go | div | WD | P-fin | arm64 | thru | 62.17 | - | - | - | Rgosw2 |  |
| go | div | ET | P-fin | arm64 | thru | 11.68 | - | - | - | Rgosw2 |  |
| go | div | PT | P-fin | arm64 | thru | 6.52 | - | - | - | Rgosw2 |  |

<!-- END GENERATED pfin-rel-go -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED pfin-rel-go-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| go | add | MIX | P-fin | x86_64 | thru | 15.14 | - | - | - | xRgosw2 |  |
| go | sub | MIX | P-fin | x86_64 | thru | 12.65 | - | - | - | xRgosw2 |  |
| go | mul | CP | P-fin | x86_64 | thru | 5.14 | - | - | - | xRgosw2 |  |
| go | mul | WP | P-fin | x86_64 | thru | 54.03 | - | - | - | xRgosw2 |  |
| go | div | CD | P-fin | x86_64 | thru | 114.60 | - | - | - | xRgosw2 |  |
| go | div | WD | P-fin | x86_64 | thru | 130.60 | - | - | - | xRgosw2 |  |
| go | div | ET | P-fin | x86_64 | thru | 31.17 | - | - | - | xRgosw2 |  |
| go | div | PT | P-fin | x86_64 | thru | 13.38 | - | - | - | xRgosw2 |  |

<!-- END GENERATED pfin-rel-go-x86 -->

## Add — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED add-rel-go -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| go | add | SQ | P-gen | arm64 | thru | 5.07 | - | - | - | Rgosw2 |  |
| go | add | NQ | P-gen | arm64 | thru | 10.38 | - | - | - | Rgosw2 |  |
| go | add | MQ | P-gen | arm64 | thru | 21.83 | - | - | - | Rgosw2 |  |
| go | add | OQ | P-gen | arm64 | thru | 32.50 | - | - | - | Rgosw2 |  |
| go | add | FQ | P-gen | arm64 | thru | 19.99 | - | - | - | Rgosw2 |  |

<!-- END GENERATED add-rel-go -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED add-rel-go-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| go | add | SQ | P-gen | x86_64 | thru | 12.31 | - | - | - | xRgosw2 |  |
| go | add | NQ | P-gen | x86_64 | thru | 17.70 | - | - | - | xRgosw2 |  |
| go | add | MQ | P-gen | x86_64 | thru | 42.80 | - | - | - | xRgosw2 |  |
| go | add | OQ | P-gen | x86_64 | thru | 66.05 | - | - | - | xRgosw2 |  |
| go | add | FQ | P-gen | x86_64 | thru | 40.02 | - | - | - | xRgosw2 |  |

<!-- END GENERATED add-rel-go-x86 -->

## Subtract — SQ · NQ · MQ · OQ · FQ

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED sub-rel-go -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| go | sub | SQ | P-gen | arm64 | thru | 2.69 | - | - | - | Rgosw2 |  |
| go | sub | NQ | P-gen | arm64 | thru | 10.09 | - | - | - | Rgosw2 |  |
| go | sub | MQ | P-gen | arm64 | thru | 22.03 | - | - | - | Rgosw2 |  |
| go | sub | OQ | P-gen | arm64 | thru | 32.21 | - | - | - | Rgosw2 |  |
| go | sub | FQ | P-gen | arm64 | thru | 19.60 | - | - | - | Rgosw2 |  |

<!-- END GENERATED sub-rel-go -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED sub-rel-go-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| go | sub | SQ | P-gen | x86_64 | thru | 9.46 | - | - | - | xRgosw2 |  |
| go | sub | NQ | P-gen | x86_64 | thru | 18.14 | - | - | - | xRgosw2 |  |
| go | sub | MQ | P-gen | x86_64 | thru | 43.77 | - | - | - | xRgosw2 |  |
| go | sub | OQ | P-gen | x86_64 | thru | 65.49 | - | - | - | xRgosw2 |  |
| go | sub | FQ | P-gen | x86_64 | thru | 41.29 | - | - | - | xRgosw2 |  |

<!-- END GENERATED sub-rel-go-x86 -->

## Multiply — CP · WP · XP

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED mul-rel-go -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| go | mul | CP | P-gen | arm64 | thru | 2.50 | - | - | - | Rgosw2 |  |
| go | mul | WP | P-gen | arm64 | thru | 27.04 | - | - | - | Rgosw2 |  |
| go | mul | XP | P-gen | arm64 | thru | 37.51 | - | - | - | Rgosw2 |  |

<!-- END GENERATED mul-rel-go -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED mul-rel-go-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| go | mul | CP | P-gen | x86_64 | thru | 7.44 | - | - | - | xRgosw2 |  |
| go | mul | WP | P-gen | x86_64 | thru | 54.27 | - | - | - | xRgosw2 |  |
| go | mul | XP | P-gen | x86_64 | thru | 75.89 | - | - | - | xRgosw2 |  |

<!-- END GENERATED mul-rel-go-x86 -->

## Divide — CD · WD · XD (+ ET · PT)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED div-rel-go -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| go | div | CD | P-gen | arm64 | thru | 46.91 | - | - | - | Rgosw2 |  |
| go | div | WD | P-gen | arm64 | thru | 59.31 | - | - | - | Rgosw2 |  |
| go | div | XD | P-gen | arm64 | thru | 60.13 | - | - | - | Rgosw2 |  |
| go | div | ET | P-gen | arm64 | thru | 14.92 | - | - | - | Rgosw2 |  |
| go | div | PT | P-gen | arm64 | thru | 6.56 | - | - | - | Rgosw2 |  |

<!-- END GENERATED div-rel-go -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED div-rel-go-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| go | div | CD | P-gen | x86_64 | thru | 108.90 | - | - | - | xRgosw2 |  |
| go | div | WD | P-gen | x86_64 | thru | 133.40 | - | - | - | xRgosw2 |  |
| go | div | XD | P-gen | x86_64 | thru | 116.20 | - | - | - | xRgosw2 |  |
| go | div | ET | P-gen | x86_64 | thru | 37.99 | - | - | - | xRgosw2 |  |
| go | div | PT | P-gen | x86_64 | thru | 13.33 | - | - | - | xRgosw2 |  |

<!-- END GENERATED div-rel-go-x86 -->

## FMA — FN (Barrett) · FF (fits-128)

Swept 4096-input average per band (bare `thru`; ns/op = Time/4096 over the shared `decimal128-resources/swept/` corpus, byte-identical operands every port). Relational peer table with explicit ratios; the cross-port d128 band-shape matrices are in [Port-Comparison Benchmark Results](port-compare.html).

**arm64 (M3 Pro).**

<!-- BEGIN GENERATED fma-rel-go -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| go | fma | FN | FMA | arm64 | thru | 157.70 | - | - | - | Rgosw2 |  |
| go | fma | FF | FMA | arm64 | thru | 76.56 | - | - | - | Rgosw2 |  |

<!-- END GENERATED fma-rel-go -->

**x86_64 (Intel i9-9880H).**

<!-- BEGIN GENERATED fma-rel-go-x86 -->

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| go | fma | FN | FMA | x86_64 | thru | 264.80 | - | - | - | xRgosw2 |  |
| go | fma | FF | FMA | x86_64 | thru | 147.40 | - | - | - | xRgosw2 |  |

<!-- END GENERATED fma-rel-go-x86 -->

</div>
