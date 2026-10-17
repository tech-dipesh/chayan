from chayan.config import chunk_size

seps = ["\n\n", "\n", ". ", " "]

def split(text, size=chunk_size, level=0):
    if len(text) <= size or level == len(seps): return [text]
    sep, out, cur = seps[level], [], ""
    for part in text.split(sep):
        if len(part) > size:
            if cur: out.append(cur); cur = ""
            out += split(part, size, level + 1)
        elif cur and len(cur) + len(sep) + len(part) > size:
            out.append(cur); cur = part
        else:
            cur = cur + sep + part if cur else part
    if cur: out.append(cur)
    return out

def make_recursive(pages):
    return [{"page": p["page"], "text": t.strip()} for p in pages for t in split(p["text"]) if len(t.strip()) > 50]
