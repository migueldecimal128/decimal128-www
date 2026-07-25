#!/usr/bin/env python3
"""Phase 3 — java emit. Run decimal128-java :benchmark SweptBench 4× via Gradle
(SWEPT_PROFILE, SWEPT_JSONL=1, --no-daemon so env propagates), collect the
store-shaped JSON lines, and REWRITE results.java.jsonl. Two d128 records per cell
(thru‡ headline + ea lower-bound) plus the BigDecimal peer. Mints run Rjasw2.

Usage: emit_java.py [--repo ~/decimal128/java] [--run-id Rjasw2]
"""
# CONTRACT (store-only stage): this emitter writes ONLY the JSONL store
# (results.*.jsonl / runs.*.jsonl). It never writes a report page (*.md) and
# never imports or invokes gen_bench. Splicing reports is a separate stage
# (splice_benchmark_reports.sh / gen_bench.py). See ArchSplitStoreWorkOrder.md.
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
    repo = os.path.expanduser("~/decimal128/java")
    run = "Rjasw2"
    a = sys.argv[1:]
    for i, x in enumerate(a):
        if x == "--repo": repo = os.path.expanduser(a[i+1])
        if x == "--run-id": run = a[i+1]

    recs = {}
    KEY = lambda r: (r["lang"], r["impl"], r["op"], r["cat"], r["profile"], r["mode"], r["arch"])
    for prof in PROFILES:
        env = dict(os.environ, SWEPT_PROFILE=prof, SWEPT_JSONL="1", SWEPT_RUN=run)
        print(f"running java swept SWEPT_PROFILE={prof} (gradle, --no-daemon) ...", flush=True)
        out = subprocess.run(
            ["./gradlew", ":benchmark:run", "-q", "--console=plain", "--no-daemon",
             "-PmainClass=bench.swept.SweptBench"],
            cwd=repo, env=env, text=True, capture_output=True).stdout
        n = 0
        for line in out.splitlines():
            line = line.strip()
            if line.startswith("{"):
                r = json.loads(line); r["arch"] = ARCH; recs[KEY(r)] = r; n += 1
        print(f"   {n} rows")
    print(f"collected {len(recs)} java records")

    KO = ["lang","impl","op","cat","profile","arch","mode","ns","run"]
    opo = {"add":0,"sub":1,"mul":2,"div":3,"fma":4}
    cato = {c:i for i,c in enumerate(["SQ","NQ","MQ","OQ","FQ","CP","WP","XP","CD","WD","XD","ET","PT","FN","FF","MIX"])}
    pro = {"P-fin":0,"P-gen":1,"P-max":2,"FMA":3}
    modo = {"thru‡":0,"ea":1,"thru":2}
    merged = _merge_store(os.path.join(HERE, f"results.java.{ARCH}.jsonl"), recs, KEY)
    rows = sorted(merged.values(), key=lambda r:(r["impl"],opo[r["op"]],pro[r["profile"]],cato[r["cat"]],modo.get(r["mode"],9)))
    with open(os.path.join(HERE, f"results.java.{ARCH}.jsonl"), "w") as f:
        for r in rows:
            f.write(json.dumps({k:r[k] for k in KO}, ensure_ascii=False) + "\n")
    print(f"rewrote results.java.{ARCH}.jsonl ({len(rows)} records)")

    p = os.path.join(HERE, f"runs.{ARCH}.jsonl")
    runs = [json.loads(l) for l in open(p).read().splitlines() if l.strip()]
    runs = [r for r in runs if r["run"] != run]
    runs.append({"run": run, "date": "", "machine": MACHINE,
                 "engine": "benchmark/.../swept/SweptBench.java (manual std-clock, ~300ms OSR warmup + "
                           "min-over-7; _tte add/subtract/multiply/divide); Verify.VERIFY_ENABLED=false. "
                           "TWO d128 records/cell: thru‡ (escape-forced 32B/op reified headline) + ea "
                           "(EA-elided 0-alloc lower bound). SWEPT_JSONL emit.",
                 "alternatives": "java.math.BigDecimal (MathContext.DECIMAL128; arbitrary precision ⇒ every band)",
                 "ports": "decimal128-java", "notes": "Phase-3 java emit (emit_java.py); P-gen/P-fin/P-max/FMA."})
    with open(p, "w") as f:
        for r in runs: f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"upserted run '{run}'")
    by = collections.Counter((r["impl"],r["mode"],r["profile"]) for r in recs.values())
    for k in sorted(by): print(f"   {k}: {by[k]}")

if __name__ == "__main__":
    main()
