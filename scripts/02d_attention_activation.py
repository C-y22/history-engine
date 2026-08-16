#!/usr/bin/env python3
"""H2b attention-activation — post-announcement news JUMP (Media Cloud).

Theory: latent power is activated by a visibility flip. For every CONTROLLED
commodity, measure the attention jump: context-news count in the 30 days AFTER
the announcement, divided by the pre-cutoff monthly baseline (from the exam's
24-month window already collected in mc_visibility.csv).

Prediction: pre-cutoff invisibility -> larger jump ratio (thulium: a few
stories/month -> hundreds; graphite: barely doubles).

Placebo arm: 20 never-controlled commodities (seeded random draw), measured on
the same announcement dates -> their "jump" should be ~1 (no event for them).

Usage:
  python scripts/02d_attention_activation.py --test    # one query sanity check
  python scripts/02d_attention_activation.py           # full run (~62 queries, ~3 min)

Requires: MC_API_TOKEN in env (same as 02c); data/mc_visibility.csv present.
"""
import argparse, csv, os, random, sys, time
from datetime import datetime, timedelta, date
from pathlib import Path

try:
    import mediacloud.api
except ImportError:
    sys.exit("run first:  pip install mediacloud")

DATA = Path(__file__).parent.parent / "data"
SLEEP = float(os.environ.get("MC_SLEEP", "1.5"))
COLLECTIONS = [34412234]  # United States - National (same as 02c; lock w/ methods)
CONTEXT = '(mining OR supply OR production OR export OR smelter OR refinery)'
POST_DAYS = 30
BASELINE_MONTHS = 24.0  # mc_visibility windows are 730 days
PLACEBO_N = 20
PLACEBO_SEED = 20260813
# placebos are evaluated on the first and the biggest REE announcement dates
PLACEBO_EVENTS = ["A", "E1"]

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

def term_for(c): return OVERRIDES.get(c, c)

def load_answer_key():
    exams = {}
    with open(DATA / "answer_key.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            exams[r["exam_id"]] = {
                "announce": datetime.fromisoformat(r["announce_date"]).date(),
                "positives": [p.strip() for p in r["positives"].split(";") if p.strip()],
            }
    return exams

def load_pool():
    with open(DATA / "candidate_pool.csv", encoding="utf-8") as f:
        return [r["commodity"] for r in csv.DictReader(f)]

def load_baselines():
    """(exam_id, commodity) -> 24m relevant count, from the existing 600-cell file."""
    base = {}
    with open(DATA / "mc_visibility.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            base[(r["exam_id"], r["commodity"])] = int(r["relevant_count"])
    return base

def count_stories(search, query, start, end, retries=6):
    last = "unknown"
    for attempt in range(retries):
        try:
            res = search.story_count(query, start, end, collection_ids=COLLECTIONS)
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
    ap.add_argument("-o", "--out", default=str(DATA / "mc_attention_activation.csv"))
    args = ap.parse_args()

    token = os.environ.get("MC_API_TOKEN")
    if not token:
        sys.exit("MC_API_TOKEN not set (same setup as 02c).")
    search = mediacloud.api.SearchApi(token)

    if args.test:
        rel, tot, note = count_stories(search, f"gallium AND {CONTEXT}",
                                       date(2023, 7, 3), date(2023, 8, 2))
        print(f"TEST gallium post-announcement 30d: relevant={rel} total={tot} ({note})")
        print("Expect a number well above ~16 (=394/24, its monthly baseline).")
        return

    exams = load_answer_key()
    pool = load_pool()
    baselines = load_baselines()

    # target arm: every controlled commodity at its own announcement
    tasks = []
    all_pos = set()
    for ex_id, ex in exams.items():
        for c in ex["positives"]:
            if c not in pool:
                print(f"  ! positive not in pool, skipped: {c}")
                continue
            all_pos.add(c)
            tasks.append(("target", c, ex_id, ex["announce"]))
    # placebo arm: seeded draw of never-controlled commodities
    candidates = sorted(c for c in pool if c not in all_pos and c != "rare earths")
    rng = random.Random(PLACEBO_SEED)
    placebos = rng.sample(candidates, PLACEBO_N)
    for c in placebos:
        for ex_id in PLACEBO_EVENTS:
            tasks.append(("placebo", c, ex_id, exams[ex_id]["announce"]))

    fields = ["group", "commodity", "exam_id", "announce_date", "post30_relevant",
              "post30_total", "baseline24m_relevant", "baseline_monthly_mean",
              "jump_ratio", "query", "note", "fetched_at"]
    done = set()
    if os.path.exists(args.out):
        with open(args.out, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if int(r["post30_relevant"]) >= 0:
                    done.add((r["group"], r["commodity"], r["exam_id"]))
        print(f"resuming: {len(done)} rows already done")

    mode = "a" if os.path.exists(args.out) else "w"
    with open(args.out, mode, newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        if mode == "w":
            w.writeheader()
        for i, (grp, com, ex_id, announce) in enumerate(tasks, 1):
            if (grp, com, ex_id) in done:
                continue
            q = f"{term_for(com)} AND {CONTEXT}"
            start, end = announce, announce + timedelta(days=POST_DAYS)
            rel, tot, note = count_stories(search, q, start, end)
            base = baselines.get((ex_id, com))
            monthly = round(base / BASELINE_MONTHS, 3) if base is not None else ""
            jump = round(rel / (base / BASELINE_MONTHS), 3) if (base and rel >= 0) else ""
            w.writerow({"group": grp, "commodity": com, "exam_id": ex_id,
                        "announce_date": announce.isoformat(), "post30_relevant": rel,
                        "post30_total": tot, "baseline24m_relevant": base,
                        "baseline_monthly_mean": monthly, "jump_ratio": jump,
                        "query": q, "note": note,
                        "fetched_at": datetime.now().isoformat(timespec="seconds")})
            f.flush()
            print(f"[{i}/{len(tasks)}] {grp:7} {com:26} {ex_id:3} -> {rel} (jump x{jump})")
            time.sleep(SLEEP)
    print(f"\ndone -> {args.out}")

if __name__ == "__main__":
    main()
