---
layout: default
permalink: /business-case.html
title: "Business Case — Decimal128"
description: "How Decimal128 helps business leaders in finance, accounting, and payments avoid the cost of incorrect decimal arithmetic."
heading: "Business Case"
---

Miguel's version of Decimal128 solves a problem most companies don't realize they have.

Computers were built to solve mathematical calculations using binary floating point, but binary does not always provide the accurate results in terms of rounding and decimal accuracy that is required for accounting, finance, tax, and payments. To ensure 100% accurate calculations, decimal floating point is required via additional hardware or software is needed. This leaves companies with two unsatisfying options: pay for speed by leasing IBM Z hardware, or use software that may not meet compliance standards or are very slow.

Miguel's version of Decimal128 eliminates this tradeoff, delivering both speed and compliance in a software solution.

Over time, Miguel's version can save thousands of dollars monthly by eliminating the cost of leasing IBM mainframe capacity. If you are currently using a slow software solution, Miguel's version will decrease your time to output for calculations, enabling you to work faster and ensure internal and external SLA's.

| | IBM Z (mainframe) | Intel libbid | Java Big Decimal | Python | Miguel's Version |
| --- | --- | --- | --- | --- | --- |
| Hardware vs software | hardware | software | software | N/A | software |
| Compliance | ✅ | ❌ | ❌ | ✅ | ✅ |
| Speed | fast | medium | medium | slow | fast |
| Cost | $$$ | $ | $ | N/A | free |
| Languages | N/A | C, available to C and C++ via GCC compiler extensions | N/A | N/A | N/A |

Real world examples where decimal128 is required:

- Microsoft Excel supports 15 digits per cell and automatically rounds when entering 16 digits
- [Add another real-world example here]
