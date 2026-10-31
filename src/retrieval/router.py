import re

words = ("profit", "revenue", "ebitda", "margin", "expense", "cash", "dividend", "mau", "dau", "how many", "how much", "percentage", "per share", "total")
quarters = {"1": "31 March", "2": "30 June", "3": "30 September", "4": "31 December"}

def pick(question):
    q = question.lower()
    return "bm25" if re.search(r"\d", q) or any(w in q for w in words) else "hybrid"

def expand(question): return re.sub(r"\bQ([1-4])\b", lambda m: f"three months ended {quarters[m.group(1)]}", question, flags=re.I)
