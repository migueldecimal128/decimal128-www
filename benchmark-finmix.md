---
layout: default
permalink: /benchmark/finmix.html
title: "FinMix Benchmark Results — Decimal128"
description: "decimal128 on a realistic financial operation mix (P-fin) versus peer implementations, port by port."
heading: "FinMix Benchmark Results"
---

<div class="whitepaper" markdown="1">

<p class="whitepaper-meta">Split out of `benchmark-op-results.md` 2026-07-17. Living document — as-measured results.</p>

**d128 vs the idiom financial alternative, per port — the headline ratio.** `ratio = alt / ours`
(> 1 ⇒ d128 faster). Realistic 64-bit financial operation mix (P-fin): one `MIX` add/sub stream,
mul `CP`/`WP`, div `CD`/`WD`/`ET`/`PT`. Peer = the port's in-language idiom financial type where it
exists, else the universal reference `libbid`; `-` where the peer cannot represent the band (the
28-digit compact peers `rust_decimal` / `System.Decimal` overflow the `CP`/`WP` products). C is
additionally measured against decQuad + mpdecimal. `zig` has no in-language decimal peer, so it is
measured against the universal reference `libbid` (like C); `go` has neither an in-language peer nor
a `libbid` fallback, so its rows are d128-only (`-` in the alt/ratio columns). Full profile
definition, categories, and method are in the **Key** below the tables.

## d128 vs alternatives — arm64 (M3 Pro)

<!-- BEGIN GENERATED pfin-rel -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | add | MIX | P-fin | arm64 | thru | 2.81 | libbid | 10.35 | **3.68×** | Rc2 |  |
| c | add | MIX | P-fin | arm64 | thru | 2.81 | decQuad | 22.51 | **8.01×** | Rc2 |  |
| c | add | MIX | P-fin | arm64 | thru | 2.81 | mpdecimal | 13.46 | **4.79×** | Rc2 |  |
| c | sub | MIX | P-fin | arm64 | thru | 2.04 | libbid | 10.65 | **5.22×** | Rc2 |  |
| c | sub | MIX | P-fin | arm64 | thru | 2.04 | decQuad | 23.29 | **11.42×** | Rc2 |  |
| c | sub | MIX | P-fin | arm64 | thru | 2.04 | mpdecimal | 14.99 | **7.35×** | Rc2 |  |
| c | mul | CP | P-fin | arm64 | thru | 1.21 | libbid | 23.69 | **19.58×** | Rc2 |  |
| c | mul | CP | P-fin | arm64 | thru | 1.21 | decQuad | 21.41 | **17.69×** | Rc2 |  |
| c | mul | CP | P-fin | arm64 | thru | 1.21 | mpdecimal | 9.91 | **8.19×** | Rc2 |  |
| c | mul | WP | P-fin | arm64 | thru | 20.60 | libbid | 34.45 | **1.67×** | Rc2 |  |
| c | mul | WP | P-fin | arm64 | thru | 20.60 | decQuad | 25.54 | **1.24×** | Rc2 |  |
| c | mul | WP | P-fin | arm64 | thru | 20.60 | mpdecimal | 29.78 | **1.45×** | Rc2 |  |
| c | div | CD | P-fin | arm64 | thru | 43.22 | libbid | 35.06 | **0.81×** | Rc2 |  |
| c | div | CD | P-fin | arm64 | thru | 43.22 | decQuad | 71.42 | **1.65×** | Rc2 |  |
| c | div | CD | P-fin | arm64 | thru | 43.22 | mpdecimal | 60.03 | **1.39×** | Rc2 |  |
| c | div | WD | P-fin | arm64 | thru | 39.24 | libbid | 39.18 | **1.00×** | Rc2 |  |
| c | div | WD | P-fin | arm64 | thru | 39.24 | decQuad | 117.29 | **2.99×** | Rc2 |  |
| c | div | WD | P-fin | arm64 | thru | 39.24 | mpdecimal | 87.72 | **2.24×** | Rc2 |  |
| c | div | ET | P-fin | arm64 | thru | 6.49 | libbid | 6.11 | **0.94×** | Rc2 |  |
| c | div | ET | P-fin | arm64 | thru | 6.49 | decQuad | 41.51 | **6.40×** | Rc2 |  |
| c | div | ET | P-fin | arm64 | thru | 6.49 | mpdecimal | 56.09 | **8.64×** | Rc2 |  |
| c | div | PT | P-fin | arm64 | thru | 3.16 | libbid | 6.10 | **1.93×** | Rc2 |  |
| c | div | PT | P-fin | arm64 | thru | 3.16 | decQuad | 39.27 | **12.43×** | Rc2 |  |
| c | div | PT | P-fin | arm64 | thru | 3.16 | mpdecimal | 45.89 | **14.52×** | Rc2 |  |
| rust | add | MIX | P-fin | arm64 | thru | 3.12 | rust_decimal | 3.76 | **1.21×** | Rrsw2 | compact idiom peer |
| rust | sub | MIX | P-fin | arm64 | thru | 2.47 | rust_decimal | 3.71 | **1.50×** | Rrsw2 | compact idiom peer |
| rust | mul | CP | P-fin | arm64 | thru | 1.12 | libbid | 23.69 | **21.15×** | Rrsw2 |  |
| rust | mul | WP | P-fin | arm64 | thru | 15.10 | libbid | 34.45 | **2.28×** | Rrsw2 |  |
| rust | div | CD | P-fin | arm64 | thru | 27.23 | rust_decimal | 14.40 | **0.53×** | Rrsw2 | compact idiom peer |
| rust | div | WD | P-fin | arm64 | thru | 34.43 | rust_decimal | 19.98 | **0.58×** | Rrsw2 | compact idiom peer |
| rust | div | ET | P-fin | arm64 | thru | 6.20 | rust_decimal | 3.85 | **0.62×** | Rrsw2 | compact idiom peer |
| rust | div | PT | P-fin | arm64 | thru | 3.98 | rust_decimal | 15.14 | **3.80×** | Rrsw2 | compact idiom peer |
| zig | add | MIX | P-fin | arm64 | thru | 3.14 | libbid | 10.35 | **3.30×** | Rzgsw2 |  |
| zig | sub | MIX | P-fin | arm64 | thru | 2.48 | libbid | 10.65 | **4.29×** | Rzgsw2 |  |
| zig | mul | CP | P-fin | arm64 | thru | 1.44 | libbid | 23.69 | **16.45×** | Rzgsw2 |  |
| zig | mul | WP | P-fin | arm64 | thru | 18.64 | libbid | 34.45 | **1.85×** | Rzgsw2 |  |
| zig | div | CD | P-fin | arm64 | thru | 40.61 | libbid | 35.06 | **0.86×** | Rzgsw2 |  |
| zig | div | WD | P-fin | arm64 | thru | 41.25 | libbid | 39.18 | **0.95×** | Rzgsw2 |  |
| zig | div | ET | P-fin | arm64 | thru | 7.65 | libbid | 6.11 | **0.80×** | Rzgsw2 |  |
| zig | div | PT | P-fin | arm64 | thru | 4.23 | libbid | 6.10 | **1.44×** | Rzgsw2 |  |
| swift | add | MIX | P-fin | arm64 | thru | 4.16 | Foundation.Decimal | 337.29 | **81.08×** | Rswsw2 | compact idiom peer |
| swift | sub | MIX | P-fin | arm64 | thru | 3.07 | Foundation.Decimal | 341.16 | **111.13×** | Rswsw2 | compact idiom peer |
| swift | mul | CP | P-fin | arm64 | thru | 1.78 | Foundation.Decimal | 293.46 | **164.87×** | Rswsw2 | compact idiom peer |
| swift | mul | WP | P-fin | arm64 | thru | 22.01 | Foundation.Decimal | 294.61 | **13.39×** | Rswsw2 | compact idiom peer |
| swift | div | CD | P-fin | arm64 | thru | 35.90 | Foundation.Decimal | 1291.90 | **35.99×** | Rswsw2 | compact idiom peer |
| swift | div | WD | P-fin | arm64 | thru | 48.13 | Foundation.Decimal | 693.33 | **14.41×** | Rswsw2 | compact idiom peer |
| swift | div | ET | P-fin | arm64 | thru | 8.53 | Foundation.Decimal | 3720.17 | **436.13×** | Rswsw2 | compact idiom peer |
| swift | div | PT | P-fin | arm64 | thru | 7.62 | Foundation.Decimal | 3623.83 | **475.57×** | Rswsw2 | compact idiom peer |
| csharp | add | MIX | P-fin | arm64 | thru | 4.00 | System.Decimal | 3.01 | **0.75×** | Rcs11 | compact idiom peer |
| csharp | add | MIX | P-fin | arm64 | thru | 4.00 | Decimal128 (.NET 11) | 15.67 | **3.92×** | Rcs11 |  |
| csharp | sub | MIX | P-fin | arm64 | thru | 3.00 | System.Decimal | 2.97 | **0.99×** | Rcs11 | compact idiom peer |
| csharp | sub | MIX | P-fin | arm64 | thru | 3.00 | Decimal128 (.NET 11) | 15.64 | **5.21×** | Rcs11 |  |
| csharp | mul | CP | P-fin | arm64 | thru | 1.70 | - | - | - | Rcs11 |  |
| csharp | mul | CP | P-fin | arm64 | thru | 1.70 | Decimal128 (.NET 11) | 11.05 | **6.50×** | Rcs11 |  |
| csharp | mul | WP | P-fin | arm64 | thru | 30.98 | - | - | - | Rcs11 |  |
| csharp | mul | WP | P-fin | arm64 | thru | 30.98 | Decimal128 (.NET 11) | 48.00 | **1.55×** | Rcs11 |  |
| csharp | div | CD | P-fin | arm64 | thru | 32.27 | System.Decimal | 11.27 | **0.35×** | Rcs11 | compact idiom peer |
| csharp | div | CD | P-fin | arm64 | thru | 32.27 | Decimal128 (.NET 11) | 153.50 | **4.76×** | Rcs11 |  |
| csharp | div | WD | P-fin | arm64 | thru | 53.85 | System.Decimal | 28.10 | **0.52×** | Rcs11 | compact idiom peer |
| csharp | div | WD | P-fin | arm64 | thru | 53.85 | Decimal128 (.NET 11) | 181.64 | **3.37×** | Rcs11 |  |
| csharp | div | ET | P-fin | arm64 | thru | 14.13 | System.Decimal | 5.34 | **0.38×** | Rcs11 | compact idiom peer |
| csharp | div | ET | P-fin | arm64 | thru | 14.13 | Decimal128 (.NET 11) | 236.66 | **16.75×** | Rcs11 |  |
| csharp | div | PT | P-fin | arm64 | thru | 5.29 | System.Decimal | 12.54 | **2.37×** | Rcs11 | compact idiom peer |
| csharp | div | PT | P-fin | arm64 | thru | 5.29 | Decimal128 (.NET 11) | 242.35 | **45.81×** | Rcs11 |  |
| go | add | MIX | P-fin | arm64 | thru | 8.51 | - | - | - | Rgosw2 |  |
| go | sub | MIX | P-fin | arm64 | thru | 4.17 | - | - | - | Rgosw2 |  |
| go | mul | CP | P-fin | arm64 | thru | 2.14 | - | - | - | Rgosw2 |  |
| go | mul | WP | P-fin | arm64 | thru | 28.31 | - | - | - | Rgosw2 |  |
| go | div | CD | P-fin | arm64 | thru | 47.17 | - | - | - | Rgosw2 |  |
| go | div | WD | P-fin | arm64 | thru | 62.17 | - | - | - | Rgosw2 |  |
| go | div | ET | P-fin | arm64 | thru | 11.68 | - | - | - | Rgosw2 |  |
| go | div | PT | P-fin | arm64 | thru | 6.52 | - | - | - | Rgosw2 |  |
| java | add | MIX | P-fin | arm64 | thru‡ | 6.21 | BigDecimal | 19.70 | **3.17×** | Rjasw2 | compact idiom peer |
| java | sub | MIX | P-fin | arm64 | thru‡ | 5.62 | BigDecimal | 22.73 | **4.04×** | Rjasw2 | compact idiom peer |
| java | mul | CP | P-fin | arm64 | thru‡ | 4.74 | BigDecimal | 12.60 | **2.66×** | Rjasw2 | compact idiom peer |
| java | mul | WP | P-fin | arm64 | thru‡ | 33.01 | BigDecimal | 68.67 | **2.08×** | Rjasw2 | compact idiom peer |
| java | div | CD | P-fin | arm64 | thru‡ | 38.54 | BigDecimal | 144.22 | **3.74×** | Rjasw2 | compact idiom peer |
| java | div | WD | P-fin | arm64 | thru‡ | 47.52 | BigDecimal | 91.45 | **1.92×** | Rjasw2 | compact idiom peer |
| java | div | ET | P-fin | arm64 | thru‡ | 12.35 | BigDecimal | 493.96 | **40.00×** | Rjasw2 | compact idiom peer |
| java | div | PT | P-fin | arm64 | thru‡ | 9.35 | BigDecimal | 474.04 | **50.70×** | Rjasw2 | compact idiom peer |
| kotlin | add | MIX | P-fin | arm64 | thru‡ | 7.13 | BigDecimal | 19.99 | **2.80×** | Rkosw2 | compact idiom peer |
| kotlin | sub | MIX | P-fin | arm64 | thru‡ | 6.14 | BigDecimal | 23.27 | **3.79×** | Rkosw2 | compact idiom peer |
| kotlin | mul | CP | P-fin | arm64 | thru‡ | 5.58 | BigDecimal | 12.52 | **2.24×** | Rkosw2 | compact idiom peer |
| kotlin | mul | WP | P-fin | arm64 | thru‡ | 32.07 | BigDecimal | 67.91 | **2.12×** | Rkosw2 | compact idiom peer |
| kotlin | div | CD | P-fin | arm64 | thru‡ | 42.39 | BigDecimal | 149.50 | **3.53×** | Rkosw2 | compact idiom peer |
| kotlin | div | WD | P-fin | arm64 | thru‡ | 57.14 | BigDecimal | 121.58 | **2.13×** | Rkosw2 | compact idiom peer |
| kotlin | div | ET | P-fin | arm64 | thru‡ | 19.52 | BigDecimal | 507.38 | **25.99×** | Rkosw2 | compact idiom peer |
| kotlin | div | PT | P-fin | arm64 | thru‡ | 11.73 | BigDecimal | 489.23 | **41.71×** | Rkosw2 | compact idiom peer |
| python | add | MIX | P-fin | arm64 | thru | 24.44 | decimal.Decimal | 64.71 | **2.65×** | Rpysw2 | compact idiom peer |
| python | sub | MIX | P-fin | arm64 | thru | 22.99 | decimal.Decimal | 62.23 | **2.71×** | Rpysw2 | compact idiom peer |
| python | mul | CP | P-fin | arm64 | thru | 16.65 | decimal.Decimal | 62.76 | **3.77×** | Rpysw2 | compact idiom peer |
| python | mul | WP | P-fin | arm64 | thru | 38.17 | decimal.Decimal | 67.45 | **1.77×** | Rpysw2 | compact idiom peer |
| python | div | CD | P-fin | arm64 | thru | 60.00 | decimal.Decimal | 96.43 | **1.61×** | Rpysw2 | compact idiom peer |
| python | div | WD | P-fin | arm64 | thru | 66.13 | decimal.Decimal | 100.24 | **1.52×** | Rpysw2 | compact idiom peer |
| python | div | ET | P-fin | arm64 | thru | 22.11 | decimal.Decimal | 85.68 | **3.88×** | Rpysw2 | compact idiom peer |
| python | div | PT | P-fin | arm64 | thru | 18.32 | decimal.Decimal | 83.53 | **4.56×** | Rpysw2 | compact idiom peer |

<!-- END GENERATED pfin-rel -->

## d128 vs alternatives — x86_64 (Intel i9-9880H)

<!-- BEGIN GENERATED pfin-rel-x86 -->

| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | add | MIX | P-fin | x86_64 | thru | 10.01 | libbid | 31.03 | **3.10×** | xRc2 |  |
| c | add | MIX | P-fin | x86_64 | thru | 10.01 | decQuad | 59.43 | **5.94×** | xRc2 |  |
| c | add | MIX | P-fin | x86_64 | thru | 10.01 | mpdecimal | 38.13 | **3.81×** | xRc2 |  |
| c | sub | MIX | P-fin | x86_64 | thru | 8.42 | libbid | 35.45 | **4.21×** | xRc2 |  |
| c | sub | MIX | P-fin | x86_64 | thru | 8.42 | decQuad | 60.69 | **7.21×** | xRc2 |  |
| c | sub | MIX | P-fin | x86_64 | thru | 8.42 | mpdecimal | 38.04 | **4.52×** | xRc2 |  |
| c | mul | CP | P-fin | x86_64 | thru | 2.51 | libbid | 47.15 | **18.78×** | xRc2 |  |
| c | mul | CP | P-fin | x86_64 | thru | 2.51 | decQuad | 55.98 | **22.30×** | xRc2 |  |
| c | mul | CP | P-fin | x86_64 | thru | 2.51 | mpdecimal | 32.81 | **13.07×** | xRc2 |  |
| c | mul | WP | P-fin | x86_64 | thru | 46.77 | libbid | 60.29 | **1.29×** | xRc2 |  |
| c | mul | WP | P-fin | x86_64 | thru | 46.77 | decQuad | 69.22 | **1.48×** | xRc2 |  |
| c | mul | WP | P-fin | x86_64 | thru | 46.77 | mpdecimal | 44.24 | **0.95×** | xRc2 |  |
| c | div | CD | P-fin | x86_64 | thru | 87.44 | libbid | 77.69 | **0.89×** | xRc2 |  |
| c | div | CD | P-fin | x86_64 | thru | 87.44 | decQuad | 137.65 | **1.57×** | xRc2 |  |
| c | div | CD | P-fin | x86_64 | thru | 87.44 | mpdecimal | 158.24 | **1.81×** | xRc2 |  |
| c | div | WD | P-fin | x86_64 | thru | 102.32 | libbid | 82.71 | **0.81×** | xRc2 |  |
| c | div | WD | P-fin | x86_64 | thru | 102.32 | decQuad | 240.81 | **2.35×** | xRc2 |  |
| c | div | WD | P-fin | x86_64 | thru | 102.32 | mpdecimal | 280.40 | **2.74×** | xRc2 |  |
| c | div | ET | P-fin | x86_64 | thru | 18.22 | libbid | 20.15 | **1.11×** | xRc2 |  |
| c | div | ET | P-fin | x86_64 | thru | 18.22 | decQuad | 75.78 | **4.16×** | xRc2 |  |
| c | div | ET | P-fin | x86_64 | thru | 18.22 | mpdecimal | 142.13 | **7.80×** | xRc2 |  |
| c | div | PT | P-fin | x86_64 | thru | 10.21 | libbid | 19.71 | **1.93×** | xRc2 |  |
| c | div | PT | P-fin | x86_64 | thru | 10.21 | decQuad | 67.99 | **6.66×** | xRc2 |  |
| c | div | PT | P-fin | x86_64 | thru | 10.21 | mpdecimal | 87.97 | **8.62×** | xRc2 |  |
| rust | add | MIX | P-fin | x86_64 | thru | 9.63 | rust_decimal | 14.96 | **1.55×** | xRrsw2 | compact idiom peer |
| rust | sub | MIX | P-fin | x86_64 | thru | 8.01 | rust_decimal | 14.97 | **1.87×** | xRrsw2 | compact idiom peer |
| rust | mul | CP | P-fin | x86_64 | thru | 3.15 | libbid | 47.15 | **14.97×** | xRrsw2 |  |
| rust | mul | WP | P-fin | x86_64 | thru | 29.80 | libbid | 60.29 | **2.02×** | xRrsw2 |  |
| rust | div | CD | P-fin | x86_64 | thru | 71.07 | rust_decimal | 55.38 | **0.78×** | xRrsw2 | compact idiom peer |
| rust | div | WD | P-fin | x86_64 | thru | 89.09 | rust_decimal | 75.51 | **0.85×** | xRrsw2 | compact idiom peer |
| rust | div | ET | P-fin | x86_64 | thru | 22.70 | rust_decimal | 13.95 | **0.61×** | xRrsw2 | compact idiom peer |
| rust | div | PT | P-fin | x86_64 | thru | 9.77 | rust_decimal | 51.76 | **5.30×** | xRrsw2 | compact idiom peer |
| zig | add | MIX | P-fin | x86_64 | thru | 12.33 | libbid | 31.03 | **2.52×** | xRzgsw2 |  |
| zig | sub | MIX | P-fin | x86_64 | thru | 10.34 | libbid | 35.45 | **3.43×** | xRzgsw2 |  |
| zig | mul | CP | P-fin | x86_64 | thru | 7.04 | libbid | 47.15 | **6.70×** | xRzgsw2 |  |
| zig | mul | WP | P-fin | x86_64 | thru | 29.29 | libbid | 60.29 | **2.06×** | xRzgsw2 |  |
| zig | div | CD | P-fin | x86_64 | thru | 67.73 | libbid | 77.69 | **1.15×** | xRzgsw2 |  |
| zig | div | WD | P-fin | x86_64 | thru | 92.85 | libbid | 82.71 | **0.89×** | xRzgsw2 |  |
| zig | div | ET | P-fin | x86_64 | thru | 22.82 | libbid | 20.15 | **0.88×** | xRzgsw2 |  |
| zig | div | PT | P-fin | x86_64 | thru | 12.41 | libbid | 19.71 | **1.59×** | xRzgsw2 |  |
| swift | add | MIX | P-fin | x86_64 | thru | 11.60 | Foundation.Decimal | 804.37 | **69.34×** | xRswsw2 | compact idiom peer |
| swift | sub | MIX | P-fin | x86_64 | thru | 9.91 | Foundation.Decimal | 771.75 | **77.88×** | xRswsw2 | compact idiom peer |
| swift | mul | CP | P-fin | x86_64 | thru | 3.90 | Foundation.Decimal | 689.76 | **176.86×** | xRswsw2 | compact idiom peer |
| swift | mul | WP | P-fin | x86_64 | thru | 35.41 | Foundation.Decimal | 752.01 | **21.24×** | xRswsw2 | compact idiom peer |
| swift | div | CD | P-fin | x86_64 | thru | 70.24 | Foundation.Decimal | 2939.77 | **41.85×** | xRswsw2 | compact idiom peer |
| swift | div | WD | P-fin | x86_64 | thru | 91.35 | Foundation.Decimal | 1512.92 | **16.56×** | xRswsw2 | compact idiom peer |
| swift | div | ET | P-fin | x86_64 | thru | 21.86 | Foundation.Decimal | 8453.28 | **386.70×** | xRswsw2 | compact idiom peer |
| swift | div | PT | P-fin | x86_64 | thru | 12.72 | Foundation.Decimal | 8190.50 | **643.91×** | xRswsw2 | compact idiom peer |
| csharp | add | MIX | P-fin | x86_64 | thru | 17.39 | System.Decimal | 13.29 | **0.76×** | xRcssw2 | compact idiom peer |
| csharp | sub | MIX | P-fin | x86_64 | thru | 14.70 | System.Decimal | 13.21 | **0.90×** | xRcssw2 | compact idiom peer |
| csharp | mul | CP | P-fin | x86_64 | thru | 5.81 | - | - | - | xRcssw2 |  |
| csharp | mul | WP | P-fin | x86_64 | thru | 49.41 | - | - | - | xRcssw2 |  |
| csharp | div | CD | P-fin | x86_64 | thru | 81.67 | System.Decimal | 54.10 | **0.66×** | xRcssw2 | compact idiom peer |
| csharp | div | WD | P-fin | x86_64 | thru | 116.53 | System.Decimal | 116.27 | **1.00×** | xRcssw2 | compact idiom peer |
| csharp | div | ET | P-fin | x86_64 | thru | 26.29 | System.Decimal | 16.81 | **0.64×** | xRcssw2 | compact idiom peer |
| csharp | div | PT | P-fin | x86_64 | thru | 15.61 | System.Decimal | 60.09 | **3.85×** | xRcssw2 | compact idiom peer |
| go | add | MIX | P-fin | x86_64 | thru | 15.14 | - | - | - | xRgosw2 |  |
| go | sub | MIX | P-fin | x86_64 | thru | 12.65 | - | - | - | xRgosw2 |  |
| go | mul | CP | P-fin | x86_64 | thru | 5.14 | - | - | - | xRgosw2 |  |
| go | mul | WP | P-fin | x86_64 | thru | 54.03 | - | - | - | xRgosw2 |  |
| go | div | CD | P-fin | x86_64 | thru | 114.60 | - | - | - | xRgosw2 |  |
| go | div | WD | P-fin | x86_64 | thru | 130.60 | - | - | - | xRgosw2 |  |
| go | div | ET | P-fin | x86_64 | thru | 31.17 | - | - | - | xRgosw2 |  |
| go | div | PT | P-fin | x86_64 | thru | 13.38 | - | - | - | xRgosw2 |  |
| java | add | MIX | P-fin | x86_64 | thru‡ | 16.43 | BigDecimal | 55.19 | **3.36×** | xRjasw2 | compact idiom peer |
| java | sub | MIX | P-fin | x86_64 | thru‡ | 16.23 | BigDecimal | 66.31 | **4.09×** | xRjasw2 | compact idiom peer |
| java | mul | CP | P-fin | x86_64 | thru‡ | 12.37 | BigDecimal | 41.73 | **3.37×** | xRjasw2 | compact idiom peer |
| java | mul | WP | P-fin | x86_64 | thru‡ | 49.39 | BigDecimal | 150.91 | **3.06×** | xRjasw2 | compact idiom peer |
| java | div | CD | P-fin | x86_64 | thru‡ | 97.03 | BigDecimal | 408.57 | **4.21×** | xRjasw2 | compact idiom peer |
| java | div | WD | P-fin | x86_64 | thru‡ | 122.89 | BigDecimal | 218.12 | **1.77×** | xRjasw2 | compact idiom peer |
| java | div | ET | P-fin | x86_64 | thru‡ | 44.76 | BigDecimal | 1472.00 | **32.89×** | xRjasw2 | compact idiom peer |
| java | div | PT | P-fin | x86_64 | thru‡ | 23.41 | BigDecimal | 1405.87 | **60.05×** | xRjasw2 | compact idiom peer |
| kotlin | add | MIX | P-fin | x86_64 | thru‡ | 22.06 | BigDecimal | 58.48 | **2.65×** | xRkosw2 | compact idiom peer |
| kotlin | sub | MIX | P-fin | x86_64 | thru‡ | 18.54 | BigDecimal | 69.77 | **3.76×** | xRkosw2 | compact idiom peer |
| kotlin | mul | CP | P-fin | x86_64 | thru‡ | 13.05 | BigDecimal | 42.42 | **3.25×** | xRkosw2 | compact idiom peer |
| kotlin | mul | WP | P-fin | x86_64 | thru‡ | 45.37 | BigDecimal | 164.99 | **3.64×** | xRkosw2 | compact idiom peer |
| kotlin | div | CD | P-fin | x86_64 | thru‡ | 99.57 | BigDecimal | 430.06 | **4.32×** | xRkosw2 | compact idiom peer |
| kotlin | div | WD | P-fin | x86_64 | thru‡ | 122.28 | BigDecimal | 220.62 | **1.80×** | xRkosw2 | compact idiom peer |
| kotlin | div | ET | P-fin | x86_64 | thru‡ | 49.97 | BigDecimal | 1476.04 | **29.54×** | xRkosw2 | compact idiom peer |
| kotlin | div | PT | P-fin | x86_64 | thru‡ | 25.87 | BigDecimal | 1435.33 | **55.48×** | xRkosw2 | compact idiom peer |
| python | add | MIX | P-fin | x86_64 | thru | 48.66 | decimal.Decimal | 125.37 | **2.58×** | xRpysw2 | compact idiom peer |
| python | sub | MIX | P-fin | x86_64 | thru | 46.33 | decimal.Decimal | 125.50 | **2.71×** | xRpysw2 | compact idiom peer |
| python | mul | CP | P-fin | x86_64 | thru | 38.95 | decimal.Decimal | 119.69 | **3.07×** | xRpysw2 | compact idiom peer |
| python | mul | WP | P-fin | x86_64 | thru | 76.53 | decimal.Decimal | 133.20 | **1.74×** | xRpysw2 | compact idiom peer |
| python | div | CD | P-fin | x86_64 | thru | 113.68 | decimal.Decimal | 209.71 | **1.84×** | xRpysw2 | compact idiom peer |
| python | div | WD | P-fin | x86_64 | thru | 126.57 | decimal.Decimal | 230.16 | **1.82×** | xRpysw2 | compact idiom peer |
| python | div | ET | P-fin | x86_64 | thru | 55.53 | decimal.Decimal | 186.48 | **3.36×** | xRpysw2 | compact idiom peer |
| python | div | PT | P-fin | x86_64 | thru | 43.66 | decimal.Decimal | 179.55 | **4.11×** | xRpysw2 | compact idiom peer |

<!-- END GENERATED pfin-rel-x86 -->

## Key — profile, categories & method

**Benchmark tier boundary.** Three reports sit at three altitudes over the same ports:
- **`benchmark-finmix.md`** (this doc) — isolated realistic-mix *operation* streams (P-fin).
  "How fast are the operations as real financial code calls them?"
- **`benchmark-op-results.md`** — per-kernel, per-input-band characterization (P-gen band shape §1–§5,
  P-max wide-path stress, FMA). "How fast is each kernel on each shape?"
- **`decimal128-app-benchmark`** (separate repo) — whole-application workloads (telco, euro, tax,
  banking, risk). "How fast is real financial *software*?"

**P-fin regime** (`BenchmarkMatrix.md` §2.1): coefficients < 2⁶⁴ (≤ 19 digits, log-uniform),
currency-style quanta, every operand ≥ 1 integer digit — the reality for source financial data
before any division. Add/sub run as **one realistic `MIX` stream** (75% same-quantum / 25%
independent quantum — a blend of same-exp, pack-align and >4-digit-gap alignment) rather than the
per-band SQ/NQ/… split; multiply is `CP`/`WP`; divide is `CD`/`WD`/`ET`/`PT`. This is the
**headline** profile — closest to real financial code — complementing the P-gen band-shape
(`benchmark-op-results.md` §1–§5) and the P-max wide-path stress rows.

**Method.** Swept 4096-input average, same corpus/method as `benchmark-op-results.md` §1–§5. ns/op
figures are `Time / 4096` (4096 ops per measured iteration). Columns: port · op · category · profile
· arch · mode · `ns` (d128 ns/op) · alt · alt ns/op · ratio · run · notes. Rows are ordered by port,
then op (add/sub/mul/div). JVM `thru‡` = escape-forced
alloc-inclusive; `compact idiom peer` notes flag the in-language financial type (vs the `libbid`
universal reference).


</div>
