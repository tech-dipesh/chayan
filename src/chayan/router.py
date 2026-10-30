import re

words = ("profit", "revenue", "ebitda", "margin", "expense", "cash", "dividend", "mau", "dau", "how many", "how much", "percentage", "per share", "total")

def pick(question):
    q = question.lower()
    return "bm25" if re.search(r"\d", q) or any(w in q for w in words) else "hybrid"
