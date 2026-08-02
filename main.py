from rag import generate_rag_answer

if __name__ == "__main__":
    test_queries = [
        "What happens if I microwave fish?",
        "How much PTO do I get?"
    ]

    for query in test_queries:
        print(f"\nQuestion: {query}")
        print("-" * 40)
        answer = generate_rag_answer(query)
        print(f"Answer:\n{answer}\n")