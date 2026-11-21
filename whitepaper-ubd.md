---
layout: default
permalink: /whitepapers/ubd.html
title: "UBD: An Unpacked Binary Decimal Format for Fast Software Decoding of IEEE 754 decimal128 — Decimal128"
description: "UBD (Unpacked Binary Decimal) is a software-oriented in-memory format for IEEE 754 decimal128, designed for fast decoding on general-purpose CPUs."
heading: "UBD (An Unpacked Binary Decimal Format for Fast Software Decoding of IEEE 754 decimal128)"
---

<div class="whitepaper" markdown="1">

<div class="whitepaper-abstract" markdown="1">

**Abstract.** UBD (Unpacked Binary Decimal) is a software-oriented in-memory format for IEEE 754 decimal128, designed for fast decoding on general-purpose CPUs. The two interchange encodings defined by IEEE 754 — Densely Packed Decimal (DPD) and Binary Integer Decimal (BID) — were designed primarily for hardware implementation, which remains rare outside IBM processors. In software, both interchange formats carry a decode cost: DPD requires substantial work to unpack its declet-based coefficient, while BID, though cheaper to unpack, still makes exponent recovery and operand classification non-trivial. Consequently, most software implementations unpack each operand into a wider, more memory-hungry working representation. UBD instead fits the full decimal128 coefficient range and NaN/infinity semantics into 128 bits while making the binary coefficient accessible via a single masking operation and the quantum exponent via a single arithmetic shift. All non-finite special values are stored with oversized coefficients, eliminating a separate operand check on the fast path. The result makes common-case operand checks and field extractions for addition, subtraction, and multiplication trivial. Multiple implementations in different programming languages using UBD format pass the Cowlishaw/IBM `decTest`, IBM FPgen `fptest`, and Intel `libbid` decimal128 test-vector suites. In a fork of the Go toolchain that stores Go's built-in `decimal128` as UBD, small inline fast paths in front of kernel calls run seven application benchmarks within 1.2% of the BID-based original on average, with 42% of its code.

**Keywords:** decimal floating-point, IEEE 754, decimal128, DPD, BID, software arithmetic, in-memory encoding.

</div>

---

## 1. Introduction

Decimal floating-point arithmetic matters wherever results must match human, regulatory, or accounting expectations exactly — finance, tax, billing, and commerce — because binary floating-point cannot represent common decimal fractions such as 0.1 exactly [Goldberg 1991]. IEEE 754-2008 standardized decimal floating-point alongside its binary counterpart, and the 2019 revision carried these formats forward. The standard defines the `decimal128` format with a 34-digit coefficient and a wide exponent range, making it the natural choice for general-purpose decimal computation.

The standard defines two *interchange* encodings for storing decimal values: Densely Packed Decimal (DPD) and Binary Integer Decimal (BID). Both were designed primarily with hardware implementation in mind. In practice, that hardware is rare. IBM processors and Fujitsu SPARC64 support DPD decimal floating-point, but most general-purpose CPUs — including x86_64 and arm64 architectures — do not. Intel has argued, through its `libbid` implementation, that dedicated hardware is unnecessary and that decimal arithmetic can be carried out competitively in software [Cornea et al. 2009].

This creates a tension. The interchange encodings are optimized for the hardware that most platforms lack, yet the software that must stand in for that hardware pays a decode cost on every operation. This paper argues that software implementations benefit from a distinct *in-memory* encoding — one chosen for inexpensive decoding on commodity CPUs rather than for the density and regularity that suit silicon — and presents UBD (Unpacked Binary Decimal) as such an encoding for `decimal128`.

The contributions of this paper are:

1. **UBD**, a 128-bit 16-byte in-memory encoding for `decimal128` that preserves the full coefficient range and NaN/infinity semantics while exposing the coefficient and exponent through single, cheap operations with a high degree of instruction-level parallelism (ILP).
2. A **special-value scheme** that stores all non-finite values with oversized coefficients, reducing the need for a dedicated operand-classification step on the arithmetic fast path.
3. **Conforming implementations** in Swift, C, C#, Java, Kotlin Multiplatform (KMP), Rust, Go, and Zig, all of which demonstrate high performance. 
4. A **compiler integration**: Go's predeclared `decimal128` type, in a fork of the Go toolchain, stored as UBD, with its inline fast paths selectable by level and measured on whole applications against the BID-based original (Sections 5.1 and 6.3).

## 2. Background and Related Work

### 2.1 The decimal128 format

The decimal arithmetic standardized in IEEE 754 grew out of a long effort led by Mike Cowlishaw (IBM Fellow), whose General Decimal Arithmetic Specification (GDAS) provides the language- and encoding-independent definition on which the standard's decimal formats and arithmetic are based [Cowlishaw 2009]. IEEE 754 `decimal128` represents a value as a sign, a non-negative integer coefficient, and a base-10 *quantum* exponent, with a finite value equal to (−1)^sign × coefficient × 10^exponent. The coefficient holds up to 34 decimal digits. Unlike binary floating-point, decimal formats are not normalized: the same numeric value may have multiple representations differing in exponent (its *cohort*), and the chosen exponent — the *quantum* — is significant and must be preserved by arithmetic.

Normalized scientific notation has one digit to the left of the decimal point with the exponent scale applied accordingly. Decimal floating-point is modeled differently. It is an integer coefficient with the qExponent quantum exponent to the right of the integer coefficient.

| Scientific notation | Integer coefficient × 10^qExp |
|---|---|
| 1.23E4 | 123E2 |
| 1.00 | 100E-2 |

### 2.2 Densely Packed Decimal (DPD)

DPD encodes the coefficient as a sequence of *declets*: each group of three decimal digits is packed into 10 bits. This is dense and maps cleanly to decimal hardware, but in software each declet must first be expanded back into a digit-triple and then scaled by the appropriate power of ten before binary integer arithmetic can proceed. This unpacking represents substantial per-operand work.

### 2.3 Binary Integer Decimal (BID)

BID stores the coefficient as a binary integer, which is far friendlier to software because the value is already in a form that general-purpose CPUs compute on directly. BID is the basis of Intel's `libbid` [Cornea et al. 2009]. However, BID is less straightforward than it first appears: the encoding uses a combination field that, for large coefficients, shifts where the leading coefficient bits and the exponent live. Recovering the quantum exponent and classifying the operand (finite, infinity, NaN) therefore still require conditional logic that executes on the common path [Cornea et al. 2009].

### 2.4 Working representations in software libraries

Because both interchange encodings carry a decode cost, many software implementations do not operate on the interchange form directly. Instead they unpack each operand into a wider working representation — separating sign, exponent, and coefficient into independently addressable fields — which is convenient for computation but generally consumes more memory than the 16-byte interchange form. Intel's `libbid` is a notable exception: it operates directly on the BID encoding, exploiting the fact that a BID coefficient is already a binary integer. Even so, it still pays the combination-field and operand-classification costs noted in Section 2.3 on the common path. UBD is positioned precisely here: it retains the 16-byte size of the interchange form, like the packed approaches, while making the coefficient, exponent, and classification trivially accessible, unlike either.

## 3. The UBD Encoding

### 3.1 Design goals

UBD is built around four goals:

- **Size parity.** A UBD value occupies exactly 128 bits (16 bytes), matching the interchange form so that arrays of decimals cost no more memory (or bandwidth) than they would under DPD or BID. The 16-byte size also makes it possible to pass arguments and return values in registers on existing 64-bit processors.
- **Single-operation coefficient access.** The binary coefficient is recoverable with a single masking operation.
- **Single-operation exponent access.** The two's-complement quantum exponent is recoverable with a single arithmetic shift.
- **Branch-free special-value handling.** Non-finite values are arranged so that the fast path for addition, subtraction, and multiplication need not test for them explicitly.

### 3.2 Field layout

IEEE 754-2008/2019 define parameterized patterns for the representation of binary and decimal floating-point interchange formats at 32, 64, and 128 bits. UBD is designed to work only with `decimal128`: a precision of 34 decimal digits and a quantum exponent range of [−6176, 6111], corresponding to a *normal* scientific exponent range of [−6143, 6144] with an extended subnormal range down to 1E−6176.

The UBD layout is as follows:

| Field | Bits | Position |
|---|---|---|
| coefficient | 113 | b0..b112 |
| signBit | 1 | b113 |
| qExp | 14 | b114..b127 |

It is convenient to assume that UBD values are processed on a 64-bit machine. The terms *hi64* and *lo64* refer to the upper and lower 64 bits of a 128-bit value.

Implementations bind these halves to concretely named stored fields — `ubdLo64` and `ubdHi64`, declared lo-first — and that field list (names, types, declaration order) is the uniform cross-platform surface (PrimitiveLayer.md D27): a JVM `Decimal128` is two `long`s with these names, a C struct two `int64_t`. Both halves are carried as signed 64-bit integers across every implementation. The driver is the JVM, which offers no unsigned primitive integer types, so a signed 64-bit integer is the only type available in common to all ports; the signed (arithmetic) shift that decodes qExp (Section 3.2.3) then falls out naturally from that choice rather than motivating it. Constructors and whole-value accessors remain platform-local.

#### 3.2.1 Coefficient field

`decimal128` defines 34 digits of precision. 113 bits is sufficient to hold integer values up through 10^34 − 1; in fact, 113 bits admits values up through 2^113 − 1. We use the term *oversized* to describe coefficient values in the range [10^34, 2^113 − 1], which lie beyond the valid 34-digit precision of finite `decimal128` values. The hi64 bits of 10^34 have the hex representation `0x1ED09BEAD87C0`.

#### 3.2.2 Sign bit field

All `decimal128` computation is sign-magnitude. Negative zero (−0) is a perfectly valid value. UBD therefore needs a dedicated sign bit, but its exact location does not matter much. Since our representation is not encoding two's-complement integers directly, there is no compelling reason to place the value sign in the traditional most-significant-bit position. It is more important that the sign bit not interfere with its companion fields. UBD places the sign bit at b113 — that is, b49 of ubdHi64 — where it sits between the qExp and the coefficient. The sign-bit field is otherwise unremarkable.

#### 3.2.3 Quantum exponent field

In `decimal128` the quantum exponent *qExp* must represent values in the range [−6176, 6111]. Coupled with the 34-digit integer coefficient, this corresponds to a normal scientific exponent range of [−6143, 6144].

IEEE 754 binary floating-point — like many other floating-point representations — stores a *biased* exponent as a packed field. This requires an addition or subtraction during packing and unpacking, which is trivial in hardware but is an extra operation when decoding in software.

UBD instead packs qExp in unbiased two's-complement form in the top 14 bits of the value. Because the field carries no bias, decoding it to an Int64 is a single signed (arithmetic) shift right of ubdHi64 by 50 bits — there is nothing to subtract, and the two's-complement value sign-extends on its own:

```
qExp = ubdHi64 >> 50      // signed shift right: ubdHi64 is a signed 64-bit integer, so qExp sign-extends
```

Here `>>` denotes a signed shift, as distinct from the unsigned `>>>` used for the special-value tag tests in Section 3.4.2. Conversely, a validated Int64 qExp is positioned for packing by shifting left 50 bits.

Observe that 14 bits lets the qExp field represent two's-complement values in the range [−8192, 8191], while the finite range we must represent is only [−6176, 6111]. Values outside the finite range are therefore available to denote non-finite special values — Infinity and the NaN variants.

The intended consequence of the layout is that decoding a finite operand reduces to two independent, dependency-free operations: a mask that yields the binary coefficient and an arithmetic shift that yields the signed quantum exponent. Neither requires a table lookup or a conditional branch or the subtraction of an exponent bias. 

### 3.3 Finite values

Any value with a qExp in [−6176, 6111] and a coefficient less than 10^34 is a finite, valid `decimal128` value. Because values are never *normalized*, there is no special treatment for *subnormal* values in the binary floating-point sense. This is a fundamental characteristic of decimal floating-point as formalized by Cowlishaw and has nothing to do with the UBD representation.

One useful consequence of the UBD layout is that unsigned integers less than 10^34 have exactly the same binary representation in UBD: the coefficient *is* the integer value, and the qExp and sign are zero. A UInt64 (or a non-negative Int64) can therefore be converted to a UBD value simply by setting hi64 to zero. Negative two's-complement values are slightly more involved, since `decimal128` is sign-magnitude: to represent an Int64, ubdLo64 becomes the absolute value and the sign bit is placed at b49 of ubdHi64.

### 3.4 Special values

The IEEE 754 specification defines values and behavior for Infinity and NaN, referring to these non-finite values collectively as *special values*. All values, including special values, carry a sign, so there are ±Infinity and ±NaN. NaN comes in a quiet form and a signaling form (sNaN), and may carry an integer payload of up to 33 decimal digits — one less than the 34 digits of precision. (Recovering the extra digit to reach a full 34 is part of the packing/unpacking complexity of the DPD/BID interchange formats.)

In UBD, every special value has *both*:

1. an oversized qExp above the normal range — greater than 6111; and
2. an oversized coefficient above the valid limit of 10^34 − 1 (34 nines of precision).

Every non-finite value thus offers two independent ways to determine whether one or more operands is finite. Within these constraints, specific encodings are chosen to make encoding and decoding cheap on general-purpose processors.

#### 3.4.1 Special values — coefficient field

The full `decimal128` coefficient range tops out at 34 decimal digits. UBD reserves coefficient values *above* this legal maximum to denote non-finite operands — infinities and quiet/signaling NaNs — with their sign and NaN payload carried in the surrounding bits.

The hi64 bits of 10^34 have the hex representation `0x1ED09BEAD87C0`, or with underscore separators `0x1_ED09_BEAD_87C0`. The separators make it easy to confirm the width: 1 + (3 × 16) = 49 bits. We use the term *coeffHi49* for the upper 49 bits of the 113-bit coefficient; note that coeffHi49 occupies the lower 49 bits of ubdHi64. 

Any value greater than 10^34 − 1 could serve as the oversized threshold. This particular value begins with `0x1E`, so any value beginning with `0x1F` is clearly well into the oversized range. UBD therefore requires that all valid special values have coefficients beginning with `0x1F`. The coeffHi49 bits of Infinity and of NaN with payload zero (NaN0) are `0x1_F000_0000_0000`.

For NaN, all bits after the `0x1F` prefix — 113 − 5 = 108 bits — are available for payload. However, 108 bits only allows us to represent 32 decimal digits. Representing the 33 NaN payload decimal digits required by IEEE 754-2019 requires 110 bits, leaving us two bits short. To meet the full 33-digit payload requirement of the specification, those two bits are recovered from the qExp field, as described next.

#### 3.4.2 Special values — qExp

Two ranges of non-finite qExp values are available: above 6111 or below −6176. Each carries subtle complexity owing to two's-complement notation. Viewed as a 14-bit field, the top four bits of 6111 are `0b0101` (`0x5`). The UBD format tags all special values with a top nibble of `0b0111` (`0x7`, i.e. 7168 and above). After this prefix, the NaN bit distinguishes Infinity from NaN; if the NaN bit is set, the next bit (the signaling bit) distinguishes qNaN from sNaN. For a NaN, the low two bits of the qExp field hold two additional payload bits; combined with the 108 bits available in the coefficient, this gives 110 bits — sufficient to represent 10^33 − 1 (33 nines) of payload. 

Within the 14-bit qExp field, special values are encoded as follows:

```
0b0111xx_000000_xx   non-finite
0b0111ns_000000_pp   n: NaN bit, s: signaling bit, pp: payloadHi2
0b011100_000000_00   Infinity (7168)
0b01111x_000000_pp   NaN
0b011110_000000_pp   qNaN
0b011111_000000_pp   sNaN (7936..7939)
```

All non-finite values fall in the range [7168, 7939], with substantial gaps. Decoding that range might appear complicated — and decoding complexity is precisely what UBD aims to avoid — but in pseudocode one can see that decoding is straightforward. Assuming a 64-bit register width, `>>>` denoting an unsigned (logical) shift right, decimal integer constants, and `ubdHi64` holding the upper 64 bits of the encoded value:

```
isFinite     { (ubdHi64 >>> 60) != 7 }
isNonFinite  { (ubdHi64 >>> 60) == 7 }
isInfinite   { (ubdHi64 >>> 59) == 14 }
isNaN        { (ubdHi64 >>> 59) == 15 }
isQNaN       { (ubdHi64 >>> 58) == 30 }
isSNaN       { (ubdHi64 >>> 58) == 31 }
```

The shift amount selects how many of the leading qExp bits to examine, and each successive predicate simply keeps one more bit than the last. Shifting right by 60 isolates the 4-bit tag: `0b0111` (7) marks any non-finite value, exactly the `0x7` special-value prefix introduced above. Shifting by 59 retains one additional bit — the NaN bit — so `0b01110` (14) is Infinity and `0b01111` (15) is NaN. Shifting by 58 retains one more still — the signaling bit — so `0b011110` (30) is qNaN and `0b011111` (31) is sNaN. The constants 14, 15, 30, and 31 are therefore just the `0x7` tag extended by the class bits, not independent magic numbers.

This gives a full set of predicates, each computed with a single shift and a comparison against a small immediate constant carried in the instruction stream. Each predicate stands alone; none assumes a prior finiteness test. Moreover, this decoding happens only off the fast path; fast-path operations never reach it.

#### 3.4.3 NaN payload reconstruction

A 33-decimal-digit NaN payload requires 110 bits, while the coefficient field has 113 bits. Setting the top five bits of the coefficient to `0x1F` — the oversized baseline — leaves 108 bits. The remaining two high bits of the payload are stored in the low two bits of the qExp field. The encoding is:

```
payload110    110-bit payload
payloadLo64   low 64 bits of payload
payloadHi46   high 46 bits of payload
payloadHi2    payloadHi46 >>> 44
payloadMid44  payloadHi46 & BIT_MASK_44
```

Decoding reverses these steps.

With coefficient, exponent, and operand class each reachable by a single instruction, the layout is now ready to pay off where it matters — the common path of the basic operations, which the next section develops.

## 4. Arithmetic on UBD

UBD's value is realized on the common-case path of the basic operations. For addition, subtraction, and multiplication, the common case is two finite operands, and UBD makes the per-operand preamble trivial: mask out each coefficient, shift out each exponent, and proceed. There is no declet expansion, no combination-field case analysis, and no standalone class test. For a set of simple but common fast-path cases, the resulting code is small enough to be inlinable. The examples below are drawn from the existing implementations.

### 4.1 Addition

Addition proceeds as follows:

- the coefficient hi64 values are masked to obtain coeffHi49 values;
- the coeffHi49 values are added, producing sumHi49;
- the combined qExp-and-sign-bit value is extracted from each operand with a single shift; and
- if `x.qExpAndSignBit == y.qExpAndSignBit` and `(sumHi49 >>> 48) == 0`, the fast path is taken; otherwise the slow path.

The fast path is taken only when the high bit of coeffHi49 is clear. A minority of valid 34-digit values route to the slow path, but they are handled correctly there. In effect, the check for non-finite operands is rolled into the overflow check. On the fast path, sumHi49 is available and ready to accept the carry out of sumLo64. 

#### 4.1.1 Addition fast path

The fast path applies only when the quanta are equal, the signs are equal, and sumHi49 fits in 48 bits. By design it does not compute the full 113-bit sum: on a 64-bit processor that would add instructions and latency ahead of the fast-path test. It need only complete the sum by adding the two coeffLo64 values, with any carry out of sumLo64 added into sumHi49; the result coefficient remains valid even in the worst-case carry. The qExp and signBit are taken from one of the input operands. No range check is needed, because the qExp came from a valid value and the resulting coefficient is valid.

Masking the operand coefficients and shifting the qExpAndSignBit values are completely independent across the two operands, exposing instruction-level parallelism. The instruction sequence is small enough that the fast path can reasonably be inlined.

Recall that every non-finite value has the high bit of coeffHi49 set. For +Infinity + +Infinity, for instance, the qExpAndSignBit values match, but sumHi49 exceeds 48 bits and so forces the slow path.

This fast-path case applies only to aligned values of the same sign — a situation that nonetheless arises frequently, as when summing values from a fixed-scale database column.

#### 4.1.2 Addition slow path

The addition slow path catches:

- unequal qExp;
- unequal signBit;
- valid 34-digit values that occupy more than 48 bits of coeffHi49;
- genuine overflow values (113 or 114 bits); and
- non-finite special values.

The slow path falls back to the traditional methods of classifying operands and making decisions accordingly.

### 4.2 Subtraction

The subtraction fast path gates on equal qExp together with the same coefficient-magnitude bound used by addition. Because the special-value qExp tags lie outside the finite range, equal in-range qExp also guarantees that both operands are finite — so the same test that aligns the operands rules out the non-finite cases, with no separate classification step. Within the gate, the operation consults qExpAndSignBit to choose its path: when the operands' signs differ the magnitudes are summed (as in addition), and when they agree the magnitudes are subtracted. The subtract-magnitudes result cannot overflow; an exactly-zero difference is handed to the slow path, so that the result's quantum and sign of zero follow the IEEE rules.

The branchless computation of the signed magnitude difference is a two's-complement technique independent of UBD, and is deferred to a companion paper.

### 4.3 Multiplication

The multiplication fast path selects finite operands meeting three criteria: the qExp sum is in range, the coefficient product fits, and the product occupies 112 bits or fewer.

```
if ((sumHi49 >>> 48) == 0 &&
    prodQExp >= -6176 &&
    prodQExp <= 6111 &&
    (prodHi | (prodLo >>> 112)) == 0)
{
    return Decimal128(sign: prodSignFlag, qExp: prodQExp, coeff: prodLo)
}
```

### 4.4 Rounding and re-encoding

UBD supports all finite values defined by IEEE 754-2008/2019. Rounding is a matter of computation and is independent of the representation. Once precision and quantum have been reduced into the finite range, packing is straightforward:

```
ubdHi64 = (qExp << 50) | (signBit << 49) | coeffHi49
ubdLo64 = coeffLo64
```

### 4.5 Conversion to and from interchange formats

The existing implementations support conversion to and from BID128 and DPD128, performed when data in a known `decimal128` interchange format is read or written. The cost of this encoding and decoding is comparable to the packing and unpacking any software implementation must perform. For DPD128 in particular, current implementations perform declet decoding using Cowlishaw's Boolean bit-manipulation algorithms [Cowlishaw 2002] rather than a lookup into a 2^10 = 1024-entry table.

## 5. Implementation

As of Jul 2026, UBD decimal128 is implemented in 8 programming languages — **Swift**, **C**, **C#**, **Java**, **Kotlin Multiplatform**, **Rust**, **Go**, and **Zig** — giving native decimal128 support without going through a _wrapper_ to _drop down_ into C. The Python implementation, _does_ rely on a _C extension wrapper_ to call the existing C core in order to implement the Decimal128 type. 

The Swift value-type memory model is well suited to a numeric datatype. The implementation is written in Swift 6.3, makes heavy use of the `UInt128` type and of the overflow operators, and is 100% Swift with no external dependencies. Similarly, **C**, **C#**, Rust, and Go use the "value struct" memory model. By contrast, the **Java** and **Kotlin Multiplatform** implementations must use a JVM-style heap-allocated-object model. 

The Kotlin compiler enforces immutability through `val` fields. The core is 100% Kotlin, restricted to JVM-native signed types (no Kotlin pseudo-unsigned types). The implementation is heap-friendly: each core operation, including all arithmetic, allocates at most one 32-byte object (a 12-byte header, 4 unused bytes, and 2 × 8 bytes of UBD).

All implementations are kept as syntactically similar as practical. This is accomplished (in part) by restricting language constructs to a shared core. An effort is made to keep base filenames the same across all ports. These cross-platform goals and constraints are the subject of a companion paper. 

### 5.1 UBD as a compiler built-in: the Go fork

A proposal to add decimal floating-point types to Go [Go #19787] has a prototype toolchain by Marcelo Cantos [Cantos decimal] in which `decimal64` and `decimal128` are predeclared types with operators, implemented on BID: a `decimal128` is stored as its BID encoding with the high word XORed with the encoding of +0E+0, so that all bits clear is the zero value (*XOR-BID*). Its compiler expands each operator into integer fast paths inline, with calls into a software kernel for the rest.

The `ubd128` fork of that toolchain [go-decimal-ubd] stores `decimal128` as UBD instead, unchanged in layout from Section 3, so that all bits clear is +0E+0 with no mask. The runtime, the conversions, formatting and parsing, and the kernel all work on UBD directly; BID appears only at the interchange boundary (reading and writing BID bits) and in a compile-time zero test of constants. The kernel is the prototype's BID kernel with its decoding and packing replaced by UBD's and its arithmetic unchanged. On amd64 and arm64, each operator compiles to a direct call into a kernel entry that takes the two 64-bit words of each operand in the registers they already occupy, low word first, so a call site moves nothing into place, optionally preceded by an inline fast path. (`decimal64` remains XOR-BID.)

How much is inlined is chosen by the compiler flag `-d=ubdlevel`:

| Level | Inline code at each call site |
|---|---|
| 1 | none: every operation is its kernel call, the smallest code |
| **2** (default) | the narrowed fast paths below, in front of the kernel calls |
| 3 | the large inline paths the prototype's compiler had for BID, moved to UBD's bit positions, in front of the same kernel calls |

The level-2 paths narrow the paths of Section 4 to operands whose coefficients fit one 64-bit word. One test then serves addition, subtraction, and comparison:

```
(xHi64 ^ yHi64) | (xHi64 << 15) == 0
```

The high words are equal, so the operands share qExp and sign, and x's high word holds no coefficient bits, so both coefficients are below 2^64. Because every special value carries the `0x1F` coefficient prefix in its high word (Section 3.4.1), the same test excludes them: the special-value check is folded into the operand test, as in Section 4.1, now for comparisons as well.

- **Addition** of operands of one qExp and one sign: the low words are added and the carry is added into the high word, an exact sum below 2^65. qExp and sign ride along in x's high word.
- **Subtraction** of operands of one qExp and one sign: one subtraction of the low words; a borrow means |y| > |x|, and the difference is negated and the sign flipped; an exact zero is +0.
- **Multiplication:** both coefficients below 2^56 and the qExp sum in range; the 64 × 64-bit product is then below 2^112, exact at the preferred exponent.
- **Comparison with zero:** `(hi << 15) | lo == 0` for equality; the ordered comparisons place the sign above the coefficient in one word and test it as a signed integer. There is no kernel call at all.
- **Comparison of two values:** the low words compared, XORed with a sign mask for the ordered comparisons.

Every other operand pair takes the kernel call. Table 2 shows the code each operator costs at a call site.

| Operator | XOR-BID | UBD level 1 | **UBD level 2** | UBD level 3 |
|---|--:|--:|--:|--:|
| `x + y` | 169 / 119 | 2 / 3 | **12 / 8** | 101 / 74 |
| `x - y` | 179 / 126 | 2 / 3 | **25 / 14** | 102 / 76 |
| `x * y` | 84 / 65 | 2 / 3 | **28 / 20** | 38 / 32 |
| `x == y` | 169 / 131 | 2 / 3 | **12 / 7** | 69 / 58 |
| `x < y` | 201 / 152 | 2 / 3 | **17 / 10** | 86 / 68 |
| `x == 0` | 30 / 31 | 4 / 5 | **5 / 4** | 5 / 4 |
| `x > 0` | 41 / 40 | 4 / 5 | **13 / 10** | 14 / 11 |

*Table 2. Instructions per call site, amd64 / arm64: the inline fast paths and the call setup, without the enclosing function's frame.*

## 6. Evaluation

UBD is evaluated on two axes: *conformance* — that implementations built on the format compute `decimal128` results exactly as the standard requires — and *decode cost* — the per-operand work the format demands of a general-purpose CPU. The first is measured against independent test-vector suites; the second is a structural, CPU-independent complexity argument.

### 6.1 Conformance

All 8 implementations pass three independent `decimal128` test-vector suites:

- the **Cowlishaw/IBM `decTest`** suite [Cowlishaw decTest],
- the **IBM FPgen `fptest`** suite [Aharoni et al. 2003], and
- the **Intel `libbid`** decimal128 vectors.

Each of these contains one or more text files with multiple test vectors per file. The formats differ, but fundamentally they are conveying the same information:
`operation rounding operand1 operand2 => result flags`

_Performing the given **operation** with the specified **rounding** on these **operands** should generate this expected **result** with these **flags**._


We built a general test harness named **Rosetta** to dynamically translate from each of these individual (ancient) scripts to a test vector instance. See the 'Rosetta' companion paper for additional detail.

┌─────────┬───────────────┬─────────┐
│ Corpus  │ Passed (d128) │ Skipped │
├─────────┼───────────────┼─────────┤
│ fptest  │        24,602 │       0 │
├─────────┼───────────────┼─────────┤
│ intel   │        14,283 │      43 │
├─────────┼───────────────┼─────────┤
│ dectest │        12,388 │     160 │
├─────────┼───────────────┼─────────┤
│ Total   │        51,273 │     203 │
└─────────┴───────────────┴─────────┘

Together they comprise 51,273 decimal128 test cases, both hand selected and algorithmically generated by the respective IBM and Intel teams, that collectively stress-test all of the operations under different rounding conditions. 

Note that there are some cases that are skipped. One category of skipped cases represents changes to the behavior of min/max between IEEE 754 2008 and 2019. Another example is select cases where the expected flags are incorrect. 

### 6.2 Decode cost

UBD's second claim concerns decode *cost*, and it is a complexity claim rather than a wall-clock one. On the finite fast path, recovering an operand reduces to a single mask for the coefficient and a single arithmetic shift for the exponent, with operand classification subsumed by a range check the arithmetic already performs. This contrasts with the declet expansion DPD requires and the combination-field case analysis BID requires. Table 1 summarizes the per-operand decode work each encoding demands on a general-purpose CPU.

| Encoding | Coefficient recovery | Exponent recovery | Operand classification |
|---|---|---|---|
| DPD | Declet unpack (table / bit-twiddling) | Field extract + decode | Combination-field decode |
| BID | Conditional extract (combination field) | Conditional extract | Combination-field decode |
| **UBD** | **Single mask** | **Single arithmetic shift** | **Folded into range check** |

*Table 1. Qualitative per-operand decode work on a general-purpose CPU.*

Because every non-finite value carries a coefficient larger than any finite value can, the question "is this operand non-finite?" reduces to a single magnitude comparison against the finite maximum — and that comparison can often be folded into work the operation already performs, such as an overflow or range check, rather than standing as a separate classification step. The fast path for two finite operands thus contains no special-value branch at all; the slow path is entered only when a check the operation needs anyway reveals an out-of-range coefficient. These are structural properties of the encoding, independent of any particular CPU, compiler, or workload. 

Benchmarks showing a performance breakdown of add/sub/mul/div with different operand shapes are run across the different implementations. See the companion BenchmarkMatrix and BenchmarkResults documents. 

### 6.3 Application benchmarks: inline code against speed

The Go toolchains of Section 5.1 are measured on whole applications with the go-decimal128-app-benchmark suite [go-decimal128-app-benchmark]: Go translations of the UW-Madison decimal floating-point application benchmarks [Wang et al. 2007; Anderson et al. 2009] (euro conversion, risk management, three tax forms, banking) and of Cowlishaw's telco benchmark [Cowlishaw telco]. Each program's output is checked byte for byte against the reference output on every run. The baseline is the XOR-BID toolchain the fork started from; UBD is measured at its three levels. All four builds were run interleaved on an Apple M3 Pro (arm64), with every function aligned to 64 bytes so that code placement does not differ between builds (November 2026).

Table 3 gives the time of each program's own timed loop, in ns per record; lower is better.

| App | XOR-BID, ns | UBD level 1, ns | **UBD level 2, ns** | UBD level 3, ns |
|---|--:|--:|--:|--:|
| euro | 881.2 | 872.1 (−1.0%) | **865.6 (−1.8%)** | 857.3 (−2.7%) |
| risk | 5,777.1 | 7,693.8 (+33.2%) | **6,422.9 (+11.2%)** | 5,725.0 (−0.9%) |
| tax fed | 2,347.9 | 2,851.2 (+21.4%) | **2,409.7 (+2.6%)** | 2,212.9 (−5.7%) |
| tax ca | 500.2 | 575.5 (+15.1%) | **509.5 (+1.9%)** | 449.7 (−10.1%) |
| tax nc | 805.0 | 822.4 (+2.2%) | **758.2 (−5.8%)** | 708.9 (−11.9%) |
| banking | 648.8 | 698.9 (+7.7%) | **661.1 (+1.9%)** | 636.0 (−2.0%) |
| telco | 32.1 | 43.8 (+36.3%) | **31.9 (−0.7%)** | 28.7 (−10.7%) |
| **time vs XOR-BID, geometric mean (%)** | — | **+15.6%** | **+1.2%** | **−6.4%** |

*Table 3. Compute time, ns per record, with the change against XOR-BID.*

Table 4 gives the size of each program's own machine code, in KB: its main package and the adapter through which it reaches the decimal type, where the operators are compiled and inlined. The kernel, runtime, and standard library are shared by every program and not counted.

| App | XOR-BID, KB | UBD level 1, KB | **UBD level 2, KB** | UBD level 3, KB |
|---|--:|--:|--:|--:|
| euro | 11.0 | 7.8 | **8.4** | 9.5 |
| risk | 25.2 | 10.1 | **12.1** | 19.5 |
| tax fed | 154.2 | 30.7 | **44.9** | 101.9 |
| tax ca | 40.8 | 12.1 | **15.5** | 29.2 |
| tax nc | 64.4 | 14.6 | **20.9** | 44.3 |
| banking | 131.7 | 65.2 | **74.4** | 105.4 |
| telco | 9.5 | 5.9 | **6.5** | 9.1 |
| **total of the seven (KB)** | **436.7 KB** | **146.4 KB (−66%)** | **182.7 KB (−58%)** | **318.9 KB (−27%)** |

*Table 4. Code size, KB per program, with the change in total against XOR-BID.*

The levels trace a curve of code against speed. Level 2 adds 36 KB (+25%) to level 1 and is 12.5% faster on the geometric mean; level 3 adds a further 136 KB (+75%) for a further 7.5%. Level 2 is at most 2.6% slower than XOR-BID on six of the seven programs, and faster on three of them (euro, nc, telco), with 42% of its code; level 3 is faster than XOR-BID on all seven with 73% of its code. The remaining gap at level 2 is risk (+11.2%): about two in five of its additions and subtractions have operands of different exponents or of opposite signs for the operator, money-sized values that nonetheless take the kernel call. Two attempts to close it without growing the inline code did not succeed: computing the kernel's word-path addition without branches (the branches it removed were predicted better in risk than in random data) and an inline path for either sign (its code cost as much time as the calls it saved).

One kernel change did close a gap without any inline code: telco's quantize to cents spent its time on a mispredicted branch deciding whether the remainder passed half, not on the division; computing that decision without a branch took the kernel's word path from 6.5 to 4.3 ns and telco from 36.0 to 31.8 ns per record, level with XOR-BID.

## 7. Discussion

### 7.1 When UBD helps and when it does not

UBD optimizes the arithmetic fast path at the cost of conversions at interchange boundaries. It is therefore most valuable in workloads that perform many operations per value loaded or stored — typical of computation-heavy financial and analytical code — and less advantageous where values are touched once between encode and decode.

### 7.2 Limitations

UBD trades work at the interchange boundary for cheaper arithmetic, so it is not the right choice everywhere (see Section 7.1). Two design limitations are worth stating plainly. First, the "folded" special-value check is only free to the extent that an operation already performs a range check on its coefficient or product; where it does not, an explicit comparison is reintroduced, though it remains a single magnitude test rather than a combination-field decode. Second, UBD is an in-memory format: values must still be converted to a standard interchange encoding (DPD or BID) for storage and exchange, and the cost of that conversion is borne at I/O boundaries.

This decode cost is not peculiar to UBD. Converting an interchange encoding into a form suitable for computation is work that every software implementation must perform, and UBD's conversion is no more expensive than the unpacking DPD or BID would otherwise require. The only case in which UBD can lose is a workload that touches each value exactly once and whose inputs already arrive in the target interchange form — summing a column that is already BID-encoded, for example. There the total cost is a two-stage translate-then-add, where a BID-native library can operate closer to in place. The extra stage is precisely the decode UBD normally amortizes across many operations, now standing alone in front of a single one.

This conversion cost issue only applies to binary data that is already in DPD/BID format. Parsing of text representations converts directly to UBD. 

### 7.3 Future work

A standard architecture for multi-platform support — the shared-core discipline that keeps the 8 implementations syntactically aligned — has been designed and is described in an accompanying whitepaper. A quantitative companion study characterizes the arithmetic kernels built on UBD across operand shapes and implementations (Section 6.2).

In the Go fork (Sections 5.1 and 6.3), the remaining work is the additions the level-2 paths send to the kernel, operands of different exponents or of opposite signs, which keep risk 11% behind XOR-BID, without giving up the small call sites that make level 2 worth having.


## 8. Conclusion

UBD reframes the decimal128 storage question for the common case of software implementations of decimal floating-point. UBD maintains the density of the DPD and BID interchange formats while allowing the coded coefficient and qExp to be accessed with a single trivial operation each. Conforming implementations in Swift, C, C#, Java, Kotlin Multiplatform, Rust, Go, and Zig pass the Cowlishaw/IBM `decTest`, IBM FPgen `fptest`, and Intel `libbid` test suites. A quantitative study of the arithmetic kernels built on this format is left to a companion paper. As the storage of Go's built-in `decimal128` in a fork of the Go toolchain, UBD lets small inline fast paths — one test for exponent, sign, coefficient size, and special values — keep seven application benchmarks within 1.2% of the BID-based original on average with 42% of its code, and larger ones run them 6.4% faster with 73% of it.

## References

[Goldberg 1991] D. Goldberg, "What Every Computer Scientist Should Know About Floating-Point Arithmetic," *ACM Computing Surveys*, vol. 23, no. 1, pp. 5–48, March 1991. Available (edited reprint): https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html

[Cowlishaw 2009] M. F. Cowlishaw, *General Decimal Arithmetic Specification*, version 1.70, IBM, 25 March 2009. Available: https://speleotrove.com/decimal/decarith.pdf

[Cornea et al. 2009] M. Cornea, J. Harrison, C. Anderson, P. T. P. Tang, E. Schneider, and E. Gvozdev, "A Software Implementation of the IEEE 754R Decimal Floating-Point Arithmetic Using the Binary Encoding Format," *IEEE Transactions on Computers*, vol. 58, no. 2, pp. 148–162, February 2009. Available: https://www.cl.cam.ac.uk/~jrh13/papers/decimal.pdf

[IEEE 754-2019] IEEE, *IEEE Standard for Floating-Point Arithmetic*, IEEE Std 754-2019 (revision of IEEE Std 754-2008), Institute of Electrical and Electronics Engineers, July 2019. DOI: 10.1109/IEEESTD.2019.8766229. Available: https://ieeexplore.ieee.org/document/8766229

[Aharoni et al. 2003] M. Aharoni, S. Asaf, L. Fournier, A. Koifman, and R. Nagel, "FPgen — A Test Generation Framework for Datapath Floating-Point Verification," in *Proc. Eighth IEEE International High-Level Design Validation and Test Workshop (HLDVT)*, 2003, pp. 17–22. DOI: 10.1109/HLDVT.2003.1252469. Available: https://ieeexplore.ieee.org/document/1252469/. The associated IEEE 754R test suite (*fptest*) was distributed by IBM Research, Haifa.

[Go #19787] "proposal: spec: add decimal float types (IEEE 754-2008)," Go issue 19787. Available: https://go.dev/issue/19787

[Cantos decimal] M. Cantos, Go toolchain with predeclared decimal types, branch `decimal` of https://github.com/marcelocantos/go, commit `5032fd77`; proposal and toolchain lock at https://github.com/marcelocantos/go-decimal-proposal

[go-decimal-ubd] The `ubd128` fork of [Cantos decimal], storing `decimal128` as UBD. Available: https://github.com/migueldecimal128/go-decimal-ubd/tree/ubd128 (measured at commit `45ff73c327`)

[Wang et al. 2007] L.-K. Wang, C. Tsen, M. J. Schulte, and D. Jhalani, "Benchmarks and Performance Analysis of Decimal Floating-Point Applications," in *Proc. 25th IEEE International Conference on Computer Design (ICCD)*, October 2007, pp. 164–170.

[Anderson et al. 2009] M. J. Anderson, C. Tsen, L.-K. Wang, K. Compton, and M. J. Schulte, "Performance Analysis of Decimal Floating-Point Libraries and Its Impact on Decimal Hardware and Software Solutions," in *Proc. 27th IEEE International Conference on Computer Design (ICCD)*, October 2009, pp. 465–471.

[go-decimal128-app-benchmark] Go application benchmarks for decimal128 libraries: the UW-Madison decimal floating-point application benchmarks (v1.0) [Wang et al. 2007; Anderson et al. 2009] and Cowlishaw's telco benchmark, with byte-exact output gates and a runner. Available: https://github.com/migueldecimal128/go-decimal128-app-benchmark

[Cowlishaw telco] M. F. Cowlishaw, "The 'telco' benchmark." Available: https://speleotrove.com/decimal/telco.html

[Cowlishaw 2002] M. F. Cowlishaw, "Densely Packed Decimal Encoding," *IEEE Proceedings — Computers and Digital Techniques*, vol. 149, no. 3, pp. 102–104, May 2002. ISSN 1350-2387. A summary is available at https://speleotrove.com/decimal/DPDecimal.html

</div>

[Cowlishaw decTest] M. F. Cowlishaw, *General Decimal Arithmetic Testcases*, version 2.44, IBM, 24 March 2009. Available: https://speleotrove.com/decimal/dectest.pdf (testcase files at https://speleotrove.com/decimal/)

[Intel libbid] Intel Corporation, *Intel® Decimal Floating-Point Math Library*, a software implementation of the IEEE 754 decimal floating-point arithmetic specification. Available: https://www.intel.com/content/www/us/en/developer/articles/tool/intel-decimal-floating-point-math-library.html