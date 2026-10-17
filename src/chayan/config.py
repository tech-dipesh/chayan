
from pathlib import Path

root = Path(__file__).resolve().parents[2]
pdf_path = root / "data" / "tecent.pdf"
first_page, last_page = 5, 26
chunk_size, overlap = 800, 100
top_k = 4
llm = "qwen2.5:3b"
embed = "nomic-embed-text"
