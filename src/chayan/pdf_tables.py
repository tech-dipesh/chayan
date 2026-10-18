import pdfplumber

from chayan.config import first_page, last_page, pdf_path

settings = {"vertical_strategy": "text", "horizontal_strategy": "lines", "snap_tolerance": 4}

def read_tables():
    out = []
    with pdfplumber.open(pdf_path) as pdf:
        for n in range(first_page, last_page + 1):
            for t in pdf.pages[n - 1].extract_tables(settings):
                rows = [[(c or "").replace("\n", " ").strip() for c in r] for r in t]
                rows = [r for r in rows if any(r)]
                if len(rows) > 1: out.append({"page": n, "rows": rows})
    return out

if __name__ == "__main__":
    tables = read_tables()
    print(len(tables), "tables")
    for t in tables: print("page", t["page"], len(t["rows"]), "rows", t["rows"][:2])
