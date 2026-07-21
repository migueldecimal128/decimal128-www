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

<div class="lang-pills">
  <a href="#lang-c" class="lang-pill">C</a>
  <a href="#lang-csharp" class="lang-pill">C#</a>
  <a href="#lang-java" class="lang-pill">Java</a>
  <a href="#lang-kotlin" class="lang-pill">Kotlin KMP</a>
  <a href="#lang-swift" class="lang-pill">Swift</a>
  <a href="#lang-rust" class="lang-pill">Rust</a>
  <a href="#lang-go" class="lang-pill">Go</a>
  <a href="#lang-python" class="lang-pill">Python</a>
  <a href="#lang-zig" class="lang-pill">Zig</a>
</div>

## Per-language results

<div class="kb-results">

<details class="kb-entry" id="lang-c">
  <summary>C</summary>
  <div class="kb-entry-body" markdown="1">

[**C Benchmark Results →**](benchmark/vs-c.html) — FinMix headline, then add / subtract / multiply / divide / FMA band tables (arm64 + x86_64), with ratios.

**Ratio by Operation.** Each row is the ratio for that reference library on x86_64 (Intel i9-9880H): `ratio = libbid / ours`, `ratio = decQuad / ours`, or `ratio = mpdecimal / ours` (&gt; 1× ⇒ d128 faster).

| | Add | Subtract | Multiply | Divide |
|---|---|---|---|---|
| ratio = libbid / Miguel | 3× | 4× | 1.3× – 19× | 0.8× – 1.9× |
| ratio = decQuad / Miguel | 6× | 7× | 1.5× – 22× | 1.6× – 7× |
| ratio = mpdecimal / Miguel | 4× | 5× | 1.0× – 13× | 1.8× – 9× |

  </div>
</details>

<details class="kb-entry" id="lang-csharp">
  <summary>C#</summary>
  <div class="kb-entry-body" markdown="1">

[**C# Benchmark Results →**](benchmark/vs-csharp.html) — FinMix headline, then add / subtract / multiply / divide / FMA band tables (arm64 + x86_64), with ratios.

**Ratio by Operation.** Each row is the ratio for that reference/idiom peer on x86_64 (Intel i9-9880H): `ratio = System.Decimal / ours` or `ratio = Decimal128 (.NET 11) / ours` (&gt; 1× ⇒ d128 faster). `System.Decimal` has no wide-product multiply band, so that cell is blank.

| | Add | Subtract | Multiply | Divide |
|---|---|---|---|---|
| ratio = System.Decimal / Miguel | 0.8× | 0.9× | — | 0.5× – 5× |
| ratio = Decimal128 (.NET 11) / Miguel | 2.5× | 2.9× | 2.2× – 8× | 4× – 54× |

  </div>
</details>

<details class="kb-entry" id="lang-java">
  <summary>Java</summary>
  <div class="kb-entry-body" markdown="1">

[**Java Benchmark Results →**](benchmark/vs-java.html) — FinMix headline, then add / subtract / multiply / divide / FMA band tables (arm64 + x86_64), with ratios.

**Ratio by Operation.** The ratio for Java's idiom peer on x86_64 (Intel i9-9880H): `ratio = BigDecimal / ours` (&gt; 1× ⇒ d128 faster).

| | Add | Subtract | Multiply | Divide |
|---|---|---|---|---|
| ratio = BigDecimal / Miguel | 3× | 4× | 3× | 1.8× – 60× |

  </div>
</details>

<details class="kb-entry" id="lang-kotlin">
  <summary>Kotlin KMP</summary>
  <div class="kb-entry-body" markdown="1">

[**Kotlin Benchmark Results →**](benchmark/vs-kotlin.html) — FinMix headline, then add / subtract / multiply / divide / FMA band tables (arm64 + x86_64), with ratios.

**Ratio by Operation.** The ratio for Kotlin's idiom peer on x86_64 (Intel i9-9880H): `ratio = BigDecimal / ours` (&gt; 1× ⇒ d128 faster).

| | Add | Subtract | Multiply | Divide |
|---|---|---|---|---|
| ratio = BigDecimal / Miguel | 2.7× | 4× | 3× – 4× | 1.8× – 55× |

  </div>
</details>

<details class="kb-entry" id="lang-swift">
  <summary>Swift</summary>
  <div class="kb-entry-body" markdown="1">

[**Swift Benchmark Results →**](benchmark/vs-swift.html) — FinMix headline, then add / subtract / multiply / divide / FMA band tables (arm64 + x86_64), with ratios.

**Ratio by Operation.** The ratio for Swift's idiom peer on x86_64 (Intel i9-9880H): `ratio = Foundation.Decimal / ours` (&gt; 1× ⇒ d128 faster).

| | Add | Subtract | Multiply | Divide |
|---|---|---|---|---|
| ratio = Foundation.Decimal / Miguel | 69× | 78× | 21× – 177× | 17× – 644× |

  </div>
</details>

<details class="kb-entry" id="lang-rust">
  <summary>Rust</summary>
  <div class="kb-entry-body" markdown="1">

[**Rust Benchmark Results →**](benchmark/vs-rust.html) — FinMix headline, then add / subtract / multiply / divide / FMA band tables (arm64 + x86_64), with ratios.

**Ratio by Operation.** Each row is the ratio for that reference/idiom peer on x86_64 (Intel i9-9880H): `ratio = rust_decimal / ours` or `ratio = libbid / ours` (&gt; 1× ⇒ d128 faster). `rust_decimal` has no wide-product multiply band (that falls back to libbid), and libbid isn't used for add/subtract/divide, so those cells are blank.

| | Add | Subtract | Multiply | Divide |
|---|---|---|---|---|
| ratio = rust_decimal / Miguel | 1.6× | 1.9× | — | 0.6× – 5× |
| ratio = libbid / Miguel | — | — | 2.0× – 15× | — |

  </div>
</details>

<details class="kb-entry" id="lang-go">
  <summary>Go</summary>
  <div class="kb-entry-body" markdown="1">

[**Go Benchmark Results →**](benchmark/vs-go.html) — FinMix headline, then add / subtract / multiply / divide / FMA band tables (arm64 + x86_64), with ratios.

**Ratio by Operation.** Go has no in-language decimal peer and takes no libbid fallback, so there is no alternative to compute a ratio against.

  </div>
</details>

<details class="kb-entry" id="lang-python">
  <summary>Python</summary>
  <div class="kb-entry-body" markdown="1">

[**Python Benchmark Results →**](benchmark/vs-python.html) — FinMix headline, then add / subtract / multiply / divide / FMA band tables (arm64 + x86_64), with ratios.

**Ratio by Operation.** The ratio for Python's idiom peer on x86_64 (Intel i9-9880H): `ratio = decimal.Decimal / ours` (&gt; 1× ⇒ d128 faster).

| | Add | Subtract | Multiply | Divide |
|---|---|---|---|---|
| ratio = decimal.Decimal / Miguel | 2.6× | 2.7× | 1.7× – 3× | 1.8× – 4× |

  </div>
</details>

<details class="kb-entry" id="lang-zig">
  <summary>Zig</summary>
  <div class="kb-entry-body" markdown="1">

[**Zig Benchmark Results →**](benchmark/vs-zig.html) — FinMix headline, then add / subtract / multiply / divide / FMA band tables (arm64 + x86_64), with ratios.

**Ratio by Operation.** The ratio for Zig's reference library on x86_64 (Intel i9-9880H): `ratio = libbid / ours` (&gt; 1× ⇒ d128 faster). Zig has no in-language decimal peer.

| | Add | Subtract | Multiply | Divide |
|---|---|---|---|---|
| ratio = libbid / Miguel | 2.5× | 3× | 2.1× – 7× | 0.9× – 1.6× |

  </div>
</details>

</div>

<script>
document.querySelectorAll('.lang-pill').forEach(function (link) {
  link.addEventListener('click', function (e) {
    var target = document.querySelector(link.getAttribute('href'));
    if (target && target.tagName === 'DETAILS') {
      e.preventDefault();
      target.open = true;
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      history.pushState(null, '', link.getAttribute('href'));
    }
  });
});
</script>
