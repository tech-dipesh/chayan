import math
import re
from collections import Counter

import numpy as np


def tokens(text): return re.findall(r"\w+", text.lower())

def build(chunks):
    docs = [Counter(tokens(c["text"])) for c in chunks]
    lens = [sum(d.values()) for d in docs]
    df = Counter(w for d in docs for w in d)
    return {"docs": docs, "lens": lens, "df": df, "avg": sum(lens) / len(lens)}

def bm25_search(query, chunks, idx, k=5, k1=1.5, b=0.75):
    n, words = len(chunks), tokens(query)
    scores = []
    for d, size in zip(idx["docs"], idx["lens"]):
        s = 0
        for w in words:
            if w not in d: continue
            idf = math.log(1 + (n - idx["df"][w] + 0.5) / (idx["df"][w] + 0.5))
            s += idf * d[w] * (k1 + 1) / (d[w] + k1 * (1 - b + b * size / idx["avg"]))
        scores.append(s)
    best = np.argsort(scores)[::-1][:k]
    return [{**chunks[i], "score": float(scores[i])} for i in best]
