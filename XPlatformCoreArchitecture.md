# Core Architecture and the Cross-Language Constraint Regime for Multiplatform Decimal128

*First draft*

## 1. Purpose and Scope

This document describes the architecture of a multiplatform IEEE 754-2019 decimal128 library and the deliberate language-constraint regime that governs its core implementations. It covers two tightly related ideas: the separation of a language-neutral *core engine* from language-specific *wrappers*, and the restricted subset of language features the core implementations are permitted to use so that parallel implementations in different languages remain mechanically translatable and mutually verifiable.

It does **not** cover, except by reference, the internal numeric representation (UBD), the full IEEE 754-2019 arithmetic semantics, the DecContext flag- and trap-propagation mechanism, the final name-mangling rules, the primitive arithmetic layer, or the eventual translation tooling. Those are the subjects of companion documents.

## 2. Architectural Overview

### 2.1 Core, Primitive Arithmetic, and Wrapper Layers

The library is split into three layers with a clean division of responsibilities.

The **core** is responsible for the complete implementation of IEEE 754-2019 decimal128. It owns the arithmetic, rounding, encoding, decoding, text parsing and text formatting logic. It does not deal with language-specific features, idioms, or conveniences. 

The **primitive arithmetic** layer provides basic arithmetic functions on unsigned 128-bit and 256-bit integer values. Core uses these functions to perform basic arithmetic on 113-bit decimal128 coefficients. Multiplication of two 113-bit values may produce a 226 bit intermediate result. Fused-multiply-add fma operations require alignment of coefficients in the 256-bit world in order to achieve the single-rounding functionality dictated by the IEEE 754-2019 specification. Addition, subtraction, multiplication and simple division of 128/256-bit values are part of the primitive arithmetic layer. Note that advanced division algorithms for division by powers of 10 are part of the core, not part of the primitive arithmetic layer. 

The **wrapper** provides user-facing functionality. It adapts the core to the characteristics and idioms of its host language — operator overloading, protocol or interface conformance, idiomatic naming, optional/nullable conventions, and so on. The wrapper adapts decimal128 values to be (as near as possible) first-class datatypes of the target language.

This split provides a clean division of responsibilities, isolating the primitive arithmetic layer that must be hand-tuned per platform from the parts that must behave identically everywhere, and makes it possible to verify the numeric engine independently of presentation concerns.

### 2.2 Anticipated Core Implementations

The design explicitly does **not** call for a single implementation in C with interfaces for Java/Kotlin and Swift. Rather the goal is to implement the core in the target language to the largest extent possible. To that end, four core implementations are anticipated:

- Swift
- Kotlin (pure Kotlin Multiplatform)
- C
- Java (pure Java, no JNI)

Each core is an **independent, full implementation** that passes the standard IEEE 754 decimal128 validation suites on its own. They are *not* generated from a single shared source. However, by restricting the set of language features each core uses, the implementations are kept structurally parallel, which facilitates semi-automated translation of modules from one language to the next and lets human and AI maintainers confirm equivalent behavior between parallel function implementations.

### 2.3 Anticipated Wrapper Implementations

The following wrapper implementations are anticipated as architectural goals. Not all are guaranteed to ship to customers; they represent the intended shape of the system.

- swift over swift core
- swift over C core*
- Kotlin Multiplatform over Kotlin Multiplatform core
- Kotlin Multiplatform Native over C core*
- Rust over C core
- Python over C core
- Go over C core
- Scala over Java core

The naming pattern is *wrapper-over-core*. Two of these — swift-over-C and Kotlin/Native-over-C — will be valuable during development of the C core: existing test suites already written in Swift and Kotlin can drive the C core through the wrapper. This is expected to make development and validation of the C core relatively straightforward.

### 2.4 Current State

### 2.4.1 2026-06-01

The C core does not yet exist. 

The Java core does not yet exist. 

The Kotlin Multiplatform KMP implementation was the first decimal128 implementation undertaken. It is written in 100% Kotlin, running on jvm, native, and JavaScript. Unpublished benchmarks (available in the source) demonstrate excellent performance and heap behavior. It is publicly available in pre-release at `decimal128.com` hosted on github. It is fully functional, but does not adhere to the UBD in-memory format or the separation of layers described. The Kotlin KMP implementation will not be officially released until it is reworked to comply with the architecture described herein. 

The existing Swift (v6.3) implementation was based upon the Kotlin KMP experience. The Swift value struct memory model forced a shift in perspective. The availability of intrinsic UInt128 support simplified a number of operations. That simplification brought clarification and insight into improvements for both implementations. The swift implementation also passes the same comprehensive set of IBM/Cowlishaw dectest, IBM FPgen/fptest, and Intel test vectors. 

Both the Kotlin KMP and Swift implementations pass a rigid suite of decimal128 test vectors from 3 different sources: IBM/Cowlishaw dectest, IBM FPgen/fptest, and Intel `libbid` tests. For finite numeric answers, _passing_ means using the specified rounding direction to getting the same bitwise value in the same cohort. For non-finite results it means getting the same Infinity/NaN/sNaN result with the same sign and the same payload. The test vectors have proven exceptionally valuable in validating the existing implementations. Frankly, without the test vectors the ambitious architecture described here would not be possible. Details about the tests and how they are run can be found in an upcoming companion paper.

**Immediate next steps**

The Swift platform is closest to the architecture described here. The Swift platform will be split into the wrapper, core, and primitive arithmetic layers described here. 

Work will begin on separating out the Kotlin KMP primitive arithmetic layer


## 3. The Cross-Language Constraint Regime

### 3.1 Rationale

The core implementations all share the same architecture. But the design goes beyond simply sharing the same algorithms. We strive for consistency in the physical shape of the code across the various implementations. To the extent possible, base file names, function names, function signatures, and textual indentation are exactly the same on all platforms. This provides familiarity and regularity as developers move across platforms. More importantly, it makes it easier for both humans and AI tools to validate correctness across the implementations.

To achieve this goal, we have adopted strict rules on which language features may-or-may-not be used. We will truly lower ourselves to the least common denominator because C is the most primitive of the core implementation languages; Java and Swift are C-family languages; Kotlin is derived from Java. The core implementations restrict their use of Java, Kotlin, and Swift features to those with a direct mapping to C.

This restriction serves two purposes. It makes semi-automated translation between implementations tractable — eventually, the goal is 100% reliable translation, possibly via a tool built on a language with a good parse-tree API such as Swift. It also makes it far easier for human and AI maintainers to confirm correct, equivalent behavior between parallel function implementations, because the implementations look alike.

The term **HLL** (high-level language) is used to mean Swift, Kotlin, and Java collectively. It explicitly *excludes* C, which is treated as a MOHLL machine-oriented-high-level-language.

### 3.2 The Guiding Principle

The constraints bind *shippable core logic only*. They do not bind transient diagnostic code. Debug scaffolding is exempt by category: string interpolation is permitted in debug-print paths for all datatypes including enums, and more broadly any HLL-specific language feature is permitted in dynamic or temporary scaffolding used during development. The boundary is the principle, not an enumerated list of exceptions — the moment code is shippable core logic, the regime applies.

A second guiding principle is that the regime aims for **parallel structure with platform-honest bodies**, not identical source text. Where a language must spell something its own way to be correct (unsigned operations on signed types, native 128-bit arithmetic, value-return versus fill-in), it does so. What stays identical is the structure, the names, and the behavior.

### 3.3 HLL Features Excluded (no direct C mapping)

The HLL cores do not use:

- method dispatch
- overloaded functions
- default parameters
- tagged (named) parameters
- closures
- advanced loop iteration syntax
- switch / multi-way branch statements
- unparenthesized predicates in `if` and `while`
- unblocked (braceless) branches for `if`/`else`/`while`
- higher-level data types
- generics / type parameters
- exceptions (try/catch/throw)
- properties with custom getters/setters (computed properties)
- extension functions / extensions
- operator overloading
- string interpolation (outside debug scaffolding)
- lambdas passed as arguments
- destructuring declarations
- namespace-style singletons (companion/companion-object namespacing)
- heap-allocated memory other than preallocated thread-local temporaries on Kotlin and JVM. ... see below

**Exception:** nullable/optional types are excluded *except* for `DecContext` and `DecTrapHandler`, where optional is permitted.

**Exception:** default parameters are excluded *except* for the compiler-generated source-location parameters (filename, line number) on the verification primitives `verify`, `demand`, and `impossible` — see Section 9.

### 3.4 Features Excluded from Both C and HLL Cores

Neither the C core nor the HLL cores use:

- assignment as an embedded expression
- pre/post increment operators `x++` `--y` ... use `x += 1` `y -= 1`
- bare (braceless) statement as a conditional branch or loop body
- library functions (stdlib, Foundation, etc.)
- multiple declarations per statement
- implicit numeric conversions (every width change is explicit)
- recursion (see exception below)
- `goto`

**Recursion exception:** there is no general use of recursion. Neither Knuth D division nor string formatting recurses. One isolated case — implementation of `remainderTrunc` / `remainderNear` — *may* recurse exactly one level.

### 3.5 HLL Restrict-To List

The HLL cores restrict themselves to:

- static and top-level functions
- ASCII throughout
- C naming conventions for variable and function identifiers
- function naming conventions that give unique signatures to "overloaded" functionality
- primitive integer data types
- arrays of primitive integer data types
- the `while` loop for iteration, using a single `int` loop iterator
- only simple, isolated use of array-fill for initializing arrays in memory
- the `if` statement as the only branching construct (no `switch`)
- isolated use of the ternary conditional (with allowance for `if`-as-expression in Kotlin)
- `String` data types
- simple enum data types whose representation is an `Int`
- one declaration with at most one initialization per line
- braces on every block, always

### 3.6 Conditional expressions

Conditional expressions are intended for simple selection between simple choices. Generally, this is targeted at branchless CMOV conditional move instructions that do not cause a change in control flow. Conditional expressions should not extend beyond one line of source text.

In Swift/Java/C use the `(condition) ? a : b` ternary operator. Kotlin does not have this and is allowed to use `if (condition) a else b` if-expression. In both cases the conditional predicate must be parenthesized. The values may be parenthesized.

We may consider a lambda/closure or macro to encapsulate a conditional expression.

### 3.7 Control-Flow Rules

#### 3.7.1 `if` statements

**`if` statements.** Predicates must be enclosed in parentheses. The `if` and `else` clause bodies must be enclosed in braces. This matches the `while` rule exactly.

#### 3.7.2 `while` loops

**Loops.** The `while` loop is the only looping construct. It is the one form whose syntax and semantics are identical across C, Swift, Kotlin, and Java. Kotlin has no C-style `for` loop, and the `for-in` / range forms diverge across the HLLs, so excluding them removes the principal translation hazard. The cost is mechanical boilerplate, which aids verification rather than harming it.

#### 3.7.3 counted loops

**The counted-loop idiom.** Every counted loop follows a single named idiom so that all counted loops look identical and a reviewer can pattern-match them at a glance: declare an `int` index before the loop, test it in the parenthesized predicate, execute the braced body, and increment the index as the last statement of the body, incrementing as a plain statement using the `+=` assignment operator.

## 4. Data Representation

### 4.1 The Decimal128 Type

`Decimal128` is a separate, immutable type, distinct from the coefficient containers. It has two 64-bit coefficient fields named `ubdHi64` and `ubdLo64`. In Kotlin, `ubdHi64` and `ubdLo64` are `val` properties and in Swift they are `let` properties.

On the JVM, the object's heap layout is: a 12-byte header, a 4-byte `Int` field named `TBD` placed immediately after the header to pad to a 16-byte boundary, and the two 8-byte `Long` fields (`ubdHi64`, `ubdLo64`) — for a total heap allocation of 32 bytes per `Decimal128`. The JVM aligns the `Long` fields to an 8-byte boundary, so `TBD` precedes them. `TBD` is, at present, free space arising from heap-quantum padding; it has several potential uses, all deferred to a future discussion.

### 4.2 The Magnitude Types: U128 and U256

`U128` and `U256` are **pure arithmetic magnitudes**. They carry no role-specific meaning: coefficient, quotient, and intermediate are *roles* layered on top by usage, not subtypes. They are completely distinct from `Decimal128`.

`U128` holds two 64-bit dwords; `U256` holds four. Fields are named `dw0`, `dw1`, `dw2`, `dw3`, with `dw0` least significant.

The representation is structurally identical across all four cores:

- **C and Swift:** a `struct` of dwords.
- **Java and Kotlin:** a mutable `class` of dwords.

Native 128-bit machine types (`UInt128` in Swift, `unsigned __int128` in C) appear **only inside the bodies of arithmetic primitives**, never in the type's public shape. Parameters are passed as the individual dword fields (`.dw0`, `.dw1`, …). On Swift, packing dwords into a native `UInt128` and unpacking the result has been observed to compile to zero runtime cost under LLVM; the same fusion is expected from C compilers.

There is no inheritance among these or any other core types. All core classes are `final` classes.

### 4.3 Dword Signedness

All dwords are **signed 64-bit integers** on every core: `long` on Java, `Long` on Kotlin, `Int64` on Swift and `int64_t` on C.

Java has no unsigned 64-bit primitive, so it must use signed `Long`. Kotlin follows Java and uses signed primitive integers; its unsigned wrapper types are avoided in the core because they have been observed to generate poor/noisy JVM bytecode. Swift and C *could* use unsigned dwords, but signed dwords were chosen across the board for full type-level uniformity. Because the dwords are bit-buckets and signedness is a source-level interpretation, this carries **zero runtime cost** on Swift and C given correct field ordering. The only consequence is explicit source-level casting to unsigned within the arithmetic primitives where unsigned semantics matter (comparison, right shift, division, high-word checks) — a cost confined to the hand-written primitive layer that already receives per-platform care.

Kotlin and Java are prohibited from using boxed integer types. See Heap Memory Usage below.

### 4.4 Int usage

Int values are used for in-memory values. The most common example in the core is the qExp quantum exponent. After extraction from the top of ubdHi64 qExp values are passed around as Int/int. The size of an Int/int is not the same on all platforms. Core developers are cautioned. The qExp value range required by decimal128 is small (it fits comfortably within a few decimal digits), so it is always safely within the range of a 32-bit two's-complement integer; the cross-platform width difference is therefore benign for qExp and for the other small in-memory Int values the core passes around.

#### 4.4.1 Int on Kotlin and Java

Kotlin and Java pre-define the size of an Int/int to be 32-bit two's-complement. No further discussion required.

#### 4.4.2 Int on Swift

We target modern machines. We flatly/boldly assume Int to be 64 bits two's-complement on Swift.

#### 4.4.3 Int on C

We will probably use `int32_t` on C. TBD.

### 4.5 Boolean usage and Bool/Int conversion

We assume a boolean/Boolean/Bool type on all platforms.

Converting between a Bool and a 0/1 integer is common, and in the current code it is the principal source of conditional expressions such as `(signFlag) ? 1 : 0` or `if (signFlag) 1 else 0`. To standardize the look of these conversions and eliminate most of those conditional expressions, the core defines a small family of named conversion functions with identical names and behavior across all four cores. Naming the operation lets each platform emit its best branchless lowering without the source appearing to branch.

The sign concept has three representations, named so that each carries its representation in the name:

- `signFlag` — `false`/`true` (Bool)
- `signBit` — `0`/`1` (Int)
- `signMask` — `0`/`-1` (Int, all-ones when negative)

`signFlag` is the committed term for the boolean sign throughout the core; the bare term `sign` is not used.

The core-wide conversion functions are:

- `signBitOf(signFlag)` — Bool → Int `0`/`1`.
- `signFlagOf(signBit)` — Int → Bool, with `!= 0` behavior and no assertion (core flags are known to be 0/1, and this has not been a problem in practice).
- `signMaskOf(signBit)` — Int `0`/`1` → Int `0`/`-1`, implemented branchlessly as `-signBit`.

These three are identical in name and behavior on all four cores.

A separate Bool → 64-bit conversion, `carryBitOf(carryFlag)`, returns a 64-bit `0`/`1` and is used only when synthesizing multi-limb arithmetic by hand. It is **not** a core-wide function: it lives in the primitive arithmetic layer (Section 4.6), follows that layer's local type conventions rather than the signed-dword core rule, and is expected to be absent on platforms whose native types provide carry directly — for example Swift, which obtains carry and full-width products from `UInt128` operations.

### 4.6 Native 128-bit Usage Summary and the Primitive Arithmetic Layer

After the memory model, the use of native 128-bit types is the largest sanctioned divergence. It is confined to the bodies of arithmetic primitives. Swift and C are encouraged to use native 128-bit arithmetic there; Java and Kotlin synthesize the same results from signed `Long` pairs (and quads for 256-bit) using unsigned-operation helpers.

These primitives belong to a distinct **primitive 128/256 arithmetic layer** that presents a uniform API — the same function names and signatures — across all four cores, while the implementations are entirely hand-written per platform. This is the one layer where the bodies are *expected* to differ, and where the constraint regime deliberately relaxes: native 128-bit types, explicit unsigned casts, and local helpers such as `carryBitOf` (Section 4.5) live here. The design of this layer — its full API, the per-platform implementations, carry/borrow handling, and Knuth D — is the subject of a separate companion whitepaper and is out of scope here.

### 4.7 Heap Memory Usage Ban

#### 4.7.1 DecContext

The `DecContext` object provides an IEEE 754 compliant method of capturing stateful `DecFlags` status flags and user-settable `DecTrapHandler` functions for notification of signaled exception conditions (in IEEE 754 terminology). These are heap-allocated objects that are only created when a user specifically requests them. The following ban on heap allocation does not apply to `DecContext` and friends.

#### 4.7.2 Swift and C heap memory ban

Swift and C are not allowed to allocate heap memory. An `AsciiPrintBuffer` struct of fixed size 64-bytes can be allocated on the stack and passed by inout/reference. All other core struct datatypes can be passed in registers as parameters and return types.

The existing Swift implementation passes all tests while performing no heap allocation.

#### 4.7.3 Kotlin and Java heap memory restrictions

Kotlin and Java must allocate Decimal128 objects from the heap as return values. This is a fundamental design of the language architecture and is unavoidable.

A set of pre-allocated `U128/U256/AsciiPrintBuffer/KnuthDTemp` objects are accessible thru a `DecPrefs` temporary that is ThreadLocal. These mutable shared temp objects are used by different core operator implementation functions. This prevents heap allocation and keeps the temps hot in the CPU cache.

Core functions that require temporary space are allowed to perform one ThreadLocal lookup to obtain the DecTmps object. They may use tmp instances for the duration of their computation.

The existing Kotlin implementation passes all basic arithmetic operations and `pown(int)` while allocating at most 32 bytes per operation, as demonstrated by the jmh benchmarking harness. (See anticipated companion paper)

## 5. Calling Conventions and Multi-Value Return

### 5.1 The Asymmetry

C returns a single value. Several core operations must return more than one value — most importantly, division by powers of ten returns a quotient together with a `Residue`. This is handled by a small set of small aggregate result types, with a deliberate, well-localized divergence in *how* they are returned:

- **Swift and C** generally return the result aggregate struct **by value** in registers (an `inout` reference may occasionally be necessary).
- **Java and Kotlin** pass a **caller-owned mutable instance** that the called function fills in. These instances are generally drawn from a thread-local pool of reused temporaries and generally do not allocate from the heap. See 4.7.3.

The translation rule is mechanical: *value-return* on Swift/C corresponds to *fill the caller's instance* on Java/Kotlin. The function logic stays parallel; only the signature and the return mechanism differ.

Where the fill-in convention applies, the destination parameter comes **first** and scratch/context parameters come **last**: `op(result, operand…, scratch/ctx…)` (settled June 2026 with the primitive-layer companion). Destination-first keeps the operands positionally identical to the Swift/C value-return line (`let z = op(x, y)` ↔ `op(z, x, y)`) and holds the destination at position 0 under varying operand arity.

### 5.2 Quot128Residue

The division result type for the `div_pow10_*` family is `Quot128Residue`. It pairs a 128-bit quotient magnitude with the `residue` that categorizes the lost digits that represent the digits that were shifted out to the right ... the remainder.

- On Swift and C it is a `struct` returned by value.
- On Java and Kotlin it is a mutable `class` filled in from the thread-local pool.

The residue lives as its own field within the `Quot128Residue` result type. On Swift/C it comes after dw1/dw0. On Kotlin/Java it comes before dw1 dw0 because of the 12-byte object header and alignment issues. Otherwise, the behavior is identical on all platforms, and only the ownership and return mechanics differ.

## 6. Enumerations

### 6.1 Core Enums Are Distinct from User-Facing Enums

Core enum types are kept completely distinct from the user-facing enum types. The two have different obligations. The user-facing enum is a stable API contract with idiomatic, documented names. The core enum is an implementation detail whose integer values are load-bearing — internal tables depend on the ordering. Keeping them separate prevents a user-facing rename or reorder from silently corrupting core tables. At the wrapper/core boundary these values cross either as the core enum type or as an `Int`; `Int` is the representation all four cores share trivially.

### 6.2 Enum Naming and Capitalization

All core implementations use `SCREAMING_SNAKE_CASE` for enum value names, which reads naturally for C, Java, and Kotlin and signals that the names map to fixed integer values. User-facing enums default to `camelCase` across platforms for cross-platform consistency, with (reluctant) willingness to defer to a language style guide if language-zealots go to the pitchforks.

### 6.3 Enum Representation per Language

The goal is integer performance with as much compile-time type safety as each language affords. This lands differently per language and is itself a sanctioned divergence:

- **Swift and Kotlin:** a value class wrapping the `Int` — zero overhead, full type checking, and natural support for bit-manipulation methods. Retained.
- **C:** `enum` for the named constants. C enums are weakly typed (they convert freely to and from `int`), so they provide names but little safety; bit-manipulation is done on the integer value regardless.
- **Java core:** `static final int` constants — honest about what they are, zero overhead, and exactly what the bit-manipulation needs. A real Java `enum` is rejected for core use because it is a heap object, violating the no-heap / no-boxing rule and defeating the bit-manipulation story. Narrowing to `byte`/`short` is rejected because it creates no distinct type and only adds widening noise. A real Java `enum` remains a candidate for the *user-facing* layer, where idiom outweighs the no-heap rule.

So the pattern is: the core pays for performance with weaker typing; the wrapper recovers idiom and safety at the boundary. The same conceptual enum appears as value-class-over-Int (Swift/Kotlin), `enum` (C, names only), and `static final int` (Java core) — one integer semantics, several type-safety levels.

### 6.4 The Primary Enum Types

**Residue** (internal, not visible to the wrapper; per the companion whitepaper's D17 it is a 2-bit Int defined at the primitive layer rather than an enum — Java cannot express a zero-cost wrapper, so no core wraps it) has four values, encoded so that bit 1 is the rounding bit and bit 0 is the sticky bit:

- `EXACT   = 0` (0b00)
- `LT_HALF = 1` (0b01)
- `HALF    = 2` (0b10)
- `GT_HALF = 3` (0b11)

**Rounding** (user-facing, with distinct wrapper and core implementations) enumerates the five IEEE 754 rounding directions. Because it crosses the wrapper/core boundary it exists in both forms described in 6.3: an idiomatic user-facing enum in the wrapper and a load-bearing integer form in the core. Internal tables depend on this ordering:

- `TIES_TO_EVEN    = 0`
- `TIES_TO_AWAY    = 1`
- `TOWARD_ZERO     = 2`
- `TOWARD_POSITIVE = 3`
- `TOWARD_NEGATIVE = 4`

**FormatStyle** (user-facing, with distinct wrapper and core implementations) has four values; like `Rounding`, it exists in both the wrapper and core forms described in 6.3. The first three are required for IEEE 754-2019 compliance:

- `AUTO`
- `EXPONENTIAL`
- `ENGINEERING`
- `COEFFICIENT_QEXP` (under consideration; retained for now)

## 7. Interchange Formats

The core operates entirely in the library's internal UBD representation. The two IEEE 754 interchange formats, DPD128 and BID128, are handled as **boundary concerns**: static conversions to and from UBD. The core never carries a DPD or BID value through its logic — conversion happens only at the edges. (Details of the UBD representation are covered in the publication paper and are out of scope here.)

## 8. Function Naming

Function names are **identical across all four cores**. Only signatures diverge, and only where the value-return-versus-fill-in rule or the type-representation rules force it.

Because C has no overloading, a manual name-mangling scheme provides unique names for what would otherwise be overloaded functionality. The scheme is codified (June 2026, settled during the primitive-layer specification — see the companion whitepaper):

```
name      ::= op '_' result '_' operands { '_' qualifier }
operands  ::= width ('x' width)*
result    ::= width | aggregate segment
```

**The result segment leads.** Name order then mirrors call-site order on every platform: `let q = divPow10_q128res_256(x, k)` on Swift/C and `divPow10_q128res_256(q, x, k)` under the Java/Kotlin fill-in convention (Section 5.1) both put the result leftmost. Result aggregates use terse segments: `q128res` (Quot128Residue), `q256r64` (Quot256Rem64), `d256swap` (Diff256Swap).

- **Width segments** (`64`, `128`, `256`) name the operand widths in declaration order, subsuming the earlier free-floating `_128`/`_256` suffixes.
- **Operands implied by the op are not spelled**: the power-of-ten exponent in `mulPow10`/`divPow10` names, an Int shift count.
- **Qualifiers trail**: `_tte` ties-to-even, `_rnd` a rounding-direction parameter, `_ctx` a required `DecContext`, `_ctxnull` an optional/nullable `DecContext`, and algorithm markers (`_barrett`, `_knuth`) where one contract has strategy-split implementations.

`_ctxnull` resolves the earlier problem of `_ctx` doing double duty: `_ctx` always means a required `DecContext` parameter; `_ctxnull` is officially the optional/nullable variant.

The core's division-by-powers-of-ten family illustrates the grammar: `divPow10_q128res_*`, e.g. `divPow10_q128res_256_barrett` (today's `div_256_pow10_q128res_barrett`, which carries its result segment in third position and reorders when touched).

Base op names are `camelCase`; result, operand, and qualifier segments are digits and lower case, separated by underbars. The tier-0 scalar primitives originally carried inline widths without segments (`unsignedMul64Hi64`, `clz64`); the companion whitepaper's D11 folds them into the grammar (`umulHi_64_64x64`, `clz_int_64`), with a `u` op prefix marking unsigned semantics at the dword width.

Still open: whether the qualifier set is closed, and the spelling of scalar result segments (`int`, `bool`) — tracked in Section 11.

## 9. Error Handling

The core uses **no exception or error-handling mechanism**. IEEE conditions are reported thru the return value and optionally thru status flags carried in `DecContext` (the propagation mechanism is the subject of a companion document). For internal state verification there are three distinct, deliberately separated mechanisms.

All three of these primitives accept compiler-generated source-location parameters — filename and line number — defaulted to the call site. This is the regime's one sanctioned exception to the default-parameter prohibition (Section 3.3): the location is supplied by each platform's native mechanism (Swift `#file`/`#line`, C's `__FILE__`/`__LINE__` macros, the JVM equivalents) and has no portable spelling as an ordinary argument, so defaulting it is unavoidable. The exception is scoped to location only — the `String` message parameter remains mandatory and non-defaulted (Sections 9.2, 9.3).

### 9.1 verify — compile-time-gated state assertion

`verify` asserts internal state during development and is compiled out completely in production. It takes a condition (today, a `() -> Bool` closure on Swift and Kotlin) and is gated on a compile-time flag.

- **Kotlin:** an inline function taking a `() -> Boolean` block, gated on a `const` boolean, calling `check`.
- **Swift:** an `@inlinable @inline(__always)` function taking a `() -> Bool`, compiled under `#if VERIFY_ENABLED`, calling `precondition`.
- **Java (to port):** a `BooleanSupplier` lambda gated on a `static final boolean`, so the JIT eliminates it when disabled.
- **C:** a parenthesized macro rather than a brace closure, expanding to a check under a `VERIFY_ENABLED` guard and to nothing otherwise.

The closure-versus-macro difference is a sanctioned, localized divergence. `verify` is essential for robust development and error catching and is one of the most important tools in the codebase. Use it early and often.

### 9.2 demand — production runtime guard

`demand` is a runtime precondition that **survives into production**. It evaluates a condition and, on failure, routes through `impossible`. It takes a mandatory `String` message; the empty string `""` is the legal way to omit a message (this avoids defaulting the message, which the regime still prohibits — only the source-location parameters are exempt, per the note opening Section 9).

The contract is exactly: `demand(cond, msg)` is equivalent to `if (!cond) { impossible(msg) }`.

The name `demand` was chosen over `require` precisely because it stands alone: `require` already exists in the Kotlin standard library with a different contract (it throws a catchable `IllegalArgumentException` for argument validation), so reusing the name would read as familiar while behaving differently, and it would masquerade as stdlib on Kotlin while being an obvious invention everywhere else. `demand` is uniformly the library's own word on all four platforms.

### 9.3 impossible — production unconditional abort

`impossible` is an unconditional runtime abort for unreachable code, taking a mandatory `String` message (`""` permitted). It is the single termination primitive that `demand` funnels through. On Swift it returns `Never` and calls `fatalError`; Kotlin and Java do not return normally (throw / error); C uses a `noreturn` attribute and aborts. The non-returning contract is identical; only the spelling of "does not return" diverges per platform.

### 9.4 Debugging

During debugging, plain `print` / `println` statements are used freely. As with all debug scaffolding, any language feature is fair game in transient diagnostic code.

## 10. Sanctioned Divergences

These are the points where the four cores do **not** translate purely mechanically. Each is deliberate, localized, and documented. Everything outside this list is intended to be structurally parallel across all four cores.

1. **Memory model.** C and Swift use `struct`; Java and Kotlin use `class`. This is the largest divergence and drives several of the others.
2. **Value-return versus fill-in.** Swift and C return small result aggregates by value; Java and Kotlin fill a caller-owned mutable instance drawn from a thread-local pool.
3. **Native 128-bit arithmetic.** Confined to the bodies of arithmetic primitives. Swift and C use native 128-bit types; Java and Kotlin synthesize results from signed `Long` pairs/quads. The U128/U256 *type shape* is identical everywhere; only the primitive bodies differ.
4. **Signed-dword casting.** All cores use signed dwords, so Swift and C cast to unsigned within arithmetic primitive bodies where unsigned semantics are required.
5. **Enum representation.** Value-class-over-Int (Swift/Kotlin), `enum` for names only (C), `static final int` (Java core). Identical integer semantics, differing type safety.
6. **`verify` form.** Closure/lambda on the HLLs, parenthesized macro on C; compiled out in production everywhere.
7. **`impossible` non-return spelling.** `-> Never` on Swift; throw/error on Java and Kotlin; `noreturn` attribute on C.

## 11. Open Items

The following are explicitly unresolved and are tracked for future work:

- Naming leftovers (Section 8): whether the qualifier set is closed, and confirmation of the scalar result segments (`int`, `bool`). The segment grammar, result-first ordering, and the `_ctxnull` token are settled.
- The `DecContext` status-flag and `DecTrapHandler` trap-propagation mechanism — wrapper-facing and substantial enough to warrant its own document.
- The use(s) of the free `Int` field (`TBD`) in `Decimal128`.
- The fate of `FormatStyle.COEFFICIENT_QEXP`.
- The design and construction of the semi-automated translation tooling (likely parse-tree-driven, with Swift as a candidate source language).
- Production messaging for `demand` / `impossible` (messages omitted by default today; platform location reporting suffices during development).
- The C `int` width decision (`int32_t` versus other), Section 4.4.3.
- The primitive 128/256 arithmetic layer — its uniform API and per-platform hand-written implementations — to be specified in a separate companion whitepaper (Section 4.6).

---

*End of first draft.*