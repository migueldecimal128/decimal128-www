---
layout: default
permalink: /whitepapers/ubd64.html
title: "UBD64: A Proposed Unpacked Binary Decimal Encoding for IEEE 754 decimal64 — Decimal128"
description: "UBD64 applies the UBD construction to IEEE 754 decimal64: a mask-and-shift decode for common coefficients, a second layout for the largest coefficients, and specials that route aligned addition to the general routine without decoding tags."
heading: "UBD64 (A Proposed Unpacked Binary Decimal Encoding for IEEE 754 decimal64)"
---

<div class="whitepaper" markdown="1">

<div class="whitepaper-abstract" markdown="1">

**Abstract.** UBD128 places a binary integer coefficient, a sign bit, and an unbiased quantum exponent in one 128-bit word. This layout exposes the coefficient with a mask and the signed quantum exponent with an arithmetic shift. The processor can execute the two instructions in parallel, and the simple decoding reduces the instruction count on the arithmetic fast path. Applying the same construction to decimal64 requires 65 bits. UBD64 recovers the missing bit by giving the largest coefficients a second layout. In the common layout, a mask extracts the coefficient and an arithmetic shift extracts the quantum exponent. The large finite layout stores the low 50 coefficient bits and sets bit 52 of the word. Infinity and NaN also set bit 52. The coefficient-sum bound used by aligned addition therefore routes all three cases to the general routine without decoding their tags. This removes an independent exponent-range check from each inlined addition.

**Keywords.** Decimal floating-point, IEEE 754, decimal64, binary integer coefficient, in-memory encoding.

</div>

---

## 1. Introduction

Consider the decimal64 addition 1.25 + 2.50. The coefficients are 125 and 250, and both operands have quantum exponent −2. Adding the coefficients gives 375. Retaining the shared exponent gives the result 3.75. In UBD128 [1], a mask extracts the upper bits of each coefficient (the low word already holds the lower bits), and an arithmetic shift extracts each signed quantum exponent. These operations are independent both within and across operands, so the processor can execute them in parallel. How much of this property can an eight-byte decimal64 retain?

IEEE 754 decimal64 provides 16 digits of precision. A finite value has the form (−1)ˢ × C × 10ᑫ, where 0 ≤ C < 10¹⁶ and −398 ≤ q ≤ 369 [2]. This gives 768 possible quantum exponents. Storing each field independently takes 54 bits for C, 10 for q, and one for s. The opportunity lies in the unused portions of both fields. Some 10-bit exponent codes are available as tags, and the largest legal coefficients share four leading bits.

UBD64 uses those two observations to fit the full decimal64 value set in one word. Like UBD128, it is an in-memory representation designed for simple decoding on conventional CPUs. Existing DPD64 and BID64 interfaces continue to use their specified interchange encodings.

## 2. The UBD64 encoding

Bit 0 is the least significant bit. The operand sign is 0 for positive and 1 for negative. The symbol q denotes the mathematical quantum exponent, stored in two’s complement in the common layout. The following table specifies canonical words, with fields listed from most to least significant.

| Class | Fields, high to low | Field widths |
|---|---|---|
| Common finite | q · sign · coefficient | 10 + 1 + 53 |
| Large finite | largeCode · sign · 1 · eLo2 · coefficientLo50 | 10 + 1 + 1 + 2 + 50 |
| Infinity | 0101111000 · sign · 111 · zero | 10 + 1 + 3 + 50 |
| Quiet NaN | 0101111100 · sign · 111 · payload | 10 + 1 + 3 + 50 |
| Signaling NaN | 0101111110 · sign · 111 · payload | 10 + 1 + 3 + 50 |

### 2.1 Common finite values

For C < 2⁵³, bits 0–52 hold C, bit 53 holds the sign, and bits 54–63 hold q. In the pseudocode below, ASR is a signed arithmetic right shift, LSR is a logical right shift, and MASK(k) has its low k bits set.

    q = ASR(word, 54)
    sign = LSR(word, 53) & 1
    coefficient = word & MASK(53)

These extractions are independent. Every coefficient of 15 digits or fewer fits this layout, as do 16-digit coefficients through 9,007,199,254,740,991. At q = 0, a nonnegative integer in this range has the same bit pattern as its integer coefficient. The all-zero word represents +0 at quantum zero. Other zero cohorts and negative zero retain their exponent and sign.

### 2.2 Large finite values

The largest coefficient is 9,999,999,999,999,999. Observe that

    2⁵³ ≤ C < 10¹⁶ < 2⁵³ + 2⁵⁰.

The first inequality here selects the large layout. Throughout this interval, coefficient bit 53 is one and bits 52, 51, and 50 are zero. Only bits 0–49 vary. The encoding stores those 50 bits in their natural positions. For example, at C = 2⁵³ the stored low field is zero, and the tag supplies the entire coefficient magnitude.

The sign occupies bit 53 in every layout. In a large finite word, bit 52 is always one, even though bit 52 of the decoded coefficient is always zero. To make room for this marker, split the biased exponent e = q + 398, which ranges from 0 through 767. Store its low two bits at positions 51–50. Its upper eight bits select one of 192 reserved codes in positions 63–54.

    e = q + 398
    largeCode = 384 + LSR(e, 2)
    word = (largeCode << 54) | (sign << 53) | (1 << 52)
           | ((e & 3) << 50) | (coefficient & MASK(50))

Decoding a canonical large finite word reverses these steps. All shifts operate on 64-bit words.

    largeCode = LSR(word, 54)
    sign = LSR(word, 53) & 1
    e = ((largeCode − 384) << 2) | (LSR(word, 50) & 3)
    q = e − 398
    coefficient = (1 << 53) | (word & MASK(50))

At q = −398 the code is 384 and the two low exponent bits are 00. At q = 369 the code is 575 and the two bits are 11. The split exponent adds work only when packing or decoding the large layout.

### 2.3 Infinity and NaN

The gap between the maximum common exponent (369) and the first large-layout prefix (384) supplies the special-value codes. The ten high bits have the form 0101111ns0. With n and s both clear, code 376 denotes infinity. Setting n gives code 380 for quiet NaN. Setting both gives code 382 for signaling NaN. Each class retains its operand sign at bit 53.

Bits 52–50 are 111 for every special. Infinity has zeros in the remaining 50 bits. A NaN stores its payload there as an unsigned integer in [0, 10¹⁵−1]. Since 10¹⁵ < 2⁵⁰, the full 15-digit payload can be extracted with one mask. In particular, infinity, quiet NaN with payload zero, and signaling NaN with payload zero have identical low fields and distinct high tags.

Bit 52 serves the same purpose here as in a large finite word. Masking off the low 53 bits of any such operand yields an unsigned integer of at least 2⁵². A common finite coefficient may also have bit 52 set. The arithmetic fast path needs only the implication in the other direction: a masked value below 2⁵² guarantees a common finite operand.

### 2.4 Canonical decoding

Read bits 63–54 as an unsigned code. Codes 0–369 and 626–1023 identify common finite words, with the latter interval representing q from −398 through −1. Codes 384–575 select the large layout. Codes 376, 380, and 382 select the specials. All other codes are reserved. For raw input, canonical validation also checks the marker and coefficient bound for large finite words, and the fixed prefix and zero or payload field specified in §2.3 for specials. Arithmetic below assumes canonical operands.

## 3. Arithmetic on UBD64

### 3.1 Aligned addition

The inline path adds the low field of y into the whole word x, so the sign and quantum of x ride along in the sum. It then tests two quantities: the difference in the high fields as a bitwise exclusive-or, and the bits of the sum from bit 52 up against the high bits of x with bit 52 clear.

    sum = x + (y & MASK(53))
    highDiff = LSR(x ^ y, 53)
    overflow = LSR(sum ^ (x & ~MASK(53)), 52)
    if (highDiff | overflow) == 0:
        return sum
    return addGeneral(x, y, roundingDirection)

The high bits of x have bits 52 and below clear, so the bits of the sum from bit 52 up equal them exactly when the two low fields together are below 2⁵². That is the fast-path bound: overflow is zero exactly when (x & MASK(53)) + (y & MASK(53)) < 2⁵². Both low fields are unsigned and below 2⁵³, so their sum needs at most 54 bits and cannot wrap the register. Every large finite operand, infinity, or NaN has bit 52 set, contributes at least 2⁵² to that sum, and so fails the bound. If the bound holds, both fields are ordinary coefficients, their exact sum fits the result field, and the sum is the result word: the shared sign and quantum of x over the sum of the coefficients. Equality of the high eleven bits establishes that x and y share them.

Masking both low fields and then copying the high bits of x into the result computes the same predicate and the same result, with two more instructions: the mask of x and the merge. Adding into x leaves the header in place. This is the arrangement BID64's aligned addition uses for its own header.

**Why this matters when addition is inlined.** An explicit classification would first establish that the shared exponent is in range. The operation would still have to test whether the result fits. Here the existing sum comparison serves both purposes. The inline body contains two predicates: high-field equality and the sum bound. It performs no separate exponent extraction or range test. This matters even on a processor that can overlap an independent range check with the coefficient addition through instruction-level parallelism. When the check generates extra instructions, those instructions still occupy space at each inline site and consume front-end and execution resources when run. Removing the check can reduce those costs even if the critical-path latency stays the same. The machine-instruction count and code size can be measured independently of elapsed time.

The tighter bound has a cost. At quantum zero, adding 1 to 2⁵²−1 goes to the general routine even though the result still fits the common layout. Adding 1 to 2⁵³−1 also goes there, this time producing a large-layout result with a zero low coefficient field. Both sums are exact. Every pair of coefficients of at most 15 digits satisfies the tighter magnitude bound because 2 × (10¹⁵−1) < 2⁵². Their signs and quanta must still match.

### 3.2 Subtraction and multiplication

Aligned magnitude subtraction cannot increase coefficient width. If two common-layout operands produce a nonzero magnitude difference at their shared quantum, the result fits the common layout. Exact cancellation requires the signed-zero rule for the operation and rounding direction. With no sum to bound, the inline path establishes that both operands use the common layout by testing bit 52 of each, which a large finite word or a special always sets. The test also refuses common coefficients from 2⁵² up, which the general routine then handles.

For multiplication, two common-layout coefficients can produce a 106-bit product. The inline path forms the full product of the two low fields and accepts it under three conditions.

    (hi, lo) = MUL128(x & MASK(53), y & MASK(53))
    q = ASR(x, 54) + ASR(y, 54)
    if (hi | LSR(lo, 53) | ((x | y) & (1 << 52))) == 0 and (q + 398) as unsigned < 768:
        return (q << 54) | ((x ^ y) & (1 << 53)) | lo
    return mulGeneral(x, y, roundingDirection)

First, the product fits the common coefficient field: its high word is zero and its low word is below 2⁵³. Second, both operands use the common layout: bit 52 is clear in each. The product bound alone does not establish this, because a large finite or special operand multiplied by a zero coefficient gives a zero product. Third, the exponent sum lies in [−398, 369]. This test is required even for two common operands, whose exponents can sum outside the range (−398 + −398 = −796). The two exponents are added after extraction rather than in the header, because the sign at bit 53 lies directly below the quantum field and adding the headers would carry the sign bits into it. The result packs the exponent sum, the exclusive-or of the operand signs, and the product.

A narrower gate requires each coefficient to fit in 26 bits, so that the exact product fits in 52 bits. It also proves both operands common, since bit 52 is then clear, and it can use a 64-bit multiply. It sends every coefficient of 2²⁶ (about 6.7 × 10⁷) or more to the general routine, which includes money amounts above about 671,088.64 at quantum −2. The full-product gate accepts what BID64's in-place multiplication accepts.

## 4. Evaluation and limitations

The finite layouts partition the integer interval [0, 10¹⁶−1] at 2⁵³. In the lower interval the coefficient is stored verbatim. In the upper interval the stored field is C − 2⁵³, which is nonnegative and fits in 50 bits. Both layouts preserve all 768 quantum exponents and both signs. Together with the disjoint special tags, these properties give a unique canonical encoding for each sign, quantum, and coefficient tuple and for each supported special value and payload.

The common layout covers about 90.07% of the possible coefficient magnitudes. This fraction describes the encoding space. Actual fast-path frequency depends on the workload, including the quantum and sign relationships between operands. A column of 16-digit identifiers and a column of fixed-scale invoice amounts can exercise quite different paths.

The bit-52 marker that lets §3.1 omit the range test also halves the addition bound. BID64's aligned addition accepts a coefficient sum below 2⁵³, the width of its first-form coefficient field. UBD64 accepts a sum below 2⁵², because a sum from 2⁵² up cannot be told apart from an operand with the marker set. Coefficients of at most 15 digits are unaffected, since 2 × (10¹⁵ − 1) < 2⁵². Sixteen-digit coefficients summing to between 2⁵² and 2⁵³ go to the general routine, which BID64 would decide inline. Such sums arise in interest and allocation arithmetic, where intermediate results are rounded to full precision. For example, the coefficients of 0.3541666666666667 and 0.2916666666666667 sum to about 6.46 × 10¹⁵. In one measurement adding pairs of 16-digit monthly-interest values, 25.7% took the UBD64 inline path against 53.7% for BID64.

The principal cost relative to UBD128 is visible in §3.1: some finite inputs need another decode, and an exact finite result can cross a layout boundary. BID64 also uses an implicit leading pattern for large coefficients. The case for UBD64 therefore depends on the cost of its common-layout unbiased exponent, adjacent exponent and sign, coefficient-sum test, and repacking in actual arithmetic kernels. A controlled UBD64/BID64 comparison using the same kernels would measure that cost. An inline comparison should record emitted instruction count and code bytes at the call site alongside elapsed time and the fraction of sums sent to the general routine. The conformance results reported for UBD128 apply to that implementation family. Decimal64 arithmetic conformance and comparative timings remain to be established.

## 5. Conclusion

Decimal64 is one bit short of a fully independent sign, exponent, and binary coefficient. Its largest coefficients have enough fixed high bits to recover that bit while preserving an eight-byte representation. UBD64 consequently retains the mask-and-shift decode for small coefficients, accommodates the full finite range in a second layout, and carries each NaN payload in one contiguous field. Setting bit 52 in every large finite and special word lets the coefficient addition itself route these operands to the general routine.

## References

[1] Miguel. *UBD (An Unpacked Binary Decimal Format for Fast Software Decoding of IEEE 754 decimal128).* [Whitepaper](https://migueldecimal128.github.io/decimal128-www/whitepapers/ubd.html)

[2] IEEE. *IEEE Standard for Floating-Point Arithmetic*, IEEE Std 754-2019, especially §3.5 and Table 3.6. [DOI 10.1109/IEEESTD.2019.8766229](https://doi.org/10.1109/IEEESTD.2019.8766229)

</div>
