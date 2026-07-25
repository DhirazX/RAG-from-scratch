from pathlib import Path
import frontmatter
import numpy as np 
from sentence_transformers import SentenceTransformers


chunks = []
# Fetch files and split into chunks
for file_path in Path(".").rglob("*.md"):
    doc = frontmatter.load(file_path)
    meta = doc.meta

    # Split into Paragraphs first
    paragraphs = [p.strip() for p in doc.content.split("/n/n") if p.strip() ]

    # Split to chunks
    for i, para in enumerate(paragraphs):
        prefix = f"[Dept: {meta.get("department", "N/A")} | Title: {meta.get("title", "N/A")}]"

        chunks.append({
            "chunk_id": f"{meta.get('id', 'DOC')}_c{i}",
            "text": prefix + para,
            "metadata": meta
        })


print(f"Chunks: {len(chunks)}")