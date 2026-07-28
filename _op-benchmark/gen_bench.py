#!/usr/bin/env python3
"""Generate the benchmark pipe-tables from the JSONL store.

Source of truth = the store in this directory:
  results.<lang>.jsonl   fact table (one record per measured cell; upsert-by-key)
  runs.jsonl             run-id provenance dimension
  impls.json             impl registry (display name, idiom_peer, mantissa, lang_pinned)

Generated tables are spliced inside marker regions
  <!-- BEGIN GENERATED <id> --> ... <!-- END GENERATED <id> -->
into report files that live one level up in this same decimal128-www SITE repo (hub
~/decimal128/www; this store + tooling is the Jekyll-excluded `_op-benchmark/` dir; the
pages publish as Jekyll whitepapers under /benchmark/). Pass the report path to
--splice/--check; all prose (front-matter, intros, captions) stays hand-written OUTSIDE
the markers:
  ../benchmark-vs-<port>.md     PER-LANGUAGE relational tier — one page per port holding that
                                port's finmix + op blocks: pfin-rel-<port>, add/sub/mul/div/fma-rel-<port>
                                (each + its -x86 counterpart). d128 vs alternatives, one language.
  ../benchmark-port-compare.md  band-shape tier — the *-pgen / *-pmax / fma matrix blocks (d128-only, all ports)
--splice/--check operate per FILE and act only on markers present in that FILE (each spec is
skipped where its marker is absent), so a spec renders into whichever report holds its markers.
Regenerate the per-port pages + port-compare (run from this dir; in-repo, same-repo commit):
  for p in c rust zig swift csharp go java kotlin python; do ./gen_bench.py --splice ../benchmark-vs-$p.md; done
  ./gen_bench.py --splice ../benchmark-port-compare.md

Derived at render (never stored): alt / alt_ns / ratio (pair on op,cat,profile,arch),
and the `-` cell (rendered on peer-record absence).

Usage:
  gen_bench.py --emit <id>     print one generated block to stdout
  gen_bench.py --splice FILE   splice every block into FILE in place (markers must exist)
  gen_bench.py --check FILE    diff each generated block vs the block currently in FILE
"""
import json, glob, sys, os, re

HERE = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------------ schema ----
LANGS    = {"c","swift","java","kotlin","rust","go","csharp","zig","python"}
IMPLS    = {"d128","libbid","libdecquad","libmpdecimal","rust_decimal",
            "System.Decimal","System.Numerics.Decimal128","Foundation.Decimal","BigDecimal","decimal.Decimal"}
OPS      = {"add","sub","mul","div","fma","toString","quantize"}
CATS     = {"SQss","SQos","NQss","NQos","MQss","MQos","OQss","OQos","FQss","FQos",
            "CP","WP","XP","CD","WD","XD","PT","ET","FN","FF","MIX"}
PROFILES = {"P-fin","P-gen","P-max","FMA"}
ARCHES   = {"arm64","x86_64"}
MODES    = {"thru","thru*","thru‡","tte","ea"}
REQUIRED = ("lang","impl","op","cat","profile","arch","mode","ns","run")

def validate(r, where=""):
    for k in REQUIRED:
        if k not in r:
            raise ValueError(f"{where}: record missing '{k}': {r}")
    checks = (("lang",LANGS),("impl",IMPLS),("op",OPS),("cat",CATS),
              ("profile",PROFILES),("arch",ARCHES),("mode",MODES))
    for k, dom in checks:
        if r[k] not in dom:
            raise ValueError(f"{where}: '{k}'={r[k]!r} not in domain {sorted(dom)}")
    if not isinstance(r["ns"], (int, float)):
        raise ValueError(f"{where}: ns not numeric: {r}")
    return r

# -------------------------------------------------------------------- load ----
def load_impls():
    return json.load(open(os.path.join(HERE, "impls.json")))

def load_runs():
    # Glob every runs.<arch>.jsonl (the store is arch-split: each box writes only its own
    # arch's provenance file). Run-ids are globally unique across arches, so union by run-id
    # is conflict-free.
    idx = {}
    for p in sorted(glob.glob(os.path.join(HERE, "runs.*.jsonl"))):
        for line in open(p):
            line = line.strip()
            if line:
                r = json.loads(line); idx[r["run"]] = r
    return idx

def load_results():
    """Glob every results.<lang>.<arch>.jsonl (the store is arch-split — each box owns its
    own arch's files), validate, upsert into an index keyed by
    (lang,impl,op,cat,profile,mode,arch) -- one record per cell (last wins)."""
    idx, runs_cited = {}, set()
    for path in sorted(glob.glob(os.path.join(HERE, "results.*.jsonl"))):
        for line in open(path):
            line = line.strip()
            if not line:
                continue
            r = validate(json.loads(line), os.path.basename(path))
            key = (r["lang"],r["impl"],r["op"],r["cat"],r["profile"],r["mode"],r["arch"])
            idx[key] = r
            runs_cited.add(r["run"])
    return idx, runs_cited

def load_annotations():
    """Per-relational-row hand-written notes, keyed by
    (lang,impl,op,cat,profile,mode,arch). Editorial content (not benchmark output)."""
    idx = {}
    p = os.path.join(HERE, "annotations.jsonl")
    if os.path.exists(p):
        for line in open(p):
            line = line.strip()
            if line:
                a = json.loads(line)
                idx[(a["lang"],a["impl"],a["op"],a["cat"],a["profile"],a["mode"],a["arch"])] = a["note"]
    return idx

# ------------------------------------------------------------------ lookup ----
def fmt(x):
    return f"{x:.2f}"

# Headline mode priority: a value-type port's `thru` / `thru*`, then the JVM
# escape-forced `thru‡` headline, `tte`, and finally the JVM `ea` 0-alloc lower
# bound. A JVM cell stores BOTH thru‡ and ea; the headline render picks thru‡.
MODE_PRIORITY = ["thru", "thru*", "thru‡", "tte", "ea"]

def get(idx, lang, impl, op, cat, profile, arch="arm64"):
    """Return the headline record for a cell (mode picked by MODE_PRIORITY).
    None if absent."""
    for mode in MODE_PRIORITY:
        k = (lang,impl,op,cat,profile,mode,arch)
        if k in idx:
            return idx[k]
    return None

def has_any(idx, impl, ops, profile, arch="arm64"):
    """True if the impl has any record for one of `ops` in this profile/arch.
    Op-aware: an idiom peer with add/sub P-gen records must NOT be selected for a
    mul/div group where it has no records."""
    ops = set(ops)
    return any(k[1]==impl and k[2] in ops and k[4]==profile and k[6]==arch for k in idx)

IMPLS_REG = load_impls()
ANNOS = load_annotations()

def idiom_peer_of(lang):
    """The idiom peer impl pinned to this lang (idiom_peer=true), else None."""
    for impl, meta in IMPLS_REG.items():
        if not meta.get("idiom_peer"):
            continue
        lp = meta.get("lang_pinned")
        if lp == lang or (isinstance(lp, list) and lang in lp):
            return impl
    return None

def peer_lang_for(impl, port):
    """Which lang's records hold this peer: C-hosted references live in results.c;
    an idiom peer lives under the port's own lang."""
    return "c" if impl in ("libbid","libdecquad","libmpdecimal") else port

# ------------------------------------------------------------ render: matrix --
JVM = {"java","kotlin"}

# Ports that never fall back to the libbid universal reference: they show their
# in-language idiom peer where it is representable, else "-" (never libbid). go has
# no idiom peer at all ⇒ always "-"; csharp shows System.Decimal on the compact
# bands it can represent and "-" on the wide bands it cannot.
NO_LIBBID_PORTS = {"go", "csharp"}

def render_matrix(idx, spec):
    profile, ports = spec["profile"], spec["ports"]
    arch = spec.get("arch", "arm64")
    # Columns are explicit (op, cat) pairs when given (heterogeneous band sets, e.g.
    # P-fin's add/sub MIX + mul CP/WP + div CD/WD/ET/PT); else the ops×cats product.
    pairs = spec.get("pairs") or [(op, c) for op in spec["ops"] for c in spec["cats"]]
    cols = [f"{op} {c}" for (op, c) in pairs]
    # gather cells (strings), track per-column max width
    labels, rows = [], []
    for port in ports:
        lbl = port + ("‡" if port in JVM else "")
        labels.append(lbl)
        cells = []
        for op, c in pairs:
            r = get(idx, port, "d128", op, c, profile, arch)
            cells.append(fmt(r["ns"]) if r else "—")
        rows.append(cells)
    lw = max(len(l) for l in labels)
    cw = [max(len(rows[i][j]) for i in range(len(rows))) for j in range(len(cols))]
    out = ["| port | " + " | ".join(cols) + " |",
           "|------|" + "|".join(["-------:"]*len(cols)) + "|"]
    for lbl, cells in zip(labels, rows):
        body = "|".join(f" {cells[j]:>{cw[j]}} " for j in range(len(cols)))
        out.append(f"| {lbl:<{lw}}|{body}|")
    return "\n".join(out)

# -------------------------------------------------------- render: relational --
REL_HEADER = "| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |"
REL_SEP    = "|---|---|---|---|---|---|---|---|---|---|---|---|"

def _rel_row(idx, port, impl, op, cat, profile, arch):
    # One relational row for (port, impl, op, cat). impl is None => this cell carries
    # NO alt (d128-only): alt/alt ns/ratio render as "-". Returns [] when the d128 cell
    # itself is absent (so callers can concatenate freely).
    d = get(idx, port, "d128", op, cat, profile, arch)
    if not d:
        return []
    no_alt = impl is None
    disp = "" if no_alt else IMPLS_REG[impl]["display"]
    default_note = "" if no_alt or not IMPLS_REG[impl].get("idiom_peer") else "compact idiom peer"
    plang = None if no_alt else peer_lang_for(impl, port)
    akey_impl = "d128" if no_alt else impl
    p = None if no_alt else get(idx, plang, impl, op, cat, profile, arch)
    anno = ANNOS.get((port, akey_impl, op, cat, profile, d["mode"], arch))
    if p:
        alt, altns = disp, fmt(p["ns"])
        ratio = f"**{p['ns']/d['ns']:.2f}×**"
        row_note = anno if anno is not None else default_note
    else:
        alt, altns, ratio = "-", "-", "-"
        row_note = anno if anno is not None else ""   # note only where authored
    return [f"| {port} | {op} | {cat} | {profile} | {arch} | {d['mode']} | "
            f"{fmt(d['ns'])} | {alt} | {altns} | {ratio} | {d['run']} | {row_note} |"]

def _covering_impls(idx, port, real, op, cat, profile, arch):
    """Which peers to render for one (op,cat) cell: every `real` series peer that has a
    record here (so bare no-peer "-" rows are suppressed where a peer covers the cell);
    or a single [None] d128-only row when NO peer can represent it (e.g. csharp fma, go)."""
    cov = [s for s in real if get(idx, peer_lang_for(s, port), s, op, cat, profile, arch)]
    return cov or [None]

def render_relational(idx, spec):
    """A relational table = one or more row-GROUPS. Each group has its own
    (profile, ops, cats, ports, extra) and its own D1 idiom-peer selection, so a
    swept P-gen group and a fixed-operand P-fin thru* group render in one table.
    Rows are ordered port -> alt -> op -> cat: the idiom/reference peer sweeps all
    ops×cats first, then each `extra` conformant peer does the same (matches
    render_relational_pfin)."""
    arch = spec.get("arch", "arm64")
    groups = spec.get("groups") or [spec]
    out = [REL_HEADER, REL_SEP]
    for g in groups:
        ops, cats, ports, profile = g["ops"], g["cats"], g["ports"], g["profile"]
        for port in ports:
            ip = idiom_peer_of(port)
            if ip and has_any(idx, ip, ops, profile, arch):
                peer = ip
            elif port in NO_LIBBID_PORTS:
                peer = None          # idiom-peer-or-nothing: libbid fallback suppressed
            elif profile == "FMA" and port != "c":
                peer = None          # libbid is a C library, not an FMA alternative a
                                     # rust/zig/swift/java/kotlin programmer can reach; only
                                     # C keeps libbid here (python uses its decimal.Decimal peer)
            else:
                peer = "libbid"
            # real = the reference/idiom peer + this port's conformant extra peers, minus the
            # None placeholder. Each cell renders one row per covering peer (else one d128-only
            # row); rows are then ordered port -> alt -> op -> cat (real peers in series order,
            # the d128-only fallback last).
            real = [s for s in [peer] + [xi for (xl, xi) in g.get("extra", []) if xl == port]
                    if s is not None]
            rows = [(impl, op, cat)
                    for op in ops for cat in cats
                    for impl in _covering_impls(idx, port, real, op, cat, profile, arch)]
            rank = lambda impl: real.index(impl) if impl in real else len(real)
            rows.sort(key=lambda r: (rank(r[0]), ops.index(r[1]), cats.index(r[2])))
            for impl, op, cat in rows:
                out += _rel_row(idx, port, impl, op, cat, profile, arch)
    return "\n".join(out)

# ------------------------------ render: relational, port-major (FinMix / P-fin) --
# Rows ordered by port, then op (add/sub/mul/div), then cat -- NOT op-major like
# render_relational. Each port's peer is chosen ONCE across all ops (idiom peer where
# it has records, else the libbid universal reference, else "-" for the no-fallback
# ports); C additionally carries decQuad + mpdecimal inline per cell. Column 7 is
# headed "ns" (the d128 measurement) rather than "ours" -- FinMix-only; the
# OpBenchmarkResults.md relational tables keep the shared REL_HEADER.
PFIN_REL_HEADER = "| port | op | cat | profile | arch | mode | ns | alt | alt ns | ratio | run | notes |"

def render_relational_pfin(idx, spec):
    arch = spec.get("arch", "arm64")
    profile, ports = spec["profile"], spec["ports"]
    ops_cats, extra = spec["ops_cats"], spec.get("extra", [])
    out = [PFIN_REL_HEADER, REL_SEP]
    for port in ports:
        ip = idiom_peer_of(port)
        # Peer is chosen PER OP (mirrors render_relational's per-group selection): the idiom
        # peer where it has records for THIS op, else the libbid universal reference, else "-"
        # for the no-fallback ports. So e.g. rust's mul (which rust_decimal cannot represent)
        # still falls back to libbid, not "-". Build each op's series, then collect the distinct
        # alts in first-appearance (series) order so we can iterate port -> alt -> op -> cat.
        op_real, alt_order = [], []
        for op, cats in ops_cats:
            if ip and has_any(idx, ip, [op], profile, arch):
                series = [ip]
            elif port in NO_LIBBID_PORTS:
                series = [None]             # idiom-peer-or-nothing: no libbid fallback
            else:
                series = ["libbid"]
            series += [ximpl for (xlang, ximpl) in extra if xlang == port]
            real = [s for s in series if s is not None]
            op_real.append((op, cats, real))
            for s in real:
                if s not in alt_order:
                    alt_order.append(s)
        alt_order.append(None)              # d128-only fallback group sorts last (cells no peer covers)
        # port -> alt -> op -> cat: each alt sweeps every (op it covers)×cat before the next; a
        # cell is rendered under a peer only where that peer actually has a record.
        for alt in alt_order:
            for op, cats, real in op_real:
                for cat in cats:
                    if alt in _covering_impls(idx, port, real, op, cat, profile, arch):
                        out += _rel_row(idx, port, alt, op, cat, profile, arch)
    return "\n".join(out)

def render_fma(idx, spec):
    """d128-only FMA table: FN, FF, FN÷FF (computed), run."""
    ports, arch = spec["ports"], spec.get("arch", "arm64")
    rows = []
    for port in ports:
        lbl = port + ("‡" if port in JVM else "")
        fn = get(idx, port, "d128", "fma", "FN", "FMA", arch)
        ff = get(idx, port, "d128", "fma", "FF", "FMA", arch)
        if not (fn and ff):
            continue
        rows.append((lbl, fmt(fn["ns"]), fmt(ff["ns"]), f"{fn['ns']/ff['ns']:.2f}×", fn["run"]))
    lw = max(len(r[0]) for r in rows)
    w = [max(len(r[i]) for r in rows) for i in range(1, 5)]
    out = ["| port | FN | FF | FN÷FF | run |", "|------|---:|---:|---:|-----|"]
    for lbl, fn, ff, rt, run in rows:
        out.append(f"| {lbl:<{lw}}| {fn:>{w[0]}} | {ff:>{w[1]}} | {rt:>{w[2]}} | {run:<{w[3]}} |")
    return "\n".join(out)

# ---------------------------------------------------------------- specs -------
ALL_PORTS = ["c","rust","zig","swift","csharp","go","java","kotlin","python"]
_REL_PORTS = ["c","rust","zig","swift","csharp","go","java","kotlin","python"]
_REL_EXTRA = [("c","libdecquad"),("c","libmpdecimal")]
# Non-FMA ops additionally show csharp's conformant .NET 11 peer (System.Numerics.Decimal128)
# as an extra row per cell — mirroring how C shows decQuad/mpdecimal alongside its d128 row.
# FMA is excluded: System.Numerics.Decimal128 has no fused multiply-add.
_REL_EXTRA_NONFMA = _REL_EXTRA + [("csharp","System.Numerics.Decimal128")]
SPECS = {
  # 4.1 Add — add-only matrices + relational
  "add-pgen": dict(kind="matrix", profile="P-gen", ops=["add"], cats=["SQss","SQos","NQss","NQos","MQss","MQos","OQss","OQos","FQss","FQos"], ports=ALL_PORTS),
  "add-pmax": dict(kind="matrix", profile="P-max", ops=["add"], cats=["SQss","SQos","OQss","OQos","FQss","FQos"], ports=ALL_PORTS),
  "add-rel":  dict(kind="relational", profile="P-gen", ops=["add"], cats=["SQss","SQos","NQss","NQos","MQss","MQos","OQss","OQos","FQss","FQos"],
                   ports=_REL_PORTS, extra=_REL_EXTRA_NONFMA),
  # 4.2 Subtract — sub-only matrices + relational
  "sub-pgen": dict(kind="matrix", profile="P-gen", ops=["sub"], cats=["SQss","SQos","NQss","NQos","MQss","MQos","OQss","OQos","FQss","FQos"], ports=ALL_PORTS),
  "sub-pmax": dict(kind="matrix", profile="P-max", ops=["sub"], cats=["SQss","SQos","OQss","OQos","FQss","FQos"], ports=ALL_PORTS),
  "sub-rel":  dict(kind="relational", profile="P-gen", ops=["sub"], cats=["SQss","SQos","NQss","NQos","MQss","MQos","OQss","OQos","FQss","FQos"],
                   ports=_REL_PORTS, extra=_REL_EXTRA_NONFMA),
  # 4.3 Multiply — CP·WP·XP matrices + relational. (No P-fin idiom-peer group: the
  # swept CP band's products overflow rust_decimal's 28 digits ⇒ no swept mul peer.)
  "mul-pgen": dict(kind="matrix", profile="P-gen", ops=["mul"], cats=["CP","WP","XP"], ports=ALL_PORTS),
  "mul-pmax": dict(kind="matrix", profile="P-max", ops=["mul"], cats=["XP"], ports=ALL_PORTS),
  "mul-rel":  dict(kind="relational", groups=[
                   dict(profile="P-gen", ops=["mul"], cats=["CP","WP","XP"], ports=_REL_PORTS, extra=_REL_EXTRA_NONFMA),
               ]),
  # Divide — CD·WD·XD·ET·PT matrices + P-gen relational. (No P-fin group: P-fin is
  # unrendered pending a proper per-op P-fin scheme; the P-fin data stays in the store.)
  "div-pgen": dict(kind="matrix", profile="P-gen", ops=["div"], cats=["CD","WD","XD","ET","PT"], ports=ALL_PORTS),
  "div-pmax": dict(kind="matrix", profile="P-max", ops=["div"], cats=["XD"], ports=ALL_PORTS),
  "div-rel":  dict(kind="relational", groups=[
                   dict(profile="P-gen", ops=["div"], cats=["CD","WD","XD","ET","PT"], ports=_REL_PORTS, extra=_REL_EXTRA_NONFMA),
               ]),
  # FMA — d128 band-shape (FN/FF/FN÷FF) matrix + peer relational. The only reachable
  # fused-multiply-add peers are the ones exposed in each language: C libbid/decQuad/mpd
  # + python decimal.Decimal. libbid is NOT borrowed as a universal FMA reference for the
  # other ports (it is a C library no rust/zig/swift/java/kotlin programmer would reach for
  # FMA), so rust/zig/swift/java/kotlin — like go/csharp — show "-" (d128-only).
  "fma":  dict(kind="fma", ports=ALL_PORTS),
  "fma-rel": dict(kind="relational", groups=[
                   dict(profile="FMA", ops=["fma"], cats=["FN","FF"], ports=_REL_PORTS, extra=_REL_EXTRA),
               ]),
  # P-fin financial headline — realistic 64-bit workload: one MIX add/sub stream,
  # mul CP/WP, div CD/WD/ET/PT. The peer head-to-head (ratio to alternatives) is the whole
  # report; the cross-port d128 band-shape matrix was intentionally dropped (FinMix leads with
  # the ratio, not the port-by-port ns spread).
  "pfin-rel": dict(kind="relational_pfin", profile="P-fin", ports=_REL_PORTS, extra=_REL_EXTRA_NONFMA,
                   ops_cats=[("add",["MIX"]),("sub",["MIX"]),
                             ("mul",["CP","WP"]),("div",["CD","WD","ET","PT"])]),
}

# ------------------------------------------------------- per-port projections --
# The relational / finmix reports are published PER LANGUAGE (one benchmark-vs-<port>.md
# page each), not as one all-port document. For every relational base spec we derive a
# port-filtered clone `<base>-<port>` with ports=[port] and its `extra` peer rows narrowed
# to that port -- otherwise render_relational would emit C's decQuad/mpdecimal (or csharp's
# .NET 11 Decimal128) extra rows into every port's page regardless of `ports`. The x86 clone
# loop below then produces `<base>-<port>-x86` for free. The all-port base specs are removed
# afterward: the single-document benchmark-op-results.md / benchmark-finmix.md they fed are
# retired in favour of the per-port pages (band-shape matrices in benchmark-port-compare.md
# are unaffected -- they keep the all-port matrix/fma specs).
import copy as _copy

_REL_BASES = ["pfin-rel", "add-rel", "sub-rel", "mul-rel", "div-rel", "fma-rel"]

def _port_filtered(spec, port):
    s = _copy.deepcopy(spec)
    for holder in [s] + s.get("groups", []):
        if "ports" in holder:
            holder["ports"] = [port]
        if "extra" in holder:
            holder["extra"] = [e for e in holder["extra"] if e[0] == port]
    return s

for _base in _REL_BASES:
    for _port in ALL_PORTS:
        SPECS[f"{_base}-{_port}"] = _port_filtered(SPECS[_base], _port)
    del SPECS[_base]        # retire the all-port document spec

# x86_64 counterparts: clone every spec with arch flipped. Rendered into the
# parallel `<id>-x86` marker regions (matrices honor spec["arch"]; relational and
# fma read spec.get("arch")). Same store, different arch projection. System.Numerics.Decimal128
# is now measured on x86 too (net11 InProcess run xRcs11, 2026-07-20), so the x86 clones keep
# the csharp .NET 11 conformant peer just like arm64 (the arm64-only strip is retired).
for _sid in list(SPECS):
    _x = _copy.deepcopy(SPECS[_sid])
    _x["arch"] = "x86_64"
    SPECS[f"{_sid}-x86"] = _x

_RENDERERS = {"matrix": render_matrix, "relational": render_relational,
              "relational_pfin": render_relational_pfin, "fma": render_fma}

def render(idx, sid):
    spec = SPECS[sid]
    return _RENDERERS[spec["kind"]](idx, spec)

# ------------------------------------------------------------ marker splice ---
def marker_re(sid):
    b = re.escape(f"<!-- BEGIN GENERATED {sid} -->")
    e = re.escape(f"<!-- END GENERATED {sid} -->")
    return re.compile(b + r"\n.*?\n" + e, re.DOTALL)

def current_block(text, sid):
    m = marker_re(sid).search(text)
    if not m:
        return None
    inner = m.group(0).split("\n", 1)[1].rsplit("\n", 1)[0]
    # Tolerate the blank-line padding splice() puts around the table (see below):
    # compare on the bare block so --check stays idempotent for both old and new files.
    return inner.strip("\n")

def splice(text, sid, block):
    # Pad the table with a blank line on each side, INSIDE the markers. kramdown (the
    # Jekyll site's parser) will not recognise a pipe table that sits flush against the
    # preceding `<!-- BEGIN GENERATED -->` HTML comment — it folds the rows into the
    # comment's HTML block and emits raw text instead of a <table>. The blank lines set
    # the table off as its own block so it renders. (current_block strips them back off.)
    repl = f"<!-- BEGIN GENERATED {sid} -->\n\n{block}\n\n<!-- END GENERATED {sid} -->"
    new, n = marker_re(sid).subn(lambda _: repl, text)
    if n == 0:
        raise ValueError(f"no marker region for {sid}")
    return new

# ------------------------------------------------------------------- main -----
def main():
    idx, cited = load_results()
    runs = load_runs()
    missing = cited - set(runs)
    if missing:
        sys.stderr.write(f"WARN: results cite runs with no runs.jsonl entry: {sorted(missing)}\n")
    args = sys.argv[1:]
    if not args:
        print(__doc__); return
    if args[0] == "--emit":
        print(render(idx, args[1]))
    elif args[0] in ("--splice", "--check"):
        path = args[1]
        text = open(path).read()
        ok = True
        for sid in SPECS:
            if not marker_re(sid).search(text):
                continue
            block = render(idx, sid)
            if args[0] == "--check":
                cur = current_block(text, sid)
                same = (cur == block)
                print(f"[{'OK ' if same else 'DIFF'}] {sid}")
                ok = ok and same
            else:
                text = splice(text, sid, block)
        if args[0] == "--splice":
            open(path, "w").write(text)
            print(f"spliced -> {path}")
        else:
            sys.exit(0 if ok else 1)
    else:
        sys.stderr.write(f"unknown arg {args[0]}\n"); sys.exit(2)

if __name__ == "__main__":
    main()
