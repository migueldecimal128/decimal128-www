# Rust Port — Swift `decimal128-swift` → `decimal128-rust`

*As-built — 2026-06-18*

A **native Rust port** of decimal128, transliterated from the Swift reference and
validated continuously by the **Rosetta** harness. It now spans the full stack —
Primitive + Core engine, the §9 math, the public `Decimal128` **wrapper**, and
**BasicFinance** — mirroring the Swift reference end to end. Unlike `decimal128-c`
(the C *convergence target*), Rust is a full native transliteration — the 5th
first-class implementation alongside Swift, C, Java, Kotlin — **not** a binding
over `decimal128-c`. The C core is a differential oracle during the port, never a
runtime dependency.

This document records what was built and the decisions taken; the authoritative
specs are the companions below.

References: `CrossPlatformArchitecture.md` (the constraint regime, "§n"),
`Rosetta.md` (the harness, "R§n"), `PrimitiveLayer.md`, `UBD.md`.

--------------------------------------------------------------------------------
## 0. Where things stand

**Complete end to end: Primitive + Core engine, §9 math, the full Rosetta
conformance harness, the public `Decimal128` wrapper, and BasicFinance.** The
engine passes **all four** corpora the Swift reference uses, through the internal
`d128_*` surface:

| Corpus  | Dialect                          | Vectors (passing) |
|---------|----------------------------------|-------------------|
| dectest | `#`DPD / ctx-parse               | (decimal128 dq*)  |
| fptest  | `Q`/`S` / parseOrNaN             | d128 lines only   |
| Intel   | `[hex]` BID                      | bid128_ included  |
| native  | all forms (hand-authored)        | every `.txt`      |
| **Total** |                                | **52 820 pass / 0 fail / 203 skip** |

(434 dectest vectors are "unimplemented" by design — the GDAS-only excludes
`plus`/`shift`/`canonical`/`class`, mirroring the Swift maps.)

And the **public-API** WrapperRosetta — the dectest + fptest + Intel corpora
driven through the public `Decimal128` surface only (§7 below) — passes
**46 507 / 0**, the exact parity number of the Swift/Kotlin/Java wrappers.

Gate suite, all green: `cargo fmt --check`; `cargo clippy --all-targets
--all-features -- -D warnings`; `cargo test` (106 lib tests incl. both Rosetta
gates + 22 public-API integration tests); `cargo test --features verify` (107,
internal invariants armed); `cargo build --no-default-features` (no_std).

--------------------------------------------------------------------------------
## 1. Settled decisions (D-R1 … D-R12)

- **D-R1 — single crate.** One crate `decimal128` (edition 2024). Modules
  `primitive` and `core_` are `pub(crate)`; the public wrapper is re-exported at
  the crate root. `core_` (trailing underscore) avoids shadowing the `::core`
  std crate, which this no_std-capable crate references throughout.
- **D-R2 — native `u128`.** Mirrors the current Swift reference
  (`typealias U128 = UInt128`), blessed for native-capable ports by §4.2/§4.6.
  A newtype `struct U128(u128)` exposes only the signed `dw0()/dw1()` dword
  surface (confining the native type per §4.6). U256 has no native type
  anywhere → a four-`i64`-dword struct.
- **D-R8 — tier-faithful identifiers.** Internal tiers mirror Swift's exact
  identifiers (e.g. `umulHi_64_64x64`, `decimalFNZ_128`) for cross-port grep
  parity, with `#![allow(non_snake_case, non_camel_case_types,
  non_upper_case_globals, clippy::upper_case_acronyms, …)]` scoped to the tier.
- **D-R9 — wrapper encapsulates.** The public `Decimal128` will permanently
  *encapsulate* a `core: D128` field (value struct → wrapping is zero-cost; the
  Java D128→Decimal128 flatten was heap-driven and does not transfer).
- **D-R10 — `Int` → `i64`.** Swift `Int` → Rust `i64`, cast to `usize` only at
  index sites. Swift masking ops `&+`/`&<<`/`&>>` → `wrapping_*`.
- **D-R11 — Context threading.** `Context { round, flags: Cell<Flags> }`,
  threaded `&Context` / `Option<&Context>`. `&Context` is `Copy`, so this
  reproduces Swift's reference-passing without `&mut` reborrow friction; `Cell`
  keeps it no_std-clean.
- **D-R12 — integer sqrt seed.** `U256Sqrt` seeds its floor root from an integer
  `bitLen` estimate, not `f64::sqrt` (which is std-only and would cascade
  no_std-breakage through all sqrt/transcendental ops). The ±1 pin makes the
  floor exact regardless of seed.

The `verify!` macro is feature-gated (`verify`); `demand`/`impossible` are
always-on (message-first, mirroring Swift); `impossible` returns `!`. The crate
is `#![forbid(unsafe_code)]`.

--------------------------------------------------------------------------------
## 2. Memory model

Rust mirrors the Swift **value-return** arm: `Copy` value structs (`D128`,
`D38`), native 128-bit arithmetic, a heap-free core, `impossible → !` for Swift's
`Never`. The Java/Kotlin fill-in / thread-local-pool arm (§4.7.3) does **not**
apply. `D128` derives `Clone, Copy` only (no `PartialEq` — structural compare is
the explicit `d128_bitwiseEQ`).

--------------------------------------------------------------------------------
## 3. Layout

```
decimal128-rust/
  src/
    lib.rs              // crate root; #![cfg_attr(not(feature="std"), no_std)]
    verify.rs           // verify! macro + demand/impossible
    primitive/          // U128/U256, Quot* aggregates, POW10/POW5 tables,
                        //   divPow10 kernels (magic/Barrett/RRMP10/Knuth), …
    core_/              // D38 + D128 engine, finalize/round pipeline,
                        //   arith/compare/parse/print/serde/math,
                        //   rosetta/  (the in-crate conformance harness)
  tests/resources/      // dectest/ fptest/ intel/ native/ golden/ (corpora)
```

The Rosetta harness lives **in-crate** under `core_::rosetta` (gated
`#[cfg(all(test, feature = "std"))]`), because the core is `pub(crate)` — an
external `tests/` crate cannot reach the `d128_*` functions. Corpora are read at
test time from `CARGO_MANIFEST_DIR/tests/resources/`.

--------------------------------------------------------------------------------
## 4. Rosetta harness (R§)

Ported the dectest + fptest + Intel + native paths as a Source-aware runner that
shares one dispatch:

- **`case.rs`** — `Source{Dectest,Fptest,Intel,Native}` + the neutral `Case`.
- **`dectest.rs` / `fptest.rs` / `intel.rs` / `native.rs`** — per-corpus parsers
  emitting `Case`s; each maps its op vocabulary to a shared dispatch token and
  renders the flag column to the canonical `xuozi` string.
- **`dispatch.rs`** — one op match (~90 arms), per-source operand/expected
  decode, and reconciliation:
  - *plain path* (dectest + Intel + native): value-by-kind, flags exact, with
    the Intel int-sentinel allowance (`i64::MIN` ≡ `i32::MIN` when invalid).
  - *fptest path*: trap-unwrap (re-derive the 1985 wrapped result via
    `scaleB ±9216`) + tininess-`u`-strip.
  - *Intel expectation-normalize*: rewrite Intel's pre-GDAS NaN-payload /
    number-cohort picks to the library's (expected value only; flags unchanged).
- The `RosettaDectestSkips` and `RosettaIntelSkips` per-line vector filters are
  ported verbatim.

The full 22+22 compare-predicate `_ctx` set was completed (the Intel corpus
exercises all of them). `bid128_pow`/`cbrt`/trig are Intel-excluded, so
pow/pown/rootn/compound are covered solely by the **native** corpus (bitwise
value + flags) — plus the focused in-crate `wave_*` unit tests.

Not ported (test-infra niceties, noted for later): the `RosettaSiblings`
ladder-consistency check and the `testIntel/DectestOperatorCoverage` meta-tests.

--------------------------------------------------------------------------------
## 5. Math (§9)

exp/exp10, ln/log10 use the Swift D38-domain [9,9] Padé kernels — the constant
tables transliterate byte-for-byte (`D38::from_raw(qExpAndSignBit, lo, hi)`, made
`const fn` so the tables are `const [D38; N]`; top-bit-set limbs as
`0x…u64 as i64`). pow = `exp10(y·log10(x))` (single round + GDAS preferred
exponent); pown = binary exponentiation; rootn = repeated correctly-rounded √ for
power-of-two n, else via pow; compound = `(1+x)^n` via pown. The bar is
correctly-rounded for the decTest vectors (faithful Padé, not a redesign);
trig/inverse/hyperbolic are permanently out of scope.

--------------------------------------------------------------------------------
## 6. The public wrapper + finance (`WrapperLayer.md`, `Finance.md`)

The public `Decimal128` surface lives at the crate root (`mod wrapper; pub use
wrapper::*`), encapsulating the engine `D128` zero-cost (D-R9). It uses Rust's
full idiom, unbound by the engine's constraint regime — the per-port divergences
(`WrapperLayer.md §5`) applied to Rust:

- **`Decimal128`** = `#[derive(Clone, Copy)] struct { core: D128 }`; **IEEE
  `PartialEq`/`PartialOrd`, no `Eq`/`Ord`/`Hash`** — exactly `f64`'s shape
  (`+0 == -0`, NaN unequal/unordered). `std::ops` operators (`+ - * /` + assign,
  unary `-` = bit-level negate).
- **Three-form arithmetic** by name suffix (the operators are the bare
  ties-to-even form): `adding_rounding`/`adding_context`, etc.; the
  engine-context-only ops (fma/sqrt/math/remainder/…) get bare + `_context`.
  `pow` surfaces as `raised_to` (Swift `raised(to:)`); `pown`/`rootn` stay
  engine-internal.
- **Supporting types** (discriminants mirror the engine codes, so each crossing
  is a cast / `from_raw`): `Rounding`(0–4), `DecimalStyle`(0–3),
  `DecimalComparison`, `IeeeClass`(0–9, custom — Rust's `FpCategory` has only 5),
  `DecimalFlags` (newtype bitset), `DecimalContext` (wraps the engine `Context`;
  its `Cell` flag sink makes it `!Sync`, so the compiler enforces the
  "one context per task" rule Swift can only document).
- **Interchange** uses native `u128` directly (`from_bid_bits`/`bid_bits`, dpd) —
  no hi/lo split (unlike the JVM ports); the `U128` newtype surfaces only inside
  those bodies (§4.7).
- **Parse**: `Decimal128::parse(&str) -> Option` (context-free);
  `DecimalContext::parse_or_nan(&str) -> Decimal128` (GDAS: round + flag, NaN on
  malformed). `from_i128_exactly`/`from_u128_exactly -> Option` for the
  `exactly:` >34-digit failure (Option, not `TryFrom` — matches `init?`).
- **Formatting** (`string(style)` + `Display`/`Debug`) is `std`-gated.

**BasicFinance** lives in **Core** (`Finance.md §2`), not the wrapper, so every
port runs one byte-identical algorithm: the 13 `d128_*_tte` compositions
(interest, mortgage/amortization, annuity/single-flow, npv/irr/mirr) over the
math ops, single ties-to-even form (§3), `irr` non-convergence → `D128_QNAN0`
(§5.1), preconditions via `verify!` (§5.2). The public **`Finance`** facade is an
uninstantiable `enum Finance {}` namespace forwarding to it, mapping the `irr`
NaN sentinel → `Option`. The engine + facade are `std`-gated (the schedule /
cash-flow APIs allocate).

**Validation:** the **WrapperRosetta** (`tests/rosetta/wrapper.rs`) reuses the
engine harness's corpus parsers but re-points dispatch + comparison at the
**public** API only — operands via `from_bid/dpd_bits` / `parse_or_nan` / `parse`,
results compared by rendered string (dectest) / cohort (fptest) / canonical BID
(Intel), the predicate family derived from the three-way `compared`. It shares
the parsers in-crate (no copy — the Rust analog of the C "link, don't copy"
note). **46 507 / 0**, exact ecosystem parity. Public-API unit tests live in
`tests/wrapper.rs` (the first tests that legitimately can — they touch only the
public surface); finance is checked tolerance-based per `Finance.md §8`.

--------------------------------------------------------------------------------
## 7. Status summary

| Layer / area              | State                                            |
|---------------------------|--------------------------------------------------|
| Primitive                 | complete                                         |
| Core — finalize/round     | complete                                         |
| Core — D38 engine         | complete                                         |
| Core — D128 §5 ops        | complete (arith, compare 22+22, parse, print, serde, sqrt, min/max, quantize, scaleB/logB, nextUp/Down, totalOrder, toIntegral, convertToInt64) |
| Core — §9 math            | complete (exp/exp10, ln/log10, pow, pown, rootn, compound) |
| BasicFinance (Core)       | complete (std-gated)                             |
| Rosetta — engine          | complete (dectest + fptest + Intel + native; 52 820/0) |
| Public `Decimal128` wrapper | complete (D-R9)                                |
| Rosetta — public API      | complete (46 507/0, exact parity)               |
| Public `Finance` facade   | complete (std-gated)                            |

The port now mirrors the Swift reference's full stack. Deferred test-infra
niceties: `RosettaSiblings`, the operator-coverage meta-tests.
