from chayan.answer import ask_llm
from chayan.bm25 import build
from chayan.config import top_k
from chayan.index import load_index
from chayan.pipeline import load_cutoff, run

def main():
    chunks, vectors = load_index("table")
    idx, cutoff = build(chunks), load_cutoff()
    print(len(chunks), "chunks ready, empty line to quit")
    while q := input("\nask> ").strip():
        route, hits = run(q, chunks, vectors, idx, k=top_k)
        if hits[0]["rerank"] < cutoff: print("I am unaware about it")
        else:
            for part in ask_llm(q, hits): print(part, end="", flush=True)
            print()
        print("\nroute:", route, "| sources:", ", ".join(f"p{h['page']} ({h['rerank']})" for h in hits))

if __name__ == "__main__":
    main()
