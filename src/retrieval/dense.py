import numpy as np

from src.config import top_k
from src.retrieval.embed import embed_texts


def search(query, chunks, vectors, k=top_k, w=None):
    q = embed_texts([query], "search_query: ")[0]
    q = q if w is None else w @ q
    q /= np.linalg.norm(q)
    scores = vectors @ q
    best = np.argsort(scores)[::-1][:k]
    return [{**chunks[i], "score": float(scores[i])} for i in best]
