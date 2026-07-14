---
layout: default
permalink: /business-case.html
title: "Business Case — Decimal128"
description: "How Decimal128 helps business leaders in finance, accounting, and payments avoid the cost of incorrect decimal arithmetic."
heading: "Business Case"
---

Decimal128 solves a problem most companies don't realize they have.

Computers were built to solve mathematical calculations using binary floating point, but binary does not always produce accurate results in terms of decimal precision and rounding that is required for accounting, finance, tax, and payments. To ensure 100% accurate and auditable calculations, decimal floating point is required via additional hardware or software. This leaves companies with two unsatisfying options: pay for speed running on IBM hardware, or use software that may not meet compliance standards or is very slow.

Miguel's version of Decimal128 eliminates this tradeoff, delivering a compliant software solution that benchmarks faster than other software implementations.

Over time, Miguel's version can save thousands of dollars monthly by eliminating the cost of leasing IBM mainframe capacity. If you are currently using a slow software solution, Miguel's version will decrease your time to output for calculations, enabling your batch processing jobs to complete faster and ensure internal and external SLA's.

<div markdown="1" class="table-fixed">

| | IBM Z (mainframe) | Intel libbid decimal128 | Java BigDecimal | Python Decimal | Miguel's Version |
| --- | --- | --- | --- | --- | --- |
| Hardware vs software | hardware | software | software | software | software |
| Compliance (IEEE 754-2019) | ✅ | ✅ | ❌ | ❌ | ✅ |
| Speed | fastest | fast | medium | slow | fast |
| Cost | \$\$\$\$ | free | free | free | TBD |
| Operating System | System Z mainframe | Linux, Mac OS | Linux, Mac OS, Windows, System Z mainframe | Linux, Mac OS, Windows | Linux, Mac OS, Windows, System Z mainframe, iOS, Android, JavaScript, WASM |
| Languages | COBOL, Java, TBD | C/C++ | Java, Kotlin JVM | Python | C, C#, Java, Kotlin KMP, Swift, Rust, Go, Python, Zig |

</div>

Real world examples where decimal128 is required:

- All computers using binary floating point will produce: 0.1 + 0.2 → 0.30000000000000004
- $1.015 gets truncated to $1.01 when it should be $1.02
- Microsoft Excel supports 15 digits per cell and automatically rounds when entering 16 digits. Apple Sheets converts 16 digits into text to circumvent issues
