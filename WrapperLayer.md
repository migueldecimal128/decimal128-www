# The Wrapper Layer — Design and Porting Spec

*Derived from the Swift reference wrapper (`decimal128-swift`, target
`Decimal128` over `Core`). This document is the spec for porting the wrapper to
the other languages. Kotlin is now done (`decimal128-kotlin` `wrapper/` module —
see §8); next Rust/Python/Go/Scala per CrossPlatformArchitecture.md §2.3.*

## 1. Purpose and Scope

The **wrapper** adapts the package-internal **Core** to the idioms of its host
language so a `Decimal128` value feels first-class (operators, protocol/interface
conformances, idiomatic naming, optional/nullable conventions). See
CrossPlatformArchitecture.md §2.1/§2.3.

Unlike the Core, the wrapper is **not** bound by the cross-language constraint
regime (§3 of that doc) — it is *allowed* and *expected* to use each language's
full idiom: operator overloading, protocol conformances, computed properties,
enums, closures. What stays uniform across ports is the **shape of the public
surface and the behavior**, not the source text. This document fixes that shape
and records why each decision was made, so ports transliterate decisions rather
than re-deriving them.

The Core boundary it sits on is the `Int`-typed, package-scoped `d128_*` surface
(CrossPlatformArchitecture.md §6.1). The wrapper's whole job is to restore, at
the public edge, the idiom the Core surrenders.

## 2. The Public Surface

The Swift reference exposes one public value type `Decimal128` plus a small set
of supporting public types. Every method below forwards to a `d128_*` Core call;
the wrapper adds no arithmetic of its own.

### 2.1 `Decimal128` — the value type

- **Construction:** from a machine integer; from a string (failable, see §4.5);
  integer & string literals; `init?(exactly:)` from any integer type;
  `init(signOf:magnitudeOf:)` (copySign); `init(bidBitPattern:)` /
  `init(dpdBitPattern:)` (§4.7).
- **Well-known values:** `zero`, `nan`, `signalingNaN`, `infinity`.
- **Operators:** `+ - * /` and compound forms, unary `-`, `==`, `<` (§4.1–4.3).
- **Arithmetic methods, three forms each** — bare (ties-to-even, quiet),
  `(_, rounding:)`, `(_, context:)`: `adding`, `subtracting`, `multiplied(by:)`,
  `divided(by:)`. Plus `addingProduct(_:_:)` (fma), `squareRoot()`,
  `exp/exp10/ln/log10`, `truncatingRemainder(dividingBy:)` /
  `remainder(dividingBy:)`, `integerDivided(by:)`, `logB()`, `rounded(_:)`,
  `scaled(byPowerOf10:)`, `quantized(to:)`, `strippingTrailingZeros()`.
- **Magnitude / sign:** `magnitude`, unary `-`, `negate()` — **bit-level**, not
  GDAS computational (§4.4).
- **Classification:** `isNaN`, `isSignalingNaN`, `isFinite`, `isInfinite`,
  `isZero`, `isNormal`, `isSubnormal`, `isCanonical`, `sign`,
  `floatingPointClass` (§4.9).
- **Comparison:** `compared(to:[context:])`, `comparedSignaling(to:context:)`,
  `totalOrdering(comparedTo:)`, `totalMagnitudeOrdering(comparedTo:)`,
  `isTotallyOrdered(belowOrEqualTo:)`, `isTotallyOrderedByMagnitude(belowOrEqualTo:)`,
  and the quiet predicates `isEqual(to:)`, `isLess(than:)`,
  `isLessThanOrEqualTo(_:)`, `isUnordered(with:)` (§4.10).
- **Quantum:** `hasSameQuantum(as:)`, `quantumExponent(context:)`.
- **Min/max (static):** `minimum`/`maximum`/`minimumMagnitude`/`maximumMagnitude`
  (NaN-propagating) and the `…Number` variants (NaN-ignoring), bare + `context:`.
- **Conversion:** `toInt64(rounding:context:)` /
  `toInt64SignalingInexact(rounding:context:)` (§4.8); `bidBitPattern` /
  `dpdBitPattern` (§4.7); `string(_ style:)` and `description` (§4.6 formatting).

### 2.2 Supporting public types

| Type | Kind | Cases / members |
|---|---|---|
| `Rounding` | enum:Int | `toNearestOrEven`(0), `toNearestOrAwayFromZero`(1), `towardZero`(2), `towardPositive`(3), `towardNegative`(4) |
| `DecimalStyle` | enum:Int | `automatic`(0), `exponential`(1), `engineering`(2), `coefficientExponent`(3) |
| `DecimalFlags` | OptionSet:Int | `invalidOperation`(1<<0), `divisionByZero`(1<<1), `overflow`(1<<2), `underflow`(1<<3), `inexact`(1<<4) |
| `DecimalComparison` | enum | `ascending`, `equal`, `descending`, `unordered` |
| `DecimalContext` | class (reference) | `rounding`, `raisedFlags`, `clearFlags()`, `parseIEEE(_:)` |
| `floatingPointClass` | (Swift stdlib `FloatingPointClassification`) | the 10 IEEE classes; see §4.9 |

All enum `rawValue`s **mirror the Core's load-bearing codes** (Round 0–4,
FORMAT_* 0–3, Exception754 bit positions 0–4, CLASS_* 0–9). This makes the
wrapper↔Core crossing a zero-translation `rawValue` / `init(rawValue:)`.

## 3. Naming and Collision Avoidance

The wrapper names must not collide with the host language's standard library.
The Swift collisions found, and the resolutions (these are the *concepts*; each
port re-checks against its own stdlib):

- **`Rounding`** — the user-facing rounding enum, distinct from the Core's
  `Round`. (CrossPlatformArchitecture.md §6.4.)
- **`DecimalStyle`** — the format-style enum. It must **not** be named
  `FormatStyle`: Swift/Foundation owns `FormatStyle` (the protocol and its
  `IntegerFormatStyle` / `NumberFormatStyleConfiguration` family); a public
  `FormatStyle` would clash and read as a Foundation conformance it isn't. §6.4
  records `FormatStyle` as the *conceptual* name only.
- **`DecimalFlags`** — the raised-exception set.
- **`DecimalContext`** — the arithmetic context. A bare `Context` is far too
  generic for a public top-level type.
- **`parseIEEE`** — the context-aware parse entry point (§4.5).

Decimal-prefixed names (`DecimalStyle`, `DecimalFlags`, `DecimalContext`) echo
Foundation's `Decimal` without colliding; a port may prefer its own prefix.

## 4. Design Decisions

### 4.1 The operator / rounding / context triad

Bare operators (`+ - * /`) and the bare arithmetic methods **round ties-to-even
and raise no flags** — exactly how `Double` arithmetic behaves. Two opt-in forms
add control:

- `(_, rounding:)` — an explicit `Rounding`, still no flag tracking.
- `(_, context:)` — rounds by the context and **records raised flags** into it.

Map to the Core's `_tte` / `_rnd` / `_ctx` op families respectively. For ops the
Core only exposes with a context, the wrapper provides bare + `context:` and
skips the standalone `rounding:` form.

### 4.2 Equality, ordering, hashing

`==` and `<` use **IEEE semantics** (matching `Double`): `+0 == -0`, NaN compares
unequal to everything incl. itself, NaN is unordered under `<`. This yields
`Comparable` (and `sorted()`) for free.

**`Hashable` is deliberately *not* conformed** in the reference: doing it
correctly needs a total-order/cohort decision (NaN-consistency, `1.0` vs `1.00`).
Deferred. Ports should likewise hold off until that's specified.

### 4.3 Numeric-protocol conformances

Conform to the host's numeric protocols where they exist:
`AdditiveArithmetic` + `Numeric` + `SignedNumeric` (Swift). These hand you
`+=`/`-=`/`*=` and `.zero` via protocol defaults, so the wrapper only spells the
primitive operators. `init?(exactly:)` fails only when the integer exceeds 34
significant digits. **Division is *not* a `Numeric` requirement** — `/` is spelled
separately. (Kotlin/Java/etc. lack this protocol family; they expose the same
operators directly.)

### 4.4 `magnitude` / unary `-` are bit-level, **not** GDAS abs/minus

`magnitude` and unary `-` are the **IEEE sign operations** (bit-level: clear /
flip the sign), matching `Double` (`-(+0) → -0`, `abs(NaN)` clears the sign).
They forward to the Core's `d128_abs`/`d128_negate`.

These are **different operations** from the GDAS *computational* `abs`/`minus`
(which quiet sNaN→invalid, preserve a quiet NaN's sign, and give `minus(+0) →
+0`). The wrapper exposes the bit-level idiom; it does **not** surface
computational abs/minus. (In the conformance harness, the divergent GDAS vectors
are the ones on the shared skip list.)

### 4.5 Two parse entry points

- **`init?(parsing: String) -> Decimal128?`** — context-free, the Swift-optional
  idiom: returns `nil` for unparseable input, ties-to-even, no flags.
- **`DecimalContext.parseIEEE(_ String) -> Decimal128`** — IEEE/GDAS
  convertFromDecimalCharacter: rounds an over-precision literal by the context's
  rounding (raising `inexact`), and a malformed string yields a quiet **NaN** with
  `invalidOperation` (never nil/trap). Flags accumulate into the context.

`parseIEEE` is **wrapper-only** — it composes the Core's `d128_parse_ctx`, no Core
change. Putting it on the context (the parse environment) also sidesteps a
failable-vs-non-failable initializer collision.

**Footgun (Swift-specific):** because `Decimal128` is `ExpressibleByStringLiteral`,
`Decimal128("3.14")` on a *literal* binds to the literal initializer
(non-optional, traps on bad input), while `Decimal128(someVar)` binds to
`init?` (optional). The runtime parse is therefore labeled `parsing:` to keep the
two unambiguous. Ports without string-literal conformance won't hit this.

### 4.6 `DecimalContext` and `DecimalFlags`

`DecimalContext` is a **reference type** holding a rounding direction and an
accumulating flag sink; it is **not** thread-safe / not `Sendable` — one context
per task (the Core's `Context` contract). `Decimal128` values themselves *are*
value types / `Sendable`; only the flag-tracking context is not — document this
asymmetry. A value-`struct` context would silently share the sink (it wraps a
reference), so a class is the honest choice.

`raisedFlags` returns a `DecimalFlags` **value snapshot** read from the context
(via the one Core accessor `Context.exceptionFlagsInt() -> Int`). `DecimalFlags`
is an `OptionSet`/bitset over the Core's `Exception754` bit positions — so
`DecimalFlags(rawValue: coreInt)` is a zero-translation crossing.

Formatting (`string(_:)` / `description`) is the inverse: `description` uses
`DecimalStyle.automatic` (GDAS to-scientific-string); the four styles map to the
Core `FORMAT_*` codes.

### 4.7 Interchange (BID / DPD)

The two IEEE interchange encodings are exposed as **128-bit patterns** — the
analog of `Double.bitPattern` scaled to 128 bits: `init(bidBitPattern:)` /
`var bidBitPattern`, and the same for `dpd`. In Swift the type is native
`UInt128` (and the Core's `U128` is literally `typealias U128 = UInt128`, so it's
a direct pass-through). A port whose language lacks a native 128-bit unsigned
integer must choose a representation (e.g. a hi/lo `ULong` pair, or reuse the
Primitive `U128`); the *behavior* — lossless cohort/payload-preserving
re-encoding, never rounding/signaling — is fixed.

### 4.8 Integer conversion

`toInt64(rounding:context:)` (default truncate-toward-zero, matching
`Int(Double)`) and `toInt64SignalingInexact(rounding:context:)` (also raises
`inexact` on a discarded fraction). Each dispatches on the `Rounding` to the
matching Core `d128_toInt64<Direction>[SignalInexact]`. NaN/∞/out-of-range is an
*invalid* conversion: raises `invalidOperation` and returns an unspecified
sentinel.

### 4.9 Classification and quantum

`floatingPointClass` returns the host's standard 10-case class enum where one
exists (Swift `FloatingPointClassification` — the `Double.floatingPointClass`
analog), mapped from the Core's `d128_ieeeClass` 0–9 via a `switch`. A port whose
stdlib has **no** such enum should define its own `IEEEClass: Int` (the type
CrossPlatformArchitecture.md §6.4 anticipated), with rawValues 0–9 matching the
`CLASS_*` codes — then both directions are `rawValue`/`init(rawValue:)`, no
switch.

`quantumExponent(context:)` returns the value's quantum exponent `q` (its quantum
is `1×10^q`); NaN/∞ raise `invalidOperation`.

### 4.10 Three-way compare + predicate derivation

The comparison core is the **three-way** `compared(to:[context:])` →
`DecimalComparison{ascending,equal,descending,unordered}` (quiet; sNaN signals),
`comparedSignaling(to:context:)` (any NaN signals), and the total-order
`totalOrdering`/`totalMagnitudeOrdering` (never `.unordered`).

The full IEEE **boolean predicate family** (`isGreater`, `isLessEqual`,
`isNotGreater`, `isOrdered`, `isLessUnordered`, … and their signaling variants —
~20) is **not** individually surfaced: every one reduces to the three-way result
(e.g. `isLessEqual = compared ∈ {ascending, equal}`). Swift's `FloatingPoint`
exposes only the minimal `isEqual`/`isLess`/`isLessThanOrEqualTo`, which the
wrapper provides; the rest are left to `compared(to:)`. (The conformance harness
*derives* the full family from the three-way result, which validates exactly that
reduction.)

## 5. Sanctioned Per-Port Divergences

The behavior and surface shape are uniform; these implementation points are
idiom-forced and expected to differ:

1. **128-bit interchange type** — native `UInt128` (Swift) vs a synthesized
   representation elsewhere (§4.7). Kotlin (no native 128-bit unsigned) exposes a
   **hi/lo `Long` pair**: `Decimal128.fromBID(high, low)` / `fromDPD(high, low)`
   and `bidBitPatternHigh`/`bidBitPatternLow` (+ dpd). The core `U128` is built/
   read only inside those bodies — it never appears in a public signature.
2. **Class enum** — stdlib `FloatingPointClassification` (Swift) vs a custom
   `IEEEClass: Int` (§4.9).
3. **Numeric protocols** — `AdditiveArithmetic`/`Numeric`/`SignedNumeric` (Swift)
   vs direct operators (§4.3).
4. **String-literal conformance** — Swift's `ExpressibleByStringLiteral` and its
   footgun (§4.5) have no equivalent in most ports.
5. **Context as a class** — uniform intent, but value/reference and Sendable/
   thread-marking spell differently per language.
6. **Operator overloading & value-class** conventions — per the
   `port-conventions` memory.
7. **Argument labels** — Swift's external labels (`quantized(to:)`,
   `multiplied(by:)`, `isTotallyOrdered(belowOrEqualTo:)`) have no Kotlin
   equivalent. Fold the label into the method name
   (`isTotallyOrderedBelowOrEqualTo`) or keep a plain parameter the caller may
   name (`quantized(to = …)`). Beware the hard keywords `by`/`as` — illegal as
   parameter names (use `dividingBy`, `other`).
8. **Equality / ordering surface** — where `==`/`<` are operators distinct from
   hashing (Swift), conform IEEE `Equatable`/`Comparable` and defer `Hashable`
   (§4.2). Where `==`≡`equals` and `<`≡`compareTo` (Kotlin), IEEE semantics make
   an unlawful `equals`/`Comparable` (NaN) and pair badly with the deferred
   `Hashable`, so expose IEEE comparison **only** through named methods
   (`isEqual`/`isLess`/`isLessThanOrEqualTo`/`isUnordered`/`compared`) and leave
   `equals`/`hashCode`/`Comparable` at their defaults — deferred alongside
   `Hashable`. (The compound operators `+=`/`-=`/`*=` still come for free, synthesized
   from `plus`/`minus`/`times`.) Static factories (`minimum`, `fromBID`, …) become
   `companion object` extensions so call sites read `Decimal128.minimum(a, b)`.

## 6. Gotchas (learned building the Swift reference)

- The `Decimal128("literal")` vs `Decimal128(var)` optionality split (§4.5).
- `magnitude`/`-` ≠ GDAS abs/minus (§4.4) — do not wire them to a corpus's
  computational `abs`/`minus` op.
- Don't conform `Hashable` yet (§4.2).
- `Numeric`'s `*=` default may not resolve — spell `*=` explicitly if the compiler
  complains.
- Enum `rawValue`s are **load-bearing** (they mirror Core codes); keep the order.

## 7. Validation: the public-API Rosetta variant

The wrapper is validated by a **Rosetta variant that drives the conformance
corpora through the public API only** (no Core access) — the real proof the
wrapper transduces the validated engine. It reuses the neutral `RosettaCase` and
the existing corpus parsers; only the dispatch + comparison are re-pointed.

Key techniques (transliterate these):

- **Operands** decode via public construction: `bid/dpdBitPattern` for hex,
  `ctx.parseIEEE` for **dectest** decimals (round + flag on parse),
  context-free parse elsewhere, plus the `Q`/`S` NaN literals.
- **dectest results** compare by **rendered string** (`string(.automatic)` =
  GDAS toString), with a **cohort fallback**: on a string miss (non-format op),
  parse the expected and compare via `.coefficientExponent` (value-exact,
  spelling-agnostic — matches the Core harness's decode-and-compare). This
  rescues vectors that echo operand spelling (`-Inf`, `088`).
- **fptest results** are a **raw cohort encoding** (`+coeff e exp`), not GDAS.
  Compare in `.coefficientExponent`, converting the expected with 4 textual
  steps: drop the coefficient `+`, uppercase `e→E`, **add** `+` to a non-negative
  exponent (our format emits it; fptest omits it), map specials. Skip `#`
  (don't-care) and trap-enabled lines; strip `u` (tininess) from both flag sides.
- **Intel / hex results** compare by **canonical value**: decode the expected and
  compare via the (canonical) `bidBitPattern` — DPD has redundant non-canonical
  encodings (the `dqcan` vectors) a UBD-internal library canonicalizes on decode,
  so raw-bit comparison is wrong.
- **`parseIEEE` is gated to dectest** — Intel's `from_string` overflows to
  Infinity and raises no GDAS parse flags, so Intel/fptest operands stay
  context-free.
- **Reuse the Core harness's own skip lists** (`RosettaDectestSkips` /
  `RosettaIntelSkips`) by reference, not by copy — single source of truth for the
  obsolete pre-2019 vectors.
- **Intentional skips** (documented, never converted): Intel-only NaN-payload and
  min/max equal-value **cohort conventions** (reconciled only at the D128 level
  by the Core harness's Intel-normalize), the fptest 1985 trap-wrap, and a few
  DPD-hex NaN compare results.
- **Flag-accumulation fidelity** is the recurring failure source — combined
  parse-flags + op-flags must match the corpus; expect a handful to diagnose.

## 8. Current State (Swift reference, 2026-06-15)

The Swift wrapper is complete and validated against all three corpora **through
the public API**, zero failures:

| corpus | passed |
|---|---|
| dectest | 12,382 |
| fptest | 19,915 |
| Intel | 14,210 |
| **total** | **~46,500 vectors** |

Remaining skips are all intentional (§7). Public unit tests live alongside in
`WrapperTests`.

The **Kotlin** wrapper (`decimal128-kotlin` `wrapper/` module, package
`com.decimal128.decimal128kotlin.wrapper`) is complete and validated on **all
three KMP targets** (jvm, macosArm64, wasmJs/Node), with pass counts **identical**
to the Swift reference:

| corpus | passed |
|---|---|
| dectest | 12,382 |
| fptest | 19,915 |
| Intel | 14,210 |
| **total** | **46,507** |

13 source files transliterate the Swift surface (the §5 divergences applied);
a 36-test public unit suite + the 3-corpus `WrapperRosetta` run green. The
wrapper Rosetta currently **copies** the neutral corpus harness + 13 MB corpora
from `core/src/commonTest` into its own test set (a deliberate choice, accepting
drift); de-duplicating it via a shared test module is on the punchlist
(*"Revisit shared Rosetta harness (Kotlin)"*).

Next port: Rust/Python/Go/Scala.

---

*End of first draft.*
