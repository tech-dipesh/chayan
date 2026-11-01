import json
import sys
import time
from src.retrieval.bm25 import bm25_search, build
from src.config import root
from src.retrieval.hybrid import hybrid_search
from src.retrieval.index import chunkers, load_index
from src.evaluation.multi_questions import make_multi_questions
from src.evaluation.page_questions import make_page_questions
from src.evaluation.questions import make_questions
from src.retrieval.rewrite import rewrite
from src.retrieval.router import pick
from src.evaluation.score import covered, hit_rank, hit_rank_page, summarize
from src.retrieval.dense import search
from src.training.adapter import load_adapter

adapter = load_adapter()
kinds = (("dense+a", "hybrid+a") if adapter is not None else ())

def retrieve(kind, q, chunks, vectors, idx):
    if kind == "bm25": return bm25_search(q, chunks, idx, 5)
    if kind == "hybrid": return hybrid_search(q, chunks, vectors, idx)
    if kind == "routed": return bm25_search(q, chunks, idx, 5) if pick(q) == "bm25" else hybrid_search(q, chunks, vectors, idx)
    if kind == "rewrite": return bm25_search(rewrite(q), chunks, idx, 5)
    if kind == "dense+a": return search(q, chunks, vectors, 5, adapter)
    if kind == "hybrid+a": return hybrid_search(q, chunks, vectors, idx, w=adapter)
    return search(q, chunks, vectors, 5)

def mrr_of(ranks): return sum(1 / r for r in ranks if r) / len(ranks) if ranks else 0

def multi():
    qs = make_multi_questions()
    print(f"{'chunker':10} {'retriever':8} both@5 any@5")
    for name in chunkers:
        chunks, vectors = load_index(name)
        idx = build(chunks)
        for kind in ("dense", "bm25", "hybrid") + kinds:
            got = [covered(retrieve(kind, q["question"], chunks, vectors, idx), q) for q in qs]
            print(f"{name:10} {kind:8} {sum(g == 2 for g in got) / len(got):7.2f} {sum(g >= 1 for g in got) / len(got):6.2f}")

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "chunk"
    if mode == "multi": return multi()
    qs = make_page_questions() if mode == "page" else make_questions()
    rows = []
    print(f"{'chunker':10} {'retriever':8} hit@1 hit@3 hit@5   mrr prose table  ms")
    for name in chunkers:
        chunks, vectors = load_index(name)
        idx = build(chunks)
        for kind in ("dense", "bm25", "hybrid", "routed", "rewrite") + kinds:
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
