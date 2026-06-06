# The Primitive Arithmetic Layer for Multiplatform Decimal128

*First draft — companion to "Core Architecture and the Cross-Language Constraint Regime for Multiplatform Decimal128"*

## 1. Purpose and Scope

This document specifies the **primitive 128/256 arithmetic layer** promised by the parent architecture document (Sections 4.6 and 11): the uniform API of basic unsigned 128-bit and 256-bit integer operations that every core implementation consumes, together with the rules governing its per-platform, hand-written implementations. It is the one layer where the cross-language constraint regime deliberately relaxes — native 128-bit types, explicit unsigned casts, and platform intrinsics live here and nowhere else.

It covers: the two-tier structure of the layer; the boundary between primitive and core (with the full classification decision log); the U128/U256 arithmetic vocabulary that core code must use in place of native 128-bit expressions; result aggregates and return mechanics; naming; and per-platform implementation notes for Swift, C, Kotlin Multiplatform, and Java.

It does **not** cover the division algorithms (Barrett, Knuth D, range-reciprocal mulPow10, power-of-ten dispatch) — those are core, not primitive, by settled decision — nor the UBD representation, rounding/finalize semantics, DecContext propagation, or translation tooling. Those remain the subjects of the parent document and its other companions.

## 2. Decision Log

The classifications in this document were settled as explicit decisions (June 2026), recorded here so they read as commitments rather than emergent prose. Later sections elaborate each one.

| # | Decision |
|---|---|
| D1 | The layer is **two-tier**: tier 0 = the irreducible per-platform operations; tier 1 = multi-word kernels with a uniform API and platform-honest bodies. Core consumes the union; the tiers describe implementation provenance, not visibility. |
| D2 | `subAbs` (U256−U128 and U256−U256 forms) is a **tier-1 primitive** returning a typed `Diff256Swap` aggregate. |
| D3 | **Simple division** — `divRem_q256r64_256x64` (today's `u256DivRem64`) together with everything below it (fast paths, divisor-width dispatch, the divMod{64,128,192,256}x{16,32} kernels, `divRem256by64`) — is one self-contained tier-1 unit. `u256DivRem128`, `u256DivRem_128`, `u256DivRem256`, and residue computation remain **core**. |
| D4 | The **mulPow10 family** — plain `mulPow10` plus `fusedMulPow10Add` and `fusedMulPow10SubAbs` — is tier-1: it is performance-critical and benefits from platform-specific tuning. The `POW10`/`POW10_256` tables are defined at the primitive layer as read-only constants, directly readable by core. |
| D5 | The parent Section 4.2 confinement rule is **enforced**: core code routes all U128 arithmetic expressions through a tier-1 vocabulary of uniformly named functions. Swift retains `UInt128` as the *physical* representation of U128, with computed `.dw0`/`.dw1` accessors providing the uniform dword surface. |
| D6 | The **calcBitLen/calcDigitLen family** (128- and 256-bit forms, including the `WithBitLen` variants) is tier-1. `calcDigitLen` is performance-critical and requires unsigned compares that Kotlin/Java cannot express directly. Tier 0 gains `clz_int_64`. |
| D7 | **bitLen/digitLen are recomputed, never cached.** Magnitude types carry dwords only. Kotlin's `steal` packed-lengths field (and its packed-zero-flag trick) is removed during the Kotlin rework. |
| D8 | **Fill-in parameter order: destination first, scratch/ctx last** — `op(result, operand…, scratch/ctx…)`. Keeps operand order identical to the Swift/C value-return line, holds the destination at position 0 under varying arity, and matches the existing Kotlin kernels and C precedent. |
| D9 | **Names lead with the result, in full segment form throughout the uniform API**: `op_result_operands[_qualifier]` — `divRem_q256r64_256x64`, `add_256_256x64`, `subAbs_d256swap_256x128`. Type-prefix abbreviations were considered and rejected. Tier-0 scalar ops were originally excepted with inline-width short names; D11 retires that exception and folds them into the grammar. |
| D10 | **`barrettStep` is promoted to tier 1** as `divRem_q64r64_64x64x64_mu_barrettStep`, reversing its Section 4.3 retention. The single reciprocal-multiply division step is decimal-agnostic, and its branch-free correction is exactly the Section 6.2 confined idiom — keeping it core would force that idiom into JVM-family core source. Barrett *strategy* — the mu tables, the 10^k = 2^k·5^k split, dividend-width dispatch, and the chunk-kernel ladder — remains core. |
| D11 | **Tier-0 names fold into the D9 segment grammar**, retiring the inline-width exception: `umulHi_64_64x64`, `udiv_64_64x64`, `urem_64_64x64`, `ucmp_int_64x64`, `ushr_64_64`, `clz_int_64` — count of leading zeros — (and `ntz_int_64` — number of trailing zeros — if confirmed). The `u` op prefix marks the unsigned semantics that signed dwords obscure — information the 128/256 families don't need (their types are unsigned) but 64-bit ops do (signed dwords have two real shifts and compares). The exception had eroded: the set outgrew "five ops, learned once," and `ucmp_int_64x64`/`cmp_int_128x128`, `ushr_64_64`/`shr_128_128`/`shr_256_256` now form one grammar instead of two systems. |
| D12 | **The U128 vocabulary is frozen.** The Section 5.3 confinement sweep of the Swift reference is complete (June 2026); per the rule that the sweep is the authority, membership is fixed at the twelve Section 4.2 ops plus `mul_128_64x64`. **U128 vocabulary arithmetic is wrapping** (bit-bucket semantics, matching the native `&+`/`&-`/`&*` expressions it replaced); trap-on-overflow exists only in the U256 family. Expression forms the sweep found but deferred are tracked as candidate members in Open Items: the sign-mask/conditional-negate idiom, 128÷128 divRem, and the `hi32`/`lo32` dword half-word ops. |
| D13 | **`hi32_64`/`lo32_64` join tier 0**, resolving the half-word question in favor of dedicated ops over bare `ushr_64_64` spellings: the high half of an arbitrary dword is the dominant logical-shift shape in the kernels (Knuth loads, Barrett 32-bit chunking), and the named pair reads as intent where a shift count reads as arithmetic. The logical-shift confinement pass is complete in the Swift reference — field/flag extraction (dfd predicates, BID/DPD words, residue sign checks) and chunk-boundary shifts spell `ushr_64_64`; half-word extraction spells `hi32_64`/`lo32_64` — except the rrmp10 kernel interiors, which await the Section 3.4 exemption decision. |
| D14 | **subAbs extends to 128 bits**: `subAbs_d128swap_128x128` returning `Diff128Swap` joins the D2 family. The confinement sweep's deferred sign-mask/conditional-negate idiom was recognized as subAbs in disguise — all five core sites computed |x−y| plus a swapped flag. With this member the idiom is spelled only inside primitive bodies (per parent Section 4.3), and the Swift body needs no signed cast at all: the borrow flag of the subtract is the swapped flag. |
| D15 | **`divRem_q128r128_128x128` joins the division family** (returning `Quot128Rem128`), and the table's `divRem_q128r64_128x64` is implemented; core's last four native `quotientAndRemainder` sites convert. With D14 and the deletion of the unused `d128_coeffSigned` accessor, the confinement sweep is complete: core contains no native 128-bit arithmetic outside `verify` closures. JVM bodies need no Knuth D: the 128÷64 form is the divlu kernel; the 128÷128 form delegates to it (divisor < 2^64) or clz-normalizes and corrects one estimate (divisor ≥ 2^64, quotient fits 64 bits). |
| D16 | **The rrmp10 kernels are promoted to tier 1** behind two uniform entry points (`divPow10_q128rs_128_rrmp10`, `divPow10_q128rs_256_rrmp10`) returning the new dword-only aggregate `Quot128RoundSticky` — a 128-bit quotient plus *raw* rounding inputs (round bit, sticky compare, pre-shift sticky bits). The quotient is 128-bit **by contract**: rrmp10 reduces to 34/38 digits (256-bit dividends) or ≤18 digits (128-bit path), and the entries demand the fit — the earlier 256-bit return shape was a legacy of the Kotlin implementation's full 256-bit mutable surface, which is being discarded. Core categorizes the raw bits into a `Residue`, so rounding semantics stay core; strategy (digitLen range demands, the digitLen→pIndex choice) stays core. **All shared read-only tables now live at the primitive layer** — the RRMP10 params *and* lookups join POW10/POW10_256/POW5_64 — because primitive residence gives each platform its native table spelling: multiplier limbs with bit 63 set stay unsigned on Swift/C (signed-Long bit patterns on the JVM), and byte-packed lookup values above 127 avoid the JVM's signed-byte masking. Refinement of D4: dword-and-wider tables remain directly readable by core; sub-dword tables are read through Int-returning accessor functions (`rrmp10Lookup128` etc.), since a direct byte read cannot be spelled uniformly. |
| D17 | **Residue de-structs to a 2-bit Int**, defined at the primitive layer: `RESIDUE_EXACT/LT_HALF/HALF/GT_HALF` = 0–3, encoding frozen as `(round << 1) | sticky` — the universal IEEE round/sticky pair, direction-free and base-free. Java cannot express a zero-cost wrapper, so under line-for-line translatability the wrapper was unrepresentable on one core anyway; a residue is a 2-bit bucket, the same move as signed dwords. Operations verify the low-2-bits invariant; four values keep it human-debuggable. Consequences: `Quot128Residue`/`Quot256Residue` become dword-only by shape and join their primitive-layer siblings (the Section 6.3 exception evaporates rather than being reversed — its premise is gone); the rrmp10 entry points return `Quot128Residue` directly, superseding D16's raw-bits seam (`Quot128RoundSticky` is deleted); the residue classification helpers remain core *code*, movable per-function. Direction semantics — `needsRoundUp` and the rounding maps — are core, always. |

Three earlier decisions from the parent-document era are restated because this layer inherits them: `u128StripTrailingZeroDigits` is primitive; the division *algorithms* are core; and multi-value returns use **typed result aggregates** (the Quot* family) rather than a single untyped scratch object, with JVM cores value-returning small aggregates by default in reliance on C2 escape analysis (Section 6.4).

## 3. The Two-Tier Structure

### 3.1 One API, Two Tiers

The primitive layer presents a single uniform API to core — the same function names and signatures on all four platforms, per parent Section 4.6. Internally that API has two kinds of members, distinguished by where their implementations come from:

- **Tier 0** operations are irreducible: each platform supplies them from intrinsics, stdlib calls, or shims, and no portable expression of them exists at acceptable cost.
- **Tier 1** operations are multi-word kernels *composable* from tier 0, with bodies that are platform-honest (Section 3.3).

Core code may call operations of either tier by their uniform names; the existing cores already do (Swift's core Knuth D consumes `udiv_64_64x64` and `ucmp_int_64x64` directly in its q-hat estimate). The tier boundary constrains implementers, not callers.

This structure is not hypothetical. The Kotlin Multiplatform implementation proved it: its `expect`/`actual` split isolated *all* platform divergence to four unsigned 64-bit operations, with every multi-word kernel built portably above them in common source shared by the JVM, Native, and JS targets.

### 3.2 Tier 0 — The Irreducible Operations

Tier 0 is deliberately tiny, and every tier-0 operation returns a **single value** — no result aggregates, no out-parameters. The multi-value machinery of Section 6 begins at tier 1.

| Operation | Contract | Swift | C | Kotlin JVM | Kotlin Native | Java |
|---|---|---|---|---|---|---|
| `umulHi_64_64x64(a, b)` | high 64 bits of the unsigned 64×64 product | native (`multipliedFullWidth(by:).high` / `UInt128` product) | `(unsigned __int128)a * b >> 64` | `Math.unsignedMultiplyHigh` | C shim via `__uint128_t` | `Math.unsignedMultiplyHigh` |
| `udiv_64_64x64(a, b)` | unsigned 64÷64 quotient | native `/` | native `/` on `uint64_t` | `Long.divideUnsigned` | `toULong() / toULong()` | `Long.divideUnsigned` |
| `urem_64_64x64(a, b)` | unsigned 64÷64 remainder | native `%` | native `%` | `Long.remainderUnsigned` | `toULong() % toULong()` | `Long.remainderUnsigned` |
| `ucmp_int_64x64(a, b)` | −1/0/+1 unsigned compare | native compare | native compare | `Long.compareUnsigned` | xor-`MIN_VALUE` compare | `Long.compareUnsigned` |
| `clz_int_64(a)` | leading zero count, `clz_int_64(0) == 64` | `leadingZeroBitCount` | `__builtin_clzll` (zero-guarded) | `Long.numberOfLeadingZeros` | `countLeadingZeroBits` | `Long.numberOfLeadingZeros` |
| `ushr_64_64(a, n)` | logical right shift, `n` in `0..<64` | native `>>` on `UInt64` | native `>>` on `uint64_t` | `ushr` | `ushr` | `>>>` |
| `hi32_64(a)` | high 32 bits, zero-extended in a dword | `a >> 32` | `a >> 32` | `a ushr 32` | `a ushr 32` | `a >>> 32` |
| `lo32_64(a)` | low 32 bits, zero-extended in a dword | `a & 0xFFFF_FFFF` | `a & 0xFFFFFFFF` | `a and 0xFFFF_FFFFL` | `a and 0xFFFF_FFFFL` | `a & 0xFFFF_FFFFL` |

(`ntz_int_64` — number of trailing zeros, the twin of `clz_int_64`'s count of leading zeros — is proposed because the strip and power-of-two-divisor paths consume it, but is not yet confirmed; see Open Items.)

Two realization notes:

- **Swift and C tier 0 is approximately free.** Their native unsigned types and 128-bit arithmetic provide every tier-0 contract directly, so they need not materialize tier-0 functions at all; their tier-1 bodies simply use native operations. They *may* define the tier-0 names as always-inline wrappers for documentation parity, but nothing requires it.
- **Kotlin and Java realize tier 0 differently** — `expect`/`actual` declarations on Kotlin MP, `static` wrappers over JDK intrinsics on Java — but with identical names, so their tier-1 kernel sources stay structurally parallel. This is a sanctioned divergence (Section 9).

### 3.3 Tier 1 — Portable Kernels with Platform-Honest Bodies

Tier 1 is the bulk of the layer: multi-word add/sub/subAbs, the multiply family, mulPow10 and its fused forms, simple division, shifts, the U128 vocabulary (Section 5), bit/digit length, and trailing-zero stripping.

The uniform API — names, signatures, result types, preconditions — is identical on all four platforms. The **bodies** follow the parent document's guiding principle of *parallel structure with platform-honest bodies* (parent Section 3.2):

- **Kotlin MP** writes tier-1 kernels once in common source, in regime-compliant style, shared verbatim across the JVM, Native, and JS targets. All platform divergence stays below, in the tier-0 actuals.
- **Java** mirrors the Kotlin kernel source structurally — same names, same statement shapes — differing only in language syntax.
- **Swift and C** are *sanctioned to implement tier-1 bodies with native 128-bit arithmetic* (`UInt128`, `unsigned __int128`) rather than composing from tier 0. This extends parent sanctioned divergence #3 from "primitives" generally to tier-1 bodies specifically. Where no native advantage exists, Swift/C bodies should mirror the Kotlin kernel structure instead, so that divergence is paid for only where it buys something.

The practical consequence: a tier-1 function has at most **three** body families to maintain and verify — the JVM-family kernel (Kotlin and Java, structurally identical), the Swift body, and the C body — and the latter two are frequently near-identical as well.

### 3.4 Platform-Local Decomposition Is Not Contract

Below the uniform API, each platform decomposes freely. Kotlin's `SumU64.kt` kernels (`sumU64` over 2–9 operands with tree-structured carry propagation, `diffU64`, `umul128x128to192`, …), Swift's private `u64StripTrailingZeroDigits` helper, and the Swift divMod kernel ladder inside the simple-division unit (Section 4.4) are all **internal decomposition**: useful, tuned, and invisible to core. They carry no cross-platform naming or shape obligations, though convergent shapes (and there are striking ones — see Section 8.5 of the operation inventory) are welcome evidence of correctness.

The same applies to loose-dword parameter passing. Kotlin's kernels pass operands as individual `Long` arguments (`x1, x0, y1, y0`) rather than objects — proven efficient on the JVM and consistent with parent Section 4.2's "parameters are passed as the individual dword fields." That style is the *internal* idiom of JVM-family kernel decomposition. The *uniform* API that core calls takes U128/U256 values and returns typed aggregates (Section 6).

## 4. The Layer Boundary

### 4.1 The Classification Rule

The primitive layer contains **basic 128/256-bit integer operations**; the core contains **algorithms and strategy**. The line, applied across every decided case:

- A *loop or carry chain over limbs* with no decimal semantics → primitive.
- A *choice among methods* (which algorithm, which table, which width class — when the choice encodes numeric strategy) → core.
- Decimal-*flavored* but mechanically basic and performance-critical (strip, mulPow10, digitLen) → primitive, because these benefit from per-platform tuning and sit on hot paths.
- Decimal-*semantic* (residue categorization, rounding, finalize, parse/print) → core, always.

### 4.2 The Primitive Inventory

The uniform API, by family, in the D9 full segment grammar `op_result_operands` (Section 7). Names marked ◆ are spellings not yet final (invented segments, or waiting on another open decision). Where a function name differs from today's Swift core spelling, the old name is given in the Notes column. Preconditions trap via `demand`/`impossible` per parent Section 9.

| Family | Operations | Result | Notes |
|---|---|---|---|
| tier 0 | `umulHi_64_64x64`, `udiv_64_64x64`, `urem_64_64x64`, `ucmp_int_64x64`, `ushr_64_64`, `hi32_64`, `lo32_64`, `clz_int_64` | dword / Int | Section 3.2; grammar names with `u` op prefix per D11; half-word ops per D13 |
| U128 vocabulary | `add_128_128x128`, `sub_128_128x128`, `mul_128_128x128`, `shl_128_128`, `shr_128_128`, `and_128_128x128`, `or_128_128x128`, `xor_128_128x128`, `not_128_128`, `cmp_int_128x128`, `isZero_bool_128`, `fromDwords_128_64x64` | U128 / Int / Bool | Section 5; membership FROZEN by the completed sweep (D12); arithmetic is wrapping |
| 64→128 product | `mul_128_64x64(a, b)` | U128 | full-width 64×64 by construction; replaces core-visible `multipliedFullWidth` |
| 128÷64 | `divRem_q128r64_128x64(x, y)` | `Quot128Rem64` | general |
| 128÷64, q fits 64 | `divRem_q64r64_128x64(hi, lo, y)` | `Quot64Rem64` | the `dividingFullWidth` contract; the result segment carries the quotient-fits precondition |
| 64÷64 by reciprocal | `divRem_q64r64_64x64x64_mu_barrettStep(dw, denom, mu)` | `Quot64Rem64` | D10; single Barrett correction step; precondition `mu = floor(2^64 / denom)` with q-hat at most 1 below the true quotient |
| 128÷128 | `divRem_q128r128_128x128(x, y)` | `Quot128Rem128` | D15; general; JVM body composes from the 128÷64 kernel — no Knuth D |
| U256 add | `add_256_256x64`, `add_256_256x128`, `add_256_256x256`, `add_256_128x128` | U256 | traps on 256-bit overflow |
| U256 sub | `sub_256_256x256` | U256 | traps on underflow |
| U256 subAbs | `subAbs_d256swap_256x128`, `subAbs_d256swap_256x256` | `Diff256Swap` | D2; single-pass borrow chain + branch-free conditional negate |
| U128 subAbs | `subAbs_d128swap_128x128` | `Diff128Swap` | D14; absorbs core's sign-mask conditional-negate idiom |
| U256 mul | `mul_256_128x64`, `mul_256_128x128`, `mul_256_256x64`, `mul_256_256x128`, `mul_256_256x256` | U256 | traps where the result must fit |
| mulPow10 | `mulPow10_128_128`, `mulPow10_256_128`, `mulPow10_256_256` | U128 / U256 | D4; table-driven; the Int exponent operand is implied by the op (formerly `mul_128_pow10_p128`, `U256.mulPow10`; retired) |
| fused mulPow10 | `fusedMulPow10Add_256_128x128`, `fusedMulPow10Add_256_256x64`, `fusedMulPow10Add_256_256x128`, `fusedMulPow10SubAbs_d256swap_128x128`, `fusedMulPow10SubAbs_d256swap_256x128` | U256 / `Diff256Swap` | D4; platforms may interleave limbs (Swift does) or sequence two primitives |
| simple division | `divRem_q256r64_256x64(x, y)` | `Quot256Rem64` | D3; the self-contained unit of Section 4.4 (formerly `u256DivRem64`; retired) |
| rrmp10 kernels | `divPow10_q128res_128_rrmp10(x, pIndex, pow10)`, `divPow10_q128res_256_rrmp10(x, pIndex, pow10)` | `Quot128Residue` | D16/D17; quotient fits 128 by contract; kernel interiors are platform-local (§3.4) |
| shifts | `shl1_256_256`, `shr1_256_256`, `shr_256_256` | U256 | Int shift count implied for the counted form |
| length | `bitLen_int_128`, `digitLen_int_128`, `digitLen_int_128_withBitLen`, `bitLen_int_256`, `digitLen_int_256`, `digitLen_int_256_withBitLen` ◆ | Int | D6, D7; today's `calcBitLen128` family; `int`/`bool` result segments pending confirmation |
| strip | `u128StripTrailingZeroDigits(x, maxToStrip)` ◆ | `Stripped128` ◆ | settled primitive; full-form spelling waits on the result-shape decision (Open Items) |
| constants | `POW10[0…38]` (U128), `POW10_256[39…77]` (U256) | — | D4; defined here, read-only, directly readable by core |

### 4.3 Core Retentions

For the avoidance of doubt, the following stay in core and are **not** primitive, however arithmetic they look:

- **Barrett division strategy** — the mu tables, the 10^k = 2^k·5^k split, dividend-width dispatch, and the chunk-kernel ladder (`barrettStep` itself is tier-1 by D10) — **Knuth D**, **rrmp10 strategy** — the digitLen range demands and digitLen→pIndex lookup choice (the kernels are tier-1 by D16) — and the **power-of-ten divisor dispatch**.
- `u256DivRem128`, `u256DivRem_128`, `u256DivRem256` — these are *strategy*: they choose among the simple-division primitive, special cases, and Knuth D. In particular `u256DivRem256` falls through to Knuth D, which is core; a primitive must never call up into core.
- `u256DivResidue_128`/`_256` and the `residueFrom*` classification helpers remain core code today (movable per-function — D17 made `Residue` a primitive-layer 2-bit Int, so no type gravity holds them). Rounding *direction* semantics — `needsRoundUp` and the rounding maps — are core, always.
- Finalize/rounding, parse/print, DPD/BID conversion, dfd packing logic (which after the Section 5 sweep is expressed *through* the U128 vocabulary but remains core code).

### 4.4 The Simple-Division Unit

`divRem_q256r64_256x64` (today's `u256DivRem64`) is the layer's one large composite primitive, and D3 fixes its boundary by call direction: it calls only downward, so the whole ladder ships as one unit behind one uniform entry point.

The Swift reference structure, which other platforms may mirror or re-tune:

1. Fast paths: divisor ≤ 1 (trap on 0, identity on 1); dividend fits 64 bits (single hardware divide); power-of-two divisor (shift + mask via trailing-zero count).
2. Divisor-width dispatch: ≤16-bit and ≤32-bit divisors route to specialized limb kernels (`divMod{64,128,192,256}x{16,32}`), selected by dividend bit length.
3. 33–64-bit divisors: 4-step base-2⁶⁴ long division (`divRem256by64`), one `dividingFullWidth`-contract step per limb.

Everything inside is platform-local decomposition (Section 3.4): the kernel ladder is Swift's tuning, not contract. The contract is the entry point's behavior: full 256÷64 quotient and 64-bit remainder, divisor nonzero.

Its production consumer today is general decimal division (via core's `u256DivRem_128` strategy wrapper) — small divisor *coefficients* (÷2, ÷3, ÷100) in ordinary division. The pow10 paths never reach it; Barrett and rrmp10 own those in core.

### 4.5 The mulPow10 Family and the POW10 Tables

mulPow10 is hot enough, and shaped conveniently enough per platform, that the whole family is tier-1 (D4). Swift already hand-interleaves the limb products of `fusedMulPow10Add` with the addend's carry chain; the JVM family composes `umul128xPow10`-style kernels from `umulHi_64_64x64`; platforms without an advantage may implement the fused forms as plain mulPow10-then-add/subAbs sequencing. All of that is body freedom under one API.

The `POW10` (10⁰…10³⁸ as U128) and `POW10_256` (10³⁹…10⁷⁷ as U256) tables are **defined at the primitive layer** as read-only constants and are **directly readable by core** — core's own table uses (digitLen comparisons, division pow10 dispatch) read them without an accessor hop. They are shared constants with identical values everywhere, not an ownership wall. D16 generalizes the rule: **all shared read-only tables live at the primitive layer** (POW5_64 and the RRMP10 tables included), with one refinement — sub-dword tables (the byte-packed RRMP10 lookups) are read through Int-returning accessors, because a direct byte-element read cannot be spelled uniformly on signed-Long platforms.

### 4.6 Length Calculation: Recompute, Never Cache

The length family — today's `calcBitLen*`/`calcDigitLen*`, full-form `bitLen_int_*`/`digitLen_int_*` (Section 4.2) — is tier-1 (D6). digitLen is the classic two-step: `(bitLen × 1233) >> 12` for a floor estimate, then one unsigned table compare against `POW10` — and that unsigned compare is exactly what Kotlin/Java cannot write natively, which is what pushed the family into this layer. bitLen composes from `clz_int_64` with the branch-free two-word idiom (Section 6.2).

D7 makes the storage rule explicit: **magnitude types carry dwords only, and lengths are always recomputed.** The Kotlin implementation's `steal` field — cached bitLen/digitLen packed into C256's heap-padding Int, doubling as a zero flag — is removed during its architecture rework. The reasoning: clz is 1–2 cycles everywhere; a cache imposes a maintain-the-invariant obligation on every mutating kernel (a standing JVM-only bug source, invisible at call sites); and a cache field would force a fifth dword-sized member into the Swift/C value structs, violating the four-dword shape of parent Section 4.2. If profiling later shows a hot recompute, caching may return as a measured, localized optimization — not as the default.

## 5. The U128/U256 Core Vocabulary

### 5.1 The Confinement Rule, Enforced

Parent Section 4.2 states that native 128-bit machine types appear only inside the bodies of arithmetic primitives. D5 resolves how that rule meets reality: **it is enforced, by giving core a complete vocabulary of uniformly named U128 operations** — `add_128_128x128`, `shl_128_128`, `and_128_128x128`, `cmp_int_128x128`, and the rest of the Section 4.2 table — and requiring core to express all 128-bit arithmetic through it.

On Swift and C the vocabulary functions are always-inline wrappers over native 128-bit operations, observed (Swift) and expected (C) to compile to zero runtime cost. On Kotlin and Java they are the synthesized Long-pair kernels. The result is that the ~10 core files that today perform direct `UInt128` mask/shift/compare/wrapping arithmetic — `D128.swift` (dfd packing), `D128ArithAddSub`, `D128ArithMul`, `D128ArithFma`, `D128Parse`, `D128SerdBid`, `D128SerdeDpd`, `Dec38AddSub`, `D128ToIntegral`, `Finalize` — become expression-level translatable: their future Kotlin/Java translations match line for line precisely in the bit-trickiest code, where mutual verification matters most. The cost is a one-time mechanical sweep of those files.

### 5.2 Representation: Behavioral Dwords

`U128` and `U256` are **defined at the primitive layer**: the type definitions, their accessor bodies, and their representation choices live with the arithmetic that owns them. Core consumes the types through their uniform dword surface and never sees what is behind it.

The vocabulary decision lets the *representation* question land gently:

- **Kotlin and Java:** U128/U256 are final mutable classes of stored signed-Long dwords, per parent Section 4.2 — unchanged.
- **C:** U128/U256 are structs of `int64_t` dwords. C has no computed properties, so the dword fields must be physically real; bodies pack to `unsigned __int128` and unpack, which C compilers are expected to fuse.
- **Swift:** U128 keeps **`UInt128` as its physical representation**, with computed `.dw0`/`.dw1` accessors (mask, shift-by-64) providing the dword surface. Core source reads `x.dw0` identically on all four platforms; whether that is a stored field or a zero-cost computed property is confined to the accessor body — itself primitive-layer territory. The computed-accessor exception was already sanctioned during the accessor sweep (`dw0`/`dw1`/`hi64`/`lo64` remain computed vars); D5 makes it load-bearing.

The parent Section 4.2 "dword restructure" of Swift's U128 is therefore satisfied *behaviorally* rather than physically, and is no longer pending as a physical change. U256 on Swift remains hi/lo-of-UInt128 physically with `dw0…dw3` computed accessors, by the same reasoning.

### 5.3 What the Sweep Changes

For the Swift core, enforcement means:

- Native U128 expressions in core files (`a &+ b`, `x >> 110`, `x & mask`, `x < y`) are rewritten as vocabulary calls (`add_128_128x128(a, b)`, `shr_128_128(x, 110)`, `and_128_128x128(x, mask)`, `cmp_int_128x128(x, y) < 0`).
- The U256 *method* surface (`x.add(y)`, `x.mul(y)`, `x.subAbs(y)`) migrates to top-level functions (`add_256_256x256(x, y)`, …), because the uniform API must be expressible in C, which has no methods, and the regime's restrict-to list already names "static and top-level functions" as the shape of core code.
- Core files keep reading `.dw0…dw3`, `.bitLen()`/`.digitLen()` (or their top-level spellings) — accessor reads are not arithmetic and are uniform already.

The vocabulary's exact membership was derived mechanically: the sweep of the core files (completed in the Swift reference, June 2026) enumerated every distinct native-128 expression form. The Section 4.2 list is now frozen (D12). All expression forms the sweep found are now vocabulary members: the sign-mask/conditional-negate idiom resolved into `subAbs_d128swap_128x128` (D14), the native `quotientAndRemainder` sites into the divRem family (D15), and the one signed `Int128` accessor (`d128_coeffSigned`) proved dead and was deleted. With the rrmp10 kernels promoted (D16), core contains no native 128-bit arithmetic outside `verify` closures — the confinement rule holds without exemptions.

## 6. Signatures, Signedness, and Multi-Value Return

### 6.1 Signed Dwords at the API

Per parent Section 4.3, dwords are signed 64-bit integers on every core, and this layer is where the consequences concentrate: every unsigned compare, logical right shift, division, and high-word check that the signed representation obscures is spelled out *here*, inside primitive bodies, and nowhere else. Uniform API signatures use the platform dword type (`Int64`/`int64_t`/`Long`/`long`), `Int` for counts, lengths, and powers, and `Bool` where the contract is genuinely boolean.

The current Swift core is unsigned-native (`UInt64`/`UInt128` spellings); its migration to signed dwords is sequenced with the Section 5.3 sweep (see Open Items) and changes spellings, not behavior — the dwords are bit-buckets either way.

### 6.2 The Unsigned-Idiom Inventory

The parent Section 4.3 "cast inventory" exists in production form in the Kotlin implementation and is adopted as this layer's reference idiom set for JVM-family bodies:

| Need | JVM-family idiom |
|---|---|
| unsigned less-than | `(x xor Long.MIN_VALUE) < (y xor Long.MIN_VALUE)` |
| carry detect after add | `carry = if (unsignedLT(sum, a)) 1L else 0L` |
| branch-free nonzero mask | `((dw or -dw) shr 63)` (and `.inv()` for the zero mask) |
| branch-free conditional subtract | `adjust = ((rHat - denom) shr 63).inv(); q = qHat - adjust; r = rHat - (adjust and denom)` |
| two-word bitLen, branch-free | `128 - nlz1 - (nlz0 and dw1IsZeroMask)` |

Swift and C bodies achieve the same with explicit unsigned casts (`UInt64(bitPattern:)`, `(uint64_t)`), per parent sanctioned divergence #4. The `carryBitOf(carryFlag)` Bool→64-bit helper of parent Section 4.5 lives here, in JVM-family bodies, and is expected to be absent on Swift/C.

### 6.3 Typed Result Aggregates

Multi-value returns use **typed result aggregates** with positional initializers — the Quot* family — resolving the typed-but-many (Swift Quot*) versus untyped-but-single (Kotlin `Pentad`) design fork in favor of typed. Field meaning lives in the type, not in per-call-site convention; the types are small enough for value-return everywhere (Section 6.4); and proliferation has a natural ceiling — the family is closed over the quotient/remainder/residue shapes the layer actually produces.

The family, with producers:

| Aggregate | Fields | Produced by |
|---|---|---|
| `Quot64Rem64` | q64, r64 | `divRem_q64r64_128x64`, `divRem_q64r64_64x64x64_mu_barrettStep` (both primitive, D10) |
| `Quot128Rem64` | q128, r64 | `divRem_q128r64_128x64` (primitive) |
| `Quot128Rem128` | q128, r128 | `divRem_q128r128_128x128` (primitive, D15); core division strategy |
| `Quot256Rem64` | q256, r64 | `divRem_q256r64_256x64` (primitive) |
| `Quot256Rem128` | q256, r128 | core division strategy |
| `Quot256Rem256` | q256, r256 | core division strategy |
| `Quot128Residue` | q128, residue | `divPow10_q128res_128/256_rrmp10` (primitive, D17); core division strategy |
| `Quot256Residue` | q256, residue | core division strategy |
| `Diff128Swap` | diff128, swapped | `subAbs_d128swap_128x128` (D14) |
| `Diff256Swap` | diff256, swapped | `subAbs_d256swap_256x128/256`, `fusedMulPow10SubAbs_d256swap_*` (D2, D4) |
| `Stripped128` ◆ | stripped128, stripCount | `u128StripTrailingZeroDigits` (shape provisional — Open Items) |

The aggregate *types* are defined once with uniform names and field order on all platforms, with the parent Section 5.2 caveat that JVM field ordering may differ physically for alignment; behavior is identical. Kotlin's `Pentad` is retired at rework; its role survives only as the loose-dword internal idiom of Section 3.4.

**Type ownership.** The primitive layer defines `U128`, `U256`, and every result aggregate — `Quot64Rem64`, `Quot128Rem64`, `Quot128Rem128`, `Quot256Rem64`, `Quot256Rem128`, `Quot256Rem256`, `Quot128Residue`, `Quot256Residue`, `Diff128Swap`, `Diff256Swap`, and (provisionally) `Stripped128`. The rule is by *shape*: every field is a regime scalar (dwords, U128/U256, Int, Bool — and since D17, `Residue` is a 2-bit Int). Ownership is **not** by producer: several aggregates are produced only by core division strategy today, but they stay with their primitive-layer siblings rather than splitting the family across layers by call graph. (Before D17, `Quot128Residue`/`Quot256Residue` were core-defined exceptions because their `residue` field was a core enum; de-structing the enum dissolved the exception.)

### 6.4 Return Mechanics

Parent Section 5.1's asymmetry applies, with the settled refinement:

- **Swift and C** return aggregates **by value** in registers.
- **Kotlin and Java** also **value-return by default**, constructing the small aggregate and relying on C2 escape analysis to scalarize it — verified per aggregate type with `jmh -prof gc` showing zero allocation on the hot paths. The thread-local pool of parent Section 4.7.3 is demoted to a **measured fallback**: any aggregate type that fails its escape-analysis verification reverts to the caller-owned fill-in convention for that type only.

Where the fill-in convention applies — the measured-fallback types and mutating kernels such as strip — the **destination comes first and scratch/context parameters come last**: `op(result, operand…, scratch/ctx…)` (D8). Destination-first keeps the operands positionally identical to the Swift/C value-return line (`let z = op(x, y)` ↔ `op(z, x, y)`), holds the destination at position 0 under varying operand arity, and matches both the existing Kotlin kernels (`sumU64(sum, …)`, `c256SetFma(z, x, y, a, pentad)`) and long C precedent (`memcpy(dest, src)`; decNumber's `decNumberAdd(result, lhs, rhs, ctx)`).

The translation rule stays mechanical either way: value-return on Swift/C corresponds to value-return-or-fill-in on the JVM family, decided per type by measurement, recorded in this document as results arrive (Open Items).

The primitive layer itself allocates nothing on any platform; the only allocation question is the aggregate-return mechanics above, and the default answer is "scalarized away."

## 7. Naming

Function names are identical across all four cores, governed by the segment grammar now codified in parent Section 8 — it originated here as D9, and the parent is the authority. This section restates it with the layer-specific notes.

**The segment grammar — result first:**

```
name     ::= op '_' result '_' operands [ '_' qualifier ]
operands ::= width ('x' width)*
result   ::= width | aggregate segment (q256r64, q128res, d256swap, …)
```

The result leads the name so that name order mirrors call-site order on every platform: `let z = mul_256_128x64(x, y)` on Swift/C and `mul_256_128x64(z, x, y)` under the JVM fill-in convention (Section 6.4, D8) both put the result leftmost. Examples: `mul_256_128x64`, `divRem_q256r64_256x64`, `subAbs_d256swap_256x128`. Result-aggregate segments use the established terse forms (`q256r64` = Quot256Rem64, `q128res` = Quot128Residue, `d256swap` = Diff256Swap).

**Full segment form is used throughout the uniform API.** A type-prefix abbreviation (`u128Add`, `u256Mul128x64`) was considered for operations whose prefix fully determines the signature, and rejected: one grammar everywhere keeps the result visible at every call site, keeps every name mechanically parseable for the translation tooling, and avoids a mixed-style API surface. The division contracts show the payoff: `divRem_q128r64_128x64` versus `divRem_q64r64_128x64` differ only in the result segment, making the quotient-fits precondition part of the name where a bare `_128` suffix once said it by private convention.

**Tier-0 names** follow the same grammar (D11): `umulHi_64_64x64`, `udiv_64_64x64`, `urem_64_64x64`, `ucmp_int_64x64`, `ushr_64_64`, `clz_int_64`. The `u` op prefix marks unsigned semantics, needed at the dword width where the signed representation makes it ambiguous; the earlier inline-width short forms (`unsignedMul64Hi64`, `clz64`) are retired.

Known inconsistencies to reconcile during the sweep rather than per-file: today's type-prefix spellings (`u256DivRem64`, the `calcBitLen128` family, `mul_128_pow10_p128`) rename to the full grammar per the Section 4.2 table; method-form U256 operations become top-level spellings; the core division-strategy names (`div_256_pow10_q128res_barrett`) carry their result segment in third position and reorder to result-first with the exponent folded into the op (`divPow10_q128res_256_barrett`, parent Section 8) when touched; Kotlin's `umul128x128to192`-style kernels use a result-*last* `to` form but are platform-internal decomposition (Section 3.4) and may follow at leisure. The reconciliation is mechanical renaming and belongs to the same change that moves these functions into primitive-layer source files.

## 8. Per-Platform Implementation Notes

### 8.1 Swift

Tier 0 is native; tier-1 bodies use `UInt128` freely (sanctioned). U128 is physically `UInt128` with computed dword accessors (Section 5.2). Carry/borrow chains use `addingReportingOverflow`/`subtractingReportingOverflow`; full products use `multipliedFullWidth`; the `dividingFullWidth` q-fits contract backs `divRem_q64r64_128x64`. The simple-division kernel ladder (Section 4.4) is the Swift decomposition reference. Primitive sources live beside core sources in the same module until the layering split lands; the earlier premature target split is not repeated until this spec settles.

### 8.2 C

Structs of `int64_t` dwords; bodies cast to `unsigned __int128` and back, with the compiler expected to fuse pack/unpack. `clz_int_64` guards the `__builtin_clzll(0)` undefined case explicitly. The C core does not yet exist; this layer is where its implementation starts, because the Swift-over-C and Kotlin/Native-over-C wrappers let the existing test suites drive it immediately. MSVC's lack of `__int128` is noted in Open Items.

### 8.3 Kotlin Multiplatform

Tier 0 is the four unsigned-operation expect/actuals from `XPlatform.kt` (renamed per D11 at the rework), plus `clz_int_64` (which may realize as common-source `countLeadingZeroBits` rather than expect/actual — tier 0 is contract, not mechanism). Tier-1 kernels are common source shared by JVM, Native, and JS targets, evolving from `SumU64.kt`. The rework retires `Pentad` (Section 6.3) and the `steal` cache (D7). JS performance rests on emulated Longs and is measured, not assumed (Open Items).

### 8.4 Java

Tier 0 as `static` wrappers over `Math.unsignedMultiplyHigh`, `Long.divideUnsigned`/`remainderUnsigned`/`compareUnsigned`, `Long.numberOfLeadingZeros`. Tier-1 source mirrors the Kotlin kernels statement for statement. The Java core does not yet exist; like C, it begins here.

## 9. Sanctioned Divergences

These extend the parent Section 10 list within this layer. Everything else in the layer — names, signatures, aggregate shapes, preconditions, behavior — is identical across the four cores.

| # | Divergence |
|---|---|
| P1 | **Tier-1 body style.** Swift/C: native 128-bit arithmetic. Kotlin/Java: synthesized signed-Long kernels. (Extends parent #3.) |
| P2 | **Tier-0 realization.** Swift/C: not materialized (native ops suffice). Kotlin MP: expect/actual (or common stdlib where adequate). Java: static wrappers over JDK intrinsics. |
| P3 | **U128 physical representation.** Swift: `UInt128`-backed with computed `.dw0`/`.dw1`. C: true struct of dwords (no computed properties exist). Kotlin/Java: mutable class of stored Longs. The dword *access surface* is identical everywhere. |
| P4 | **Unsigned idiom spelling.** JVM family: xor-MIN_VALUE compares, mask algebra (Section 6.2). Swift/C: explicit unsigned casts. (Realizes parent #4 inside this layer.) |
| P5 | **Aggregate return mechanics.** Swift/C: value-return. JVM family: value-return by default under verified escape analysis, with per-type measured fallback to caller-owned fill-in. (Refines parent #2.) |
| P6 | **Platform-local decomposition.** Sub-API helpers, kernel ladders, and loose-dword internal calling conventions are unconstrained per platform. (Section 3.4.) |

## 10. Implications for Existing Code

**Swift (this repo, the reference implementation):**

- The confinement sweep of ~10 core files (Section 5.3), rewriting native U128 expressions as vocabulary calls and U256 methods as top-level functions.
- Relocation of the decided primitives — mulPow10 family, subAbs, strip, the length family, `divRem_q256r64_256x64` (today's `u256DivRem64`) and its ladder, `barrettStep` (D10), the U128 vocabulary — into primitive-layer source files under their D9 names; `u256DivRem128/_128/256`, residue, and the division algorithms' strategy layers stay in core files.
- New `Diff256Swap` (and provisional `Stripped128`) aggregates replacing the last primitive-layer tuples; `fusedMulPow10SubAbs` and `subAbs` callers updated.
- Naming reconciliation per Section 7.

**Kotlin (decimal128-kotlin, at architecture rework):**

- Drop `steal` (D7) and its zero-flag trick, retire `Pentad` in favor of typed aggregates with EA-verified value return.
- Keep the four proven tier-0 expect/actuals (renamed per D11); add `clz_int_64` if expect/actual proves necessary; align kernel names to the uniform API.
- The SumU64 kernel suite persists as internal decomposition beneath the uniform tier-1 names.

**C and Java:** greenfield; begin at tier 0 and the aggregate definitions, then tier 1, then core translation.

## 11. Open Items

The following are explicitly unresolved and tracked for future revisions of this document:

- **`ntz_int_64` in tier 0** — number of trailing zeros, the twin of `clz_int_64` (strip and power-of-two paths consume it); confirm or fold into platform-local bodies.
- **`Stripped128` shape** — typed aggregate (consistent with the family, EA-default) versus the inventory's earlier mutate-in-place-plus-count recommendation for JVM; decide once the EA measurements for the smallest aggregates are in.
- **Per-type escape-analysis verification** — the `jmh -prof gc` results for each aggregate (notably the five-field `Quot256Rem256`) that confirm or revoke value-return-by-default, to be recorded here.
- **Swift signed-dword migration sequencing** — whether the parent Section 4.3 signedness change rides the confinement sweep or follows it as a separate spelling pass.
- **Final naming reconciliation** — depends on the parent's open name-mangling rules; the Section 7 conventions are provisional.
- **C specifics** — `__int128` unavailability on MSVC (fallback: JVM-family-style synthesized kernels), and the C `int` width decision inherited from parent Section 4.4.3.
- **Kotlin/JS tier-0 performance** — emulated-Long costs for the JS actuals; measure before committing JS to the same kernel shapes.
- **Double support for sqrt seeding** — the Kotlin sqrt seeds from a platform Double square root (`kotlin.math.sqrt`) and converts magnitudes to/from Double (`c256ToFloorDouble`, Double→C256 set). These are Double operations consumed by a core algorithm; when sqrt is ported into the regime they need uniform primitive spellings (a `mathSqrt` tier-0 op plus conversion kernels).
- **`remTruncFnzFnz (Decimal128, Bool)`** — a core-layer multi-value return, out of this layer's scope; tracked here only so it is not lost (it belongs to the parent document's open items).

---

*End of first draft.*
