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

| Operation | P-fin range | P-gen range |
|---|---|---|
| Add | 3.1× – 5.9× | 0.9× – 5.9× |
| Subtract | 4.2× – 7.2× | 1.0× – 10.6× |
| Multiply | 1.0× – 22.3× | 1.4× – 13.5× |
| Divide | 0.8× – 8.6× | 0.8× – 10.5× |

  </div>
</details>

<details class="kb-entry">
  <summary>C#</summary>
  <div class="kb-entry-body" markdown="1">

[**C# Benchmark Results →**](benchmark/vs-csharp.html) — FinMix headline, then add / subtract / multiply / divide / FMA band tables (arm64 + x86_64), with ratios.

**Summary — Ratio Range by Operation.** Min–max `ratio = alt / ours` (&gt; 1× ⇒ d128 faster) on x86_64 (Intel i9-9880H), across both reference/idiom peers (`System.Decimal`, `Decimal128` .NET 11), split by profile.

| Operation | P-fin range | P-gen range |
|---|---|---|
| Add | 0.8× – 2.5× | 0.4× – 50.9× |
| Subtract | 0.9× – 2.9× | 0.3× – 50.3× |
| Multiply | 2.2× – 7.6× | 2.1× – 33.6× |
| Divide | 0.5× – 54.1× | 3.4× – 43.6× |

  </div>
</details>

<details class="kb-entry">
  <summary>Java</summary>
  <div class="kb-entry-body" markdown="1">

[**Java Benchmark Results →**](benchmark/vs-java.html) — FinMix headline, then add / subtract / multiply / divide / FMA band tables (arm64 + x86_64), with ratios.

**Summary — Ratio Range by Operation.** Min–max `ratio = alt / ours` (&gt; 1× ⇒ d128 faster) on x86_64 (Intel i9-9880H), across both reference/idiom peers (`BigDecimal`, libbid), split by profile.

| Operation | P-fin range | P-gen range |
|---|---|---|
| Add | 3.4× | 2.3× – 6.0× |
| Subtract | 4.1× | 2.3× – 4.9× |
| Multiply | 3.1× – 3.4× | 2.7× – 3.6× |
| Divide | 1.8× – 60.1× | 2.1× – 43.9× |

  </div>
</details>

<details class="kb-entry">
  <summary>Kotlin KMP</summary>
  <div class="kb-entry-body" markdown="1">

[**Kotlin Benchmark Results →**](benchmark/vs-kotlin.html) — FinMix headline, then add / subtract / multiply / divide / FMA band tables (arm64 + x86_64), with ratios.

**Summary — Ratio Range by Operation.** Min–max `ratio = alt / ours` (&gt; 1× ⇒ d128 faster) on x86_64 (Intel i9-9880H), across both reference/idiom peers (`BigDecimal`, libbid), split by profile.

| Operation | P-fin range | P-gen range |
|---|---|---|
| Add | 2.7× | 2.0× – 4.6× |
| Subtract | 3.8× | 2.3× – 4.7× |
| Multiply | 3.3× – 3.6× | 2.9× – 3.3× |
| Divide | 1.8× – 55.5× | 2.2× – 40.5× |

  </div>
</details>

<details class="kb-entry">
  <summary>Swift</summary>
  <div class="kb-entry-body" markdown="1">

[**Swift Benchmark Results →**](benchmark/vs-swift.html) — FinMix headline, then add / subtract / multiply / divide / FMA band tables (arm64 + x86_64), with ratios.

**Summary — Ratio Range by Operation.** Min–max `ratio = alt / ours` (&gt; 1× ⇒ d128 faster) on x86_64 (Intel i9-9880H), across both reference/idiom peers (`Foundation.Decimal`, libbid), split by profile.

| Operation | P-fin range | P-gen range |
|---|---|---|
| Add | 69.3× | 21.6× – 83.1× |
| Subtract | 77.9× | 21.5× – 100.4× |
| Multiply | 21.2× – 176.9× | 22.0× – 102.8× |
| Divide | 16.6× – 643.9× | 16.2× – 551.1× |

  </div>
</details>

<details class="kb-entry">
  <summary>Rust</summary>
  <div class="kb-entry-body" markdown="1">

[**Rust Benchmark Results →**](benchmark/vs-rust.html) — FinMix headline, then add / subtract / multiply / divide / FMA band tables (arm64 + x86_64), with ratios.

**Summary — Ratio Range by Operation.** Min–max `ratio = alt / ours` (&gt; 1× ⇒ d128 faster) on x86_64 (Intel i9-9880H), across both reference/idiom peers (`rust_decimal`, libbid), split by profile.

| Operation | P-fin range | P-gen range |
|---|---|---|
| Add | 1.6× | 0.8× – 1.9× |
| Subtract | 1.9× | 0.7× – 1.9× |
| Multiply | 2.0× – 15.0× | 2.2× – 9.0× |
| Divide | 0.6× – 5.3× | 1.0× – 3.1× |

  </div>
</details>

<details class="kb-entry">
  <summary>Go</summary>
  <div class="kb-entry-body" markdown="1">

[**Go Benchmark Results →**](benchmark/vs-go.html) — FinMix headline, then add / subtract / multiply / divide / FMA band tables (arm64 + x86_64), with ratios.

**Summary — Ratio Range by Operation.** Go has no in-language decimal peer and takes no libbid fallback, so every row is d128-only — there is no alternative to compute a ratio against.

| Operation | P-fin range | P-gen range |
|---|---|---|
| Add | — | — |
| Subtract | — | — |
| Multiply | — | — |
| Divide | — | — |

  </div>
</details>

<details class="kb-entry">
  <summary>Python</summary>
  <div class="kb-entry-body" markdown="1">

[**Python Benchmark Results →**](benchmark/vs-python.html) — FinMix headline, then add / subtract / multiply / divide / FMA band tables (arm64 + x86_64), with ratios.

**Summary — Ratio Range by Operation.** Min–max `ratio = alt / ours` (&gt; 1× ⇒ d128 faster) on x86_64 (Intel i9-9880H) for Python's idiom peer (`decimal.Decimal`), split by profile.

| Operation | P-fin range | P-gen range |
|---|---|---|
| Add | 2.6× | 2.2× – 3.0× |
| Subtract | 2.7× | 2.2× – 2.9× |
| Multiply | 1.7× – 3.1× | 1.9× – 2.8× |
| Divide | 1.8× – 4.1× | 1.8× – 4.2× |

  </div>
</details>

<details class="kb-entry">
  <summary>Zig</summary>
  <div class="kb-entry-body" markdown="1">

[**Zig Benchmark Results →**](benchmark/vs-zig.html) — FinMix headline, then add / subtract / multiply / divide / FMA band tables (arm64 + x86_64), with ratios.

**Summary — Ratio Range by Operation.** Min–max `ratio = alt / ours` (&gt; 1× ⇒ d128 faster) on x86_64 (Intel i9-9880H) for Zig's reference library (libbid — Zig has no in-language decimal peer), split by profile.

| Operation | P-fin range | P-gen range |
|---|---|---|
| Add | 2.5× | 1.2× – 2.8× |
| Subtract | 3.4× | 1.4× – 4.6× |
| Multiply | 2.1× – 6.7× | 2.3× – 6.1× |
| Divide | 0.9× – 1.6× | 0.9× – 2.5× |

  </div>
</details>

</div>
