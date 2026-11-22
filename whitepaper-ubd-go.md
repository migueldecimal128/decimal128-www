---
layout: default
permalink: /whitepapers/ubd-go.html
title: "UBD in a Compiler: Go's Built-in decimal128 Stored as UBD — Decimal128"
description: "A fork of the Go decimal toolchain stores the predeclared decimal128 type as UBD, with inline fast paths chosen by level, measured on whole applications against the XOR-BID original."
heading: "UBD in a Compiler (Go's Built-in decimal128 Stored as UBD)"
---

<div class="whitepaper" markdown="1">

<div class="whitepaper-abstract" markdown="1">

**Abstract.** The UBD whitepaper [UBD] defines an in-memory format for IEEE 754 decimal128 whose coefficient and exponent are recovered with a single mask and a single shift, and whose special values carry oversized coefficients. This companion paper reports what that format does as the storage of a language's built-in decimal type. In a fork of a prototype Go toolchain with predeclared decimal types, `decimal128` is stored as UBD instead of XOR-BID (BID with the high word XORed so that all bits clear is zero), every operator is a call into a kernel that works on UBD directly, and a compiler flag chooses how much is inlined in front of those calls. At the default level, one test covers exponent, sign, coefficient size, and special values, and the inline code at a binary operator's call site is 7 to 28 instructions instead of XOR-BID's 65 to 201. On seven application benchmarks the default build is within 1.2% of XOR-BID on average on arm64 and 0.6% faster on x86_64, with 37–42% of its code; a level with XOR-BID's larger inline paths, moved onto UBD, is 6–7% faster with 65–73% of XOR-BID's code.

**Keywords:** decimal floating-point, IEEE 754, decimal128, UBD, BID, XOR-BID, Go, compiler, inlining, code size.

</div>

---

## 1. Introduction

The UBD whitepaper [UBD] argues for UBD on structural grounds: decoding an operand costs a mask and a shift, and the check for special values folds into a range check the arithmetic already performs. Its implementations are libraries. A built-in type is a different setting: every arithmetic operator in a program is expanded by the compiler, so the size of the code at each call site is multiplied by the number of call sites, and the choice between inlining a fast path and calling a kernel is made once for every program.

Go has a proposal to add decimal floating-point types [Go #19787], with a prototype toolchain by Marcelo Cantos [Cantos decimal] that stores `decimal128` as XOR-BID, a variant of BID. This paper describes a fork of that toolchain that stores it as UBD [go-decimal-ubd] (Section 2), the inline fast paths its compiler can place in front of the kernel calls, chosen by level (Section 3), and their cost and benefit on whole applications against XOR-BID, on arm64 and x86_64 (Section 4). Section 5 reports a kernel change that closed one gap and two attempts that did not close another, and Section 6 what remains.

## 2. Go's built-in decimal128 on UBD

A proposal to add decimal floating-point types to Go [Go #19787] has a prototype toolchain by Marcelo Cantos [Cantos decimal] in which `decimal64` and `decimal128` are predeclared types with operators, implemented on BID: a `decimal128` is stored as its BID encoding with the high word XORed with the encoding of +0E+0, so that all bits clear is the zero value (*XOR-BID*). Its compiler expands each operator into integer fast paths inline, with calls into a software kernel for the rest.

The `ubd128` fork of that toolchain [go-decimal-ubd] stores `decimal128` as UBD instead, unchanged in layout from the UBD whitepaper [UBD], so that all bits clear is +0E+0 with no mask. The runtime, the conversions, formatting and parsing, and the kernel all work on UBD directly; BID appears only at the interchange boundary (reading and writing BID bits) and in a compile-time zero test of constants. The kernel is the XOR-BID kernel with its decoding and packing replaced by UBD's and its arithmetic unchanged. On amd64 and arm64, each operator compiles to a direct call into a kernel entry that takes the two 64-bit words of each operand in the registers they already occupy, low word first, so a call site moves nothing into place, optionally preceded by an inline fast path. (`decimal64` remains XOR-BID.)

## 3. Inline levels

How much is inlined is chosen by the compiler flag `-d=ubdlevel`:

| Level | Inline code at each call site |
|---|---|
| 1 | none: every operation is a function call to the general-path kernel implementation — the smallest code, but the slowest performance |
| **2** (default) | the narrowed fast paths described below, with function call fall-back to general-path kernel implementations |
| 3 | the same large inline paths the prototype's compiler had for XOR-BID, modified for UBD structure, in front of the same kernel implementations also modified for UBD structure |

The level-2 paths narrow the fast paths of [UBD] (Section 4) to operands whose coefficients fit one 64-bit word, effectively covering up through 19 decimal digits. One test then serves addition, subtraction, and comparison:

```
(xHi64 ^ yHi64) | (xHi64 << 15) == 0
```

The high words are equal, so the operands share qExp and sign, and x's high word holds no coefficient bits, so both coefficients are below 2^64. Because every special value carries the `0x1F` coefficient prefix in its high word ([UBD], Section 3.4.1), the same test excludes them: the special-value check is folded into the operand test, as for addition in [UBD] (Section 4.1), now for comparisons as well.

In plain terms, the inline code finishes the operation itself, with no call, in these cases:

- **Addition `x + y`:** x and y have the same sign and the same exponent, and both coefficients fit in 64 bits (up through 19 decimal digits). The sum needs no further test: it may be one bit wider than 64 bits, and that bit goes into the high word, where the coefficient continues. The result keeps x's sign and exponent.
- **Subtraction `x - y`:** the same conditions: same sign, same exponent, both coefficients in 64 bits. The coefficients are subtracted; if y's is the larger, the difference is negated and the result takes the opposite sign. A zero result is +0.
- **Multiplication `x * y`:** any signs and any exponents, provided both coefficients fit in 56 bits (up through 16 decimal digits) and the sum of the exponents is in range. The product then fits in 112 bits and is exact; its sign is the exclusive or of the signs.
- **Comparison of two values:** the same conditions as addition: same sign, same exponent, both coefficients in 64 bits. The coefficients are compared directly, with the order reversed for negative values.
- **Comparison with zero:** always inline, with no kernel call at all. Equality tests `(hi << 15) | lo == 0`; the ordered comparisons place the sign above the coefficient in one word and test it as a signed integer.

Every other operand pair takes the kernel call. Table 1 shows the code each operator costs at a call site.

| Operator | XOR-BID | UBD level 1 | **UBD level 2** | UBD level 3 |
|---|--:|--:|--:|--:|
| `x + y` | 169 / 119 | 2 / 3 | **12 / 8** | 101 / 74 |
| `x - y` | 179 / 126 | 2 / 3 | **25 / 14** | 102 / 76 |
| `x * y` | 84 / 65 | 2 / 3 | **28 / 20** | 38 / 32 |
| `x == y` | 169 / 131 | 2 / 3 | **12 / 7** | 69 / 58 |
| `x < y` | 201 / 152 | 2 / 3 | **17 / 10** | 86 / 68 |
| `x == 0` | 30 / 31 | 4 / 5 | **5 / 4** | 5 / 4 |
| `x > 0` | 41 / 40 | 4 / 5 | **13 / 10** | 14 / 11 |

*Table 1. Instructions per call site, amd64 / arm64: the inline fast paths and the call setup, without the enclosing function's frame.*

## 4. Application benchmarks: inline code against speed

The toolchains of Section 2 are measured on whole applications with the go-decimal128-app-benchmark suite [go-decimal128-app-benchmark]: Go translations of the UW-Madison decimal floating-point application benchmarks [Wang et al. 2007; Anderson et al. 2009] (euro conversion, risk management, three tax forms, banking) and of Cowlishaw's telco benchmark [Cowlishaw telco]. Each program's output is checked byte for byte against the reference output on every run. The baseline is the XOR-BID toolchain the fork started from; UBD is measured at its three levels. The four builds were run interleaved on two machines, an Apple M3 Pro (arm64) and an Intel Core i9-9880H laptop (x86_64), with every function aligned to 64 bytes so that code placement does not differ between builds (November 2026).

Table 2 gives the time of each program's own timed loop on the Apple M3 Pro, in ns per record; lower is better.

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

*Table 2. Compute time on the Apple M3 Pro (arm64), ns per record, with the change against XOR-BID.*

Table 3 gives the size of each program's own machine code on arm64, in KB: its main package and the adapter through which it reaches the decimal type, where the operators are compiled and inlined. The kernel, runtime, and standard library are shared by every program and not counted.

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

*Table 3. Code size on arm64, KB per program, with the change in total against XOR-BID.*

Tables 4 and 5 give the same measurements on the Intel Core i9-9880H. That machine is a laptop, and its run was noisier: several programs' cross-checks of the timed loop against the runner's own clock fell outside their limit, and the slowest samples were often twice the fastest. The fastest sample, which the tables report, is the measure least affected by that noise.

| App | XOR-BID, ns | UBD level 1, ns | **UBD level 2, ns** | UBD level 3, ns |
|---|--:|--:|--:|--:|
| euro | 1,997.7 | 1,942.5 (−2.8%) | **1,913.2 (−4.2%)** | 1,883.4 (−5.7%) |
| risk | 15,723.0 | 18,607.4 (+18.3%) | **16,994.5 (+8.1%)** | 15,505.2 (−1.4%) |
| tax fed | 5,067.7 | 5,612.9 (+10.8%) | **4,952.8 (−2.3%)** | 4,409.5 (−13.0%) |
| tax ca | 1,122.5 | 1,224.3 (+9.1%) | **1,125.6 (+0.3%)** | 1,012.9 (−9.8%) |
| tax nc | 1,754.4 | 1,836.9 (+4.7%) | **1,726.9 (−1.6%)** | 1,628.5 (−7.2%) |
| banking | 1,454.9 | 1,524.6 (+4.8%) | **1,450.4 (−0.3%)** | 1,392.2 (−4.3%) |
| telco | 80.7 | 101.4 (+25.6%) | **77.9 (−3.5%)** | 74.2 (−8.1%) |
| **time vs XOR-BID, geometric mean (%)** | — | **+9.7%** | **−0.6%** | **−7.1%** |

*Table 4. Compute time on the Intel Core i9-9880H (x86_64), ns per record, with the change against XOR-BID.*

| App | XOR-BID, KB | UBD level 1, KB | **UBD level 2, KB** | UBD level 3, KB |
|---|--:|--:|--:|--:|
| euro | 14.1 | 9.4 | **10.1** | 11.6 |
| risk | 36.2 | 12.1 | **14.9** | 24.9 |
| tax fed | 235.3 | 39.9 | **58.7** | 136.1 |
| tax ca | 58.9 | 15.4 | **20.0** | 37.7 |
| tax nc | 96.1 | 19.7 | **27.9** | 59.9 |
| banking | 183.1 | 81.5 | **93.2** | 135.7 |
| telco | 13.5 | 7.3 | **8.0** | 11.2 |
| **total of the seven (KB)** | **637.2 KB** | **185.4 KB (−71%)** | **232.7 KB (−63%)** | **417.2 KB (−35%)** |

*Table 5. Code size on amd64, KB per program, with the change in total against XOR-BID.*

The levels trace a curve of code against speed, the same on both machines. On arm64, level 2 adds 36 KB (+25%) to level 1 and is 12.5% faster on the geometric mean; level 3 adds a further 136 KB (+75%) for a further 7.5%. Level 2 is at most 2.6% slower than XOR-BID on six of the seven programs, and faster on three of them (euro, nc, telco), with 42% of its code; level 3 is faster than XOR-BID on all seven with 73% of its code. On x86_64 the kernel calls cost relatively less: level 1 is 9.7% slower than XOR-BID rather than 15.6%, and level 2 is 0.6% faster on the geometric mean, faster on five of the seven programs and level on a sixth (tax ca, +0.3%), with 37% of its code; level 3 is 7.1% faster with 65%. On both machines the remaining gap at level 2 is risk (+11.2% on arm64, +8.1% on x86_64): about two in five of its additions and subtractions have operands of different exponents or of opposite signs for the operator, money-sized values that nonetheless take the kernel call.

## 5. A kernel change, and two attempts

A kernel change closed one gap without any inline code. Telco's quantize to cents spent its time on a mispredicted branch deciding whether the remainder passed half, not on the division: replacing the division by a reciprocal multiplication made it 3% slower, while computing the rounding decision without a branch took the kernel's word path from 6.5 to 4.3 ns and telco from 36.0 to 31.8 ns per record, level with XOR-BID.

Two attempts to close risk's gap did not succeed. Computing the kernel's word-path addition without branches made risk 4.5% slower: the branches it removed, on which operand is the larger, were predicted much better on risk's data than on random operands. An inline path for operands of either sign took about a third of risk's kernel addition time inline, but grew each `+` and `-` call site from 8 and 14 instructions to 31 and 32 on arm64, and its code cost as much time as the calls it saved.

## 6. Discussion and future work

The levels separate two costs that a library cannot: the code each call site carries, which grows with the number of operators in a program, and the time spent in calls that a larger inline path would have avoided. Level 2 keeps the first small — 37–42% of XOR-BID's application code — while matching XOR-BID's speed on all but one program; level 3 shows how much speed the larger inline paths still buy. The kernel change for quantize shows that some of a gap can be closed in the kernel, at no cost to call sites, once the profile shows where the time goes; the two rejected changes show that a microbenchmark of random operands can mislead where the application's data is more regular.

The application benchmarks favour large inline paths. They date from 2007–2009 and are small programs: each one's hot loop is a few dozen decimal operations, whose code fits in the instruction cache however large its inline paths are, so a larger path saves calls and costs nothing in cache misses. It is not clear that they represent modern financial workloads, such as valuation and pricing models with thousands of distinct operations on the hot path. There, inline code multiplies with the number of operations. From Table 1, a thousand mixed operations on arm64 take about 470 KB of inline code for XOR-BID, 250 KB for UBD level 3, 50 KB for level 2, and 12 KB for level 1. XOR-BID's figure is several times the 32 KB L1 instruction cache of the i9-9880H and the 192 KB of the M3 Pro's performance cores, and adds pressure on the instruction TLB and the branch predictor, while level 2's nearly fits even the smaller cache. Beyond some number of hot operations, level 2 may therefore overtake level 3 and XOR-BID; the benchmarks here are too small to show where.

Two pieces of work remain. One is a benchmark large enough to find that crossover. The other is the additions level 2 sends to the kernel, operands of different exponents or of opposite signs for the operator, which keep risk 8–11% behind XOR-BID; they should be handled without giving up the small call sites that make level 2 worth having.

## 7. Conclusion

Stored as UBD, Go's built-in `decimal128` needs one test — for exponent, sign, coefficient size, and special values — in front of a kernel call to take the common case of addition, subtraction, and comparison inline. With those small paths, seven application benchmarks run within 1.2% of XOR-BID on arm64 and 0.6% ahead of it on x86_64, with 37–42% of its code; with XOR-BID's larger paths moved onto UBD, they run 6–7% faster with 65–73% of XOR-BID's code.

## References

[UBD] "UBD: An Unpacked Binary Decimal Format for Fast Software Decoding of IEEE 754 decimal128." Available: https://migueldecimal128.github.io/decimal128-www/whitepapers/ubd.html

[Go #19787] "proposal: spec: add decimal float types (IEEE 754-2008)," Go issue 19787. Available: https://go.dev/issue/19787

[Cantos decimal] M. Cantos, Go toolchain with predeclared decimal types, branch `decimal` of https://github.com/marcelocantos/go, commit `5032fd77`; proposal and toolchain lock at https://github.com/marcelocantos/go-decimal-proposal

[go-decimal-ubd] The `ubd128` fork of [Cantos decimal], storing `decimal128` as UBD. Available: https://github.com/migueldecimal128/go-decimal-ubd/tree/ubd128 (measured at commit `45ff73c327`)

[Wang et al. 2007] L.-K. Wang, C. Tsen, M. J. Schulte, and D. Jhalani, "Benchmarks and Performance Analysis of Decimal Floating-Point Applications," in *Proc. 25th IEEE International Conference on Computer Design (ICCD)*, October 2007, pp. 164–170.

[Anderson et al. 2009] M. J. Anderson, C. Tsen, L.-K. Wang, K. Compton, and M. J. Schulte, "Performance Analysis of Decimal Floating-Point Libraries and Its Impact on Decimal Hardware and Software Solutions," in *Proc. 27th IEEE International Conference on Computer Design (ICCD)*, October 2009, pp. 465–471.

[go-decimal128-app-benchmark] Go application benchmarks for decimal128 libraries: the UW-Madison decimal floating-point application benchmarks (v1.0) [Wang et al. 2007; Anderson et al. 2009] and Cowlishaw's telco benchmark, with byte-exact output gates and a runner. Available: https://github.com/migueldecimal128/go-decimal128-app-benchmark

[Cowlishaw telco] M. F. Cowlishaw, "The 'telco' benchmark." Available: https://speleotrove.com/decimal/telco.html

</div>
