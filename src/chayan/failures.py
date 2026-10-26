import json
import re
from collections import Counter
from chayan.bm25 import bm25_search, build
from chayan.config import root
from chayan.hybrid import hybrid_search
from chayan.index import chunkers, load_index
from chayan.page_questions import make_page_questions
from chayan.score import hit_rank_page, norm
from chayan.search import search

labels = ("split evidence", "table flattened", "embedding miss", "ranking miss")

def ranked(kind, q, chunks, vectors, idx):
    n = len(chunks)
    if kind == "bm25": return bm25_search(q, chunks, idx, n)
    if kind == "hybrid": return hybrid_search(q, chunks, vectors, idx, n, n)
    return search(q, chunks, vectors, n)

def label_miss(q, rank, chunks):
    a = norm(q["answer"])
    gold = [norm(c["text"]) for c in chunks if c["page"] == q["page"] and a in norm(c["text"])]
    if not gold: return "split evidence"
    if q.get("kind") == "table":
        label, period = re.match(r"What was (.+) for (.+)\?$", q["question"]).groups()
        if not any(norm(label) in t and norm(period) in t for t in gold): return "table flattened"
    return "ranking miss" if rank and rank <= 20 else "embedding miss"

def main():
    qs = make_page_questions()
    rows = []
    print(f"{'chunker':10} {'retriever':8} miss " + " ".join(f"{l:>15}" for l in labels))
    for name in chunkers:
        chunks, vectors = load_index(name)
        idx = build(chunks)
        for kind in ("dense", "bm25", "hybrid"):
            count = Counter()
            for q in qs:
                rank = hit_rank_page(ranked(kind, q["question"], chunks, vectors, idx), q)
                if rank is not None and rank <= 5: continue
                why = label_miss(q, rank, chunks)
                count[why] += 1
                rows.append({"chunker": name, "retriever": kind, "question": q["question"], "page": q["page"], "label": why})
            print(f"{name:10} {kind:8} {sum(count.values()):4} " + " ".join(f"{count[l]:15d}" for l in labels))
    (root / "data" / "failures.json").write_text(json.dumps(rows, indent=1))

if __name__ == "__main__":
    main()
