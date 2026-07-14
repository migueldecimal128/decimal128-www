---
layout: default
permalink: /index.html
title: "Decimal128 — Home"
description: "Decimal128 builds open-source tools and shares them publicly on GitHub. This is our informational, read-only website."
heading: "Decimal128"
---

## The Problem

Binary floating point (Float/Double) has been the primary
floating-point number format on general-purpose computers since the
adoption of IEEE 754 in 1985. For mathematical reasons rooted in
base 2, most decimal fractions (like 0.10) cannot be represented
exactly. In addition, correctly rounding a decimal value to a given
number of decimal places cannot be done in binary — rounding 1.015
to the nearest cent should give 1.02 under banker's rounding, but
binary yields 1.01.

For domains such as finance, accounting, taxation, and payments,
these discrepancies are unacceptable. Legal, contractual, and audit
requirements demand arithmetic that produces exactly the same
results as manual decimal calculations.

Currently the only fast hardware option for decimal is found on IBM
Z (mainframe) and POWER processors. Slower software implementations
are required for all other general purpose computers. Intel libbid
is an implementation in C, available to C and C++ developers via
gcc compiler extensions. Java BigDecimal is widely used, but is not
IEEE 754 compliant. Python has excellent Decimal support that
predates IEEE 754 decimal floating point, but Python is relatively
slow and Python is not frequently used in commercial financial
applications.

## The Solution

I developed an IEEE 754-2019 compliant decimal128 high-performance
software architecture, implemented in eight programming languages —
C, C#, Java, Kotlin KMP, Swift, Rust, Go, and Python.

This implementation guarantees identical, auditable, spec-compliant
decimal arithmetic on every platform for financial systems:

- Ensures exactness for decimals up to 34 digits of precision
- Provides five rounding directions with correct status-flag behavior
- Outperforms the IBM (libdecnumber) and Intel (libbid) reference libraries, and Python's libmpdec
- Passes all three major industry correctness suites: IBM decTest, IBM fptest, and Intel libbid test vectors
- Removes the industry-wide barrier of "no good decimal option"

This solution makes it possible to move decimal financial workloads
off the IBM mainframe to the cloud without sacrificing the numerical
correctness, determinism, or auditability that regulated
environments depend on.

The decimal128 architecture is implemented natively in eight
programming languages, so systems built on different platforms can
share exactly the same arithmetic behaviour:

`C` · `C#` · `Java` · `Kotlin KMP` · `Swift` · `Rust` · `Go` · `Python`

The Swift and Kotlin implementations run natively on iOS and
Android — reaching mobile fintech, payments, and point-of-sale
applications, which have only had limited, slow, non-standardized
decimal options.
