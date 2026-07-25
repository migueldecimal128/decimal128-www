---
layout: default
permalink: /reviews/dotnet/net11-preview7.html
title: "System.Numerics.Decimal128 (.NET 11 Preview 7): An Independent Review — Decimal128"
description: "An independent, standards-anchored review of Microsoft's System.Numerics.Decimal128 as of .NET 11 preview 7 — verified numerically correct, with findings on rounding (double-rounding), status flags, division performance, and BID encapsulation."
heading: "System.Numerics.Decimal128 — .NET 11 Preview 7"
---

<div class="whitepaper" markdown="1">

*First in a series — one report per release candidate through GA*

> **Author stance:** independent, self-appointed decimal128 specialist. Not affiliated
> with the .NET team. Findings are anchored to IEEE 754-2019 and GDAS (Cowlishaw) and
> cross-checked with an independent conformant implementation (d128) plus libbid.

---

## 1. Framing
- I am an independent decimal128 specialist. 
  I have no affiliation with the .NET team. 
  I don't know anyone on the .NET team.
  I maintain my own conformant implementation (decimal128-csharp) and a 
  cross-checking (Rosetta) suite that
  consolidates 60k IEEE 754 decimal128 test vectors in three different text formats from IBM and Intel. Rosetta parses the text formats in their original form, calls the appropriate operation for the implementation under test, and compares bit-wise conformance of the expected result. 
- This document, Rosetta, and the benchmark harness are written with
  the assistance of Anthropic Claude AI, 
  but I take ownership and responsibility for the claims/content/results. 
- Reference materials include
  * IEEE 754-2019 specification
  * the Cowlishaw GDAS General Decimal Arithmetic Specification
  * IBM Cowlishaw decTest validation suite
  * IBM Haifa FPgen/FPtest hardware decimal floating point validation suite
  * Intel 'libbid' Decimal Floating Point library 
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
  double-rounded and *will produce incorrect results* very close to boundaries. Not
  compliant with IEEE 754. 
- Status flags are absent. Strictly speaking, not compliant with IEEE 754. 
- `ToString` conversion is currently not quantum-preserving for strictly
  positive exponents. For positive exponents (1E2) parse => format => parse
  will lose the exponent/cohort. Not compliant with
  IEEE 754 clause 5.12, which requires at least one quantum-preserving output conversion. (`ToString` is clearly a work-in-progress ... see below)
- `fusedMultiplyAdd` is absent — a required IEEE 754 operation. Not compliant
  with IEEE 754 clause 5.4.1.
- BID is well-hidden today; the representation is not exposed by the current
  API. The risk is the DPD conversion they plan to add: if BID is surfaced 
  there as the native value rather than as a peer interchange format, 
  the option of changing the internal representation 
  in the future would require a breaking change. Exposure of BID as anything
  other than a peer of DPD is effectively BID lock-in.
- **Scorecard:** Correct results ✅ / IEEE 754 conformance ❌ — five clause-cited gaps:
  rounding (5.1), flags (5.2), string conversion (5.3), `fusedMultiplyAdd` (5.4), and
  `CompareTo` order (5.5, fix in progress) / Performance ⚠️ / Design — BID lock-in ⚠️.

## 3. Scope & Methodology
- **Version under test:** .NET 11 preview 7, SDK 11.0.100-preview.7.26366.102 as of 2026-07-14
- **Reference standards:** IEEE 754-2019 decimal128 + GDAS.
- **Verification suite:** Rosetta bit-identity against industry reference
  **dectest, fptest, and libbid** test vector suites. 
- **Bit-bridge caveat:** the SUT exposes no way to read its bits and no bitwise-equality
  operator, so the bit-identity check reaches the encoding by reinterpreting the value as its
  BID128 bit pattern (`Unsafe.BitCast`) and comparing through the port's BID codec. This is
  valid only because — and only while — the SUT's in-memory layout *is* the BID128 interchange
  encoding; that is an unsupported implementation detail, not an API contract (see section 7). It also
  means cohort/quantum differences are caught, not just values. 
- **Comparison cohort:** `System.Numerics.Decimal128` (the *system under test*, SUT), Intel libbid release 4, decimal128-csharp, `System.Decimal` (96-bit BCL baseline, flagged
  out-of-cohort on range).
- **Benchmark harness:** op-benchmark .NET 11 arm, InProcess toolchain, per-op input
  categories.
- **Fairness caveats:** bit-for-bit comparison of expected result values against only
  tiesToEven vectors since the SUT only offers tiesToEven. 
- **Reproducibility:** everything needed to rerun, so the series is auditable RC-over-RC.

## 4. What They Got Right
- **Correct results, verified** — the central, non-trivial achievement; walk through the
  suite agreement (dectest / fptest / libbid).
- **tiesToEven as the default rounding-direction attribute, is the  correct, IEEE-consistent choice**
  Operators can't carry a rounding attribute; binding
  `+ − × ÷` to the standard default is clearly/exactly right. 
- Clean first-class BCL type and generic-math integration.
- BID over DPD is the defensible/obvious representation choice. However, it does not
  need to be the assume/preferred representation visible through the API. 

## 5. IEEE 754 Non-Compliance

The areas below are where preview 7 does **not** conform to IEEE 754-2019, each anchored to the
clause it fails. Divergences the standard *permits*, or that are deliberate, are kept separate in
section 6.

### 5.1 Rounding 

Rounding behavior is fundamental to the design of the IEEE 754 specifications. 
It is not something that was/is simply 'bolted on' ... because if you try to
add it on later then you will get incorrect results. 

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
*operands*; dividing two full-precision decimals is completely routine.

**When it occurs.** This *cannot* happen
to a value that fits in 34 digits — the operation would be exact and the rounding applied
to the true value. It requires the exact result to overflow the format's precision. That is
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
- Microsoft could address this deficiency **Later** by providing additional library 
  entry points with roundingDirection as a passed parameter or receiver. 
- For **Now** Microsoft should not claim IEEE 754 rounding conformance with
  the current implementation; they should not present their two-step rounding
  as correctly-rounded. 

### 5.2 Flags
- No exception/status-flag support (inexact, invalid, overflow, underflow, division-by-zero).
- Flags are *required* under IEEE 754.
- Admittedly, flags are a minor functional gap for the vast majority of users.
- The absence of flags is consistent with binary floating point (double/binary64).
- The bigger issue is, it contributes to concerns about the spec-conformance of the
  implementation. For a new implementation, flags (against known test vectors)
  provide an *independent verification channel* to confirm that results are being computed by
  the correct path.
- **The absence of flags is a direct contributor to the confidence cost of section 5.6.**
  Had they been present they would have restored some confidence about the rounding issue.
  However, the absence of flags plants another *seed of doubt*.

### 5.3 No quantum-preserving string conversion (IEEE 754 clause 5.12)
IEEE 754-2019 **clause 5.12** requires, for decimal formats: *"All conversions from external
character sequences to supported decimal formats shall preserve the quantum … unless rounding is
necessary. At least one conversion from each supported decimal format shall preserve the quantum
as well as the value and sign."* Two obligations — one for parsing, one for formatting. The SUT
meets the first and fails the second.

- **Into the format (parse) — compliant.** `Parse` preserves the quantum: `Parse("1E+2")` stores
  coefficient 1 / exponent 2; `Parse("100")` stores coefficient 100 / exponent 0 — distinct
  cohort members with distinct bits. Compliance is confirmed by looking at the bits with 
  `Unsafe.BitCast`. 
- **Out of the format (format) — non-compliant.** No conversion from `Decimal128` to a string
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
  there is none, the SUT is **not conformant with clause 5.12** — an explicit IEEE 754
  non-compliance, not a GDAS style preference.
- **Scope: the value is always correct — the failure is quantum-only.** The round-trip preserves
  the value across the entire range, including the qExp = 6111 extreme: a 6,112-character string
  parses back to the exact value (verified, and confirmed sensitive to a perturbed digit, so it
  is genuinely read, not clamped). No precision or overflow bug hides in the long-string case; it
  is strictly the cohort/quantum that is lost.
- **Aggravating factors.** `ToString` **never uses exponential notation** — confirmed across the
  entire exponent range, positive and negative — whereas GDAS `to-scientific-string` (GDAS 1.7,
  *Conversions*, p. 19) introduces E-notation once the exponent is positive or the *adjusted*
  exponent (exponent + coefficient-length − 1) falls below −6. So toward decimal128's magnitude
  limits it emits
  enormous strings where the canonical form emits ~40. These are not contrived literals; they are
  what the type's own constants print:
  - `Decimal128.MaxValue.ToString()` → **6,145 characters** (34 nines followed by 6,111 zeros)
  - `Decimal128.MinValue.ToString()` → **6,146 characters**
  - `Decimal128.Epsilon.ToString()` → **6,178 characters** (`0.` + 6,175 zeros + `1`)

  So `Console.WriteLine(Decimal128.MaxValue)` prints a 6,145-character line. Separately,
  `ToString("R")` — nominally the round-trip format — failing to round-trip the cohort is, on its
  own, a bug.
- Presumably `ToString` is still under construction ... I doubt anyone wants to see
  `ToString` return a result with thousands of digits. 
- For an accepted set of industry-standard rules, see GDAS 1.7,
  Conversions, p. 19 `to-scientific-string`
- Until some cohort-preserving method exists (i.e. '1E+2' => BID => '1E+2')
  exists, the type cannot claim IEEE 754-2019 clause 5.12 conformance.

### 5.4 No `fusedMultiplyAdd` (IEEE 754 clause 5.4.1)
- **A required operation is missing.** `fusedMultiplyAdd` is a *required* general-computational
  operation under IEEE 754-2019 **clause 5.4.1** — not a convenience. Its absence is a conformance
  gap in its own right, parallel to the rounding gap in section 5.1.
- I acknowledge the presence of a `System.Numerics.Decimal128.MultiplyAddEstimate(Decimal128 left, Decimal128 right, Decimal128 addend)` which offers full disclosure
about the semantics. 
- **Remediation is additive → a "Later" (section 9.2).** Adding the op breaks no existing caller;
  it can land in a future release.
- A correct FMA forms the *exact* product
  `a*b` and rounds **once** after adding `c`. Their multiply is already correctly-rounded, so
  they *can* form and round an exact wide product — the capability exists. Yet a correct FMA
  cannot be composed from their `multiply` then `add` (that rounds `a*b` first — the section 5.1
  double-rounding again); it needs the same general *compute-exact-then-round-once* core that
  correct directed rounding needs. FMA and directed rounding are one missing piece seen from
  two different angles (section 5.1).

### 5.5 `CompareTo` is value-order, not `totalOrder` (IEEE 754 clause 5.10)
- *A real conformance gap.* As of preview 7, `CompareTo` orders by numeric value; it does not
  implement IEEE 754-2019 clause 5.10 `totalOrder` (which distinguishes ±0, orders NaNs, and
  separates cohort members).
- **In progress:** commits landing toward RC1 indicate the team is already working on
  `totalOrder`, so I expect to mark this *resolved* in the next installment.

### 5.6 Erodes confidence

Reputational exposure (section 5.1) is the visible risk.
The quieter risk is inferential: correctly-rounded single rounding is the foundation of the
standard, not a fine point, so exposing directed rounding as a second pass over an
already-rounded value raises a fair question about how completely Microsoft understands
the problem space.

A careful evaluator cannot contain that question to the rounding path alone — if
a load-bearing invariant was missed here, confidence in the un-audited surface has to be
discounted too. To be clear about scope: the numerical core is *verified correct*, so this
reads as an API-design gap rather than an engine defect. But it is precisely why independent,
standards-anchored verification is warranted, and why this series revisits each release
rather than taking the surface at face value.

The confidence cost is also **cumulative, not a single data point** — this section is a cluster
of clause-cited failures, not one slip. The absence of flags (section 5.2) compounds the others
directly: it removes one of the independent channels that would let an outside evaluator confirm
results were computed correctly, so the very evidence that could *restore* confidence after the
rounding finding is the evidence that isn't there. The sharpest corroboration is structural: the
un-exposed directed rounding (section 5.1) and the absent `fusedMultiplyAdd` (section 5.4) are
**two required-operation gaps, reached from different angles, that resolve to a single
architectural cause** — the apparent absence of a general *compute-exact-then-round-once*
core. That absence starts to smell like a design flaw rather than an isolated slip. 

## 6. Permitted & Intentional Divergences

Two divergences the Rosetta harness surfaced that are **not** non-compliance with the
IEEE 754 standard. The standard permits the first, and the second is a deliberate .NET 
convention. 

- **min/max cohort quantum differs from GDAS** — *IEEE-permitted, not a defect.* When
  `min`/`max` return one of two numerically-equal operands, the quantum (cohort member) chosen
  differs from GDAS's selection (GDAS 1.7 p32). IEEE 754 permits this latitude, so it's a
  documented behavioral divergence for interop awareness, nothing more. (I suspect that 
  this may relate to current relative weakness in the `compare` space)

- **Canonical NaN is negative** — *intentional; interop note only.* `Decimal128.NaN` is a
  negative quiet NaN (`0xFC00…`), **verified on preview 7** (SDK `11.0.100-preview.7.26366.102`). This seems to be consistent with .NET's long-standing NaN
  convention: `double.NaN` (`0xFFF8…`), `float.NaN` (`0xFFC00000`), and `Half.NaN` (`0xFE00`)
  are all negative. Fully IEEE-compliant.
  Noted here simply because most IEEE/C reference implementations use a *positive* canonical NaN
  (`0x7C00…`), so anyone performing bitWise comparison should know that Microsoft's default is
  negative.

## 7. Design: The BID Lock-In Question
- **7.1 BID internally is the right call — and confirmed.** The type stores BID: reflection
  shows two private `UInt64` words plus a non-public combination-field encoder, and the team
  has said the implementation is based on BID and libbid (*per public github comments*).
  BID over DPD is the defensible choice for a software implementation. 
- **7.2 Today the representation is fully hidden — there is nothing leaking yet.** Preview 7
  exposes *no* way to see or construct from the raw bits: no `GetBits`/`UInt128` accessor, no
  constructor from bits, no binary interchange at all — the only I/O is string parse/format
  (verified against the preview 7 SDK). The BID encoding is genuinely encapsulated. It stays
  observable only the way any blittable struct's memory is (`MemoryMarshal` over its 16 bytes),
  which is a property of all CLR value types, not an API decision.
- **7.3 The concern is the interchange surface they are about to add.** The team has implied
  it will offer conversion from DPD. That is exactly when the
  representation can begin to leak — and "conversion *from* DPD" hints at the asymmetry to
  avoid: DPD treated as a foreign import while BID is exposed as the native value. 
  (My hunch is that in 2026 there is more DPD128 than BID128 data in the world)
- **7.4 The recommendation — symmetric interchange, decided now.** Treat BID and DPD as *peer*
  interchange formats: an explicit **decode** inbound and **encode** outbound for *both*, with
  neither surfaced as "the raw value." Keep BID internally if you like, but explicitly
  encode/decode through that API boundary, so the internal representation can change later
  without breaking callers. This surface is being designed right now, so getting the symmetry
  right should be nearly free; retrofitting it after GA is a breaking change ... and in
  practice it will probably never change. 

## 8. Performance
- **8.1 The division problem** — the current divide is a naive algorithm; scaling operations
  pay for it.
- **8.2 The double hit** — The divide operation itself is slow,
  *then* trailing-zero stripping requires additional (slow) division operations, so
  division-heavy workloads are penalized heavily. (Shared root cause with section 5.1: the exact
  quotient is where both the correctness bug and the perf cost live.)
- **8.3 Four-by-four benchmarks** — per-op tables (`Decimal128` / libbid / decimal128-csharp / 
  `System.Decimal`) by input category, in operator order: add, sub, mul, div.

Generated from the op-benchmark store (ns/op, lower is better; each op shows two machines —
M3 Pro arm64, then i9-9880H x86_64). `decimal128-csharp` is
this reviewer's port; `Decimal128 (.NET 11)` is the type under review; libbid is the C
reference. `System.Decimal` (28 digits) is blank on any band its range cannot represent.

*Realistic financial mix (P-fin) — M3 Pro (arm64):*

<!-- BEGIN GENERATED net11-pfin-abs -->

| op | cat | Decimal128 (.NET 11) | libbid | decimal128-csharp | System.Decimal |
|---|---|---:|---:|---:|---:|
| add | MIX | 16.77 | 11.09 | 2.66 | 2.86 |
| sub | MIX | 17.36 | 11.65 | 3.21 | 2.96 |
| mul | CP | 11.01 | 23.54 | 1.87 | — |
| mul | WP | 51.33 | 32.10 | 23.86 | — |
| div | CD | 151.29 | 37.72 | 26.08 | 11.16 |
| div | WD | 188.46 | 39.06 | 45.99 | 27.22 |
| div | ET | 235.56 | 5.96 | 14.15 | 5.16 |
| div | PT | 240.20 | 6.06 | 5.22 | 12.34 |

<!-- END GENERATED net11-pfin-abs -->

*Realistic financial mix (P-fin) — i9-9880H (x86_64):*

<!-- BEGIN GENERATED net11-pfin-abs-x86 -->

| op | cat | Decimal128 (.NET 11) | libbid | decimal128-csharp | System.Decimal |
|---|---|---:|---:|---:|---:|
| add | MIX | 34.24 | 32.11 | 9.23 | 9.21 |
| sub | MIX | 38.10 | 36.74 | 12.81 | 10.99 |
| mul | CP | 39.19 | 46.14 | 5.89 | — |
| mul | WP | 150.39 | 60.57 | 44.00 | — |
| div | CD | 427.92 | 78.27 | 100.36 | 53.57 |
| div | WD | 476.74 | 82.95 | 115.88 | 102.94 |
| div | ET | 620.41 | 19.44 | 27.94 | 14.45 |
| div | PT | 626.14 | 19.26 | 13.45 | 59.99 |

<!-- END GENERATED net11-pfin-abs-x86 -->

*Add (P-gen) — M3 Pro (arm64):*

<!-- BEGIN GENERATED net11-add-abs -->

| op | cat | Decimal128 (.NET 11) | libbid | decimal128-csharp | System.Decimal |
|---|---|---:|---:|---:|---:|
| add | SQ | 19.35 | 8.63 | 5.97 | 2.49 |
| add | NQ | 19.49 | 8.34 | 4.92 | 4.11 |
| add | MQ | 20.15 | 8.63 | 15.76 | 4.18 |
| add | OQ | 142.85 | 13.40 | 39.40 | — |
| add | FQ | 1245.45 | 9.21 | 34.98 | — |

<!-- END GENERATED net11-add-abs -->

*Add (P-gen) — i9-9880H (x86_64):*

<!-- BEGIN GENERATED net11-add-abs-x86 -->

| op | cat | Decimal128 (.NET 11) | libbid | decimal128-csharp | System.Decimal |
|---|---|---:|---:|---:|---:|
| add | SQ | 64.42 | 30.55 | 16.85 | 11.85 |
| add | NQ | 67.34 | 32.21 | 16.65 | 16.67 |
| add | MQ | 67.92 | 31.68 | 42.58 | 17.57 |
| add | OQ | 353.25 | 47.35 | 84.60 | — |
| add | FQ | 3162.13 | 30.07 | 65.20 | — |

<!-- END GENERATED net11-add-abs-x86 -->

*Subtract (P-gen) — M3 Pro (arm64):*

<!-- BEGIN GENERATED net11-sub-abs -->

| op | cat | Decimal128 (.NET 11) | libbid | decimal128-csharp | System.Decimal |
|---|---|---:|---:|---:|---:|
| sub | SQ | 19.50 | 9.06 | 9.06 | 2.66 |
| sub | NQ | 19.21 | 10.86 | 5.83 | 4.16 |
| sub | MQ | 19.17 | 8.85 | 14.81 | 4.11 |
| sub | OQ | 142.13 | 16.89 | 39.87 | — |
| sub | FQ | 1244.61 | 10.25 | 32.31 | — |

<!-- END GENERATED net11-sub-abs -->

*Subtract (P-gen) — i9-9880H (x86_64):*

<!-- BEGIN GENERATED net11-sub-abs-x86 -->

| op | cat | Decimal128 (.NET 11) | libbid | decimal128-csharp | System.Decimal |
|---|---|---:|---:|---:|---:|
| sub | SQ | 64.83 | 35.44 | 19.32 | 12.03 |
| sub | NQ | 66.44 | 37.04 | 19.00 | 16.70 |
| sub | MQ | 68.44 | 35.97 | 41.83 | 16.02 |
| sub | OQ | 356.31 | 51.86 | 85.34 | — |
| sub | FQ | 3150.05 | 34.95 | 63.64 | — |

<!-- END GENERATED net11-sub-abs-x86 -->

*Multiply (P-gen) — M3 Pro (arm64):*

<!-- BEGIN GENERATED net11-mul-abs -->

| op | cat | Decimal128 (.NET 11) | libbid | decimal128-csharp | System.Decimal |
|---|---|---:|---:|---:|---:|
| mul | CP | 10.93 | 23.10 | 2.24 | — |
| mul | WP | 47.85 | 33.19 | 22.03 | — |
| mul | XP | 1217.57 | 42.29 | 50.99 | — |

<!-- END GENERATED net11-mul-abs -->

*Multiply (P-gen) — i9-9880H (x86_64):*

<!-- BEGIN GENERATED net11-mul-abs-x86 -->

| op | cat | Decimal128 (.NET 11) | libbid | decimal128-csharp | System.Decimal |
|---|---|---:|---:|---:|---:|
| mul | CP | 41.41 | 46.33 | 7.59 | — |
| mul | WP | 130.07 | 67.28 | 52.80 | — |
| mul | XP | 2986.32 | 95.35 | 84.97 | — |

<!-- END GENERATED net11-mul-abs-x86 -->

*Divide (P-gen) — M3 Pro (arm64):*

<!-- BEGIN GENERATED net11-div-abs -->

| op | cat | Decimal128 (.NET 11) | libbid | decimal128-csharp | System.Decimal |
|---|---|---:|---:|---:|---:|
| div | CD | 118.44 | 36.52 | 29.33 | — |
| div | WD | 157.80 | 37.53 | 48.07 | — |
| div | XD | 560.19 | 39.01 | 48.34 | — |
| div | ET | 152.48 | 10.87 | 19.17 | — |
| div | PT | 148.50 | 10.76 | 10.98 | — |

<!-- END GENERATED net11-div-abs -->

*Divide (P-gen) — i9-9880H (x86_64):*

<!-- BEGIN GENERATED net11-div-abs-x86 -->

| op | cat | Decimal128 (.NET 11) | libbid | decimal128-csharp | System.Decimal |
|---|---|---:|---:|---:|---:|
| div | CD | 379.53 | 82.56 | 104.79 | — |
| div | WD | 442.40 | 87.22 | 116.41 | — |
| div | XD | 1189.40 | 86.84 | 115.59 | — |
| div | ET | 540.04 | 30.95 | 52.30 | — |
| div | PT | 525.23 | 31.12 | 11.85 | — |

<!-- END GENERATED net11-div-abs-x86 -->

- **8.4 Interpretation** — where the gap is algorithmic vs. JIT/runtime; call out
  `System.Decimal`'s 96-bit range difference so it isn't read as like-for-like. And note the
  tell: the SUT stores BID internally — verified here by decoding its bits — and the team has
  said it is based on libbid (per public github comments), yet Decimal128 runs 3–30× slower than
  libbid across these bands. The gap is therefore the managed reimplementation, not the BID
  approach — their own reference is the fast one.
- **8.5 The stakes** — a slow first release reinforces the myth that *software* decimal
  floating point is inherently slow. It isn't; d128 and libbid show the headroom — and libbid
  is the very reference their implementation is based on. This is the narrative cost of
  shipping performance-last.
- **8.6 Why this is a "Later"** — every number here is improvable in a future release without
  breaking a single caller.
- **8.7 Series baseline** — these are the numbers the next RC is measured against.

## 9. Recommendations

### 9.1 Now — before GA
- **State the truth regarding Rounding:** correctly-rounded operations are TTE-only;
  do not claim IEEE 754 rounding conformance beyond `roundTiesToEven`; do not present
  composed directed rounding as correctly-rounded (section 5.1).
- **Fix `ToString` to properly retain cohorts for round-trips:** no output conversion
  preserves the quantum, so `ToString` is not IEEE 754 clause 5.12-conformant. 
  Presumably this is in-the-works because nobody wants huge strings of digits. 
- **Settle the interchange API** so BID/DPD are treated symmetrically and the
  internal representation remains hidden. It will keep the door open for options in
  the future. 
- **Reserve the flag surface** so the verification channel and future semantics aren't
  foreclosed (section 5.2).
- Rationale: these are semantic and API contracts, plus disclosure — cheap now, breaking or
  reputation-damaging after GA.

### 9.2 Later — after GA (additive, non-breaking)
- **Add fused rounding-direction operations:** alternate methods taking an explicit
  `roundingDirection`, rounding the exact result once. Use a true rounding-direction type,
  not `MidpointRounding` (section 5.1). Consider making RoundingDirection the receiver ...
  `RoundingDirection.add()`, `RoundingDirection.subtract()`
- **Implement `fusedMultiplyAdd` (clause 5.4.1):** the required fused op (section 5.4). It almost certainly
  shares the same *compute-exact-then-round-once* finalize as the fused rounding-direction
  methods above, so the two are natural to build together.
- **Add a quantum-preserving string conversion** (GDAS `to-scientific-string`) — a new format
  specifier or method that round-trips the cohort (section 5.3). Closes the clause 5.12 gap;
  non-breaking, so the familiar default can stay.
- **Replace the naive division algorithm;** make scaling and trailing-zero stripping fast (section 8).
- Broader performance tuning across op categories.
- Full flag semantics behind the (Now-reserved) surface.
- Rationale: purely additive; no reason to gate GA on them, safe to iterate across the series.

> **Judgment call (not a "Now"):** even though the fused rounding API is additive, there is a
> reputational case for MS *choosing* to ship it at GA so the correct path exists from day
> one. Their call to make — phrased as a recommendation, not a requirement.

## 10. Conclusion
- They got the math right — the foundation is sound. What remains is making rounding *fused*
  before the composed pattern hardens into an assumed contract, being honest about the
  conformance boundary, and not letting a slow first release define the ceiling for software
  decimal.
- Callback to the through-line: the open items are less about any single wrong answer than
  about how much of the un-audited surface has earned trust — which is what the series exists
  to keep testing.
- What I'll be watching for in the next RC (fused rounding-direction ops; the scorecard 1/5
  climbing; division/scaling perf; any flag surface).

## 11. Appendices
- **A. Rounding worked example** — the ties-away vs. TTE divergence (the ~2.5 case), plus the
  necessary-condition note (why a value that fits in 34 digits can never trigger it).
- **B. Full per-op benchmark tables** — raw ns/op from the op-benchmark store.

*FMA — M3 Pro (arm64). `Decimal128` and `System.Decimal` are blank because neither has a fused
multiply-add; this corroborates section 5.4.*

<!-- BEGIN GENERATED net11-fma-abs -->

| op | cat | Decimal128 (.NET 11) | libbid | decimal128-csharp | System.Decimal |
|---|---|---:|---:|---:|---:|
| fma | FN | — | 84.00 | 107.51 | — |
| fma | FF | — | 57.07 | 83.93 | — |

<!-- END GENERATED net11-fma-abs -->

*FMA — i9-9880H (x86_64):*

<!-- BEGIN GENERATED net11-fma-abs-x86 -->

| op | cat | Decimal128 (.NET 11) | libbid | decimal128-csharp | System.Decimal |
|---|---|---:|---:|---:|---:|
| fma | FN | — | 160.41 | 187.99 | — |
| fma | FF | — | 123.46 | 146.06 | — |

<!-- END GENERATED net11-fma-abs-x86 -->

- **C. Verification methodology** — vector sources (dectest / fptest / libbid), counts, and
  any skip/divergence list.
- **D. Environment & reproduction** — SDK versions, toolchain flags, machine/arch.

</div>
