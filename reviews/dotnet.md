---
layout: default
permalink: /reviews/dotnet.html
title: ".NET — System.Numerics.Decimal128 Reviews — Decimal128"
description: "An independent, standards-anchored review series tracking Microsoft's System.Numerics.Decimal128 across the .NET 11 previews and release candidates through GA, and onward."
heading: ".NET — System.Numerics.Decimal128"
---

A per-release review series tracking **`System.Numerics.Decimal128`**, the
128-bit decimal floating-point type Microsoft is introducing in .NET. One
installment is published for each preview and release candidate through GA, and
the series continues into subsequent .NET versions — each edition run through the
same standards-anchored harness so the type can be watched as it converges.

New here? The full method and motivation live on the
[Reviews home](../reviews.html): an independent decimal128 specialist, unaffiliated
with the .NET team, measuring against IEEE 754-2019 and GDAS with a conformant
reference implementation (`d128`) and a Rosetta suite over `decTest` / `fptest` /
`libbid`. Every edition below also restates that framing so it stands alone.

## Scorecard

Headline conformance measures, tracked edition to edition.

| Measure | Preview 7 |
|---------|-----------|
| Numerical results (value) correct vs. `decTest` / `fptest` / `libbid` | ✅ verified |
| Correctly-rounded operations (of 5 IEEE rounding-direction attributes) | **1 / 5** (`roundTiesToEven` only) |
| Status flags | ❌ none |
| `CompareTo` implements §5.10 `totalOrder` | ❌ (in progress toward RC1) |

*Columns are added as each release is reviewed, so the trend is visible at a glance.*

## The reviews

### .NET 11

| Date | Release | Review | Headline |
|------|---------|--------|----------|
| 2026-07-14 | preview 7 | [Read →](dotnet/net11-preview7.html) *(draft — in progress)* | Numerically correct; rounding is composed rather than fused (double-rounding); no status flags; naive division. |

*Release candidate and GA editions will be added under this heading as they are
published; later .NET versions get their own heading above this one.*
