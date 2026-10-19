import re
from chayan.ingest import read_pages

num = r"\(?[\d,]+(?:\.\d+)?%?\)?|–"
years = re.compile(r"\b20\d\d\b")
period = re.compile(r"(?:\d{1,2} [A-Z][a-z]+ )?20\d\d")

def split_row(line):
    words = line.split()
    i = len(words)
    while i > 0 and re.fullmatch(num, words[i - 1]): i -= 1
    return " ".join(words[:i]), words[i:]

def is_row(label, values): return len(values) >= 2 and label != "" and len(label.split()) <= 8 and "annual report" not in label.lower() and not all(years.fullmatch(v) for v in values)

def find_head(lines, i):
    up = []
    for x in reversed(lines[max(0, i - 8):i]):
        if x.endswith((".", ":")): break
        up.insert(0, x)
    head = " ".join(up)
    return head if len(period.findall(head)) >= 2 else ""

def read_tables(pages):
    out = []
    for p in pages:
        lines = [x.strip() for x in p["text"].split("\n") if x.strip()]
        rows, head, gap = [], "", 0
        for i, line in enumerate(lines + [""]):
            label, values = split_row(line)
            if is_row(label, values):
                if not rows: head = find_head(lines, i)
                rows, gap = rows + [(label, values)], 0
                continue
            gap += 1
            if rows and gap > 2:
                if len(rows) >= 2: out.append({"page": p["page"], "head": head, "cols": period.findall(head), "rows": rows})
                rows = []
        if len(rows) >= 2: out.append({"page": p["page"], "head": head, "cols": period.findall(head), "rows": rows})
    return out

if __name__ == "__main__":
    tables = read_tables(read_pages())
    print(len(tables), "tables")
    for t in tables: print("page", t["page"], len(t["rows"]), "rows | head:", t["head"][:50], "|", t["rows"][0])
