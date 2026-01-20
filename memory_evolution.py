import time
import math
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, Range

try:
    client = QdrantClient(host="localhost", port=6333)
except Exception as e:
    print(f"Error initializing client: {e}")
    client = None
def reinforce_memory(collection_name: str, point_id: str, delta: float= 0.05):
    if not client: return
    try:
        points = client.retrieve(
            collection_name=collection_name,
            ids=[point_id],
            with_payload=True
        )
        if not points: 
            print(f"[Error] Point {point_id} not found in {collection_name}")
            return
        point = points[0]
        current_importance = point.payload.get("importance", 0.5)
        new_importance=min(1.0,current_importance+delta)
        client.set_payload(
            collection_name=collection_name,
            payload={"importance": new_importance},
            points=[point_id]
        )
        print(f"[REINFORCE] Updated {point_id}: {current_importance:.4f} -> {new_importance:.4f}")
    except Exception as E:
        print(f"Error Failed to reinforce memory: {E}")

def apply_decay(collection_name: str, decay_rate: float = 0.99):
    if not client: return
    print(f"DECAY!!!!!!!! Starting decay process for '{collection_name}'...")
    try:
        offset = None
        update_count=0
        current_time=time.time()
        while True:
            points, next_page_offset =client.scroll(
                collection_name=collection_name,
                offset=offset,
                limit=50, #processing in batches of 50
                with_payload=True
            )
            for point in points:
                payload=point.payload
                if "created_at" in payload and "importance" in payload:
                    created_at = payload["created_at"]
                    current_importance = payload["importance"]
                    age_seconds=current_time - created_at
                    days_old = age_seconds/(24*3600)
                    decay_factor = decay_rate**days_old
                    new_importance = current_importance*decay_factor
                    client.set_payload(
                        collection_name=collection_name,
                        payload={"importance": new_importance},
                        points=[point.id]
                    )
                    update_count += 1
            offset = next_page_offset
            if offset is None:
                break
        print(f"[Decay] Completed.....Updated {update_count} memories")
    except Exception as e:
        print(f"Error...Failed to apply decay: {e} ")

def cleanup_memory(collection_name: str, threshold: float = 0.2):

    if not client: return

    print(f"[CLEANUP] removing points with importance < {threshold} from '{collection_name}'...")
    try:
        delete_filter = Filter(
            must=[
                FieldCondition(
                    key="importance",
                    range=Range(lt=threshold)
                )
            ]
        )
        result = client.delete(
            collection_name=collection_name,
            points_selector=delete_filter
        )
        print(f"[CLEANUP] Operation status: {result}")
    except Exception as e:
        print(f"ERROR Failed to cleanup memory: {e} ")


if __name__ == "__main__":
    apply_decay("knowledge_memory")

    # Cleanup weak memories
    cleanup_memory("knowledge_memory")

    print("Memory evolution applied.")  
