import numpy as np
import ollama

from chayan.config import embed as model


def embed_texts(texts, prefix="search_document: "):
    out = []
    for i in range(0, len(texts), 32):
        out += ollama.embed(model=model, input=[prefix + t for t in texts[i:i + 32]])["embeddings"]
    return np.array(out, dtype="float32")
