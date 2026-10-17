from chayan.bm25 import bm25_search
from chayan.search import search


def rrf(lists, k=5, c=60):
    score, keep = {}, {}
    for hits in lists:
        for rank, h in enumerate(hits):
            score[h["text"]] = score.get(h["text"], 0) + 1 / (c + rank + 1)
            keep[h["text"]] = h
    best = sorted(score, key=score.get, reverse=True)[:k]
    return [{**keep[t], "score": score[t]} for t in best]

def hybrid_search(query, chunks, vectors, idx, k=5, pool=20):
    return rrf([search(query, chunks, vectors, pool), bm25_search(query, chunks, idx, pool)], k)
