# RAG from Scratch

This project is a Retrieval-Augmented Generation (RAG) system built from scratch in Python to answer questions using custom document chunks.

## What Has Been Done

1. BM25 Search: Implemented keyword-based lexical search using BM25Okapi.
2. Dense Vector Search: Used Sentence Transformers (`all-MiniLM-L6-v2`) to compute embeddings and match text semantically using dot product similarity.
3. Hybrid Search with RRF: Combined keyword and vector search results using Reciprocal Rank Fusion (RRF) to rank the most relevant text chunks.
4. Gemini Integration: Connected the retrieved context to Google's Gemini API (`gemini-3.5-flash`) so the model answers questions strictly using the provided documents.


## How to Setup and Run

1. Create and activate a virtual environment:
   python -m venv .venv
   source .venv/bin/activate

2. Install the required libraries:
   pip install rank-bm25 sentence-transformers python-dotenv google-genai numpy

3. Create a .env file in the project folder and add your Gemini API key:
   GEMINI_API_KEY=your_api_key_here

4. Run the main script:
   python main.py