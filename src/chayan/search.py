import numpy as np

from chayan.config import top_k
from chayan.embed import embed_texts


def search(query, chunks, vectors, k=top_k):
    q = embed_texts([query], "search_query: ")[0]
    q /= np.linalg.norm(q)
    scores = vectors @ q
    best = np.argsort(scores)[::-1][:k]
    return [{**chunks[i], "score": float(scores[i])} for i in best]
