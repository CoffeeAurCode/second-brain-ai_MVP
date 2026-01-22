import time
from memory_writer import store_knowledge
from memory_retriever import retrieve_knowledge
from memory_evolution import apply_decay, reinforce_memory

# 1. Teaching it two facts
store_knowledge("The speed of light is 299,792 km/s.", "Physics", source="Textbook")
store_knowledge("The mitochondria is the powerhouse of the cell.", "Biology", source="Meme")
time.sleep(1)

# 2. Reinforcing the physics one
print("--- Reinforcing Physics ---")
for _ in range(3):
    results = retrieve_knowledge("fastest speed universe", topic="Physics")
    if results:
        # Simulate the user finding this useful
        reinforce_memory("knowledge_memory", results[0]['id'])

# 3. Bhari decay hoga
print("--- Time Passing (Decay) ---")
apply_decay("knowledge_memory", decay_rate=0.8) # 20% decay per 'day'

# 4. Check scores
print("--- Final Scores ---")
phys_res = retrieve_knowledge("speed of light", topic="Physics")
bio_res = retrieve_knowledge("mitochondria", topic="Biology")

print(f"Physics Score (Reinforced): {phys_res[0]['payload']['importance']:.4f}")
print(f"Biology Score (Neglected):  {bio_res[0]['payload']['importance']:.4f}")