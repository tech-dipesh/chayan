import numpy as np

from src.retrieval.embed import embed_texts
from src.retrieval.index import load_index
from src.training.adapter import fit, path
from src.training.pairs import make_pairs


def main():
    chunks, d = load_index("table")
    pos = {c["text"]: i for i, c in enumerate(chunks)}
    pairs = [p for p in make_pairs() if p["chunk"] in pos]
    print(len(pairs), "training pairs")
    x = embed_texts([p["question"] for p in pairs], "search_query: ")
    x /= np.linalg.norm(x, axis=1, keepdims=True)
    y = np.array([pos[p["chunk"]] for p in pairs])
    order = np.random.default_rng(1).permutation(len(x))
    np.save(path, fit(x[order], d, y[order]))
    print("saved", path)

if __name__ == "__main__":
    main()
