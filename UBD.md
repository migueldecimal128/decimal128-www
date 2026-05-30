# UBD: An Unpacked Binary Decimal Encoding for Fast Software Decoding of IEEE 754 decimal128

**Abstract.** UBD (Unpacked Binary Decimal) is a software-oriented in-memory encoding for IEEE 754 decimal128, designed for fast decoding on general-purpose CPUs. The two interchange encodings defined by IEEE 754 — Densely Packed Decimal (DPD) and Binary Integer Decimal (BID) — were designed primarily for hardware, which remains rare outside IBM processors. In software, both carry a decode cost: DPD requires substantial work to unpack its declet-based coefficient, while BID, though cheaper to unpack, still makes exponent recovery and operand classification non-trivial. Consequently, most software implementations unpack each operand into a wider, more memory-hungry working representation. UBD128 instead fits the full decimal128 coefficient range and NaN/infinity semantics into 128 bits while making the binary coefficient accessible via a single masking operation and the quantum exponent via a single arithmetic shift. All non-finite special values are stored with oversized coefficients, eliminating a separate operand check on the fast path. The result makes common-case operand checks and field extractions for addition, subtraction, and multiplication trivial. Implementations in Swift and Kotlin Multiplatform pass the Cowlishaw/IBM decTest, IBM FPtest, and Intel libbid decimal128 test-vector suites; a core C implementation is in progress to extend UBD to other languages.

**Keywords:** decimal floating-point, IEEE 754, decimal128, DPD, BID, software arithmetic, in-memory encoding.

---

## 1. Introduction

Decimal floating-point arithmetic matters wherever results must match human, regulatory, or accounting expectations exactly — finance, tax, billing, and commerce — because binary floating-point cannot represent common decimal fractions such as 0.1 exactly [Goldberg 1991]. IEEE 754-2008 standardized decimal floating-point alongside its binary counterpart, and the 2019 revision carried these formats forward. The standard defines the `decimal128` format with a 34-digit coefficient and a wide exponent range, making it the natural choice for general-purpose decimal computation.

The standard defines two *interchange* encodings for storing decimal values: Densely Packed Decimal (DPD) and Binary Integer Decimal (BID). Both were designed primarily with hardware implementation in mind. In practice, that hardware is rare. IBM processors and Fujitsu Sparc64 support DPD decimal floating-point, but most general-purpose CPUs — including Intel's — do not. Intel has effectively argued, through its `libbid` implementation, that dedicated hardware is unnecessary and that decimal arithmetic can be carried out competitively in software [Cornea et al. 2009].

This creates a tension. The interchange encodings are optimized for the hardware that most platforms lack, yet the software that must stand in for that hardware pays a decode cost on every operation. This paper argues that software implementations benefit from a distinct *in-memory* encoding — one chosen for cheap decoding on commodity CPUs rather than for the density and regularity that suit silicon — and presents UBD (Unpacked Binary Decimal) as such an encoding for `decimal128`.

The contributions of this paper are:

1. **UBD**, a 128-bit in-memory encoding for `decimal128` that preserves the full coefficient range and NaN/infinity semantics while exposing the coefficient and exponent through single, cheap operations that can often run in parallel integer ALUs
2. A **special-value scheme** that stores all non-finite values with oversized coefficients, removing the need for a dedicated operand-classification step on the arithmetic fast path.
3. **Conforming implementations** in Swift and Kotlin Multiplatform validated against three independent industry test suites, and a design for a portable C core.

## 2. Background and Related Work

### 2.1 The decimal128 format

The decimal arithmetic standardized in IEEE 754 grew out of a long effort led by Mike Cowlishaw (IBM Fellow), whose General Decimal Arithmetic Specification (GDAS) provides the language- and encoding-independent definition on which the standard's decimal formats and arithmetic are based [Cowlishaw 2009]. IEEE 754 `decimal128` represents a value as a sign, a non-negative integer coefficient, and a base-10 *quantum* exponent, with a finite value equal to (−1)^sign × coefficient × 10^exponent. The coefficient holds up to 34 decimal digits. Unlike binary floating-point, decimal formats are not normalized: the same numeric value may have multiple representations differing in exponent (its *cohort*), and the chosen exponent — the *quantum* — is significant and must be preserved by arithmetic.

### 2.2 Densely Packed Decimal (DPD)

DPD encodes the coefficient as a sequence of *declets*: each group of three decimal digits is packed into 10 bits. This is dense and maps cleanly to decimal hardware, but in software each declet must be expanded back into digit-triples, and then scaled by powers of 10 before binary integer arithmetic can proceed. This unpacking represents substantual per-operand work. 

### 2.3 Binary Integer Decimal (BID)

BID stores the coefficient as a binary integer, which is far friendlier to software because the value is already in a form CPUs compute on directly. BID is the basis of Intel's `libbid` [Cornea et al. 2009]. However, BID is less straightforward than it first appears: the encoding uses a combination field that, for large coefficients, shifts where the leading coefficient bits and the exponent live. Recovering the quantum exponent and classifying the operand (finite, infinity, NaN) therefore still require conditional logic that executes on the common path [Cornea et al. 2009].

### 2.4 Working representations in software libraries

Because both interchange encodings carry a decode cost, most software implementations do not operate on the interchange form directly. Instead they unpack each operand into a wider working representation — separating sign, exponent, and coefficient into independently addressable fields — which is convenient for computation but generally consumes more memory than the 16-byte interchange form. UBD is positioned precisely here: it retains the 16-byte size of the interchange form while delivering the decode-friendliness of a working representation.

## 3. The UBD Encoding

### 3.1 Design goals

UBD is built around four goals:

- **Size parity.** A UBD value occupies exactly 128 bits (16 bytes), matching the interchange form so that arrays and buffers of decimals cost no more memory than they would under DPD or BID. The 16-byte size also makes it possible to pass arguments and return values in registers on existing 64-bit processors. 
- **Single-operation coefficient access.** The binary coefficient is recoverable with a single masking operation. 
- **Single-operation exponent access.** The two's-complement quantum exponent is recoverable with a single arithmetic shift.
- **Branch-free special-value handling.** Non-finite values are arranged so that the fast path need not test for them explicitly.

### 3.2 Field layout

IEEE 754-2008/2019 define parameterized patterns for representation of binary/decimal floating point interchange formats for 32, 64, and 128 bits. The UBD format is designed to work only with `decimal128` precision of 34 decimal digits and quantum exponent range of [-6176..6111], corresponding to a _normal_ scientific exponent range of [-6143..6144] with an extended subnormal range down to 1E-6176. 

UBD layout is as follows:
coefficient - 113 bits - b0..b112
sign - 1 bit - b113
qExp - 14 bits - b114..b127

It will be convenient to assume that UBD values are being processed on a 64-bit machine. The terms _hi64_ and _lo64_ refer to the upper and lower 64 bits of a 128 bit value. 

#### 3.2.1 Coefficient field
`decimal128` defines 34 digits of precision. 113 bits is sufficient to hold integer values up thru 10^34-1. The allocation of 113 bits allows values up thru 2^113 - 1. We use the term _oversized_ to describe coefficient values in the range [10^34, 2^113-1] that are beyond the valid 34-digit precision of finite `decimal12` values. 
The hex representation of the hi64 bits of 10^34 is
0x1ED09BEAD87C0 

#### 3.2.2 Sign bit field
All `decimal128` computation is sign-magnitude. Negative zero -0 is a perfectly valid value. We need a dedicated sign bit, but the exact location of the sign bit doesn't really matter that much. There is no compelling reason to put the UBD sign bit in the traditional MSB most significant bit position. It is more important that we not put it someplace that interferes with something else. UBD format places the sign bit at bit position b113, or b49 of the hi64, where it doesn't interfere with either the qExp or the coefficient. The sign bit field is relatively uninteresting ... it must exist for all finite and non-finite values and therefore must be a dedicated bit. 

#### 3.2.3 Quantum Exponent field
In `decimal128` the quantum exponent _qExp_ needs to represent values in the range [-6176..6111]. When coupled with the 34-digit integer coefficient this corresponds to a normal scientific exponent range of [-6143,6144]. 

IEEE 754 binary floating point (and many other floating point representations) store a _biased_ exponent as a packed field of the representation. This requires an addition/subtraction operation during packing and unpacking ... easily accomplished in hardware, but another operator for decoding in software. 

UBD packs the qExp exponent in unbiased, two's-complement form in the top 14 bits of the value. The qExp can extracted/decoded to Int64 simply by performing a signed arithmetic shift right of hi64 by 49 bits. Conversely, a validated Int64 qExp can be isolated for packing simply by shifting left 49 bits. 

Observe that 14 bits allows the qExp field to represent two's-complement values in the range [-8192..8191]. The range of finite values we need to represent is [-6176..6111]. Therefore, values outside the finite range are available to represent non-finite special values ... Infinity and NAN variants. 

The intended consequence of the layout is that decoding a finite operand reduces to two independent, dependency-free operations: a mask that yields the binary coefficient and an arithmetic shift that yields the signed quantum exponent. Neither requires a table lookup or a conditional branch.

### 3.3 Finite values

All values that have a qExp in the range [-6176..6111] and a coefficient less than 10^34 are finite and valid `decimal128` values. Since values are never _normalized_ there is no special treatment required for _subnormal_ values in the binary floating point sense. These are fundamental characteristics of decimal floating point (as formalized by Cowlishaw) and has nothing to do with UBD representation. 

All finite UBD values have qExp in the range [-6176..6111] and coefficient less than 10^34. 

One interesting result of from the UBD format is that UInt128 integers less than 10**34 have exactly the same binary representation in UBD. The coefficient value is the value of the integer. The qExp and sign are zero. This means that a UInt64 (or a non-negative Int64) can be converted to a UBD128 by setting the hi64 to zero. 

Negative two's-complement values are slightly more complicated since `decimal128` is sign-magnitude. For UBD representation of an Int64, the _lo64_ become the absolute value and the sign bit gets slid to bit 49 of _hi64_. 

### 3.4 Special values

The IEEE 754 specification defines values and behavior for Infinity and NaN, referring to these non-finite values collectively as _special values_. All values, including special values, have a sign. Therefore, we have +/- Infinity and +/- NaN. NaN is available in a quiet form and a signaling form, sNaN. NaN values may also have an integer payload of up to 33 decimal digits. Indeed the payload limit is 33 digits, one less than the precision of 34. The extra digit to achieve 34 digits of precision was/is part of the packing complexity associated with the `decimal128` DPD/BID interchange formats. 

Broadly, in UBD encoding, all special values have _both_:
1. an oversized qExp that is above the normal range ... greater than 6111
2. an oversized coefficient that is above the valid limit of 10**34 - 1 ... 34 9's of precision

Every non-finite value has two independent ways to determine if one or more operands is finite. 



However, specific values are chosen to facilitate software encoding/decoding on general-purpose processors. 


#### 3.4.1 Special values - coefficient field

The full `decimal128` coefficient range tops out at 34 decimal digits. UBD128 reserves coefficient field values *above* this legal maximum to denote non-finite operands — infinities and quiet/signaling NaNs — with their sign and NaN payload carried in the surrounding bits.

The hex representation of the hi64 bits of 10^34 is
0x1ED09BEAD87C0
0x1_ED09_BEAD_87C0

With underscore separators it is easier to confirm 49 bits ... 1 + (3 * 16) = 1 + 48 = 49

The term _coeffHi49_ is used to refer to the upper 49 bits of the 113-bit coefficient. Note that _coeffHi49_ refers to the lower 49 bits of hi64 of the 128-bit value. 

Any value greater than this could be chosen. 
Note that this value starts with 0x1E. It is clear that all values starting with 0x1F are well into the oversized range. 

All valid UBD special values have coefficients that start with 0x1F. 

The hex representation of the coeffHi49 bits of Inf and NaN0 == NaN with payload zero is:
0x1_F000_0000_0000

In the case of NaN, all of the bits after the 0x1F prefix, 113 - 5 = 108 bits are available to store payload. 
However, representing 33 digits requires 110 bits, so we are 2 bits short of meeting our 33-digit-payload requirement. 
To support the full 33-digit payload required the the spec, we add some complexity to the qExp field. 

#### 3.4.2 Special values - qExp

There are two ranges of non-finite qExp values available ... above 6111 or below -6176. Each has subtle complexity brought on by characteristics of two's-complement notation. 
When viewed in a 14-bit field, the top 4 bits of 6111 are 0b0101 or 0x5.
UBD tags all special values with the top 4 bits being 0b0111 or 0x7, corresponding to 7168. 
After the first 4 bits, the nan bit distinguishes Infinity from NaN
If the NaN bit is set, then the next bit is the Signaling bit, distinguishing qNaN from sNaN. 
If the qExp identifies a NaN, then the lo 2 bits of the qExpField represent 2 additional bits that are part of the payload. When combined with the 108 bits available in the coefficient this gives us 2 + 108 = 110 bits ... sufficient to represent 10^33-1 == 33 9's.

Within the 14-bit qExp field, special values are encoded as follows:

0b0111xx_000000_xx == non-finite
0b0111ns_000000_pp == n: NaN bit, s:Signaling bit, pp = payloadHi2
0b011100_000000_00 == Infinity == 6176
0b01111x_000000_pp == NaN
0b011110_000000_pp == qNaN
0b011111_000000_pp == sNaN (7963..7967)

All of our non-finite values fall in the range [7168,7967] with a lot of gaps. That seems somewhat complicated to decode ... and decoding complexity is what we are trying to avoid. 

If we look at this in pseudo-code, the decoding complexity doesn't look quote so bad. For the following we assume:
 * 64-bit register width
 * >>> is an unsigned shift right
 * integer constants are decimal values
 * hi64 represents he the hi64 bits of the UBD-encoded value in question

 isFinite    { (hi64 >>> 60) != 7 }
 isNonFinite { (hi64 >>> 60) == 7 }
 isInfinite  { (hi64 >>> 59) == 14 }
 isNaN       { (hi64 >>> 59) == 15 }
 isQNaN      { (hi64 >>> 58) == 30 }
 isSNaN      { (hi64 >>> 58) == 31 }

This gives us a full range of predicates, all accessible with a single shift and compare against a small immediate constant that is stored in the instruction/instruction-stream. In addition, this decoding only happens off the fast-path ... for fast-path operations we never get this far. 

#### 3.4.3 NaN payload reconstruction

NaN payload of 33 decimal digits requires 110 bits. 
Our coefficient field has 113 bits. 
Setting the top 5 bits of the coefficient field to 0x1F is our baseline for oversized coefficients. 
This leaves us 113 - 5 = 108 bits. 
We store the highest 2 bits of the NaN payload in the lowest 2 bits of the qExp field. 

The encoding process is as follows:

payload110 == 110 bit payload
payloadLo64 == lo 64 bits of payload
payloadHi46 == hi 46 bits of payload
payloadHi2 == payloadHi46 >>> 44
payloadMid44 = payloadHi44 & BIT_MASK_44

decoding is the opposite


### 3.4 Decoding cost compared

Be careful ... I don't want to overstate the case with this table

| Encoding | Coefficient recovery | Exponent recovery | Operand classification |
|---|---|---|---|
| DPD | Declet unpack (table / bit-twiddling) | Field extract + decode | Combination-field decode |
| BID | Conditional extract (combination field) | Conditional extract | Combination-field decode |
| **UBD** | **Single mask** | **Single arithmetic shift** | **Folded into range check** |

*Table 1. Qualitative per-operand decode work on a general-purpose CPU.*

The oversized coefficient pays off for fast-path addition, subtractionFor addition, subtraction, and multiplication the fast-path operation can proceed, and fall back to the sl

Every non-finite value carries a coefficient larger than any finite value can, the question "is this operand non-finite?" becomes a single magnitude comparison against the finite maximum — and that comparison can often be folded into the arithmetic an operation already performs (for example, an overflow/range check), rather than standing as a separate classification step. The fast path for two finite operands thus contains no special-value branch at all; the slow path is entered only when a comparison that the operation needs anyway reveals an out-of-range coefficient.


## 4. Arithmetic on UBD128

For a set of simple but common fast-path cases, UBD offers fast execution that is small enough to be inlinable. Examples below are taken from existin implementations. 

UBD's value is realized in the inner loops of the basic operations. For addition, subtraction, and multiplication, the common case is two finite operands, and UBD makes the per-operand preamble trivial: mask out each coefficient, shift out each exponent, and proceed. There is no declet expansion, no combination-field case analysis, and no standalone class test.


### 4.1 Addition

Addition proceeds as follows: 
 * coefficient hi64 values are masked to generate coeffHi49 values
 * coeffHi49 values are added together, generating sumHi49
 * qExpAndSignBit values are extracted, each with a single shift operation
 * if (x.qExpAndSignBit == y.qExpAndSignBit) && ((sumHi49 >> 48) == 0) { fast-path } else { slow-path }

Observe that the fast-path is only taken if the hi-bit of coeffHi49 is not set. A minority of 34-digit values route to the slow-path, but they will be handled fine over there. 
With UBD the check for non-finite values gets rolled into the overflow check. 

#### 4.1.1 Addition fast-path

fast-path only happens when qExp are equal, signs are equal, and sumHi49 fits in 48 bits. The maximum possible value for sum113 is
0x1_0000_0000_0000 0xFFFF_FFFF_FFFF_FFFE. 

The fast-path does not compute the entire 113 bit sum113 by design. On a 64-bit processor that would lead to additional instructions and increased latency before the fast-path condition. 

The fast-path simply has to fully construct the full sum by summing the two coeffLo64 values. Any carry generated out of the sumLo64 gets added to sumHi49. If all the lower 48 bits of sumHi49 were turned on 0x0_FFFF_FFFF_FFFF then this might roll up to 0x1_0000_0000_0000. But this is the correct result coefficient. qExpAndSignBit are taken from one of the input operands. Range checking does not need to be performed because qExp came from a valid value and sum113 is valid. 

Observe that the masking of operand coefficients and shifting of qExpAndSignBit for the two operands are completely independent. Processors with multiple integer ALUs can execute these operations in parallel. 

The instruction sequence is small enough that the fast-path might be considered inlinable. 

Recall that all non-finite values have the hi bit of hi49 set. For example, in the case of +Infinity + +Infity, the qExpAndSignBit is the same, but the sumHi49 of exceeds 48 bits, thereby forcing to the slow-path. 

This fast-path case only works for aligned values of the same sign, but that situation can occur frequently, for example when summing the values 
in a database column where the schema defines a fixed decimal point. 

#### 4.1.2 Addition slow path

The addition slow-path catches the following: 
 * unequal qExp
 * unequal signBit
 * valid 34-digit values with 113 bits
 * genuine overflow values with 113 or 114 bits
 * non-finite special values

The slow-path falls back to traditional methods of classifying operands to make decisions. 

### 4.2 Subtraction

Subtraction of values with like qExpAndSignBit cannot overflow. 
The same sumHi49 is used to confirm that both operands are finite. 

### 4.3 Multiplication

The multiplication fast-path selects finite values which meet three criteria. 
1. qExp sum in range
2. coeff
3. coeffProd 112 bits or less

     if ((hi49Sum >> 48) == 0 && 
         prodQExp >= -6176 && 
         prodQExp <= 6111 && 
         (prodHi | (prodLo >> 112)) == 0)
    {
        return Decimal128(sign: prodSignFlag, qExp: prodQExp, coeff: prodLo)
    }


### 4.3 Rounding and re-encoding

UBD supports all finite values defined by IEEE 754-2008/2019. 
Rounding is a computational thing and has nothing to do with the representation. 

Once the precision and/or qExp are reduced to the finite range, packing is straightforward. 
(qExp shl 50) | (signBit shl 49) | hi49
lo64

### 4.4 Conversion to and from interchange formats

existing implementations support only to/fromBID128 and to/fromDPD128. These are done when data in a known `decimal128` interchange format is being read or written. The cost of this decoding/encoding is presumably comparable to the unpacking/packing cost required by any software implementation, although the current Swift and Kotlin implementations are presumably not as well tuned as more mature implementations. For to/fromDPD128 in particular, the declet decoding is implemented using Cowlishaw's decbits algorithms rather than lookup into a table with 2^10 = 1024 table entries. 

## 5. Implementation

UBD is implemented in **Swift** and in **Kotlin Multiplatform**, giving native decimal128 support across the platforms those toolchains target. 

The Swift value-class memory model is ideally suited to a numeric datatype. The implemention is written in Swift 6.3 and makes heavy use of the UInt128 datatype. It is 100% written in Swift with no external dependencies. (honestly, I don't even know how to pull in Swift dependency) Understandably, the Swift implementation makes heavy use of the _overflow operators_ (?)

The **Kotlin Multiplatform** implementation offers a Java/Java-style heap-allocated-object model. The values are immutable, enforced by the Kotlin compiler by using _val_ fields. The core implementation is 100% Kotlin, restricted to JVM-native signed types ... no Kotlin pseudo-unsigned types. (The only operation written in C on for Kotlin native is unsignedMulHi, which provides the hi 128 bits of a 64x64 unsigned multiply ... which is available on JVM but is not avail in the standard Kotlin multiplatform library.) The Kotlin implementation is quite heap-friendly. Core operations, include all arithmetic operations, allocate at most 1 32-byte object ... 12-byte header + 4 bytes unused + 2x8-bytes UBD. 

Syntatically, the Swift and Kotlin implementations look as much alike as possible. Over time they will look more alike. Subject for a companion paper. 

A portable **C core** is in progress, intended to serve as a single shared implementation that other languages can bind to. 

At this time the C core is not intended to be used directly. Rather, it is intended to be wrapped by 

> *Placeholder.* Summarize the architecture shared across implementations, any platform-specific concerns (e.g., availability of 128-bit integer types, wide-multiply intrinsics), and how the C core is designed to be embedded.

### 5.1 Conformance

The Swift and Kotlin Multiplatform implementations pass three independent `decimal128` test-vector suites:

- the **Cowlishaw/IBM decTest** suite,
- the **IBM FPtest** suite, and
- the **Intel `libbid`** decimal128 vectors.

> *Placeholder.* Report coverage: which operations and corner cases (rounding modes, cohort/quantum preservation, NaN propagation, signaling-NaN behavior, subnormal handling) each suite exercises, and confirm full pass status with version identifiers for reproducibility.

## 6. Decode Cost

UBD's contribution is a complexity claim about decoding, not a wall-clock one. On the finite fast path, recovering an operand reduces to a single mask for the coefficient and a single arithmetic shift for the exponent, with operand classification subsumed by a range check the arithmetic already performs. This contrasts with the declet expansion DPD requires and the combination-field case analysis BID requires, as summarized in Table 1 (Section 3.4). These are structural properties of the encoding, independent of any particular CPU, compiler, or workload.

A quantitative performance study — microbenchmarks of per-operand decode, operation throughput against a BID baseline such as Intel `libbid`, and the cost of the RRMP10 multiply/shift path relative to hardware division — belongs with the arithmetic kernels it measures and is the subject of a forthcoming companion paper.

## 7. Discussion

### 7.1 When UBD helps and when it does not

UBD optimizes the arithmetic fast path at the cost of conversions at interchange boundaries. It is therefore most valuable in workloads that perform many operations per value loaded or stored — typical of computation-heavy financial and analytical code — and less advantageous where values are touched once between encode and decode.

### 7.2 Limitations

UBD trades work at the interchange boundary for cheaper arithmetic, so it is not the right choice everywhere (see Section 7.1). Two design limitations are worth stating plainly. First, the "folded" special-value check is only free to the extent that an operation already performs a range check on its coefficient or product; where it does not, an explicit comparison is reintroduced, though it remains a single magnitude test rather than a combination-field decode. Second, UBD is an in-memory format: values must still be converted to a standard interchange encoding (DPD or BID) for storage and exchange, and the cost of that conversion is borne at I/O boundaries.

Honestly, this cost is very low and not much more than the cost that would normally be associated with any operation. If you are reading from a file and summing values the cost might be slightly higher, but I'm not sure it would be measurable. If this were perceived to be a true limitation then I could take another look at optimizing the decoding.  

The real truth is, users would not have another option. 

### 7.3 Future work

Candidate directions do *NOT* include a `decimal64` variant because nobody wants it. 
completion of the portable C core ... yep
formal verification of the encode/decode round-trip and the special-value invariants ... nope
and a quantitative performance study of the arithmetic kernels and the RRMP10 rounding path, planned for companion papers. 

## 8. Conclusion

UBD reframes the decimal128 storage question for the common case of software implementations of decimal floating point. UBD is able to maintain the density of the DPD and BID interchange formats while simultaneously allowing for access to coded coefficient and qExp with a single trivial operation. Conforming Swift and Kotlin Multiplatform implementations pass the Cowlishaw/IBM decTest, IBM FPtest, and Intel `libbid` suites. A quantitative study of the arithmetic kernels built on this format is left to a companion paper.

## References

[Goldberg 1991] D. Goldberg, "What Every Computer Scientist Should Know About Floating-Point Arithmetic," *ACM Computing Surveys*, vol. 23, no. 1, pp. 5–48, March 1991. Available (edited reprint): https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html

[Cowlishaw 2009] M. F. Cowlishaw, *General Decimal Arithmetic Specification*, version 1.70, IBM, 25 March 2009. Available: https://speleotrove.com/decimal/decarith.pdf

[Cornea et al. 2009] M. Cornea, J. Harrison, C. Anderson, P. T. P. Tang, E. Schneider, and E. Gvozdev, "A Software Implementation of the IEEE 754R Decimal Floating-Point Arithmetic Using the Binary Encoding Format," *IEEE Transactions on Computers*, vol. 58, no. 2, pp. 148–162, February 2009. Available: https://www.cl.cam.ac.uk/~jrh13/papers/decimal.pdf

> *Placeholder — remaining references to be completed in the target venue's citation style.* Anticipated additions include:
>
> - IEEE Std 754-2019, *IEEE Standard for Floating-Point Arithmetic.*
> - M. F. Cowlishaw, *Decimal Arithmetic Encodings* (the IEEE 754 decimal interchange encodings, DPD and the combination field), available at https://speleotrove.com/decimal/decbits.pdf. The *decTest* test suite is available at https://speleotrove.com/decimal/.
> - M. F. Cowlishaw, "Decimal Floating-Point: Algorism for Computers," *Proc. 16th IEEE Symposium on Computer Arithmetic*, 2003.
> - Intel, *Intel Decimal Floating-Point Math Library* (`libbid`).
> - IBM, *FPtest* / FPgen test suite documentation.