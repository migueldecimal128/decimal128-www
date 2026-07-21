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

**Summary — Ratio Range by Operation.** Min–max `ratio = alt / ours` (&gt; 1× ⇒ d128 faster) on x86_64 (Intel i9-9880H), across all three reference libraries (libbid, decQuad, mpdecimal), split by profile.

| Operation | P-fin range | P-gen range | FMA range |
|---|---|---|---|
| Add | 3.10× – 5.94× | 0.89× – 5.89× | — |
| Subtract | 4.21× – 7.21× | 1.04× – 10.59× | — |
| Multiply | 0.95× – 22.30× | 1.41× – 13.50× | — |
| Divide | 0.81× – 8.62× | 0.81× – 10.49× | — |
| FMA | — | — | 0.98× – 3.64× |

  </div>
</details>

<details class="kb-entry">
  <summary>C#</summary>
  <div class="kb-entry-body" markdown="1">

[**C# Benchmark Results →**](benchmark/vs-csharp.html) — FinMix headline, then add / subtract / multiply / divide / FMA band tables (arm64 + x86_64), with ratios.

**Summary — Ratio Range by Operation.** Min–max `ratio = alt / ours` (&gt; 1× ⇒ d128 faster) on x86_64 (Intel i9-9880H), across both reference/idiom peers (`System.Decimal`, `Decimal128` .NET 11), split by profile. FMA has no reference comparison in C#.

| Operation | P-fin range | P-gen range | FMA range |
|---|---|---|---|
| Add | 0.79× – 2.54× | 0.35× – 50.85× | — |
| Subtract | 0.86× – 2.93× | 0.31× – 50.25× | — |
| Multiply | 2.21× – 7.58× | 2.05× – 33.63× | — |
| Divide | 0.53× – 54.12× | 3.35× – 43.63× | — |
| FMA | — | — | — |

  </div>
</details>

<details class="kb-entry">
  <summary>Java</summary>
  <div class="kb-entry-body" markdown="1">

[**Java Benchmark Results →**](benchmark/vs-java.html) — FinMix headline, then add / subtract / multiply / divide / FMA band tables (arm64 + x86_64), with ratios.

**Summary — Ratio Range by Operation.** Min–max `ratio = alt / ours` (&gt; 1× ⇒ d128 faster) on x86_64 (Intel i9-9880H), across both reference/idiom peers (`BigDecimal`, libbid), split by profile.

| Operation | P-fin range | P-gen range | FMA range |
|---|---|---|---|
| Add | 3.36× | 2.29× – 5.96× | — |
| Subtract | 4.09× | 2.33× – 4.92× | — |
| Multiply | 3.06× – 3.37× | 2.74× – 3.59× | — |
| Divide | 1.77× – 60.05× | 2.14× – 43.88× | — |
| FMA | — | — | 0.63× – 0.73× |

  </div>
</details>

<details class="kb-entry">
  <summary>Kotlin KMP</summary>
  <div class="kb-entry-body" markdown="1">

[**Kotlin Benchmark Results →**](benchmark/vs-kotlin.html) — FinMix headline, then add / subtract / multiply / divide / FMA band tables (arm64 + x86_64), with ratios.

**Summary — Ratio Range by Operation.** Min–max `ratio = alt / ours` (&gt; 1× ⇒ d128 faster) on x86_64 (Intel i9-9880H), across both reference/idiom peers (`BigDecimal`, libbid), split by profile.

| Operation | P-fin range | P-gen range | FMA range |
|---|---|---|---|
| Add | 2.65× | 2.01× – 4.59× | — |
| Subtract | 3.76× | 2.28× – 4.69× | — |
| Multiply | 3.25× – 3.64× | 2.90× – 3.34× | — |
| Divide | 1.80× – 55.48× | 2.20× – 40.54× | — |
| FMA | — | — | 0.55× – 0.62× |

  </div>
</details>

<details class="kb-entry">
  <summary>Swift</summary>
  <div class="kb-entry-body" markdown="1">

[**Swift Benchmark Results →**](benchmark/vs-swift.html) — FinMix headline, then add / subtract / multiply / divide / FMA band tables (arm64 + x86_64), with ratios.

**Summary — Ratio Range by Operation.** Min–max `ratio = alt / ours` (&gt; 1× ⇒ d128 faster) on x86_64 (Intel i9-9880H), across both reference/idiom peers (`Foundation.Decimal`, libbid), split by profile.

| Operation | P-fin range | P-gen range | FMA range |
|---|---|---|---|
| Add | 69.34× | 21.58× – 83.08× | — |
| Subtract | 77.88× | 21.46× – 100.42× | — |
| Multiply | 21.24× – 176.86× | 21.98× – 102.80× | — |
| Divide | 16.56× – 643.91× | 16.21× – 551.06× | — |
| FMA | — | — | 1.07× – 1.45× |

  </div>
</details>

<details class="kb-entry">
  <summary>Rust</summary>
  <div class="kb-entry-body" markdown="1">

[**Rust Benchmark Results →**](benchmark/vs-rust.html) — FinMix headline, then add / subtract / multiply / divide / FMA band tables (arm64 + x86_64), with ratios.

**Summary — Ratio Range by Operation.** Min–max `ratio = alt / ours` (&gt; 1× ⇒ d128 faster) on x86_64 (Intel i9-9880H), across both reference/idiom peers (`rust_decimal`, libbid), split by profile.

| Operation | P-fin range | P-gen range | FMA range |
|---|---|---|---|
| Add | 1.55× | 0.81× – 1.88× | — |
| Subtract | 1.87× | 0.74× – 1.87× | — |
| Multiply | 2.02× – 14.97× | 2.15× – 9.04× | — |
| Divide | 0.61× – 5.30× | 0.97× – 3.14× | — |
| FMA | — | — | 1.83× – 2.57× |

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

**Summary — Ratio Range by Operation.** Min–max `ratio = alt / ours` (&gt; 1× ⇒ d128 faster) on x86_64 (Intel i9-9880H) for Python's idiom peer (`decimal.Decimal`), split by profile.

| Operation | P-fin range | P-gen range | FMA range |
|---|---|---|---|
| Add | 2.58× | 2.20× – 3.00× | — |
| Subtract | 2.71× | 2.23× – 2.94× | — |
| Multiply | 1.74× – 3.07× | 1.85× – 2.78× | — |
| Divide | 1.82× – 4.11× | 1.84× – 4.21× | — |
| FMA | — | — | 1.28× – 1.82× |

  </div>
</details>

<details class="kb-entry">
  <summary>Zig</summary>
  <div class="kb-entry-body" markdown="1">

[**Zig Benchmark Results →**](benchmark/vs-zig.html) — FinMix headline, then add / subtract / multiply / divide / FMA band tables (arm64 + x86_64), with ratios.

**Summary — Ratio Range by Operation.** Min–max `ratio = alt / ours` (&gt; 1× ⇒ d128 faster) on x86_64 (Intel i9-9880H) for Zig's reference library (libbid — Zig has no in-language decimal peer), split by profile.

| Operation | P-fin range | P-gen range | FMA range |
|---|---|---|---|
| Add | 2.52× | 1.23× – 2.80× | — |
| Subtract | 3.43× | 1.38× – 4.55× | — |
| Multiply | 2.06× – 6.70× | 2.26× – 6.14× | — |
| Divide | 0.88× – 1.59× | 0.85× – 2.52× | — |
| FMA | — | — | 1.51× – 1.66× |

  </div>
</details>

</div>
