#!/usr/bin/env python3
"""Phase 4 — python emit. Run decimal128-python benchmark/swept_bench.py 4×
(SWEPT_PROFILE = P-gen/P-fin/P-max/FMA, SWEPT_JSONL=1) in the repo venv, collect
the store-shaped JSON lines it prints, and REWRITE results.python.jsonl (python
arm: C-extension d128 + decimal.Decimal peer where it's add/sub/mul/div). Mints run
Rpysw2 in runs.jsonl.

The harness reads resources/swept/<profile>/<band>.txt, so the binary MUST run with
cwd=<repo> (the resources/ submodule must be bumped to the swept commit).

Usage: emit_python.py [--repo ~/decimal128/python] [--run-id Rpysw2]
"""
import json, os, sys, subprocess, collections

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
    repo = os.path.expanduser("~/decimal128/python")
    run = "Rpysw2"
    a = sys.argv[1:]
    for i, x in enumerate(a):
        if x == "--repo": repo = os.path.expanduser(a[i + 1])
        if x == "--run-id": run = a[i + 1]

    py = os.path.join(repo, ".venv/bin/python")
    harness = os.path.join(repo, "benchmark/swept_bench.py")

    recs = {}
    KEY = lambda r: (r["lang"], r["impl"], r["op"], r["cat"], r["profile"], r["mode"], r["arch"])
    for prof in PROFILES:
        env = dict(os.environ, SWEPT_PROFILE=prof, SWEPT_JSONL="1", SWEPT_RUN=run)
        print(f"running python swept SWEPT_PROFILE={prof} ...", flush=True)
        out = subprocess.run([py, harness], env=env, cwd=repo, text=True,
                             capture_output=True).stdout
        n = 0
        for line in out.splitlines():
            line = line.strip()
            if line.startswith("{"):
                r = json.loads(line); r["arch"] = ARCH; recs[KEY(r)] = r; n += 1
        print(f"   {n} rows")
    print(f"collected {len(recs)} python records")

    KO = ["lang", "impl", "op", "cat", "profile", "arch", "mode", "ns", "run"]
    opo = {"add": 0, "sub": 1, "mul": 2, "div": 3, "fma": 4}
    cato = {c: i for i, c in enumerate(["SQ", "NQ", "MQ", "OQ", "FQ", "CP", "WP", "XP",
                                        "CD", "WD", "XD", "ET", "PT", "FN", "FF", "MIX"])}
    pro = {"P-fin": 0, "P-gen": 1, "P-max": 2, "FMA": 3}
    merged = _merge_store(os.path.join(HERE, "results.python.jsonl"), recs, KEY)
    rows = sorted(merged.values(), key=lambda r: (r["impl"], opo[r["op"]], pro[r["profile"]], cato[r["cat"]]))
    with open(os.path.join(HERE, "results.python.jsonl"), "w") as f:
        for r in rows:
            f.write(json.dumps({k: r[k] for k in KO}, ensure_ascii=False) + "\n")
    print(f"rewrote results.python.jsonl ({len(rows)} records)")

    p = os.path.join(HERE, "runs.jsonl")
    runs = [json.loads(l) for l in open(p).read().splitlines() if l.strip()]
    runs = [r for r in runs if r["run"] != run]
    runs.append({"run": run, "date": "", "machine": MACHINE,
                 "engine": "benchmark/swept_bench.py (C-extension wrapper; timeit autorange>=0.2s + "
                           "median-over-15; `+ - * /` = flag-free _tte operators, FMA via "
                           "DecimalContext.fma = flag-bearing _ctx rung — no bare wrapper FMA). "
                           "ns/op = elapsed/(passes*4096). SWEPT_JSONL emit.",
                 "alternatives": "stdlib decimal.Decimal (libmpdec; IEEE-parity Context prec=34 "
                                 "HALF_EVEN; arbitrary precision ⇒ every add/sub/mul/div band + a true "
                                 "fused FMA peer via Decimal.fma).",
                 "ports": "decimal128-python", "notes": "Phase-4 python emit (emit_python.py); "
                          "P-gen/P-fin/P-max/FMA. Requires resources/ bumped to the swept corpus commit."})
    with open(p, "w") as f:
        for r in runs:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"upserted run '{run}'")
    by = collections.Counter((r["impl"], r["profile"]) for r in recs.values())
    for k in sorted(by):
        print(f"   {k}: {by[k]}")


if __name__ == "__main__":
    main()
