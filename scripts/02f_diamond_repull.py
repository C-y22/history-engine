#!/usr/bin/env python3
"""Diamond term-correction re-pull (rule (d), term_map_lock v1.1).

The frozen query "industrial diamond" missed the trade press's actual vocabulary
(synthetic / lab-grown diamond), so diamond's visibility is understated. This
script re-pulls ALL 7 diamond cells with the corrected term:

  ("industrial diamond" OR "synthetic diamond") AND (mining OR supply OR
   production OR export OR smelter OR refinery)

Windows:
  - six 24-month pre-cutoff windows (one per exam), ending on each cutoff date
  - one post-announcement window: 2025-10-09 + 30 days (restores diamond to the
    H2b attention sample, n=21 -> 22)

Decision bounds (computed 2026-08-15, exam A):
  corrected 24m count < 11  -> diamond keeps rank #1
  corrected 24m count < 65  -> diamond keeps top-10
  corrected 24m count >= 65 -> diamond drops out of exam A's top ten

Usage:
  export MC_API_TOKEN=...        # same setup as 02c/02d
  python scripts/02f_diamond_repull.py          # ~7 queries, <1 min
  python scripts/02f_diamond_repull.py --test   # one sanity query only

Output: data/mc_diamond_repull.csv  (send this file back for the final rerun)
"""
import argparse, csv, os, sys, time
from datetime import date, datetime, timedelta
from pathlib import Path

try:
    import mediacloud.api
except ImportError:
    sys.exit("run first:  pip install mediacloud")

DATA = Path(__file__).parent.parent / "data"
SLEEP = float(os.environ.get("MC_SLEEP", "1.5"))
COLLECTIONS = [34412234]  # United States - National (same as 02c/02d)
CONTEXT = '(mining OR supply OR production OR export OR smelter OR refinery)'
TERM = '("industrial diamond" OR "synthetic diamond")'
QUERY = f"{TERM} AND {CONTEXT}"
WINDOW_DAYS = 730  # matches mc_visibility 24-month windows

CUTOFFS = {  # exam_id -> cutoff date (window = cutoff-730d .. cutoff)
    "A":  date(2023, 7, 2),
    "B":  date(2023, 10, 19),
    "C":  date(2024, 8, 14),
    "D":  date(2025, 1, 31),
    "E1": date(2025, 4, 1),
    "E2": date(2025, 10, 8),
}
POST = ("E2_post30", date(2025, 10, 9), date(2025, 10, 9) + timedelta(days=30))

def count_stories(search, start, end, retries=6):
    last = "unknown"
    for attempt in range(retries):
        try:
            res = search.story_count(QUERY, start, end, collection_ids=COLLECTIONS)
            if isinstance(res, dict):
                if "relevant" in res:
                    return int(res["relevant"]), int(res.get("total", -1)), "ok"
                if "count" in res and isinstance(res["count"], dict):
                    c = res["count"]
                    return int(c.get("relevant", -1)), int(c.get("total", -1)), "ok"
            return -1, -1, f"unexpected shape: {str(res)[:120]}"
        except Exception as e:
            last = f"{type(e).__name__}: {str(e)[:120]}"
            print(f"    retry {attempt+1}/{retries}: {last}")
            time.sleep(5 * (attempt + 1))
    return -1, -1, f"failed; last: {last}"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--test", action="store_true")
    ap.add_argument("-o", "--out", default=str(DATA / "mc_diamond_repull.csv"))
    args = ap.parse_args()

    token = os.environ.get("MC_API_TOKEN")
    if not token:
        sys.exit("MC_API_TOKEN not set (same setup as 02c/02d).")
    search = mediacloud.api.SearchApi(token)

    if args.test:
        end = CUTOFFS["A"]
        rel, tot, note = count_stories(search, end - timedelta(days=WINDOW_DAYS), end)
        print(f"TEST exam-A window: relevant={rel} total={tot} ({note})")
        print("Old term gave 4. Bounds: <11 keeps #1, <65 keeps top-10.")
        return

    tasks = [(ex, cut - timedelta(days=WINDOW_DAYS), cut) for ex, cut in CUTOFFS.items()]
    tasks.append(POST)

    fields = ["window", "start", "end", "relevant_count", "total_count",
              "query", "note", "fetched_at"]
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for i, (label, start, end) in enumerate(tasks, 1):
            rel, tot, note = count_stories(search, start, end)
            w.writerow({"window": label, "start": start.isoformat(),
                        "end": end.isoformat(), "relevant_count": rel,
                        "total_count": tot, "query": QUERY, "note": note,
                        "fetched_at": datetime.now().isoformat(timespec="seconds")})
            f.flush()
            print(f"[{i}/7] {label:9} {start} .. {end} -> {rel}")
            time.sleep(SLEEP)
    print(f"\ndone -> {args.out}   (send this file back)")

if __name__ == "__main__":
    main()
