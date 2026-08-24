---
layout: default
permalink: /reviews/dotnet/net11-preview7-26376.106.html
title: "System.Numerics.Decimal128 (.NET 11 Preview 7, build 26376.106): An Independent Review — Decimal128"
description: "An independent, standards-anchored review of Microsoft's System.Numerics.Decimal128 as of .NET 11 SDK 11.0.100-preview.7.26376.106 — FMA and the IEEE 754 recommended-function surface arrive, division gets up to 4x faster, with new findings on ln/log10 accuracy near 1 and transcendental rounding."
heading: "System.Numerics.Decimal128 — .NET 11 Preview 7, build 26376.106"
---

<div class="whitepaper" markdown="1">

*Second in a [series](../dotnet.html) — one report per release candidate through GA.
Previous edition: [preview 7, build 26366.102](net11-preview7.html) (frozen as published).*

> **Author stance:** independent, self-appointed decimal128 specialist. Not affiliated
> with the .NET team. Findings are anchored to IEEE 754-2019 and GDAS (Cowlishaw) and
> cross-checked with an independent conformant implementation (d128) plus Intel libbid.

---

## 1. Framing

I did not understand the MSFT release naming convention, so I screwed up on the "name" 
of the previous review. Hopefully this will be more clear. 

This edition reviews **SDK 11.0.100-preview.7.26376.106** (daily build 26376.106,
2026-07-26 in Microsoft's date-coded build scheme), superseding the
[build 26366.102 edition](net11-preview7.html) published 2026-07-14. Both builds are
"preview 7"; the daily-build number is what distinguishes them — and the delta between
these two dailies is a large step, on
both surface area and performance.

The prior edition is frozen as published; every prior finding is retested here against
the new build and explicitly marked **FIXED**, **IMPROVED**, or **UNCHANGED**.

## 2. Executive Summary

- **`FusedMultiplyAdd` exists now, and it is truly fused** (single rounding — verified
  against the corpus). The prior edition's §5.4 "no fusedMultiplyAdd" finding is
  **FIXED**.
- **The IEEE 754 recommended-function surface arrived**: `Decimal128` now implements
  `IFloatingPointIeee754`/`IDecimalFloatingPointIeee754` — sqrt, exp/exp10, ln/log10,
  pow/rootn, quantize, scaleB/logB, round-to-integral in every direction, nextUp/
  nextDown, both remainders (`%` = remainderTrunc, `Ieee754Remainder` =
  remainderNear), quantum queries, and saturating integer conversion
  (`ConvertToInteger<T>`). The
  conformance sweep runs 51,197 vectors GREEN on the required surface.
- **Division is up to 4× faster than build 26366.102** at identical inputs, on both
  x86-64 and Apple silicon — a runtime change, isolated from everything else in this
  review's methodology (see §7). The prior edition's "naive division" headline is
  **IMPROVED**; §7 analyzes what changed and what the algorithm still leaves
  on the table.
- **New accuracy findings on the recommended functions**: the logarithms lose
  catastrophic precision for arguments near 1 — most of the format's 34 digits —
  because the engine converts the decimal operand to a binary working format and
  a near-1 decimal does not survive the re-encoding (§5.7). The other IEEE 754
  clause 9.2 operations are faithfully-rounded rather than correctly-rounded
  (§5.6). IEEE 754 only *recommends* correct rounding there — counted findings,
  not conformance failures — but the near-1 loss lands squarely on this type's
  target domain (log-returns; §5.7 includes the workaround).
- **Microsoft got `RootN` right — and caught a bug of mine**: 
  `RootN` with negative n is correctly rounded
  where my own implementation (and its sibling ports) are 1–2 ulp off — a bug the
  comparison surfaced in *my* engines, now on my punchlist. Credit where due.
  There are no `rootn` vectors in either dectest or intel libbid, presumably because
  the function was added in IEEE 754-2019. 
  
## 3. Scope & Methodology

- **Version under test:** .NET 11 preview 7, SDK **11.0.100-preview.7.26376.106**.
- **Harness:** the same standards-anchored rosetta dispatch as the prior edition,
  extended to drive the full new `IFloatingPointIeee754` surface (fma, transcendentals,
  quantize/scaleB, round-integral in all five directions, directed int64/uint64
  conversion, remainderTrunc/remainderNear, quantum queries). NaN results now run
  through the quieted-propagation oracle instead of being skipped.
- **Bit bridge — changed from the prior edition, caveat retired.** Build 26366.102
  exposed no way to read `Decimal128`'s bits, so the prior run bridged values with a
  raw reinterpreting cast, resting on the empirically-verified assumption that the
  in-memory layout is canonical BID128. This build ships the IEEE 754 clause 5.5.2
  re-encoding operations, and the harness now uses them: every value crossing the
  bridge — every operand in, every result out, and therefore every bit-level
  equality verdict in the sweep — flows through Microsoft's own
  `DecodeBinary`/`EncodeBinary`, cross-checked against the raw cast on each of the
  sweep's 133,615 crossings (zero divergence). Hex-encoded corpus operands are
  additionally decoded through Microsoft's own APIs and cross-checked against the
  independent codec: dectest's DPD operands via `DecodeDecimal`/`EncodeDecimal`
  (clean, both directions), Intel's BID operands via `DecodeBinary`. The prior
  edition verified Microsoft's arithmetic through an assumption about their bits;
  this edition verifies it through their own encoding contract.
- **Benchmark process isolation (new this edition):** on .NET, tier-1 code is
  compiled once per process from the profile gathered when a method first runs
  hot, and never recompiled — so a benchmark cell's result depends on what ran
  before it in the same process. Every cell in this edition therefore runs in
  its own process, trained on its own workload. This applies to the system
  under test as much as the comparison columns — several of Microsoft's divide
  cells measure up to 2× faster than under the prior shared-process
  methodology — and it is one more reason this edition's absolute numbers are
  not directly comparable to the prior edition's tables.
- **Benchmark corpus change (important):** the add/sub benchmark bands are now
  **sign-split datasets** — each band ships a same-sign (`ss`) and an opposite-sign
  (`os`) variant with identical magnitudes, each run on both add and sub, so every
  cell measures exactly one code path (the like-sign *add path* or the unlike-sign
  *magnitude-subtract path*). The prior edition's blended add/sub cells are **not
  comparable** to this edition's tables. Mul/div/FMA bands are unchanged and remain
  comparable.
- **Comparison cohort:** unchanged — `System.Numerics.Decimal128` (SUT), Intel libbid,
  decimal128-csharp, `System.Decimal`.

## 4. What They Got Right

- Everything from the prior edition stands (numeric correctness on the required
  arithmetic surface; canonical BID encoding; honest subnormal handling).
- **FMA is genuinely fused** — not a mul-then-add composition (§5.4-prior: FIXED).
- **`RootN(x, n)` including negative n is correctly rounded** — see §2.
- The five directed round-to-integral operations and the saturating
  `ConvertToInteger<T>` semantics match IEEE 754 clauses 5.8 and 5.9 exactly on the corpus.

## 5. IEEE 754 Compliance — prior findings retested, new findings

Each finding from the [26366.102 edition](net11-preview7.html) §5, retested against this
build, then the findings this build's new surface introduces. Verdict up front on each.

### 5.1 Rounding — **UNCHANGED**

The prior edition's finding stands: arithmetic rounds tiesToEven only, with no
rounding-attribute surface (IEEE 754-2019 clause 4.3), and composing directed results from
already-rounded tiesToEven arithmetic double-rounds. Nothing in this build changes
that, and I do not expect it to change on any near timeline — the
design stance appears settled, and moving it will be a long conversation rather than
a build-over-build fix. The finding is restated here so the series keeps measuring
it, not because this edition expects motion.

One clarification the new surface makes worth stating precisely: the five
round-to-integral operations (IEEE 754 clause 5.9 — `Round`, `Round(…, AwayFromZero)`, `Truncate`,
`Ceiling`, `Floor`), now first-class via `IFloatingPointIeee754`, are themselves
correct value operations, `Decimal128 → Decimal128`. They are not the missing
rounding attributes and were never this finding's target — the double-rounding
concern applies to composing them with already-rounded *arithmetic*, which remains
the only arithmetic there is.

### 5.2 Flags — **UNCHANGED**

No exception/status-flag surface in this build either; the review harness still runs
value-only, exactly as before. The prior edition's argument stands verbatim, including
the confidence-cost point: flags remain the cheapest independent verification channel
Microsoft could give reviewers, and their absence still forces exactly the kind of
external cross-implementation sweep this series performs.

### 5.3 Quantum-preserving string conversion (IEEE 754 clause 5.12) — **UNCHANGED**

Re-verified on this build, more broadly than the prior edition's 18-path analysis:
across **49 formatting paths** (default, `G`, `G0`–`G34`, `R`, `E`/`E0`/`E10`,
`F`/`F0`/`F4`, `N`/`N0`, and custom exponential forms), **none** distinguishes the
positive-exponent cohort members `1E+2` and `100` — and `Parse(x.ToString("R"))`,
nominally the round-trip format, still does not recover the quantum. The parse side
remains compliant, now verified through this build's own API rather than a bit
cast: `Parse("1E+2")` and `Parse("100")` produce distinct encodings under
`EncodeBinary` (coefficient 1 at exponent +2 vs coefficient 100 at exponent 0).
Negative-exponent quantum distinction (`1.0` vs `1.00`) also still works wherever
the format has the precision to express it. The clause 5.12 rendering finding
stands exactly as published.

### 5.4 fusedMultiplyAdd (IEEE 754 clause 5.4.1) — **FIXED**

The prior edition's headline gap is closed, and closed *properly*:

- `Decimal128.FusedMultiplyAdd(left, right, addend)` computes `left*right + addend`
  with a **single rounding**. Verified two independent ways: the conformance sweep's
  FMA vectors (bit-exact against two independent correctly-rounded implementations),
  and the benchmark corpus's FN/FF regimes — the FN band forces the genuinely-wide
  product where a composed multiply-then-add *must* double-round, and this build gets
  those cases bit-exact.
- This is a *required* IEEE 754 clause 5.4.1 operation arriving as a required operation — not
  an estimate. (`MultiplyAddEstimate`, the honestly-named prior stopgap, remains
  available alongside; its continued existence is now an API-hygiene question rather
  than a conformance one.)
- Performance-wise: correct, and currently expensive — the most expensive operation
  in the benchmark suite (≈2 µs on Apple silicon, ≈5 µs on x86-64; §7.6). A
  defensible order of landing: correctness first, speed later.
- Editorially: the prior edition scored this "Later — after GA". Microsoft landed it
  inside preview 7. That deserves explicit credit, and it retires the largest single
  item on the prior edition's recommendation list.

### 5.5 totalOrder (IEEE 754 clause 5.10) — **CHANGED: now reachable; conformant except for cohorts**

The prior edition reported totalOrder absent and expected progress; progress
arrived, most of it real. There is still no `TotalOrder` API on `Decimal128`
itself, but .NET's standard totalOrder vehicle, `TotalOrderIeee754Comparer<T>`
(generic over `IFloatingPointIeee754<T>`), now instantiates and runs for
`Decimal128` as a direct consequence of this build's interface work — and on
everything I probed except one clause, it is correct: ordinary ordering, −0
before +0, and NaN placement at both extremes (−NaN before −∞, +NaN after +∞,
with `Decimal128.NaN` itself a *negative* NaN, as in `double`).

The exception is the one decimal-specific requirement of IEEE 754 clause 5.10:
**cohort members compare equal** — `Compare(100, 1E+2)` returns 0 in every
direction and sign, where the clause requires ordering by exponent. The shipped
source admits it; the comparer's generic path reads, verbatim:

> *"Equivalant values are compared by their exponent parts, and the value with
> smaller exponent is considered closer to zero. This only applies to IEEE 754
> decimals. **Consider to add support if decimals are added into .NET.**
> return 0;"*

Decimals have been added into .NET; the TODO awaits. It is a small, contained
fix — and it is also the quantum-indifference pattern's third appearance, after
§5.3 and the §5.6 exact-result exponents: the implementation is consistently
correct about decimal *values* and consistently indifferent to decimal
*quantums*. See §8.1.

### 5.6 NEW — the IEEE 754 clause 9 recommended functions: present, but faithful rather than correctly rounded

This build implements the IEEE 754-2019 **clause 9.2 recommended operations** —
`Exp`, `Exp10`, `Log` (ln), `Log10`, `Pow`, `RootN` — plus the required `Sqrt` it
already had. Clause 9.2 *recommends* (not requires) correct rounding for these, so
what follows are counted findings against the recommendation, not conformance
failures. My position, stated plainly: for a 34-digit decimal format
whose whole reason to exist is exactness, correctly-rounded is the bar that matters,
and "within 1 ulp" is a specification of doubt.

- **`Sqrt` is correctly rounded** across the sweep, with GDAS-consistent preferred
  exponents on exact cases (`Sqrt(0.16) = 0.4`, not `0.40000…`). No findings.
- **`Exp`/`Pow`/`RootN` are faithfully rounded**: divergences from the
  correctly-rounded reference are sporadic last-place misses, counted per-operation
  in the sweep rather than enumerated here.
- **Exact-result quantum divergence** (cohort-member choice): on exact recommended-op
  results Microsoft returns the full-precision cohort member where GDAS prescribes
  the ideal exponent. Value-correct, quantum-divergent — same IEEE 754 clause 5.12-adjacent
  instinct as the ToString finding (§5.3): the implementation is consistently
  indifferent to the quantum on its way *out*.

### 5.7 NEW — `Log`/`Log2`/`Log10` lose catastrophic precision near 1

The one recommended-function finding that is not a last-place miss: for arguments
near 1, the logarithms lose most of the format's 34 significant digits — the closer
to 1, the worse (`Log(1 + 1e-28)`, an input decimal128 represents *exactly*, comes
back with about 10 correct digits). The root cause is architectural: the
transcendental engine converts the decimal operand into a binary working format
before evaluating, and a near-1 decimal value does not survive that re-encoding —
the digits are gone before the algorithm runs. To my eye this is a mistake in kind,
not in degree: converting to base 2 in a base-10 world discards exactly the
information the format exists to preserve. The provenance explains the choice
without excusing it: the engine derives from Intel's math library, where a
128-bit binary evaluation core already existed as a separate effort — reusing
it for the decimal formats came essentially "for free," and that economy has now
been inherited. The proof that only the conversion is at
fault: `LogP1`, on the same engine, is correctly rounded — handed ε instead of 1+ε,
the machinery is flawless. (That is also the interim workaround: near 1, `x − 1` is
exact in decimal, so `LogP1(x - 1)` gives the full-precision answer `Log(x)`
cannot.) For the financial mathematics this type targets — log-returns,
continuously-compounded rates — near 1 is precisely the regime that matters;
until it changes, the `LogP1(x − 1)` workaround above is the practical answer.

### 5.8 NEW — `RootN`: Microsoft is correctly rounded where my implementations are not

On `RootN(x, n)` with negative `n`, this build is correctly
rounded on cases where my own implementation (and its sibling
ports, which share the algorithm) are off by 1–2 ulp (`RootN(27, -3)`,
`RootN(2, -2³¹)`, …). The comparison harness caught my implementations, not the
system under test. The bug (a rounded reciprocal-exponent feeding `pow`, plus a
double-rounding power-of-two path) is now on my own punchlist, and the affected
oracle vectors are being regenerated against an independent high-precision source.
There are no `rootn` vectors in either dectest or intel libbid, presumably because
the function was added in IEEE 754-2019.

## 6. Permitted & Intentional Divergences

- **Non-canonical propagation through the re-encoding operations** (new surface,
  verified this edition): `DecodeBinary`/`EncodeBinary` propagate non-canonical
  encodings raw — permitted by IEEE 754-2019 clause 5.5.2 ("these operations may
  propagate non-canonical encodings"). Implementations that canonicalize on
  decode will observe pattern differences on non-canonical interchange data,
  never value differences (2,153 such vectors in this edition's sweep; values
  agree on all of them). There is a strong argument that best-practice is for
  implementations to not generate/emit non-canonical values. 
  In addition, if non-canonical
  values were canonicalized upon decode (rather than simply pass-thru),
  then the op execution paths would not
  have to deal with this case, eliminating the need for a run-time check during
  execution. Note that this is not an option for hardware implementations, 
  because they have no control
  over where the operand bits are coming from. 
- **Min/max family**: retest deferred in this edition's sweep (the NaN-handling
  oracle for min/max semantics is still being wired); no verdict asserted either way.
- The remaining prior-edition §6 items stand as published pending the retest pass.

## 7. Performance

The performance story of this build is division. Between the two dailies,
`Decimal128` divide got **up to 4× faster at identical inputs** — attribution
established by A/B-ing the two SDKs against fixed comparison binaries and a fixed
corpus, isolating the runtime from every other variable, and confirmed on both
Apple silicon and x86-64. The change is dotnet/runtime PR **#130957** (merged
2026-07-19, squarely between the two daily builds), whose own microbenchmarks
report Decimal128 divide going 417.7 → 109.0 ns — the same ~4× this review
measures. The same PR modestly improved add/sub/multiply and dramatically improved
several conversions.

**What the 4× is — and is not** (this matters for reading §7.5): the prior
edition called the division "naive," and the source confirmed it — digit-serial
long division, producing the ~35-digit quotient *one decimal digit at a time*,
each digit costing a full software `UInt128` division (~35 of them per divide).
PR #130957 keeps the same algorithm and batches the loop: each iteration now
brings down as many digits as the remainder's leading-zero headroom allows
(`10^k` at a time) and extracts them with a single `DivRem` — cutting the ~35
software divisions per divide to a divisor-width-dependent handful (a narrow
divisor lets each step take ~33 digits; a full-width divisor only ~4, which is
why the XD band remains the most expensive). **It is an optimization of the naive
algorithm, not a change of algorithm** — and underneath it sits the same design
constraint as before: no integer wider than one 128-bit limb, ever.

That constraint shapes what the algorithm can and cannot see. The loop runs
identically whatever the divisor is: it has no notion of divisor width, and no
notion of divisor *value* — a division by an exact power of ten walks the same
digit-extraction path as any other. The divide table below shows the consequence
band by band; the comparison columns (Intel's libbid among them) indicate how
much of the cost is inherent to 34-digit decimal division versus inherent to
this algorithm. Intel's own techniques are documented in Cornea et al., ["A
Software Implementation of the IEEE 754R Decimal Floating-Point Arithmetic
Using the Binary Encoding Format"](https://www.cl.cam.ac.uk/~jrh13/papers/decimal.pdf),
*IEEE Transactions on Computers*, vol. 58, no. 2, Feb. 2009 — the standing
description of what a mature software implementation of this format does. To be fair to the design: the one-limb invariant buys a single
generic implementation serving Decimal32/64/128, no wide-integer machinery, and
easily-audited correctness (the PR differential-tested 9M cases against the old
loop). But it also means the next 4× is not available by tuning the loop — it
will require a different algorithm. 

### 7.1 P-fin (financial profile)

*Realistic financial mix (P-fin) — M3 Pro (arm64):*

<!-- BEGIN GENERATED net11-pfin-abs -->

| op | cat | Decimal128 (.NET 11) | libbid C | decimal128-csharp | System.Decimal |
|---|---|---:|---:|---:|---:|
| add | MIX | 9.67 | 10.72 | 2.72 | 2.79 |
| sub | MIX | 10.30 | 11.80 | 3.26 | 3.03 |
| mul | CP | 8.69 | 23.57 | 1.62 | — |
| mul | WP | 31.13 | 34.52 | 17.44 | — |
| div | CD | 60.35 | 35.07 | 23.57 | 11.30 |
| div | WD | 50.50 | 40.37 | 32.48 | 19.19 |
| div | ET | 103.42 | 6.09 | 6.96 | 5.01 |
| div | PT | 105.00 | 6.09 | 5.15 | 11.30 |

<!-- END GENERATED net11-pfin-abs -->

*Realistic financial mix (P-fin) — i9-9880H (x86_64):*

<!-- BEGIN GENERATED net11-pfin-abs-x86 -->

| op | cat | Decimal128 (.NET 11) | libbid C | decimal128-csharp | System.Decimal |
|---|---|---:|---:|---:|---:|
| add | MIX | 23.51 | 27.49 | 8.62 | 8.73 |
| sub | MIX | 27.17 | 28.61 | 12.63 | 10.09 |
| mul | CP | 34.18 | 44.36 | 4.82 | — |
| mul | WP | 98.75 | 57.85 | 40.40 | — |
| div | CD | 198.67 | 74.56 | 87.22 | 53.38 |
| div | WD | 161.47 | 80.65 | 94.93 | 95.33 |
| div | ET | 387.07 | 19.63 | 23.19 | 13.84 |
| div | PT | 405.51 | 19.55 | 12.36 | 58.43 |

<!-- END GENERATED net11-pfin-abs-x86 -->

### 7.2 Add (P-gen, sign-split)

*Add (P-gen, sign-split) — M3 Pro (arm64):*

<!-- BEGIN GENERATED net11-add-abs -->

| op | cat | Decimal128 (.NET 11) | libbid C | decimal128-csharp | System.Decimal |
|---|---|---:|---:|---:|---:|
| add | SQss | 11.93 | 7.96 | 1.41 | 2.84 |
| add | SQos | 12.68 | 8.69 | 3.40 | 2.88 |
| add | NQss | 14.36 | 9.36 | 7.04 | 3.72 |
| add | NQos | 14.91 | 9.78 | 7.02 | 3.84 |
| add | MQss | 15.85 | 9.75 | 8.68 | 3.70 |
| add | MQos | 15.11 | 9.71 | 25.44 | 3.78 |
| add | OQss | 99.34 | 13.66 | 17.29 | — |
| add | OQos | 99.39 | 15.31 | 33.77 | — |
| add | FQss | 724.49 | 9.32 | 13.06 | — |
| add | FQos | 765.70 | 10.38 | 15.90 | — |

<!-- END GENERATED net11-add-abs -->

*Add (P-gen, sign-split) — i9-9880H (x86_64):*

<!-- BEGIN GENERATED net11-add-abs-x86 -->

| op | cat | Decimal128 (.NET 11) | libbid C | decimal128-csharp | System.Decimal |
|---|---|---:|---:|---:|---:|
| add | SQss | 45.51 | 27.16 | 3.61 | 7.42 |
| add | SQos | 57.00 | 25.75 | 11.00 | 10.09 |
| add | NQss | 51.06 | 29.03 | 14.73 | 11.55 |
| add | NQos | 55.58 | 28.31 | 21.06 | 13.21 |
| add | MQss | 52.94 | 27.10 | 19.62 | 11.04 |
| add | MQos | 56.15 | 26.84 | 44.01 | 12.55 |
| add | OQss | 264.80 | 43.08 | 46.94 | — |
| add | OQos | 265.03 | 43.29 | 75.53 | — |
| add | FQss | 1720.58 | 28.98 | 36.19 | — |
| add | FQos | 1726.56 | 29.89 | 43.83 | — |

<!-- END GENERATED net11-add-abs-x86 -->

### 7.3 Subtract (P-gen, sign-split)

*Subtract (P-gen, sign-split) — M3 Pro (arm64):*

<!-- BEGIN GENERATED net11-sub-abs -->

| op | cat | Decimal128 (.NET 11) | libbid C | decimal128-csharp | System.Decimal |
|---|---|---:|---:|---:|---:|
| sub | SQss | 12.93 | 9.68 | 2.29 | 2.36 |
| sub | SQos | 11.97 | 10.04 | 1.52 | 3.54 |
| sub | NQss | 14.61 | 10.87 | 6.37 | 3.85 |
| sub | NQos | 14.24 | 11.42 | 5.61 | 3.76 |
| sub | MQss | 14.88 | 9.94 | 15.91 | 3.77 |
| sub | MQos | 15.70 | 9.78 | 8.68 | 3.79 |
| sub | OQss | 99.83 | 15.79 | 31.44 | — |
| sub | OQos | 98.54 | 14.84 | 16.25 | — |
| sub | FQss | 735.35 | 9.39 | 14.63 | — |
| sub | FQos | 724.71 | 9.48 | 12.14 | — |

<!-- END GENERATED net11-sub-abs -->

*Subtract (P-gen, sign-split) — i9-9880H (x86_64):*

<!-- BEGIN GENERATED net11-sub-abs-x86 -->

| op | cat | Decimal128 (.NET 11) | libbid C | decimal128-csharp | System.Decimal |
|---|---|---:|---:|---:|---:|
| sub | SQss | 49.93 | 31.21 | 9.87 | 9.60 |
| sub | SQos | 45.39 | 29.85 | 4.52 | 7.07 |
| sub | NQss | 56.03 | 31.57 | 18.19 | 13.53 |
| sub | NQos | 52.06 | 32.24 | 11.43 | 12.44 |
| sub | MQss | 57.68 | 30.59 | 42.52 | 12.39 |
| sub | MQos | 54.67 | 30.70 | 21.06 | 10.84 |
| sub | OQss | 265.54 | 46.61 | 77.01 | — |
| sub | OQos | 266.68 | 46.07 | 44.27 | — |
| sub | FQss | 1706.63 | 33.80 | 41.50 | — |
| sub | FQos | 1722.73 | 32.91 | 35.68 | — |

<!-- END GENERATED net11-sub-abs-x86 -->

### 7.4 Multiply (P-gen)

Multiply also improved in PR #130957, via two fast paths its summary doesn't
mention: when both coefficients fit in 64 bits, one native multiply replaces the
four-multiply schoolbook decomposition (the CP regime), and the rounding step's
trailing-digit drop — previously performed *one digit at a time* for this format,
the same digit-serial pattern as the old divide — now removes all excess digits
with a single division when the product fits one limb (why WP, which always drops
1–4 digits, improved the most at ~1.8×). Products wider than 38 digits fail both
guards and keep the old wide machinery — XP improved too, but remains far the
weakest band in the table at ~16–18× libbid.

*Multiply (P-gen) — M3 Pro (arm64):*

<!-- BEGIN GENERATED net11-mul-abs -->

| op | cat | Decimal128 (.NET 11) | libbid C | decimal128-csharp | System.Decimal |
|---|---|---:|---:|---:|---:|
| mul | CP | 9.17 | 23.13 | 2.07 | — |
| mul | WP | 29.79 | 35.06 | 16.46 | — |
| mul | XP | 742.39 | 45.24 | 43.54 | — |

<!-- END GENERATED net11-mul-abs -->

*Multiply (P-gen) — i9-9880H (x86_64):*

<!-- BEGIN GENERATED net11-mul-abs-x86 -->

| op | cat | Decimal128 (.NET 11) | libbid C | decimal128-csharp | System.Decimal |
|---|---|---:|---:|---:|---:|
| mul | CP | 36.21 | 45.57 | 7.59 | — |
| mul | WP | 101.35 | 64.59 | 43.06 | — |
| mul | XP | 1654.32 | 93.63 | 77.48 | — |

<!-- END GENERATED net11-mul-abs-x86 -->

### 7.5 Divide (P-gen)

Read this table against the algorithm analysis in the §7 intro. The bands split by
divisor width (CD compact / WD wide / XD extra-wide) and by value-driven structure
(ET exact quotients, PT power-of-ten divisors). Two signatures of the batched-loop
design are visible. First, CD/WD/XD costs show no divisor-width structure — the loop
doesn't know the divisor's width. Second,
and counter-intuitively, **the structurally easy bands are among Microsoft's most
expensive**: ET and PT — exact quotients and power-of-ten divisors, the cases with
the least mathematical work in them — cost roughly *double* the width-generic
CD/WD bands. The reason is in the source: an exact quotient takes
the trailing-zero strip loop, which PR #130957 left untouched — and it still strips
**one digit per iteration**, a `DivRem`-by-ten each. The naive digit-serial pattern
was optimized out of the quotient loop and survives in the strip loop, and PT/ET is
where it bites (an 8–12× gap to Intel's libbid on PT in these tables).

*Divide (P-gen) — M3 Pro (arm64):*

<!-- BEGIN GENERATED net11-div-abs -->

| op | cat | Decimal128 (.NET 11) | libbid C | decimal128-csharp | System.Decimal |
|---|---|---:|---:|---:|---:|
| div | CD | 56.63 | 36.77 | 28.67 | — |
| div | WD | 52.06 | 37.54 | 31.31 | — |
| div | XD | 109.37 | 38.97 | 35.54 | — |
| div | ET | 96.04 | 11.68 | 13.16 | — |
| div | PT | 91.45 | 11.45 | 5.05 | — |

<!-- END GENERATED net11-div-abs -->

*Divide (P-gen) — i9-9880H (x86_64):*

<!-- BEGIN GENERATED net11-div-abs-x86 -->

| op | cat | Decimal128 (.NET 11) | libbid C | decimal128-csharp | System.Decimal |
|---|---|---:|---:|---:|---:|
| div | CD | 198.46 | 81.20 | 93.04 | — |
| div | WD | 171.65 | 82.98 | 97.29 | — |
| div | XD | 293.82 | 82.60 | 105.37 | — |
| div | ET | 352.22 | 29.87 | 32.85 | — |
| div | PT | 347.94 | 30.17 | 10.58 | — |

<!-- END GENERATED net11-div-abs-x86 -->

### 7.6 FMA

The newly-landed `FusedMultiplyAdd` (§5.4) is verified correct, and it is the most
expensive operation in the suite — roughly 20–50× libbid (≈1.9–2.3 µs on Apple
silicon, ≈4.7–5.8 µs on x86-64). The
mechanism follows directly from the §7 analysis: a fused decimal128 FMA must form
the exact ~68-digit product, which is the one intermediate that *cannot* fit in a
single 128-bit limb — so the operation misses both of PR #130957's fast paths (the
single-native-multiply shortcut and the batched digit drop, §7.4) and runs the wide
fallback machinery end to end, including the per-digit drop loop. That also explains
the table's inversion: FF — the structurally easy regime, where the addend dwarfs
the product and the result fits comfortably in 128 bits — costs *more* than the
genuinely-wide FN regime, because nearly all of the product's ~60 excess digits must
be discarded one at a time, and FF has the most digits to discard. The digit-serial
pattern surfaces here at full amplitude, after divide's ET/PT strip (§7.5) and
multiply's XP band (§7.4). The inversion reproduces identically on both
architectures, as a purely algorithmic effect should.

*FMA — M3 Pro (arm64):*

<!-- BEGIN GENERATED net11-fma-abs -->

| op | cat | Decimal128 (.NET 11) | libbid C | decimal128-csharp | System.Decimal |
|---|---|---:|---:|---:|---:|
| fma | FN | 1944.22 | 82.83 | 103.37 | — |
| fma | FF | 2339.28 | 58.46 | 76.63 | — |

<!-- END GENERATED net11-fma-abs -->

*FMA — i9-9880H (x86_64):*

<!-- BEGIN GENERATED net11-fma-abs-x86 -->

| op | cat | Decimal128 (.NET 11) | libbid C | decimal128-csharp | System.Decimal |
|---|---|---:|---:|---:|---:|
| fma | FN | 4650.50 | 155.17 | 186.16 | — |
| fma | FF | 5766.63 | 119.14 | 130.74 | — |

<!-- END GENERATED net11-fma-abs-x86 -->

## 8. Recommendations

### 8.1 Now — before GA

1. **Quantum-preserving render** (§5.3): one formatting path — even a dedicated
   method — that round-trips the cohort member would satisfy IEEE 754 clause 5.12.
2. **Finish `TotalOrderIeee754Comparer<Decimal128>`'s cohort ordering** (§5.5).
   Most of totalOrder arrived correct with the interface work; the one missing
   clause is the decimal-specific cohort ordering, and the generic path already
   carries the TODO acknowledging it. Before GA is the window, because after GA
   cohort-equal ordering becomes observable behavior someone depends on.
3. **API hygiene**: decide `MultiplyAddEstimate`'s fate now that the real
   `FusedMultiplyAdd` exists (§5.4) — surface decisions are exactly what a GA
   locks in.

### 8.2 Later — after GA (additive, non-breaking)

- **Rounding attributes for arithmetic** (§5.1): kept on the list as the standing
  long-horizon item. I expect this to be a sustained conversation across
  releases, not a preview fix, and will keep measuring it each edition.
- **Status flags** (§5.2): still the cheapest independent verification channel;
  additive as an opt-in context or out-parameter surface.

## 9. Conclusion


The implementation team has been introducing significant functionality. 
They have maintained correctly rounded tiesToEven arithmetic. 
I wish them luck over the coming weeks as they finalize functionality prior
to code freeze. 
