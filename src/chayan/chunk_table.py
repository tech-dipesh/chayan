import re

from chayan.config import chunk_size
from chayan.pdf_tables import read_tables
from chayan.recursive import make_recursive


def is_header(row): return not any(re.search(r"\d,\d{3}", c) for c in row)

def row_text(head, row):
    pairs = [f"{h} {v}" if h else v for h, v in zip(head, row[1:]) if v]
    return f"{row[0]}: " + ", ".join(pairs)

def table_chunks(t):
    head, rows = ([], t["rows"]) if not is_header(t["rows"][0]) else (t["rows"][0][1:], t["rows"][1:])
    top = " | ".join(h for h in head if h)
    out, cur = [], top
    for r in rows:
        line = row_text(head or [""] * len(r), r)
        if len(cur) + len(line) > chunk_size and cur != top: out.append(cur); cur = top
        cur = cur + "\n" + line if cur else line
    if cur != top: out.append(cur)
    return [{"page": t["page"], "text": c, "kind": "table"} for c in out]

def make_table_chunks(pages):
    tables = [c for t in read_tables() for c in table_chunks(t)]
    return make_recursive(pages) + tables
