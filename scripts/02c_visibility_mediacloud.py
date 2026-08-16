#!/usr/bin/env python3
"""Visibility via Media Cloud — news story counts (the PRIMARY measure).

Academic lineage: news-count attention measures (Fang & Peress 2009 JF;
Baker-Bloom-Davis 2016 QJE construct their EPU index from newspaper term counts).
Media Cloud is the academic open platform for exactly this (MIT/Berkeley/UMass).

For each exam x commodity: counts stories matching a supply-context query in the
24 months ending at the exam cutoff, within a defined source collection.
Also records the collection's TOTAL story count per window, so the paper can use
the normalized share (relevant/total) — controls for corpus growth over time.

Setup (once):
  pip install mediacloud
  # token already in ~/.zshrc as MC_API_TOKEN

Usage:
  python scripts/02c_visibility_mediacloud.py --test    # one query, sanity check
  python scripts/02c_visibility_mediacloud.py           # full run (~516 queries)
"""
import argparse, csv, os, sys, time
from datetime import datetime, timedelta
from pathlib import Path

try:
    import mediacloud.api
except ImportError:
    sys.exit("run first:  pip install mediacloud")

DATA = Path(__file__).parent.parent / "data"
SLEEP = 1.5
# Methods decision (lock with coauthor): which source universe?
# 34412234 = Media Cloud's long-standing "United States - National" collection.
COLLECTIONS = [34412234]
CONTEXT = '(mining OR supply OR production OR export OR smelter OR refinery)'

OVERRIDES = {
    "rare earths": '"rare earth"',
    "magnesium metal": "magnesium",
    "magnesium compounds": '"magnesium compounds"',
    "graphite (natural)": "graphite",
    "platinum-group metals": '(platinum OR palladium)',
    "bauxite and alumina": "bauxite",
    "iron ore": '"iron ore"',
    "iron and steel": '"steel industry"',
    "iron and steel scrap": '"steel scrap"',
    "iron and steel slag": '"steel slag"',
    "iron oxide pigments": '"iron oxide"',
    "diamond (industrial)": '"industrial diamond"',
    "garnet (industrial)": "garnet",
    "quartz crystal (industrial)": '"quartz crystal"',
    "abrasives (manufactured)": "abrasives",
    "mica (natural)": "mica",
    "zeolites (natural)": "zeolites",
    "sand and gravel": '"sand and gravel"',
    "talc and pyrophyllite": "talc",
    "pumice and pumicite": "pumice",
    "nitrogen (fixed)-ammonia": "ammonia",
    "soda ash": '"soda ash"',
    "phosphate rock": '"phosphate rock"',
}

def term_for(commodity: str) -> str:
    return OVERRIDES.get(commodity, commodity)

def load_exams():
    exams = []
    with open(DATA / "answer_key.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            end = datetime.fromisoformat(r["cutoff_date"]).date()
            start = end - timedelta(days=730)
            exams.append({"exam_id": r["exam_id"], "cutoff": r["cutoff_date"],
                          "start": start, "end": end})
    return exams

def load_pool():
    with open(DATA / "candidate_pool.csv", encoding="utf-8") as f:
        return [r["commodity"] for r in csv.DictReader(f)]

def count_stories(search, query, start, end, retries=6):
    last = "unknown"
    for attempt in range(retries):
        try:
            res = search.story_count(query, start, end, collection_ids=COLLECTIONS)
            # client versions differ in return shape; handle both
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
    ap.add_argument("-o", "--out", default=str(DATA / "mc_visibility.csv"))
    args = ap.parse_args()

    token = os.environ.get("MC_API_TOKEN")
    if not token:
        sys.exit("MC_API_TOKEN not set. Add it to ~/.zshrc (see earlier instructions) "
                 "or run:  MC_API_TOKEN=yourtoken python scripts/02c_...")
    search = mediacloud.api.SearchApi(token)

    if args.test:
        from datetime import date
        rel, tot, note = count_stories(search, f"gallium AND {CONTEXT}",
                                       date(2021, 7, 2), date(2023, 7, 2))
        print(f"TEST gallium supply-context 2021-07~2023-07: relevant={rel} total={tot} ({note})")
        print("Positive number => API works. Run without --test for the full pool.")
        return

    exams, pool = load_exams(), load_pool()
    fields = ["exam_id", "cutoff", "commodity", "query", "relevant_count",
              "total_count", "note", "fetched_at"]
    done = set()
    if os.path.exists(args.out):
        with open(args.out, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if int(r["relevant_count"]) >= 0:
                    done.add((r["exam_id"], r["commodity"]))
        print(f"resuming: {len(done)} rows already done")

    mode = "a" if os.path.exists(args.out) else "w"
    with open(args.out, mode, newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        if mode == "w":
            w.writeheader()
        total_n = len(exams) * len(pool)
        i = 0
        for ex in exams:
            for com in pool:
                i += 1
                if (ex["exam_id"], com) in done:
                    continue
                q = f"{term_for(com)} AND {CONTEXT}"
                rel, tot, note = count_stories(search, q, ex["start"], ex["end"])
                print(f"[{i}/{total_n}] exam {ex['exam_id']} · {com} = {rel}")
                w.writerow({"exam_id": ex["exam_id"], "cutoff": ex["cutoff"],
                            "commodity": com, "query": q, "relevant_count": rel,
                            "total_count": tot, "note": note,
                            "fetched_at": datetime.now().isoformat(timespec="seconds")})
                f.flush()
                time.sleep(SLEEP)
    print(f"-> {args.out}")

if __name__ == "__main__":
    main()
