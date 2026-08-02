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


# print(f"Chunks: {len(chunks)}")
# print(chunks[7])

# Extract text only data from chunks
corpus_text = [c["text"] for c in chunks]

# Tokenize with BM25 for keyword search
tokenized_corpus = [text.lower().split() for text in corpus_text]
bm25_index = BM25Okapi(tokenized_corpus)

# Make NumpyMatrix of embeddings for semantic search
model = SentenceTransformer("all-MiniLM-L6-v2")
vector_matrix = model.encode(corpus_text, normalize_embeddings=True)
print(f"Vector matrix shape: {vector_matrix.shape}")

# Lexical Search with BM25
def lexical_search(query, top_k = 20):
    tokenized_query = query.lower().split()
    scores = bm25_index.get_scores(tokenized_query)

    # Get top_k indices sorted by score (descending)
    top_indices = np.argsort(scores)[::-1][:top_k]
    return [(idx, float(scores[idx])) for idx in top_indices]


def semantic_search(query, top_k = 20):
    query_vector = model.encode(query, normalize_embeddings=True)
    scores = np.dot(vector_matrix, query_vector )

    top_indices = np.argsort(scores)[::-1][:top_k]
    return [(idx, float(scores[idx])) for idx in top_indices]

# Reciprocal Rank Fusion (RRF)
def hybrid_search(query, top_k = 5, k_constant = 60): 

    bm25_results = lexical_search(query)
    vector_results = semantic_search(query)

    rrf_scores={}

    for rank, (idx, _) in enumerate(bm25_results, start=1):
        rrf_scores[idx] = rrf_scores.get(idx, 0.0) + (1/(k_constant + rank ))
    
    for rank, (idx, _) in enumerate(vector_results, start=1):
        rrf_scores[idx] = rrf_scores.get(idx, 0.0) + (1/(k_constant + rank))

    # Sort by descending order and by values, not index
    sorted_indices = sorted(rrf_scores.keys(), key=lambda i: rrf_scores[i], reverse=True)

    return [(idx, rrf_scores[idx]) for idx in sorted_indices[:top_k]]


if __name__ == "__main__":
    test_query = "What happens if I microwave fish?"
    
    hybrid_results = hybrid_search(test_query, top_k=3)

    for rank, (idx, rrf_score) in enumerate(hybrid_results, start=1):
        print(f"Rank {rank}, RRF Score: {rrf_score:.5f}, Chunk ID: {chunks[idx]['chunk_id']}")
        print(f"Text Snippet: {chunks[idx]['text'][:100]}...\n")


    # Lexical Search
    # bm25_results = lexical_search(test_query, top_k=3)
    # print("///Top 3 BM25 Matches")
    # for idx, score in bm25_results:
    #     print(f"Score: {score:.2f}, Chunk ID: {chunks[idx]['chunk_id']}")
    #     print(f"Text Snippet: {chunks[idx]['text'][:500]}\n")
        
    # Vector Search
    # vector_results = semantic_search(test_query, top_k=3)
    # print("///Top 3 Vector Semantic Matches")
    # for idx, score in vector_results:
    #     print(f"Score: {score:.4f}, Chunk ID: {chunks[idx]['chunk_id']}")
    #     print(f"Text Snippet: {chunks[idx]['text'][:500]}\n")