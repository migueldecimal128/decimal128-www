# Micro-benchmark results store — schema sketch (v0)

Source of truth = JSONL (one measurement per line). `benchmark-op-results.md` §4.x tables
are GENERATED from it. Prose/analysis/run-log stay hand-written (hybrid doc).

## 1. Measurement record  (one JSONL line = one impl's number for one cell)

```json
{
  "lang":    "rust",          // c|swift|java|kotlin|rust|go|csharp|zig|python
  "impl":    "d128",          // d128|libbid|rust_decimal|System.Decimal|Foundation.Decimal|libdecquad|libmpdecimal|BigDecimal|decimal.Decimal
  "op":      "add",           // add|sub|mul|div|fma|toString|...
  "cat":     "SQ",            // SQ|NQ|MQ|OQ|FQ | CP|WP|XP | CD|WD|XD|PT|ET | FN|FF
  "profile": "P-gen",         // P-fin|P-gen|P-max|FMA
  "arch":    "arm64",         // arm64|x86_64
  "mode":    "thru",          // thru|thru*|thru‡ (harness/packaging variant)
  "ns":      3.08,            // ns/op — THE measurement, the only number stored
  "run":     "Rprof",         // provenance run-id (joins to the run log)
  "notes":   null             // optional per-measurement note
}
```

NO `alt`, `alt_ns`, `ratio` — all derived. A comparison table pairs two records on the
join key **(op, cat, profile, arch)** and computes `ratio = peer.ns / d128.ns`.

## 2. impl registry  (impl-level facts — stored ONCE, not per measurement)

```json
{
  "d128":               {"conformant": true,  "idiom_peer": false, "mantissa_digits": 34,          "lang_pinned": null,     "encoding": "BID"},
  "libbid":             {"conformant": true,  "idiom_peer": false, "mantissa_digits": 34,          "lang_pinned": "c",      "encoding": "BID"},
  "libdecquad":         {"conformant": true,  "idiom_peer": false, "mantissa_digits": 34,          "lang_pinned": "c",      "encoding": "DPD"},
  "libmpdecimal":       {"conformant": true,  "idiom_peer": false, "mantissa_digits": "arbitrary", "lang_pinned": "c"},
  "rust_decimal":       {"conformant": false, "idiom_peer": true,  "mantissa_digits": 28,          "lang_pinned": "rust"},
  "System.Decimal":     {"conformant": false, "idiom_peer": true,  "mantissa_digits": 28,          "lang_pinned": "csharp"},
  "Foundation.Decimal": {"conformant": false, "idiom_peer": true,  "mantissa_digits": 38,          "lang_pinned": "swift"},
  "BigDecimal":         {"conformant": false, "idiom_peer": true,  "mantissa_digits": "arbitrary", "lang_pinned": ["java","kotlin"]},
  "decimal.Decimal":    {"conformant": false, "idiom_peer": true,  "mantissa_digits": "arbitrary", "lang_pinned": "python"}
}
```

Note: `BigDecimal` and `decimal.Decimal` are arbitrary-precision ⇒ **no `-` cells** (they can
represent every band, unlike the 28-digit peers). `decimal.Decimal` is the interpreter path over
libmpdec — distinct impl from `libmpdecimal` (direct C); pairing them isolates CPython overhead.

The generator reads this to:
- **Render `-` by absence.** 28-digit peers can't represent OQ/FQ/wide bands ⇒ no record
  exists ⇒ table cell renders `-`. (No hand-entered dashes.)
- **Label the cross-harness caveat automatically.** A pairing whose two records have
  different `lang` is cross-harness (carries the packaging/harness term); same `lang` = clean.
  e.g. `d128@rust vs rust_decimal@rust` = clean; `d128@rust vs libbid@c` = cross-harness.

## 3. Valid (lang, impl) combinations

| impl | langs it appears under |
|---|---|
| d128 | all 9 (c, swift, java, kotlin, rust, go, csharp, zig, python) |
| libbid / libdecquad / libmpdecimal | c only |
| rust_decimal | rust |
| System.Decimal | csharp |
| Foundation.Decimal | swift |
| BigDecimal | java, kotlin |
| decimal.Decimal | python |

9 impls total. (BigDecimal pinned to java+kotlin — same java.math.BigDecimal on the JVM;
say if you want java-only.)

## 4. NOTES
- Impl spellings here differ from the **app-benchmark** tier (which uses
  `decnumber`/`mpdec`/`systemdecimal`/`foundation`/`bigdecimal`). Fine if the two stores stay
  separate; only matters if you'd ever union them.

## 5. What generation looks like (per §4.x table)
- filter records by {op set, cat order, profile, arch, mode}
- for each (op,cat): find the d128 record for the target lang + the chosen peer record
- compute ratio, emit row; missing peer ⇒ `-`
- band matrices (compact d128 P-gen/P-max grids) = same records, different projection
