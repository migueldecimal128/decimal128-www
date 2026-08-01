#!/usr/bin/env python3
"""Three-implementation benchmark tables for the .NET 11 RC 1 DAILY BUILD
26380.103 review edition (SDK 11.0.100-rc.1.26380.103).

DELIBERATELY STANDALONE — this does NOT import gen_bench.py, and that is the point.

This review is a point-in-time artifact: its tables are live for a few weeks and then the
page is archived. gen_bench.py is the long-lived shared generator for the site's benchmark
pages and will keep evolving for years. Decoupling this script means:
  (a) future changes to gen_bench.py can never break an already-archived review, and
  (b) short-lived, review-specific table specs never accrete inside the shared generator.
Each review edition gets its own gen_bench_<edition>.py; when the edition is archived, this
file is archived alongside its page and its frozen data snapshot.

It reads the shared JSONL store in this directory (results.*.jsonl) — the same fact table
gen_bench.py reads — and splices three-column absolute-ns tables into the review page's
marker regions:  <!-- BEGIN GENERATED <id> --> ... <!-- END GENERATED <id> -->
(All prose in the page stays hand-written OUTSIDE the markers.)

Columns (editorial order — system-under-test first):
    Decimal128 (.NET 11)  |  libbid C  |  decimal128-csharp-bid
Changes from the 26376.106 edition: System.Decimal is retired from the cohort, and the
comparison port column is decimal128-csharp-bid (BID128-native in memory) — so all three
columns operate on the BID128 interchange encoding. The Decimal128 (.NET 11) and
decimal128-csharp-bid rows come from the SAME emit run under the SAME rc.1 SDK
(lang=csharp-bid store rows, emit_csharp_bid.py); libbid is C-hosted (runtime-independent).
A cell is the headline ns/op for that impl at that band/arch, or an em dash where no
record exists yet (e.g. x86 rows before the i9 mirror lands).

Usage (run from this directory):
    gen_bench_net11_rc1_26380_103.py --emit  <id>        print one table block to stdout
    gen_bench_net11_rc1_26380_103.py --splice [FILE]     splice all blocks into FILE in place
    gen_bench_net11_rc1_26380_103.py --check  [FILE]     diff each block vs the block in FILE
FILE defaults to the review page (../reviews/dotnet/net11-rc1-26380.103.md).
"""
import json, glob, os, re, sys

HERE   = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.normpath(os.path.join(HERE, "..", "reviews", "dotnet", "net11-rc1-26380.103.md"))

# Columns: (langs, impl, header). `langs` is a priority list of results.<lang>.jsonl files
# to search for the record (first hit wins). The SUT + port pair live in the csharp-bid arm.
# libbid prefers the SAME-SESSION re-measured C arm (lang c-rc1 — exists on x86_64, where
# the i9 shows ~10% day-scale drift and cross-day rows would flatter the comparison) and
# falls back to the standing cross-port C arm (lang c — the arm64 rows; the M3's same-day
# drift is ~0 so cross-day is sound there). Order is editorial: SUT first.
COLS = [(("csharp-bid",), "System.Numerics.Decimal128", "Decimal128 (.NET 11)"),
        (("c-rc1", "c"),  "libbid",                     "libbid C"),
        (("csharp-bid",), "d128",                       "decimal128-csharp-bid")]

# base marker id -> (profile, [(op, cat), ...]). Each base renders for both arches; the x86
# variant uses the "<id>-x86" marker, rendered directly below its arm64 twin.
TABLES = {
  "net11-pfin-abs": ("P-fin", [("add","MIX"),("sub","MIX"),("mul","CP"),("mul","WP"),
                               ("div","CD"),("div","WD"),("div","ET"),("div","PT")]),
  # Add/sub bands are the sign-split ss/os datasets (AddSubSignSplitWorkOrder):
  # each cell is one pure path (ss on add = add path, os on add = subtract path, and
  # mirrored on sub). Same corpus as the 26376.106 edition — comparable to it; NOT
  # comparable to the 26366.102 edition's blended add/sub rows.
  "net11-add-abs":  ("P-gen", [("add", c) for c in ("SQss","SQos","NQss","NQos","MQss","MQos","OQss","OQos","FQss","FQos")]),
  "net11-sub-abs":  ("P-gen", [("sub", c) for c in ("SQss","SQos","NQss","NQos","MQss","MQos","OQss","OQos","FQss","FQos")]),
  "net11-mul-abs":  ("P-gen", [("mul", c) for c in ("CP","WP","XP")]),
  "net11-div-abs":  ("P-gen", [("div", c) for c in ("CD","WD","XD","ET","PT")]),
  "net11-fma-abs":  ("FMA",   [("fma","FN"),("fma","FF")]),
}
ARCHES = [("arm64", ""), ("x86_64", "-x86")]

# Headline mode priority — a value-type port's thru/thru*, then the JVM escape-forced thru‡,
# tte, and the JVM 0-alloc lower bound. (Frozen copy of gen_bench.py's order at split time.)
MODE_PRIORITY = ["thru", "thru*", "thru‡", "tte", "ea"]

def load_store():
    """Upsert every results.<lang>.jsonl into an index keyed by
    (lang,impl,op,cat,profile,mode,arch); last record wins."""
    idx = {}
    for path in sorted(glob.glob(os.path.join(HERE, "results.*.jsonl"))):
        for line in open(path):
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            idx[(r["lang"], r["impl"], r["op"], r["cat"], r["profile"], r["mode"], r["arch"])] = r
    return idx

def get(idx, langs, impl, op, cat, profile, arch):
    for lang in langs:
        for mode in MODE_PRIORITY:
            k = (lang, impl, op, cat, profile, mode, arch)
            if k in idx:
                return idx[k]
    return None

def render(idx, profile, pairs, arch):
    heads = [h for (_l, _i, h) in COLS]
    out = ["| op | cat | " + " | ".join(heads) + " |",
           "|---|---|" + "|".join(["---:"] * len(heads)) + "|"]
    for op, cat in pairs:
        cells = []
        for (lang, impl, _h) in COLS:
            r = get(idx, lang, impl, op, cat, profile, arch)
            cells.append(f"{r['ns']:.2f}" if r else "—")
        out.append(f"| {op} | {cat} | " + " | ".join(cells) + " |")
    return "\n".join(out)

def all_blocks(idx):
    """sid -> rendered table, arm64 and x86_64."""
    blocks = {}
    for base, (profile, pairs) in TABLES.items():
        for arch, suffix in ARCHES:
            blocks[base + suffix] = render(idx, profile, pairs, arch)
    return blocks

def marker_re(sid):
    # (?:...)? — an EMPTY region (BEGIN directly followed by END, as in a fresh
    # scaffold) must also match, else splice silently no-ops on adjacent markers.
    b = re.escape(f"<!-- BEGIN GENERATED {sid} -->")
    e = re.escape(f"<!-- END GENERATED {sid} -->")
    return re.compile(b + r"\n(?:.*?\n)?" + e, re.DOTALL)

def current_block(text, sid):
    m = marker_re(sid).search(text)
    if not m:
        return None
    return m.group(0).split("\n", 1)[1].rsplit("\n", 1)[0].strip("\n")

def splice(text, sid, block):
    # Blank line padding INSIDE the markers so kramdown parses the pipe table as its own block
    # (identical convention to gen_bench.py; current_block strips it back off for --check).
    repl = f"<!-- BEGIN GENERATED {sid} -->\n\n{block}\n\n<!-- END GENERATED {sid} -->"
    new, n = marker_re(sid).subn(lambda _: repl, text)
    if n == 0:
        raise ValueError(f"no marker region for {sid}")
    return new

def main():
    idx = load_store()
    blocks = all_blocks(idx)
    args = sys.argv[1:]
    if not args:
        print(__doc__); return
    if args[0] == "--emit":
        print(blocks[args[1]]); return
    if args[0] in ("--splice", "--check"):
        path = args[1] if len(args) > 1 else TARGET
        text = open(path).read()
        ok = True
        for sid, block in blocks.items():
            if not marker_re(sid).search(text):
                continue
            if args[0] == "--check":
                same = (current_block(text, sid) == block)
                print(f"[{'OK ' if same else 'DIFF'}] {sid}")
                ok = ok and same
            else:
                text = splice(text, sid, block)
        if args[0] == "--splice":
            open(path, "w").write(text)
            print(f"spliced -> {path}")
        else:
            sys.exit(0 if ok else 1)
        return
    sys.stderr.write(f"unknown arg {args[0]}\n"); sys.exit(2)

if __name__ == "__main__":
    main()
