#!/usr/bin/env python3
"""Visibility via Wikipedia pageviews (Wikimedia REST API) — the no-throttle route.

Academic lineage: Wikipedia pageviews as public-attention measure (Moat et al. 2013,
Sci Rep); sits alongside Google SVI (Da-Engelberg-Gao 2011 JF) and news counts
(Fang-Peress 2009 JF; Baker-Bloom-Davis 2016 QJE). Use as primary measure; add
GDELT/Factiva news counts and Google Trends as robustness columns later.

For each exam in data/answer_key.csv x each commodity in data/candidate_pool.csv:
sums daily EN-Wikipedia article views over the 24 months ending at the exam cutoff.
~516 calls; Wikimedia's limits are generous — full run ≈ 10-20 minutes.

Usage:
  python scripts/02b_visibility_wikipedia.py --test     # one article, sanity check
  python scripts/02b_visibility_wikipedia.py            # full run
"""
import argparse, csv, json, os, time, urllib.parse, urllib.request
from datetime import datetime, timedelta
from pathlib import Path

DATA = Path(__file__).parent.parent / "data"
SLEEP = 0.4  # polite; well under Wikimedia guidelines
HEADERS = {"User-Agent": "HistoryEngineResearch/0.1 (academic study of supply-chain "
                         "attention; contact: dorazhang0322@gmail.com)"}

# commodity (as in candidate_pool.csv) -> EN Wikipedia article title
TITLE_MAP = {
    "abrasives (manufactured)": "Abrasive",
    "aluminum": "Aluminium",
    "barite": "Baryte",
    "bauxite and alumina": "Bauxite",
    "cesium": "Caesium",
    "clays": "Clay",
    "diamond (industrial)": "Diamond",
    "diatomite": "Diatomaceous_earth",
    "fluorspar": "Fluorite",
    "garnet (industrial)": "Garnet",
    "gemstones": "Gemstone",
    "graphite (natural)": "Graphite",
    "iron and steel": "Steel",
    "iron and steel scrap": "Scrap",
    "iron and steel slag": "Slag",
    "iron ore": "Iron_ore",
    "iron oxide pigments": "Iron_oxide",
    "lime": "Lime_(material)",
    "magnesium compounds": "Magnesium_oxide",
    "magnesium metal": "Magnesium",
    "mercury": "Mercury_(element)",
    "mica (natural)": "Mica",
    "nitrogen (fixed)-ammonia": "Ammonia",
    "phosphate rock": "Phosphorite",
    "platinum-group metals": "Platinum_group",
    "pumice and pumicite": "Pumice",
    "quartz crystal (industrial)": "Quartz",
    "rare earths": "Rare-earth_element",
    "sand and gravel": "Sand",
    "soda ash": "Sodium_carbonate",
    "stone": "Crushed_stone",
    "talc and pyrophyllite": "Talc",
    "zeolites (natural)": "Zeolite",
}

def title_for(commodity: str) -> str:
    return TITLE_MAP.get(commodity, commodity.strip().capitalize().replace(" ", "_"))

def load_exams():
    exams = []
    with open(DATA / "answer_key.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            end = datetime.fromisoformat(r["cutoff_date"])
            start = end - timedelta(days=730)
            exams.append({"exam_id": r["exam_id"], "cutoff": r["cutoff_date"],
                          "start": start.strftime("%Y%m%d"), "end": end.strftime("%Y%m%d")})
    return exams

def load_pool():
    with open(DATA / "candidate_pool.csv", encoding="utf-8") as f:
        return [r["commodity"] for r in csv.DictReader(f)]

def fetch_views(title: str, start: str, end: str, retries: int = 7):
    """Return summed daily views, or (-1, note) on failure. Loud about errors."""
    url = ("https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"
           f"en.wikipedia/all-access/user/{urllib.parse.quote(title, safe='')}/daily/{start}/{end}")
    last_err = "unknown"
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=60) as r:
                data = json.loads(r.read().decode())
            items = data.get("items", [])
            return sum(int(it.get("views", 0)) for it in items), f"{len(items)} days"
        except urllib.error.HTTPError as e:
            # NOTE: the pageviews API sometimes returns transient 404s for valid
            # articles (storage-layer hiccup) — so 404 is retried too, not trusted.
            last_err = f"HTTP {e.code}"
            print(f"    retry {attempt+1}/{retries} for {title}: {last_err}")
            time.sleep(10 * (attempt + 1))
        except Exception as e:
            last_err = f"{type(e).__name__}: {e}"
            print(f"    retry {attempt+1}/{retries} for {title}: {last_err}")
            time.sleep(10 * (attempt + 1))
    return -1, f"failed after {retries} retries; last: {last_err}"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--test", action="store_true", help="fetch one article and exit")
    ap.add_argument("-o", "--out", default=str(DATA / "wiki_visibility.csv"))
    args = ap.parse_args()

    if args.test:
        views, note = fetch_views("Gallium", "20230601", "20230701")
        print(f"TEST Gallium 2023-06: views={views} ({note})")
        print("If you see a positive number, the API works. Run without --test for the full pool.")
        return

    exams, pool = load_exams(), load_pool()
    fields = ["exam_id", "cutoff", "commodity", "wiki_title", "views_sum", "note", "fetched_at"]

    done = set()
    if os.path.exists(args.out):
        with open(args.out, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if int(r["views_sum"]) >= 0:
                    done.add((r["exam_id"], r["commodity"]))
        print(f"resuming: {len(done)} rows already done")

    mode = "a" if os.path.exists(args.out) else "w"
    with open(args.out, mode, newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        if mode == "w":
            w.writeheader()
        total = len(exams) * len(pool)
        i = 0
        for ex in exams:
            for com in pool:
                i += 1
                if (ex["exam_id"], com) in done:
                    continue
                title = title_for(com)
                views, note = fetch_views(title, ex["start"], ex["end"])
                print(f"[{i}/{total}] exam {ex['exam_id']} · {com} ({title}) = {views}")
                w.writerow({"exam_id": ex["exam_id"], "cutoff": ex["cutoff"],
                            "commodity": com, "wiki_title": title,
                            "views_sum": views, "note": note,
                            "fetched_at": datetime.now().isoformat(timespec="seconds")})
                f.flush()
                time.sleep(SLEEP)
    print(f"-> {args.out}")
    print("Rows with views_sum = -1 need a TITLE_MAP fix; rerun to fill them.")

if __name__ == "__main__":
    main()
