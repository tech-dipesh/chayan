import json
from src.retrieval.bm25 import bm25_search
from src.config import root
from src.answer.judge import score_chunk

def run(question, chunks, idx, k=5): return bm25_search(question, chunks, idx, k)

def gate_score(question, hits, n=3): return max(score_chunk(question, h["text"]) for h in hits[:n])

def load_cutoff():
    f = root / "data" / "cutoff.json"
    return json.loads(f.read_text())["min_score"] if f.exists() else 5
