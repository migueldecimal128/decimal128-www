# Java Core Port Plan — Swift `Sources/Core` → `decimal128-java/core`

*Draft — 2026-06-11*

Plan to port the decimal128 **Core** layer from Swift to pure Java (no JNI),
validated continuously by porting the **Rosetta** test harness alongside it.
The Primitive layer is already ported (`decimal128-java/primitive`); the Java
Core sits on it and calls its name-compatible API.

This plan does not begin translation. It fixes scope, sequencing, conventions,
and the two settled decisions:

- **Memory model: immutable value-return.** Match the shipped Java Primitive
  layer (immutable `final` classes, value-returned, relying on C2 escape
  analysis). The architecture doc's ThreadLocal fill-in pool (§4.7.3 / §5.1) is
  the *measured fallback*, adopted per-type only if `jmh -prof gc` later shows a
  type escaping. Not built up front.
- **Order: IEEE-required first.** Arithmetic + serde + parse/print + sqrt +
  min/max + quantize/toIntegral land before the transcendentals
  (exp/ln/log10). Co-evolution (below) means all of Core is reached eventually;
  this fixes only the ordering.

References: `CrossPlatformArchitecture.md` (the constraint regime, cited as
"§n" below), `Rosetta.md` (the harness, cited as "R§n"), `PrimitiveLayer.md`.

--------------------------------------------------------------------------------
## 1. Ground truth established

- **Target module.** `decimal128-java/core` is an empty Gradle module already
  wired in `settings.gradle.kts` (`include("primitive","core","wrapper")`).
  Package: `com.decimal128.decimal128java.core`. Java 21, JUnit 5, mirroring the
  `primitive` module's `build.gradle.kts`.
- **Primitive API is name-compatible.** The Java Primitive layer exposes the
  same mangled names the Swift Core already calls: `add_128_128x128`,
  `mul_256_256x256`, `mulPow10_128_128`, `divPow10_q128res_128_rrmp10`,
  `divRem_q256r64_256x64`, `U128`, `U256`, `Residue`, `Verify.verify/demand/
  impossible`, etc. Core-Java calls these unchanged.
- **Scope.** `Sources/Core` = 52 files, ~8,168 lines.
- **Swift Core is already in the portable subset.** Zero `switch`; zero
  `for-in`; one operator overload (`Flags.==`); Int-backed simple enums; **no
  closures outside the verify/demand suppliers** (the former Padé-constant
  `.map`/`.enumerated` chains and the `Flags` `.filter/.map/.joined` chain were
  converted to counted loops — see §2). The port is line-by-line
  transliteration, not a restructuring.
- **Foundation usage is negligible.** `BExpMinMax.swift` (import appears
  unused); `IntegerParsePrint.swift` (`String(decoding: bytes, as: UTF8.self)`
  → `new String(bytes, 0, len, StandardCharsets.US_ASCII)`).
- **Rosetta harness** = 25 files, ~3,011 lines, ~90 `CanonicalOp` dispatch arms.
  Corpora are data: dectest 2.5M, fptest 3M, intel 9M, native 132K — copied
  verbatim into the Java test module's resources.

--------------------------------------------------------------------------------
## 2. Translation conventions (the regime, applied to Core)

Core is **shippable logic**, so the constraint regime (§3) binds it fully:

- **Branching:** `if` only (no `switch`); parenthesized predicates; braces
  always; `while` the only loop with a single `int` index, counted-loop idiom
  (§3.7.3).
- **Functions:** `public static` top-level; C naming; manual name-mangling for
  "overloads" (§8). No method dispatch, default params (except verify/demand/
  impossible source-location), tagged params, closures (except the
  verify/demand `BooleanSupplier`), or operator overloads.

  **Padé constant tables (`D128ExpConstants`/`D128LogConstants`).** The `D38`
  weight arrays are built at module load from `[String]` literals through two
  counted-loop helpers in `D38.swift` — `parseD38Weights([String]) -> [D38]`
  (parse each coefficient) and `negateOddIndexed([D38]) -> [D38]` (derive the
  denominator `Q(z) = P(−z)` by negating odd-index weights). Transliterate the
  helpers to `static D38[]` methods with `for` loops; the module-global `let`s
  become Java `static final D38[]` filled in a `static {}` block. These were
  the last `.map`/`.enumerated` chains in Core; together with the former
  `Flags.filter/.map/.joined` (removed when `Flags.description` adopted the
  canonical `xuozi` letter form, dropping `getSetExceptions`,
  `Exception754: CaseIterable`, and `Set<Exception754>`), Core now carries no
  closures outside verify/demand.
- **Types:** signed `long` dwords everywhere (§4.3); `int` for in-memory
  scalars (qExp etc., §4.4); primitive integer types and arrays thereof. Native
  128-bit types never appear in Core — they are confined to the Primitive layer.
- **Enums → `static final int`** (§6.3). Core enums are core-internal and
  load-bearing:
  - `Exception754` (INVALID_OPERATION=0 … INEXACT=4; bit positions, §6.4)
  - `Residue` (already in Primitive: EXACT/LT_HALF/HALF/GT_HALF)
  - `Round` (TIES_TO_EVEN=0 … TOWARD_NEGATIVE=4)
  - `Comparison754`, `InvalidCause`, `ParseStatus`, and the `D128Print` style enum
  SCREAMING_SNAKE_CASE names (§6.2).
- **Memory:** `Decimal128` is a heap `final` class with `long ubdHi64, ubdLo64`
  (§4.1; the `int TBD` padding field per §4.1 is optional, deferred). All result
  aggregates (`Quot128Residue`, `D38`, U128/U256) are **immutable final
  classes, value-returned** — the settled decision. No ThreadLocal pool now.
- **Errors:** no exceptions in core logic; conditions flow through return values
  and `Context` flags. Internal checks via `Verify.verify/demand/impossible`
  (already in Primitive; reuse or re-expose for Core).
- **`Context`/`Flags`:** `Context` is the mutable flag/trap carrier; nullable
  `Context?` (the `_ctxnull` family) is the *one* sanctioned optional (§3.3) →
  Java `Context` reference that may be `null`.

Sanctioned divergences from Swift to expect (§10): heap class vs struct;
`-> Never`/`fatalError` → `throw`/`AssertionError` (already handled in
`Verify`); enum-as-int; the `Flags.==` overload becomes a named
`Flags.equals`-style method or inline compare.

--------------------------------------------------------------------------------
## 3. Core dependency tiers (port order within each phase)

1. **Value/enum/context:** Exception754, Comparison754, InvalidCause,
   ParseStatus, Round, Flags, Context, Residue.
2. **D128 type:** D128 (the `Decimal128` class), D128Constants,
   D128NonComputational (predicates: isNaN/isFinite/sign/…).
3. **Finalize/rounding:** Finalize, Residue handling, Round.
4. **divPow10 Core dispatch:** DivPow10, DivBarrett, DivKnuth, DivDirect,
   DivRangeRecipMulPow10, U256Div, U256Sqrt. (These are the *Core-level*
   dispatch over the Primitive `divPow10_*`/barrett/knuth kernels — the
   `div_128_pow10_*`/`div_256_pow10_*` names in Swift Core are Core functions,
   not Primitive.)
5. **Extended precision:** D38 + AddSub/Compare/Div/Fma/Finalize/
   RoundToIntegral/Sqrt.
6. **D128 arithmetic:** ArithAddSub, ArithMul, ArithDiv, ArithCompare, ArithFma.
7. **Serde:** SerdeBid, SerdeDpd.
8. **Text:** Parse, Print, IntegerParsePrint.
9. **Transcendental/tail (deferred per ordering):** Exp, Log, Sqrt,
   LogBScaleB, BExpMinMax, MinMax, CtxMinMax, ToIntegral, NextUpDown,
   TotalOrder, StripTrailingZeros (+ their constants files).

--------------------------------------------------------------------------------
## 4. Rosetta is co-evolved, not sequenced

Rosetta's stage-2 dispatch bodies *call Core*, so the harness cannot be cleanly
ordered before or after Core. Split it along its existing seam (R§11) and grow
it with Core:

- **Rosetta-infra** — parsers (Intel/Dectest/Fptest/Native), RosettaCase,
  ResultValue, DispatchResult, flag rendering, `RosettaText`, dialect decoders,
  the runner loop, by-kind compare, include/exclude maps + the coverage
  meta-tests. Depends only on Core's decode/parse/flag/compare surface
  (`d128_fromBID`, `d128_fromDPD`, `d128_parse_ctx`, `d128_bitwiseEQ`, `Flags`,
  `Context`) — available after Core Phase B.
- **Rosetta-dispatch** — the ~90 arms. Grows one arm per operator as each Core
  phase delivers it; that op's corpus vectors light up immediately.

**Rosetta is test code → regime-exempt (§3.2).** Write it idiomatically in Java:
- `CanonicalOp` as a **real Java `enum`** → an **exhaustive `switch`** restores
  Swift's "missing arm = compile error" guarantee (a no-switch if-ladder would
  degrade this to a runtime "no arm"). C keys on the int regardless; Java need
  not.
- `ResultValue` as a sealed interface / record (not a hand-rolled tagged union).
- `Map`/`Set` literals, `split`, streams permitted in parsers.
- The R§13 "not-yet-converted" Swift bits (`guard…else`, `Set`/dict literals,
  parser `-> T?`) go fully idiomatic.

Keep structure parallel to the Swift harness so it stays line-checkable; use
Java idiom where it buys safety (the dispatch switch, ResultValue).

Per-language artifacts to author fresh (R§11): the stage-2 dispatch bodies, the
`RosettaText` bodies, and `CanonicalOp.name`/`byName`.

--------------------------------------------------------------------------------
## 5. Phased plan

Each phase compiles green and is validated by the corpus vectors its arms
unlock before the next begins.

**Phase 0 — module scaffold.**
- `core/build.gradle.kts` (Java 21, JUnit 5, `implementation(project(":primitive"))`).
- Package `com.decimal128.decimal128java.core`. Confirm `core` builds empty.

**Phase A — value/enum/context tier.**
- Port Exception754, Comparison754, InvalidCause, ParseStatus, Round, Flags,
  Context (tier 1). Small, dependency-free, unblocks everything.

**Phase B — D128 type + decode/parse surface.**
- `Decimal128` class + D128Constants + D128NonComputational (tier 2).
- The decode/parse/compare surface Rosetta-infra needs: SerdeBid/SerdeDpd
  *decode* paths, `d128_parse_ctx`, `d128_bitwiseEQ`.

**Phase R0 — Rosetta-infra standup (de-risks the whole harness).**
- Stand up all four parsers + `RosettaText` + dialect decoders + include/exclude
  maps + the **coverage meta-tests**; wire one trivial dispatch arm.
- Copy the four corpora into the test module resources; confirm the loader path.
- Exit: pipeline reads all four sources; partition meta-tests green; the one arm
  validates against its vectors. Harness proven independent of ~88 ops.

**Phase C — finalize + divPow10 Core dispatch.**
- Tiers 3–4: Finalize/Round machinery and the Core divPow10 family. The rounding
  heart all arithmetic depends on. Validate via any op whose arm exists.

**Phase D — IEEE-required arithmetic (+ D38).**
- Tier 6 ops in order: add/sub → mul → div → compare → fma, plus the D38
  engine (tier 5) that fma/div/sqrt need. Wire each op's dispatch arm as it
  lands; corpus vectors validate immediately.

**Phase E — serde (encode) + text.**
- SerdeBid/SerdeDpd encode paths, Parse, Print, IntegerParsePrint (tiers 7–8).
- Replace the lone Foundation call with `new String(bytes, 0, len, US_ASCII)`.

**Phase F — sqrt + remaining IEEE-required tail.**
- Sqrt, MinMax, CtxMinMax, ToIntegral, NextUpDown, TotalOrder,
  StripTrailingZeros, LogBScaleB, BExpMinMax + their arms.

**Phase G — transcendentals (deferred ordering).**
- Exp, Log (ln/log10) + D38 Padé support + their constants and arms. Last,
  per IEEE-required-first.

Validation is continuous (corpus vectors per arm) — there is no separate
end-stage validation phase.

--------------------------------------------------------------------------------
## 6. Risks / things to budget for

- **`RosettaText`** — the one exacting reimplementation (tokenize/hasPrefix/
  trim/indexOf against Java `String`). Get it green with the parser tests first.
- **`#`DPD / `[hex]`BID operand decoders** must match Swift bit-for-bit (part of
  the dialect). The native-source strict path (no skips, R§12) is the early
  canary.
- **Resources loader** — classpath resource vs file path for ~14.5 MB of
  vectors; trivial but a real step.
- **`Context` nullability** — the `_ctxnull` family is the single sanctioned
  optional; keep the `null`-vs-non-null `Context` discipline explicit at the
  seam.
- **Escape-analysis assumption** — the immutable value-return choice assumes C2
  scalarizes the aggregates on hot paths. Not verified until a `jmh -prof gc`
  pass; ThreadLocal pool remains the documented fallback per-type if it doesn't.

--------------------------------------------------------------------------------
## 7. Settled vs open

**Settled:** target module/package; immutable value-return memory model;
IEEE-required-first ordering; co-evolution of Rosetta with Core; Rosetta written
idiomatically (regime-exempt) with a real-enum `CanonicalOp` switch.

**Open (revisit later, not blocking):** whether any aggregate needs the
ThreadLocal pool (pending jmh); the `int TBD` padding field in `Decimal128`;
exact home/name of this plan doc; whether the wrapper layer follows.
