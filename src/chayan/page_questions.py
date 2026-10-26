import json
import random
import re
from collections import Counter
import ollama
from chayan.config import llm, root
from chayan.ingest import read_pages
from chayan.pdf_tables import read_tables
from chayan.score import norm

path = root / "data" / "page_questions.json"

def table_questions(pages, n):
    tables = read_tables(pages)
    count = Counter(label for t in tables for label, _ in t["rows"])
    out = []
    for t in tables:
        cols = t["cols"]
        for label, values in t["rows"]:
            ok = count[label] == 1 and cols and len(values) >= len(cols) and label[0].isupper() and len(label.split()) <= 6 and "(" not in label
            if not ok: continue
            i = random.randrange(len(cols))
            if len(norm(values[i])) >= 3: out.append({"question": f"What was {label} for {cols[i]}?", "answer": values[i], "label": label, "page": t["page"], "kind": "table"})
    random.shuffle(out)
    return out[:n]

def prose_questions(pages, n):
    out, seen, done = [], set(), {}
    pool = [p for p in pages if len(p["text"]) > 1500] * 4
    random.shuffle(pool)
    for p in pool:
        if len(out) >= n: break
        skip = "; ".join(done.get(p["page"], []))
        prompt = f"Read this page. Write one question about a single fact stated in a normal sentence, not in a table. Do not ask about: {skip or 'nothing yet'}. Then give the answer copied word for word from the page, at most 6 words. Reply exactly as:\nQuestion: ...\nAnswer: ...\n\nPage:\n{p['text'][:3500]}"
        reply = ollama.chat(model=llm, messages=[{"role": "user", "content": prompt}], options={"temperature": 0.8})["message"]["content"]
        m = re.search(r"Question:\s*(.+?)\s*Answer:\s*(.+)", reply, re.S)
        if not m: continue
        q, a = m.group(1).strip(), m.group(2).strip().strip('."')
        key = (p["page"], norm(a))
        if len(norm(a)) >= 3 and norm(a) in norm(p["text"]) and norm(a) not in norm(q) and key not in seen:
            seen.add(key)
            done.setdefault(p["page"], []).append(a)
            out.append({"question": q, "answer": a, "page": p["page"], "kind": "prose"})
            print(len(out), q, "->", a)
    return out

def make_page_questions(n=40):
    if path.exists(): return json.loads(path.read_text())
    random.seed(11)
    pages = read_pages()
    tables = table_questions(pages, n // 2)
    out = prose_questions(pages, n - len(tables)) + tables
    path.write_text(json.dumps(out, indent=1))
    return out
