import ollama

from chayan.config import llm


def ask_llm(question, hits):
    context = "\n\n".join(f"[page {h['page']}]\n{h['text']}" for h in hits)
    prompt = f"Answer using only the context below. Keep it short. If the answer is not in the context, say: I am unaware about it.\n\nContext:\n{context}\n\nQuestion: {question}"
    for part in ollama.chat(model=llm, messages=[{"role": "user", "content": prompt}], stream=True):
        yield part["message"]["content"]
