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
: `./dev`