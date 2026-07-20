#!/usr/bin/env python3
"""Phase 3 — zig emit (d128-only). Build + run decimal128-zig bench/swept.zig 4×
(SWEPT_PROFILE, SWEPT_JSONL=1), collect the store-shaped JSON lines (zig prints via
std.debug.print → stderr), and REWRITE results.zig.jsonl. Mints run Rzgsw2.

Usage: emit_zig.py [--crate ~/decimal128/zig] [--run-id Rzgsw2]
"""
import json, os, sys, subprocess, glob, collections

HERE = os.path.dirname(os.path.abspath(__file__))

import platform


def _host_arch():
    m = platform.machine().lower()
    return {"amd64": "x86_64", "x64": "x86_64", "x86_64": "x86_64",
            "aarch64": "arm64", "arm64": "arm64"}.get(m, m)


ARCH = _host_arch()
MACHINE = (f"Intel Core i9-9880H ({os.cpu_count()} cpus), x86_64"
           if ARCH == "x86_64" else "Apple M3 Pro (12 cores), arm64")


def _merge_store(path, recs, KEY):
    """Fold this run's recs into the on-disk store, upsert by KEY so other-arch
    and unmeasured rows survive (no clobber). Returns the merged dict."""
    store = {}
    if os.path.exists(path):
        for _l in open(path):
            _l = _l.strip()
            if _l:
                _e = json.loads(_l)
                store[KEY(_e)] = _e
    store.update(recs)
    return store
PROFILES = ["P-gen", "P-fin", "P-max", "FMA"]

def main():
    crate = os.path.expanduser("~/decimal128/zig")
    run = "Rzgsw2"
    a = sys.argv[1:]
    for i, x in enumerate(a):
        if x == "--crate": crate = os.path.expanduser(a[i+1])
        if x == "--run-id": run = a[i+1]

    # build (this also runs it once in human mode; we ignore that) then find freshest binary
    subprocess.run(["zig", "build", "swept", "-Doptimize=ReleaseFast"],
                   cwd=crate, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    bins = glob.glob(os.path.join(crate, ".zig-cache/o/*/swept"))
    binary = max((b for b in bins if os.access(b, os.X_OK)), key=os.path.getmtime)
    print(f"binary: {binary}")

    recs = {}
    KEY = lambda r: (r["lang"], r["impl"], r["op"], r["cat"], r["profile"], r["mode"], r["arch"])
    for prof in PROFILES:
        env = dict(os.environ, SWEPT_PROFILE=prof, SWEPT_JSONL="1", SWEPT_RUN=run)
        print(f"running zig swept SWEPT_PROFILE={prof} ...", flush=True)
        p = subprocess.run([binary], env=env, text=True, capture_output=True, cwd=crate)
        n = 0
        for line in (p.stdout + p.stderr).splitlines():
            line = line.strip()
            if line.startswith("{"):
                r = json.loads(line); r["arch"] = ARCH; recs[KEY(r)] = r; n += 1
        print(f"   {n} rows")
    print(f"collected {len(recs)} zig records")

    KO = ["lang","impl","op","cat","profile","arch","mode","ns","run"]
    opo = {"add":0,"sub":1,"mul":2,"div":3,"fma":4}
    cato = {c:i for i,c in enumerate(["SQ","NQ","MQ","OQ","FQ","CP","WP","XP","CD","WD","XD","ET","PT","FN","FF","MIX"])}
    pro = {"P-fin":0,"P-gen":1,"P-max":2,"FMA":3}
    merged = _merge_store(os.path.join(HERE, "results.zig.jsonl"), recs, KEY)
    rows = sorted(merged.values(), key=lambda r:(r["impl"],opo[r["op"]],pro[r["profile"]],cato[r["cat"]]))
    with open(os.path.join(HERE, "results.zig.jsonl"), "w") as f:
        for r in rows:
            f.write(json.dumps({k:r[k] for k in KO}, ensure_ascii=False) + "\n")
    print(f"rewrote results.zig.jsonl ({len(rows)} records)")

    p = os.path.join(HERE, "runs.jsonl")
    runs = [json.loads(l) for l in open(p).read().splitlines() if l.strip()]
    runs = [r for r in runs if r["run"] != run]
    runs.append({"run": run, "date": "", "machine": MACHINE,
                 "engine": "bench/swept.zig (manual std-clock, ~30ms/measurement min-over-reps, "
                           "doNotOptimizeAway; _tte rung); SWEPT_JSONL emit",
                 "alternatives": "none (d128-only)", "ports": "decimal128-zig",
                 "notes": "Phase-3 zig emit (emit_zig.py); P-gen/P-fin/P-max/FMA."})
    with open(p, "w") as f:
        for r in runs: f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"upserted run '{run}'")
    by = collections.Counter((r["impl"],r["profile"]) for r in recs.values())
    for k in sorted(by): print(f"   {k}: {by[k]}")

if __name__ == "__main__":
    main()
