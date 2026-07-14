---
layout: default
permalink: /whitepapers/benchmark-matrix.html
title: "Benchmark Matrix: Operation Categories, Input Generators, and Alternative-Implementation Parity — Decimal128"
description: "The benchmark matrix for the multiplatform decimal128 library: per-operation input categories, generators, alternative-implementation baselines, and measurement methodology."
heading: "Benchmark Matrix"
---


*First draft*

## 1. Purpose and Scope

This document specifies the **benchmark matrix** for the multiplatform decimal128
library: the per-operation *input categories* that exercise distinct internal
paths, the *input generators* that target each category, the *alternative-implementation
baselines* and the parity settings required to compare against them fairly, and
the *measurement methodology* and *reporting format*.

The goal is **attributable** performance results: each category isolates one
path-selecting variable so that a slope, a regression, or a shortfall against an
alternative implementation can be localized to a specific kernel or finalize path
rather than averaged away. These categories drive cross-port comparison (all eight
cores: Swift, C, Java, Kotlin, Rust, Go, C#, Zig) and comparison against external
**alternative implementations** (Intel `libbid`; IBM/Cowlishaw
`libdecnumber`/decNumber; Stefan Krah's `libmpdec`/mpdecimal, measured **directly
as a C peer** — distinct from the `decimal.Decimal` interpreter path that wraps it;
`java.BigDecimal`; Python `decimal.Decimal`; .NET `System.Decimal`; for Swift,
Foundation's built-in `Decimal` and the `mgriebling/DecimalNumbers` package; and
for Rust, the `rust_decimal` crate). One system is **explicitly excluded** as
non-distinct — GCC's `libgcc` decimal runtime (§5.1).

We use *alternative implementation* (not "competitor") deliberately: these are
fellow decimal libraries we measure against and learn from, several of them
long-standing references in their ecosystems.

It does **not** specify the harness implementation, the BID/UBD conversion at
the bench boundary, or the per-port build wiring; those live with each port's
benchmark code (e.g. `decimal128-c` `bench/`). The category taxonomy here is the
contract those harnesses implement; the as-measured numbers live in the results
hub **`BenchmarkResults.md`**. Companion documents:
`CrossPlatformArchitecture.md` (the engine paths these categories map to),
`PrimitiveLayer.md` (the divPow10 / divide kernels), `BenchmarkResults.md`
(consolidated results), and the legacy `decimal128-c` `bench/BENCHMARK_FINDINGS.md`.

## 2. Principles

- **One category = one input partition = one path.** A category fixes the
  variable that selects a code path (alignment for add/sub, product width for
  multiply, divisor width for divide) and holds the rest representative, so the
  measured cost belongs to that path.
- **Width-driven vs value-driven.** Most categories are *width-driven* (selected
  by digit lengths / exponent gaps, deterministic from operand shape). A few are
  *value-driven* (power-of-ten divisor, exact/terminating quotient) and require
  constructed inputs.
- **Representative magnitude profiles, not max-width defaults.** Operand coefficient
  *width* is an orthogonal axis (§2.1), not a fixed default. Defaulting to full
  34-digit coefficients is **unrepresentative and unfair to the fast paths**, and it
  is **not enough merely to stay under 112 bits**: in financial workloads essentially
  all operands *before any division* fit in **64 bits (≤ 19 digits)**, and several
  alternative implementations have their own **64-bit fast paths** (e.g. BigDecimal's
  `intCompact` long path, libmpdec's single-word path). The realistic profile must
  therefore land squarely in the **64-bit regime** — both because that is the actual
  data and because only there do we compare our fast path against *their* fast path
  like-for-like. A 34-digit default would measure everyone's wide path and hide that
  real workloads exercise everyone's 64-bit path. Each operation is run under realistic
  magnitude profiles (§2.1), with full-width (34-digit) retained as a **separately
  reported stress diagnostic**, never the headline.
- **Deterministic generators.** Every generator is seeded with a fixed per-category
  PRNG seed for reproducibility, and asserts the *realized* band of each generated
  pair (e.g. the actual product `digitLen` landed in the target band) before the
  vector is admitted.
- **No silent truncation.** If a generator cannot fill a band (e.g. too few
  exact-terminating cases at a given width), it reports the shortfall rather than
  padding with off-band inputs.

### 2.1 Operand Magnitude Profiles (cross-cutting axis)

Operand coefficient **width** (significant-digit count) is orthogonal to the
path categories of §3 and is decisive for the *fast paths* — both ours and the
alternatives' — which are gated on fixed bit widths, not on the
alignment/product/divisor category:

- **our** add/sub same-exp pack-direct: coefficient sum **< 2¹¹²** (≈ 33.7 digits)
- **our** add/sub near-aligned pack-direct: result **< 10³⁴**
- **our** multiply `_tte` 64×64 path: **both coefficients < 2⁶⁴** (≈ 19 digits);
  general pack-direct: product **< 2¹¹²**
- **alternatives'** 64-bit paths: BigDecimal `intCompact` (unscaled value fits a
  `long`), libmpdec single-word coefficient, and likely others — all keyed on the
  operand fitting in **64 bits**

So the same category (say SQ add) lands on a *different* path — in our code and in
theirs — depending purely on operand width. Each category is therefore measured
under one or more **magnitude profiles**, and the headline number uses a realistic
profile — not full width.

| Profile | Width distribution | Exponents | Role |
|---|---|---|---|
| **P-fin** (financial / 64-bit) | coefficients **< 2⁶⁴ (≤ 19 sig digits)** — the reality for source financial data before any division | clustered at currency scale (e.g. qExp ∈ {0, −2, −4}; a minority of higher-precision rates) | **Headline for add/sub and mul.** Both operands fit 64 bits ⇒ our pack-direct / 64×64 fast paths fire, *and* the alternatives' 64-bit fast paths fire — a true like-for-like comparison at the size that dominates production. |
| **P-gen** (general) | significant digits log-uniform over **1–34** (favoring smaller; spans the >64-bit regime that arises from prior **division results**) | full representable range | All-purpose profile; covers operands wider than 64 bits (e.g. a quotient fed into a later add). |
| **P-max** (full-width stress) | significant digits pinned at **33–34** | chosen to drive each category's wide path | Worst-case **diagnostic** only — reported separately, never the headline. |

Why the 64-bit boundary, not 112: financial source data is ≤ 19 digits, and 64 bits
is where the alternatives concentrate their optimizations; restricting only to
"< 2¹¹²" would still let an alternative's 64-bit path beat a 100-bit operand of ours
and misattribute the gap. The **only** way a financial operand exceeds 64 bits is as
the *result of a division* (a quotient can reach 34 digits); P-gen covers that tail.

The "width distribution" column is a **digit-length** distribution, realized by
digit-length-first sampling (draw `d`, then a uniform `d`-digit value) — *not* a
uniform draw over the integer range, which would collapse to the top decade. See §4.

Rules:
- **Report the profile in every result row.** A bare "add OQ" number is
  meaningless without its profile.
- The default headline profile is **P-fin** for add/sub and multiply; **P-gen** adds
  the post-division wider-operand tail. (Divide is special — see §3.3: even with
  64-bit *inputs* its intermediates are always ≥ 35 digits.)
- **P-max is never dropped** — the wide path is real and must be tracked — but it
  is labeled `stress` and excluded from headline/marketing ratios.
- Exact width distributions are tunable; the parameters above are the starting
  point and an open item (§9) pending real workload sampling.

## 3. Operation Category Taxonomy

The canonical two/three-letter codes below are the stable identifiers used in
code, comments, generators, and result tables across all ports.

### 3.1 Add / Subtract — by operand qExponent alignment

Renames and extends the former SE/NE/FE split (the new band is **OQ**). The
driver is the alignment relationship between the operands' quantum exponents.

For operands with the larger-MSD operand **L** and the smaller **S**, let
`Δ = |qExp(x) − qExp(y)|`, let the result span
`resultDigits = maxMSDpos − minLSDpos + 1`, and let `trim = max(0, resultDigits − 34)`
(the low digits discarded ⇒ the `divPow10` width on the unaligned path).

| Code | Name | Condition | Path / cost |
|---|---|---|---|
| **SQ** | Same qExp | `Δ = 0` | coefficients pre-aligned; direct add/sub, residue `EXACT`, no `divPow10`. Fastest. |
| **NQ** | Near qExp | `1 ≤ Δ ≤ 4`, `trim = 0` | small align shift on the **pack-direct** fast path, result ≤ 34 digits, no rounding (residue `EXACT`). Both operands fully retained. |
| **MQ** | Middle qExp | `Δ > 4`, `trim = 0` | larger align shift ⇒ the **qAlignDelta>4** path, still no rounding (result ≤ 34 digits, residue `EXACT`). Splits the no-round region at the pack-direct boundary (`Δ ≤ 4`). |
| **OQ** | Overlapping qExp | `trim ≥ 1` **and** S's MSD ≥ the post-trim result LSD | genuine align + round: wide `divPow10` over a coefficient that includes S's digits; residue any of LT/HALF/GT. The heaviest add/sub path. |
| **FQ** | Far qExp | S entirely below the kept 34 digits (`shiftRight > digitLen` ⇒ fully swamped; `==` borderline) | swamped fast path: S contributes only a sub-half sticky residue; the wide `divPow10` and the coefficient add are skipped. |

Notes:
- **Width gates the fast path, so the magnitude profile (§2.1) is decisive here.**
  SQ packs directly only when the coefficient sum is `< 2¹¹²` (`hi49 sum < 2^48`);
  NQ (shift ≤ 4) packs only when the result is `< 10³⁴`. Under **P-fin** the great
  majority of SQ/NQ hits these pack-direct paths (the production-realistic result);
  **P-max** (34-digit) pushes the same categories into the wide finalize. Both must
  be measured and reported with their profile — the 34-digit number alone misrepresents
  add/sub.
- With **full 34-digit operands** (P-max), any `Δ ≥ 1` already forces `trim ≥ 1`, so
  **neither NQ nor MQ is feasible** — both need `digitLen(L) + Δ ≤ 34` (narrower
  operands), which P-fin and P-gen produce naturally. SQ, OQ, FQ are reachable at any
  width, so P-max's add/sub set is **SQ / OQ / FQ only**.
- **SQ / NQ / MQ are the compact-alternative-comparable bands; OQ / FQ are not.** To
  let the 28-digit idiom peers (rust_decimal / System.Decimal / Foundation.Decimal) run
  on the *same* operands, P-gen generates SQ/NQ/MQ with **qExp ∈ [0, −8]** (scale ≤ 8)
  and coefficients sized so the add/sub **result** stays `< 10²⁸` (≤ 28 significant
  digits — covers both the sum and the opposite-sign subtract carry). `Δ ≤ 8` follows
  from the qExp window, so NQ (`Δ ≤ 4`) and MQ (`Δ 5–8`) partition it. **OQ/FQ** round /
  swamp and span > 28 digits, so no compact alternative can hold them — **libbid is the
  reference peer there** (and the full-34-digit peer everywhere; §8, §5).
- **Subtract cancellation is a cross-cutting modifier, not a fifth band.** Near-equal
  operands (small `Δ`, close coefficients) produce catastrophic cancellation — a
  few result digits with a normalization shift — exercising a different finalize
  cost within SQ/NQ. Generators must include a *cancellation* variant of SQ and
  NQ for subtract (tag `SQ-x`, `NQ-x`).

### 3.2 Multiply — by product digitLen

The driver is the significant-digit count of the exact product, which is exactly
the 128-bit / 256-bit `divPow10` (recipMulPow10 / "rmp10") boundary (38 digits is
the largest that fits in 128 bits; 39 needs 256).

| Code | Name | Condition `d = digitLen(product)` | Scaling |
|---|---|---|---|
| **CP** | Compact Product | `d ≤ 34` | none — pack directly, no `divPow10` |
| **WP** | Wide Product | `35 ≤ d ≤ 38` | small scale: **128-bit** `recipMulPow10` |
| **XP** | eXtra-wide Product | `d > 38` (up to 68) | full scale: **256-bit** `recipMulPow10` |

The realized product `digitLen` is `digitLen(x) + digitLen(y)` or that minus 1
(carry-dependent); generators assert the realized band, not the nominal sum.

**Fast-path note (operand width within CP).** CP is the no-scale band, but it
further splits on operand width: when **both coefficients are < 2⁶⁴** (≈ ≤19 digits
each) the `_tte` path takes the single `mul_128_64x64` (64×64) kernel; wider CP
operands take the 128×128 product with a direct pack while the product stays
`< 2¹¹²`. Under **P-fin** (e.g. price × quantity) the 64×64 sub-case is common, so
the CP generator must include it explicitly (tag `CP-64`) — otherwise CP measures
only the 128×128 path and understates the realistic multiply.

### 3.3 Divide — by divisor digitLen (+ value-driven fast paths)

Key fact for the **WD/XD scaled path** (`divFnzFnz`, `CrossPlatformArchitecture.md`):
the numerator is scaled by `numeratorScale = 34 − (digitLen(x) − digitLen(y))`, so the
**scaled dividend always has exactly `34 + digitLen(y)` significant digits** — the dividend
`digitLen(x)` cancels. Therefore **`digitLen(y)` alone selects the divide kernel**,
setting both the dividend width and the divisor limb count. **CD-width divisors
(`digitLen(y) ≤ 4`) no longer take this scaled path** — they use the quotient-first divide
(§2.4.10), which integer-divides the *unscaled* `cx` and fills the fraction from the
remainder (see the CD/ET rows and notes below).

| Code | Name | Condition `digitLen(y)` | Scaled dividend | Divisor | Kernel (cost) |
|---|---|---|---|---|---|
| **CD** | Compact Divide | `1–4` | — (no scale) | 1 word (< 2⁶⁴) | **quotient-first** (§2.4.10): 128÷64 integer divide of unscaled `cx` + a small remainder-only fraction divide; `R0==0` early-out |
| **WD** | Wide Divide | `5–~19` | 39–53 dig (2²⁵⁶) | 1 word | 256÷64 single-reciprocal (scaled path) |
| **XD** | eXtra Divide | `~20–34` | 54–68 dig (2²⁵⁶) | 2 words (≥ 2⁶⁴) | 256÷128 Möller–Granlund, reciprocal build + 2× DIV3BY2 (costliest) |

Value-driven categories (orthogonal to width):

| Code | Name | Condition | Path |
|---|---|---|---|
| **PT** | Power-of-Ten divisor | `y = 10^k` — divisor coefficient is a power of ten (cohort-invariant: `Cy == 10^(digitLen(y)−1)`) | exact, coefficient-preserving result via the dedicated `divPow10Divisor` fast path (one dword compare → trailing-zero strip + `finalize`); **skips the divide kernel** (CrossPlatformArchitecture §2.4.9) |
| **ET** | Exact / Terminating | `x/y` exact (residue `EXACT`) | bench draws ET at **CD width**, so it takes the quotient-first path (§2.4.10): the exact case (`R0==0`) terminates with no rounding and no strip — d128's biggest divide deficit, now a win (run h4). A terminating *fraction* (`remF==0`) still strips toward the preferred exponent |

Notes:
- **WD and XD use the scaled-numerator path**; the genuine kernel switch is **WD → XD**
  (single-word → two-word M&G) at the `y.dw1 == 0` boundary (≈ digitLen 19–20), recorded
  by the realized `digitLen(y)`. **CD diverges (run h4, §2.4.10):** for `digitLen(y) ≤ 4`
  the quotient-first path integer-divides the *unscaled* `cx` (128÷64), so CD no longer
  pre-scales to a ≥35-digit dividend — its cost dropped (41 → 38 ns, libbid 0.90× → 0.97×).
- For WD/XD the scaled dividend is **always ≥ 35 digits**, so those bands have **no
  width-driven "free" tier** (unlike multiply's CP). The cheap divides are the value-driven
  fast paths **PT** (`divPow10Divisor`) and **ET** (quotient-first `R0==0` early-out, 8.3 ns)
  plus the CD quotient-first improvement. For WD/XD specifically, **64-bit inputs still do
  not make divide cheap** — a P-fin dividend and ≥5-digit divisor produce a ≥ 35-digit
  scaled dividend and run the full wide divide.
- **Under P-fin the divisor is ≤ 19 digits (64-bit), so financial divide is always
  CD or WD — never XD.** XD requires `digitLen(y) ≥ 20`, i.e. a two-word divisor,
  which in a financial pipeline only arises when the divisor is itself a wide value
  (typically a prior **division result**). So XD belongs to P-gen/P-max; the realistic
  financial divide headline is CD/WD (single-word-divisor kernel) with ≤ 19-digit
  divisors.
- `digitLen(x)` is free to vary (it cancels from the path); generators set it per
  profile for realism (§4.3), not because it changes the kernel. The 128÷128 sub-branch
  of `u256DivRem_128` is **unreachable from d128 divide** — it serves sqrt/D38 and is
  out of scope for this matrix.

### 3.4 FMA — by finalize path (FN / FF)

FMA (`self + lhs·rhs`) has two cost axes — the product width (§3.2) and the addend
alignment (§3.1) — but crossing them (15 cells) is disproportionate for an op almost
nobody uses, and neither axis is where the cost lives: FMA is dominated by finalizing
the wide (~68-digit) intermediate. The one actionable distinction is **binary — does
the result land on the fits-128 fast path or the genuinely-wide (256-bit Barrett)
finalize?** So FMA gets **two bands**, both with a wide product (33–34-digit `lhs`/`rhs`,
~66–68-digit product) and `self`'s exponent selecting the path:

| Code | Name | Condition | Path / cost |
|---|---|---|---|
| **FN** | FMA Near | `self` exponent **inside** the product's digit span | the full wide product survives ⇒ **256-bit Barrett finalize** (slow). |
| **FF** | FMA Far | `self` far **above** the product MSD | product rounds off ⇒ result **fits 128 ⇒ fits-128 fast path** (fast; ≈ 2× FN cross-port). |

FMA is **d128-only** (no compliant decimal FMA in the alternatives, so no peer column)
and **regime-based, not a magnitude profile** — one FN/FF set (P-gen-width operands),
run as its own sweep (`SWEPT_PROFILE=FMA`, corpus `swept/FMA/{FN,FF}.txt`, 3 operands
per line: `self lhs rhs`). Reported in §4.4.

sqrt and the IEEE 754 §9.2 recommended functions (exp/ln/pow/…) have their own internal
iteration counts; they are **out of scope for the first matrix** and are tracked as a
follow-up (§9, Open Items).

## 4. Input Generators

Each generator yields a vector set of operand pairs for one category **under a
magnitude profile** (§2.1), seeded deterministically, asserting the realized band
per pair. Every generator runs under at least the headline profile **and** P-max;
operand widths come from the profile, *not* a fixed 34.

**Coefficient sampling is digit-length-first, never uniform over the integer range.**
A uniform draw over `[0, 2⁶⁴)` lands at 19–20 digits ~99% of the time (the top decade
dominates the range), so it would almost never exercise short operands and would
collapse a profile's width distribution. Instead, to draw one coefficient:

1. draw a digit length `d` from the profile's **digit-length distribution** (the §2.1
   "width distribution" column — e.g. uniform over `[1, 19]` for P-fin, log-uniform
   over `[1, 34]` for P-gen, fixed `33–34` for P-max);
2. draw a uniform integer in `[10^(d−1), 10^d − 1]` (exactly `d` significant digits).

Sign and exponent are drawn separately per the category/profile. This makes the
profile's width distribution the *direct* control knob and gives even coverage across
widths (and thus across the fast/slow path boundaries) rather than the integer-uniform
bias toward the maximum width.

### 4.1 Add / Subtract generators

Parameters: `(profile, Δ, sign-pattern)`; coefficient widths drawn from the profile.
Headline **P-fin**; also run **P-max**. (P-fin keeps sums < 2¹¹², so SQ/NQ land on
the pack-direct fast path, MQ on the `qAlignDelta>4` no-round path; P-max forces the
wide finalize.) **Under P-gen, SQ/NQ/MQ use the compact construction** (§3.1 note):
qExp ∈ [0, −8] and widths sized so the result stays `< 10²⁸`, so the compact idiom
peers can run on the same operands. OQ/FQ keep the profile's full width/exponent range.

- **SQ:** `Δ = 0`; widths per profile (P-gen: qExp ∈ [0,−8], both operands ≤27 digits ⇒
  sum ≤28). Subtract variant `SQ-x`: draw the second operand within a small ULP window
  of the first (cancellation).
- **NQ:** `1 ≤ Δ ≤ 4` (pack-direct), `trim = 0` via `digitLen(higher) + Δ ≤ 27` so the
  result ≤28 digits (P-gen compact; P-fin/P-gen produce the no-round condition naturally;
  infeasible under P-max). Subtract variant `NQ-x`: near-cancellation within the window.
- **MQ:** `5 ≤ Δ ≤ 8` (the `qAlignDelta>4` path), same `trim = 0` construction as NQ with
  the wider gap. Infeasible under P-max.
- **OQ:** widths per profile with `Δ` large enough that `trim ≥ 1`, drawn so the
  residue distribution spans LT/HALF/GT (include exact-half cases for ties). Most
  prominent under P-max; under P-fin it occurs when a small operand straddles a
  modest-width result's LSD.
- **FQ:** `Δ` large enough that S is fully swamped. Include the borderline case
  explicitly (Fully vs Borderline Swamped).

### 4.2 Multiply generators

Parameters: `(dlX, dlY)`, chosen so the realized product lands in the band. The
operand widths within a band track the profile (§2.1); headline **P-fin** (both
operands ≤ 19 digits, so the product is ≤ 38 digits and lands in **CP or WP** — with
the `CP-64` sub-case common — never XP), with **P-gen** for the wider post-division
tail and **P-max** for the deepest 256-bit scale.

- **CP:** `dlX + dlY ≤ 34` (e.g. 17×17, also 1×33 to vary shape). Include the
  **`CP-64`** sub-case (both operands `< 2⁶⁴`, ≈ ≤19 digits each) that takes the 64×64
  `_tte` kernel — the common P-fin case (price × quantity).
- **WP:** `dlX + dlY ∈ {35..38}` (e.g. 18×18, 19×19).
- **XP:** `dlX + dlY ≥ 39` (e.g. 20×20 … 34×34 for the deepest 256-bit scale).

Square (`x·x`) is a sub-generator of each band (`CP²/WP²/XP²`) since it has its own
fast-path prologue.

### 4.3 Divide generators

Parameters: `(dlX, dlY)`, binned by the divisor. `digitLen(x)` cancels from the path
(§3.3) so it is set per profile only for realism (default a profile-typical width;
P-max uses 34); `digitLen(y)` is the band driver and under P-fin/P-gen follows the
realistic *small-divisor-common* distribution:

- **CD:** `digitLen(y) ∈ {1..4}`.
- **WD:** `digitLen(y) ∈ {5..19}` (assert `y.dw1 == 0`).
- **XD:** `digitLen(y) ∈ {20..34}` (assert `y.dw1 != 0`).
- **PT:** `y = 10^k` over the representable exponent range.
- **ET:** construct `x = y · q` for random `q` (guarantees exact), or draw `y` whose
  coefficient factors only into 2 and 5; spread across CD/WD/XD widths and record the
  strip count distribution.

Within CD/WD, optionally sweep `dlX ∈ {4, 19, 34}` to expose the dividend-width
sub-effect (same kernel, fewer significant limbs).

### 4.4 FMA generators

Regime-based, not profile-based (§3.4): one FN/FF set of `self lhs rhs` triples.
`lhs`/`rhs` are 33–34-digit coefficients at a fixed small exponent ⇒ a ~66–68-digit
product (value ~1e9, spanning exp ~9..−58). `self` is a 1–3-digit coefficient whose
exponent selects the finalize path:

- **FN:** `self` exponent **inside** the product's span (e.g. exp −4..4) ⇒ the wide
  product survives ⇒ 256-bit Barrett finalize (slow).
- **FF:** `self` exponent far **above** the product MSD (e.g. exp 18..24) ⇒ the product
  rounds off ⇒ result fits 128 ⇒ fits-128 fast path (fast).

d128-only (no decimal-FMA peer); run as its own sweep (`SWEPT_PROFILE=FMA`).

## 5. Alternative Implementations and Parity

| Alternative | Kind | Parity required | Caveats |
|---|---|---|---|
| **Intel `libbid`** | Native IEEE decimal128, fixed 128-bit, BID encoding | Default nearest-even; convert UBD↔BID at the bench boundary | The truest apples-to-apples **BID** peer. **Alignment-flat** where our ports are alignment-sloped — directly probed by SQ→FQ and CD→XD. |
| **`libdecnumber` / decNumber** (IBM/Cowlishaw) | The reference General Decimal Arithmetic implementation. `decQuad` = fixed 128-bit decimal128 (DPD); `decNumber` = arbitrary precision. (Vendored in GCC as `libdecnumber/`.) | `decQuad` is decimal128 natively; for `decNumber`, `decContextDefault(&ctx, DEC_INIT_DECIMAL128)` (digits 34, emax 6144, emin −6143, `ROUND_HALF_EVEN`, clamp) | The canonical correctness oracle and the lineage of our dectest corpus. `decQuad` is a second true fixed-128 peer alongside libbid — the **DPD** lineage vs libbid's BID. Software; C library ⇒ same-process, ratio-clean with the C arm. |
| **`java.BigDecimal`** | Arbitrary-precision (BigInteger; `intCompact` long fast path) | Pin `MathContext.DECIMAL128` (prec 34, `HALF_EVEN`); pass it to `divide` | Not fixed decimal128: cost is digit-driven with no 34-digit ceiling. Strong on CP/CD (small via `intCompact`), degrades with width. `divide()` **throws** on non-terminating without a MathContext — interacts with ET. |
| **`libmpdec` / mpdecimal** (Stefan Krah) | Arbitrary-precision decimal, pure C; the library **underneath** CPython's `decimal`. **single-word fast path** for small coefficients; radix-10⁹ limbs otherwise | `mpd_context_t` set to IEEE-128 semantics (`mpd_ieee_context(&ctx, 128)` ⇒ prec 34, Emax 6144, Emin −6143, `MPD_ROUND_HALF_EVEN`, clamp) | The **direct** C measurement of the engine that Python's `Decimal` wraps — linked into the C bench on identical BID operands, **no CPython in the loop** (distinct from the Python row below, which is the same kernel *through* the interpreter; the gap between them pins interpreter overhead at ~27 ns/op). Not fixed decimal128: arbitrary precision, digit-driven cost, no 34-digit ceiling; its single-word path makes the **P-fin (64-bit)** regime its strong suit. Native C ⇒ same-process, **ratio-clean** with the C arm. |
| **Python `decimal.Decimal`** | Arbitrary-precision over libmpdec (C-accelerated; **single-word fast path** for small coefficients) | `Context(prec=34, Emax=6144, Emin=-6143, clamp=1, rounding=ROUND_HALF_EVEN)` | Same digit-driven-cost caveat; its single-word path makes the **P-fin (64-bit)** regime its strong suit. Separate-language harness ⇒ order-of-magnitude external baseline, not a same-process ratio. The **`libmpdec` row above is the same kernel measured directly** (no interpreter), so this row isolates CPython overhead rather than the arithmetic. |
| **`mgriebling/DecimalNumbers`** (Swift package) | Pure-Swift IEEE 754 decimal128 | Native decimal128 nearest-even; same 34-digit format | The apples-to-apples **Swift** peer (same format and precision). **BLOCKED on Swift 6.3** (as of 2026-06-25), two-part: (1) build — `main` uses the pre-3.2 `mgriebling/UInt128` API, but the dep floats to 3.2.0 which renamed it; pinning UInt128 to 3.1.0 fixes the build; (2) runtime — UInt128 3.1.0's `init(integerLiteral: StaticBigInt)` then traps ("Not enough bits to represent the passed value") on the ≥128-bit table literals; 3.1.5/3.2.0 fix that init but break the build. No off-the-shelf version both builds and runs ⇒ needs a fork/patch of one of the two unmaintained libs. `Foundation.Decimal` is the substitute. |
| **Swift `Foundation.Decimal`** (built-in) | Foundation value type; ~38-digit base-10, `NSDecimalNumber`-backed | Rounding via `NSDecimalNumberHandler` (`HALF_EVEN`) | **Not** IEEE decimal128: ~38 significant digits, a different cohort/exponent model, and no decimal128 special-value semantics. Treat as the *idiomatic Swift baseline* (what a Swift developer reaches for today), not a conformance peer. |
| **`rust_decimal`** (Rust crate) | Fixed 128-bit, pure Rust: 96-bit integer mantissa + scale 0–28 + sign; **financial-focused** | Default banker's rounding (`RoundingStrategy::MidpointNearestEven`); match scale/rounding | **Not** IEEE decimal128: 96-bit mantissa ⇒ ~28 significant digits (vs 34), scale limited to **0–28**, **no Inf/NaN**, smaller range. The *idiomatic Rust financial baseline* (what a Rust developer reaches for), not a conformance peer. Native Rust ⇒ same-process, ratio-clean for the Rust port; well-tuned for small/P-fin values. |
| **.NET `System.Decimal`** (C# `decimal`) | Fixed 128-bit BCL value type: **96-bit integer mantissa + scale 0–28 + sign** — the design `rust_decimal` was modeled on; **financial-focused** | Operators round the 29th digit (banker's not guaranteed on `*`/`/`); no context object — precision/range are fixed by the type | **Major non-compliant** peer, same class as `rust_decimal`: 96-bit mantissa ⇒ **~28–29 significant digits** (vs 34), scale **0–28**, **no Inf/NaN** (throws `OverflowException`/`DivideByZeroException`), smaller range. The *idiomatic .NET financial baseline* (what a C# developer reaches for), **not** a conformance peer. **A native d128 C# port now exists** (`decimal128-csharp`), so `System.Decimal` is measured **in-process, ratio-clean** against it (the `rust_decimal` model — BenchmarkDotNet, both types on identical operands per band); it was previously only a standalone cross-language baseline. Wide bands (WP/XP/WD/XD) and all P-max **overflow the 28-digit mantissa ⇒ d128-only** (as with `rust_decimal`); only the P-fin compact regime is a head-to-head. |

The alternatives with explicit **64-bit fast paths** (BigDecimal `intCompact`,
libmpdec single-word) are precisely why the **P-fin profile is mandatory** (§2.1):
only a 64-bit-regime workload pits our small-operand fast path against theirs at the
operand sizes that dominate real financial use. Comparing only at wide widths would
flatter or unfairly penalize us depending on whose wide path is better, and would
miss the comparison that actually matters in production.

The two fixed-128 peers, **libbid (BID)** and **decNumber/decQuad (DPD)**, together
cover both IEEE decimal128 encoding lineages, so a slope that appears against one but
not the other localizes to the encoding rather than the arithmetic.

### 5.1 Explicitly Excluded: GCC `libgcc` decimal (`__bid_*` / `__dpd_*`)

GCC's `libgcc` decimal runtime is **not an algorithmically distinct implementation**
and is excluded to avoid double-counting. What sits underneath is fixed at build time
by the chosen encoding:

- **BID configuration** (`--enable-decimal-float=bid`, the default on x86/x86-64):
  the `__bid_*` runtime routines are built from a vendored copy of Intel's libbid
  (`libgcc/config/libbid/`). This is the **same code already in our inventory as
  `libbid`** — identical kernels, merely `__bid_`-prefixed.
- **DPD configuration** (`--enable-decimal-float=dpd`, the default on POWER/s390):
  the `__dpd_*` routines are GCC's `libgcc/config/dfp-bit.*` wrapping IBM's decNumber
  (`libdecnumber/`) — the **same lineage as `libdecnumber`/decQuad above**.

The dispatch layer (`dfp-bit.c`/`.h`) that the compiler's `_Decimal*` operations
lower to is GCC's own thin glue; the arithmetic kernels are vendored third-party code
in both configurations. So `libgcc` decimal adds no new algorithm: the BID path *is*
libbid, the DPD path *is* decNumber, both already covered above. (If the compiler's
build-integration / lowering overhead were ever of interest, it could be measured as a
*packaging* variant — not as a distinct arithmetic implementation.)

## 6. Pairing and Harness Plan

| Pair | Harness | Comparison quality |
|---|---|---|
| `decimal128-c` ↔ `libbid` & `libdecnumber` (`decQuad`) | shared C / Google Benchmark, both linked in-process (libbid the BID peer, decQuad the DPD peer; libbid the invariant control) | ratio-clean (extend the existing pairing table to the §3 categories) |
| `decimal128-c` ↔ `libmpdec` (mpdecimal) | shared C / Google Benchmark, linked in-process on identical BID operands (no CPython) | ratio-clean; the **direct** arbitrary-precision C peer (runs `Rmpd`/`xc2`), distinct from the Python `Decimal` baseline below which wraps the same kernel |
| `decimal128-java` ↔ `java.BigDecimal` | JMH, same process | clean — **requires reviving the JMH arm** (currently removed) |
| `decimal128-swift` ↔ `Foundation.Decimal` (and `mgriebling/DecimalNumbers` once it builds) | shared Swift harness (same-process loop) | ratio-clean; `Foundation.Decimal` is the idiom baseline (in place). `DecimalNumbers` is the intended conformance peer but is **blocked on Swift 6.3** (stdlib `UInt128` collision, see §5) |
| `decimal128-rust` ↔ `rust_decimal` | shared Rust harness (same-process loop) | ratio-clean; idiom baseline only (28-digit, no specials — not a conformance peer) |
| `decimal128-csharp` ↔ .NET `System.Decimal` | shared C# **BenchmarkDotNet** harness (`decimal128-csharp/benchmarks/`), both types on identical operands per band | ratio-clean; idiom baseline only (28-digit, no specials — not a conformance peer). Compact bands only (wide/P-max overflow `System.Decimal` ⇒ d128-only) |
| `decimal128-zig` ↔ `libbid` (BID) | Zig harness (`decimal128-zig/bench/main.zig`) + a **matched standalone C libbid arm** replaying the *identical* fixed operands with the same min-over-reps method (run `Rzg`) | operand/machine/method-clean, but **not same-process** (Zig cannot link libbid easily) — libbid runs in a separate binary; libbid's alignment-flatness keeps profile drift small. No idiomatic same-language Zig peer exists |
| Any port ↔ Python `Decimal` | standalone Python `timeit` harness | order-of-magnitude baseline only |
| Any port ↔ .NET `System.Decimal` (pre-port) | standalone C# **BenchmarkDotNet** harness (`~/dotnet/DecimalBench`) | order-of-magnitude baseline only; **superseded** by the in-process `decimal128-csharp` pair above now that a d128 .NET port exists. Compact bands only |

Kotlin and Go are benchmarked **cross-port against the C reference** on the same
categories to surface per-port slope, independent of the external alternatives (neither
has an idiomatic same-language decimal128 peer); **Zig** likewise has no same-language
peer but pairs against libbid via the matched standalone arm above. Swift, Rust, and C#
additionally have the same-language alternatives above (`Foundation.Decimal`,
`rust_decimal`, `System.Decimal`).

## 7. Measurement Methodology

- **Engine:** Google Benchmark (C arm); JMH (JVM arm). Per-category benchmark
  functions named by code **and profile**, e.g. `bm_add_OQ_pfin`, `bm_add_OQ_pmax`,
  `bm_mul_CP64_pfin`, `bm_div_XD_pgen`.
- **Ratios, not absolute times.** Report each category as a within-run ratio against
  the alternative implementation measured in the *same process* (`libbid`'s absolute times drift
  ~20% run-to-run on an unpinned laptop; same-process ratios are stable).
- **Units: ns/op.** The absolute metric is **nanoseconds per operation**, reported in
  both latency and throughput modes; the headline stays the dimensionless ratio. We do
  **not** use MFLOPS — decimal operations are not FLOPs, ns/op composes directly
  (pipeline cost = N × ns/op), and it expresses latency, which a throughput-only metric
  cannot.
- **Build:** `-O3 -march=native`, `VERIFY_ENABLED=0`, **`-flto` confirmed on the
  actual compile *and* link lines** (an LTO-stale bench build previously mismeasured
  the FE path as a loss). Equally, **confirm `-O3 -DNDEBUG` reaches the benchmark
  translation unit itself**, not just the library under test: on the x86 setup
  `CMAKE_BUILD_TYPE=Release` did *not* propagate its per-config CXX flags to the bench
  target, leaving `bench_main.cpp` (the timed loop) at `-O0` and the FetchContent'd
  Google Benchmark library in DEBUG. That fixed harness overhead is added to every arm
  and **compresses all same-process ratios (~30%)** — pass the flags explicitly in
  `CMAKE_C_FLAGS`/`CMAKE_CXX_FLAGS` (`BenchmarkResults.md` run `xc2`).
- **Architectures:** report both **arm64** and **x86 (i9-class, the 2019 headline
  target)**; they diverge (e.g. divide throughput/latency inverts on x86).
- **Throughput and latency** both, where they can diverge (divide on x86 is the
  known case: libbid wins throughput, we win latency).
- **Warmup / iteration counts** sufficient for JIT steady-state on the JVM arm.

## 8. Reporting Format

Results are recorded in a **generated store** under `decimal128-www/op-benchmark/`, and the
per-operation tables in **`BenchmarkResults.md` §1–§5** are rendered from it — this spec is the
contract, that file is the data.

**Store** (`op-benchmark/`):
- `results.<lang>.jsonl` — the fact table, one record per measured cell, upsert-by-key
  `(lang, impl, op, cat, profile, mode, arch)`. Each record carries a single number `ns`
  (ns/op) plus its `run` id. **`ns` is the only stored measurement** — `alt`, `alt ns`,
  `ratio`, and the `-` (peer-absent) cell are **derived at render** by pairing the port's
  `d128` cell against its alternative on `(op, cat, profile, arch)`.
- `runs.jsonl` — one provenance record per `run` id (machine, toolchain, flags, date, engine).
- `impls.json` — the implementation registry (display name, idiom-peer flag, mantissa width,
  language pinning) that drives peer selection.

**Row (as rendered):** `port · op · category · profile · arch · mode · ours(ns) · alt · alt(ns) · ratio · run · notes`.
- `category` is a §3 code (`SQ NQ MQ OQ FQ` / `CP WP XP` / `CD WD XD ET PT`, plus the add/sub
  financial `MIX` and the FMA `FN`/`FF`).
- `profile` ∈ `{P-fin, P-gen, P-max, FMA}` and is **mandatory** (§2.1) — `P-max` rows are the
  wide-path `stress` diagnostic, excluded from headline aggregates.
- `mode` records the methodology of the number: `thru` (swept 4096-input average, the headline),
  `thru*` (fixed-operand best-case diagnostic), `thru‡` / `ea` (JVM escape-forced alloc-inclusive
  headline / EA-elided 0-alloc lower bound), `tte`.
- `ratio = alt(ns) / ours(ns)` (> 1 ⇒ ours faster), computed only for a representable same-process pair.

**Rendering:** `gen_bench.py --emit <id>` prints one table; `gen_bench.py --splice BenchmarkResults.md`
rewrites every `<!-- BEGIN/END GENERATED <id> -->` block in place; `gen_bench.py --check BenchmarkResults.md`
diffs the store against what is currently in the file. **Never hand-edit inside a GENERATED marker** —
only the prose outside the markers is hand-written.

**Headline / marketing ratios use the realistic profile (P-fin / P-gen); P-max rows are labeled
`stress` and excluded from headline aggregates** but always reported. The category column makes every
shortfall localizable to a path. The legacy per-port file `decimal128-c` `bench/BENCHMARK_FINDINGS.md`
predates this taxonomy and feeds in until superseded (the Go port's `BENCHMARKS.md` was deleted
2026-07-03 — fully superseded by the Go rows in `BenchmarkResults.md` §1–§5).

## 9. Open Items

- **Magnitude-profile distributions (§2.1) are provisional.** The P-fin width
  (≤ 19 digits / 64-bit) is settled in principle; its *within-64-bit* digit/exponent
  distribution and the P-gen log-uniform spread are a starting point pending **real
  workload sampling** (financial ledgers, scientific datasets). Calibrate against
  actual operand traces before publishing headline ratios.
- sqrt and the IEEE 754 §9.2 recommended functions (exp/ln/pow/pown/rootn/compound) —
  their own iteration-count categories, deferred to a second matrix.
- FMA category cross-product (the §3.1 addend axis × §3.2 product axis) — confirm the
  generator coverage is tractable or sample it.
- The PT (power-of-ten divisor) fast path is a *candidate*, not implemented; measure
  the CD baseline first to size the potential win.
- JMH arm revival scope (which operators, steady-state cost) for the BigDecimal pair.
- Whether Python `Decimal` warrants a binding-based same-process harness rather than a
  standalone baseline.

---

*End of first draft.*
