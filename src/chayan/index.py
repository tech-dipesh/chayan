import hashlib
import json

import numpy as np

from chayan.chunk import make_chunks
from chayan.chunk_table import make_table_chunks
from chayan.config import chunk_size, first_page, last_page, overlap, pdf_path, root
from chayan.embed import embed_texts
from chayan.ingest import read_pages
from chayan.recursive import make_recursive

cache = root / ".cache"
chunkers = {"fixed": make_chunks, "recursive": make_recursive, "table": make_table_chunks}

def load_index(name="fixed"):
    raw = pdf_path.read_bytes() + f"{first_page}{last_page}{chunk_size}{overlap}".encode()
    if name != "fixed": raw += name.encode()
    key = hashlib.sha1(raw).hexdigest()[:10]
    meta, vecs = cache / f"{key}.json", cache / f"{key}.npy"
    if meta.exists() and vecs.exists(): return json.loads(meta.read_text()), np.load(vecs)
    chunks = chunkers[name](read_pages())
    print(f"embedding {len(chunks)} {name} chunks, first run only")
    vectors = embed_texts([c["text"] for c in chunks])
    vectors /= np.linalg.norm(vectors, axis=1, keepdims=True)
    cache.mkdir(exist_ok=True)
    meta.write_text(json.dumps(chunks))
    np.save(vecs, vectors)
    return chunks, vectors
