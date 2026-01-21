import time
from memory_writer import store_knowledge, store_interaction
from memory_retriever import retrieve_knowledge
from memory_evolution import apply_decay, cleanup_memory, reinforce_memory

def main():
    print("...............Second Brain System Demo.............................\n")

    # Yaad ho raha hai
    print("Step 1: Storing Knowledge...")
    topic = "Machine Learning"
    knowledge_text = (
        "Gradient descent is an optimization algorithm used to minimize some function "
        "by iteratively moving in the direction of steepest descent as defined by the negative of the gradient."
    )
    store_knowledge(text=knowledge_text, topic=topic, source="demo_script")
    
    # Sone se accha yaad hota hai
    time.sleep(1) 

    
    print("\nStep 2: Storing User Interaction...")
    user_query = "Can you explain how gradient descent works?"
    store_interaction(text=user_query, intent="explanation_request")
    
    time.sleep(1)

    # 3. Retrieve Knowledge (Before Decay)
    print(f"\nStep 3: Retrieving Knowledge for query: '{user_query}'")
    results = retrieve_knowledge(query=user_query, topic=topic)
    
    print(f"Found {len(results)} results:")
    for res in results:
        payload = res['payload']
        print(f" - [Score: {res['score']:.4f}] {res['text'][:80]}...")
        print(f"   Importance: {payload.get('importance')}")

    print("\nStep 4: Reinforceing Retrived Memories....")
    if results:
        for res in results:
            reinforce_memory(collection_name="knowledge_memory", point_id=res['id'])
    else:
        print("no memories to reinforce")
    #  Apply Decay
    print("\nStep 5: Applying Memory Decay...")
    # In a real app, this would be closer to 0.99
    apply_decay(collection_name="knowledge_memory", decay_rate=0.5)

    #  Cleanup Memory
    print("\nStep 6: Running Memory Cleanup...")
    # Remove memories that have fallen below 0.2 importance
    cleanup_memory(collection_name="knowledge_memory", threshold=0.2)

    #  Retrieve Knowledge (After Decay/Cleanup)
    print("\nStep 7: Retrieving Knowledge Again (After Evolution)...")
    results_after = retrieve_knowledge(query=user_query, topic=topic)
    
    if not results_after:
        print("No results found. The memory might have been cleaned up due to low importance.")
    else:
        print(f"Found {len(results_after)} results:")
        for res in results_after:
            payload = res['payload']
            print(f" - [Score: {res['score']:.4f}] {res['text'][:80]}...")
            print(f"   Importance: {payload.get('importance')}")

    print("\n...........Demo Complete................")

if __name__ == "__main__":
    main()