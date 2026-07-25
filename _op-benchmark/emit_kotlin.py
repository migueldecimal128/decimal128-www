#!/usr/bin/env python3
"""Phase 3 — kotlin emit. Run decimal128-kotlin :core:jvmTest SweptBenchTest 4×
via Gradle (SWEPT_PROFILE, SWEPT_JSONL_OUT=<file> since test stdout is buffered,
--rerun-tasks to defeat test caching, --no-daemon so env propagates), read the
per-profile JSONL files, and REWRITE results.kotlin.jsonl. Two d128 records/cell
(thru‡ + ea) plus the BigDecimal peer. Mints run Rkosw2.

Usage: emit_kotlin.py [--repo ~/decimal128/kotlin] [--run-id Rkosw2]
"""
# CONTRACT (store-only stage): this emitter writes ONLY the JSONL store
# (results.*.jsonl / runs.*.jsonl). It never writes a report page (*.md) and
# never imports or invokes gen_bench. Splicing reports is a separate stage
# (splice_benchmark_reports.sh / gen_bench.py). See ArchSplitStoreWorkOrder.md.
import json, os, sys, subprocess, collections, tempfile

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
    repo = os.path.expanduser("~/decimal128/kotlin")
    run = "Rkosw2"
    a = sys.argv[1:]
    for i, x in enumerate(a):
        if x == "--repo": repo = os.path.expanduser(a[i+1])
        if x == "--run-id": run = a[i+1]

    recs = {}
    KEY = lambda r: (r["lang"], r["impl"], r["op"], r["cat"], r["profile"], r["mode"], r["arch"])
    for prof in PROFILES:
        out = os.path.join(tempfile.gettempdir(), f"_kotlin_{prof}.jsonl")
        try: os.remove(out)
        except FileNotFoundError: pass
        env = dict(os.environ, SWEPT_PROFILE=prof, SWEPT_JSONL_OUT=out, SWEPT_RUN=run)
        print(f"running kotlin swept SWEPT_PROFILE={prof} (gradle jvmTest --rerun-tasks) ...", flush=True)
        subprocess.run(["./gradlew", ":core:jvmTest", "--tests", "com.decimal128.kotlin.SweptBenchTest",
                        "--rerun-tasks", "-q", "--console=plain", "--no-daemon"],
                       cwd=repo, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        n = 0
        if os.path.exists(out):
            for line in open(out):
                line = line.strip()
                if line.startswith("{"):
                    r = json.loads(line); r["arch"] = ARCH; recs[KEY(r)] = r; n += 1
        print(f"   {n} rows")
    print(f"collected {len(recs)} kotlin records")

    KO = ["lang","impl","op","cat","profile","arch","mode","ns","run"]
    opo = {"add":0,"sub":1,"mul":2,"div":3,"fma":4}
    cato = {c:i for i,c in enumerate(["SQ","NQ","MQ","OQ","FQ","CP","WP","XP","CD","WD","XD","ET","PT","FN","FF","MIX"])}
    pro = {"P-fin":0,"P-gen":1,"P-max":2,"FMA":3}
    modo = {"thru‡":0,"ea":1,"thru":2}
    merged = _merge_store(os.path.join(HERE, f"results.kotlin.{ARCH}.jsonl"), recs, KEY)
    rows = sorted(merged.values(), key=lambda r:(r["impl"],opo[r["op"]],pro[r["profile"]],cato[r["cat"]],modo.get(r["mode"],9)))
    with open(os.path.join(HERE, f"results.kotlin.{ARCH}.jsonl"), "w") as f:
        for r in rows:
            f.write(json.dumps({k:r[k] for k in KO}, ensure_ascii=False) + "\n")
    print(f"rewrote results.kotlin.{ARCH}.jsonl ({len(rows)} records)")

    p = os.path.join(HERE, f"runs.{ARCH}.jsonl")
    runs = [json.loads(l) for l in open(p).read().splitlines() if l.strip()]
    runs = [r for r in runs if r["run"] != run]
    runs.append({"run": run, "date": "", "machine": MACHINE,
                 "engine": "core/.../SweptBenchTest.kt (JVM test; manual std-clock ~300ms warmup + min-over-7; "
                           "_tte + - * /); VERIFY_ENABLED=false. TWO d128 records/cell: thru‡ (escape-forced "
                           "reified headline) + ea (0-alloc lower bound). SWEPT_JSONL_OUT file emit.",
                 "alternatives": "java.math.BigDecimal (MathContext.DECIMAL128; arbitrary precision ⇒ every band)",
                 "ports": "decimal128-kotlin", "notes": "Phase-3 kotlin emit (emit_kotlin.py); P-gen/P-fin/P-max/FMA."})
    with open(p, "w") as f:
        for r in runs: f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"upserted run '{run}'")
    by = collections.Counter((r["impl"],r["mode"],r["profile"]) for r in recs.values())
    for k in sorted(by): print(f"   {k}: {by[k]}")

if __name__ == "__main__":
    main()
