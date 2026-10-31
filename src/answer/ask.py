from src.answer.llm import ask_llm
from src.retrieval.bm25 import build
from src.config import top_k
from src.retrieval.index import load_index
from src.answer.pipeline import gate_score, load_cutoff, run
from src.retrieval.rewrite import rewrite

def main():
    chunks, _ = load_index("table")
    idx, cutoff = build(chunks), load_cutoff()
    print(len(chunks), "chunks ready, empty line to quit")
    while raw := input("\nask> ").strip():
        q = rewrite(raw)
        if q != raw: print("searching:", q)
        hits = run(q, chunks, idx, top_k)
        score = gate_score(q, hits)
        if score < cutoff: print("I am unaware about it")
        else:
            for part in ask_llm(q, hits): print(part, end="", flush=True)
            print()
        pages = ", ".join("p" + str(h["page"]) for h in hits)
        print(f"\nsources: {pages} | check {score}/10")

if __name__ == "__main__":
    main()
