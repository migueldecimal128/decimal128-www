# C Core Port Notes — Swift `Sources/Core` → `decimal128-c/core`

Practical companion for porting the **core** layer of decimal128 from Swift to C.
The authoritative specs live alongside this file; read them first:

- **[CrossPlatformArchitecture.md](CrossPlatformArchitecture.md)** — THE
  cross-language constraint regime. C is the *convergence target*: the Swift /
  Java / Kotlin "HLL" cores were written so they map cleanly to C. §3 (the
  regime), §4 (data representation, native-128 substrate, heap ban), §5
  (multi-value return), §6 (enums) are the rules you are implementing.
- **[PrimitiveLayer.md](PrimitiveLayer.md)** — the primitive contract.
- **[Rosetta.md](Rosetta.md)** — the conformance-harness design.
- **[UBD.md](UBD.md)** — the in-memory D128 representation.

> Vantage note: these notes were written by someone who ported the **Java** and
> **Kotlin** cores and read the Swift source mainly *through those ports' comments*.
> Treat any specific Swift-API claim below as "verify against
> `~/VSCodeProjects/decimal128-swift` first." Where Swift semantics are ambiguous,
> the Java and Kotlin ports are known-good cross-checks (the Kotlin port passes
> the full ~51k-vector Rosetta suite, see below).

## 0. Where things stand

`decimal128-c` currently has **`primitive/`** (src + include + tests, CMake) in
progress and **no `core/`** — the same starting point Kotlin had. So this port is
the **core layer plus the Rosetta test harness**, on top of a (mostly done)
primitive layer. Confirm the primitive seam below exists before starting core.

## 1. The one thing that makes the port tractable: the seam

Core is intended to be **near-identical across languages**; all per-language
divergence is pushed into the **primitive layer**. The critical seam Core calls:

- Dword accessors over flat limb tables: `pow10Dw0(p)/pow10Dw1(p)`,
  `pow10_256Dw0..3(i)`, plus `POW10_34/_38`, `isLt/isGe_pow10_34_bool_128`,
  `MASK54L`, `calcDigitLenInt`, the `cmp_int_256x256` compare, the `Quot256Rem128
  / Rem256 / Residue` aggregates, and the `U256<->double` sqrt-seed bridges.

In the Kotlin port these were **missing from primitive** and had to be added
before core would build — budget for the same audit here: grep the Swift Core for
every primitive symbol it calls and make sure `decimal128-c/primitive` exports
each one (same name) before porting core. This is the #1 thing that blocks a clean
core build.

## 2. C is *closer* to Swift than Java/Kotlin were

The regime (CrossPlatformArchitecture §4) targets C, so much of what Java/Kotlin
treated as "sanctioned divergence" you implement the Swift way:

| concern | Swift | C (this port) | Java/Kotlin (diverged) |
|---|---|---|---|
| 128/256-bit int | native `UInt128` | native `unsigned __int128` (or limb structs) | synthesized from signed-long limbs |
| value types (D128, U128, Quot*) | `struct` | `struct` (value semantics; **no heap** — §4.7) | heap classes |
| multi-value return | tuple/struct | `struct` by value (§5, e.g. `Quot128Residue`) | class/record |
| core enums (Round/Residue/Comparison754/Exception754) | `enum: Int` | `enum`/`#define` int constants (§6) | bare `int` constants |
| `Never` / unreachable | `Never` | `_Noreturn` + `abort()` (`verify`/`demand`/`impossible`, §9) | `Nothing` / throw |
| optional (`D128?` from parse) | `D128?` | out-param + `bool`, or a sentinel | nullable ref |
| ASCII scratch (`InlineArray<64,UInt8>`) | inline array | `uint8_t[64]` | byte array |

Decide early whether U128/U256 are `unsigned __int128` (closest to Swift,
simplest transliteration) **or** limb structs — the seam (§1) must expose dword
accessors either way because Core reads `.dw0/.dw1` style fields.

## 3. Scale and port order

Core is **~50 files / ~8000 LOC**. Go in dependency tiers, compiling often:

1. **Foundational**: the enum/int-constant holders (Round, Residue,
   Comparison754, Exception754, InvalidCause, ParseStatus), `Flags`, `AsciiBuffer`,
   `Context`, `D128Constants`.
2. **Value types**: `D128`, `D38` (+ their accessors/factories).
3. **Wide math used by core**: `U256Div` (Knuth-D), `U256Sqrt`, `DivKnuth`,
   `DivBarrett`, `DivDirect`, `DivRangeRecipMulPow10`, `DivPow10`, `Residue`.
4. **Finalize/rounding**: `Round`, `Finalize`, `D38Finalize`, `D128NextUpDown`.
5. **Arithmetic**: add/sub, mul, div, fma (D128 and D38), compare, min/max,
   total-order, round-to-integral, strip-trailing-zeros, logB/scaleB/quantize,
   non-computational (abs/negate/copy/copySign).
6. **Parse / print / serde**: `IntegerParsePrint`, `D128Parse`, `D128Print`,
   `D128SerdeBid`, `D128SerdeDpd`.
7. **Transcendentals**: `D128Exp`, `D128Log` (+ the `*Constants` Padé tables),
   `D38Sqrt`.

Kotlin file list (1:1 with Swift Core names) is a good checklist:
`decimal128-kotlin/core/src/commonMain/kotlin/.../core/*.kt`.

## 4. Validate with Rosetta — this is the whole payoff

The **Rosetta** harness (Rosetta.md) runs four corpora through one
dispatch+reconcile core. Copy the vectors (identical across ports) from
`decimal128-java/core/src/test/resources/{dectest,fptest,intel,native,golden}`.

Target (the Kotlin port hits this on both JVM and native, **0 failures**):

| corpus | passed | skipped |
|---|---|---|
| IBM dectest | 12388 | 160 |
| fptest | 24602 | 0 |
| Intel RDFP (`readtest.in`) | 14283 | 43 |

Plus `golden/kotlin_logexp.txt` (ln/log10/exp/exp10 bit-exact oracle) and the
direct unit tests. The single most comprehensive test is the corpus runner
(Kotlin `TestRosettaRunner`); everything else is narrower.

Harness shape to reproduce in C: resource load (plain `fopen`/`fread` — no
classpath needed), per-source parsers (dectest / Intel / fptest / native), the
`CanonicalOp` dispatch over ~90 arms, by-kind result + flag reconcile, the
per-source include/exclude maps and skip lists, Intel expectation-normalize, and
the ladder-sibling consistency check. It's ~34 files / ~3800 LOC and translates
cleanly (mostly data + dispatch). The hex parsers (BID `[..]`, DPD `#..`) and the
big skip/include literal tables are the bulk — generate the literal tables from
the Swift/Java source with a script rather than hand-transcribing.

## 5. Lessons from the Java/Kotlin ports that transfer

- **No tests = silent corruption risk.** A wrong shift compiles fine and quietly
  returns wrong bits. Port carefully *and* stand up Rosetta early so correctness
  is machine-checked, not assumed.
- **Audit the primitive seam first** (§1) — missing primitive exports are the main
  thing that stops core from building.
- **Unsigned 64-bit constants**: in C use explicit `ULL` / `UINT64_C(...)`; the
  top-bit-set 64-bit table literals are where transcription bugs hide. Prefer
  generating tables from the shared source.
- **Cross-check against Java/Kotlin** when a Swift result is ambiguous — both pass
  the full corpus, so a divergence usually means a port bug, not a spec question.
- **CRLF**: some dectest corpora are CRLF; the line splitter must drop a trailing
  `\r` (the harness already specifies this).

## 6. Wrapper

Out of scope for the core port (and not yet started in any port). The
public-API/`wrapper` layer (CrossPlatformArchitecture §2.3, §4.3) comes after a
green core + Rosetta.
