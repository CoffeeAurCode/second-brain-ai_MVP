import time, uuid
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

try:
    from embeddings import embed
except ImportError:
    print("Error: Could not import 'embed' from 'embeddings'. Please ensure the file exists.")
    def embed(text):
        return [0.0]*384

client = QdrantClient(host="localhost", port=6333)
def store_knowledge(text: str, topic: str, source: str = "manual"):
    #storing factual knowlege into the knowledge memory using semantic embeddings
    collection_name = "knowledge_memory"
    vector = embed(text) 
    point_id= str(uuid.uuid4())
    payload = {
        "text": text, #context
        "memory_type": "knowledge",
        "topic": topic, #content ka subject
        "source": source, #content ka source
        "importance": 0.5, 
        "created_at": time.time()
    }
    try:
        client.upsert(
            collection_name=collection_name,
            points=[
                PointStruct(
                    id=point_id,
                    vector=vector,
                    payload=payload
                )
            ]
        )
        print(f"[KNOWLEDGE] Storied: '{topic}' | ID: {point_id}")
    except Exception as e:
        print(f"[ERROR] Could not store Knowledge: {e}")

def store_interaction(text: str, intent: str):
    #this stores user interaction in the interaction memory
    collection_name="interaction_memory"
    vector=embed(text)
    point_id= str(uuid.uuid4())
    payload = {
        "text": text,
        "memory_type": "interaction",
        "intent": intent,
        "importance": 0.3,
        "created_at": time.time()
    }
    try:
        client.upsert(
            collection_name=collection_name,
            points=[
                PointStruct(
                    id=point_id,
                    vector=vector,
                    payload=payload
                )
            ]
        )
        print(f"[Interaction] Stored: '{intent}' | ID: {point_id}")
    except Exception as e:
        print(f"[Error] Could not store interaction: {e}")

if __name__ == "__main__":
    #simple test to verify the module works stand alone
    store_knowledge(
        text="The mitochondria is the power house of the cell",
        topic= "Biology",
        source= "textbook"
    )
    store_interaction(
        text="Why is kolaveri Di",
        intent="query"
    )