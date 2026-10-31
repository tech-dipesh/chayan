import json
import random
import ollama
from src.chunking.table import row_text
from src.config import llm, root
from src.evaluation.multi_questions import make_multi_questions
from src.evaluation.page_questions import make_page_questions
from src.evaluation.score import norm
from src.ingest.pages import read_pages
from src.ingest.tables import read_tables
from src.retrieval.index import load_index

path = root / "data" / "train_pairs.json"
forms = ["What was {} for {}?", "{} in {}", "How much was {} for {}?"]

def banned_answers():
    out = [(q["page"], norm(q["answer"])) for q in make_page_questions()]
    return out + [(a["page"], norm(a["answer"])) for q in make_multi_questions() for a in q["answers"]]

def leaks(chunk, banned): return any(p == chunk["page"] and a in norm(chunk["text"]) for p, a in banned)

def table_pairs(chunks, banned):
    out = []
    for t in read_tables(read_pages()):
        cols = t["cols"]
        for label, values in t["rows"]:
            if not cols or len(values) < len(cols): continue
            line = row_text(label, values, cols)
            i = next((i for i, c in enumerate(chunks) if c.get("kind") == "table" and c["page"] == t["page"] and line in c["text"]), None)
            if i is None or leaks(chunks[i], banned): continue
            out += [{"question": f.format(label, c), "chunk": chunks[i]["text"]} for f, c in zip(random.sample(forms, 2), random.sample(cols, min(2, len(cols))))]
    return out

def prose_pairs(chunks, banned):
    out = []
    for c in chunks:
        if c.get("kind") == "table" or len(c["text"]) < 300 or leaks(c, banned): continue
        for _ in range(2):
            prompt = f"Write one short question that can be answered only from this passage. Do not mention the passage or the text. Reply with the question only.\n\nPassage:\n{c['text']}"
            q = ollama.chat(model=llm, messages=[{"role": "user", "content": prompt}], options={"temperature": 0.8})["message"]["content"].strip()
            if 10 < len(q) < 200: out.append({"question": q, "chunk": c["text"]})
        print(len(out), "prose pairs", end="\r")
    return out

def make_pairs():
    if path.exists(): return json.loads(path.read_text())
    random.seed(3)
    chunks, _ = load_index("table")
    banned = banned_answers()
    out = table_pairs(chunks, banned)
    print(len(out), "table pairs")
    out += prose_pairs(chunks, banned)
    path.write_text(json.dumps(out, indent=1))
    return out
