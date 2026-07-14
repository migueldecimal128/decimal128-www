---
layout: default
permalink: /whitepapers/conformance-evidence.html
title: "Three Scripts, One Truth: Conformance Evidence — Decimal128"
description: "The provenance and validity of decimal128's conformance evidence — how three independent test corpora, plus a fourth gap-filling suite, reconcile bit-for-bit across eight language implementations."
heading: "Three Scripts, One Truth"
---

### The provenance and validity of decimal128's conformance evidence

*How do you know a decimal arithmetic library is correct? Not by trusting its
author. You know it the way the Rosetta Stone was decoded: by taking the same
statement, written independently in different scripts by parties who never
coordinated, and confirming they agree. decimal128 is checked against three such
scripts — from IBM's software-decimal lineage, IBM's hardware-verification
lineage, and Intel's implementation lineage — plus a fourth suite written to
cover what the first three do not. Over fifty thousand test vectors reconcile to
one answer, bit for bit, in eight independent language implementations.*

---

## 1. The problem with "trust me"

Decimal floating-point is the arithmetic of money, tax, billing, and
measurement — domains where "close enough" is a defect, not a rounding
convenience. IEEE 754-2008 standardized three decimal formats (`decimal32`,
`decimal64`, `decimal128`); the 2019 revision carried them forward. decimal128
is the 128-bit member: 34 significant decimal digits, exponent range 10^−6143
to 10^6144. A correct implementation must not merely produce a plausible answer;
it must produce *the* answer the standard prescribes — the correctly-rounded
result, the correct sign of zero, the exact NaN payload, and the exact set of
signaled exceptions — for every operation on every input.

That is an enormous claim surface, and it cannot be discharged by the
implementer's own tests alone. An author's tests encode the author's
understanding; where that understanding is wrong, the tests are wrong in the
same direction, and they pass. The only way out is **external, independent
evidence**: test vectors authored by other people, for other implementations,
under other assumptions, that nonetheless demand the same mathematical result.

decimal128 rests its correctness claim on exactly that. This document sets out
where the evidence comes from, how much of it there is, how the sources
disagree, and why their agreement — once the disagreements are understood —
constitutes a strong validity argument.

## 2. Three independent authorities

The three external corpora are not three copies of one test suite. They come
from three distinct engineering traditions, were built for three different
purposes, and encode their numbers in three incompatible notations. That
independence is the whole point; it is worth stating precisely.

### 2.1 IBM / Mike Cowlishaw — the General Decimal Arithmetic testcases (`dectest`)

The decimal formats in IEEE 754 exist largely because of Mike Cowlishaw's work
at IBM. His *General Decimal Arithmetic Specification* defined the arithmetic
model — significand-and-exponent, unnormalized "cohorts," precise rounding and
exception behavior — that the standard's decimal formats adopted. The same body
of work produced the reference software (`decNumber`) behind Java's
`BigDecimal`, Python's `decimal` module, GCC's decimal support, and IBM's own
hardware decimal units.

Alongside the specification, Cowlishaw published the **General Decimal
Arithmetic Testcases**: a directive-driven conformance corpus in the `decTest`
format.

> *General Decimal Arithmetic Testcases*, Mike Cowlishaw, IBM Fellow, IBM UK
> Laboratories. Version 2.44 (24 March 2009); the corpus files used here are
> version 2.62. © IBM Corporation 2000–2009.
> [speleotrove.com/decimal](http://speleotrove.com/decimal)

The `decQuad` subset (files prefixed `dq`) targets the 128-bit decimal format
**exactly** — every argument is representable in a decimal128, precision fixed
at 34, clamping on, the same format decimal128 implements. Operands appear as
human-readable decimal strings, and separately in hexadecimal **Densely Packed Decimal
(DPD)** — the compact encoding Cowlishaw co-designed, in which three decimal
digits pack into ten bits. Rounding is named in words (`half_even`, `ceiling`,
`floor`, `down`, `half_up`); exceptions are named as conditions (`Inexact`,
`Overflow`, `Division_by_zero`, `Invalid_operation`, and the non-signaling
`Clamped`, `Rounded`, `Subnormal`).

In this project the `decQuad` operation files, plus the multi-precision
transcendental files (`ln`, `exp`, `log10`), contribute **14,288 test vectors
across 40 files**.

### 2.2 IBM Haifa — FPgen and the `fptest` corpus

The second corpus comes from a different discipline entirely: **hardware
verification**. IBM's Haifa Research Lab built **FPgen**, a coverage-model-based
test generator for floating-point datapaths.

> [*FPgen — A Test Generation Framework for Datapath Floating-Point
> Verification*](https://web.archive.org/web/20061018135927/http://www.haifa.il.ibm.com/projects/verification/fpgen/papers/HLDVT-2003-FPGen.pdf),
> Merav Aharoni, Sigal Asaf, Laurent Fournier, Anatoly Koifman, Raviv Nagel.
> IBM Haifa Research Labs. 8th IEEE International High-Level Design Validation
> and Test Workshop (HLDVT), 2003. The IBM Haifa project site is now defunct; it
> survives via the Internet Archive — the paper (linked above), the
> [project documentation](https://web.archive.org/web/20081006095103/http://www.haifa.il.ibm.com/projects/verification/fpgen/doc.html),
> and the
> [test-suite download page](https://web.archive.org/web/20190724031753/https://www.research.ibm.com/cgi-bin/haifa/test_suite_download.pl?first=elenag&second=webmaster)
> from which this corpus was obtained.

FPgen's purpose was to hunt the *corner cases* of IEEE 754 — the inputs where
real silicon breaks: the boundaries of rounding, the emergence of infinities and
NaNs, signed zeros, the subnormal range, clamping, and the interaction of
trailing and leading zeros with the format's cohort structure. Rather than a
fixed list, it defined "coverage models" and solved constraints to generate
vectors that provably exercise each modeled situation. The published decimal
suite (© IBM Corp. 2007) is organized by exactly these themes — its file names
are a table of contents of what breaks floating-point:

```
Decimal-Basic-Types-Inputs        Decimal-Rounding
Decimal-Basic-Types-Intermediate  Decimal-Trailing-And-Leading-Zeros-Input
Decimal-Clamping                  Decimal-Trailing-And-Leading-Zeros-Result
Decimal-Mul-Trailing-Zeros        Decimal-Underflow
Decimal-Overflow
```

The `fptest` notation is its own: single-letter exception flags (`x u o z i`), a
compact rounding code (`=0 =^ > < 0`), `Q`/`S` literals for quiet and signaling
NaNs, and — critically — a separate **trap column** that records IEEE
754-*1985* trap-handler behavior (see §5). The suite spans **roughly 37,000
lines across nine files**; the decimal64 lines are filtered out, leaving the
decimal128 vectors this library is responsible for.

### 2.3 Intel — the RDFP Math Library and `readtest.in`

The third corpus is the regression driver of a shipping **implementation**:
Intel's Decimal Floating-Point Math Library, the reference software realization
of IEEE 754 decimal in the **Binary Integer Decimal (BID)** encoding.

> *Software Implementation of the IEEE 754R Decimal Floating-Point Arithmetic
> Using the Binary Encoding Format*, Marius Cornea, Cristina Anderson, John
> Harrison, Peter Tang, Eric Schneider, Evgeny Gvozdev, Charles Tsen. ARITH-18,
> 2007 (extended in *IEEE Transactions on Computers*, 2009). See also Marius
> Cornea, *IEEE 754-2008 Decimal Floating-Point for Intel Architecture
> Processors*, ARITH-19, 2009.

BID is the *other* standard interchange format — the alternative to DPD — in which the
significand is stored as a plain binary integer. Intel's library — `libbid` — is
its de-facto reference implementation; GCC incorporates that same Intel code for
its own decimal support, and Bloomberg's BDE vendors it as the back end of its
`bdldfp::Decimal128` type. The corpus used here is that library's own
regression input, `TESTS/readtest.in` from `IntelRDFPMathLib20U4` (© Intel Corp.
2007–2025, BSD-style license). Operands are **hex-BID** bit patterns, exceptions
a **hex flag byte**, rounding an **integer code** (`0`–`4`). The file carries
**126,437 lines** covering `bid32`/`bid64`/`bid128` across the full operation
set; the decimal128 lines for the IEEE-required operations — together with the
core transcendentals this library provides (`exp`, `exp10`, `log`, `log10`) —
are retained, while Intel's further transcendental *extensions* (trigonometry,
`erf`, `cbrt`, `pow`, …), none of which IEEE 754 requires, are consciously
excluded, each with a recorded reason.

### 2.4 The fourth script — hand-authored `native` cases

Three external corpora, however independent, still share a blind spot: they test
what their authors thought to test. A fourth suite, **`native`**, is authored
directly against the decimal128 API to cover what the external corpora do not —
the NaN-*propagating* `min`/`max` variants, specific string `FormatStyle`s,
hand-built NaN payloads, predicate queries (`isQNaN`, `isFinite`), and the
raw-bits accessors. These **1,547 cases across 31 files** are held to a stricter
standard than the corpus paths (see §6): they permit *no* skips.

## 3. One canonical language

Three scripts, three notations. To compare them they must be decoded into one.
The **Rosetta harness** (`Rosetta.md`) does this: four parsers
translate their native encodings — DPD hex, BID hex, decimal strings, letter
flags, hex flag bytes, five different rounding vocabularies — into a single
neutral test-case record of *operation, rounding, operands, expected result,
expected flags*. From there, one dispatch core runs every vector the same way.

The decode is deliberately total and auditable. Every operator token that
appears in any corpus must be explicitly classified as **included** (mapped to a
tested operation) or **excluded** (declined, with a written reason); a token in
neither fails the build. This means the corpora cannot silently drift out of
coverage: refresh Intel's `readtest.in` with a new operation and the harness
refuses to build until a human decides whether it is in scope. The set of
included operations *is* the coverage report.

## 4. Comparison is bit-for-bit

The comparison bar is the strongest available: **bitwise equality of the
result** (`d128_bitwiseEQ`), not "within one unit in the last place," not "equal
as numbers." Two decimal128 values that are numerically equal but differ in
cohort (say `1.0` versus `1.00`), or in the sign of a zero, or in a NaN payload,
are treated as **different** — because under the standard they *are* different,
and a correct operation must produce the specific one prescribed. Alongside the
value, the **exact set of signaled exceptions** is compared as a canonical
string, so a missing or spurious `inexact` flag is a failure just as a wrong
digit is.

This is a far harder target than numerical agreement, and it is applied
uniformly to all four sources. It is what elevates the exercise from "the
answers are about right" to "the answers are exactly, reproducibly, the standard
ones."

## 5. Where the sources disagree — and why that strengthens the case

Independent authorities do not agree on everything, and a validity argument that
hid the disagreements would be worthless. decimal128's do not hide them; each
divergence is understood, documented, and reconciled by an explicit,
narrowly-scoped rule — never by relaxing the comparison. The disagreements are,
in fact, evidence *for* independence: identical corpora would not diverge.

- **NaN propagation.** When an operation has two NaN inputs, which one
  propagates? The IBM/Cowlishaw corpora follow the General Decimal Arithmetic
  rule ("a signaling NaN is preferred, otherwise the first"); Intel's library
  follows "the first NaN wins." decimal128 implements the standard/GDAS
  behavior, and the harness rewrites *Intel's* expectations to that rule in a
  single Intel-only NaN-normalization step. The library is not bent to match a
  vendor; the vendor's differing convention is translated at the seam.

- **Trap-wrapped results (`fptest`).** The FPgen corpus predates the modern
  default-exception model: where an overflow or underflow trap is enabled, it
  records the IEEE 754-*1985* trap handler's **wrapped** value — the true result
  with its exponent biased by ±9216 (three-halves of Emax) so it stays
  representable for a handler to inspect. A 754-2019 default-handling library
  instead delivers ±∞ or a subnormal. Rather than discard these ~900 vectors,
  the harness *un-wraps* them — rescaling by the known bias re-applies the same
  rounding and range-clamp the operation performed — and they then reconcile
  **bit-for-bit**. A historical convention becomes recovered coverage, not a
  skip.

- **Tininess detection (`fptest`).** For decimal, IEEE 754 mandates detecting
  underflow **before** rounding. Some legacy FPgen underflow lines carry
  tininess-*after*-rounding expectations (a binary-centric habit). Here the
  standard is not negotiable: the library detects tininess before rounding, and
  the small set of non-conforming legacy lines is filtered rather than
  weakening the flag comparison for everyone.

- **Transcendental flags (`intel`).** Intel's `exp` and `exp10` are
  faithfully-rounded transcendental *extensions* — beyond the operations IEEE
  754-2019 requires of decimal — and their exception bookkeeping is
  correspondingly loose. Two families of Intel vectors carry demonstrably wrong
  flags: `exp` of a tiny nonzero input rounds to exactly `1.0` yet is marked
  *exact* (the result is inexact, and this library signals it); and `exp10`
  results that flush to ±0 or ±∞ are marked *inexact only*, dropping the
  underflow/overflow flag the standard requires alongside. On these ~29 vectors
  the *value* agrees and only Intel's flags are wrong, so they are line-skipped
  rather than reconciled. Tellingly, the divergence is confined to `exp`/`exp10`:
  `sqrt` — the one IEEE-*required*, correctly-rounded operation among these — and
  Intel's own `log`/`log10` alike match this library bit-for-bit, with no skips
  at all.

- **Corpus errata.** The authorities are candid that their suites are imperfect.
  Cowlishaw's testcases state plainly that they are "experimental ('beta'
  versions), and they may contain errors … achieving the same results as the
  tests here is not a guarantee that an implementation complies with any
  Standard." In that spirit, one FPgen overflow file required correction before
  its expectations were internally consistent; it is retained under a name that
  records the fact (`Decimal-Overflow-correctedByMTH`). Errata are handled in
  the open, at the level of individual vectors, with the reasoning attached.

Everything else — the overwhelming majority — agrees with no adjustment at all.

## 6. Three more layers of self-consistency

External agreement is the core of the argument; three internal checks reinforce
it.

- **Ladder-sibling identity.** Most arithmetic operations exist in several
  internal forms that must, by construction, agree: the general
  context-threaded form, an explicit-rounding form, a ties-to-even fast form,
  and a no-exception "quiet" form. For every result-bearing vector — regardless
  of which corpus it came from — the harness recomputes through each applicable
  sibling and asserts **bit-identity** with the primary result. A discrepancy
  reveals a forwarding or rounding bug even on inputs where the corpus value
  itself happened to match.

- **Public-API replay.** The entire corpus is run a *second* time through each
  port's public `Decimal128` wrapper — separate construction, separate method
  surface, separate flag plumbing — and checked for the same results. Correct
  internals reached through a broken public API would still be a broken library;
  this closes that gap.

- **Primitive-layer oracles.** Beneath the operation level, each port
  independently verifies the low-level unsigned 128-/256-bit kernels (the
  multiply, divide, and `divPow10` reciprocal-multiply routines) by whatever
  reference is most trustworthy in that language. Most ports compare the kernels
  against an established big-integer library: Java against `java.math.BigInteger`,
  Go against `math/big`, C against GMP (`mpz_t`), and Kotlin and Swift against
  their own portable big-integer packages (`bigint-kotlin`, run from common test
  code so the check also covers the JavaScript and WebAssembly targets, and
  `bigint-swift`) — with `bigint-kotlin` in turn cross-checked against
  `java.math.BigInteger` on the JVM. Two ports instead prove the kernels
  algebraically against themselves: Rust reconstructs the dividend from the
  returned quotient and remainder and asserts the defining inequalities, and Zig
  checks each result against native ultra-wide-integer (`u512`) arithmetic. C#
  carries no separate primitive suite; its kernels are exercised entirely through
  the full corpus and public-API replays above. A defect in any of these kernels
  would surface as a Rosetta divergence, but these targeted oracles localize it to
  the exact primitive at fault.

## 7. The result: fifty thousand agreements, eight times over

After decoding, filtering to decimal128, and applying the §5 handling, the
runnable core corpus is about **52,800 vectors**, with the public-API replay
(§6) adding roughly **46,500** more. And this is not one program's success:
decimal128 is implemented **eight independent times** — in C, Swift, Java,
Kotlin, Rust, Go, C#, and Zig — from a shared architecture but with genuinely
different code, compilers, and numeric primitives, all reading the *same* shared
corpus. That corpus passes, bit for bit, in every one.

Stack the claims:

- **Three independent external authorities** — Cowlishaw/IBM software decimal,
  IBM Haifa hardware verification, Intel BID implementation — plus a fourth
  gap-filling suite.
- **Three incompatible encodings** — DPD, BID, and decimal strings — so an
  encode/decode error cannot masquerade as a correct result across sources.
- **Two NaN-propagation philosophies, two exception-model eras**, each
  reconciled explicitly rather than papered over.
- **The strictest comparison available** — full bitwise value equality plus
  exact exception flags.
- **~50,000 vectors**, agreeing **bit-for-bit**, across **eight independent
  implementations**, reinforced by internal ladder-sibling identity and a
  full public-API replay.

No single one of these would be conclusive. Together they make the proposition —
*decimal128 computes the result IEEE 754 prescribes* — about as thoroughly
externally corroborated as a software arithmetic library can be.

## 8. Reproducibility

The evidence is public and re-runnable. The corpora are redistributed verbatim
in the `decimal128-resources` repository under
`rosetta/{dectest,fptest,intel,native}`, with each source's original license and
copyright preserved. Every port consumes that repository as a pinned submodule
and runs the Rosetta harness as part of its ordinary test suite, so any reader
can reproduce the bit-for-bit agreement from source. The harness itself is
described in `Rosetta.md`; the operations it exercises are
enumerated in `CoreFunctionMap.md` and `WrapperFunctionMap.md`.

Claims about correctness should be checkable by strangers. These are.

---

### Sources

- Mike Cowlishaw. *General Decimal Arithmetic Specification* and *General
  Decimal Arithmetic Testcases* (v2.44/2.62). IBM. speleotrove.com/decimal.
- M. Aharoni, S. Asaf, L. Fournier, A. Koifman, R. Nagel.
  [*FPgen — A Test Generation Framework for Datapath Floating-Point
  Verification.*](https://web.archive.org/web/20061018135927/http://www.haifa.il.ibm.com/projects/verification/fpgen/papers/HLDVT-2003-FPGen.pdf)
  IBM Haifa Research Labs, HLDVT 2003. Project site (via the Internet Archive):
  [documentation](https://web.archive.org/web/20081006095103/http://www.haifa.il.ibm.com/projects/verification/fpgen/doc.html),
  [test-suite download](https://web.archive.org/web/20190724031753/https://www.research.ibm.com/cgi-bin/haifa/test_suite_download.pl?first=elenag&second=webmaster).
- M. Cornea, C. Anderson, J. Harrison, P. Tang, E. Schneider, E. Gvozdev,
  C. Tsen. *Software Implementation of the IEEE 754R Decimal Floating-Point
  Arithmetic Using the Binary Encoding Format.* ARITH-18, 2007;
  *IEEE Trans. Computers*, 2009. Intel Decimal Floating-Point Math Library
  (`IntelRDFPMathLib`).
- *IEEE Standard for Floating-Point Arithmetic*, IEEE 754-2008 and 754-2019.
