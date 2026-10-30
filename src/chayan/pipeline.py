import json

from chayan.bm25 import bm25_search
from chayan.config import root
from chayan.hybrid import hybrid_search
from chayan.rerank import rerank
from chayan.router import pick


def run(question, chunks, vectors, idx, pool=8, k=5):
    route = pick(question)
    hits = bm25_search(question, chunks, idx, pool) if route == "bm25" else hybrid_search(question, chunks, vectors, idx, pool)
    return route, rerank(question, hits, k)

def load_cutoff():
    f = root / "data" / "cutoff.json"
    return json.loads(f.read_text())["min_score"] if f.exists() else 5
