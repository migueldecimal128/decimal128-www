---
layout: default
permalink: /benchmarks.html
title: "Benchmarks — Decimal128"
description: "Performance benchmarks comparing Decimal128 against the IBM libdecnumber, Intel libbid, and Python libmpdec reference libraries."
heading: "Benchmarks"
---

How Decimal128 performs across the supported languages, measured against the
IBM (decQuad), Intel (libbid), and Python (libmpdec) reference libraries and each
language's idiomatic decimal type. The results are split into three views:

- **[Op Benchmark Results](benchmark/op-results.html)** — d128 vs alternatives,
  per operation band, with explicit ratios.
- **[Port-Comparison Benchmark Results](benchmark/port-compare.html)** — each
  port's own d128 band shape on identical operands (no alternatives).
- **[FinMix Benchmark Results](benchmark/finmix.html)** — a realistic financial
  operation mix (P-fin) versus peer implementations.

Methodology and the operation-category taxonomy are in the
[Benchmark Matrix](whitepapers/benchmark-matrix.html).
