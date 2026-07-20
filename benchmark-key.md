---
layout: default
permalink: /benchmark/key.html
title: "Benchmark Key — Decimal128"
description: "Shared legend for the decimal128 benchmark pages: operation-category codes, magnitude profiles, timing modes, and method."
heading: "Benchmark Key"
---

<div class="whitepaper" markdown="1">

<p class="whitepaper-meta">Shared legend for the per-language benchmark pages. Living document.</p>

This is the shared legend for the per-language **`benchmark-vs-<port>`** pages (and the
cross-port **`benchmark-port-compare`** matrices). Each of those pages records numbers
**as-measured**; the categories, magnitude profiles, units, parity settings, and methodology
are defined here and, authoritatively, in the companion **`BenchmarkMatrix.md`** — read it
first; the benchmark pages just record numbers produced under that contract.

## Benchmark tier boundary

Three views sit at three altitudes over the same ports:

- **`benchmark-vs-<port>`** (per-language) — for one language, the realistic-mix **FinMix**
  (P-fin) headline followed by the per-kernel, per-input-band characterization (P-gen band
  shape, FMA). "How fast are the operations, and each kernel, for *this* language — versus the
  alternatives available to it?"
- **`benchmark-port-compare`** — the cross-port d128 **band-shape matrices** (P-gen §1–§5,
  P-max stress, FMA FN/FF), d128-only, **no** alternatives. "How does each port's own d128
  band shape compare, port to port, on identical operands?"
- **`decimal128-app-benchmark`** (separate repo) — whole-application workloads (telco, euro,
  tax, banking, risk). "How fast is real financial *software*?"

## Columns & units

Columns: port · op · category · profile · arch · mode · `ns` (d128 ns/op) · alt · alt ns/op ·
ratio · run · notes.

ns/op figures are `Time / 4096` (4096 ops per measured iteration). `ratio = alt / ours`
(`> 1` ⇒ ours faster). `ours`/`ns` = decimal128 `_ctx` rung vs `alt` = the peer in that row
(the `libbid` universal reference, an in-language idiom peer, or a C-hosted decQuad/mpdecimal).
The `-` cell marks a band the peer cannot represent (e.g. the 28-digit compact peers
`rust_decimal` / `System.Decimal` overflow the `CP`/`WP` products), or a port with no peer at
all. **The ratio carries each port's own harness/packaging term** (Swift `opaque()`, Go
backend, …), since d128 is timed in-port while the universal `libbid`/decQuad/mpdecimal peers
are timed in C on the identical operands.

## Category & column codes (`BenchmarkMatrix.md` §3 is authoritative)

**Add / subtract** — binned by the operands' qExp gap (alignment work), §3.1:

| code | name | what it exercises |
|---|---|---|
| `SQ` | Same qExp | Δexp = 0; pack-direct fast path, no align |
| `NQ` | Near qExp | small gap, **no** rounding (result still fits 34 digits) |
| `MQ` | Mid qExp | gap > 4 digits (`qAlignDelta`), still no rounding |
| `OQ` | Overlapping qExp | gap forces align **+ round** (the heaviest add path) |
| `FQ` | Far qExp | smaller operand fully swamped (gap ≫ 34) |
| `MIX` | Realistic mix | 75% same-quantum / 25% independent quantum (P-fin add/sub stream) |
| `SQ-x` / `NQ-x` | …cancellation | subtract modifier: near-equal operands cancel (catastrophic) |

**Multiply** — binned by the exact product's digitLen, §3.2:

| code | name | what it exercises |
|---|---|---|
| `CP` | Compact Product | ≤ 34 digits — no scaling |
| `WP` | Wide Product | 35–38 digits — 128-bit recipMulPow10 |
| `XP` | eXtra-wide Product | > 38 (up to 68) — 256-bit recipMulPow10 |
| `CP-64` | …64-bit | CP with 64-bit (P-fin) operands |

**Divide** — binned by divisor digitLen (scaled dividend = 34 + digitLen(y)), §3.3:

| code | name | what it exercises |
|---|---|---|
| `CD` | Compact Divide | divisor 1–4 digits — 128÷64 |
| `WD` | Wide Divide | divisor 5–19 — 256÷64 |
| `XD` | eXtra Divide | divisor 20–34 — 256÷128 Möller–Granlund |
| `ET` | Exact / Terminating | `x/y` exact (residue `EXACT`) — full divide + trailing-zero strip |
| `PT` | Power-of-Ten divisor | `y = 10^k` — exact, coefficient-preserving result via the dedicated `divPow10Divisor` fast path (CrossPlatformArchitecture §2.4.9) |

**FMA** — `self + lhs·rhs` over 3-operand regimes (§3.4), by the finalize path `self` selects:

| code | name | what it exercises |
|---|---|---|
| `FN` | wide product kept | 256-bit Barrett finalize |
| `FF` | product swamped | fits-128 fast path |

## Profiles & modes

**Profiles** (operand-magnitude regime, §2.1, mandatory per row): `P-fin` = financial
(64-bit / ≤ 19-digit operands — the **headline**, closest to real financial code) · `P-gen` =
general (digit-length-uniform widths; per-band SQ/FQ 1–34, NQ 1–14, OQ 25–34) · `P-max` =
stress (34-digit; tagged `stress`, excluded from headline aggregates).

**P-fin regime** (`BenchmarkMatrix.md` §2.1): coefficients < 2⁶⁴ (≤ 19 digits, log-uniform),
currency-style quanta, every operand ≥ 1 integer digit — the reality for source financial data
before any division. Add/sub run as **one realistic `MIX` stream** (75% same-quantum / 25%
independent quantum — a blend of same-exp, pack-align and >4-digit-gap alignment) rather than
the per-band SQ/NQ/… split; multiply is `CP`/`WP`; divide is `CD`/`WD`/`ET`/`PT`.

**Modes:** `thru` = throughput · `lat` = latency (dependent chain). `thru*` = best-case
fixed-operand throughput · `thru‡` = JVM escape-forced alloc-inclusive headline (Java/Kotlin).
A bare `N` (e.g. "N (blend)") = an un-binned random baseline, not a taxonomy code.

## Method

Swept 4096-input average per band: ns/op = `Time / 4096` over the shared
`decimal128-resources/swept/<profile>/` corpus — **byte-identical operands every port**.
arm64 (M3 Pro) and x86_64 (Intel i9-9880H) are reported side by side. JVM verify-off; `‡` =
escape-forced alloc-inclusive. Peer selection per row: the port's in-language idiom decimal
type where it exists and can represent the band, else the universal reference `libbid`, else
`-` (the no-fallback ports). C additionally carries decQuad (DPD) and mpdecimal inline.

</div>
