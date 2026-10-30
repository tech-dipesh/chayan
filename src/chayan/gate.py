import json
from chayan.bm25 import build
from chayan.config import root
from chayan.index import load_index
from chayan.page_questions import make_page_questions
from chayan.pipeline import run

unaware = [
    "When was Tencent founded?",
    "Where is Tencent's headquarters located?",
    "Who is the chief executive officer of Apple?",
    "What was Alibaba's revenue in 2025?",
    "What is the capital of France?",
    "Which university did Ma Huateng attend?",
    "What is the weather in Shenzhen today?",
    "What was Tencent's revenue in 2010?",
    "Who won the 2022 FIFA World Cup?",
    "What is the boiling point of water?",
]

def main():
    chunks, vectors = load_index("table")
    idx = build(chunks)
    top = lambda q: run(q, chunks, vectors, idx)[1][0]["rerank"]
    good = [top(q["question"]) for q in make_page_questions()]
    bad = [top(q) for q in unaware]
    print("cutoff  answerable kept  unaware rejected")
    for c in range(11): print(f"{c:6d}  {sum(s >= c for s in good) / len(good):15.2f}  {sum(s < c for s in bad) / len(bad):16.2f}")
    best = max(range(11), key=lambda c: (sum(s >= c for s in good) + sum(s < c for s in bad), -c))
    print("best cutoff:", best)
    (root / "data" / "cutoff.json").write_text(json.dumps({"min_score": best, "answerable": good, "unaware": bad}))

if __name__ == "__main__":
    main()
