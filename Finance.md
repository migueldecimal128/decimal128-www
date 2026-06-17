# BasicFinance — Design and Porting Spec

*Derived from the Swift reference (`decimal128-swift`, `Core/BasicFinance.swift`
+ the public `Decimal128/Finance.swift` wrapper). Ported from the
Kotlin-legacy `BasicFinance.kt`. Done across all four ports (Swift reference, C,
Kotlin, Java); the public wrapper is exposed in Swift/Kotlin/Java (C has no
wrapper). This document fixes the shape and records why each decision was made,
so future ports transliterate decisions rather than re-derive them.*

## 1. Purpose and Scope

**BasicFinance** is a small library of everyday financial calculations —
interest, annuities, mortgage amortization, and the discounted-cash-flow trio
NPV / IRR / MIRR — built **entirely on top of** the decimal128 arithmetic
surface. It adds no new numeric kernel; every function is a composition of
existing `d128_*` operations (`multiply`, `add`, `subtract`, `divide`,
`compound`, `rootn`, `abs`, `negate`, the comparisons).

Its reason to exist is **exact decimal money math**: the same calculations done
in binary floating point accrue representation error (see the README's
"bad sum" screenshots), whereas decimal128 carries cents exactly.

## 2. The Core/Wrapper Split — and why finance is in **Core**

The decisive architectural decision: **the finance algorithms live in Core, not
in the wrapper.** (CrossPlatformArchitecture.md §2.1 — Core is the shared,
constraint-bound engine; the wrapper is the per-language idiom layer.)

A natural first instinct is to put "convenience" functions like these in the
wrapper, since they are conveniences rather than IEEE operations. That instinct
is **wrong here**, for one reason: **cross-platform consistency.** If each
wrapper re-implemented `irr` in its host language, the four ports would be four
independent Newton-Raphson loops that could diverge in iteration order,
intermediate rounding, or convergence behavior. By placing the algorithm in
Core — over the byte-identical `d128_*_tte` ops — **every platform runs the one
same computation and produces the one same bit pattern.** The wrapper's job
shrinks to forwarding (§7).

This mirrors the rule already used for the IEEE §9.2 power family (`pown`,
`pow`, `rootn`, `compound`): the math is in Core; the wrapper only renames and
re-types it.

## 3. The single `_tte` form — no rounding/flag ladder

Core computational ops come in a **ladder** of forms — `_tte` (ties-to-even,
quiet), `_rnd` (caller rounding mode), `_ctx` (rounding + flag sink), and the
private `_rnd_ctxnull` (CrossPlatformArchitecture.md §6.1). Finance functions
expose **only the single `_tte` form**, e.g. `d128_irr_tte`.

Rationale: the ladder exists for **IEEE primitive operations**, where the
standard mandates per-operation rounding-direction and exception-flag control.
Finance functions are **compositions, not primitives** — IEEE says nothing about
"the correctly-rounded IRR." Threading a rounding mode and a flag sink through a
multi-step composition would have no well-defined meaning (which intermediate
rounds? whose flags accumulate?). So each finance function is a single
ties-to-even, quiet computation. This was an explicit decision ("collapse to
`_tte`") and is settled.

Consequence: the bar for these functions is **internal consistency and
agreement with the reference oracle**, not IEEE correctly-rounded — they are
inexact by nature (transcendental `rootn`, iterative `irr`).

## 4. Function Catalog

All take/return `D128` (the Core engine type) and compute at ties-to-even.
`compound(x, n) = (1+x)^n` (`d128_compound`); `rootn(x, n)` is the integer
n-th root. Integer counts (`numPeriods`, `numPayments`, `timesPerYear`) are
host `Int`, matching the `compound`/`rootn` exponent type.

### 4.1 Interest

| Function | Formula |
|---|---|
| `simpleInterest(principal, rate, periods)` | principal · rate · periods |
| `compoundInterest(principal, rate, n)` | principal · (1+rate)ⁿ |
| `effectiveAnnualRate(nominalRate, m)` | (1 + nominalRate/m)ᵐ − 1 |

### 4.2 Mortgage / annuity payment

- `mortgagePayment(principal, r, n)` = PV·r·(1+r)ⁿ / ((1+r)ⁿ − 1).
  **r = 0 → PV / n** (interest-free loan; avoids 0/0).
- `amortizationSchedule(principal, r, n)` → one `AmortizationRow`
  `{period, payment, interest, principalPaid, balance}` per period. Each period:
  `interest = balance·r`, `principalPaid = payment − interest`,
  `balance −= principalPaid`. **The final balance is snapped to exactly zero when
  its magnitude is below half a cent** (`0.005`) — a fixed-payment rounding
  artifact, not a real residual.

### 4.3 Annuity / single-flow value

| Function | Formula | r = 0 case |
|---|---|---|
| `presentValueAnnuity(pmt, r, n)` | pmt · (1 − (1+r)⁻ⁿ) / r | pmt · n |
| `futureValueAnnuity(pmt, r, n)` | pmt · ((1+r)ⁿ − 1) / r | pmt · n |
| `presentValue(fv, r, n)` | fv / (1+r)ⁿ | — |
| `futureValue(pv, r, n)` | pv · (1+r)ⁿ | — |
| `cagr(pv, fv, n)` | (fv/pv)^(1/n) − 1 | — |

### 4.4 Discounted cash flow

`cashFlows` is an ordered series; `cashFlows[0]` is the **immediate (t = 0,
undiscounted)** flow.

- `npv(rate, cashFlows)` = Σₜ CFₜ / (1+rate)ᵗ.
- `irr(cashFlows, guess, tolerance, maxIter)` — the rate making NPV = 0, via
  **Newton-Raphson with the analytic derivative** (NPV′ = Σₜ −t·CFₜ /
  (1+r)^(t+1)). Each iteration accumulates NPV and NPV′ in one pass over the
  flows, then `rate −= NPV/NPV′`; converges when `|step| < tolerance`.
- `mirr(cashFlows, financeRate, reinvestRate)` = (FV₊ / |PV₋|)^(1/(n−1)) − 1,
  where negative flows are discounted at `financeRate` and positive flows
  compounded forward at `reinvestRate`.

## 5. Behavioral Decisions

### 5.1 `irr` non-convergence → NaN sentinel (in Core)

`irr` can fail to converge (or hit a vanishing derivative). The legacy returned
a nullable. Core, being constraint-bound and shared, **cannot** return a
language-specific optional, so **Core `d128_irr_tte` returns `D128_QNAN0`** (a
quiet NaN) on non-convergence. This is portable across all four languages and is
mapped back to an idiomatic optional **at the wrapper edge** (§7).

### 5.2 Caller-contract checks via `verify`

Three preconditions are asserted with the Core `verify` mechanism
(CrossPlatformArchitecture.md — `verify`/`demand`/`impossible` contracts), not
returned as errors:

- `irr`: needs **≥ 2 cash flows**.
- `mirr`: needs **at least one negative cash flow** (else `|PV₋| = 0`, divide
  by zero). The Java port must capture the loop-reassigned `pvNeg` into an
  effectively-final local for the `verify` lambda.
- `cagr`: **`presentValue` and `futureValue` must both be positive** (the n-th
  root of a ratio).

These are programmer-error contracts (bad inputs), distinct from the runtime
non-convergence of §5.1.

### 5.3 Cash-flow representation is per-language

The cash-flow series is the one input that doesn't reduce to scalars, so each
port uses its idiomatic sequence type at the Core boundary:

| Port | Cash flows | Schedule out |
|---|---|---|
| Swift | `[D128]` | `[AmortizationRow]` |
| Kotlin | `List<D128>` | `List<AmortizationRow>` |
| Java | `D128[]` | `AmortizationRow[]` |
| C | `const D128 *cashFlows, int count` | caller-allocated `AmortizationRow *out` |

`AmortizationRow` is a small struct/`data class`/`record`/`struct` of one `int`
period + four `D128`.

## 6. Why NPV/IRR/MIRR are **not** in Rosetta

The Rosetta conformance harness (Rosetta.md) validates ops whose operands are a
fixed, small number of single-token decimal values (`<op> TIES_TO_EVEN <a> <b>
-> <r>`). NPV/IRR/MIRR take a **variable-length array** of cash flows, which does
not fit that single-token operand model. So finance is validated by a
**dedicated unit test** (`TestFinance`), tolerance-based, rather than by a
Rosetta `.txt` vector file. The scalar functions could be Rosetta-shaped but are
kept with their siblings in the one finance test for cohesion.

## 7. The Public Wrapper — the `Finance` namespace

Each wrapper (Swift/Kotlin/Java) exposes a **`Finance` namespace** over the
public `Decimal128` type, forwarding to the Core `d128_<name>_tte` ops. It adds
no arithmetic (WrapperLayer.md §1).

- **Carrier:** Swift caseless `enum Finance` · Kotlin `object Finance` · Java
  `public final class Finance` (private ctor). Members are `static`/object
  functions. A **public `AmortizationRow`** with `Decimal128` fields sits beside
  it (distinct from the Core one's `D128` fields).
- **Naming rule (settled).** Drop the `d128_`/`_tte` decoration and use the plain
  financial names. **Keep the dominant, unambiguous finance acronym; spell out
  otherwise.** So `irr`, `npv`, `mirr`, `cagr` stay abbreviated (these are *the*
  canonical identifiers — Excel/Sheets, numpy-financial, every textbook), while
  `effectiveAnnualRate` is spelled out ("EAR" is not a reliably recognized
  standalone acronym). Spelling out `internalRateOfReturn` was considered and
  rejected as verbose and not how finance APIs read.
- **`irr` → optional.** The wrapper maps the Core `D128_QNAN0` sentinel to the
  host's "may fail" type: Swift/Kotlin `Decimal128?` (nil), Java
  `Optional<Decimal128>` (empty).
- **`irr` defaults** (`guess = 0.1`, `tolerance = 1e-10`, `maxIter = 200`)
  surface at the public edge: Swift/Kotlin default parameters; Java a convenience
  `irr(cashFlows)` overload alongside the full-control one.

## 8. Validation

- **Core:** `TestFinance` (ported from the legacy) checks all functions against
  the legacy expected values, **tolerance-based** (finance is inexact: `rootn`
  is transcendental, `irr` iterates). 18 checks, including `irr ≈ 0.14332…`,
  `npv(irr, flows) ≈ 0`, and `mirr ≈ 0.13490…`. Passes in all four ports.
- **Wrapper:** `TestFinanceWrapper` re-runs the same 18 checks **through the
  public `Finance` API**, confirming the wrapper forwards correctly. Passes in
  Swift/Kotlin/Java.

Cross-platform consistency comes from the shared Core algorithm over
byte-identical `d128_*` ops plus identical test vectors and tolerances.

## 9. Current State

| Layer | Swift | C | Kotlin | Java |
|---|---|---|---|---|
| Core `BasicFinance` + `TestFinance` | `3d43e88` | `cc44416` | `b62a286` | `0cec6ff` |
| Public `Finance` wrapper + `TestFinanceWrapper` | `a06590d` | — (no wrapper) | `d504302` | `2a5bfca` |

All on `main`, all green.
