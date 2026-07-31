#!/usr/bin/env python3
"""Phase 2 — C reference emitter.

Runs the decimal128-c Google Benchmark suite 3x (SWEPT_PROFILE = P-gen / P-fin / P-max),
reshapes benchmarks[].name -> store records, and REWRITES results.c.jsonl (the C arm is
fully emit-owned: d128 + libbid + decQuad + mpdecimal). Mints a fresh run in runs.jsonl.

ns/op = 1e9 / items_per_second  (SetItemsProcessed basis = iterations * dataset.size(),
and dataset.size() == kDefaultN == 4096, so items_per_second is per-OP — verified).
Runs 15 repetitions with --benchmark_report_aggregates_only and reads the MEDIAN
aggregate (the cross-port estimator; 1e9/median(ips) == median(ns) by monotonicity).

d128 rung per the Rprof methodology: add/sub via the flag-free `_tte` rung, mul/div via the
plain `_ctx` arm (no per-band _tte exists for mul/div), FMA via `fma_{FN,FF}_tte`.
Peers (libbid/decq/mpd) via the plain per-band benchmark.

Usage: emit_c.py <bench_binary> [--run-id Rc2] [--min-time 0.05s] [--no-build]

Rebuilds the binary from its CMake build tree first (walks up to CMakeCache.txt);
--no-build measures the binary as-is.
"""
# CONTRACT (store-only stage): this emitter writes ONLY the JSONL store
# (results.*.jsonl / runs.*.jsonl). It never writes a report page (*.md) and
# never imports or invokes gen_bench. Splicing reports is a separate stage
# (splice_benchmark_reports.sh / gen_bench.py). See ArchSplitStoreWorkOrder.md.
import json, re, sys, os, subprocess, glob, collections

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
PROFILES = ["P-gen", "P-fin", "P-max", "FMA"]   # FMA is its own SWEPT_PROFILE (FN/FF regimes)
IMPL = {"d128": "d128", "libbid": "libbid", "decq": "libdecquad", "mpd": "libmpdecimal"}
BAND_RE = re.compile(r"^BM_(d128|libbid|decq|mpd)_(add|sub|mul|div)_"
                     r"((?:SQ|NQ|MQ|OQ|FQ)_(?:ss|os)|MIX|CP|WP|XP|CD|WD|XD|ET|PT)(_tte|_rnd)?$")
# FMA now carries peers: d128 via the flag-free _tte rung, libbid/decq/mpd via their
# native fused multiply-add (__bid128_fma / decQuadFMA / mpd_qfma), plain (no suffix).
FMA_RE  = re.compile(r"^BM_(d128|libbid|decq|mpd)_fma_(FN|FF)(_tte)?$")

def _git_head(path):
    """Short HEAD of the benchmarked port repo, '+dirty' if TRACKED files differ.

    A run record that names only the arm cannot tell two engine states apart;
    the commit is what makes a number reproducible. Untracked files are ignored
    (-uno) on purpose: build trees (build-bench/, bin/, obj/) live inside the port
    repos and would otherwise mark every run dirty. `git -C` resolves the enclosing
    repo, so any path inside the port works."""
    try:
        h = subprocess.run(["git", "-C", path, "rev-parse", "--short", "HEAD"],
                           capture_output=True, text=True, timeout=60)
        if h.returncode != 0:
            return "unknown"
        s = subprocess.run(["git", "-C", path, "status", "--porcelain", "-uno"],
                           capture_output=True, text=True, timeout=60)
        return h.stdout.strip() + ("+dirty" if (s.stdout or "").strip() else "")
    except Exception:
        return "unknown"


def _os_desc():
    rel = platform.mac_ver()[0]
    return f"macOS {rel} [Darwin {platform.release()}]" if rel else platform.platform()


def _tool_version(cmd, cwd=None):
    """First line of a toolchain version probe. Provenance only — returns
    "unknown" rather than failing the run if the probe errors."""
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=120, cwd=cwd)
        out = ((r.stdout or "") + (r.stderr or "")).strip()
        return out.splitlines()[0].strip() if r.returncode == 0 and out else "unknown"
    except Exception:
        return "unknown"


def _c_build_flags(binary):
    """How the bench binary was actually configured, read from the CMakeCache
    beside it (walking up from the binary; typically <build>/benchmark/<bin>).

    Recorded because the flags silently decide what the numbers mean: the root
    CMakeLists appends -flto only to CMAKE_C/CXX_FLAGS_RELEASE, so a build with
    an empty CMAKE_BUILD_TYPE gets NO LTO and understates d128 by ~1.5x. A run
    record carrying the flags makes that visible instead of invisible."""
    d = os.path.dirname(os.path.abspath(binary))
    for _ in range(4):
        cache = os.path.join(d, "CMakeCache.txt")
        if os.path.exists(cache):
            want = {"CMAKE_BUILD_TYPE": None, "CMAKE_C_FLAGS": None, "DECIMAL128C_NO_LTO": None}
            for ln in open(cache, errors="replace"):
                k = ln.split(":", 1)[0]
                if k in want and want[k] is None and "=" in ln:
                    want[k] = ln.split("=", 1)[1].strip()
            bt = want["CMAKE_BUILD_TYPE"] or "(none)"
            cf = want["CMAKE_C_FLAGS"] or ""
            lto = ("thin-LTO" if "-flto=thin" in cf else
                   "full-LTO" if "-flto" in cf else
                   "LTO via Release" if bt.lower() == "release" and want["DECIMAL128C_NO_LTO"] != "ON"
                   else "NO LTO")
            return f"build: CMAKE_BUILD_TYPE={bt}, C_FLAGS='{cf}' [{lto}]"
        d = os.path.dirname(d)
    return "build: CMakeCache not found"


def run_bench(binary, profile, min_time, out):
    env = dict(os.environ, SWEPT_PROFILE=profile)
    subprocess.run([binary, f"--benchmark_min_time={min_time}",
                    "--benchmark_repetitions=15", "--benchmark_report_aggregates_only=true",
                    "--benchmark_out_format=json", f"--benchmark_out={out}"],
                   env=env, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return json.load(open(out))

def reshape(j, profile, run):
    """Yield store records for one profile's JSON."""
    for b in j["benchmarks"]:
        # --benchmark_repetitions=15 --benchmark_report_aggregates_only ⇒ each
        # benchmark emits mean/median/stddev/cv aggregate rows. Take the MEDIAN (the
        # cross-port estimator); run_name carries the base BM_* name (no _median tag).
        # Median commutes with the monotone 1e9/ips map, so 1e9/median(ips) == median(ns).
        if b.get("run_type") == "aggregate" and b.get("aggregate_name") != "median":
            continue
        name = b.get("run_name") or b["name"]
        ips = b.get("items_per_second")
        if ips:
            ns = round(1e9 / ips, 2)
        else:                                    # fallback: median real_time (per 4096-op iter)
            rt = b.get("real_time")
            if rt is None:
                continue
            factor = {"ns": 1.0, "us": 1e3, "ms": 1e6, "s": 1e9}.get(b.get("time_unit", "ns"), 1.0)
            ns = round(rt * factor / 4096.0, 2)
        m = FMA_RE.match(name)
        if m:                                    # only present under SWEPT_PROFILE=FMA
            raw_impl, cat, suffix = m.groups()
            # d128 reports the _tte rung; peers report their plain fused arm.
            if (raw_impl == "d128") != (suffix == "_tte"):
                continue
            yield dict(lang="c", impl=IMPL[raw_impl], op="fma", cat=cat, profile="FMA",
                       arch=ARCH, mode="thru", ns=ns, run=run)
            continue
        m = BAND_RE.match(name)
        if not m:
            continue
        raw_impl, op, band, suffix = m.groups()
        cat = band.replace("_", "")   # store cat: "SQ_ss" -> "SQss"
        impl = IMPL[raw_impl]
        if impl == "d128":
            # add/sub: flag-free _tte rung; mul/div: plain _ctx arm
            want = "_tte" if op in ("add", "sub") else None
            if (suffix or None) != want:
                continue
        else:
            if suffix:                            # peers: plain benchmark only
                continue
        yield dict(lang="c", impl=impl, op=op, cat=cat, profile=profile,
                   arch=ARCH, mode="thru", ns=ns, run=run)

def build_bench(binary):
    """Rebuild the bench binary from its CMake build tree before measuring —
    the same build-before-bench contract every other emit has implicitly
    (swift build / cargo build / gradle happen inside their emits). Locates the
    build dir by walking up from the binary to CMakeCache.txt; a binary outside
    any build tree (or --no-build) is measured as-is with a loud warning, since
    a stale binary silently measures the WRONG code (the 2026-07-24 stale-LTO
    incident, and any harness-arm change like the ss/os split)."""
    d = os.path.dirname(os.path.abspath(binary))
    for _ in range(4):
        if os.path.exists(os.path.join(d, "CMakeCache.txt")):
            print(f"building bench binary ({d}) ...", flush=True)
            r = subprocess.run(["cmake", "--build", d, "--target", "bench_libbid_vs_d128",
                                "-j", str(os.cpu_count() or 4)],
                               stdout=subprocess.DEVNULL)
            if r.returncode != 0:
                sys.exit("error: cmake build of bench_libbid_vs_d128 failed")
            return
        d = os.path.dirname(d)
    print("WARNING: no CMakeCache.txt near binary — skipping rebuild, measuring as-is", flush=True)


def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    binary = sys.argv[1]
    run = "Rc2"
    min_time = "0.05s"
    a = sys.argv[2:]
    for i, x in enumerate(a):
        if x == "--run-id": run = a[i+1]
        if x == "--min-time": min_time = a[i+1]
    if "--no-build" not in a:
        build_bench(binary)

    recs, ctx = {}, None
    KEY = lambda r: (r["lang"], r["impl"], r["op"], r["cat"], r["profile"], r["mode"], r["arch"])
    for prof in PROFILES:
        out = os.path.join(HERE, f"_cbench_{prof}.json")
        print(f"running C bench SWEPT_PROFILE={prof} ...", flush=True)
        j = run_bench(binary, prof, min_time, out)
        ctx = ctx or j["context"]
        for r in reshape(j, prof, run):
            recs[KEY(r)] = r
    print(f"reshaped {len(recs)} C records")

    # rewrite results.c.jsonl (C arm fully emit-owned)
    KO = ["lang","impl","op","cat","profile","arch","mode","ns","run"]
    opo = {"add":0,"sub":1,"mul":2,"div":3,"fma":4}
    cato = {c:i for i,c in enumerate(["SQss","SQos","NQss","NQos","MQss","MQos","OQss","OQos","FQss","FQos","CP","WP","XP","CD","WD","XD","ET","PT","FN","FF","MIX"])}
    pro = {"P-fin":0,"P-gen":1,"P-max":2,"FMA":3}
    merged = _merge_store(os.path.join(HERE, f"results.c.{ARCH}.jsonl"), recs, KEY)
    rows = sorted(merged.values(), key=lambda r:(r["impl"],opo[r["op"]],pro[r["profile"]],cato[r["cat"]]))
    with open(os.path.join(HERE, f"results.c.{ARCH}.jsonl"), "w") as f:
        for r in rows:
            f.write(json.dumps({k:r[k] for k in KO}, ensure_ascii=False) + "\n")
    print(f"rewrote results.c.{ARCH}.jsonl ({len(rows)} records)")

    # mint / update the run in runs.jsonl
    upsert_run(run, ctx, f"{_os_desc()}; {_tool_version(['cc', '--version'])}; "
                         f"{_c_build_flags(binary)}.",
               _git_head(os.path.dirname(os.path.abspath(binary))))
    by = collections.Counter((r["impl"],r["profile"]) for r in recs.values())
    for k in sorted(by): print(f"   {k}: {by[k]}")

def upsert_run(run, ctx, toolchain, port_commit="unknown"):
    p = os.path.join(HERE, f"runs.{ARCH}.jsonl")
    lines = [l for l in open(p).read().splitlines() if l.strip()]
    runs = [json.loads(l) for l in lines]
    runs = [r for r in runs if r["run"] != run]
    rec = {"run": run, "date": (ctx or {}).get("date","")[:10],
           "machine": f"{(ctx or {}).get('host_name','?')} ({(ctx or {}).get('num_cpus','?')} cpus)",
           "port_commit": port_commit,
           "os_toolchain": toolchain,
           "engine": "Google Benchmark (bench_main.cpp), in-process; d128 add/sub _tte rung, "
                     "mul/div _ctx arm, FMA _tte; 15-rep MEDIAN aggregate "
                     "(--benchmark_repetitions=15 --benchmark_report_aggregates_only), "
                     "ns/op=1e9/items_per_second (basis 4096)",
           "alternatives": "Intel libbid, IBM decQuad, libmpdecimal (all C, full 34-digit); "
                     "FMA peers via native fused multiply-add (__bid128_fma / decQuadFMA / mpd_qfma)",
           "ports": "decimal128-c", "notes": "Phase-2 C reference emit (emit_c.py); SWEPT_PROFILE "
                     "P-gen/P-fin/P-max/FMA. FMA now carries libbid/decQuad/mpd peer arms (one-rounding "
                     "fused). Fresh emit — supersedes transcribed C rows. Add/sub bands sign-split ss/os as of 2026-07-28 (AddSubSignSplitWorkOrder; corpus regen by swift CorpusGen) — prior blended add/sub rows non-comparable."}
    runs.append(rec)
    with open(p, "w") as f:
        for r in runs:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"upserted run '{run}' in runs.jsonl")

if __name__ == "__main__":
    main()
