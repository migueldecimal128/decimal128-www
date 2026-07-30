#!/usr/bin/env python3
"""csharp-bid emit — the BID-representation migration arm (decimal128-csharp-migration).
Runs the migration repo's SweptBench under the .NET 11 runtime, one BDN process per
cell, and REWRITES results.csharp-bid.<arch>.jsonl with the d128 cells ONLY: the
SysDec_/SysD128_ peer cells are identical code to the csharp arm and are already
measured there (results.csharp.<arch>.jsonl) — re-measuring them here would double the
wall-clock for duplicate numbers. lang key = "csharp-bid", impl stays "d128" (the store
key's lang field disambiguates from the csharp arm; impls.json needs no new entry).
NOTE: BDN numbers are the **Median** of 15 iterations — the cross-port estimator.
Needs the .NET 11 preview SDK. Mints run Rcsbid1 and stamps the migration repo's HEAD
commit into the run record (port_commit) — the baseline is meaningful only against a
known engine commit.

Baseline freeze: after a run that is declared a baseline, copy the results file to
baselines/csharp-bid.baseline.<arch>.jsonl (see baselines/README.md). This emitter
NEVER writes into baselines/.

Usage: emit_csharp_bid.py [--proj <Decimal128.Benchmarks.Net11 dir>] [--run-id Rcsbid1]
                          [--profiles P-gen,P-fin,P-max,FMA] [--cells <regex>] [--note <text>]
       DOTNET11=/path/to/dotnet   net11 SDK (default ~/dotnet/current/dotnet)
"""
# CONTRACT (store-only stage): this emitter writes ONLY the JSONL store
# (results.*.jsonl / runs.*.jsonl). It never writes a report page (*.md) and
# never imports or invokes gen_bench. Splicing reports is a separate stage
# (splice_benchmark_reports.sh / gen_bench.py). See ArchSplitStoreWorkOrder.md.
import json, os, sys, subprocess, glob, collections, re

HERE = os.path.dirname(os.path.abspath(__file__))

import platform

LANG = "csharp-bid"


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


def _git_head(repo):
    """Short HEAD of the benchmarked engine repo, '+dirty' if the tree differs."""
    try:
        h = subprocess.run(["git", "-C", repo, "rev-parse", "--short", "HEAD"],
                           capture_output=True, text=True, timeout=60)
        if h.returncode != 0:
            return "unknown"
        s = subprocess.run(["git", "-C", repo, "status", "--porcelain"],
                           capture_output=True, text=True, timeout=60)
        dirty = "+dirty" if (s.stdout or "").strip() else ""
        return h.stdout.strip() + dirty
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
# d128 cells only — no SysDec_/SysD128_ prefix arm here (see module docstring).
METH = re.compile(r"^(Add|Sub|Mul|Div|Fma)_([A-Z]+(?:_(?:ss|os))?)$")

def main():
    proj = os.path.expanduser("~/decimal128/csharp-migration/benchmark/Decimal128.Benchmarks.Net11")
    run = "Rcsbid1"
    profiles = list(PROFILES)
    cells_re = None
    note = ""
    a = sys.argv[1:]
    for i, x in enumerate(a):
        if x == "--proj": proj = os.path.expanduser(a[i+1])
        if x == "--run-id": run = a[i+1]
        if x == "--profiles": profiles = [p for p in a[i+1].split(",") if p]
        if x == "--cells": cells_re = re.compile(a[i+1])
        if x == "--note": note = a[i+1]

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
    port_repo = os.path.dirname(os.path.dirname(proj.rstrip("/")))
    port_commit = _git_head(port_repo)
    print(f"using .NET SDK {sdk_ver} ({dotnet}); engine {port_repo} @ {port_commit}", flush=True)

    recs = {}
    KEY = lambda r: (r["lang"], r["impl"], r["op"], r["cat"], r["profile"], r["mode"], r["arch"])
    # PER-CELL PROCESS ISOLATION: .NET tier-1 code is compiled once per process,
    # shaped by dynamic PGO from whatever stream runs first. Cells sharing a
    # process inherit that training (measured: a pure like-sign cell first
    # pessimizes later unlike-sign cells by ~15 ns/op, growing with band depth;
    # HotSpot deopts + retrains, so only .NET needs this). One BDN launch per
    # benchmark method makes every cell "cost in a process trained on this
    # workload" — the same semantics the untier'd native ports measure.
    for prof in profiles:
        env = dict(os.environ, SWEPT_PROFILE=prof, DOTNET_ROOT=dotnet_root)
        ls = subprocess.run([dotnet, "run", "-c", "Release", "--", "swept-list"],
                            cwd=proj, env=env, capture_output=True, text=True)
        cells = [c for c in (ls.stdout or "").split() if c]
        if ls.returncode != 0 or not cells:
            print(f"   swept-list failed for {prof}: {(ls.stderr or '').strip().splitlines()[-1:]}")
            continue
        # This arm measures the port only: drop the peer cells up front so no
        # process is ever launched for them.
        cells = [c for c in cells if METH.match(c)]
        # --cells narrows the sweep to the arms a change can actually move (e.g.
        # '^Add_' = the d128 add cells). Safe because the store upserts by key, so
        # unlisted cells keep their prior rows, and because each cell is
        # process-isolated either way: a subset run measures exactly what the same
        # cell measures in a full run.
        if cells_re is not None:
            cells = [c for c in cells if cells_re.search(c)]
            if not cells:
                print(f"   no cells match /{cells_re.pattern}/ in {prof}, skipping")
                continue
        print(f"running csharp-bid swept SWEPT_PROFILE={prof} — {len(cells)} cells, one process each ...", flush=True)
        n = 0
        for cell in cells:
            for f in glob.glob(os.path.join(proj, "BenchmarkDotNet.Artifacts/results/*-report-full.json")):
                os.remove(f)
            cenv = dict(env, SWEPT_FILTER=f"*.{cell}")
            r = subprocess.run([dotnet, "run", "-c", "Release", "--", "swept"],
                               cwd=proj, env=cenv, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            if r.returncode != 0:
                tail = (r.stderr or b"").decode("utf-8", "replace").strip().splitlines()[-4:]
                print(f"   {cell}: dotnet run failed (exit {r.returncode}): " + " | ".join(tail))
                continue
            reports = glob.glob(os.path.join(proj, "BenchmarkDotNet.Artifacts/results/*-report-full.json"))
            if not reports:
                print(f"   {cell}: NO report")
                continue
            j2 = json.load(open(max(reports, key=os.path.getmtime)))
            for b in j2["Benchmarks"]:
                st = b.get("Statistics")
                if not st:                          # e.g. an overflow that BDN couldn't measure
                    continue
                m = METH.match(b["Method"])
                if not m:
                    continue
                opw, band = m.groups()
                band = band.replace("_", "")   # store cat: "SQ_ss" -> "SQss"
                op = OP[opw]
                profile = "FMA" if op == "fma" else prof
                recs[KEY(dict(lang=LANG, impl="d128", op=op, cat=band, profile=profile, mode="thru", arch=ARCH))] = \
                    dict(lang=LANG, impl="d128", op=op, cat=band, profile=profile,
                         arch=ARCH, mode="thru", ns=round(st["Median"], 2), run=run)
                n += 1
        print(f"   {n} rows")
    print(f"collected {len(recs)} csharp-bid records")

    KO = ["lang","impl","op","cat","profile","arch","mode","ns","run"]
    opo = {"add":0,"sub":1,"mul":2,"div":3,"fma":4}
    cato = {c:i for i,c in enumerate(["SQss","SQos","NQss","NQos","MQss","MQos","OQss","OQos","FQss","FQos","CP","WP","XP","CD","WD","XD","ET","PT","FN","FF","MIX"])}
    pro = {"P-fin":0,"P-gen":1,"P-max":2,"FMA":3}
    merged = _merge_store(os.path.join(HERE, f"results.{LANG}.{ARCH}.jsonl"), recs, KEY)
    rows = sorted(merged.values(), key=lambda r:(r["impl"],opo[r["op"]],pro[r["profile"]],cato[r["cat"]]))
    with open(os.path.join(HERE, f"results.{LANG}.{ARCH}.jsonl"), "w") as f:
        for r in rows:
            f.write(json.dumps({k:r[k] for k in KO}, ensure_ascii=False) + "\n")
    print(f"rewrote results.{LANG}.{ARCH}.jsonl ({len(rows)} records)")

    p = os.path.join(HERE, f"runs.{ARCH}.jsonl")
    runs = [json.loads(l) for l in open(p).read().splitlines() if l.strip()]
    runs = [r for r in runs if r["run"] != run]
    runs.append({"run": run, "date": "", "machine": MACHINE,
                 "os_toolchain": f"{_os_desc()}; .NET SDK {sdk_ver}.",
                 "port_commit": port_commit,
                 "engine": "SweptBench.cs (BenchmarkDotNet InProcess Throughput, warmup 4 / iter 15; ONE PROCESS PER CELL — tier-1/dynamic-PGO code is per-process and training-order-dependent, so each cell runs in a fresh process trained on its own workload; "
                           "_tte Add/Sub/Mul/Quo), executed on the .NET 11 runtime (port compiled net10.0, "
                           "JIT'd by net11 — InProcess toolchain as BDN 0.15.8 lacks the net11.0 moniker). "
                           "Each op routes one operand through a non-inlined Opaque() barrier (matches swift "
                           "opaque()/rust black_box) so branch-free fast paths (mul CP, div ET) can't "
                           "free-pipeline. Numbers are the BDN **Median** of the 15 iterations — the cross-port "
                           "estimator, matching the other ports' 15-rep median. SWEPT_PROFILE-filtered by category.",
                 "alternatives": "none in this arm — d128 cells only. The System.Numerics.Decimal128 and "
                                 "System.Decimal peers are identical code measured under lang=csharp "
                                 "(results.csharp.<arch>.jsonl); compare against those rows.",
                 "ports": "decimal128-csharp-migration (csharp-bid arm: raw BID128 in-memory, arithmetic on "
                          "undecoded operands, non-canonical inputs handled in every operation)",
                 "notes": f"csharp-bid emit (emit_csharp_bid.py); {'/'.join(profiles)}"
                          + (f"; cells matching /{cells_re.pattern}/ only (partial re-emit — other cells keep their prior run's rows)" if cells_re else "")
                          + f". .NET 11 runtime, SDK {sdk_ver}. Engine commit {port_commit}."
                          + (f" {note}" if note else "")})
    with open(p, "w") as f:
        for r in runs: f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"upserted run '{run}'")
    by = collections.Counter((r["impl"],r["profile"]) for r in recs.values())
    for k in sorted(by): print(f"   {k}: {by[k]}")

if __name__ == "__main__":
    main()
