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

  </div>
</details>

<details class="kb-entry">
  <summary>C#</summary>
  <div class="kb-entry-body" markdown="1">

[**C# Benchmark Results →**](benchmark/vs-csharp.html) — FinMix headline, then add / subtract / multiply / divide / FMA band tables (arm64 + x86_64), with ratios.

  </div>
</details>

<details class="kb-entry">
  <summary>Java</summary>
  <div class="kb-entry-body" markdown="1">

[**Java Benchmark Results →**](benchmark/vs-java.html) — FinMix headline, then add / subtract / multiply / divide / FMA band tables (arm64 + x86_64), with ratios.

  </div>
</details>

<details class="kb-entry">
  <summary>Kotlin KMP</summary>
  <div class="kb-entry-body" markdown="1">

[**Kotlin Benchmark Results →**](benchmark/vs-kotlin.html) — FinMix headline, then add / subtract / multiply / divide / FMA band tables (arm64 + x86_64), with ratios.

  </div>
</details>

<details class="kb-entry">
  <summary>Swift</summary>
  <div class="kb-entry-body" markdown="1">

[**Swift Benchmark Results →**](benchmark/vs-swift.html) — FinMix headline, then add / subtract / multiply / divide / FMA band tables (arm64 + x86_64), with ratios.

  </div>
</details>

<details class="kb-entry">
  <summary>Rust</summary>
  <div class="kb-entry-body" markdown="1">

[**Rust Benchmark Results →**](benchmark/vs-rust.html) — FinMix headline, then add / subtract / multiply / divide / FMA band tables (arm64 + x86_64), with ratios.

  </div>
</details>

<details class="kb-entry">
  <summary>Go</summary>
  <div class="kb-entry-body" markdown="1">

[**Go Benchmark Results →**](benchmark/vs-go.html) — FinMix headline, then add / subtract / multiply / divide / FMA band tables (arm64 + x86_64), with ratios.

  </div>
</details>

<details class="kb-entry">
  <summary>Python</summary>
  <div class="kb-entry-body" markdown="1">

[**Python Benchmark Results →**](benchmark/vs-python.html) — FinMix headline, then add / subtract / multiply / divide / FMA band tables (arm64 + x86_64), with ratios.

  </div>
</details>

<details class="kb-entry">
  <summary>Zig</summary>
  <div class="kb-entry-body" markdown="1">

[**Zig Benchmark Results →**](benchmark/vs-zig.html) — FinMix headline, then add / subtract / multiply / divide / FMA band tables (arm64 + x86_64), with ratios.

  </div>
</details>

</div>
