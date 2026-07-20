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
binary floating-point arithmetic yields 1.01.

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

Miguel developed an IEEE 754-2019 compliant decimal128 high-performance
software architecture, implemented in nine programming languages —
C, Java, Kotlin KMP, C#, Swift, Rust, Go, Zig, and Python.

This implementation guarantees identical, auditable, spec-compliant
decimal arithmetic on every platform:

- Ensures exactness for decimals up to 34 digits of precision
- Provides five rounding directions
- Outperforms the IBM (libdecnumber) and Intel (libbid) reference libraries, and Python's libmpdec
- Passes all three major industry correctness suites: IBM decTest, IBM fptest, and Intel libbid test vectors
- Removes the "no good decimal option" barrier for the finance industry

This solution makes it possible to move decimal financial workloads
off the IBM mainframe to the cloud without sacrificing the numerical
correctness, determinism, or auditability that regulated
environments depend on.

The decimal128 architecture is implemented natively in eight
programming languages, so systems built on different platforms can
share exactly the same arithmetic behaviour:

`C` · `Java` · `Kotlin KMP` · `C#` · `Swift` · `Rust` · `Go` · `Zig` · `Python`

The Swift and Kotlin implementations run natively on iOS and
Android — reaching mobile fintech, payments, and point-of-sale
applications, which previously have only had limited, slow, non-standardized
decimal options.

## Who is Miguel?

Miguel is a retired entrepreneur, engineer, and expert in database
technology with a broad computer systems background.

Early in his career Miguel co-authored the Microsoft Applesoft Compiler
for the Apple ][ computer. Miguel was then the first non-founder
employee of Datext, where he architected a specialized time-series
database for CD-ROM for the financial services industry, later
acquired by Lotus Development Corporation. Continuing his work with
CD-ROM databases, Miguel joined Ziff Communications as VP Technology
for the Computer Library Division. He then founded InterActive
WorkPlace, a sales force information system that was acquired by
Siebel Systems. Miguel later worked with Scalent Systems as Senior
Member, Technical Staff. Scalent was later acquired by Dell to become
the cornerstone of their data center automation suite.

In more recent years, Miguel focused his time on data warehousing,
applying Big Data technologies to solve traditional business data
processing problems for several major US financial institutions.
Miguel co-founded Podium Data, which was later acquired by Qlik.
Miguel has now been working on his decimal128 software solution,
hoping to revolutionize the financial world.

Before all this, Miguel worked as a research intern at Xerox PARC
while obtaining BS and MS degrees in Computer Science from MIT.

[Miguel's LinkedIn ↗](https://www.linkedin.com/in/miguel-decimal128-howard/)
