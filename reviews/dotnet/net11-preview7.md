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
- **Who I am** — an independent decimal128 specialist; no affiliation with the .NET team.
  I maintain my own conformant implementation and a cross-checking (Rosetta) suite; that
  is the lens for everything here.
- **The bar** — IEEE 754-2019 decimal128 and GDAS (Cowlishaw), named explicitly throughout
  (never "the spec" unqualified).
- **The series** — one installment per release candidate; the same harness each time, so
  readers can watch the type converge. Per-edition status vocabulary: *resolved /
  still open / newly introduced*.
- **Reading guide** — correctness is graded against the standards; performance is reported,
  not graded, because it improves release-over-release without breaking anyone (see §8–§9).
- **Through-line to set up here:** *confidence in the whole from evidence in the part.*
  Two findings (rounding, flags) are really about how much trust the un-audited surface
  has earned.

## 2. Executive Summary
- **Lead with the win:** the numerical results are correct — verified bit-for-bit against
  dectest, fptest, and libbid via the Rosetta suite. They nailed the part that is hardest
  to get right.
- **The one that matters:** rounding is composed, not fused. Directed rounding
  (Ceiling/Floor/Round) is applied *after* ties-to-even has already rounded, so results are
  double-rounded and wrong near boundaries.
- **Scorecard:** Correct results ✅ / Rounding architecture ❌ / Flags ⚠️ absent /
  Performance ⚠️ / Design (BID lock-in) ⚠️.
- **Series scorecard line:** correctly-rounded operations = **1 of 5** rounding-direction
  attributes (`roundTiesToEven` only). Track this number across RCs.
- Findings tagged Now vs. Later up front.

## 3. Scope & Methodology
- **Version under test:** .NET 11 preview 7, exact SDK/build.
- **Reference standards:** IEEE 754-2019 decimal128 + GDAS.
- **Verification suite:** Rosetta bit-identity against **dectest, fptest, and libbid** — the
  evidentiary backbone; state vector counts and what bit-identity does and does not prove.
- **Comparison cohort:** d128, libbid, `System.Decimal` (96-bit BCL baseline, flagged
  out-of-cohort on range), `System.Numerics.Decimal128` (SUT).
- **Benchmark harness:** op-benchmark .NET 11 arm, InProcess toolchain, per-op input
  categories.
- **Fairness caveats** (stated once, up front): value + ties-to-even comparison surface
  where the SUT is TTE-only; FMA is port-only (the SUT has none).
- **Reproducibility:** everything needed to rerun, so the series is auditable RC-over-RC.

## 4. What They Got Right
- **Correct results, verified** — the central, non-trivial achievement; walk through the
  suite agreement (dectest / fptest / libbid).
- **TTE as the default rounding-direction attribute — including on the operators — is the
  correct, IEEE-consistent choice.** Operators can't carry a rounding attribute; binding
  `+ − × ÷` to the standard default is exactly right. (This is an endorsement, not a
  criticism — it sets up §5, which is about the *absence of an alternative*, not the default.)
- Clean first-class BCL type and generic-math integration.
- BID over DPD is the defensible representation choice (sets up §7's caveat).

## 5. The Rounding Problem (Headline Finding)

**5.1 What they built** — arithmetic always rounds ties-to-even; `Ceiling`/`Floor`/`Round`
are separate functions applied *after* the operation has already rounded.

**5.2 Why that's wrong — worked example.** Ask for the quotient of two full-precision
decimals, rounded to an integer ties-away-from-zero:

```
a = 4999999999999999999999999999999999      (5x10^33 - 1)
b = 2000000000000000000000000000000000      (2x10^33)

exact a / b = 2.4999999999999999999999999999999995      <- 35 digits, not representable

  correct  - round the exact quotient once, ties-away   -> 2
  the API  - 1. divide: silently rounds to 34 digits, ties-to-EVEN -> 2.5
             2. apply ties-away to 2.5                              -> 3
  result                                                            -> 3   (wrong)
```

The `.5` the user's rounding mode needed was already consumed by a ties-to-even step they
never asked for. The second rounding is handed `2.5` and has no way back to the true value.
**And the answer is 2.5 — an everyday magnitude.** What carries the 34 digits is the
*operands*; dividing two full-precision decimals is completely routine.

**5.3 The necessary condition (pre-empt the "edge case" dismissal).** This *cannot* happen
to a value that fits in 34 digits — the operation would be exact and the rounding applied
to the true value. It requires the exact result to overflow the format's precision. That is
not exotic: it is simply what happens when you divide two full-precision decimals near a
rounding boundary. (Non-representability is *necessary*; proximity to a boundary within one
ULP is what makes it *occur* — so it's real but not constant.)

**5.4 The correct model** — the rounding-direction belongs *inside* the operation: round the
exact result **once**, to the requested mode. A post-hoc `Round`/`Floor`/`Ceiling` applied to
an already-ties-to-even-rounded value is structurally incapable of producing the
correctly-rounded answer. This same *compute-exact-then-round-once* core is exactly what a
correct `fusedMultiplyAdd` requires (§6.3): a naive FMA built from their existing
multiply-then-add would round `a*b` *before* adding `c`, reproducing this very
double-rounding — which is why FMA's absence points at the same missing core, not a separate
problem.

**5.5 The conformance boundary (Now vs. Later).**
- IEEE 754-2019 **§5.1** requires each operation to be performed *"as if it first produced an
  intermediate result correct to infinite precision and with unbounded range, and then
  rounded that intermediate result"* — **once** — under the applicable rounding-direction
  attribute (**§4.3**). Post-hoc composition rounds **twice**.
- Consequence: under any non-default attribute — `roundTiesToAway`, `roundTowardPositive`,
  `roundTowardNegative`, `roundTowardZero` — decimal128 operations as exposed are **not
  correctly rounded**. The implementation conforms to §5.1 for `roundTiesToEven` **only**.
- **The fix is additive** — new fused operation overloads that take an explicit
  `roundingDirection` and round the exact result once. Existing callers untouched, no
  behavior change → the *implementation* is a legitimate **Later** (§9.2).
- **The one genuine "Now" is disclosure:** by GA, do not claim IEEE 754 rounding conformance
  beyond `roundTiesToEven`, and do not present composed directed rounding as
  correctly-rounded. Cheap, non-breaking, and it protects the reputational claim.
- Design note for the fused API: the parameter must be a true **rounding-direction** type,
  **not** `System.MidpointRounding`. `MidpointRounding` governs only *ties*; the directed
  attributes (`towardPositive/Negative/Zero`) change the rounding of *non-tie* results too,
  so the midpoint enum would under-specify exactly the modes that matter.

**5.6 The confidence cost.** The reputational exposure (§5.5) is the visible risk. The
quieter one is inferential: correctly-rounded single rounding is the foundation of the
standard, not a fine point, so exposing directed rounding as a second pass over an
already-rounded value raises a fair question about how completely the composition problem was
understood. A careful evaluator cannot contain that question to the rounding path alone — if
a load-bearing invariant was missed here, confidence in the un-audited surface has to be
discounted too. To be clear about scope: the numerical core is *verified correct*, so this
reads as an API-design gap rather than an engine defect. But it is precisely why independent,
standards-anchored verification is warranted, and why this series revisits each release
rather than taking the surface at face value.

The confidence cost is also **cumulative, not a single data point.** The absence of flags
(§6) compounds it directly: it removes one of the independent channels that would let an
outside evaluator confirm results were computed correctly, so the very evidence that could
*restore* confidence after the rounding finding is the evidence that isn't there. Two
signals pointing the same way — a missed foundational invariant, and a missing verification
channel — reinforce rather than offset each other. The sharpest corroboration, though, is
structural: the un-exposed directed rounding (§5.1) and the absent `fusedMultiplyAdd`
(§6.3, §5.4.1) are **two required-operation gaps, reached from different angles, that resolve
to a single architectural cause** — the apparent absence of a general
*compute-exact-then-round-once* core. That is no longer one isolated slip to explain away.

## 6. Secondary Findings & Conformance Observations

### 6.1 Flags (secondary finding)
- No exception/status-flag support (inexact, invalid, overflow, underflow, division-by-zero).
- **Impact is twofold:** (a) a modest functional gap for users who need sticky flags;
  (b) more importantly for a new implementation, flags-against-known-vectors are an
  *independent verification channel* — their absence removes a way to confirm results were
  computed by the right *path*, not merely to the right *value*.
- Framed ⚠️ not ❌ — reduces confidence rather than correctness.
- **This is a direct contributor to the confidence cost of §5.6**, not a parallel theme: the
  missing flags are a missing *verification channel*, so they subtract from exactly the
  evidence that could have rebuilt confidence after the rounding finding. State the linkage
  explicitly here and in the Executive Summary.

### 6.2 Other conformance observations (from the Rosetta run)
Three items surfaced by the Rosetta harness. Only the first is a real gap; the other two are a
permitted choice and a deliberate one — and saying so is the point. Distinguishing genuine
defects from IEEE-permitted / intentional behavior is what keeps this a critique rather than a
complaint list.

- **`CompareTo` is value-order, not §5.10 `totalOrder`** — *a real conformance gap.* As of
  preview 7, `CompareTo` orders by numeric value; it does not implement IEEE 754-2019 §5.10
  `totalOrder` (which distinguishes ±0, orders NaNs, and separates cohort members).
  **In progress:** commits landing toward RC1 indicate the team is already working on
  `totalOrder`, so I expect to mark this *resolved* in the next installment. (This is also the
  clean counter-evidence for §5.6: the team is demonstrably responsive on conformance where
  it's raised, which is why the confidence concern is scoped to the rounding-composition
  design specifically, not the effort broadly. Good candidate for the series' first visible
  *resolved* arc.)

- **min/max cohort quantum differs from GDAS** — *IEEE-permitted, not a defect.* When
  `min`/`max` return one of two numerically-equal operands, the quantum (cohort member) chosen
  differs from GDAS's selection. IEEE 754 permits this latitude, so it's a documented
  behavioral divergence for interop awareness, nothing more.

- **Canonical NaN is negative** — *intentional; interop note only.* `Decimal128.NaN` is a
  negative quiet NaN (`0xFC00…`), **verified on preview 7** (SDK `11.0.100-preview.7.26366.102`;
  RC1 not checked). This is not an oversight — it is consistent with .NET's long-standing NaN
  convention: `double.NaN` (`0xFFF8…`), `float.NaN` (`0xFFC00000`), and `Half.NaN` (`0xFE00`)
  are all negative. Fully IEEE-compliant (NaN sign is not numerically interpreted). Worth a line
  purely because most IEEE/C reference implementations use a *positive* canonical NaN
  (`0x7C00…`), so anyone bit-bridging against MS's default must know theirs is negative.

### 6.3 No `fusedMultiplyAdd` (secondary finding — diagnostic)
- **A required operation is missing.** `fusedMultiplyAdd` is a *required* general-computational
  operation under IEEE 754-2019 **§5.4.1** — not a convenience. Its absence is a conformance gap
  in its own right, parallel to the §5.1 rounding gap.
- **Remediation is additive → a "Later" (§9.2).** Adding the op breaks no existing caller; it
  can land in a future release.
- **But it is diagnostic — that's why it's here.** A correct FMA forms the *exact* product
  `a*b` and rounds **once** after adding `c`. Their multiply is already correctly-rounded, so
  they *can* form and round an exact wide product — the capability exists. Yet a correct FMA
  cannot be composed from their `multiply` then `add` (that rounds `a*b` first — the §5
  double-rounding again); it needs the same general *compute-exact-then-round-once* core that
  correct directed rounding needs. FMA and directed rounding are one missing core seen from two
  angles (§5.4).
- **Fair bound:** this is inference from *absence*, not proof. They demonstrably have exact wide
  multiply, so the gap is a missing *generalization* — a reusable single-rounding finalize — not
  missing capability. It feeds §5.6 as a second, independent signal; it does not by itself
  convict.

## 7. Design: The BID Lock-In Question
- **7.1 BID was the right call** vs. DPD — but it carries a complicated decode.
- **7.2 The concern** — the public API currently leaks the internal representation instead
  of abstracting it.
- **7.3 The recommendation** — treat DPD and BID as *symmetric interchange formats*: both
  require an explicit **decode** on deserialization and **encode** on serialization; neither
  is "the internal type in disguise." Keep BID internally if they like — but hide it behind
  the API so the internal representation can change later without a breaking change.
- **7.4 Why this is a "Now"** — it's an API-shape decision, cheap in preview,
  expensive-to-breaking after GA.

## 8. Performance
- **8.1 The division problem** — the current divide is a naive algorithm; scaling operations
  pay for it.
- **8.2 The double hit** — divide is slow, *then* trailing-zero stripping is slow, so
  division-heavy workloads are penalized twice. (Shared root cause with §5: the exact
  quotient is where both the correctness bug and the perf cost live.)
- **8.3 Four-way benchmarks** — per-op tables (d128 / libbid / `System.Decimal` /
  `Decimal128`) by input category; lead with division/scaling where the gap is starkest,
  then add/sub, mul, convert, round-trip.
- **8.4 Interpretation** — where the gap is algorithmic vs. JIT/runtime; call out
  `System.Decimal`'s 96-bit range difference so it isn't read as like-for-like.
- **8.5 The stakes** — a slow first release reinforces the myth that *software* decimal
  floating point is inherently slow. It isn't; d128 and libbid show the headroom. This is
  the narrative cost of shipping performance-last.
- **8.6 Why this is a "Later"** — every number here is improvable in a future release without
  breaking a single caller.
- **8.7 Series baseline** — these are the numbers the next RC is measured against.

## 9. Recommendations

### 9.1 Now — before GA (contracts, API shape, honesty)
- **State the conformance boundary honestly:** correctly-rounded operations are TTE-only;
  do not claim IEEE 754 rounding conformance beyond `roundTiesToEven`; do not present
  composed directed rounding as correctly-rounded (§5.5).
- **Settle the interchange API** so BID/DPD are symmetric and the internal representation is
  hidden (§7) — even if BID stays internal and any DPD/flag work follows later.
- **Reserve the flag surface** so the verification channel and future semantics aren't
  foreclosed (§6).
- Rationale: these are semantic and API contracts, plus disclosure — cheap now, breaking or
  reputation-damaging after GA.

### 9.2 Later — after GA (additive, non-breaking)
- **Add fused rounding-direction operations:** alternate methods taking an explicit
  `roundingDirection`, rounding the exact result once — using a true rounding-direction type,
  not `MidpointRounding` (§5.5). Drives the scorecard from 1/5 toward 5/5.
- **Implement `fusedMultiplyAdd` (§5.4.1):** the required fused op (§6.3). It almost certainly
  shares the same *compute-exact-then-round-once* finalize as the fused rounding-direction
  methods above, so the two are natural to build together.
- **Replace the naive division algorithm;** make scaling and trailing-zero stripping fast (§8).
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
- **B. Full per-op benchmark tables** — raw ns + ratios.
- **C. Verification methodology** — vector sources (dectest / fptest / libbid), counts, and
  any skip/divergence list.
- **D. Environment & reproduction** — SDK versions, toolchain flags, machine/arch.

</div>
