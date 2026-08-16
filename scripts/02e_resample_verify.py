#!/usr/bin/env python3
"""MediaCloud re-sampling verification — count stability check.

Purpose (methods appendix): Media Cloud's index can change over time (sources
added/removed, re-crawls). This script re-queries a seeded random sample of the
600 visibility cells and compares today's counts with the archived collection
run, so the paper can state measured drift instead of assuming zero.

Usage:
  python scripts/02e_resample_verify.py          # 40-cell sample, ~2 min
  python scripts/02e_resample_verify.py -n 60    # bigger sample

Requires: MC_API_TOKEN in env; data/mc_visibility.csv (the archived run).
Output: data/mc_resample_verify.csv + a drift summary printed at the end.
"""
import argparse, csv, os, random, sys, time
from datetime import datetime, timedelta
from pathlib import Path

try:
    import mediacloud.api
except ImportError:
    sys.exit("run first:  pip install mediacloud")

DATA = Path(__file__).parent.parent / "data"
SLEEP = float(os.environ.get("MC_SLEEP", "1.5"))
COLLECTIONS = [34412234]
SEED = 20260814  # fixed seed -> the sample itself is reproducible

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", type=int, default=40)
    ap.add_argument("-o", "--out", default=str(DATA / "mc_resample_verify.csv"))
    args = ap.parse_args()

    token = os.environ.get("MC_API_TOKEN")
    if not token:
        sys.exit("MC_API_TOKEN not set.")
    search = mediacloud.api.SearchApi(token)

    rows = list(csv.DictReader(open(DATA / "mc_visibility.csv", encoding="utf-8")))
    rng = random.Random(SEED)
    sample = rng.sample(rows, args.n)

    out_fields = ["exam_id", "commodity", "query", "window_start", "window_end",
                  "archived_count", "recount", "abs_diff", "pct_diff",
                  "archived_fetched_at", "refetched_at", "note"]
    results = []
    for i, r in enumerate(sample, 1):
        end = datetime.fromisoformat(r["cutoff"]).date()
        start = end - timedelta(days=730)
        note, rec = "ok", -1
        for attempt in range(6):
            try:
                res = search.story_count(r["query"], start, end, collection_ids=COLLECTIONS)
                if isinstance(res, dict) and "relevant" in res:
                    rec = int(res["relevant"]); break
                if isinstance(res, dict) and isinstance(res.get("count"), dict):
                    rec = int(res["count"].get("relevant", -1)); break
                note = f"unexpected shape: {str(res)[:80]}"; break
            except Exception as e:
                note = f"{type(e).__name__}: {str(e)[:80]}"
                time.sleep(5 * (attempt + 1))
        old = int(r["relevant_count"])
        diff = rec - old if rec >= 0 else None
        pct = round(100 * diff / old, 1) if (diff is not None and old > 0) else ""
        results.append({"exam_id": r["exam_id"], "commodity": r["commodity"],
                        "query": r["query"], "window_start": start.isoformat(),
                        "window_end": end.isoformat(), "archived_count": old,
                        "recount": rec, "abs_diff": diff if diff is not None else "",
                        "pct_diff": pct, "archived_fetched_at": r["fetched_at"],
                        "refetched_at": datetime.now().isoformat(timespec="seconds"),
                        "note": note})
        print(f"[{i}/{args.n}] {r['exam_id']:3} {r['commodity'][:24]:24} {old:6} -> {rec:6} ({pct}%)")
        time.sleep(SLEEP)

    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=out_fields); w.writeheader(); w.writerows(results)

    ok = [r for r in results if r["recount"] >= 0]
    diffs = [abs(r["abs_diff"]) for r in ok if r["abs_diff"] != ""]
    pcts = [abs(float(r["pct_diff"])) for r in ok if r["pct_diff"] != ""]
    exact = sum(1 for r in ok if r["abs_diff"] == 0)
    print("\n===== drift summary (paste into methods appendix) =====")
    print(f"sampled cells: {len(results)}   successfully re-queried: {len(ok)}")
    print(f"identical counts: {exact}/{len(ok)}")
    if pcts:
        pcts.sort()
        print(f"median |drift|: {pcts[len(pcts)//2]:.1f}%   max |drift|: {max(pcts):.1f}%")
    print(f"-> {args.out}")

if __name__ == "__main__":
    main()
