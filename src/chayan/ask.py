from chayan.answer import ask_llm
from chayan.index import load_index
from chayan.search import search


def main():
    chunks, vectors = load_index()
    print(len(chunks), "chunks ready, empty line to quit")
    while q := input("\nask> ").strip():
        hits = search(q, chunks, vectors)
        for part in ask_llm(q, hits): print(part, end="", flush=True)
        print("\n\nsources:", ", ".join(f"p{h['page']} ({h['score']:.2f})" for h in hits))

if __name__ == "__main__":
    main()
