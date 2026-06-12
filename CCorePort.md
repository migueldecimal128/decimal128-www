# C Core Port Plan — Swift `Sources/Core` → `decimal128-c/core`

*Draft — 2026-06-12*

Plan to port the decimal128 **Core** layer from Swift to portable C (C11),
validated continuously by porting the **Rosetta** test harness alongside it.
The Primitive layer is already ported (`decimal128-c/primitive`, GMP-tested) and
Core sits on it, calling its name-compatible API.

This plan does not begin translation. It fixes scope, sequencing, conventions,
and the settled decisions:

- **Memory model: value-return structs, no heap.** C is the *convergence
  target* of the regime and the closest language to Swift — `struct` value
  semantics, result aggregates returned by value in registers, zero heap
  allocation (`CrossPlatformArchitecture.md` §4.7.2). This matches the shipped C
  Primitive layer (native `unsigned __int128` in bodies, dword-struct public
  shape) rather than the JVM family's fill-in pool.
- **In-memory scalar width: `int32_t`.** qExp and the other small in-memory
  scalars are `int32_t` (§4.4.3, settling that open item). Deterministic 32-bit
  matches the Java/Kotlin cores exactly, so three of the four cores share one
  overflow boundary and Swift's 64-bit `Int` stays the single documented
  divergence (§4.4.2). `int_fast32_t` is **rejected** — it is 64-bit on some
  64-bit platforms, defeating the deterministic-behavior goal. Plain `int` is
  rejected in favor of the self-documenting fixed-width spelling.
- **Order: IEEE-required first.** Arithmetic + serde + parse/print + sqrt +
  min/max + quantize/toIntegral land before the transcendentals
  (exp/ln/log10), matching the settled `JavaCorePort.md` ordering. Co-evolution
  (below) means all of Core is reached eventually; this fixes only the order.
- **Validation: port Rosetta to C and co-evolve it with Core.** The swift-over-C
  / Kotlin-Native-over-C wrapper path (§2.3) is *not* the validation mechanism
  for this port; the C Rosetta harness is. This keeps the C core self-contained
  and machine-checked against the same corpora the other cores pass.

References: `CrossPlatformArchitecture.md` (the constraint regime, cited as
"§n"), `Rosetta.md` (the harness, "R§n"), `PrimitiveLayer.md`, and the
practical companion `PORTING-NOTES.md`.

--------------------------------------------------------------------------------
## 0. Status (handoff)

**2026-06-12 — Phase 0 primitive-seam work is COMPLETE; core not yet started.**

The primitive seam (§4) was audited, filled, and aligned across all four cores
before starting core. On the C side specifically (commits `5eb56ba`, `b3c02f6`
on `decimal128-c` `main`):

- Every seam symbol Core needs now exists in `decimal128-c/primitive`, name-
  compatible and GMP-oracle tested: `pow10Dw0/Dw1`, `pow10_256Dw0..3`,
  `pow10U128`, `isLt/isGe_pow10_34_bool_128`, `calcDigitLenInt`,
  `cmp_int_256x256`, the `Quot256Rem128/Rem256/Residue` aggregates, and the
  `U256↔double` sqrt bridge (`u128FromDouble`, `u256ToFloorDouble`). 21/21 ctest.
- The C primitive headers were renamed to the cross-core **PascalCase** base
  names (`PrimitiveTables.h`, `U128.h`, `U256AddSub.h`, `CalcBitLenDigitLen.h`,
  …) and `U128`/`U128Arith` were split — so C core `#include`s match the HLL
  file names. `rrmp10` is split into `Rrmp10Kernel` + `Rrmp10Tables`.

**Entry point for the fresh session:** the only remaining Phase 0 step is the
**core scaffold** (create `decimal128-c/core/` + wire CMake — §6 Phase 0,
second bullet). Then begin **Phase A**. The seam-audit table in §4 below is
retained for provenance but is done.

--------------------------------------------------------------------------------
## 1. Ground truth established

- **Target module.** `decimal128-c/core` does **not exist yet** — same starting
  point Kotlin and Java had. The repo currently has `primitive/` (src + include +
  tests, CMake/CTest, GMP oracle, CI green) and a top-level `CMakeLists.txt` that
  `add_subdirectory(primitive)`. Core is a net-new `core/` sibling subdirectory.
- **Primitive API is name-compatible and the seam is now COMPLETE** (§0, §4).
  The C Primitive layer exposes every mangled name Swift Core calls
  (`add_128_128x128`, `mul_256_256x256`, `mulPow10_128_128`,
  `divPow10_q128res_*`, `divRem_q256r64_256x64`, the `U128`/`U256` dword structs,
  `Residue`, `verify`/`demand`/`impossible`, …) **plus** the formerly-missing
  Core-driven symbols (`Quot256*` aggregates, `U256↔double` bridge, the pow10
  accessors, `cmp_int_256x256`, `calcDigitLenInt`) — all added and tested before
  core. Headers are PascalCase, matching the HLL file names.
- **Representation is settled by the Primitive layer.** `U128`/`U256` are dword
  `struct`s (`int64_t dw0..dw3`, dw0 least significant, §4.2/§4.3); native
  `unsigned __int128` is confined to primitive bodies via `u128_pack`/`unpack`.
  Core consumes these structs and never names a native 128-bit type. The
  "`__int128` vs limb structs" question from PORTING-NOTES §2 is therefore
  already answered: dword structs, body-only natives.
- **Scope.** `Sources/Core` = **50 files, ~8,160 lines**. The Rosetta harness is
  ~34 files / ~3,800 lines (mostly data + dispatch).
- **Swift Core is already in the portable subset.** Zero `switch`; zero
  `for-in`; Int-backed simple enums; no closures outside the
  verify/demand/impossible suppliers. The port is line-by-line transliteration,
  not a restructuring. The Java/Kotlin ports are known-good cross-checks (Kotlin
  passes the full ~51k-vector Rosetta suite).
- **Foundation/stdlib usage is negligible.** The one notable case is
  `IntegerParsePrint` building a `String` from an ASCII byte buffer; in C this is
  a fixed `uint8_t[64]` stack scratch (§4.7.2) and direct byte emission — no
  library call.

--------------------------------------------------------------------------------
## 2. Translation conventions (the regime, applied to the C Core)

C is **shippable core logic**, so the constraint regime (§3) binds it fully.
Unlike the HLLs, C is the MOHLL target the regime lowers *toward*, so most
"sanctioned divergences" land on the Swift-like side here.

- **Branching:** `if` only (no `switch` in core logic); parenthesized
  predicates; braces always; `while` the only loop, single `int32_t` index,
  counted-loop idiom (§3.7.3, index `+= 1` as the last statement). No `x++`.
- **Functions:** file-scope/`static` top-level; C naming; the names are already
  C-mangled at the source (`op_result_operands_qualifier`, §8) — C is what the
  mangling scheme was designed for, so Core function names port **verbatim** from
  Swift. No overloading to synthesize.
- **Types:** dwords are `int64_t` (§4.3); in-memory scalars (qExp, lengths, loop
  indices) are `int32_t` (settled, §1). Native 128-bit types never appear in
  Core. Every width change is an explicit cast (§3.4 — no implicit numeric
  conversion).
- **Enums → C `enum` (names only) or `#define` int constants** (§6.3). C enums
  convert freely to/from `int`, so they give names but little safety;
  bit-manipulation runs on the integer value regardless. SCREAMING_SNAKE_CASE
  (§6.2). The load-bearing orderings are fixed:
  - `Exception754` — `INVALID_OPERATION=0 … INEXACT=4` (bit positions, §6.4)
  - `Round` — `TIES_TO_EVEN=0 … TOWARD_NEGATIVE=4`
  - `Residue` — `EXACT=0 / LT_HALF=1 / HALF=2 / GT_HALF=3` (already in Primitive
    as a 2-bit int, D17 — reuse, do not redeclare)
  - `Comparison754`, `InvalidCause`, `ParseStatus`, and the `D128Print` style enum
- **Value types:** `D128` is a `struct` with `int64_t ubdHi64, ubdLo64` (§4.1;
  the JVM `TBD` padding field does not apply to C). `D38`, `Quot128Residue`,
  `Quot256*`, `U128`/`U256` are all `struct`s returned **by value** (§5).
- **Multi-value return:** value-return aggregates, in register-passed structs
  (§5.1). The Java/Kotlin fill-in convention does **not** apply to C — call sites
  read `let q = op(x, y)` ↔ `U128 q = op(x, y)`, no destination-first parameter.
  An `inout`/pointer out-param is used only where Swift itself does (the
  `AsciiPrintBuffer` scratch).
- **Errors:** no exceptions. IEEE conditions flow through return values and
  `Context` flags. Internal checks use `verify` / `demand` / `impossible`
  (already in C Primitive — reuse). `verify` is a **parenthesized macro** under a
  `VERIFY_ENABLED` guard (already wired: `VERIFY_ENABLED=1` in the CMake build,
  expands to nothing otherwise). `impossible` is `_Noreturn` + `abort()`. This is
  the closure-vs-macro and `Never`-vs-`noreturn` divergence (§10 items 6–7),
  already resolved on the C side by the Primitive port.
- **`Context` nullability:** the `_ctxnull` family is the *one* sanctioned
  optional (§3.3). In C this is a `Context *` that may be `NULL`; `_ctx` means a
  non-NULL `Context *`. Keep the NULL-vs-non-NULL discipline explicit at the
  seam. `ctxnull`-named formal params per the Swift convention.
- **Padé constant tables (`D128ExpConstants`/`D128LogConstants`).** The Swift
  `D38` weight arrays are built from `[String]` literals through two counted-loop
  helpers (`parseD38Weights`, `negateOddIndexed`). In C, transliterate the
  helpers to functions over `const char *[]` and fill `static const D38[]` once
  (a file-scope initializer or a one-time guarded init). No closures involved
  (the Swift `.map`/`.enumerated` chains were already removed).

Sanctioned divergences that **do not** apply to C (they were HLL-only): heap
class vs struct (C is struct, like Swift), value-return vs fill-in (C is
value-return, like Swift), enum-as-Int-wrapper (C uses plain `enum`). The C core
is, by design, the closest structural match to the Swift source.

--------------------------------------------------------------------------------
## 3. Core dependency tiers (port order within each phase)

1. **Value/enum/context:** Exception754, Comparison754, InvalidCause,
   ParseStatus, Round, Flags, Context, Residue (reused from Primitive),
   AsciiPrintBuffer, D128Constants.
2. **D128 type:** the `D128` struct, D128NonComputational (predicates:
   isNaN/isFinite/signFlag/…).
3. **Finalize/rounding:** Finalize, Round machinery, Residue handling.
4. **divPow10 Core dispatch:** DivPow10, DivBarrett, DivKnuth, DivDirect,
   DivRangeRecipMulPow10, U256Div (Knuth-D), U256Sqrt. These are the
   *Core-level* dispatch over the Primitive `divPow10_*` / barrett / knuth
   kernels.
5. **Extended precision:** D38 + D38AddSub / D38Compare / D38Div / D38Fma /
   D38Finalize / D38RoundToIntegral / D38Sqrt.
6. **D128 arithmetic:** D128ArithAddSub, D128ArithMul, D128ArithDiv,
   D128ArithCompare, D128ArithFma.
7. **Serde:** D128SerdeBid, D128SerdeDpd.
8. **Text:** D128Parse, D128Print, IntegerParsePrint.
9. **Transcendental/tail (deferred per ordering):** D128Exp, D128Log,
   D128Sqrt, D128LogBScaleB, BExpMinMax, D128MinMax, D128CtxMinMax,
   D128ToIntegral, D128NextUpDown, D128TotalOrder, D128StripTrailingZeros
   (+ D128ExpConstants / D128LogConstants).

The Swift `Sources/Core/*.swift` file list (50 files) is the 1:1 checklist; C
file names mirror them. The `primitive/` rename (§0) settled the casing: use the
**PascalCase Swift base name verbatim** (`D128ArithAddSub.swift` →
`D128ArithAddSub.h`/`.c`), matching the now-PascalCase primitive headers and the
HLL cores.

--------------------------------------------------------------------------------
## 4. The primitive seam audit (Phase 0 — DONE 2026-06-12)

> **DONE.** This audit was run and the seam filled before core (§0). The list and
> table below are kept for provenance; every gap is closed in `decimal128-c`
> commits `5eb56ba` + `b3c02f6`. No seam work remains.

Core is intended to be near-identical across languages; per-language divergence
is pushed into Primitive. The critical seam Core calls (PORTING-NOTES §1):

- Dword accessors over flat limb tables: `pow10Dw0(p)/pow10Dw1(p)`,
  `pow10_256Dw0..3(i)`, `POW10_34/_38`, `isLt/isGe_pow10_34_bool_128`,
  `MASK54L`, `calcDigitLenInt`, the `cmp_int_256x256` compare, the
  `Quot256Rem128 / Quot256Rem256 / Quot256Residue` aggregates, and the
  `U256↔double` sqrt-seed bridges.

A cross-language survey (not just a grep — agent-reported absence was verified
against the actual code) found these **referenced by Core but missing from the C
Primitive**, all now **added** name-compatibly with GMP-oracle + death tests:

| symbol | status |
|---|---|
| `Quot256Rem128 / Rem256 / Residue` | added as typedefs (Core constructs them; no producing op) |
| `U256↔double` bridge (`u128FromDouble`, `u256ToFloorDouble`) | added (`U256Double.h/.c`) |
| `pow10Dw0/Dw1`, `pow10_256Dw0..3`, `pow10U128` | added (`PrimitiveTables.h`) |
| `isLt/isGe_pow10_34_bool_128` | added (`PrimitiveTables.h`) |
| `calcDigitLenInt` | added (`CalcBitLenDigitLen.h/.c`) |
| `cmp_int_256x256` | added (`U256.h`) — the one the Swift-Core grep alone could **not** surface (Swift Core uses native `<` on `U256`; only the JVM/C cores need the named compare) |

Lesson recorded for the Rosetta/core port to come: a Swift-Core-only grep misses
seam symbols Swift reaches through native operators (`cmp_int_256x256` was the
example). Cross-check against the Java/Kotlin primitive surface, not just Swift
Core, when auditing a seam.

--------------------------------------------------------------------------------
## 5. Rosetta is co-evolved, not sequenced

Rosetta's stage-2 dispatch bodies *call Core*, so the harness cannot be cleanly
ordered before or after Core. Split it along its existing seam (R§11) and grow it
with Core:

- **Rosetta-infra** — parsers (Intel / Dectest / Fptest / Native), RosettaCase,
  ResultValue, DispatchResult, flag rendering, `RosettaText`, dialect decoders
  (BID `[hex]`, DPD `#..`), the runner loop, by-kind compare, include/exclude
  maps + the coverage meta-tests. Depends only on Core's decode/parse/flag/
  compare surface (`d128_fromBID`, `d128_fromDPD`, `d128_parse_ctx`,
  `d128_bitwiseEQ`, `Flags`, `Context`) — available after Core Phase B.
- **Rosetta-dispatch** — the ~90 `CanonicalOp` arms. Grows one arm per operator
  as each Core phase delivers it; that op's corpus vectors light up immediately.

**Rosetta is test code → regime-exempt (§3.2)** — but C has no escape hatch the
way Java does (Java's plan uses a *real `enum` + exhaustive `switch`* for
`CanonicalOp` to recover compile-time arm-completeness). In C, `CanonicalOp` is
an `int`/`enum` and dispatch is an `if`-ladder or function-pointer table; there
is **no compile-time "missing arm" guarantee** — compensate with a coverage
meta-test that asserts every `CanonicalOp` value has a registered arm (fail
loudly at test startup, not silently at dispatch). Parsers may use ordinary C
string handling freely (test code); `ResultValue` is a tagged `struct`
(discriminant + union) rather than a sealed type.

Harness shape to reproduce: resource load via plain `fopen`/`fread` (no
classpath — a real advantage over the JVM ports), per-source parsers, the
dispatch over ~90 arms, by-kind result + flag reconcile, per-source
include/exclude maps and skip lists, Intel expectation-normalize, and the
ladder-sibling consistency check. The hex operand decoders and the big
skip/include literal tables are the bulk — **generate the literal tables from the
Swift/Java source with a script** rather than hand-transcribing (transcription
is where bugs hide, §6).

Corpora are data, identical across ports: copy
`{dectest,fptest,intel,native,golden}` verbatim from
`decimal128-java/core/src/test/resources/` (or the Swift `Tests/.../Resources`)
into the C test tree and load by file path. Target (Kotlin hits this with **0
failures** on both JVM and native):

| corpus | passed | skipped |
|---|---|---|
| IBM dectest | 12388 | 160 |
| fptest | 24602 | 0 |
| Intel RDFP (`readtest.in`) | 14283 | 43 |

Plus `golden/*_logexp.txt` (ln/log10/exp/exp10 bit-exact oracle — exercised only
once Phase G lands) and the direct unit tests.

--------------------------------------------------------------------------------
## 6. Phased plan

Each phase compiles green and is validated by the corpus vectors its arms unlock
before the next begins. CMake/CTest throughout, mirroring `primitive/`'s setup
(`VERIFY_ENABLED=1`, GMP only where an oracle is needed, fork-based death tests
for traps).

**Phase 0 — primitive seam audit + core scaffold.**
- ~~Seam audit + fill~~ **DONE** (§0, §4) — all seam symbols added, primitive
  renamed to PascalCase, 21/21 ctest.
- **← START HERE.** Create `core/` (CMakeLists, `include/`, `src/`, `tests/`);
  wire `add_subdirectory(core)` in the top-level `CMakeLists.txt`; confirm `core`
  links against `primitive` and builds empty. Use PascalCase file names (§3).

**Phase A — value/enum/context tier (tier 1).**
- Exception754, Comparison754, InvalidCause, ParseStatus, Round, Flags, Context,
  AsciiPrintBuffer, D128Constants. Small, dependency-free, unblocks everything.

**Phase B — D128 type + decode/parse surface (tier 2).**
- `D128` struct + D128Constants + D128NonComputational.
- The decode/parse/compare surface Rosetta-infra needs: SerdeBid/SerdeDpd
  *decode* paths, `d128_parse_ctx`, `d128_bitwiseEQ`.

**Phase R0 — Rosetta-infra standup (de-risks the whole harness).**
- All four parsers + `RosettaText` + dialect decoders + include/exclude maps +
  the coverage meta-tests (incl. the every-arm-registered check, §5); wire one
  trivial dispatch arm.
- Copy the four corpora into the test tree; confirm the `fopen` loader path.
- Exit: pipeline reads all four sources; partition meta-tests green; the one arm
  validates against its vectors. Harness proven independent of ~88 ops.

**Phase C — finalize + divPow10 core dispatch (tiers 3–4).**
- Finalize/Round machinery and the Core divPow10 family (incl. U256Div,
  U256Sqrt). The rounding heart all arithmetic depends on.

**Phase D — IEEE-required arithmetic + D38 (tiers 5–6).**
- D38 engine first (D38AddSub/Compare/Div/Fma/Finalize/RoundToIntegral/Sqrt),
  then D128 ops in order: add/sub → mul → div → compare → fma. Wire each op's
  dispatch arm as it lands; corpus vectors validate immediately.

**Phase E — serde (encode) + text (tiers 7–8).**
- SerdeBid/SerdeDpd encode paths, D128Parse, D128Print, IntegerParsePrint
  (ASCII `uint8_t[64]` scratch, no library `String`).

**Phase F — sqrt + remaining IEEE-required tail (tier 9, required subset).**
- D128Sqrt, D128MinMax, D128CtxMinMax, D128ToIntegral, D128NextUpDown,
  D128TotalOrder, D128StripTrailingZeros, D128LogBScaleB, BExpMinMax + their arms.

**Phase G — transcendentals (deferred ordering).**
- D128Exp, D128Log (ln/log10) + D38 Padé support + D128ExpConstants /
  D128LogConstants and their arms. The `golden/*_logexp.txt` oracle activates
  here. Last, per IEEE-required-first.

Validation is continuous (corpus vectors per arm) — there is no separate
end-stage validation phase.

--------------------------------------------------------------------------------
## 7. Risks / things to budget for

- **Primitive seam (Phase 0).** The most likely thing to stall the core build.
  Audit and fill *before* porting core, not on demand.
- **Unsigned 64-bit table literals.** Use explicit `UINT64_C(...)` / `ULL`; the
  top-bit-set table constants are where transcription bugs hide. **Generate
  tables from the shared Swift/Java source**, do not hand-transcribe.
- **No silent corruption guard.** A wrong shift compiles fine and returns wrong
  bits with no error. Stand up Rosetta early (Phase R0) so correctness is
  machine-checked, not assumed. Cross-check against Java/Kotlin when a Swift
  result is ambiguous — both pass the full corpus, so a divergence is a port bug.
- **`RosettaText`** — the one exacting reimplementation (tokenize / hasPrefix /
  trim / indexOf against C strings). Get it green against the parser tests first.
- **Hex operand decoders** (`#`DPD / `[hex]`BID) must match Swift bit-for-bit;
  the native-source strict path (no skips, R§12) is the early canary.
- **`CanonicalOp` arm completeness.** C has no exhaustive-switch safety net; the
  every-arm-registered meta-test (§5) is the substitute — make it loud.
- **CRLF.** Some dectest corpora are CRLF; the line splitter must drop a trailing
  `\r`.
- **`int32_t` narrowing watch.** Swift uses 64-bit `Int` for loop counters and
  indices, not just qExp. Transliterating to `int32_t` is correct (all counts are
  small), but any Swift `Int` that could legitimately exceed 2³¹ is a signal to
  look closer rather than blindly narrow. None expected in this codebase.

--------------------------------------------------------------------------------
## 8. Settled vs open

**Settled:** target module (`decimal128-c/core`, CMake sibling of `primitive`);
value-return struct memory model + no heap (matches Swift and the C Primitive);
`int32_t` for in-memory scalars; IEEE-required-first ordering; Rosetta ported to
C and co-evolved with Core (not the swift-over-C wrapper path); dword-struct
U128/U256 with native `__int128` confined to Primitive bodies; `verify` macro /
`_Noreturn impossible` reused from the C Primitive.

**Open (revisit later, not blocking):** exact core file-name casing convention
(confirm against `primitive/`'s established style at Phase A); whether the
wrapper layer (swift-over-C, etc.) follows after a green core + Rosetta; the
final home/name of this plan doc; production messaging for `demand`/`impossible`.
