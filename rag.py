import os
from google import genai
from dotenv import load_dotenv
from search import hybrid_search, chunks

load_dotenv()

client = genai.Client()

def generate_rag_answer(query, top_k=3):
    rrf_results = hybrid_search(query, top_k)


    #Building context for llm
    context_blocks = []
    for rank, (idx, score) in enumerate(rrf_results, start=1):
        chunk_text = chunks[idx]["text"]
        chunk_id = chunks[idx]["chunk_id"]
        context_blocks.append(f"--- Source {rank} [{chunk_id}] ---\n{chunk_text}")
        context_str = "\n\n".join(context_blocks)


        prompt = f"""You are a helpful company policy assistant. Answer the user's question strictly based on the context below. If the answer isn't in the context, say that the policy doesn't mention it. Context: {context_str} User Question: {query} """

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return response.text