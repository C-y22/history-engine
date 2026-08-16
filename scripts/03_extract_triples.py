#!/usr/bin/env python3
"""LLM structured extraction: (facility, process, material) triples from corpus docs.

Reads text files from the exam box, sends each to the Anthropic API with the
extraction prompt (prompts/extraction_prompt.md), writes JSONL triples.

Methodological hygiene:
- Every triple carries source_file + quote so it is auditable.
- Sample >=10% of outputs for human validation; report inter-coder reliability.
- The model must NOT use outside knowledge — prompt forbids it; spot-check for leaks
  (e.g., a triple mentioning the July 2023 export controls = contamination, discard doc run).

Usage: ANTHROPIC_API_KEY=... python 03_extract_triples.py corpus/exam/ -o triples.jsonl
"""
import argparse, json, sys
from pathlib import Path

try:
    import anthropic
except ImportError:
    sys.exit("pip install anthropic")

PROMPT = (Path(__file__).parent.parent / "prompts" / "extraction_prompt.md").read_text(encoding="utf-8")
MODEL = "claude-sonnet-4-5"  # pin the model version in the paper's appendix

def extract(client, text: str, source: str) -> list:
    msg = client.messages.create(
        model=MODEL, max_tokens=4096,
        messages=[{"role": "user",
                   "content": PROMPT + "\n\n<document source='" + source + "'>\n"
                              + text[:150_000] + "\n</document>"}])
    out = msg.content[0].text
    # model is instructed to return a JSON array; be forgiving about fences
    out = out.strip().removeprefix("```json").removeprefix("```").removesuffix("```")
    try:
        triples = json.loads(out)
    except json.JSONDecodeError:
        return [{"error": "parse_failure", "source_file": source}]
    for t in triples:
        t["source_file"] = source
    return triples

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("corpus_dir")
    ap.add_argument("-o", "--out", default="triples.jsonl")
    args = ap.parse_args()
    client = anthropic.Anthropic()
    n = 0
    with open(args.out, "w", encoding="utf-8") as fo:
        for p in sorted(Path(args.corpus_dir).rglob("*.txt")):
            print(f"[{p.name}]")
            for t in extract(client, p.read_text(encoding="utf-8", errors="ignore"), str(p)):
                fo.write(json.dumps(t, ensure_ascii=False) + "\n"); n += 1
    print(f"{n} triples -> {args.out}")
    print("NOTE: PDF corpus files must be converted to .txt first (pdftotext / marker).")

if __name__ == "__main__":
    main()
