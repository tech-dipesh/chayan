from chayan.config import chunk_size, overlap
from chayan.ingest import read_pages


def split(text, size=chunk_size, step=overlap):
    parts = [text[i:i + size].strip() for i in range(0, len(text), size - step)]
    return [p for p in parts if len(p) > 50]

def make_chunks(pages):
    return [{"page": p["page"], "text": t} for p in pages for t in split(p["text"])]

if __name__ == "__main__":
    chunks = make_chunks(read_pages())
    print(len(chunks), "chunks")
    print(chunks[0]["page"], chunks[0]["text"][:300])
