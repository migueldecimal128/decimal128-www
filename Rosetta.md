Rosetta.md
Thu 11 Jun 2026  ·  updated to reflect the implemented state

Plan (now implemented) to consolidate the decimal128 test harnesses — fptest,
Intel, and dectest — into one runner over a single canonical test-case format.

The name is the point. The Rosetta Stone carried the same text in three
scripts; the three decimal floating point test suites carry the same information — operation, operands,
result, flags — in three encodings. The job is to decode them into one
canonical language. And there is a second translation underneath: the
canonical harness is then ported to Kotlin, Java, and C. Rosetta is about
both axes — many formats into one, one harness into four languages.

STATUS (2026-06-11). The Swift consolidation is COMPLETE (Phases 0–4): one
canonical harness in Tests/Decimal128Tests/rosetta/ runs all three corpora
through one dispatch core; the legacy per-op runners are gone. Two things have
been added since the original plan and are folded into the sections below:
  - a FOURTH source, `native` — hand-authored, born-canonical test lines (§12);
  - a portability-hardening pass that realizes P1 in the harness code itself:
    the canonical op is now an `Int`-backed `CanonicalOp` enum (§6), the dispatch
    returns a `DispatchResult` struct (§7), all text munging is behind a
    `RosettaText` primitive layer (§5), and the port-path uses only the portable
    subset — counted `while` loops, named functions (no operator overloads),
    structs (no tuples), no closures/HOFs, and no optionals across seams (§13).


================================================================================
1. Why
================================================================================

fptest, Intel, and dectest encode the same thing: operation, operands, result
value, result flags. dectest additionally carries per-block *context*
(precision, min/max exponent) from its directives.

Today there are three separate harnesses:

  - IntelRunnerCtx   — ~12 typed runner methods, hex-BID operands, hex flag byte
  - DectestRunnerCtx — ~5 typed runner methods, directive context, DPD operands
  - TestFptestDecimal — one bespoke `test1`, numeric comparison, letter flags

They duplicate the same loop (parse → build context → decode operands → run →
compare result → check flags) three times, in three shapes, and all of it has
to be ported to three more languages. Rosetta replaces the three with one.


================================================================================
2. Governing principles
================================================================================

These drove every decision below; when in doubt, defer to them.

P1. The Swift harness is the *reference that ports mechanically*. Express the
    core only with constructs that have clean analogues in Swift, Kotlin, Java,
    and C. No generics over result type, no curried-closure-as-parameter, no
    protocol associated types in the core path.

P2. Maximize the uniform shared core; push every format quirk into a localized,
    isolated step (one block, gated by source or operation name).

P3. Bitwise equality everywhere. Result comparison is `d128_bitwiseEQ` for
    every suite. Comparison is no longer a per-format axis.

P4. One canonical flag format, stored as data (§4).

P5. A conscious include/exclude decision on *every* operator (§6). Silence is
    an error, not a skip.


================================================================================
3. RosettaCase — the canonical test case (pure data)
================================================================================

One neutral value type that every parser produces. Everything is a string or a
small int (the canonical op is an `Int`-backed enum) — trivially serializable,
trivially portable.

    enum Source { case fptest, intel, dectest, native }   // native: §12

    struct RosettaCase {
        let source: Source
        let text: String           // original line, for diagnostics
        let canonicalOp: CanonicalOp  // resolved by stage-1 map; the stage-2 dispatch key (§6)
        let operands: [String]     // 1...3, verbatim from the source
        let resultStr: String      // verbatim from the source
        let expectedFlags: String  // canonical letter string, see §4
        let rounding: String       // Round's SCREAMING_SNAKE case name; → Round at ctx build
        // source-specific raw metadata used only by quirk steps (§8)
        let traps: String?         // fptest trap column; nil elsewhere
    }

No precision/exponent context fields: the library is always and only
decimal128 (precision 34, Emax 6144, Emin -6143), so they would be constants
masquerading as data. Their one consumer — restricting dectest's multi-
precision ln/exp/log10 blocks to precision 34 — is a PARSE-TIME vector filter:
the dectest parser drops a non-34 block, so it never becomes a RosettaCase (it is not
carried and guarded at run time).

Operand and result strings stay verbatim. Decoding to D128/Int/Bool is the
dialect's job (§5), done at run time, because each suite encodes operands
differently.


================================================================================
4. Canonical flag format
================================================================================

The standard flag representation is fptest's letter string — already the de
facto lingua franca: `Flags.getFptestExceptionsString()` renders any `Flags`
to it in fixed `xuozi` order, and the Intel and dectest runners already call it
for diagnostics.

    x = inexact   u = underflow   o = overflow   z = divByZero   i = invalid

These five letters are exactly the five `Exception754` flags the library
tracks. dectest's non-mapping conditions (clamped, rounded, subnormal,
lost_digits, ...) and Intel's 0x02 "unnormal" already have no flag counterpart
and are dropped today — no behavior change.

Rules:

  - Each parser builds expected flags by *setting bits on a `Flags` then
    rendering through the one function* — never by hand-concatenating native
    tokens. This guarantees canonical `xuozi` order and dedup, so "ox" can
    never miscompare against "xo". Empty set → "".
  - Comparison is canonical string equality: render `ctx.flags` through the
    same function, string-compare to `RosettaCase.expectedFlags`. That *is* the "exact
    flags everywhere" rule.
  - The flag string is the *signaled-exceptions* column only. fptest's separate
    *trap* column is input metadata for the trap un-wrap normalize step (§8),
    NOT the expected flags.

Cleanup: `getFptestExceptionsString()` is now a misnomer (it is neither
fptest-specific nor dectest-specific — it is *the* standard). Rename to a
neutral `exceptionLetters()`. This touches the Intel/dectest diagnostics too.


================================================================================
5. Parsers and the dialect
================================================================================

Four parsers, each producing `[RosettaCase]`:

  - IntelParser   — keep line tokenization, flag-byte decode, rounding-int
                    decode. Emit RosettaCase with canonical flags + a canonical rounding string.
  - DectestParser — keep directive accumulation (precision/min/maxExp/rounding),
                    `->` split, condition tokens. Emit RosettaCase carrying its context.
  - FptestParser  — promote the inline `Fptest` struct in TestFptestDecimal to a
                    first-class parser. Decode `=0 > < 0 =^` rounding, `xuozi`
                    flags, trap column → RosettaCase.traps.
  - NativeParser  — the 4th source (§12): a native line IS a printed RosettaCase,
                    so the parse is trivial (split the canonical fields) and there
                    is no stage-1 map — it is born canonical.

All four call the same text primitives (tokenize, hasPrefix, trim, …), which
live behind named functions in `RosettaText` so the Foundation/Swift string
idioms are confined to ONE file the port reimplements (§13).

Canonical rounding vocabulary — the strings stored in `RosettaCase.rounding` are `Round`'s
own SCREAMING_SNAKE_CASE case names, so the runner's string→`Round` step is a
direct lookup (and ports as data):

    TIES_TO_EVEN   TIES_TO_AWAY   TOWARD_POSITIVE   TOWARD_NEGATIVE   TOWARD_ZERO

Each parser maps its native rounding into one of these:

    intel:   0/1/2/3/4   -> TIES_TO_EVEN / TOWARD_NEGATIVE / TOWARD_POSITIVE /
                            TOWARD_ZERO / TIES_TO_AWAY
    dectest: half_even/half_up/ceiling/floor/down -> the matching name;
             up / 05up / half_down are unsupported -> those blocks' cases are
             filtered (§7)
    fptest:  =0/=^/>/</0 -> TIES_TO_EVEN / TIES_TO_AWAY / TOWARD_POSITIVE /
                            TOWARD_NEGATIVE / TOWARD_ZERO

What still differs per source at *run* time is the operand/result *encoding*.
That is the dialect — a small table of decode functions, selected by
`RosettaCase.source`:

    decodeOperand(_ s: String, _ ctx: Context) -> D128
        intel:   "[hex]" BID (bid128ParseIntelHex → d128_fromBID) or decimal
        dectest: "#"DPD (dpd128ParseDecTestHex → d128_fromDPD) or d128_parse_ctx
                 (observes parse-time flags on ctx)
        fptest:  "Q"/"S" → QNAN0/SNAN0, else d128_parseOrNaN
        native:  all forms (Q/S, "#"DPD, "[hex]" BID, else decimal); a malformed
                 string is a loud authoring error, not a silent NaN

    decodeResult is the same family, plus the primitive parses (Int/Int64/Bool)
    used by non-D128 result arms.

The dialect holds *only* parse-side hooks now — comparison is uniform (P3), so
there is no comparator field.


================================================================================
6. Two-stage operation mapping
================================================================================

STAGE 1 — source-specific normalization. Each source has TWO maps that
*partition* its operator universe (native is the exception: it is born
canonical, so it has no stage-1 map — §12):

    intelInclude:  "bid128_add"  -> .d128_add_ctx       // conscious INCLUDE
                   "bid128_mul"  -> .d128_multiply_ctx
                   ...
    intelExclude:  "bid128_sin"  -> "trig — not required by IEEE 754 decimal"
                   "bid128_cos"  -> "trig — out of scope"
                   ...

The exclusion map is a blacklist that *carries a reason* — the decision is
documented, not just made. It echoes the existing decision log (nextafter
declined, dq rotate/shift won't-do, etc.).

The canonical key is a `CanonicalOp` enum case whose identifier IS the
function-name mnemonic (`d128_add_ctx`). It reads like the Swift symbol but
nothing resolves it reflectively — the stage-2 switch is explicit. C cannot
`switch` on a string, so the port must turn the token into an int before dispatch
regardless; making the Swift reference key on the enum keeps all four switches
identical (§13). So Kotlin/Java/C reuse the same enum; only stage 2 changes per
language.

INVARIANT (enforced by a meta-test per source — `testIntelOperatorCoverage`,
etc.): every distinct operator token that appears in the corpus is in EXACTLY
ONE of {include, exclude}.

  - in NEITHER  -> hard error: "undecided operator 'bid128_foo' — add to
                   include or exclude map"
  - in BOTH     -> hard error: "contradictory decision for 'bid128_foo'"

This proves a conscious decision exists for every function, catches corpus
drift loudly (a new op in a refreshed readtest.in fails the build until
decided), and doubles as the coverage report: include.keys = what we test,
exclude = what we consciously skip, with reasons. No third "unknown" bucket
can exist. Both maps are pure String→CanonicalOp data (i.e. String→Int) and
port verbatim.

STAGE 2 — dispatch. One shared switch whose entire vocabulary is `CanonicalOp`
cases. By the time a case reaches it, the source format is fully behind us:
the switch never sees "+", "bid128_add", or "add".

    switch tc.canonicalOp {
      case .d128_add_ctx:      ...        // arm knows it returns D128
      case .d128_compare_ctx:  ...        // arm knows it returns Comparison754
      case .d128_isNaN:        ...        // arm knows it returns Bool
      ...
    }                                     // EXHAUSTIVE — no `default`

One arm per function, period — not functions × suites. The set of case labels
IS the list of operations the harness tests. The switch is exhaustive over
CanonicalOp (no `default`), so a new op without an arm is a COMPILE error, not a
runtime "no arm" — the old not-yet-wired histogram is therefore gone.


================================================================================
7. Result shape without generics — the tagged union
================================================================================

The old ~17 typed runner methods existed only to carry heterogeneous result
types (D128 / Bool / Int / Int64 / String / Comparison754). Generics would
solve that in Swift but not in C (P1). The portable device is a tagged union:

    enum ResultValue {
        case dec(D128)
        case int(Int64)
        case bool(Bool)
        case cmp(Comparison754)
        case str(String)
    }

In C this is a `{ kind; union }` struct; in Kotlin/Java a sealed type. Every
dispatch arm returns BOTH the observed and the expected as a `ResultValue` of
the same kind — the arm knows its return type and how to parse the expected
string, so no metadata table is needed. The pair is a struct, not a tuple (C has
no tuples), and the return is non-optional (the switch is exhaustive):

    struct DispatchResult { let observed: ResultValue; let expected: ResultValue }

    func run(_ tc: RosettaCase, _ ctx: Context) -> DispatchResult

The arm decodes the operands it needs through the dialect on the LIVE ctx,
left-to-right (dectest accumulates parse flags in operand order). The runner
loop then compares by kind via the NAMED function `ResultValue.equalsByKind`
(not an `==` overload — §13) — `.dec` → `d128_bitwiseEQ`, everything else → value
equality — and compares the flag strings (§4). One comparison site, not 17.


================================================================================
8. Isolated quirk steps
================================================================================

Per P2, the messy reconciliations live in localized blocks the uniform core
never has to know about.

INTEL EXPECTATION NORMALIZE (gated source == .intel, applied to *expected*
inside the relevant D128/Int arms):

  - NaN payload: Intel "first-NaN-wins" → GDAS "sNaN-prefers"
    (rewriteIntelNaNExpectation, and the ternary form for fma).
  - maxnum/minnum/maxnum_mag/minnum_mag: sNaN handling + equal-value cohort tie
    (rewriteIntelNumberExpectation).
  - int-returning invalid sentinel: accept Int.min or Int32.min when invalid is
    signaled (folded into the `.int` arm compare).

FPTEST EXPECTATION NORMALIZE — trap un-wrap (gated source == .fptest, applied
to *expected* inside the D128 arm). This is the resolution of Phase 0's
trap-wrapped question: it is a value TRANSFORM, not a skip.

  An fptest line with a `traps` column has the overflow/underflow trap enabled,
  so it carries the IEEE 754-1985 trap-handler's *wrapped* result: the true
  value with its exponent offset by ±bias so it is representable for the handler
  to inspect. For decimal128 the bias is 9216 = 3·Emax/2 (the 1985 binary trap
  formula 3·2^(w−2) — 192 single, 1536 double — generalized to decimal). NOTE
  the provenance: the wrap is the 1985 trap model, dropped from 754-2008/2019
  default handling; "9216" is not printed in current 754 — it is what the
  fptest/FPgen corpus encodes.

  This non-trapping, 754-2019-default library delivers ±inf (overflow) or the
  subnormal/zero (underflow) instead. The wrapped *value* is recoverable, so we
  un-wrap rather than skip: scale the expected back by the bias with the test's
  rounding context, which re-applies the same range-clamp/rounding the operator
  did, and bit-compare against the observed default result.

    - overflow  (`scaleB(expected, +9216)`): re-overflows to ±inf / largest
      finite. Gated on our own result having overflowed (`ctx.isOverflow()`).
    - underflow (`scaleB(expected, −9216)`): re-rounds onto the subnormal grid.
      Gated on our result being finite and non-normal.
    `trapWrapDelta(...) -> Int?` (formerly the skip predicate `isBadCase`)
    returns the scaleB delta or nil. All such vectors reconcile bit-for-bit
    (603 overflow + 300 exact-underflow; no inexact-underflow in the corpus).

  The signaled-FLAG column is NOT checked for these vectors — it follows 1985
  trap conventions (overflow without the implied inexact; tininess-before-
  rounding underflow) this library does not mirror. Only the value is asserted.
  (Trapping itself is unimplemented but planned; the value is identical
  regardless of delivery, and "was the handler's value used" is a separate
  future test.)

VECTOR FILTER (per-source skip of individual erroneous/out-of-scope *lines*
within an *included* operator — distinct from the operator-level exclusion of
§6):

  - fptest `u` tininess divergence: with flags now compared exactly (P3, §4),
    the `u`-divergent vectors go on this skip list rather than relaxing the flag
    comparison (resolution pending — see §10). Distinct from the trap un-wrap
    above: these are non-trapped lines where tininess detection itself differs.
  - Intel per-line skip lists; dectest `#` encoding placeholders and
    unsupported-rounding blocks (up / 05up / half_down).

LADDER SIBLINGS (orthogonal, retained): the `_rnd` / `_tte` / quiet no-flag-sink
forms checked bit-identical against the `_ctx` result, for every source (internal
consistency is source-independent). `RosettaSiblings.check` re-decodes the
operands on a throwaway ctx and compares each applicable sibling; the sibling
list is `[Sibling { label; value }]` (a struct, not a `(String, D128)` tuple).

NATIVE has NO quirk steps: a native case (§12) is born canonical and takes the
plain reconcile path (value-by-kind + flags-exact) with no normalize, no
trap-unwrap, and no skip filters.


================================================================================
9. Phasing
================================================================================

PHASE 0 — fptest → bitwise (BEFORE anything else; de-risks the whole plan).
  DONE. Result comparison switched compareQuiet754 → d128_bitwiseEQ; `#`/d64
  skips kept; getFptestExceptionsString() → exceptionLetters() (§4).
  - Triage: ZERO bitwise fallout — the library already produces bit-exact
    cohorts, signs, and NaN payloads. No real bugs, no new filter material.
  - The trap-wrapped vectors were NOT left as skips: they became the trap
    un-wrap NORMALIZE step (§8) — 903 vectors (603 overflow + 300 exact-
    underflow) reconcile bit-for-bit, converting skips into real coverage.
  - The `u` flag question was not forced (no value mismatch depended on it); it
    stays the one open `u`-divergence vector-filter item (§10).
  Exit (met): fptest green under bitwise comparison.

PHASE 1 — canonical model.
  - Add Source, RosettaCase, ResultValue, canonical flag rendering.
  - Three parser variants emitting [RosettaCase] (reuse existing parse logic).
  - Three include/exclude map pairs + the operator-coverage meta-tests.
  Exit: every corpus operator is consciously include/exclude; meta-tests green.

PHASE 2 — the engine.
  - Dialect decoders (per-source operand/result).
  - Stage-2 dispatch switch + the runner loop + by-kind comparison.
  - Intel-normalize and vector-filter quirk steps; sibling checks.
  Exit: Rosetta runs all three corpora directly, parity with today's results.

PHASE 3 — shims (zero churn).
  - Reimplement IntelRunnerCtx.* / DectestRunnerCtx.* entry points and the
    fptest test as thin wrappers over the Rosetta core. The ~90 existing test
    files keep compiling and passing unchanged.
  Exit: old names delegate to Rosetta; full suite green.

PHASE 4 — migrate (later, separate pass).
  DONE. Moved call sites onto Rosetta; deleted ~85 legacy files (80 per-op tests
  + 3 legacy runners + sibling/env helpers). Coverage now comes from the three
  parity sweeps + the meta-tests; 100 hand-written _2019 cases are preserved in
  _754_2019.dectest.

PHASE 5 — native source. DONE. Added `native` as the 4th Source (§12): a
  born-canonical printed-RosettaCase format for ops/arms no corpus exercises
  (propagate min/max, specific FormatStyles, hand-built NaN payloads).

PHASE 6 — portability hardening (§13). DONE. Tightened the harness code to the
  portable subset so the C/Java/Kotlin dispatch transliterates line-by-line:
  CanonicalOp enum, exhaustive switch, DispatchResult struct, RosettaText
  primitive layer, counted while-loops (no HOFs/for-in/closures), named
  equalsByKind (no operator overload), Sibling struct (no tuple).

(Phases 1–3 — canonical model, engine, shims — are likewise complete; see the
STATUS note at the top.)


================================================================================
10. Open items / risks
================================================================================

  - [RESOLVED — Phase 0] fptest bitwise fallout: ZERO. No real bugs, no new
    filter material; trap-wrapped vectors handled by the §8 un-wrap normalize.
  - [OPEN] The `u` tininess flag divergence: skip the divergent vectors
    (current plan), or is it a real tininess-detection bug to fix? Not forced by
    Phase 0 (no value mismatch depended on it). Note these are the *non-trapped*
    underflow lines — the trapped ones are now value-asserted via §8 and their
    1985-convention flags are deliberately not checked.
  - [RESOLVED] dectest variable precision: RosettaCase carries NO precision/exponent
    fields (library is always decimal128). The multi-precision transcendental
    blocks (ln/exp/log10) are dropped at PARSE time — a vector filter that never
    emits a RosettaCase for a non-precision-34 block, not a carried context guard.
  - [OPEN] NaN bitwise exactness for dectest/fptest payloads beyond the Intel
    divergences already handled by the normalize step.


================================================================================
11. What ports verbatim vs per-language
================================================================================

  VERBATIM (shared data / logic; transliterates mechanically):
    RosettaCase, ResultValue, DispatchResult, Source, CanonicalOp; the four
    parsers; the include/exclude map pairs and their reasons; canonical flag
    rendering; the runner loop and by-kind comparison (equalsByKind); the
    vector-filter skip lists; the Intel-normalize logic; the counted-loop bodies.

  PER-LANGUAGE (the artifacts that genuinely differ):
    1. the stage-2 dispatch switch BODIES — they hold the actual library calls,
       and the function symbols differ per language. Its *keys* are the shared
       CanonicalOp cases (Int-backed).
    2. the `RosettaText` primitive BODIES — the host's string API (or
       strtok/strncmp/strchr/…); the parsers call only the named primitives.
    3. `CanonicalOp.name` / `.byName` — the explicit enum↔string maps (C/Java/
       Kotlin spell the enum and its name table their own way).

  Everything outside those three transliterates; see §13 for the discipline that
  makes that true.


================================================================================
12. The native source (the 4th source)
================================================================================

`native` is a fourth `Source`, added after the original three-corpus plan. A
native line IS a printed `RosettaCase`: it is born canonical, so it has NO
stage-1 map and NO quirk steps — it goes straight to the stage-2 switch and the
plain reconcile path (value-by-kind + flags-exact). It exists to test ops and
arms that no external corpus exercises (the NaN-propagating min/max forms,
specific FormatStyles, hand-built NaN payloads, isQNaN, toExp/toRaw, …).

Line format (whitespace-separated; `//` and blank lines ignored):

    <canonicalOp> <ROUNDING> <op1> [op2 [op3]] -> <result> [flags]

    d128_add_ctx     TIES_TO_EVEN  1.5  2.5  -> 4.0
    d128_divide_ctx  TIES_TO_EVEN  1    3    -> 0.3333333333333333333333333333333333  x
    d128_isLess_ctx  TIES_TO_EVEN  -Inf 0    -> 1

  - <canonicalOp> is a CanonicalOp NAME (the mnemonic), resolved via
    `CanonicalOp.byName` — the inverse of `CanonicalOp.name`. Unknown → loud error.
  - <ROUNDING> is Round's SCREAMING_SNAKE name (the same vocabulary as §5).
  - operands/result are decimal strings, with `Q`/`S` (payload-0 NaNs), `#`DPD,
    and `[hex]` BID available for exact NaN payloads / bit patterns.
  - flags are the canonical `xuozi` letters (§4), rendered through the one
    function so order/dedup are canonical.

Native is STRICTER than the corpus paths: it has no skip filters (a skipped case
is a failure), and — because the stage-2 switch is exhaustive over CanonicalOp —
a missing arm is a compile error, not a runtime skip. Cases live as
`Tests/Decimal128Tests/Resources/native/*.txt`, plus inline lines and an
`assertOne` single-line path for debugging. A handful of structurally bespoke
checks (parse round-trips, sqrt-bracket, raw NaN-payload getters) stay outside
the native format on purpose.


================================================================================
13. Portability hardening (realizing P1 in the harness code)
================================================================================

P1 asks for a Swift reference that *ports mechanically*. The original plan met
that at the design level (tagged union not generics, opaque keys not reflection).
A follow-up pass tightened the harness CODE to the portable subset, so the
C/Java/Kotlin dispatch transliterates line-by-line instead of being reinvented:

  - CANONICAL OP IS AN ENUM. The canonical key is an `Int`-backed `CanonicalOp`
    enum whose case identifiers ARE the function-name mnemonics (`d128_add_ctx`,
    `d128_isFinite`). C cannot `switch` on a string, so the port must turn the
    token into an int before dispatch anyway; keying the Swift reference on the
    enum keeps all four switches identical. The include maps are
    `String→CanonicalOp` (i.e. String→Int) — as portable as the former
    String→String. The stage-2 switch is EXHAUSTIVE (no `default`): a new op
    without an arm is a compile error, not a runtime "no arm". `CanonicalOp.name`
    is an explicit (non-reflective) switch; `byName` its inverse, used by native.

  - STRUCTS, NOT TUPLES. Dispatch returns `DispatchResult { observed; expected }`
    (a C struct / JVM class). The sibling list is `[Sibling { label; value }]`,
    not `[(String, D128)]`.

  - NAMED FUNCTIONS, NOT OPERATORS. `ResultValue` by-kind equality is
    `ResultValue.equalsByKind(a, b)`, not an `==` overload.

  - A TEXT-PRIMITIVE LAYER. Every Foundation/Swift string idiom the parsers need
    (tokenize, split-lines, hasPrefix, take/drop, trim, removingChar, allCharsIn,
    indexOf→-1) lives behind named primitives in `RosettaText`. The parser bodies
    call only these; the port reimplements ONE file (strtok/strncmp/strchr/…) and
    the parsers transliterate unchanged.

  - COUNTED LOOPS, NO HOFs/CLOSURES. The port-path logic uses the counted-loop
    idiom (`var i = 0; while i < n { … ; i += 1 }`, braces always) — no `map`/
    `filter`/`compactMap`, no `for-in`, no nested capturing closures. (Diagnostic
    `print`/`joined` and the `@Test` bodies stay idiomatic — they are scaffolding,
    not ported logic.)

  - NO SEAM OPTIONALS. The optional dispatch return is gone (exhaustive switch);
    the one `D128?` sibling optional became a Bool gate. The remaining `-> T?`
    parser returns ("is this line a case?") are the one acknowledged boundary
    optional, mapping to C's `bool f(out T)`.

What is deliberately NOT yet converted (idiomatic, low-value to force now):
`guard … else`, `Set`/dictionary literals, and the parser `-> T?` returns above.
