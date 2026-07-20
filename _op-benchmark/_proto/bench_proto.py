#!/usr/bin/env python3
"""§4.1 prototype: source data -> JSONL store -> generator reads store -> markdown.
Demonstrates: ratios computed (not stored), one d128 record feeds BOTH the compact
matrix and the relational 'ours' column (dedup), notes driven by the impl registry."""
import json, pathlib

HERE = pathlib.Path(__file__).parent
STORE = HERE / "bench_4_1.jsonl"
OUT = HERE / "gen_4_1.md"

# ---- impl registry (impl-level facts, stored once) ------------------------------
REGISTRY = {
    "d128":               {"idiom_peer": False, "mantissa_digits": 34},
    "libbid":             {"idiom_peer": False, "mantissa_digits": 34},
    "libdecquad":         {"idiom_peer": False, "mantissa_digits": 34},
    "libmpdecimal":       {"idiom_peer": False, "mantissa_digits": "arbitrary"},
    "rust_decimal":       {"idiom_peer": True,  "mantissa_digits": 28},
}

# ---- SOURCE DATA (transcribed from current §4.1) --------------------------------
# d128 P-gen: port -> [add SQ,NQ,MQ,OQ,FQ, sub SQ,NQ,MQ,OQ,FQ]
PGEN = {
 'c':      [2.21,3.88,9.93,11.74,6.53, 1.66,4.03,10.87,12.08,6.84],
 'rust':   [3.08,4.57,13.50,10.59,7.56, 1.87,4.68,13.96,10.68,6.83],
 'zig':    [3.00,5.97,11.78,12.96,7.83, 1.79,5.71,12.34,12.60,7.68],
 'swift':  [4.70,5.95,15.41,17.89,13.41, 2.95,5.41,15.09,18.67,13.56],
 'csharp': [2.18,7.02,17.56,18.96,11.93, 1.47,9.79,11.95,20.14,9.19],
 'go':     [4.49,9.77,21.64,33.38,20.12, 2.98,9.75,21.04,33.18,19.49],
 'java':   [5.45,6.78,12.00,19.97,14.30, 4.49,7.34,12.40,20.12,14.66],
 'kotlin': [6.08,7.06,13.37,23.60,15.57, 4.65,7.32,13.67,24.24,14.94],
}
# d128 P-max: port -> [add SQ,OQ,FQ, sub SQ,OQ,FQ]
PMAX = {
 'c':      [3.53,18.19,7.28, 3.24,17.92,7.07],
 'rust':   [5.11,12.79,6.44, 3.87,12.82,6.64],
 'zig':    [4.01,16.47,8.55, 3.73,15.78,7.19],
 'swift':  [6.46,22.50,13.35, 4.63,22.36,11.97],
 'csharp': [6.02,23.17,9.13, 3.68,24.72,6.83],
 'go':     [7.15,42.48,18.89, 5.97,42.99,18.72],
 'java':   [6.74,19.88,16.29, 6.41,20.02,15.86],
 'kotlin': [7.27,21.00,11.21, 7.02,21.27,11.56],
}
# peers: impl -> (lang, P-gen {add:[..],sub:[..]}, P-max {add:[SQ,OQ,FQ],sub:[..]} or None, cats)
PEERS = {
 'libbid':      ('c',    {'add':[8.43,8.38,8.58,13.75,10.36],'sub':[9.89,11.66,10.39,14.86,12.30]},
                         {'add':[7.84,16.99,8.03],'sub':[8.21,18.31,9.00]}, ['SQ','NQ','MQ','OQ','FQ']),
 'libdecquad':  ('c',    {'add':[19.96,29.66,28.18,34.53,26.32],'sub':[22.17,33.85,30.13,36.84,29.97]},
                         {'add':[30.34,38.55,24.08],'sub':[30.72,41.12,27.71]}, ['SQ','NQ','MQ','OQ','FQ']),
 'libmpdecimal':('c',    {'add':[12.48,26.76,26.75,44.67,39.16],'sub':[14.31,21.22,20.51,44.55,39.13]},
                         {'add':[15.38,70.66,32.19],'sub':[15.85,71.61,33.19]}, ['SQ','NQ','MQ','OQ','FQ']),
 'rust_decimal':('rust', {'add':[4.03,5.26,5.31],'sub':[3.29,5.12,5.42]}, None, ['SQ','NQ','MQ']),
}
PORTS = ['c','rust','zig','swift','csharp','go','java','kotlin']
JVM = {'java','kotlin'}
CATS_PGEN = ['SQ','NQ','MQ','OQ','FQ']
CATS_PMAX = ['SQ','OQ','FQ']
run_for = lambda cat: 'Rc' if cat in ('OQ','FQ') else 'Rprof'

# ---- 1. BUILD THE STORE (write JSONL) -------------------------------------------
def build_store():
    recs = []
    def rec(lang, impl, op, cat, profile, ns):
        mode = 'thru‡' if (impl == 'd128' and lang in JVM) else 'thru'
        recs.append({"lang":lang,"impl":impl,"op":op,"cat":cat,"profile":profile,
                     "arch":"arm64","mode":mode,"ns":ns,"run":run_for(cat)})
    for port in PORTS:
        for oi, op in enumerate(('add','sub')):
            for ci, cat in enumerate(CATS_PGEN):
                rec(port,'d128',op,cat,'P-gen',PGEN[port][oi*5+ci])
            for ci, cat in enumerate(CATS_PMAX):
                rec(port,'d128',op,cat,'P-max',PMAX[port][oi*3+ci])
    for impl,(lang,pg,pm,cats) in PEERS.items():
        for op in ('add','sub'):
            for ci, cat in enumerate(cats):
                rec(lang,impl,op,cat,'P-gen',pg[op][ci])
            if pm:
                for ci, cat in enumerate(CATS_PMAX):
                    rec(lang,impl,op,cat,'P-max',pm[op][ci])
    with open(STORE,'w') as f:
        for r in recs: f.write(json.dumps(r,ensure_ascii=False)+"\n")
    return len(recs)

# ---- 2. GENERATOR (reads ONLY the JSONL) ----------------------------------------
def load():
    idx = {}
    for line in open(STORE):
        r = json.loads(line)
        idx[(r['lang'],r['impl'],r['op'],r['cat'],r['profile'])] = r
    return idx

def fmt(x): return f"{x:.2f}"

def compact_matrix(idx, profile, cats, title):
    cols = [f"{op} {c}" for op in ('add','sub') for c in cats]
    out = [f"**{title}**\n", "| port | "+" | ".join(cols)+" |",
           "|------|"+"|".join(["-------:"]*len(cols))+"|"]
    for port in PORTS:
        lbl = port+('‡' if port in JVM else '')
        cells = []
        for op in ('add','sub'):
            for c in cats:
                r = idx.get((port,'d128',op,c,profile))
                cells.append(fmt(r['ns']) if r else '—')
        out.append(f"| {lbl:<6}| "+" | ".join(cells)+" |")
    return "\n".join(out)

def relational(idx):
    out = ["| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |",
           "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    # (port_lang, peer_impl) pairs, in report order
    pairs = ([(p,'libbid') for p in ['c','rust','zig','swift','csharp','go']]
             + [('c','libdecquad'),('c','libmpdecimal'),('rust','rust_decimal')])
    for lang, impl in pairs:
        peer_lang = PEERS[impl][0]
        cats = PEERS[impl][3]
        note = "compact idiom peer" if REGISTRY[impl]['idiom_peer'] else ""
        for op in ('add','sub'):
            for cat in cats:
                d = idx.get((lang,'d128',op,cat,'P-gen'))
                p = idx.get((peer_lang,impl,op,cat,'P-gen'))
                if not d: continue
                if p:
                    ratio = f"**{p['ns']/d['ns']:.2f}×**"; altns = fmt(p['ns'])
                else:
                    ratio = "-"; altns = "-"          # <- '-' by absence
                out.append(f"| {lang} | {op} | {cat} | P-gen | arm64 | {d['mode']} | "
                           f"{fmt(d['ns'])} | {impl} | {altns} | {ratio} | {run_for(cat)} | {note} |")
    return "\n".join(out)

def generate():
    idx = load()
    parts = [
        "### 4.1 (GENERATED from bench_4_1.jsonl) — Add / Subtract\n",
        compact_matrix(idx,'P-gen',CATS_PGEN,"P-gen — d128 (ns/op)."), "",
        compact_matrix(idx,'P-max',CATS_PMAX,"P-max — d128 (ns/op):"), "",
        "**Relational — d128 vs peers** (ratio = peer/ours, computed; missing peer ⇒ `-`):\n",
        relational(idx),
    ]
    OUT.write_text("\n".join(parts)+"\n")
    return OUT.read_text()

if __name__ == "__main__":
    n = build_store()
    print(f"# store: {n} records -> {STORE.name}\n")
    print(generate())
