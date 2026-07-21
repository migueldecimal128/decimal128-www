---
layout: default
permalink: /benchmarks.html
title: "Benchmarks — Decimal128"
description: "Performance benchmarks comparing Decimal128 against the IBM libdecnumber, Intel libbid, and Python libmpdec reference libraries."
heading: "Benchmarks"
---

Miguel has benchmarked his solution across the supported languages, measured
against the IBM (decQuad), Intel (libbid), and Python (libmpdec) reference
libraries and each language's idiomatic decimal type. The detailed results are
published **per language** — pick a language below for its realistic
financial-mix (P-fin) headline followed by the per-operation band tables (add,
subtract, multiply, divide, FMA), d128 vs the alternatives available to it, with
explicit ratios.

Two cross-cutting views complement the per-language pages:

- **[Port-Comparison Benchmark Results](benchmark/port-compare.html)** — each
  port's own d128 band shape on identical operands (all ports, no alternatives).
- **[Benchmark Key](benchmark/key.html)** — the shared legend: category codes,
  magnitude profiles, timing modes, and method.

Methodology and the operation-category taxonomy are in the
[Benchmark Matrix](whitepapers/benchmark-matrix.html).

## Per-language results

<div class="kb-results">

<details class="kb-entry">
  <summary>C</summary>
  <div class="kb-entry-body" markdown="1">

[**C Benchmark Results →**](benchmark/vs-c.html) — FinMix headline, then add / subtract / multiply / divide / FMA band tables (arm64 + x86_64), with ratios.

**Summary — Ratio Range by Operation.** Min–max `ratio = alt / ours` (&gt; 1× ⇒ d128 faster), pooled across both architectures (arm64 + x86_64) and all three reference libraries (libbid, decQuad, mpdecimal), split by profile.

| Operation | P-fin range | P-gen range | FMA range |
|---|---|---|---|
| Add | 3.10× – 8.01× | 0.79× – 9.65× | — |
| Subtract | 4.21× – 11.42× | 0.83× – 18.72× | — |
| Multiply | 0.95× – 22.30× | 0.95× – 17.44× | — |
| Divide | 0.81× – 14.52× | 0.81× – 16.24× | — |
| FMA | — | — | 0.77× – 3.64× |

  </div>
</details>

<details class="kb-entry">
  <summary>C#</summary>
  <div class="kb-entry-body" markdown="1">

[**C# Benchmark Results →**](benchmark/vs-csharp.html) — FinMix headline, then add / subtract / multiply / divide / FMA band tables (arm64 + x86_64), with ratios.

**Summary — Ratio Range by Operation.** Min–max `ratio = alt / ours` (&gt; 1× ⇒ d128 faster), pooled across both architectures (arm64 + x86_64) and both reference/idiom peers (`System.Decimal`, `Decimal128` .NET 11), split by profile. FMA has no reference comparison in C#.

| Operation | P-fin range | P-gen range | FMA range |
|---|---|---|---|
| Add | 0.75× – 3.92× | 0.22× – 50.85× | — |
| Subtract | 0.86× – 5.21× | 0.23× – 50.25× | — |
| Multiply | 1.55× – 7.58× | 1.59× – 33.63× | — |
| Divide | 0.35× – 54.12× | 2.83× – 43.63× | — |
| FMA | — | — | — |

  </div>
</details>

<details class="kb-entry">
  <summary>Java</summary>
  <div class="kb-entry-body" markdown="1">

[**Java Benchmark Results →**](benchmark/vs-java.html) — FinMix headline, then add / subtract / multiply / divide / FMA band tables (arm64 + x86_64), with ratios.

**Summary — Ratio Range by Operation.** Min–max `ratio = alt / ours` (&gt; 1× ⇒ d128 faster), pooled across both architectures (arm64 + x86_64) and both reference/idiom peers (`BigDecimal`, libbid), split by profile.

| Operation | P-fin range | P-gen range | FMA range |
|---|---|---|---|
| Add | 3.17× – 3.36× | 1.36× – 5.96× | — |
| Subtract | 4.04× – 4.09× | 1.54× – 5.13× | — |
| Multiply | 2.08× – 3.37× | 1.97× – 3.59× | — |
| Divide | 1.77× – 60.05× | 2.14× – 43.88× | — |
| FMA | — | — | 0.63× – 0.79× |

  </div>
</details>

<details class="kb-entry">
  <summary>Kotlin KMP</summary>
  <div class="kb-entry-body" markdown="1">

[**Kotlin Benchmark Results →**](benchmark/vs-kotlin.html) — FinMix headline, then add / subtract / multiply / divide / FMA band tables (arm64 + x86_64), with ratios.

**Summary — Ratio Range by Operation.** Min–max `ratio = alt / ours` (&gt; 1× ⇒ d128 faster), pooled across both architectures (arm64 + x86_64) and both reference/idiom peers (`BigDecimal`, libbid), split by profile.

| Operation | P-fin range | P-gen range | FMA range |
|---|---|---|---|
| Add | 2.65× – 2.80× | 1.42× – 4.59× | — |
| Subtract | 3.76× – 3.79× | 1.58× – 4.75× | — |
| Multiply | 2.12× – 3.64× | 1.79× – 3.34× | — |
| Divide | 1.80× – 55.48× | 2.20× – 40.54× | — |
| FMA | — | — | 0.55× – 0.74× |

  </div>
</details>

<details class="kb-entry">
  <summary>Swift</summary>
  <div class="kb-entry-body" markdown="1">

[**Swift Benchmark Results →**](benchmark/vs-swift.html) — FinMix headline, then add / subtract / multiply / divide / FMA band tables (arm64 + x86_64), with ratios.

**Summary — Ratio Range by Operation.** Min–max `ratio = alt / ours` (&gt; 1× ⇒ d128 faster), pooled across both architectures (arm64 + x86_64) and both reference/idiom peers (`Foundation.Decimal`, libbid), split by profile.

| Operation | P-fin range | P-gen range | FMA range |
|---|---|---|---|
| Add | 69.34× – 81.08× | 21.16× – 83.08× | — |
| Subtract | 77.88× – 111.13× | 21.15× – 121.22× | — |
| Multiply | 13.39× – 176.86× | 14.02× – 102.80× | — |
| Divide | 14.41× – 643.91× | 15.43× – 551.06× | — |
| FMA | — | — | 0.96× – 1.45× |

  </div>
</details>

<details class="kb-entry">
  <summary>Rust</summary>
  <div class="kb-entry-body" markdown="1">

[**Rust Benchmark Results →**](benchmark/vs-rust.html) — FinMix headline, then add / subtract / multiply / divide / FMA band tables (arm64 + x86_64), with ratios.

**Summary — Ratio Range by Operation.** Min–max `ratio = alt / ours` (&gt; 1× ⇒ d128 faster), pooled across both architectures (arm64 + x86_64) and both reference/idiom peers (`rust_decimal`, libbid), split by profile.

| Operation | P-fin range | P-gen range | FMA range |
|---|---|---|---|
| Add | 1.21× – 1.55× | 0.41× – 1.88× | — |
| Subtract | 1.50× – 1.87× | 0.39× – 2.01× | — |
| Multiply | 2.02× – 21.15× | 1.77× – 15.54× | — |
| Divide | 0.53× – 5.30× | 0.97× – 3.14× | — |
| FMA | — | — | 1.78× – 3.58× |

  </div>
</details>

<details class="kb-entry">
  <summary>Go</summary>
  <div class="kb-entry-body" markdown="1">

[**Go Benchmark Results →**](benchmark/vs-go.html) — FinMix headline, then add / subtract / multiply / divide / FMA band tables (arm64 + x86_64), with ratios.

**Summary — Ratio Range by Operation.** Go has no in-language decimal peer and takes no libbid fallback, so every row is d128-only — there is no alternative to compute a ratio against.

| Operation | P-fin range | P-gen range | FMA range |
|---|---|---|---|
| Add | — | — | — |
| Subtract | — | — | — |
| Multiply | — | — | — |
| Divide | — | — | — |
| FMA | — | — | — |

  </div>
</details>

<details class="kb-entry">
  <summary>Python</summary>
  <div class="kb-entry-body" markdown="1">

[**Python Benchmark Results →**](benchmark/vs-python.html) — FinMix headline, then add / subtract / multiply / divide / FMA band tables (arm64 + x86_64), with ratios.

**Summary — Ratio Range by Operation.** Min–max `ratio = alt / ours` (&gt; 1× ⇒ d128 faster), pooled across both architectures (arm64 + x86_64) for Python's idiom peer (`decimal.Decimal`), split by profile.

| Operation | P-fin range | P-gen range | FMA range |
|---|---|---|---|
| Add | 2.58× – 2.65× | 2.16× – 3.21× | — |
| Subtract | 2.71× | 2.18× – 3.26× | — |
| Multiply | 1.74× – 3.77× | 1.85× – 3.32× | — |
| Divide | 1.52× – 4.56× | 1.54× – 4.95× | — |
| FMA | — | — | 1.27× – 2.02× |

  </div>
</details>

<details class="kb-entry">
  <summary>Zig</summary>
  <div class="kb-entry-body" markdown="1">

[**Zig Benchmark Results →**](benchmark/vs-zig.html) — FinMix headline, then add / subtract / multiply / divide / FMA band tables (arm64 + x86_64), with ratios.

**Summary — Ratio Range by Operation.** Min–max `ratio = alt / ours` (&gt; 1× ⇒ d128 faster), pooled across both architectures (arm64 + x86_64) for Zig's reference library (libbid — Zig has no in-language decimal peer), split by profile.

| Operation | P-fin range | P-gen range | FMA range |
|---|---|---|---|
| Add | 2.52× – 3.30× | 0.70× – 3.07× | — |
| Subtract | 3.43× – 4.29× | 0.70× – 5.88× | — |
| Multiply | 1.85× – 16.45× | 1.75× – 15.34× | — |
| Divide | 0.80× – 1.59× | 0.85× – 2.70× | — |
| FMA | — | — | 1.23× – 1.66× |

  </div>
</details>

</div>
