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

## RAG:
The Rag that is on the : `search.py, bm25.py and hybrid.py` for the G answer.py for answre wth the augmentation prompt buidl for the `answer.py` with a chunk label where else it can response with a `I am unaware about it`

## Vector Database:
As of now the vector database haven't implemented as of now just a simplest implemntation value, is somethings that on the index from a `numpy` array. With the one row per chunking form, 768 numbers per row value.
The Every row is on the scaled length 1. For the `cosine similarity` for the dot product. for building a simpler values, `vectores @ query`. For the 70 chunk each chunking happend on the `microseconds.` a database for the Chroma db for the FAISS earns the place for the brute force going slow.
When the filter and the update happaned for the hide part on the matter form.

## Ollama Used:
Ollama runs as a local server. The python package ollama sends it two kinds of requests:

- ollama.embed with nomic-embed-text, in batches of 32. nomic expects a prefix, so chunks
  go in as "search_document: ..." and questions as "search_query: ...".
- ollama.chat with qwen2.5:3b and stream=True, so words appear as they are generated.

Model names live in config.py, so trying another model is one line.

## Retrievers

- dense: meaning match through embeddings. Good at paraphrase, weak at exact tokens
  like HKD5.30 or a name.
- bm25: keyword match with term rarity and length weighting, written in plain python.
- hybrid: take the top 20 of each and merge with reciprocal rank fusion, score
  1 / (60 + rank). Only ranks are used, so the two score scales never need to match.

ask.py currently uses dense only. bm25 and hybrid are used by the evaluation first.
