import json
import random
import ollama
from chayan.config import llm, root
from chayan.index import load_index

path = root / "data" / "questions.json"

def make_questions(n=30):
    if path.exists(): return json.loads(path.read_text())
    chunks, _ = load_index()
    long = [c for c in chunks if len(c["text"]) >= 500]
    random.seed(7)
    out = []
    for c in random.sample(long, n):
        prompt = f"Write one short question that can be answered only from this passage. Do not mention the passage or the text. Reply with the question only.\n\nPassage:\n{c['text']}"
        q = ollama.chat(model=llm, messages=[{"role": "user", "content": prompt}])["message"]["content"].strip()
        out.append({"question": q, "page": c["page"], "evidence": c["text"][200:300]})
        print(len(out), q)
    path.write_text(json.dumps(out, indent=1))
    return out
