import itertools
import json
import random
from collections import Counter
from src.config import root
from src.ingest.pages import read_pages
from src.ingest.tables import read_tables
from src.evaluation.score import norm

path = root / "data" / "multi_questions.json"

def make_multi_questions(n=15):
    if path.exists(): return json.loads(path.read_text())
    random.seed(5)
    tables = read_tables(read_pages())
    count = Counter(label for t in tables for label, _ in t["rows"])
    by = {}
    for t in tables:
        for label, values in t["rows"]:
            if count[label] != 1 or not label[0].isupper() or len(label.split()) > 6 or "(" in label or len(values) < len(t["cols"]): continue
            for period, value in zip(t["cols"], values):
                if len(norm(value)) >= 3: by.setdefault(period, []).append({"page": t["page"], "label": label, "value": value})
    pairs = [(a, b) for group in by.values() for a, b in itertools.combinations(group, 2) if a["page"] != b["page"] and a["label"] != b["label"]]
    random.shuffle(pairs)
    period = lambda a: next(p for p, g in by.items() if a in g)
    out = [{"question": f"What was {a['label']} and what was {b['label']} for {period(a)}?", "answers": [{"answer": a["value"], "page": a["page"]}, {"answer": b["value"], "page": b["page"]}], "kind": "multi"} for a, b in pairs[:n]]
    path.write_text(json.dumps(out, indent=1))
    return out
