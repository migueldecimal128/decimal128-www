---
layout: default
permalink: /publications.html
title: "Publications — Decimal128"
description: "Miguel's whitepapers on the decimal128 architecture, and his independent, standards-anchored reviews of decimal implementations across languages and platforms."
heading: "Publications"
redirect_from:
  - /whitepapers.html
  - /reviews.html
---

<nav class="pub-jumpnav" markdown="0">
  <a href="#pub-whitepapers">Whitepapers</a>
  <a href="#pub-reviews">Independent Reviews</a>
</nav>

<div class="pub-section pub-section--whitepapers" id="pub-whitepapers" markdown="1">
<div class="pub-heading-row" markdown="0">
  <h2>Whitepapers</h2>
  <span class="pub-eyebrow">Miguel's Own Work</span>
</div>

These whitepapers are written by Miguel and cover the technical foundation of decimal128 — its encoding format, its conformance to the IEEE 754 and GDAS standards, and its performance against other implementations. Each whitepaper is a standalone piece.

- [UBD (An Unpacked Binary Decimal Format for Fast Software Decoding of IEEE 754 decimal128)](whitepapers/ubd.html)
- [Three Scripts, One Truth (Conformance Evidence)](whitepapers/conformance-evidence.html)
- [Benchmark Matrix](whitepapers/benchmark-matrix.html)

</div>

<div class="pub-section pub-section--reviews" id="pub-reviews" markdown="1">
<div class="pub-heading-row" markdown="0">
  <h2>Independent Reviews</h2>
  <span class="pub-eyebrow">Independent Analysis</span>
</div>

Independent, standards-anchored reviews of decimal floating-point
implementations — the decimal types shipping in mainstream languages and
platforms — measured against the published standards and against a conformant
reference implementation.

Each review is published **per release** of the thing under review, and each one
stands on its own: you can read any single edition end to end without the others.

### Who is doing this, and why?

Miguel is an independent decimal128 specialist, and is **not affiliated with
any of the teams whose work is reviewed here.** He maintains his own conformant
decimal128 implementation (`d128`) across several languages, together with a
cross-checking ("Rosetta") suite that verifies results bit-for-bit against the
recognized decimal test corpora: the Cowlishaw/IBM `decTest` vectors, the IBM
FPgen `fptest` suite, and the Intel `libbid` reference. That implementation and
that suite are the lens for everything in these reviews.

The bar is the published standards, named explicitly and never left vague:
**IEEE 754-2019** (the decimal formats and their arithmetic) and the **General
Decimal Arithmetic Specification (GDAS)** by Mike Cowlishaw. Where a review says
an operation is right or wrong, it means against those documents, with a clause
reference where it matters.

Why do this, and why per release? Because the cheapest time to influence a
numeric type is before its behavior calcifies into something real code depends
on — and the fairest way to hold one to account is to re-measure it every
release, giving credit for what improves and flagging what regresses, always
against the standard rather than against opinion.

### How to read these reviews

- **Correctness is graded against the standards.** A conformance gap is stated as
  a gap, with the clause it violates.
- **Performance is reported, not graded.** Speed improves release over release
  without breaking anyone, so benchmark numbers are evidence and a baseline for
  the next edition — not a verdict.
- **Real defects are separated from permitted or deliberate choices.** IEEE 754
  leaves genuine latitude in places; where an implementer exercises it, that is
  said plainly and not counted against them.
- **Each edition carries a status vocabulary** — *resolved / still open / newly
  introduced* — so progress across releases is legible at a glance.
- **Each series keeps a running scorecard** of its headline conformance measures,
  so the trend line is visible edition to edition.

### The series

| Target | Under review | Series |
|--------|--------------|--------|
| **.NET** | `System.Numerics.Decimal128` | [.NET reviews →](reviews/dotnet.html) |

*Additional languages and platforms will be added here as their decimal
implementations are reviewed.*

</div>
