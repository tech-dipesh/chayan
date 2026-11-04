import json
from src.retrieval.bm25 import bm25_search
from src.retrieval.split import split_question
from src.config import root
from src.answer.judge import score_chunk

def run(question, chunks, idx, k=5):
    lists = [bm25_search(p, chunks, idx, k) for p in split_question(question)]
    mixed = [h for row in zip(*lists) for h in row]
    return list({h["text"]: h for h in mixed}.values())[:k]

def gate_score(question, hits, n=3):
    parts = split_question(question)
    return min(max(score_chunk(p, h["text"]) for h in hits[:n * len(parts)]) for p in parts)

def load_cutoff():
    f = root / "data" / "cutoff.json"
    return json.loads(f.read_text())["min_score"] if f.exists() else 5
