import sys
import requests
import json
from typing import List, Optional, Dict, Any

try:
    from embeddings import embed
except ImportError:
    print("[Error] Could not import 'embed' from embeddings")
    def embed(text): return [0.0]*384
QDRANT_HOST = "http://localhost:6333"

def retrieve_knowledge(query: str, topic: Optional[str] = None, limit: int = 5) -> List[Dict[str, Any]]:
    url = f"{QDRANT_HOST}/collections/knowledge_memory/points/search"

    try:
        vector=embed(query)
        must_conditions=[
            {"key": "memory_type", "match": {"value": "knowledge"}},
            {"key": "importance", "range":{"gte": 0.3}}
        ]
        if topic:
            must_conditions.append({"key": "topic", "match":{"value": topic}})
        payload={
            "vector": vector,
            "limit":limit,
            "with_payload": True,
            "filter":{
                "must": must_conditions
            }
        }
        response= requests.post(url, json=payload,timeout=5)  #execute a request
        response.raise_for_status() #this will raise error for bad status codes
        data = response.json()
        results_list = []
        for hit in data.get("result", []):
            item_payload = hit.get("payload", {})
            results_list.append({
                "id": hit.get("id"), #id daalna bhul gaya tha
                "text": item_payload.get("text", ""),
                "payload": item_payload,
                "score": hit.get("score",0.0)
            })
        return results_list
    except Exception as e:
        print(f"[ERROR] retrieval of knowledge failed: {e}") #simple bhasha mei yaad nahi aa raha lekin yaad kiya tha
        return []
def retrieve_interactions(query: str, limit: int = 3) -> List[Dict[str, Any]]:
    url = f"{QDRANT_HOST}/collections/interaction_memory/points/search"
    try:
        vector=embed(query)
        must_conditions=[
            {"key": "memory_type", "match": {"value": "interaction"}}
        ]
        payload={
            "vector": vector,
            "limit":limit,
            "with_payload": True,
            "score_threshold": 0.5, #Fix to get the most relevent interaction
            "filter":{
                "must": must_conditions
            }
        }
        response= requests.post(url, json=payload,timeout=5)  #execute a request
        response.raise_for_status() #this will raise error for bad status codes
        data = response.json()
        results_list = []
        for hit in data.get("result", []):
            item_payload = hit.get("payload", {})
            results_list.append({
                "id": hit.get("id"),
                "text": item_payload.get("text", ""),
                "payload": item_payload,
                "score": hit.get("score",0.0)
            })
        return results_list
    except Exception as e:
        print(f"[ERROR] retrieval of interaction failed: {e}") #simple bhasha mei yaad nahi aa raha 
        return[]
if __name__ == "__main__":
    print("--- Testing Knowledge Retrieval (REST) ---")
    k_res = retrieve_knowledge("test query")
    print(f"Found {len(k_res)} knowledge items.")
    for item in k_res:
        print(f" - [{item['score']:.2f}] {item['text'][:50]}...")
    
    print("\n--- Testing Interaction Retrieval (REST) ---")
    i_res = retrieve_interactions("test query")
    print(f"Found {len(i_res)} interaction items.")
    for item in i_res:
        print(f" - [{item['score']:.2f}] {item['text'][:50]}...")