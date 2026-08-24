---
layout: default
permalink: /reviews/dotnet/net11-preview7.html
title: "System.Numerics.Decimal128 (.NET 11 Preview 7): An Independent Review — Decimal128"
description: "An independent, standards-anchored review of Microsoft's System.Numerics.Decimal128 as of .NET 11 preview 7 — verified numerically correct, with findings on rounding (double-rounding), status flags, string conversion (ToString), and division performance."
heading: "System.Numerics.Decimal128 — .NET 11 Preview 7"
---

<div class="whitepaper" markdown="1">

*First in a series — one report per release candidate through GA*

> **Author stance:** independent, self-appointed decimal128 specialist. Not affiliated
> with the .NET team. Findings are anchored to IEEE 754-2019 and GDAS (Cowlishaw) and
> cross-checked with an independent conformant implementation (d128) plus Intel libbid.

---

## 1. Framing
- I am an independent decimal128 specialist. 
  I have no affiliation with the .NET team. 
  I don't know anyone on the .NET team.
  I maintain my own conformant implementation (decimal128-csharp) and a 
  cross-checking (Rosetta) suite that
  consolidates 57k IEEE 754 decimal128 test vectors in three different text formats from IBM and Intel. Rosetta parses the text formats in their original form, calls the appropriate operation for the implementation under test, and compares bit-wise conformance of the expected result. 
- This document, Rosetta, and the benchmark harness are written with
  the assistance of Anthropic Claude AI, 
  but I take ownership and responsibility for the claims/content/results. 
- I apologize in advance for any errors in my reporting. 
- Reference materials include
  * [IEEE 754-2019 specification](https://www.google.com/search?q=ieee+754-2019+pdf)
  * [IBM Cowlishaw GDAS General Decimal Arithmetic Specification 1.70](https://speleotrove.com/decimal/decarith.pdf)
  * [IBM Cowlishaw decTest validation suite](https://speleotrove.com/decimal/dectest.html)
  * [IBM Haifa FPgen/FPtest hardware decimal floating point validation suite](https://web.archive.org/web/20081006095103/http://www.haifa.il.ibm.com/projects/verification/fpgen/doc.html)
  * [Intel 'libbid' Decimal Floating Point library](https://www.intel.com/content/www/us/en/developer/articles/tool/intel-decimal-floating-point-math-library.html)
- The planned series shall include one installment per release candidate;
  the same harness each time, so readers can watch the type converge. 
- Correctness/compliance is graded against the standards. 
  Benchmark performance is simply reported, not graded; presumably performance may show
  improvement over release candidates, prior to GA. See sections 8 & 9. 

## 2. Executive Summary
- The numerical results produced by System.Numerics.Decimal128 are correct, 
  verified bit-for-bit against dectest, fptest, and libbid test vectors for
  tiesToEven rounding. **This is the hardest part to get right, and they nailed it**
- Rounding is separately composed, not fused into the operations. Directed rounding
  (Ceiling/Floor/Round) is applied *after* tiesToEven has already rounded, so results are
  double-rounded and *will produce incorrect results* with values very close to
  boundaries. Not compliant with IEEE 754. 
- Status flags are absent. Strictly speaking, not compliant with IEEE 754. 
- `ToString` does not ever use scientific notation. As a result, `ToString` is not
  quantum-preserving for strictly positive exponents. 
  For positive exponents (1E2) parse => format => parse
  will lose the exponent/cohort. This behavior is not compliant with
  IEEE 754 clause 5.12 (`ToString` is presumably a work-in-progress ... see below)
- `fusedMultiplyAdd` is absent — a required IEEE 754 operation. Not compliant
  with IEEE 754 clause 5.4.1.
- **Scorecard:** Correct results ✅ / IEEE 754 conformance ❌ — five clause-cited gaps:
  rounding (5.1), flags (5.2), string conversion (5.3), `fusedMultiplyAdd` (5.4), and
  `CompareTo` order (5.5, fix in progress) / Performance ⚠️.

## 3. Scope & Methodology
- **Version under test:** .NET 11 preview 7, SDK 11.0.100-preview.7.26366.102, daily build
  2026-07-16
- **Reference standards:** IEEE 754-2019 decimal128 + GDAS.
- **Verification suite:** Rosetta bit-identity against industry reference
  **Cowlishaw/IBM dectest, IBM fptest, and Intel libbid** test vector suites. 
- **Bit-bridge caveat:** net11preview7 exposes no way to read its bits, 
  no bitwise-equality operator, and `ToString` does not preserve cohort. 
  Therefore, the bit-identity check reaches the encoding by reinterpreting the value as its
  BID128 bit pattern (`Unsafe.BitCast`) and comparing through the port's BID codec. This is
  valid only because in-memory layout is the BID128 interchange
  encoding; that is an unsupported implementation detail, not an API contract. It also
  means cohort/quantum differences are caught, not just values. 
- **Comparison cohort:** net11preview7 `System.Numerics.Decimal128`, Intel libbid release 4, decimal128-csharp, `System.Decimal` (96-bit BCL baseline, flagged
  out-of-cohort on range ... does not support range of values/operations).
- **Benchmark harness:** op-benchmark .NET 11 arm, InProcess toolchain, per-op input
  categories.
- **Fairness caveats:** bitwiseEQ comparison of expected result values against only
  tiesToEven vectors ... since net11preview7 only offers tiesToEven. 
- **Reproducibility:** everything needed to rerun, so the series is auditable RC-over-RC.

## 4. What They Got Right
- **Correct results, verified** — the central, non-trivial achievement; bitwiseEQ match
  of expected value with three industry-standard test vector suites. 
  Cowlishaw/IBM decTest is part of the *decNumber* IEEE 754 decimal floating point reference implementation ... 8,574 tiesToEven cases pass, 0 fail. 
  IBM FPtest was part of the FPgen effort to validate System Z hardware implementation of
  decimal floating point ... 21,740 tiesToEven cases pass, 0 fail. 
  Intel libbid ships with test vectors ... 4,691 tiesToEven cases pass, 0 fail. 
- **tiesToEven as the default rounding-direction attribute, is the  correct, IEEE-consistent choice**
  Operators can't carry a rounding attribute; binding
  `+ − × ÷` to the standard default is clearly/exactly right. 
- Clean first-class BCL type and generic-math integration.
- BID over DPD is the defensible/obvious representation choice.

## 5. IEEE 754 Non-Compliance

The areas below are where net11preview7 does **not** conform to IEEE 754-2019, each anchored
to the clause it fails. Divergences the standard *permits*, or that are deliberate, are kept separate in section 6.

### 5.1 Rounding 

Rounding behavior is fundamental to the design of the IEEE 754 specifications. 
It is not something that was/is simply 'bolted on'. 

In this implementation arithmetic always rounds tiesToEven; `Ceiling`/`Floor`/`Round`
are separate functions applied *after* the operation has already rounded. 

This *double rounding* inevitably leads to incorrect results. 

**Example.** Ask for the quotient of two full-precision
decimals, rounded to an integer ties-away-from-zero:

```
a = 4999999999999999999999999999999999      (5x10^33 - 1)
b = 2000000000000000000000000000000000      (2x10^33)

exact a / b = 2.4999999999999999999999999999999995      <- 35 digits, not representable

  correct  - round the exact quotient once, ties-away   -> 2
  the API  - 1. divide: silently rounds to 34 digits, tiesToEven -> 2.5
             2. apply ties-away to 2.5                              -> 3
  result                                                            -> 3   (wrong)
```

The `.5` the user's rounding mode needed was already consumed by a tiesToEven step they
never asked for. The second rounding is handed `2.5` and has no way back to the true value.
**And the answer is 2.5 — an everyday magnitude.** What carries the 34 digits is the
*operands*; dividing two full-precision decimals is routine.

**When it occurs.** This *cannot* happen
to a value that fits in 34 digits — the operation would be exact and the rounding applied
to the true value. Full-width values can be produced as a result of previous multiplication
and division operations. It requires the exact result to overflow the format's precision.
That is
not exotic: it is simply what happens when you divide two full-precision decimals near a
rounding boundary. (Non-representability is *necessary*; proximity to a boundary within one
ULP is what makes it *occur* — so it's real but not constant.)

**The correct model** — the rounding-direction belongs *inside* the operation: round the
exact result **once**, to the requested mode. A post-hoc `Round`/`Floor`/`Ceiling` applied to
an already-tiesToEven-rounded value is structurally incapable of producing the
correctly-rounded answer. This same *compute-exact-then-round-once* core is exactly what a
correct `fusedMultiplyAdd` requires (section 5.4): a naive FMA built from their existing
multiply-then-add would round `a*b` *before* adding `c`, reproducing this very
double-rounding — which is why FMA's absence points at the same missing core, not a separate
problem.

**The conformance boundary (Now vs. Later).**
- IEEE 754-2019 **clause 4.3** states:
  ```
  Rounding takes a number regarded as infinitely precise and, if necessary, modifies it 
  to fit in the destination’s format while signaling the inexact exception, underflow, 
  or overflow when appropriate (see Clause 7). Except where stated otherwise, every 
  operation shall be performed as if it first produced an intermediate result correct
  to infinite precision and with unbounded range, and then rounded that result
  according to one of the attributes in this clause.
  ```
- To accomplish this, rounding must be performed **once**. The existing API rounds **twice**. 
- Consequence: under any non-default attribute — `roundTiesToAway`, `roundTowardPositive`,
  `roundTowardNegative`, `roundTowardZero` — decimal128 operations as exposed are **not
  correctly rounded**. The implementation conforms to IEEE 754 clause 5.1 for `roundTiesToEven` **only**.
- Microsoft can address this deficiency **Later** by providing additional library 
  entry points with roundingDirection as a passed parameter or receiver. 
- For **Now** Microsoft should not claim IEEE 754 rounding conformance with
  the current implementation; they should not present their two-step rounding
  as correctly-rounded. 

### 5.2 Flags
- No exception/status-flag support (inexact, invalid, overflow, underflow, division-by-zero).
- Flags are *required* under IEEE 754. 
- Admittedly, flags are a minor functional gap for the vast majority of users.
- The absence of flags is consistent with *binary* floating point (double/binary64).
- I would argue that flags are slightly more important for *decimal* floating point. 
- The bigger issue is, it contributes to concerns about the spec-conformance of the
  implementation. For a new implementation, flags (against known test vectors)
  provide a somewhat *independent verification channel* to confirm that results
  are being computed by the correct path.
- **The absence of flags is a direct contributor to the confidence cost (section 9).**
  Had flags been present they would have restored some confidence about the rounding issue.
  However, the complete absence of flags plants another *seed of doubt*.

### 5.3 No quantum-preserving string conversion (IEEE 754 clause 5.12)
IEEE 754-2019 **clause 5.12** requires, for decimal formats: *"All conversions from external
character sequences to supported decimal formats shall preserve the quantum … unless rounding is
necessary. At least one conversion from each supported decimal format shall preserve the quantum
as well as the value and sign."* Net11preview7 meets the parsing obligation, but fails the 
rendering side. 

- **Into the format (parse) — compliant.** `Parse` preserves the quantum: `Parse("1E+2")` stores
  coefficient 1 / exponent 2; `Parse("100")` stores coefficient 100 / exponent 0 — distinct
  cohort members with distinct bits. Compliance is confirmed by looking at the bits with 
  `Unsafe.BitCast` and confirming BID representation. 
- **Out of the format (render) — non-compliant.** No conversion from `Decimal128` to a string
  preserves the quantum for *all* values. It does for negative exponents (`1.0` and `1.00` format
  distinctly), but **every** path collapses positive-exponent cohorts: across 18 formatting paths
  — default, `G`, `G0…G34`, `R` (round-trip), `E`, `F`, `N`, and custom exponential forms — none
  distinguishes `1×10²` from `100×10⁰`. Consequently `Parse(x.ToString())` cannot recover `x`'s
  quantum for those values, and even `ToString("R")` — nominally the round-trip format — loses it.

  | value (distinct cohort members) | quantum-preserving string | every MSFT format |
  |---|---|---|
  | 1 × 10² | `1E+2` | `100` |
  | 100 × 10⁰ | `100` | `100` |

  Because clause 5.12 requires *at least one* quantum-preserving conversion from the format and
  there is none, net11preview7 is **not conformant with IEEE754 clause 5.12**.
- **Scope: the value is always correct — the failure is quantum-only.** The round-trip preserves
  the value across the entire range, including the qExp = 6111 extreme: a 6,112-character string
  parses back to the exact value (verified, and confirmed sensitive to a perturbed digit, so it
  is genuinely read, not clamped). No precision or overflow bug hides in the long-string case; it
  is strictly the cohort/quantum that is lost.
- **Aggravating factors.** `ToString` **never uses exponential notation** — confirmed across the
  entire exponent range, positive and negative. For example:
  - `Decimal128.MaxValue.ToString()` → **6,145 characters** (34 nines followed by 6,111 zeros)
  - `Decimal128.MinValue.ToString()` → **6,146 characters**
  - `Decimal128.Epsilon.ToString()` → **6,178 characters** (`0.` + 6,175 zeros + `1`)
  So `Console.WriteLine(Decimal128.MaxValue)` prints a 6,145-character line. Separately,
  `ToString("R")` (nominally the round-trip format) fails to round-trip the cohort, which is the
  sharpest surprise. 
- Presumably `ToString` is still under construction ... I doubt anyone wants to see
  `ToString` return a result with thousands of digits. 
- **Potential remedy.** For an accepted set of industry-standard rules, see GDAS 1.70,
  Conversions, p. 19 `to-scientific-string`, which introduces E-notation for positive
  exponents if the *adjusted exponent* (exponent + coefficient-length-1) falls below -6. 
- Until some cohort-preserving method exists (i.e. '1E+2' => BID => '1E+2')
  exists, the type cannot claim IEEE 754-2019 clause 5.12 conformance.

### 5.4 No `fusedMultiplyAdd` (IEEE 754 clause 5.4.1)
- **A required operation is missing.** `fusedMultiplyAdd` is a *required* general-computational
  operation under IEEE 754-2019 **clause 5.4.1** — not a convenience. Its absence is a conformance
  gap in its own right, parallel to the rounding gap in section 5.1.
- I acknowledge the presence of a `System.Numerics.Decimal128.MultiplyAddEstimate(Decimal128 left, Decimal128 right, Decimal128 addend)` whose name offers full disclosure
about the semantics. 
- **Remediation is additive → a "Later" (section 8.2).** Adding the FMA operation breaks
  no existing caller ... it can land in a future release.
- A correct FMA forms the *exact* product
  `a*b` and rounds **once** after adding `c`. Their multiply is already correctly-rounded, so
  they *can* form and round an exact wide product — the capability exists. Yet a correct FMA
  cannot be composed from their `multiply` then `add` (that rounds `a*b` first — the section 5.1
  double-rounding again); it needs the same general *compute-exact-then-round-once* core that
  correct directed rounding needs. FMA and directed rounding are one missing piece seen from
  two different angles (section 5.1).

### 5.5 No `totalOrder` (IEEE 754 clause 5.10)
- *A real conformance gap.* net11preview7 does not
  implement IEEE 754-2019 clause 5.10 `totalOrder` (which distinguishes ±0, orders NaNs, and
  separates cohort members).
- **In progress:** commits landing toward RC1 indicate the team is already working on
  `totalOrder`, so I expect to mark this *resolved* in the next installment.

## 6. Permitted & Intentional Divergences

Two divergences the Rosetta harness surfaced that are **not** non-compliance with the
IEEE 754 standard. The standard permits the first, and the second is a deliberate .NET 
convention. 

- **min/max cohort quantum differs from GDAS** — *IEEE-permitted, not a defect.* When
  `min`/`max` return one of two numerically-equal operands, the quantum (cohort member) chosen
  differs from GDAS's selection (GDAS 1.70 p32). IEEE 754 permits this latitude, so it's a
  documented behavioral divergence for interop awareness, nothing more. (I suspect that 
  this may relate to current relative weakness in the `compare` space)

- **Canonical NaN is negative** — *intentional; interop note only.* `Decimal128.NaN` is a
  negative quiet NaN (`0xFC00…`), **verified on preview 7** (SDK `11.0.100-preview.7.26366.102`). This seems to be consistent with .NET's long-standing NaN
  convention: `double.NaN` (`0xFFF8…`), `float.NaN` (`0xFFC00000`), and `Half.NaN` (`0xFE00`)
  are all negative. Fully IEEE-compliant.
  Noted here simply because most IEEE/C reference implementations use a *positive* canonical NaN
  (`0x7C00…`), so anyone performing bitWise comparison should know that Microsoft's default is
  negative.

## 7. Performance
- **7.1 The division problem** — the current divide is a naive algorithm; scaling operations
  pay for it.
- **7.2 The double hit** — The divide operation itself is slow,
  *then* trailing-zero stripping requires additional (slow) division operations, so
  division-heavy workloads are penalized heavily. (Shared root cause with section 5.1: the exact
  quotient is where both the correctness bug and the perf cost live.)
- **7.3 Four-by-four benchmarks** — per-op tables (`Decimal128` / libbid / decimal128-csharp / 
  `System.Decimal`) by input category, in operator order: add, sub, mul, div.

Generated from the op-benchmark store (ns/op, lower is better; each op shows two machines —
M3 Pro arm64, then i9-9880H x86_64). `decimal128-csharp` is
this reviewer's port; `Decimal128 (.NET 11)` is the type under review; libbid is the C
reference. `System.Decimal` (28 digits) is blank on any band its range cannot represent.

**Key to the `cat` column.** Each operation is partitioned into input categories that exercise
distinct internal paths, so a slow band is attributable to a specific kernel rather than averaged
away.

| cat | mnemonic | description |
|---|---|---|
| SQ | same qExp | add/sub, operands pre-aligned (Δ = 0); no shift. Fastest. |
| NQ | near qExp | add/sub, small align shift (Δ ≤ 4); result ≤ 34 digits, no rounding. |
| MQ | mid qExp | add/sub, larger align shift (Δ > 4); still no rounding. |
| OQ | overlap qExp | add/sub, align **and** round (`divPow10` over a coefficient that includes the smaller operand). The heaviest add/sub path. |
| FQ | far qExp | add/sub, smaller operand falls entirely below the kept 34 digits (swamped); sticky residue only. |
| CP | compact product | multiply, product ≤ 34 digits; no scaling. |
| WP | wide product | multiply, product 35–38 digits; 128-bit rescale. |
| XP | extra-wide product | multiply, product > 38 digits; 256-bit rescale. |
| CD | compact divisor | divide, divisor 1–4 digits (128÷64). |
| WD | wide divisor | divide, divisor 5–19 digits (256÷64). |
| XD | extra-wide divisor | divide, divisor 20–34 digits (256÷128, costliest). |
| ET | exact / terminating | divide, exact quotient — early-out then trailing-zero strip. |
| PT | power-of-ten divisor | divide by 10ᵏ; dedicated fast path that skips the divide kernel. |
| MIX | financial mix | add/sub, realistic financial operand stream (P-fin): log-uniform ≤ 19-digit operands, ~15/16 positive, ~75% sharing one currency-scale quantum (qExp ∈ {0, −2, −4, −6}); spans SQ/NQ rather than a single path. |

*Realistic financial mix (P-fin) — M3 Pro (arm64):*

<!-- BEGIN GENERATED net11-pfin-abs -->

| op | cat | Decimal128 (.NET 11) | libbid | decimal128-csharp | System.Decimal |
|---|---|---:|---:|---:|---:|
| add | MIX | 17.07 | 10.75 | 2.69 | 2.79 |
| sub | MIX | 17.14 | 13.35 | 3.15 | 3.00 |
| mul | CP | 11.12 | 23.54 | 1.77 | — |
| mul | WP | 47.54 | 32.43 | 23.87 | — |
| div | CD | 154.95 | 36.12 | 27.24 | 11.15 |
| div | WD | 181.82 | 39.16 | 41.73 | 26.96 |
| div | ET | 237.56 | 6.10 | 14.03 | 5.17 |
| div | PT | 242.05 | 6.10 | 5.30 | 12.53 |

<!-- END GENERATED net11-pfin-abs -->

*Realistic financial mix (P-fin) — i9-9880H (x86_64):*

<!-- BEGIN GENERATED net11-pfin-abs-x86 -->

| op | cat | Decimal128 (.NET 11) | libbid | decimal128-csharp | System.Decimal |
|---|---|---:|---:|---:|---:|
| add | MIX | 33.88 | 28.09 | 8.73 | 8.84 |
| sub | MIX | 37.11 | 29.12 | 12.92 | 10.74 |
| mul | CP | 39.88 | 44.34 | 5.81 | — |
| mul | WP | 125.92 | 58.84 | 46.74 | — |
| div | CD | 425.02 | 73.35 | 99.01 | 52.53 |
| div | WD | 473.24 | 79.45 | 117.28 | 101.76 |
| div | ET | 619.39 | 18.93 | 27.36 | 15.59 |
| div | PT | 629.83 | 18.69 | 11.93 | 59.05 |

<!-- END GENERATED net11-pfin-abs-x86 -->

*Add (P-gen) — M3 Pro (arm64):*

<!-- BEGIN GENERATED net11-add-abs -->

| op | cat | Decimal128 (.NET 11) | libbid | decimal128-csharp | System.Decimal |
|---|---|---:|---:|---:|---:|
| add | SQ | 19.82 | 8.44 | 6.02 | 2.52 |
| add | NQ | 18.97 | 9.37 | 4.91 | 4.15 |
| add | MQ | 19.64 | 8.94 | 15.97 | 3.99 |
| add | OQ | 143.67 | 14.26 | 39.53 | — |
| add | FQ | 1251.36 | 9.34 | 34.82 | — |

<!-- END GENERATED net11-add-abs -->

*Add (P-gen) — i9-9880H (x86_64):*

<!-- BEGIN GENERATED net11-add-abs-x86 -->

| op | cat | Decimal128 (.NET 11) | libbid | decimal128-csharp | System.Decimal |
|---|---|---:|---:|---:|---:|
| add | SQ | 61.70 | 30.49 | 15.32 | 11.86 |
| add | NQ | 65.57 | 32.84 | 17.57 | 16.64 |
| add | MQ | 65.65 | 31.94 | 42.15 | 17.36 |
| add | OQ | 340.59 | 49.07 | 82.23 | — |
| add | FQ | 3044.09 | 31.26 | 62.37 | — |

<!-- END GENERATED net11-add-abs-x86 -->

*Subtract (P-gen) — M3 Pro (arm64):*

<!-- BEGIN GENERATED net11-sub-abs -->

| op | cat | Decimal128 (.NET 11) | libbid | decimal128-csharp | System.Decimal |
|---|---|---:|---:|---:|---:|
| sub | SQ | 19.58 | 8.66 | 9.15 | 2.56 |
| sub | NQ | 19.09 | 9.93 | 5.78 | 4.15 |
| sub | MQ | 19.27 | 9.08 | 14.98 | 4.08 |
| sub | OQ | 143.85 | 14.91 | 39.88 | — |
| sub | FQ | 1251.64 | 10.50 | 33.74 | — |

<!-- END GENERATED net11-sub-abs -->

*Subtract (P-gen) — i9-9880H (x86_64):*

<!-- BEGIN GENERATED net11-sub-abs-x86 -->

| op | cat | Decimal128 (.NET 11) | libbid | decimal128-csharp | System.Decimal |
|---|---|---:|---:|---:|---:|
| sub | SQ | 62.10 | 35.60 | 18.83 | 11.48 |
| sub | NQ | 64.81 | 36.06 | 18.34 | 16.47 |
| sub | MQ | 66.56 | 34.36 | 41.39 | 15.64 |
| sub | OQ | 358.81 | 50.67 | 81.43 | — |
| sub | FQ | 3094.16 | 33.98 | 64.33 | — |

<!-- END GENERATED net11-sub-abs-x86 -->

*Multiply (P-gen) — M3 Pro (arm64):*

<!-- BEGIN GENERATED net11-mul-abs -->

| op | cat | Decimal128 (.NET 11) | libbid | decimal128-csharp | System.Decimal |
|---|---|---:|---:|---:|---:|
| mul | CP | 10.95 | 22.98 | 2.18 | — |
| mul | WP | 54.22 | 33.15 | 22.83 | — |
| mul | XP | 1222.02 | 42.97 | 52.39 | — |

<!-- END GENERATED net11-mul-abs -->

*Multiply (P-gen) — i9-9880H (x86_64):*

<!-- BEGIN GENERATED net11-mul-abs-x86 -->

| op | cat | Decimal128 (.NET 11) | libbid | decimal128-csharp | System.Decimal |
|---|---|---:|---:|---:|---:|
| mul | CP | 37.33 | 46.30 | 7.38 | — |
| mul | WP | 121.90 | 64.78 | 51.32 | — |
| mul | XP | 2968.36 | 93.04 | 82.92 | — |

<!-- END GENERATED net11-mul-abs-x86 -->

*Divide (P-gen) — M3 Pro (arm64):*

<!-- BEGIN GENERATED net11-div-abs -->

| op | cat | Decimal128 (.NET 11) | libbid | decimal128-csharp | System.Decimal |
|---|---|---:|---:|---:|---:|
| div | CD | 113.46 | 37.45 | 29.45 | — |
| div | WD | 158.00 | 37.57 | 47.00 | — |
| div | XD | 561.63 | 39.17 | 49.02 | — |
| div | ET | 153.02 | 11.67 | 19.14 | — |
| div | PT | 151.10 | 11.43 | 11.67 | — |

<!-- END GENERATED net11-div-abs -->

*Divide (P-gen) — i9-9880H (x86_64):*

<!-- BEGIN GENERATED net11-div-abs-x86 -->

| op | cat | Decimal128 (.NET 11) | libbid | decimal128-csharp | System.Decimal |
|---|---|---:|---:|---:|---:|
| div | CD | 361.56 | 80.72 | 101.57 | — |
| div | WD | 428.13 | 80.21 | 110.76 | — |
| div | XD | 1160.87 | 81.28 | 112.82 | — |
| div | ET | 516.67 | 29.08 | 52.27 | — |
| div | PT | 501.95 | 29.57 | 11.28 | — |

<!-- END GENERATED net11-div-abs-x86 -->

- **7.4 Interpretation** - Intel libbid is written in C, the other 3 are implemented
  in C#. System.Decimal is not equivalent. 96-bits vs 128-bits. 28 digits vs 34 digits. No
  scaled exponent. No special values. We would expect System.Decimal to be very fast because
  it is not offering equivalent functionality. 

## 8. Recommendations

### 8.1 Now — before GA
- **State the truth regarding Rounding:** correctly-rounded operations are TTE-only;
  do not claim IEEE 754 rounding conformance beyond `roundTiesToEven`; do not present
  composed directed rounding as correctly-rounded (section 5.1).
- **Fix `ToString` to properly retain cohorts for round-trips:** no output conversion
  preserves the quantum, so `ToString` is not IEEE 754 clause 5.12-conformant. 
  Presumably this is in-the-works because nobody wants huge strings of digits. 
- I trust that the implementation team has a long list of things they would like to
  get into this release. 

### 8.2 Later — after GA (additive, non-breaking)
- **Add fused rounding-direction operations:** alternate methods taking an explicit
  `roundingDirection`, rounding the exact result once. Use a true rounding-direction type,
  not `MidpointRounding` (section 5.1). Consider making RoundingDirection the receiver ...
  `RoundingDirection.add()`, `RoundingDirection.subtract()`
- **Replace the naive division algorithm;** make scaling and trailing-zero stripping fast (section 7).
- Broader performance tuning across op categories.
- Full flag semantics, including the status-flag surface.
- Rationale: purely additive; no reason to gate GA on them, safe to iterate across the series.

## 9. Conclusion
They got the math right ... a solid start. 
  
**The confidence cost.** Reputational exposure (Rounding section 5.1) is the visible risk.
The quieter
risk is inferential: correctly-rounded single rounding is the foundation of the standard, not a
fine point, so exposing directed rounding as a second pass over an already-rounded value raises a
fair question about how completely Microsoft understands the problem space. 

The confidence cost is also **cumulative, not a single data point**. The absence of flags
(section 5.2) compounds the others directly: it removes one of the independent channels that would
let an outside evaluator confirm results were computed correctly, so the very evidence that could
*restore* confidence after the rounding finding is not present. The sharpest
corroboration is structural: the un-exposed directed rounding (section 5.1) and the absent
`fusedMultiplyAdd` (section 5.4) are **two required-operation gaps, reached from different angles,
that resolve to a single architectural cause** — the apparent absence of a general
*compute-exact-then-round-once* core. That absence starts to smell like a design flaw rather than
an isolated slip.

- What I'll be watching for in the next RC ... ToString, TotalCompare, data type conversions,
FMA, division/scaling performance. 

