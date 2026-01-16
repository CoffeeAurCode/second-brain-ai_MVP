import sys
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
def initialize_collections():
    client = QdrantClient(host ="localhost", port =6333) # Stting up connection,host and port
    vector_size = 384
    distance_metric = Distance.COSINE
    collections = [
        {
            "name": "knowledge_memory",
            "description": "Stores long term factual knowledge and documentation"
        },
        {
            "name": "interaction_memory",
            "description": "Stores history of user-agent interactions and logs"
        },
        {
            "name": "context_memory",
            "description": "Stores relevent context for current session or task"
        }
    ]
    print("Intializing Qdrant collections....")
    for col in collections:
        name = col["name"]
        if not client.collection_exists(collection_name=name):
            try:
                client.create_collection(
                    collection_name=name,
                    vectors_config=VectorParams(
                        size=vector_size,
                        distance=distance_metric
                    )
                )
                print(f"[SUCCESS] Created collections:'{name}' - {col['description']}")
            except Exception as e:
                print(f"[ERROR!!!!!] Failed to create collection '{name}': {e}")
        else:
            print(f"[SKIP] Collection '{name}' already exists")
# collection_name = "knowliedge_memory"  # the silly mistake

#     client.delete_collection(collection_name=collection_name)

#     print(f"Collection '{collection_name}' deleted successfully.")
if __name__ == "__main__":
    try:
        initialize_collections()
    except Exception as e:
        print(f"Critical Error: {e}")
        sys.exit(1)
