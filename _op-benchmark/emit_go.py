#!/usr/bin/env python3
"""Phase 3 — go emit (d128-only). Runs `go test -bench=^BenchmarkSwept$` 4×
(SWEPT_PROFILE = P-gen/P-fin/P-max/FMA), parses the `BenchmarkSwept/<op>/<band>`
ns/op lines, and REWRITES results.go.jsonl. The swept_bench_test.go harness uses
Go's auto-scaling `for b.Loop()` (each body = one op cycling through the 4096-pair
corpus), so the reported ns/op is the swept per-op average over an auto-sized
iteration count. That REQUIRES a real -benchtime (default 1s) — NOT -benchtime=1x,
which would run the body exactly once and report a single cold sample (garbage).
Mints run Rgosw2 (arm64) / pass --run-id xRgosw2 on x86.

Usage: emit_go.py [--crate ~/decimal128/go] [--run-id Rgosw2] [--benchtime 1s]
"""
# CONTRACT (store-only stage): this emitter writes ONLY the JSONL store
# (results.*.jsonl / runs.*.jsonl). It never writes a report page (*.md) and
# never imports or invokes gen_bench. Splicing reports is a separate stage
# (splice_benchmark_reports.sh / gen_bench.py). See ArchSplitStoreWorkOrder.md.
import json, os, sys, re, subprocess, collections

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
LINE_RE = re.compile(r"BenchmarkSwept/(add|sub|mul|div|fma)/(\w+)-\d+\s+\d+\s+([\d.]+)\s+ns/op")

def main():
    crate = os.path.expanduser("~/decimal128/go")
    run = "Rgosw2"; benchtime = "1s"
    a = sys.argv[1:]
    for i, x in enumerate(a):
        if x == "--crate": crate = os.path.expanduser(a[i+1])
        if x == "--run-id": run = a[i+1]
        if x == "--benchtime": benchtime = a[i+1]

    recs = {}
    KEY = lambda r: (r["lang"], r["impl"], r["op"], r["cat"], r["profile"], r["mode"], r["arch"])
    for prof in PROFILES:
        env = dict(os.environ, SWEPT_PROFILE=prof)
        print(f"running go bench SWEPT_PROFILE={prof} ...", flush=True)
        out = subprocess.run(["go", "test", "-bench=^BenchmarkSwept$", "-run=^$",
                              f"-benchtime={benchtime}"], cwd=crate, env=env,
                             text=True, capture_output=True).stdout
        n = 0
        for op, band, ns in LINE_RE.findall(out):
            profile = "FMA" if op == "fma" else prof
            recs[KEY(dict(lang="go", impl="d128", op=op, cat=band, profile=profile, mode="thru", arch=ARCH))] = \
                dict(lang="go", impl="d128", op=op, cat=band, profile=profile,
                     arch=ARCH, mode="thru", ns=round(float(ns), 2), run=run)
            n += 1
        print(f"   {n} rows")
    print(f"collected {len(recs)} go records")

    KO = ["lang","impl","op","cat","profile","arch","mode","ns","run"]
    opo = {"add":0,"sub":1,"mul":2,"div":3,"fma":4}
    cato = {c:i for i,c in enumerate(["SQ","NQ","MQ","OQ","FQ","CP","WP","XP","CD","WD","XD","ET","PT","FN","FF","MIX"])}
    pro = {"P-fin":0,"P-gen":1,"P-max":2,"FMA":3}
    merged = _merge_store(os.path.join(HERE, f"results.go.{ARCH}.jsonl"), recs, KEY)
    rows = sorted(merged.values(), key=lambda r:(r["impl"],opo[r["op"]],pro[r["profile"]],cato[r["cat"]]))
    with open(os.path.join(HERE, f"results.go.{ARCH}.jsonl"), "w") as f:
        for r in rows:
            f.write(json.dumps({k:r[k] for k in KO}, ensure_ascii=False) + "\n")
    print(f"rewrote results.go.{ARCH}.jsonl ({len(rows)} records)")

    p = os.path.join(HERE, f"runs.{ARCH}.jsonl")
    runs = [json.loads(l) for l in open(p).read().splitlines() if l.strip()]
    runs = [r for r in runs if r["run"] != run]
    runs.append({"run": run, "date": "", "machine": MACHINE,
                 "engine": "swept_bench_test.go (testing.B; auto-scaling `for b.Loop()` mean over "
                           "the 4096-pair swept corpus, _tte Add/Sub/Mul/Quo); "
                           "go test -bench=^BenchmarkSwept$ -benchtime=1s",
                 "alternatives": "none (d128-only)", "ports": "decimal128-go",
                 "notes": "Phase-3 go emit (emit_go.py); P-gen/P-fin/P-max/FMA."})
    with open(p, "w") as f:
        for r in runs: f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"upserted run '{run}'")
    by = collections.Counter((r["impl"],r["profile"]) for r in recs.values())
    for k in sorted(by): print(f"   {k}: {by[k]}")

if __name__ == "__main__":
    main()
