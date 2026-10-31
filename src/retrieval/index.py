import hashlib
import json

import numpy as np

from src.chunking.fixed import make_chunks
from src.chunking.recursive import make_recursive
from src.chunking.table import make_table_chunks
from src.config import embed as model
from src.config import root
from src.ingest.pages import read_pages
from src.retrieval.embed import embed_texts

cache = root / ".cache"
chunkers = {"fixed": make_chunks, "recursive": make_recursive, "table": make_table_chunks}

def load_index(name="fixed"):
    chunks = chunkers[name](read_pages())
    key = hashlib.sha1((json.dumps(chunks) + model).encode()).hexdigest()[:10]
    vecs = cache / f"{key}.npy"
    if vecs.exists(): return chunks, np.load(vecs)
    print(f"embedding {len(chunks)} {name} chunks, first run only")
    vectors = embed_texts([c["text"] for c in chunks])
    vectors /= np.linalg.norm(vectors, axis=1, keepdims=True)
    cache.mkdir(exist_ok=True)
    np.save(vecs, vectors)
    return chunks, vectors
