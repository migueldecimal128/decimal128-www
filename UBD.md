# UBD: An Unpacked Binary Decimal Format for Fast Software Decoding of IEEE 754 decimal128

**Abstract.** UBD (Unpacked Binary Decimal) is a software-oriented in-memory format for IEEE 754 decimal128, designed for fast decoding on general-purpose CPUs. The two interchange encodings defined by IEEE 754 — Densely Packed Decimal (DPD) and Binary Integer Decimal (BID) — were designed primarily for hardware, which remains rare outside IBM processors. In software, both carry a decode cost: DPD requires substantial work to unpack its declet-based coefficient, while BID, though cheaper to unpack, still makes exponent recovery and operand classification non-trivial. Consequently, most software implementations unpack each operand into a wider, more memory-hungry working representation. UBD instead fits the full decimal128 coefficient range and NaN/infinity semantics into 128 bits while making the binary coefficient accessible via a single masking operation and the quantum exponent via a single arithmetic shift. All non-finite special values are stored with oversized coefficients, eliminating a separate operand check on the fast path. The result makes common-case operand checks and field extractions for addition, subtraction, and multiplication trivial. A Swift implementation using UBD format passes the Cowlishaw/IBM decTest, IBM FPgen fptest, and Intel libbid decimal128 test-vector suites. An earlier Kotlin Multiplatform implementation is being retrofitted to adopt UBD format; a core C implementation is in planned to extend decimal128 availability to other languages.

**Keywords:** decimal floating-point, IEEE 754, decimal128, DPD, BID, software arithmetic, in-memory encoding.

---

## 1. Introduction

Decimal floating-point arithmetic matters wherever results must match human, regulatory, or accounting expectations exactly — finance, tax, billing, and commerce — because binary floating-point cannot represent common decimal fractions such as 0.1 exactly [Goldberg 1991]. IEEE 754-2008 standardized decimal floating-point alongside its binary counterpart, and the 2019 revision carried these formats forward. The standard defines the `decimal128` format with a 34-digit coefficient and a wide exponent range, making it the natural choice for general-purpose decimal computation.

The standard defines two *interchange* encodings for storing decimal values: Densely Packed Decimal (DPD) and Binary Integer Decimal (BID). Both were designed primarily with hardware implementation in mind. In practice, that hardware is rare. IBM processors and Fujitsu SPARC64 support DPD decimal floating-point, but most general-purpose CPUs — including Intel's — do not. Intel has effectively argued, through its `libbid` implementation, that dedicated hardware is unnecessary and that decimal arithmetic can be carried out competitively in software [Cornea et al. 2009].

This creates a tension. The interchange encodings are optimized for the hardware that most platforms lack, yet the software that must stand in for that hardware pays a decode cost on every operation. This paper argues that software implementations benefit from a distinct *in-memory* encoding — one chosen for cheap decoding on commodity CPUs rather than for the density and regularity that suit silicon — and presents UBD (Unpacked Binary Decimal) as such an encoding for `decimal128`.

The contributions of this paper are:

1. **UBD**, a 128-bit in-memory encoding for `decimal128` that preserves the full coefficient range and NaN/infinity semantics while exposing the coefficient and exponent through single, cheap operations with a high degree of instruction-level parallelism (ILP).
2. A **special-value scheme** that stores all non-finite values with oversized coefficients, reducing the need for a dedicated operand-classification step on the arithmetic fast path.
3. **Conforming implementations** A completed Swift implementation and an in-process Kotlin Multiplatform implementation, validated against three independent industry test suites.

## 2. Background and Related Work

### 2.1 The decimal128 format

The decimal arithmetic standardized in IEEE 754 grew out of a long effort led by Mike Cowlishaw (IBM Fellow), whose General Decimal Arithmetic Specification (GDAS) provides the language- and encoding-independent definition on which the standard's decimal formats and arithmetic are based [Cowlishaw 2009]. IEEE 754 `decimal128` represents a value as a sign, a non-negative integer coefficient, and a base-10 *quantum* exponent, with a finite value equal to (−1)^sign × coefficient × 10^exponent. The coefficient holds up to 34 decimal digits. Unlike binary floating-point, decimal formats are not normalized: the same numeric value may have multiple representations differing in exponent (its *cohort*), and the chosen exponent — the *quantum* — is significant and must be preserved by arithmetic.

### 2.2 Densely Packed Decimal (DPD)

DPD encodes the coefficient as a sequence of *declets*: each group of three decimal digits is packed into 10 bits. This is dense and maps cleanly to decimal hardware, but in software each declet must first be expanded back into a digit-triple and then scaled by the appropriate power of ten before binary integer arithmetic can proceed. This unpacking represents substantial per-operand work.

### 2.3 Binary Integer Decimal (BID)

BID stores the coefficient as a binary integer, which is far friendlier to software because the value is already in a form CPUs compute on directly. BID is the basis of Intel's `libbid` [Cornea et al. 2009]. However, BID is less straightforward than it first appears: the encoding uses a combination field that, for large coefficients, shifts where the leading coefficient bits and the exponent live. Recovering the quantum exponent and classifying the operand (finite, infinity, NaN) therefore still require conditional logic that executes on the common path [Cornea et al. 2009].

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

#### 3.2.1 Coefficient field

`decimal128` defines 34 digits of precision. 113 bits is sufficient to hold integer values up through 10^34 − 1; in fact, 113 bits admits values up through 2^113 − 1. We use the term *oversized* to describe coefficient values in the range [10^34, 2^113 − 1], which lie beyond the valid 34-digit precision of finite `decimal128` values. The hi64 bits of 10^34 have the hex representation `0x1ED09BEAD87C0`.

#### 3.2.2 Sign bit field

All `decimal128` computation is sign-magnitude. Negative zero (−0) is a perfectly valid value. UBD therefore needs a dedicated sign bit, but its exact location does not matter much. There is no compelling reason to place it in the traditional most-significant-bit position; what matters is that it not interfere with another field. UBD places the sign bit at b113 — that is, b49 of hi64 — where it sits clear of both the qExp and the coefficient. The sign-bit field is otherwise unremarkable: it must exist for all finite and non-finite values, and so must be a dedicated bit.

#### 3.2.3 Quantum exponent field

In `decimal128` the quantum exponent *qExp* must represent values in the range [−6176, 6111]. Coupled with the 34-digit integer coefficient, this corresponds to a normal scientific exponent range of [−6143, 6144].

IEEE 754 binary floating-point — like many other floating-point representations — stores a *biased* exponent as a packed field. This requires an addition or subtraction during packing and unpacking, which is trivial in hardware but is an extra operation when decoding in software.

UBD instead packs qExp in unbiased two's-complement form in the top 14 bits of the value. The qExp can be decoded to an Int64 simply by performing a signed (arithmetic) shift right of hi64 by 50 bits; conversely, a validated Int64 qExp can be positioned for packing by shifting left 50 bits.

Observe that 14 bits lets the qExp field represent two's-complement values in the range [−8192, 8191], while the finite range we must represent is only [−6176, 6111]. Values outside the finite range are therefore available to denote non-finite special values — Infinity and the NaN variants.

The intended consequence of the layout is that decoding a finite operand reduces to two independent, dependency-free operations: a mask that yields the binary coefficient and an arithmetic shift that yields the signed quantum exponent. Neither requires a table lookup or a conditional branch.

### 3.3 Finite values

Any value with a qExp in [−6176, 6111] and a coefficient less than 10^34 is a finite, valid `decimal128` value. Because values are never *normalized*, there is no special treatment for *subnormal* values in the binary floating-point sense. This is a fundamental characteristic of decimal floating-point as formalized by Cowlishaw and has nothing to do with the UBD representation.

One useful consequence of the layout is that a UInt128 integer less than 10^34 has exactly the same binary representation in UBD: the coefficient *is* the integer value, and the qExp and sign are zero. A UInt64 (or a non-negative Int64) can therefore be converted to a UBD value simply by setting hi64 to zero. Negative two's-complement values are slightly more involved, since `decimal128` is sign-magnitude: to represent an Int64, the lo64 becomes the absolute value and the sign bit is placed at b49 of hi64.

### 3.4 Special values

The IEEE 754 specification defines values and behavior for Infinity and NaN, referring to these non-finite values collectively as *special values*. All values, including special values, carry a sign, so there are ±Infinity and ±NaN. NaN comes in a quiet form and a signaling form (sNaN), and may carry an integer payload of up to 33 decimal digits — one less than the 34 digits of precision. (Recovering the extra digit to reach a full 34 is part of the packing/unpacking complexity of the DPD/BID interchange formats.)

In UBD, every special value has *both*:

1. an oversized qExp above the normal range — greater than 6111; and
2. an oversized coefficient above the valid limit of 10^34 − 1 (34 nines of precision).

Every non-finite value thus offers two independent ways to determine whether one or more operands is finite. Within these constraints, specific encodings are chosen to make encoding and decoding cheap on general-purpose processors.

#### 3.4.1 Special values — coefficient field

The full `decimal128` coefficient range tops out at 34 decimal digits. UBD reserves coefficient values *above* this legal maximum to denote non-finite operands — infinities and quiet/signaling NaNs — with their sign and NaN payload carried in the surrounding bits.

The hi64 bits of 10^34 have the hex representation `0x1ED09BEAD87C0`, or with underscore separators `0x1_ED09_BEAD_87C0`. The separators make it easy to confirm the width: 1 + (3 × 16) = 49 bits. We use the term *coeffHi49* for the upper 49 bits of the 113-bit coefficient; note that coeffHi49 occupies the lower 49 bits of hi64 of the 128-bit value.

Any value greater than 10^34 − 1 could serve as the oversized threshold. This particular value begins with `0x1E`, so any value beginning with `0x1F` is clearly well into the oversized range. UBD therefore requires that all valid special values have coefficients beginning with `0x1F`. The coeffHi49 bits of Infinity and of NaN with payload zero (NaN0) are `0x1_F000_0000_0000`.

For NaN, all bits after the `0x1F` prefix — 113 − 5 = 108 bits — are available for payload. Representing 33 decimal digits, however, requires 110 bits, leaving us two bits short. To meet the full 33-digit payload requirement of the specification, those two bits are recovered from the qExp field, as described next.

#### 3.4.2 Special values — qExp

Two ranges of non-finite qExp values are available: above 6111 or below −6176. Each carries subtle complexity owing to two's-complement notation. Viewed as a 14-bit field, the top four bits of 6111 are `0b0101` (`0x5`). UBD tags all special values with a top nibble of `0b0111` (`0x7`, i.e. 7168 and above). After this prefix, the NaN bit distinguishes Infinity from NaN; if the NaN bit is set, the next bit (the signaling bit) distinguishes qNaN from sNaN. For a NaN, the low two bits of the qExp field hold two additional payload bits; combined with the 108 bits available in the coefficient, this gives 110 bits — sufficient to represent 10^33 − 1 (33 nines).

Within the 14-bit qExp field, special values are encoded as follows:

```
0b0111xx_000000_xx   non-finite
0b0111ns_000000_pp   n: NaN bit, s: signaling bit, pp: payloadHi2
0b011100_000000_00   Infinity (7168)
0b01111x_000000_pp   NaN
0b011110_000000_pp   qNaN
0b011111_000000_pp   sNaN (7936..7939)
```

All non-finite values fall in the range [7168, 7939], with substantial gaps. Decoding that range might appear complicated — and decoding complexity is precisely what UBD aims to avoid — but in pseudocode it is not bad at all. Assuming a 64-bit register width, `>>>` denoting an unsigned shift right, decimal integer constants, and `hi64` holding the upper 64 bits of the encoded value:

```
isFinite     { (hi64 >>> 60) != 7 }
isNonFinite  { (hi64 >>> 60) == 7 }
isInfinite   { (hi64 >>> 59) == 14 }
isNaN        { (hi64 >>> 59) == 15 }
isQNaN       { (hi64 >>> 58) == 30 }
isSNaN       { (hi64 >>> 58) == 31 }
```

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

### 3.5 Decoding cost compared

| Encoding | Coefficient recovery | Exponent recovery | Operand classification |
|---|---|---|---|
| DPD | Declet unpack (table / bit-twiddling) | Field extract + decode | Combination-field decode |
| BID | Conditional extract (combination field) | Conditional extract | Combination-field decode |
| **UBD** | **Single mask** | **Single arithmetic shift** | **Folded into range check** |

*Table 1. Qualitative per-operand decode work on a general-purpose CPU.*

Because every non-finite value carries a coefficient larger than any finite value can, the question "is this operand non-finite?" reduces to a single magnitude comparison against the finite maximum — and that comparison can often be folded into work the operation already performs, such as an overflow or range check, rather than standing as a separate classification step. The fast path for two finite operands thus contains no special-value branch at all; the slow path is entered only when a check the operation needs anyway reveals an out-of-range coefficient.

## 4. Arithmetic on UBD

UBD's value is realized on the common-case path of the basic operations. For addition, subtraction, and multiplication, the common case is two finite operands, and UBD makes the per-operand preamble trivial: mask out each coefficient, shift out each exponent, and proceed. There is no declet expansion, no combination-field case analysis, and no standalone class test. For a set of simple but common fast-path cases, the resulting code is small enough to be inlinable. The examples below are drawn from the existing implementations.

### 4.1 Addition

Addition proceeds as follows:

- the coefficient hi64 values are masked to obtain coeffHi49 values;
- the coeffHi49 values are added, producing sumHi49;
- the combined qExp-and-sign-bit value is extracted from each operand with a single shift; and
- if `x.qExpAndSignBit == y.qExpAndSignBit` and `(sumHi49 >> 48) == 0`, the fast path is taken; otherwise the slow path.

The fast path is taken only when the high bit of coeffHi49 is clear. A minority of valid 34-digit values route to the slow path, but they are handled correctly there. In effect, the check for non-finite operands is rolled into the overflow check.

#### 4.1.1 Addition fast path

The fast path applies only when the quanta are equal, the signs are equal, and sumHi49 fits in 48 bits. By design it does not compute the full 113-bit sum: on a 64-bit processor that would add instructions and latency ahead of the fast-path test. It need only complete the sum by adding the two coeffLo64 values, with any carry out of sumLo64 added into sumHi49; the result coefficient remains valid even in the worst-case carry. The qExp and signBit are taken from one of the input operands. No range check is needed, because the qExp came from a valid value and the resulting coefficient is valid.

Masking the operand coefficients and shifting the qExpAndSignBit values are completely independent across the two operands, exposing instruction-level parallelism. The instruction sequence is small enough that the fast path can reasonably be inlined.

Recall that every non-finite value has the high bit of coeffHi49 set. For +Infinity + +Infinity, for instance, the qExpAndSignBit values match, but sumHi49 exceeds 48 bits and so forces the slow path.

This fast-path case applies only to aligned values of the same sign — a situation that nonetheless arises frequently, as when summing a fixed-scale database column.

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

The branchless computation of the signed magnitude difference is a two's-complement technique independent of UBD, and is deferred to the companion paper.

### 4.3 Multiplication

The multiplication fast path selects finite operands meeting three criteria: the qExp sum is in range, the coefficient product fits, and the product occupies 112 bits or fewer.

```
if ((hi49Sum >> 48) == 0 &&
    prodQExp >= -6176 &&
    prodQExp <= 6111 &&
    (prodHi | (prodLo >> 112)) == 0)
{
    return Decimal128(sign: prodSignFlag, qExp: prodQExp, coeff: prodLo)
}
```

### 4.4 Rounding and re-encoding

UBD supports all finite values defined by IEEE 754-2008/2019. Rounding is a matter of computation and is independent of the representation. Once precision and quantum have been reduced into the finite range, packing is straightforward:

```
hi64 = (qExp << 50) | (signBit << 49) | coeffHi49
lo64 = coeffLo64
```

### 4.5 Conversion to and from interchange formats

The existing implementations support conversion to and from BID128 and DPD128, performed when data in a known `decimal128` interchange format is read or written. The cost of this encoding and decoding is comparable to the packing and unpacking any software implementation must perform, though the current Swift and Kotlin implementations are presumably less tuned than more mature libraries. For DPD128 in particular, declet decoding uses Cowlishaw's Boolean bit-manipulation algorithms [Cowlishaw 2002] rather than a lookup into a 2^10 = 1024-entry table.

## 5. Implementation

UBD is implemented in **Swift** and in **Kotlin Multiplatform**, giving native decimal128 support across the platforms those toolchains target.

The Swift value-type memory model is well suited to a numeric datatype. The implementation is written in Swift 6.3, makes heavy use of the `UInt128` type and of the overflow operators, and is 100% Swift with no external dependencies.

The **Kotlin Multiplatform** implementation uses a JVM-style heap-allocated-object model. _As of 1 Jun 2026, retro-fitting to UBD format is in-process_ Values are immutable, enforced by the Kotlin compiler through `val` fields. The core is 100% Kotlin, restricted to JVM-native signed types (no Kotlin pseudo-unsigned types); the only routine written in C, for Kotlin/Native, is `unsignedMulHi`, which returns the high 64 bits of a 64×64 unsigned multiply — available on the JVM but absent from the standard Kotlin Multiplatform library. The implementation is heap-friendly: each core operation, including all arithmetic, allocates at most one 32-byte object (a 12-byte header, 4 unused bytes, and 2 × 8 bytes of UBD).

The Swift and Kotlin implementations are kept as syntactically similar as practical, and are intended to converge further over time — a subject for a companion paper.

A portable **C core** is in progress, intended to serve as a single shared implementation that other languages can bind to. At this stage the C core is not meant to be used directly; rather, it is intended to be wrapped by language-specific bindings.

> *Placeholder.* Summarize the architecture shared across implementations, any platform-specific concerns (e.g., availability of 128-bit integer types, wide-multiply intrinsics), and how the C core is designed to be embedded.

### 5.1 Conformance

The Swift and Kotlin Multiplatform implementations pass three independent `decimal128` test-vector suites:

- the **Cowlishaw/IBM decTest** suite [Cowlishaw decTest],
- the **IBM FPgen `fptest`** suite [Aharoni et al. 2003], and
- the **Intel `libbid`** decimal128 vectors.

> *Placeholder.* Report coverage: which operations and corner cases (rounding modes, cohort/quantum preservation, NaN propagation, signaling-NaN behavior, subnormal handling) each suite exercises, and confirm full pass status with version identifiers for reproducibility.

## 6. Decode Cost

UBD's contribution is a complexity claim about decoding, not a wall-clock one. On the finite fast path, recovering an operand reduces to a single mask for the coefficient and a single arithmetic shift for the exponent, with operand classification subsumed by a range check the arithmetic already performs. This contrasts with the declet expansion DPD requires and the combination-field case analysis BID requires, as summarized in Table 1 (Section 3.5). These are structural properties of the encoding, independent of any particular CPU, compiler, or workload.

A quantitative performance study — microbenchmarks of per-operand decode and operation throughput against a BID baseline such as Intel `libbid` — belongs with the arithmetic kernels it measures and is the subject of a forthcoming companion paper.

## 7. Discussion

### 7.1 When UBD helps and when it does not

UBD optimizes the arithmetic fast path at the cost of conversions at interchange boundaries. It is therefore most valuable in workloads that perform many operations per value loaded or stored — typical of computation-heavy financial and analytical code — and less advantageous where values are touched once between encode and decode.

### 7.2 Limitations

UBD trades work at the interchange boundary for cheaper arithmetic, so it is not the right choice everywhere (see Section 7.1). Two design limitations are worth stating plainly. First, the "folded" special-value check is only free to the extent that an operation already performs a range check on its coefficient or product; where it does not, an explicit comparison is reintroduced, though it remains a single magnitude test rather than a combination-field decode. Second, UBD is an in-memory format: values must still be converted to a standard interchange encoding (DPD or BID) for storage and exchange, and the cost of that conversion is borne at I/O boundaries.

_Honestly, this cost is very low and not much more than the cost that would normally be associated with any operation. If you are reading from a file and summing values the cost might be slightly higher, but I'm not sure it would be measurable. If this were perceived to be a true limitation then I could take another look at optimizing the decoding._

### 7.3 Future work

A standard architecture for multi-platform support has been designed. See the accompanying whitepaper. 

## 8. Conclusion

UBD reframes the decimal128 storage question for the common case of software implementations of decimal floating-point. UBD maintains the density of the DPD and BID interchange formats while allowing the coded coefficient and qExp to be accessed with a single trivial operation each. Conforming Swift and Kotlin Multiplatform implementations pass the Cowlishaw/IBM decTest, IBM FPgen fptest, and Intel `libbid` test suites. A quantitative study of the arithmetic kernels built on this format is left to a companion paper.

## References

[Goldberg 1991] D. Goldberg, "What Every Computer Scientist Should Know About Floating-Point Arithmetic," *ACM Computing Surveys*, vol. 23, no. 1, pp. 5–48, March 1991. Available (edited reprint): https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html

[Cowlishaw 2009] M. F. Cowlishaw, *General Decimal Arithmetic Specification*, version 1.70, IBM, 25 March 2009. Available: https://speleotrove.com/decimal/decarith.pdf

[Cornea et al. 2009] M. Cornea, J. Harrison, C. Anderson, P. T. P. Tang, E. Schneider, and E. Gvozdev, "A Software Implementation of the IEEE 754R Decimal Floating-Point Arithmetic Using the Binary Encoding Format," *IEEE Transactions on Computers*, vol. 58, no. 2, pp. 148–162, February 2009. Available: https://www.cl.cam.ac.uk/~jrh13/papers/decimal.pdf

[IEEE 754-2019] IEEE, *IEEE Standard for Floating-Point Arithmetic*, IEEE Std 754-2019 (revision of IEEE Std 754-2008), Institute of Electrical and Electronics Engineers, July 2019. DOI: 10.1109/IEEESTD.2019.8766229. Available: https://ieeexplore.ieee.org/document/8766229

[Aharoni et al. 2003] M. Aharoni, S. Asaf, L. Fournier, A. Koifman, and R. Nagel, "FPgen — A Test Generation Framework for Datapath Floating-Point Verification," in *Proc. Eighth IEEE International High-Level Design Validation and Test Workshop (HLDVT)*, 2003, pp. 17–22. DOI: 10.1109/HLDVT.2003.1252469. Available: https://ieeexplore.ieee.org/document/1252469/. The associated IEEE 754R test suite (*fptest*) was distributed by IBM Research, Haifa.

[Cowlishaw 2002] M. F. Cowlishaw, "Densely Packed Decimal Encoding," *IEE Proceedings — Computers and Digital Techniques*, vol. 149, no. 3, pp. 102–104, May 2002. ISSN 1350-2387. A summary is available at https://speleotrove.com/decimal/DPDecimal.html

[Cowlishaw decTest] M. F. Cowlishaw, *General Decimal Arithmetic Testcases*, version 2.44, IBM, 24 March 2009. Available: https://speleotrove.com/decimal/dectest.pdf (testcase files at https://speleotrove.com/decimal/)

[Intel libbid] Intel Corporation, *Intel® Decimal Floating-Point Math Library*, a software implementation of the IEEE 754 decimal floating-point arithmetic specification. Available: https://www.intel.com/content/www/us/en/developer/articles/tool/intel-decimal-floating-point-math-library.html