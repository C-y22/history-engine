#!/usr/bin/env python3
"""Latent score = criticality (imported) x (1 - visibility (measured)), then rank.

criticality: data/candidate_pool.csv supply_risk_score (USGS OFR 2021-1045).
  - NA scores: commodity kept but flagged (paper reports with/without).
visibility: data/visibility.csv context_count, normalized to [0,1] by log-minmax
  across the pool (log because counts span 4 orders of magnitude).

Usage: python 05_score_rank.py [-v data/visibility.csv] [-c data/candidate_pool.csv] [-o ranking.csv]
"""
import argparse, csv, math

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--criticality", default="data/candidate_pool.csv")
    ap.add_argument("-v", "--visibility", default="data/visibility.csv")
    ap.add_argument("-o", "--out", default="ranking.csv")
    args = ap.parse_args()

    crit = {}
    with open(args.criticality, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            s = r["supply_risk_score"]
            crit[r["commodity"].lower()] = {
                "score": float(s) if s not in ("NA", "") else None,
                "byproduct": r["byproduct_flag"] == "1",
                "critical_list": r["on_us_critical_list_2022"] == "1"}

    vis = {}
    with open(args.visibility, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            c = int(r.get("context_count", r.get("total_raw_or_avg_norm", 0)))
            if c >= 0:
                vis[r["term"].lower()] = c

    logs = [math.log10(v + 1) for v in vis.values()]
    lo, hi = min(logs), max(logs)

    rows = []
    for term, count in vis.items():
        v_norm = (math.log10(count + 1) - lo) / (hi - lo) if hi > lo else 0.0
        c = crit.get(term, {})
        c_score = c.get("score")
        latent = round(c_score * (1 - v_norm), 4) if c_score is not None else None
        rows.append({"commodity": term, "criticality": c_score,
                     "visibility_count": count, "visibility_norm": round(v_norm, 4),
                     "latent_score": latent,
                     "byproduct": c.get("byproduct", ""),
                     "note": "" if c_score is not None else "criticality NA (qualitative-only or unevaluated)"})

    rows.sort(key=lambda r: (r["latent_score"] is None, -(r["latent_score"] or 0)))
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    print(f"-> {args.out}")
    for r in rows[:10]:
        print(f"  {r['commodity']:<15} latent={r['latent_score']}")

if __name__ == "__main__":
    main()
