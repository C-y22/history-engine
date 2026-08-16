#!/usr/bin/env python3
"""Assemble the physical supply graph: observed triples + stoichiometric inference.

Nodes: facilities, companies, processes, materials.
Observed edges from triples.jsonl; derived edges from rules/stoichiometry.yaml:
  facility --runs--> host_process  +  rule(host_process => byproduct)
  ==> facility --POTENTIAL_SOURCE_OF--> byproduct   (deduced, not observed)

Usage: python 04_build_graph.py triples.jsonl -o graph.gpickle [--summary]
"""
import argparse, json, pickle
from pathlib import Path
import networkx as nx
import yaml

RULES = yaml.safe_load((Path(__file__).parent.parent / "rules" / "stoichiometry.yaml")
                       .read_text(encoding="utf-8"))["rules"]

def norm(s):
    return s.strip() if isinstance(s, str) and s.strip() and s.strip().lower() != "null" else None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("triples")
    ap.add_argument("-o", "--out", default="graph.gpickle")
    ap.add_argument("--summary", action="store_true")
    args = ap.parse_args()

    G = nx.MultiDiGraph()
    with open(args.triples, encoding="utf-8") as f:
        for line in f:
            t = json.loads(line)
            if "error" in t:
                continue
            fac, proc = norm(t.get("facility")), norm(t.get("process"))
            m_out, comp = norm(t.get("material_out")), norm(t.get("company"))
            if fac and proc:
                G.add_edge(fac, proc, rel="runs", src=t.get("source_file"), quote=t.get("quote"))
            if fac and m_out:
                G.add_edge(fac, m_out, rel=t.get("relation", "produces"),
                           capacity=t.get("capacity"), year=t.get("year"),
                           src=t.get("source_file"))
            if comp and fac:
                G.add_edge(comp, fac, rel="owns")

    # stoichiometric inference: the decisive step
    derived = 0
    for rule in RULES:
        host = rule["host_process"]
        bps = rule["byproduct"] if isinstance(rule["byproduct"], list) else [rule["byproduct"]]
        for fac, proc, data in list(G.edges(data=True)):
            if data.get("rel") == "runs" and host in proc:
                for bp in bps:
                    G.add_edge(fac, bp, rel="POTENTIAL_SOURCE_OF",
                               mechanism=rule["mechanism"], rule_source=rule["source"],
                               derived=True)
                    derived += 1

    with open(args.out, "wb") as f:
        pickle.dump(G, f)
    print(f"nodes={G.number_of_nodes()} edges={G.number_of_edges()} derived={derived} -> {args.out}")

    if args.summary:
        for u, v, d in G.edges(data=True):
            if d.get("derived"):
                print(f"  DEDUCED: {u} --POTENTIAL_SOURCE_OF--> {v}")

if __name__ == "__main__":
    main()
