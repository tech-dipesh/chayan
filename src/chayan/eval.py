import json
import sys
import time
from chayan.bm25 import bm25_search, build
from chayan.config import root
from chayan.hybrid import hybrid_search
from chayan.index import chunkers, load_index
from chayan.page_questions import make_page_questions
from chayan.pipeline import run
from chayan.questions import make_questions
from chayan.router import pick
from chayan.score import hit_rank, hit_rank_page, summarize
from chayan.search import search

def retrieve(kind, q, chunks, vectors, idx):
    if kind == "bm25": return bm25_search(q, chunks, idx, 5)
    if kind == "hybrid": return hybrid_search(q, chunks, vectors, idx)
    if kind == "routed": return bm25_search(q, chunks, idx, 5) if pick(q) == "bm25" else hybrid_search(q, chunks, vectors, idx)
    if kind == "reranked": return run(q, chunks, vectors, idx)[1]
    return search(q, chunks, vectors, 5)

def mrr_of(ranks): return sum(1 / r for r in ranks if r) / len(ranks) if ranks else 0

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "chunk"
    qs = make_page_questions() if mode == "page" else make_questions()
    rows = []
    print(f"{'chunker':10} {'retriever':8} hit@1 hit@3 hit@5   mrr prose table  ms")
    for name in chunkers:
        chunks, vectors = load_index(name)
        idx = build(chunks)
        for kind in ["dense", "bm25", "hybrid", "routed"] + (["reranked"] if mode == "page" and name == "table" else []):
            ranks, times = [], []
            for q in qs:
                t = time.time()
                hits = retrieve(kind, q["question"], chunks, vectors, idx)
                times.append((time.time() - t) * 1000)
                ranks.append(hit_rank_page(hits, q) if mode == "page" else hit_rank(hits, q["evidence"]))
            hit, mrr = summarize(ranks)
            by = {k: mrr_of([r for r, q in zip(ranks, qs) if q.get("kind") == k]) for k in ("prose", "table")}
            print(f"{name:10} {kind:8} {hit[1]:5.2f} {hit[3]:5.2f} {hit[5]:5.2f} {mrr:5.2f} {by['prose']:5.2f} {by['table']:5.2f} {sum(times) / len(times):3.0f}")
            rows.append({"chunker": name, "retriever": kind, "mrr": mrr, "hit": hit, "by_kind": by, "ranks": ranks})
    (root / "data" / f"eval_{mode}.json").write_text(json.dumps(rows, indent=1))

if __name__ == "__main__":
    main()
