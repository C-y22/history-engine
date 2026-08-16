#!/usr/bin/env python3
"""Visibility measurement via GDELT DOC 2.0 — v0.2 (seven-exam edition).

For EACH exam in data/answer_key.csv, measures news volume for EVERY commodity
in data/candidate_pool.csv over the 24 months ending at that exam's cutoff date.
Runs bare + supply-context queries; scoring uses the context column.

~86 commodities x 2 queries x 6 exams ≈ 1000 calls. With rate limiting expect
2-6 hours on a clean home IP — run overnight. CHECKPOINTED: safe to Ctrl-C and
rerun; finished (exam, term) rows are skipped.

Usage: python 02_visibility_gdelt.py [-o data/visibility_full.csv]
"""
import argparse, csv, json, os, time, urllib.parse, urllib.request
from datetime import datetime, timedelta
from pathlib import Path

SLEEP = float(os.environ.get("GDELT_SLEEP", "8"))
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/537.36 "
                         "(KHTML, like Gecko) Chrome/126.0 Safari/537.36 academic-research"}
CONTEXT = '("mining" OR "supply" OR "production" OR "export" OR "smelter" OR "refinery")'
DATA = Path(__file__).parent.parent / "data"

# --- term overrides: commodity name -> GDELT query term (defaults to bare name) ---
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
    # NOTE: review this map with a coauthor before the formal run; log any change.
}

def term_for(commodity: str) -> str:
    return OVERRIDES.get(commodity, commodity)

def load_exams():
    exams = []
    with open(DATA / "answer_key.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            end = datetime.fromisoformat(r["cutoff_date"])
            start = end - timedelta(days=730)
            exams.append({"exam_id": r["exam_id"],
                          "start": start.strftime("%Y%m%d") + "000000",
                          "end": end.strftime("%Y%m%d") + "235959",
                          "cutoff": r["cutoff_date"]})
    return exams

def load_pool():
    with open(DATA / "candidate_pool.csv", encoding="utf-8") as f:
        return [r["commodity"] for r in csv.DictReader(f)]

def fetch_sum(query: str, start: str, end: str, retries: int = 8) -> int:
    url = ("https://api.gdeltproject.org/api/v2/doc/doc?"
           + urllib.parse.urlencode({"query": query, "mode": "timelinevolraw",
                                     "startdatetime": start, "enddatetime": end,
                                     "format": "json"}))
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=60) as r:
                data = json.loads(r.read().decode())
            series = data.get("timeline", [{}])
            series = series[0].get("data", []) if series else []
            return sum(int(pt.get("value", 0)) for pt in series)
        except Exception as e:
            wait = SLEEP * (2 ** attempt)
            print(f"    retry {attempt+1}/{retries} in {wait:.0f}s ({e})")
            time.sleep(wait)
    return -1  # failed sentinel; rerun later (checkpoint keeps -1 rows OUT so they retry)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--out", default=str(DATA / "visibility_full.csv"))
    ap.add_argument("--exams", default="",
                    help="comma-separated exam ids to run, e.g. A,B,C (default: all). "
                         "Use to split the run across two networks/IPs.")
    ap.add_argument("--with-bare", action="store_true",
                    help="also fetch bare-term counts (diagnostic only; scoring uses context). "
                         "Default OFF to halve query count.")
    args = ap.parse_args()

    exams, pool = load_exams(), load_pool()
    if args.exams:
        wanted = {x.strip() for x in args.exams.split(",")}
        exams = [e for e in exams if e["exam_id"] in wanted]
        print(f"running exams: {[e['exam_id'] for e in exams]}")
    fields = ["exam_id", "cutoff", "commodity", "query_context", "raw_count",
              "context_count", "fetched_at"]

    done = set()
    if os.path.exists(args.out):  # resume: skip rows already fetched successfully
        with open(args.out, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                ok_ctx = int(r["context_count"]) >= 0
                ok_raw = (int(r["raw_count"]) >= 0) or not args.with_bare
                if ok_ctx and ok_raw:
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
                base = term_for(com)
                ctx_q = f"{base} {CONTEXT}"
                print(f"[{i}/{total}] exam {ex['exam_id']} · {com}")
                if args.with_bare:
                    raw = fetch_sum(base, ex["start"], ex["end"]); time.sleep(SLEEP)
                else:
                    raw = -2  # not fetched (bare skipped by design)
                ctx = fetch_sum(ctx_q, ex["start"], ex["end"]); time.sleep(SLEEP)
                w.writerow({"exam_id": ex["exam_id"], "cutoff": ex["cutoff"],
                            "commodity": com, "query_context": ctx_q,
                            "raw_count": raw, "context_count": ctx,
                            "fetched_at": datetime.now().isoformat(timespec="seconds")})
                f.flush()
    print(f"-> {args.out}")
    print("next: per exam, run 05_score_rank.py filtering visibility_full.csv to that exam_id,")
    print("      then 06_evaluate.py against answer_key positives.")

if __name__ == "__main__":
    main()
