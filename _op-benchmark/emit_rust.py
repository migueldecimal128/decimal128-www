#!/usr/bin/env python3
"""Phase 3 — rust emit. Build + run decimal128-rust benches/swept.rs 4×
(SWEPT_PROFILE = P-gen/P-fin/P-max/FMA, SWEPT_JSONL=1), collect the store-shaped
JSON lines it prints, and REWRITE results.rust.jsonl (rust arm: d128 + rust_decimal
peer where representable). Mints run Rrsw2 in runs.jsonl.

Usage: emit_rust.py [--crate ~/decimal128/rust] [--run-id Rrsw2]
"""
# CONTRACT (store-only stage): this emitter writes ONLY the JSONL store
# (results.*.jsonl / runs.*.jsonl). It never writes a report page (*.md) and
# never imports or invokes gen_bench. Splicing reports is a separate stage
# (splice_benchmark_reports.sh / gen_bench.py). See ArchSplitStoreWorkOrder.md.
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

def sh(cmd, **kw):
    return subprocess.run(cmd, check=True, text=True, capture_output=True, **kw)

def _os_desc():
    rel = platform.mac_ver()[0]
    return f"macOS {rel} [Darwin {platform.release()}]" if rel else platform.platform()


def _tool_version(cmd, cwd=None):
    """First line of a toolchain version probe (e.g. `go version`).

    Provenance only: returns "unknown" rather than failing the run if the probe
    errors. Pinning the exact build matters because a compiler or runtime bump
    can move a number severalfold with no source change (a .NET preview bump
    once moved a peer's divide 4x while the port held flat) — a run record that
    names only the major version cannot tell those pictures apart.
    """
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=120, cwd=cwd)
        out = ((r.stdout or "") + (r.stderr or "")).strip()
        return out.splitlines()[0].strip() if r.returncode == 0 and out else "unknown"
    except Exception:
        return "unknown"


def main():
    crate = os.path.expanduser("~/decimal128/rust")
    run = "Rrsw2"
    a = sys.argv[1:]
    for i, x in enumerate(a):
        if x == "--crate": crate = os.path.expanduser(a[i+1])
        if x == "--run-id": run = a[i+1]

    sh(["cargo", "build", "--release", "--bench", "swept"], cwd=crate)
    bins = [b for b in glob.glob(os.path.join(crate, "target/release/deps/swept-*")) if not b.endswith(".d")]
    binary = max(bins, key=os.path.getmtime)
    print(f"binary: {binary}")

    recs = {}
    KEY = lambda r: (r["lang"], r["impl"], r["op"], r["cat"], r["profile"], r["mode"], r["arch"])
    for prof in PROFILES:
        env = dict(os.environ, SWEPT_PROFILE=prof, SWEPT_JSONL="1", SWEPT_RUN=run)
        print(f"running rust swept SWEPT_PROFILE={prof} ...", flush=True)
        out = subprocess.run([binary], env=env, check=True, text=True, capture_output=True).stdout
        n = 0
        for line in out.splitlines():
            line = line.strip()
            if line.startswith("{"):
                r = json.loads(line); r["arch"] = ARCH; recs[KEY(r)] = r; n += 1
        print(f"   {n} rows")
    print(f"collected {len(recs)} rust records")

    KO = ["lang","impl","op","cat","profile","arch","mode","ns","run"]
    opo = {"add":0,"sub":1,"mul":2,"div":3,"fma":4}
    cato = {c:i for i,c in enumerate(["SQ","NQ","MQ","OQ","FQ","CP","WP","XP","CD","WD","XD","ET","PT","FN","FF","MIX"])}
    pro = {"P-fin":0,"P-gen":1,"P-max":2,"FMA":3}
    merged = _merge_store(os.path.join(HERE, f"results.rust.{ARCH}.jsonl"), recs, KEY)
    rows = sorted(merged.values(), key=lambda r:(r["impl"],opo[r["op"]],pro[r["profile"]],cato[r["cat"]]))
    with open(os.path.join(HERE, f"results.rust.{ARCH}.jsonl"), "w") as f:
        for r in rows:
            f.write(json.dumps({k:r[k] for k in KO}, ensure_ascii=False) + "\n")
    print(f"rewrote results.rust.{ARCH}.jsonl ({len(rows)} records)")

    # mint run
    p = os.path.join(HERE, f"runs.{ARCH}.jsonl")
    runs = [json.loads(l) for l in open(p).read().splitlines() if l.strip()]
    runs = [r for r in runs if r["run"] != run]
    toolchain = f"{_os_desc()}; {_tool_version(['rustc', '--version'])}."
    runs.append({"run": run, "date": "", "machine": MACHINE,
                 "os_toolchain": toolchain,
                 "engine": "benches/swept.rs (manual std::time, min-over-reps, black_box; _tte rung; "
                           "ns/op=elapsed/(PASSES*4096)); SWEPT_JSONL emit",
                 "alternatives": "rust_decimal 1.x (28-digit idiom peer, swept where every result stays representable)",
                 "ports": "decimal128-rust", "notes": "Phase-3 rust emit (emit_rust.py); P-gen/P-fin/P-max/FMA."})
    with open(p, "w") as f:
        for r in runs: f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"upserted run '{run}'")
    by = collections.Counter((r["impl"],r["profile"]) for r in recs.values())
    for k in sorted(by): print(f"   {k}: {by[k]}")

if __name__ == "__main__":
    main()
