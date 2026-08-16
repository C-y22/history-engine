#!/usr/bin/env python3
"""Evaluate ranking against the answer box: precision/recall@k + specificity.

answer_key.csv format:
  commodity,revealed,reveal_date,mechanism
  gallium,1,2023-07-03,export_control
  germanium,1,2023-07-03,export_control
  rubidium,0,,           # negative control: never revealed
  fluorspar,0,,

Usage: python 06_evaluate.py ranking.csv data/answer_key.csv [-k 5]
"""
import argparse, csv

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ranking"); ap.add_argument("answer_key")
    ap.add_argument("-k", type=int, default=5)
    args = ap.parse_args()

    with open(args.ranking, encoding="utf-8") as f:
        ranked = [r for r in csv.DictReader(f) if r["latent_score"] not in ("", "None")]
    with open(args.answer_key, encoding="utf-8") as f:
        key = {r["commodity"].lower(): r["revealed"] == "1" for r in csv.DictReader(f)}

    topk = [r["commodity"].lower() for r in ranked[:args.k]]
    positives = {c for c, rev in key.items() if rev}
    negatives = {c for c, rev in key.items() if not rev}

    tp = sum(1 for c in topk if c in positives)
    fp_neg = sum(1 for c in topk if c in negatives)
    prec = tp / len(topk) if topk else 0
    rec = tp / len(positives) if positives else 0

    print(f"top-{args.k}: {topk}")
    print(f"precision@{args.k} = {prec:.2f}   recall@{args.k} = {rec:.2f}")
    print(f"negative controls wrongly flagged in top-{args.k}: {fp_neg}  (specificity check)")
    for c in positives:
        pos = next((i + 1 for i, r in enumerate(ranked) if r["commodity"].lower() == c), None)
        print(f"  rank of revealed positive '{c}': {pos}")

if __name__ == "__main__":
    main()
