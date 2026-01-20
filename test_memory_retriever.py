from memory_retriever import retrieve_knowledge, retrieve_interactions

print("---- Knowledge Retrieval ----")
results = retrieve_knowledge(
    query="Explain gradient descent",
    topic="machine_learning"
)

for r in results:
    print(r["score"], r["payload"]["topic"], r["text"][:60])

print("\n---- Interaction Retrieval ----")
results = retrieve_interactions(
    query="Explain gradient descent"
)

for r in results:
    print(r["score"], r["payload"]["intent"], r["text"][:60])
