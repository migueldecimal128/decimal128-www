Rosetta.md
Thu 11 Jun 2026

Plan to consolidate the three decimal128 test harnesses — fptest, Intel, and
dectest — into one runner over a single canonical test-case format.

The name is the point. The Rosetta Stone carried the same text in three
scripts; our three suites carry the same information — operation, operands,
result, flags — in three encodings. The job is to decode all three into one
canonical language. And there is a second translation underneath: the
canonical harness is then ported to Kotlin, Java, and C. Rosetta is about
both axes — three formats into one, one harness into four languages.


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
3. TC — the canonical test case (pure data)
================================================================================

One neutral value type that all three parsers produce. Everything is a string
or a small int — trivially serializable, trivially portable.

    enum Source { case fptest, intel, dectest }

    struct TC {
        let source: Source
        let text: String          // original line, for diagnostics
        let canonicalOp: String   // resolved by stage-1 map; == a function name key
        let operands: [String]    // 1...3, verbatim from the source
        let resultStr: String     // verbatim from the source
        let expectedFlags: String // canonical letter string, see §4
        let rounding: String      // Round's SCREAMING_SNAKE case name; → Round at ctx build
        // context — defaults for intel/fptest, directive-derived for dectest
        let precision: Int        // 34 unless dectest says otherwise
        let maxExp: Int           // 6144
        let minExp: Int           // -6143
        // source-specific raw metadata used only by quirk steps (§7)
        let traps: String?        // fptest trap column; nil elsewhere
    }

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
    same function, string-compare to `TC.expectedFlags`. That *is* the "exact
    flags everywhere" rule.
  - The flag string is the *signaled-exceptions* column only. fptest's separate
    *trap* column is input metadata for the vector-filter (§7), NOT the
    expected flags.

Cleanup: `getFptestExceptionsString()` is now a misnomer (it is neither
fptest-specific nor dectest-specific — it is *the* standard). Rename to a
neutral `exceptionLetters()`. This touches the Intel/dectest diagnostics too.


================================================================================
5. Parsers and the dialect
================================================================================

Three parsers, each a variant of the existing one, each producing `[TC]`:

  - IntelParser   — keep line tokenization, flag-byte decode, rounding-int
                    decode. Emit TC with canonical flags + a canonical rounding string.
  - DectestParser — keep directive accumulation (precision/min/maxExp/rounding),
                    `->` split, condition tokens. Emit TC carrying its context.
  - FptestParser  — promote the inline `Fptest` struct in TestFptestDecimal to a
                    first-class parser. Decode `=0 > < 0 =^` rounding, `xuozi`
                    flags, trap column → TC.traps.

Canonical rounding vocabulary — the strings stored in `TC.rounding` are `Round`'s
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
`TC.source`:

    decodeOperand(_ s: String, _ ctx: Context) -> D128
        intel:   "[hex]" BID (bid128ParseIntelHex → d128_fromBID) or decimal
        dectest: "#"DPD (dpd128ParseDecTestHex → d128_fromDPD) or d128_parse_ctx
                 (observes parse-time flags on ctx)
        fptest:  "Q"/"S" → QNAN0/SNAN0, else d128_parseOrNaN

    decodeResult is the same family, plus the primitive parses (Int/Int64/Bool)
    used by non-D128 result arms.

The dialect holds *only* parse-side hooks now — comparison is uniform (P3), so
there is no comparator field.


================================================================================
6. Two-stage operation mapping
================================================================================

STAGE 1 — source-specific normalization. Each source has TWO maps that
*partition* its operator universe:

    intelInclude:  "bid128_add"  -> "d128_add_ctx"      // conscious INCLUDE
                   "bid128_mul"  -> "d128_multiply_ctx"
                   ...
    intelExclude:  "bid128_sin"  -> "trig — not required by IEEE 754 decimal"
                   "bid128_cos"  -> "trig — out of scope"
                   ...

The exclusion map is a blacklist that *carries a reason* — the decision is
documented, not just made. It echoes the existing decision log (nextafter
declined, dq rotate/shift won't-do, etc.).

The canonical string IS the function name, treated as an *opaque key*. It looks
like the Swift symbol as a mnemonic, but nothing resolves it reflectively — the
stage-2 switch is explicit. So Kotlin/Java/C reuse the same keys; only stage 2
changes per language.

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
can exist. Both maps are pure string→string data and port verbatim.

STAGE 2 — dispatch. One shared switch whose entire vocabulary is canonical
names. By the time a case reaches it, the source format is fully behind us:
the switch never sees "+", "bid128_add", or "add".

    switch tc.canonicalOp {
      case "d128_add_ctx":      ...        // arm knows it returns D128
      case "d128_compare_ctx":  ...        // arm knows it returns Comparison754
      case "d128_isNAN":        ...        // arm knows it returns Bool
      ...
    }

One arm per function, period — not functions × suites. The set of case labels
IS the list of operations the harness tests.


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
string, so no metadata table is needed:

    func dispatch(_ tc: TC, _ a: D128, _ b: D128, _ c: D128,
                  _ ctx: Context) -> (observed: ResultValue, expected: ResultValue)

The runner loop then compares by kind — `.dec` → `d128_bitwiseEQ`, everything
else → `==` — and compares the flag strings (§4). One comparison site, not 17.


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

VECTOR FILTER (per-source skip of individual erroneous/out-of-scope *lines*
within an *included* operator — distinct from the operator-level exclusion of
§6):

  - fptest trap-wrapped overflow/underflow: fptest expects the IEEE
    trap-handler's ±9216-biased result; this non-trapping library delivers the
    default (±inf / subnormal). The `isBadCase` logic moves here.
  - fptest `u` tininess divergence: with flags now compared exactly (P3, §4),
    the `u`-divergent vectors go on this skip list rather than relaxing the flag
    comparison (resolution pending Phase 0 — see §10).
  - Intel per-line skip lists; dectest `#` encoding placeholders and
    unsupported-rounding blocks (up / 05up / half_down).

LADDER SIBLINGS (orthogonal, retained): the `_rnd` / `_tte` / quiet no-flag-sink
forms checked bit-identical against the `_ctx` result. Keep BinarySibling /
TernarySibling; the D128 arms invoke them.


================================================================================
9. Phasing
================================================================================

PHASE 0 — fptest → bitwise (BEFORE anything else; de-risks the whole plan).
  - In the existing TestFptestDecimal, switch result comparison from
    compareQuiet754 (numeric) to d128_bitwiseEQ. Keep the trap-wrapped filter
    and the `#`/d64 skips.
  - Triage the fallout: cohort mismatches or NaN-payload mismatches are either
    (a) real bugs, surfaced with numbers, or (b) vectors for the filter.
  - Decide the `u` flag question with data in hand (§10).
  - Rename getFptestExceptionsString() → exceptionLetters() (§4).
  Exit: fptest green under bitwise comparison.

PHASE 1 — canonical model.
  - Add Source, TC, ResultValue, canonical flag rendering.
  - Three parser variants emitting [TC] (reuse existing parse logic).
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
  - Move call sites onto Rosetta directly; delete the old runner types.


================================================================================
10. Open items / risks
================================================================================

  - Phase 0 fallout: how many fptest vectors fail under bitwise, and how they
    split between real bugs and filter material. Unknown until run.
  - The `u` tininess flag divergence: skip the divergent vectors (current
    plan), or is it a real tininess-detection bug to fix? Decide in Phase 0.
  - dectest variable precision: the multi-precision transcendental files
    (ln/exp/log10) carry blocks at many precisions; the library is fixed
    decimal128. TC carries precision, but the runner must keep restricting to
    the precision-34 blocks (today's precisionFilter) — as a vector filter or a
    context guard. Confirm placement.
  - NaN bitwise exactness for dectest/fptest payloads beyond the Intel
    divergences already handled by the normalize step.


================================================================================
11. What ports verbatim vs per-language
================================================================================

  VERBATIM (shared data / logic; transliterates mechanically):
    TC, ResultValue, Source; the three parsers; the include/exclude map pairs
    and their reasons; canonical flag rendering; the runner loop and by-kind
    comparison; the vector-filter skip lists; the Intel-normalize logic.

  PER-LANGUAGE (the one artifact that genuinely differs):
    the stage-2 dispatch switch bodies — because they hold the actual library
    calls, and the function symbols differ per language. Its *keys* are the
    shared canonical strings.
