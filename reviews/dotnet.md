---
layout: default
permalink: /reviews/dotnet.html
title: ".NET — System.Numerics.Decimal128 Reviews — Decimal128"
description: "An independent, standards-anchored review series tracking Microsoft's System.Numerics.Decimal128 across the .NET 11 previews and release candidates through GA, and onward."
heading: ".NET — System.Numerics.Decimal128"
---

A pre-release review series tracking **`System.Numerics.Decimal128`**, the
128-bit decimal floating-point type Microsoft plans to introduce in .NET 11,
targeted Nov 2026. One installment is published for each preview and release
candidate through GA. 
Each edition run through the same standards-anchored harness so the 
type can be watched as it converges.

## The reviews

### .NET 11

| Date | Release | Review | Headline |
|------|---------|--------|----------|
| 2026-07-30 | RC 1, build 26380.103 | [Read →](dotnet/net11-rc1-26380.103.html) | totalOrder arrives and is conformant (2,702 vectors green); quantum-preserving ToString merged upstream; performance flat at the branch cut — the pre-GA profile is now visible. |
| 2026-07-28 | preview 7, build 26376.106 | [Read →](dotnet/net11-preview7-26376.106.html) | FMA arrives (truly fused); full IEEE 754 recommended-function surface; division up to 4× faster; new ln/log10 near-1 accuracy findings; RootN correct where the reference ports were not. |
| 2026-07-14 | preview 7, build 26366.102 | [Read →](dotnet/net11-preview7.html) | Numerically correct; no status flags; rounding is composed rather than fused (double-rounding); ToString needs work; missing TotalOrder; missing FMA; naive division. |

*Release candidate and GA editions will be added under this heading as they are
published.*
