#!/usr/bin/env python3
"""Phase 3 — csharp emit. Run decimal128-csharp SweptBench 4× under the .NET 11
runtime via `dotnet run -c Release -- swept` (SWEPT_PROFILE), read the BenchmarkDotNet
JSON report, and REWRITE results.csharp.jsonl with ALL THREE arms the net11 swept
emits: d128 (the port), System.Decimal (SysDec_ prefix, 28-digit idiom peer), and
System.Numerics.Decimal128 (SysD128_ prefix, the .NET 11 conformant 34-digit BID peer).
NOTE: BDN numbers are the **Median** of 15 iterations — the cross-port estimator.
Needs the .NET 11 preview SDK (System.Numerics.Decimal128 is net11-only); the port is
compiled net10.0 and JIT'd by net11. Mints run Rcs11.

Usage: emit_csharp.py [--proj <Decimal128.Benchmarks.Net11 dir>] [--run-id Rcs11]
                      [--profiles P-gen,P-fin,P-max,FMA]
       DOTNET11=/path/to/dotnet   net11 SDK (default ~/dotnet/current/dotnet)
"""
# CONTRACT (store-only stage): this emitter writes ONLY the JSONL store
# (results.*.jsonl / runs.*.jsonl). It never writes a report page (*.md) and
# never imports or invokes gen_bench. Splicing reports is a separate stage
# (splice_benchmark_reports.sh / gen_bench.py). See ArchSplitStoreWorkOrder.md.
import json, os, sys, subprocess, glob, collections, re

HERE = os.path.dirname(os.path.abspath(__file__))

import platform


def _host_arch():
    m = platform.machine().lower()
    return {"amd64": "x86_64", "x64": "x86_64", "x86_64": "x86_64",
            "aarch64": "arm64", "arm64": "arm64"}.get(m, m)


ARCH = _host_arch()
MACHINE = (f"Intel Core i9-9880H ({os.cpu_count()} cpus), x86_64"
           if ARCH == "x86_64" else "Apple M3 Pro (12 cores), arm64")


def _dotnet_version(dotnet):
    """The exact SDK build behind this run, e.g. 11.0.100-preview.7.26376.106.

    Worth pinning: between preview.7.26366.102 and preview.7.26376.106 the
    System.Numerics.Decimal128 peer's divide got up to 4x faster while d128 and
    System.Decimal held flat. A run record that says only ".NET 11" cannot tell
    those two pictures apart."""
    try:
        r = subprocess.run([dotnet, "--version"], capture_output=True, text=True, timeout=60)
        v = (r.stdout or "").strip()
        return v if r.returncode == 0 and v else "unknown"
    except Exception:
        return "unknown"


def _os_desc():
    rel = platform.mac_ver()[0]
    return f"macOS {rel} [Darwin {platform.release()}]" if rel else platform.platform()


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
OP = {"Add": "add", "Sub": "sub", "Mul": "mul", "Div": "div", "Fma": "fma"}
METH = re.compile(r"^(SysDec_|SysD128_)?(Add|Sub|Mul|Div|Fma)_([A-Z]+)$")
IMPL_OF = {"SysDec_": "System.Decimal", "SysD128_": "System.Numerics.Decimal128"}

def main():
    proj = os.path.expanduser("~/decimal128/csharp/benchmark/Decimal128.Benchmarks.Net11")
    run = "Rcs11"
    profiles = list(PROFILES)
    a = sys.argv[1:]
    for i, x in enumerate(a):
        if x == "--proj": proj = os.path.expanduser(a[i+1])
        if x == "--run-id": run = a[i+1]
        if x == "--profiles": profiles = [p for p in a[i+1].split(",") if p]

    # System.Numerics.Decimal128 is net11-only, and BDN 0.15.8 cannot target the net11.0
    # moniker out-of-process, so the swept run uses the pinned net11 preview SDK (the same
    # one benchmark/.../run.sh uses). Override with DOTNET11=/path/to/dotnet.
    dotnet = os.environ.get("DOTNET11", os.path.expanduser("~/dotnet/current/dotnet"))
    if not (os.path.isfile(dotnet) and os.access(dotnet, os.X_OK)):
        sys.exit(f"error: .NET 11 SDK not found at {dotnet}\n"
                 "  install:  dotnet-install.sh --channel 11.0 --quality daily "
                 "--install-dir $HOME/dotnet/11.0-preview\n"
                 "  then:     ln -snf 11.0-preview $HOME/dotnet/current\n"
                 "  or point DOTNET11 at a net11 SDK dotnet binary.")
    dotnet_root = os.path.dirname(dotnet)
    sdk_ver = _dotnet_version(dotnet)
    print(f"using .NET SDK {sdk_ver} ({dotnet})", flush=True)

    recs = {}
    KEY = lambda r: (r["lang"], r["impl"], r["op"], r["cat"], r["profile"], r["mode"], r["arch"])
    for prof in profiles:
        for f in glob.glob(os.path.join(proj, "BenchmarkDotNet.Artifacts/results/*-report-full.json")):
            os.remove(f)
        env = dict(os.environ, SWEPT_PROFILE=prof, DOTNET_ROOT=dotnet_root)
        print(f"running csharp swept SWEPT_PROFILE={prof} on .NET 11 (BDN, slow) ...", flush=True)
        r = subprocess.run([dotnet, "run", "-c", "Release", "--", "swept"],
                           cwd=proj, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        if r.returncode != 0:
            tail = (r.stderr or b"").decode("utf-8", "replace").strip().splitlines()[-8:]
            print(f"   dotnet run failed (exit {r.returncode}):\n     " + "\n     ".join(tail))
        reports = glob.glob(os.path.join(proj, "BenchmarkDotNet.Artifacts/results/*-report-full.json"))
        if not reports:
            print("   NO report"); continue
        j = json.load(open(max(reports, key=os.path.getmtime)))
        n = 0
        for b in j["Benchmarks"]:
            st = b.get("Statistics")
            if not st:                          # e.g. an overflow that BDN couldn't measure
                continue
            m = METH.match(b["Method"])
            if not m:
                continue
            prefix, opw, band = m.groups()
            impl = IMPL_OF.get(prefix, "d128")
            op = OP[opw]
            profile = "FMA" if op == "fma" else prof
            recs[KEY(dict(lang="csharp", impl=impl, op=op, cat=band, profile=profile, mode="thru", arch=ARCH))] = \
                dict(lang="csharp", impl=impl, op=op, cat=band, profile=profile,
                     arch=ARCH, mode="thru", ns=round(st["Median"], 2), run=run)
            n += 1
        print(f"   {n} rows")
    print(f"collected {len(recs)} csharp records")

    KO = ["lang","impl","op","cat","profile","arch","mode","ns","run"]
    opo = {"add":0,"sub":1,"mul":2,"div":3,"fma":4}
    cato = {c:i for i,c in enumerate(["SQ","NQ","MQ","OQ","FQ","CP","WP","XP","CD","WD","XD","ET","PT","FN","FF","MIX"])}
    pro = {"P-fin":0,"P-gen":1,"P-max":2,"FMA":3}
    merged = _merge_store(os.path.join(HERE, f"results.csharp.{ARCH}.jsonl"), recs, KEY)
    rows = sorted(merged.values(), key=lambda r:(r["impl"],opo[r["op"]],pro[r["profile"]],cato[r["cat"]]))
    with open(os.path.join(HERE, f"results.csharp.{ARCH}.jsonl"), "w") as f:
        for r in rows:
            f.write(json.dumps({k:r[k] for k in KO}, ensure_ascii=False) + "\n")
    print(f"rewrote results.csharp.{ARCH}.jsonl ({len(rows)} records)")

    p = os.path.join(HERE, f"runs.{ARCH}.jsonl")
    runs = [json.loads(l) for l in open(p).read().splitlines() if l.strip()]
    runs = [r for r in runs if r["run"] != run]
    runs.append({"run": run, "date": "", "machine": MACHINE,
                 "os_toolchain": f"{_os_desc()}; .NET SDK {sdk_ver}.",
                 "engine": "SweptBench.cs (BenchmarkDotNet InProcess Throughput, warmup 4 / iter 15 / launch 1; "
                           "_tte Add/Sub/Mul/Quo), executed on the .NET 11 runtime (System.Numerics.Decimal128 is "
                           "net11-only; port compiled net10.0, JIT'd by net11 — InProcess toolchain as BDN 0.15.8 "
                           "lacks the net11.0 moniker). Each op routes one operand through a non-inlined Opaque() "
                           "barrier (matches swift opaque()/rust black_box) so branch-free fast paths (mul CP, div ET) "
                           "can't free-pipeline. Numbers are the BDN **Median** of the 15 iterations — the cross-port "
                           "estimator, matching the other ports' 15-rep median. SWEPT_PROFILE-filtered by category.",
                 "alternatives": "System.Numerics.Decimal128 (.NET 11 conformant 34-digit BID peer, all bands) + "
                                 "System.Decimal (96-bit/28-digit idiom peer; compact bands only — wide bands "
                                 "overflow its ~7.9e28 ceiling)",
                 "ports": "decimal128-csharp",
                 "notes": f"csharp emit (emit_csharp.py); P-gen/P-fin/P-max/FMA. "
                          f".NET 11 runtime, SDK {sdk_ver}."})
    with open(p, "w") as f:
        for r in runs: f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"upserted run '{run}'")
    by = collections.Counter((r["impl"],r["profile"]) for r in recs.values())
    for k in sorted(by): print(f"   {k}: {by[k]}")

if __name__ == "__main__":
    main()
