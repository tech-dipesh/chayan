# Chayan:
Chayan Rag Read every pdf that you uploaded

- REad the Pdf From a Retrieval Augmentation Generation
-
## Features:
- Building a rag Chunking system while other are just for the chunking for every document, rather it make a profiles for each pdf, with test the multiple chunk and retrieval strategies with from own generated question and make the winner.
Load a big PDF and keep page numbers, text blocks, font sizes and table regions.
Profile the PDF (pages, table density, heading ratio, scanned or not).
Four chunkers behind one interface: fixed, recursive, heading-aware, table-aware.
Three retrievers: dense, BM25, hybrid (reciprocal rank fusion).
Eval questions generated from pages, not chunks, so no chunker gets an unfair edge.
Scoring with hit@k, MRR, latency and index size for all 12 combinations.
Rule-based failure labels for every miss.
Chat on the winning combination, with source pages shown.
Start Project: 06/10/2026

## How it Work:
- The Rag System answers most probably hold answer or ask llm
- the llm integration i belive it'll be a complex so let's see 

## Way to Run a Server:
- uv sync
- `./dev`



## For This Soluton I'm trying to take a approach of the tencent 2025 annual report with a sepcific page:
- It include a only a specific pdf pages.
- Every thing i include here is the local
- No cluod api is needed
- as Of now the vector database as it's a real time response
- with teh ask question and the evaluation and the self generaation question.
- **Our smallest modeel qwen model of 3b with 4gb gpu weill can read a 4 paragraph at a time.**
- If retrieval pick a wrong one we just make a retriaval no chat.


## Table Aware Chunking:
- For Now the chunking is the simplere now it try to become a more clever based on the table aware chunking
- The initally there is the starting with the: `data/tencent.pdf` which is a pdf and goes to the: 


## Working:
    data/tecent.pdf
          |
          v
    ingest.py      pypdf reads pages 5-26 -> [{page, text}]
          |
          v
    chunk.py       fixed 800 chars, 100 overlap     \  two chunkers,
    recursive.py   paragraph > line > sentence      /  same output shape
          |
          v
    embed.py       Ollama nomic-embed-text -> one vector per chunk
          |
          v
    index.py       normalise, save .cache/<hash>.json + .npy
          |
    ------+------------------------- question time -------------------
          |
    ask.py   you type a question
          |
          v
    search.py      embed the question, dot product with all chunks, top 4
          |
          v
    answer.py      chunks + question -> Ollama qwen2.5:3b, streamed
          |
          v
    answer text + "sources: p7 (0.76), p22 (0.68) ..."

## How We Making a Chunk:


Pages are read first, then chunked page by page, so every chunk keeps the PDF page it
came from. That page number is what makes citations possible, and later it is what lets
page-based evaluation compare chunkers fairly.

Fixed chunker: cut every 800 characters, step back 100 so neighbours overlap. Fast and
predictable, but it cuts through sentences and through table rows.

Recursive chunker: try to split on blank lines, then on line breaks, then on ". ", then
on spaces, and pack the pieces up to 800 characters. Chunks end where the text naturally
ends. Chunks under 50 characters are dropped as page-number noise.
