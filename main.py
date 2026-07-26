from pathlib import Path
import frontmatter
import numpy as np 
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer


chunks = []
# Fetch files and split into chunks
for file_path in Path("dzcore_dynamics_handbook").rglob("*.md"):
    doc = frontmatter.load(file_path)
    meta = doc.metadata

    # Split into Paragraphs first
    paragraphs = [p.strip() for p in doc.content.split("\n\n") if p.strip() ]

    # Split to chunks
    for i, para in enumerate(paragraphs):
        dept = meta.get('department', 'N/A')
        title = meta.get('title', 'N/A')
        prefix = f"[Dept: {dept} | Title: {title}] "

        chunks.append({
            "chunk_id": f"{meta.get('id', 'DOC')}_c{i}",
            "text": prefix + para,
            "metadata": meta
        })


print(f"Chunks: {len(chunks)}")
print(chunks[7])

# Extract text only data from chunks
corpus_text = [c["text"] for c in chunks]

# Tokenize with BM25 for keyword search
tokenized_corpus = [text.lower().split() for text in corpus_text]
bm25_index = BM25Okapi(tokenized_corpus)

# Make NumpyMatrix of embeddings for semantic search
model = SentenceTransformer("all-MiniLM-L6-v2")
vector_matrix = model.encode(corpus_text, normalize_embeddings=True)
print(f"Vector matrix shape: {vector_matrix.shape}")