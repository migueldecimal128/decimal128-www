---
layout: default
permalink: /whitepapers/rounding-receiver.html
title: "Rounding as a Receiver: Explicit Rounding Control for Decimal Arithmetic in Concurrent Programs — Decimal128"
description: "Why the rounding direction of a decimal operation belongs at the point where the operation is written, carried as the receiver of the operation, rather than in ambient per-thread state."
heading: "Rounding as a Receiver (Explicit Rounding Control for Decimal Arithmetic in Concurrent Programs)"
---

<div class="whitepaper" markdown="1">

<div class="whitepaper-abstract" markdown="1">

**Abstract.** The rounding direction of a decimal operation should be chosen by the programmer at the point where the operation is written, and carried there explicitly as the receiver of the operation: `towardZero.multiply(price, rate)` rather than `price * rate` under a mode set somewhere else. For historical reasons, most decimal floating-point environments do the opposite. They treat the rounding direction as ambient state, modeled on the control register of binary floating-point hardware: a library or thread-local variable that every operation silently reads. That model dates from single-threaded programs on processors with one floating-point control word. It does not survive thread pools, coroutines, async/await or Go's goroutines, where the code that sets a mode and the code that depends on it routinely run on different threads, or the same thread interleaved with unrelated work. This paper separates what IEEE 754 actually requires (a rounding-direction *attribute* for a block of code) from how it came to be implemented (mutable per-thread state), compares three placements for the mode (ambient, parameter and receiver), and argues for the receiver. The model ships in Decimal128 by Miguel, for Swift, Kotlin, Java, Rust, Go, C#, Zig and Python, with C exposing the equivalent flattened form.

**Keywords:** decimal floating-point, IEEE 754, decimal128, rounding direction, floating-point environment, concurrency, coroutines, API design.

**Terminology.** Rounding directions in this paper are named exactly as IEEE 754-2019 names its rounding-direction attributes: `roundTiesToEven`, `roundTiesToAway`, `roundTowardPositive`, `roundTowardNegative` and `roundTowardZero` [IEEE 754-2019]. Informal names such as "half-up", "banker's rounding", "ceiling" or "truncation" vary between languages and libraries, and are used here only where a quoted rule or an operation's own name requires them.

</div>

---

## 1. Introduction

In decimal arithmetic the rounding direction is part of the program's meaning, not a numerical nicety. A tax authority may require that a computed levy be rounded to the cent under `roundTiesToAway` or `roundTowardPositive`. Legislation or accounting principles may require that a bank round interest owed to the customer under `roundTowardNegative` and interest owed by the customer under `roundTowardPositive`. An interval computation needs its lower bound rounded under `roundTowardNegative` and its upper bound under `roundTowardPositive`, in the same expression. Each of these is a business or correctness rule, and each belongs to a specific operation in a specific place in the source code.

IEEE 754 recognizes this. It defines five rounding directions, requires that a program be able to choose among them, and specifies how the chosen one is applied: "every operation shall be performed as if it first produced an intermediate result correct to infinite precision and with unbounded range, and then rounded that result according to one of the attributes in this clause" [IEEE 754-2019 §4.3]. One exact result, rounded once, in the chosen direction. What it leaves to languages is *how* the choice is expressed. 

The dominant answer, inherited from floating-point hardware, long predating IEEE 754, and codified in C's `<fenv.h>`, is a *dynamic mode*: a piece of state that every subsequent operation reads implicitly until someone changes it. Decimal libraries, which have no hardware register to mirror, mostly copied this model.

A dynamic mode is a global variable with a narrower scope. It carries the usual costs of a global variable: the meaning of `a * b` depends on code that is not on the screen. Those costs were tolerable when one program ran one thread of control from start to finish. They are not tolerable now. Modern code runs on thread pools, schedules continuations onto whichever worker is free, and in languages such as Go multiplexes hundreds of thousands of goroutines onto a handful of operating-system threads. In these settings "the current rounding mode" is either undefined, defined for the wrong unit of work, or defined correctly only because every library on the call path cooperated.

This paper argues for a different placement, a placement that is still compliant with IEEE 754. The rounding direction should be an explicit value, chosen where the operation is written, and supplied as the *receiver* of the operation:

```go
lower := decimal128.TowardNegative.Quo(a, b)
upper := decimal128.TowardPositive.Quo(a, b)
```

There is nothing to set and nothing to restore. The two lines can run in either order, on any thread, in any goroutine, and their results are fixed by what is written.

The contributions of this paper are:

1. **A separation of requirement from mechanism.** IEEE 754 requires a rounding-direction *attribute* for a block of code; it does not require global or per-thread mutable state. Section 2 traces how the second came to stand in for the first.
2. **An analysis of why ambient rounding state fails** under modern concurrency models: threads, thread pools, coroutines, async/await and goroutines (Section 3).
3. **A comparison of three placements** for the rounding mode: ambient, parameter and receiver (Section 4).
4. **The receiver model**, in which bare arithmetic always rounds under `roundTiesToEven`, a `Rounding` value hosts directed arithmetic, and a `DecimalContext` value hosts arithmetic that also records exception flags (Section 5). The model ships across Decimal128 by Miguel.

## 2. Background

### 2.1 What IEEE 754 requires

IEEE 754-2019 defines five rounding-direction attributes: `roundTiesToEven`, `roundTiesToAway`, `roundTowardZero`, `roundTowardPositive` and `roundTowardNegative`. `roundTiesToEven` is the default for decimal results.

Some languages offer more than these five rounding directions. Java's `RoundingMode`, co-authored by Cowlishaw and drawn from the General Decimal Arithmetic Specification [Cowlishaw 2009], is a superset: `HALF_EVEN`, `HALF_UP`, `DOWN`, `CEILING` and `FLOOR` correspond to the five IEEE 754-2019 attributes, while `UP`, `HALF_DOWN` and `UNNECESSARY` have no IEEE 754 counterpart [JDK-8240624]. Python's `decimal` module, also built on GDAS, offers all eight GDAS modes: the same five IEEE 754 equivalents (`ROUND_HALF_EVEN`, the default, `ROUND_HALF_UP`, `ROUND_DOWN`, `ROUND_CEILING`, `ROUND_FLOOR`) plus `ROUND_UP`, `ROUND_HALF_DOWN` and `ROUND_05UP` [PEP 327]. The order of events explains the difference: GDAS, available in draft form by 2000, predates IEEE 754-2008 and was the basis for its decimal arithmetic. Java 5 and Python 2.4 both adopted GDAS rounding modes in 2004, four years before IEEE 754 standardized decimal floating-point. The IEEE 754 attributes are the subset of that earlier vocabulary that the standard chose to require.

The word the standard uses is *attribute*, and it attaches attributes to blocks of program text, not to processors or threads: "An attribute is logically associated with a program block to modify its numerical and exception semantics" [IEEE 754-2019 §4.1]. Rounding direction is the first attribute that language standards "shall specify", and the standard describes its effect in terms this paper takes literally: such attributes "have the effect of an implicit parameter to most individual operations." The requirement is to set that parameter in program text. The implementation "shall provide language-defined means, such as compiler directives, to specify a constant value for the attribute parameter for the operations in a block; the scope of the attribute value is the block with which it is associated" [IEEE 754-2019 §4.1]. How large a block is, the standard leaves to the language: "Language standards might provide means for users to specify attributes for blocks of varying scopes, even as large as an entire program and as small as a single operation" [IEEE 754-2019 §2.1]. Dynamic modes, whose value "might not be known until program execution", come second: attributes "shall be supported with the constant specification of 4.1", while language standards "should also support dynamic-mode specification", "particularly to support debugging" [IEEE 754-2019 §4.2]. The standard is also explicit that it "does not specify the underlying implementation mechanisms for constant attributes or dynamic modes." The receiver model makes the standard's implicit parameter explicit.

A constant attribute is a property of the source code. A dynamic attribute is a property of the execution. Everything that follows turns on the difference.

### 2.2 How the dynamic mode became ambient state

The floating-point units that IEEE 754 grew up alongside selected rounding through a control register. An instruction did not name its rounding direction; it read it from the register. Patent literature from the period describes this directly: with dynamic rounding control the mode is the value of bits in a control register, and some processors offered only dynamic control [US 6,058,410]. The x87 control word, and later SSE's `MXCSR` and AArch64's `FPCR`, all work this way.

C standardized access to that register through `<fenv.h>`: `fesetround` writes the mode, `fegetround` reads it. When C11 and C++11 added threads, they had to say whose register this was. The answer was that the floating-point environment has *thread storage duration*: each thread has its own, and a new thread starts with a copy of its creator's [ISO C11 §7.6; C++ cfenv].

So the language-level realization of IEEE 754's dynamic attribute is a mutable, per-thread variable that every floating-point operation reads. Programmers usually call it "the global rounding mode", and for a single-threaded program that is exactly what it is.

### 2.3 How decimal libraries inherited it

Decimal arithmetic on x86 and ARM is (unfortunately) done in software, so there is no register to mirror. Libraries nevertheless reproduced the model, sometimes as an option and sometimes as the only option:

| Library | Where the rounding mode lives |
|---|---|
| Intel Decimal Floating-Point Math Library (libbid) | Build-time choice: a function argument, or with `DECIMAL_GLOBAL_ROUNDING=1` a global variable `_IDEC_glbround` [Intel libbid README]. GCC's copy marks that global thread-local [GCC libbid]. |
| Boost.Decimal | A library-global mode set with `boost::decimal::fesetround`; its documentation notes that, unlike the Intel library, functions do not take a rounding argument [Boost.Decimal]. |
| Python `decimal` | A current context returned by `getcontext()`, originally thread-local, now a context variable [PEP 567]. |
| Java `BigDecimal` | An immutable `MathContext` passed as an argument [Java MathContext]. |
| decNumber, libmpdec | A context structure passed by pointer to each operation. |

The last two rows show that an explicit alternative has existed for decades. The rest of this paper explains why it should be the norm, and why the receiver is a better spelling of it than the parameter.

## 3. Why Ambient Rounding Fails

Ambient rounding state fails because the unit that owns the state (an OS thread) is no longer the unit that does the work (a request, a task, a coroutine). The failures below get worse in that order. IEEE 754 itself does not resolve them: the effect of changing a dynamic-mode variable "in an asynchronous event, such as in another thread or signal handler" is left for each language to define [IEEE 754-2019 §4.2].

### 3.1 Action at a distance, even with one thread

With a dynamic mode, the meaning of `total = price * qty` cannot be read off the line. It depends on the last `fesetround` executed before it, which may be in a caller, a callback, or a library the author never opened. Every library routine that needs a particular direction must save the mode, set it, compute, and restore it on every exit path, including exceptions. Every routine that needs the *default* must either do the same or trust that nobody upstream left the mode changed.

The rounding direction also becomes invisible to review. A reviewer looking at a diff that adds `price * qty` cannot tell whether it rounds under `roundTiesToEven` or `roundTowardZero` without reconstructing the dynamic call path that reaches it.

### 3.2 Threads and thread pools

Making the environment thread-local (Section 2.2) removed data races on the mode itself. It did not make the mode follow the work. In a thread pool, a worker thread runs task A, then task B. If task A sets the rounding direction and fails to restore it, task B silently runs under A's mode. If task B expects a mode set by the code that *submitted* it, it does not get it, because submission happened on a different thread. Java programmers know this as the `ThreadLocal` problem: a value one task stores in a `ThreadLocal` stays on the pooled thread until something removes it, and the JDK itself warns that such values can leak into unrelated tasks [JEP 506]. Java's decimal type was never exposed to it, because `BigDecimal` takes its `MathContext` explicitly.

### 3.3 Coroutines, async/await and goroutines

Lightweight concurrency breaks the remaining assumption, that one unit of work runs on one thread.

- **One task, many threads.** In Kotlin, Swift and C#, a coroutine or async method that suspends can resume on a different worker thread. A dynamic mode set before an `await` is not, in general, the mode in effect after it.
- **No local storage at all.** Go multiplexes goroutines onto OS threads and deliberately offers no goroutine-local storage or goroutine IDs. The Go team's stated reason is that a single task is routinely spread across many goroutines, so any per-goroutine state is the wrong abstraction; context is passed explicitly instead [Go FAQ; golang/go#22770].

In each case the runtime would need to capture, propagate and restore the rounding mode at every suspension point for the dynamic model to remain correct. Go has explicitly declined to. A decimal library cannot supply it on the runtime's behalf.

### 3.4 Optimizers assume the default

Compilers also prefer the mode to be fixed. Unless `#pragma STDC FENV_ACCESS ON` is in effect, a C implementation may assume the floating-point control modes are the defaults [cppreference fenv]. Constant folding, code motion and common-subexpression elimination are all valid only under that assumption. Dynamic rounding is therefore not merely invisible to people; it is invisible to the optimizer unless the programmer explicitly turns optimizations off.

### 3.5 Testing

A function whose result depends on ambient state is not a function of its arguments. Its tests must set up the state, and its results in production depend on state its tests did not set. A test suite that runs tests in parallel, which most modern test runners do by default, inherits all of the problems in Sections 3.2 and 3.3.

## 4. Three Placements for the Rounding Mode

There are three places an API can put the rounding direction. Only the ambient placement is unsafe under concurrency; between the two explicit placements, the receiver is the better design.

**Ambient.** The mode is state read implicitly by every operation: a control register, a thread-local, a library global, or a context variable.

```c
fesetround(FE_DOWNWARD);   /* somewhere */
z = x * y;                 /* somewhere else */
```

**Parameter.** The mode is an argument of the operation, usually trailing and often optional.

```java
BigDecimal z = x.multiply(y, MathContext.DECIMAL128);
```

**Receiver.** The mode is the object the operation is invoked on, and the operands are the arguments.

```swift
let z = Rounding.towardNegative.multiply(x, y)
```

| Property | Ambient | Parameter | Receiver |
|---|---|---|---|
| Direction visible at the call site | No | Yes, after the operands | Yes, before the operands |
| Result depends only on the written arguments | No | Yes | Yes |
| Safe across threads, pools, coroutines, goroutines | Only with runtime propagation | Yes | Yes |
| Save/restore discipline required | Yes, on every exit path | No | No |
| Can be silently omitted | Always: the operation reads whatever is set | When the parameter is optional or overloaded | No: there is no call without it |
| Groups directed operations for discovery | No | No: spread across the value type | Yes: all on `Rounding` / `DecimalContext` |
| Cost per operation | A register or thread-local read | Pass an argument | Pass the receiver |

The parameter and receiver placements carry exactly the same information. In compiled form they are the same call: `ctx.add(a, b)` and C's `d128_add_ctx(a, b, ctx)` pass the same tuple. The differences are in how the code reads and how the API is used, and Section 5 argues those differences matter.

## 5. Rounding as a Receiver

### 5.1 The model

Decimal128 by Miguel splits arithmetic into three tiers, distinguished by *where* the operation lives rather than by an argument:

| Tier | Lives on | Rounds | Records flags | Example (Swift) |
|---|---|---|---|---|
| Bare | `Decimal128` | `roundTiesToEven`, always | No | `a + b`, `a.squareRoot()` |
| Directed | `Rounding` | In the receiver's direction | No | `Rounding.towardZero.add(a, b)` |
| Context | `DecimalContext` | In the context's direction | Yes, into the context | `ctx.add(a, b)` |

The rule that holds the design together is simple: **no operation takes a rounding mode or context as a parameter.** Every operation either names its rounding direction through its receiver, or uses `roundTiesToEven`, the IEEE 754 default. There is no third case, in which the rounding direction comes from somewhere the reader cannot see.

Bare arithmetic never consults hidden state. `a + b` means `roundTiesToEven` in every thread, coroutine and goroutine, which is what lets operators exist at all without reintroducing an ambient mode.

### 5.2 Why the receiver, not a parameter

A parameter already removes the ambient state. The receiver goes further in four ways.

1. **It reads as the rule it implements.** `Rounding.towardNegative.quantized(interest, to: cent)` reads left to right as the business rule: `roundTowardNegative`, this amount, to the cent. A trailing parameter puts the rule last, after the reader has already formed an expectation from the operands.
2. **It cannot be left out.** A parameter invites a default value or an overload without it, and the default silently becomes an implicit mode again. A directed operation spelled on `Rounding` has no form without a direction.
3. **The type documents which operations round.** Autocompletion on `Rounding.towardZero.` lists exactly the operations whose result depends on a direction. `minimum`, `maximum` and the comparisons select or compare rather than round, so they are absent from `Rounding` and appear only on `DecimalContext`, where they can still raise invalid-operation. The API surface itself states the semantics.
4. **It is spelled the same in every language.** Go has no default arguments or overloading, Java has no extension methods, and Rust's orphan rule prevents adding methods to another crate's enum. A custom `Rounding` type carrying methods works in all of them: `TowardZero.Add(a, b)` in Go, `Rounding.TOWARD_ZERO.add(a, b)` in Java and Kotlin, `.towardZero.add(a, b)` in Swift and Zig.

The C library, which has no methods, uses the flattened form `d128_add_rnd(a, b, ROUND_TOWARD_ZERO)` and `d128_add_ctx(a, b, ctx)`. This is the same tuple with the modifier trailing, and it is what every receiver call compiles down to.

### 5.3 Flags are the other half of the problem

IEEE 754's exception flags (inexact, underflow, overflow, division by zero, invalid operation) are also part of the C floating-point environment, and they suffer the same problems as the rounding mode. A sticky flag raised in one task and tested in another is meaningless.

Most programs never read the flags at all. In Decimal128 by Miguel, bare arithmetic and the `Rounding` receiver neither record nor carry flags, so those programs pay nothing for a feature they do not use. The small set of programs that do need status, for example to confirm that a ledger total was exact or to detect an overflow, opt in by using a `DecimalContext`, and get flags scoped to their own work instead of a global status register shared with everything else.

The receiver model handles flags the same way it handles rounding. A `DecimalContext` holds a rounding direction and an accumulating set of raised flags. It is created where a unit of work begins and passed to the code that does that work, in the same way Go passes `context.Context`. The documentation for the Go port of Decimal128 by Miguel is explicit that a context is not safe for concurrent use and that each goroutine should have its own; `Decimal128` values are immutable and freely shared. Ownership is visible in the source, so the question "which flags did *this* calculation raise?" always has an answer.

### 5.4 Examples

Interval bounds computed concurrently. Each goroutine's rounding is fixed by the line it runs, so scheduling cannot change either result:

```go
import (
	"sync"

	d "github.com/migueldecimal128/decimal128-go"
)

func quotientBounds(a, b d.Decimal128) (lo, hi d.Decimal128) {
	var wg sync.WaitGroup
	wg.Add(2)
	go func() { defer wg.Done(); lo = d.TowardNegative.Quo(a, b) }()
	go func() { defer wg.Done(); hi = d.TowardPositive.Quo(a, b) }()
	wg.Wait()
	return
}
```

Asymmetric rounding rules in one expression, with no state to set:

```swift
let cent: Decimal128 = "0.01"
let creditToCustomer = Rounding.towardNegative.quantized(interestEarned, to: cent)
let chargeToCustomer = Rounding.towardPositive.quantized(interestOwed, to: cent)
```

A per-task context that also answers whether anything was rounded:

```go
func invoiceLine(qty, unit, rate d.Decimal128) (total d.Decimal128, rounded bool) {
	ctx := d.NewContextWithRounding(d.TiesToAway) // owned by this call
	net := ctx.Mul(qty, unit)
	tax := ctx.Quantize(ctx.Mul(net, rate), d.MustParse("0.01"))
	return ctx.Add(net, tax), ctx.RaisedFlags().Has(d.FlagInexact)
}
```

`invoiceLine` can run in ten thousand goroutines at once. Each call's rounding and flags are its own.

### 5.5 Cost

An explicit mode is not slower than an ambient one. Most importantly, the vast majority of operations use the default `roundTiesToEven` through bare arithmetic, which neither passes a rounding direction nor retrieves one from global state, so those operations incur neither cost. For the few directed operations, invoking an operation on a `Rounding` receiver passes the direction the same way any argument is passed, with no global or thread-local state to read. In Decimal128 by Miguel the direction selects the rounding outcome through a branch-free lookup in a packed constant, so a known direction costs nothing beyond that lookup, and a constant receiver such as `Rounding.towardZero` can be folded by the compiler. A software decimal library using the ambient model, by contrast, must load a global or thread-local variable on every operation, and correct callers must also save and restore it.

## 6. Objections

**"IEEE 754 requires a dynamic rounding mode."** What it requires is a language-defined means to specify a constant rounding-direction attribute for the operations in a block, with dynamic modes a recommended addition, "particularly to support debugging" (Section 2.1). A receiver that is a literal, such as `Rounding.towardZero`, specifies a constant attribute for a block of one operation, the smallest block the standard contemplates (Section 2.1). A receiver that is a variable, such as a `Rounding` read from configuration, is a dynamic attribute whose scope is the variable's scope. Both are expressed in the language; neither needs mutable state shared with code the programmer did not write.

**"Compute with the default rounding, then round the result afterward."** This is the design of the `Decimal128` type in .NET 11's `System.Numerics`. Its arithmetic is exposed only as operators with no rounding argument, and directed rounding is available only by applying `Round(value, digits, MidpointRounding)` or `Quantize` to a result that has already been rounded [.NET Decimal128]. It looks equivalent to rounding in the operation. It is not: it is not proper rounding, and it is not compliant with IEEE 754.

Take an operation whose exact result is 0.9999…9, with more 9s than fit in 34 digits: for example 1 − 10⁻⁴⁰. The rule is to truncate (`roundTowardZero`) to an integer. The exact value is less than 1, so the correct answer is `0`.

| Step | Round in the operation | Round afterward |
|---|---|---|
| 1 − 10⁻⁴⁰, to 34 digits | `roundTowardZero`: `0.9999999999999999999999999999999999` | `roundTiesToEven`: `1.000000000000000000000000000000000` |
| Truncate to an integer | `0` | `1` |

Rounded under `roundTiesToEven`, the subtraction turns 0.9999…9 into exactly 1. Truncating 1 gives 1. The truncation was applied correctly; it was applied to the wrong number, because the first rounding had already pushed the value across the integer boundary it was supposed to stay below. Rounded under `roundTowardZero` in the operation, the result stays below 1 and truncates to the correct `0`. Both columns were run against Decimal128 by Miguel.

As Section 1 quotes, IEEE 754 requires each operation to round its exact result once, in the applicable direction, and it requires implementations to provide the directed attributes for that rounding [IEEE 754-2019 §4.3]. An API whose arithmetic always rounds under `roundTiesToEven`, and which offers directed rounding only as a second step, cannot meet that requirement: the second step rounds a different number.

In discussions with Microsoft on GitHub chats, the rationale given for this design was performance: the belief that accepting a user-supplied rounding direction slows down arithmetic. It does not, for three reasons.

1. **Exact results never consult the direction.** Rounding only happens when a result does not fit in 34 digits, and in decimal work most additions, subtractions and multiplications fit. Adding two prices, subtracting a discount, or multiplying a quantity by a unit price produces a result with far fewer than 34 digits, so it is exact. In Decimal128 by Miguel an exact result returns before the rounding step is reached, so the direction is never read. For these operations the cost of a user-supplied rounding direction is zero.
2. **Inexact results cost the same in every direction, and a constant direction is free.** Every direction, `roundTiesToEven` included, goes through the same branch-free lookup, and a literal receiver can be folded by the compiler (Section 5.5).
3. **Rounding afterward is the expensive design.** It does all the work of a `roundTiesToEven` operation and then a second rounding operation, `Round` or `Quantize`, on every directed result. It also gives the wrong answer (above).

Intel's libbid, often used as the performance reference for software decimal arithmetic, takes the same view: its documented default Linux build passes the rounding mode to each function as an argument [Intel libbid README]. In practice that argument is almost always `roundTiesToEven`. Every caller pays to pass it, and the library is still the benchmark others are measured against. Decimal128 by Miguel goes one step further: bare arithmetic carries no rounding argument at all, and only the few operations that need a direction name one.

**"It is more verbose."** Only where it should be. The common case, `roundTiesToEven` with no flags, uses the bare operators and is no longer than with an ambient mode. The directed case adds one word per operation, and that word is the rounding rule a reviewer needs to see. A block that uses one direction throughout can bind it once: `let r = Rounding.towardZero`, then `r.add`, `r.multiply`.

**"Our whole application uses one mode, set at startup."** The premise does not survive contact with the rules it claims to implement. Regulations that prescribe rounding name a *quantum* and a *point in the calculation*, not a mode for the program:

- **Euro conversion.** Council Regulation (EC) No 1103/97 fixes conversion rates to six significant figures, forbids rounding or truncating them during conversion, and forbids inverse rates. Only the resulting amount is rounded, to the nearest cent, with exact halves rounded up, which is `roundTiesToAway` [EC 1103/97, Arts. 4–5].
- **US sales tax.** The Streamlined Sales and Use Tax Agreement, as enacted by member states, requires the tax computation to be carried to the third decimal place and then rounded to a whole cent, half a cent or more rounding up, which is `roundTiesToAway`, on either an item or an invoice basis at the seller's election [R.I. Gen. Laws § 44-18.1-25; Minnesota RN 05-08].
- **UK VAT.** HMRC's rounding concession for invoice traders applies to the VAT amount charged on an invoice, at line or invoice level, not to the arithmetic that produces it [HMRC VATREC12010].

Each rule applies once, to one named quantity, at one named step, and everything before that step is either unrounded or explicitly protected from rounding. A program-wide mode governs something else entirely: the rounding of every intermediate result to 34 digits. It cannot express "round the tax on this invoice to the cent under `roundTiesToAway`", because that rule needs a quantization to the cent, and the quantization is a specific operation in a specific place. That operation is where the direction belongs, and the receiver puts it there: bare arithmetic everywhere, and `Rounding.tiesToAway.quantized(tax, to: cent)` at the one line the regulation describes.

**"Python and others fixed this with context variables."** Context variables make the ambient model correct for one runtime's tasks, and they are the right repair for an API that already promised implicit state. They do not remove the action at a distance of Section 3.1, they depend on every scheduler propagating them, and they do not exist in Go by design. A library designed today does not need the repair if it never makes the promise.

**"This does not help binary floating-point hardware."** Correct, and out of scope: binary `float` and `double` operations take their rounding from the hardware control register, and in practice that register is almost never changed from `roundTiesToEven`. The experience of binary floating-point is itself evidence that directed rounding is needed rarely and locally. Even there, the direction of travel is toward static rounding, as Section 7 shows. Decimal128 is implemented in software on x86 and ARM, so a decimal library has no register to inherit and every reason not to imitate one.

## 7. Related Work and Convergence

The receiver model is not an isolated preference. Standards and languages have each been moving the rounding direction from execution state toward program text.

- **C23 static rounding.** C23 adds `#pragma STDC FENV_ROUND direction`, which sets a *constant* rounding direction for a translation unit or compound statement, and `#pragma STDC FENV_DEC_ROUND` as its decimal analog [WG14 N3702]. The dynamic mode remains available as `FE_DYNAMIC`. The C committee's own direction is to make the common case lexical.
- **Java `MathContext`.** Java's `BigDecimal` has always taken its precision and rounding from an immutable `MathContext` passed per operation, with a predefined `MathContext.DECIMAL128` [Java MathContext]. It is the parameter placement of Section 4, and it has no ambient-state problems.
- **Java scoped values.** JDK 25 delivered `ScopedValue` as an alternative to `ThreadLocal` for passing data down a call chain. Its rationale names three faults of thread-local variables: any code that can read one can change it, its value lives until someone removes it, and child threads must copy it. A scoped value is immutable and bound only for the duration of a call [JEP 506]. The Java platform has moved from mutable per-thread state toward values fixed by program structure, which is the move this paper makes for rounding.
- **Go `context.Context`.** Go's refusal to provide goroutine-local storage, and its convention of passing a `Context` explicitly as a first argument, is the same principle applied to request-scoped data in general [Go FAQ; golang/go#22770].
- **GDAS and Python `decimal.Context` methods.** Cowlishaw's General Decimal Arithmetic Specification models every operation as taking a context, and Python's `decimal.Context` exposes the arithmetic as methods (`ctx.add(a, b)`). The `DecimalContext` in Decimal128 by Miguel follows that precedent; the `Rounding` receiver extends it to a lighter-weight object for the case where no flags are wanted.

## 8. Conclusion

IEEE 754 asks that a program be able to say how its results are rounded. It does not ask that the answer be kept in a register that every operation reads and any code may change. That implementation choice was reasonable for single-threaded programs on processors with one control word. It is the wrong choice for software decimal arithmetic in programs built from thread pools, coroutines and goroutines, where the code that sets state and the code that reads it no longer share a thread or a lifetime.

The alternative is to make the rounding direction an ordinary value and to put it where the operation is written. Bare arithmetic rounds under `roundTiesToEven` and touches nothing. Directed arithmetic is invoked on the direction: `Rounding.towardZero.add(a, b)`. Arithmetic that must also report exceptions is invoked on a context the caller owns: `ctx.add(a, b)`. Each line then means what it says, on any thread, in any order, under any scheduler.

Decimal128 by Miguel ships this model in Swift, Kotlin, Java, Rust, Go, C#, Zig and Python, with the equivalent flattened form in C, and passes the decTest, FPgen and Intel libbid conformance suites with it. The rounding mode belongs to the code, not to the thread.

## References

[.NET Decimal128] Microsoft, *Decimal128 Struct (System.Numerics)*, .NET 11. Available: https://learn.microsoft.com/dotnet/api/system.numerics.decimal128?view=net-11.0. See also the .NET 11 Preview 7 libraries release notes: https://github.com/dotnet/core/blob/main/release-notes/11.0/preview/preview7/libraries.md

[Boost.Decimal] Boost.Decimal, *`<cfenv>` support*. Available: https://develop.decimal.cpp.al/decimal/cfenv.html

[C++ cfenv] ISO C++ working draft, *The floating-point environment [cfenv]*. Available: https://timsong-cpp.github.io/cppwp/n4659/cfenv

[cppreference fenv] cppreference, *Floating-point environment*. Available: https://www.cppreference.com/w/c/numeric/fenv.html

[Cowlishaw 2009] M. F. Cowlishaw, *General Decimal Arithmetic Specification*, version 1.70, IBM, 25 March 2009. Earlier drafts include Draft 0.66 (28 July 2000) and Draft 1.00 (5 July 2002). Available: https://speleotrove.com/decimal/decarith.pdf. The General Decimal Arithmetic home page, with the specification, its history and related material: https://speleotrove.com/decimal/

[EC 1103/97] Council Regulation (EC) No 1103/97 of 17 June 1997 on certain provisions relating to the introduction of the euro, Articles 4–5. Available: https://lawplayer.com/eu/act/31997R1103

[GCC libbid] GCC, *libgcc/config/libbid/bid_decimal_globals.c*. Available: https://gnu.googlesource.com/gcc/+/trunk/libgcc/config/libbid/bid_decimal_globals.c

[Go FAQ] The Go Authors, *doc/faq: explain why goroutines are anonymous*. Available: https://go.googlesource.com/go/+/992ce90f662467f04dd93b3bb565bb0414f82999%5E%21/

[golang/go#22770] *faq: document why there is no way to get a goroutine ID*. Available: https://golang.org/issue/22770

[HMRC VATREC12010] HMRC, *Rounding on invoices and rounding at retailers: What is the rounding concession?* Available: https://www.gov.uk/hmrc-internal-manuals/vat-trader-records/vatrec12010

[IEEE 754-2019] IEEE, *IEEE Standard for Floating-Point Arithmetic*, IEEE Std 754-2019, July 2019. DOI: 10.1109/IEEESTD.2019.8766229. Available: https://ieeexplore.ieee.org/document/8766229

[ISO C11 §7.6] ISO/IEC 9899:2011, 7.6 Floating-point environment `<fenv.h>`; thread storage duration as quoted in *fenv support vs. SMP systems* (newlib mailing list). Available: https://ecos.sourceware.org/ml/newlib/current/017770.html

[Intel libbid README] Intel, *Intel Decimal Floating-Point Math Library v2.3, README*. Available: https://netlib.org/misc/intel/README.txt

[Java MathContext] Oracle, *java.math.MathContext*. Available: https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/math/MathContext.html

[JDK-8240624] *Note mapping of RoundingMode constants to equivalent IEEE 754-2019 policy*. Available: https://bugs.openjdk.org/browse/JDK-8240624

[JEP 506] OpenJDK, *JEP 506: Scoped Values*, delivered in JDK 25. Available: https://openjdk.org/jeps/506

[Minnesota RN 05-08] Minnesota Department of Revenue, *Revenue Notice 05-08: Sales and Use Tax – Rounding – Per Item or Per Invoice*. Available: https://www.revenue.state.mn.us/revenue-notice/05-08-sales-and-use-tax-rounding-item-or-invoice

[PEP 327] F. Batista, *PEP 327 – Decimal Data Type*, created 17 October 2003, Python 2.4. Available: https://peps.python.org/pep-0327/

[PEP 567] Y. Selivanov, *PEP 567 – Context Variables*. Available: https://peps.python.org/pep-0567/

[R.I. Gen. Laws § 44-18.1-25] Rhode Island, *Streamlined Sales and Use Tax Agreement: rounding rule*. Available: https://webserver.rilegislature.gov/Statutes/TITLE44/44-18.1/44-18.1-25.htm

[US 6,058,410] *Method and apparatus for selecting a rounding mode for a numeric operation*. Available: https://patents.justia.com/patent/6058410

[WG14 N3702] ISO/IEC JTC1/SC22/WG14, *N3702*. Available: https://www.open-std.org/jtc1/sc22/wg14/www/docs/n3702.pdf

</div>
