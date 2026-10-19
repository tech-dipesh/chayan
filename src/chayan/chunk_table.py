from chayan.config import chunk_size
from chayan.pdf_tables import read_tables
from chayan.recursive import make_recursive


def row_text(label, values, cols):
    pairs = [f"{c} {v}" for c, v in zip(cols, values)] + values[len(cols):] if cols and len(values) >= len(cols) else values
    return f"{label}: " + ", ".join(pairs)

def table_chunks(t):
    cols = t["cols"]
    out, cur = [], t["head"]
    for label, values in t["rows"]:
        line = row_text(label, values, cols)
        if len(cur) + len(line) > chunk_size and "\n" in cur: out.append(cur); cur = t["head"]
        cur = cur + "\n" + line if cur else line
    out.append(cur)
    return [{"page": t["page"], "text": c, "kind": "table"} for c in out]

def make_table_chunks(pages):
    tables = [c for t in read_tables(pages) for c in table_chunks(t)]
    return make_recursive(pages) + tables
