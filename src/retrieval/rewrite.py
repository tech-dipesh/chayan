import re

ends = {"1": "31 March", "2": "30 June", "3": "30 September", "4": "31 December"}

def rewrite(question):
    q = re.sub(r"\bq([1-4])(?:\s*(?:of\s*)?(20\d\d))?", lambda m: f"three months ended {ends[m.group(1)]} {m.group(2) or ''}".strip(), question, flags=re.I)
    return re.sub(r"\b(?:fy|full[- ]year)\s*(20\d\d)?", lambda m: f"year ended 31 December {m.group(1) or ''}".strip(), q, flags=re.I)
