#!/usr/bin/env python3
"""Register corpus files: SHA-256 hash + metadata manifest.

Usage: python 01_hash_manifest.py corpus/exam/ [-o manifest.csv]
Every file entering the exam box MUST pass through here. The manifest is the
evidence chain: url and pub_date must be filled in by hand afterwards if the
sidecar .meta.json is absent.

Sidecar convention: for corpus/exam/foo.pdf, an optional corpus/exam/foo.pdf.meta.json
  {"url": "...", "pub_date": "YYYY-MM-DD", "title": "...", "commodity": "gallium", "lang": "zh"}
"""
import argparse, csv, hashlib, json, sys
from datetime import date
from pathlib import Path

CUTOFF = date(2023, 7, 2)

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("corpus_dir")
    ap.add_argument("-o", "--out", default="manifest.csv")
    args = ap.parse_args()

    rows, violations = [], []
    for p in sorted(Path(args.corpus_dir).rglob("*")):
        if not p.is_file() or p.suffix == ".json":
            continue
        meta = {}
        side = p.with_name(p.name + ".meta.json")
        if side.exists():
            meta = json.loads(side.read_text(encoding="utf-8"))
        pub = meta.get("pub_date", "")
        if pub:
            try:
                if date.fromisoformat(pub) > CUTOFF:
                    violations.append((str(p), pub))
            except ValueError:
                pass
        rows.append({
            "file": str(p), "sha256": sha256(p),
            "url": meta.get("url", ""), "pub_date": pub,
            "download_date": date.today().isoformat(),
            "title": meta.get("title", ""), "commodity": meta.get("commodity", ""),
            "lang": meta.get("lang", ""),
        })

    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["file"])
        w.writeheader(); w.writerows(rows)
    print(f"registered {len(rows)} files -> {args.out}")

    if violations:
        print("\n!!! CUTOFF VIOLATIONS (post-2023-07-02 files in exam box) !!!", file=sys.stderr)
        for f_, d_ in violations:
            print(f"  {f_}  pub_date={d_}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
