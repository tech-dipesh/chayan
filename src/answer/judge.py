import re
import ollama
from src.config import llm

def score_chunk(question, text):
    prompt = f"Question: {question}\n\nPassage:\n{text}\n\nHow well does the passage answer the question? Reply with one number from 0 (not at all) to 10 (fully). Number only."
    reply = ollama.chat(model=llm, messages=[{"role": "user", "content": prompt}], options={"temperature": 0, "num_predict": 4})["message"]["content"]
    m = re.search(r"\d+", reply)
    return min(int(m.group()), 10) if m else 0
