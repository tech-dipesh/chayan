import json
import time
from chayan.bm25 import bm25_search, build
from chayan.config import root
from chayan.hybrid import hybrid_search
from chayan.index import chunkers, load_index
from chayan.questions import make_questions
from chayan.score import hit_rank, summarize
from chayan.search import search

def retrieve(kind, q, chunks, vectors, idx):
    if kind == "bm25": return bm25_search(q, chunks, idx, 5)
    if kind == "hybrid": return hybrid_search(q, chunks, vectors, idx)
    return search(q, chunks, vectors, 5)

def main():
    qs = make_questions()
    rows = []
    print(f"{'chunker':10} {'retriever':8} hit@1 hit@3 hit@5   mrr  ms")
    for name in chunkers:
        chunks, vectors = load_index(name)
        idx = build(chunks)
        for kind in ("dense", "bm25", "hybrid"):
            ranks, times = [], []
            for q in qs:
                t = time.time()
                hits = retrieve(kind, q["question"], chunks, vectors, idx)
                times.append((time.time() - t) * 1000)
                ranks.append(hit_rank(hits, q["evidence"]))
            hit, mrr = summarize(ranks)
            print(f"{name:10} {kind:8} {hit[1]:5.2f} {hit[3]:5.2f} {hit[5]:5.2f} {mrr:5.2f} {sum(times) / len(times):3.0f}")
            rows.append({"chunker": name, "retriever": kind, "mrr": mrr, "hit": hit, "ranks": ranks})
    (root / "data" / "eval.json").write_text(json.dumps(rows, indent=1))

if __name__ == "__main__":
    main()
