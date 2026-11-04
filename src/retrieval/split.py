import re

lead = r"\s+and\s+(?=(?:what|how|who|when|which|where)\b)"
tail = r"\s((?:for|in|during|at|as of)\s[^?]+)\??$"

def split_question(question):
    parts = re.split(lead, question.strip().rstrip("?"), flags=re.I)
    if len(parts) < 2: return [question]
    shared = re.search(tail, parts[-1], flags=re.I)
    return [p if not shared or re.search(tail, p, flags=re.I) else f"{p} {shared.group(1)}" for p in parts]
