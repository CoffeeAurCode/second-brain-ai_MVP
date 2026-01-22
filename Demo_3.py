from memory_writer import store_knowledge
from memory_retriever import retrieve_knowledge
import time

# 1. Store data
store_knowledge("Apples are rich in fiber and vitamin C.", "Nutrition")
store_knowledge("Apple Inc. was founded by Steve Jobs.", "Tech")
time.sleep(1)

# 2. Search with Topic Filter
print("--- Query: 'Apple' (Filter: Tech) ---")
tech_results = retrieve_knowledge("Apple", topic="Tech")
for r in tech_results:
    print(f"Result: {r['text']}")

print("\n--- Query: 'Apple' (Filter: Nutrition) ---")
food_results = retrieve_knowledge("Apple", topic="Nutrition")
for r in food_results:
    print(f"Result: {r['text']}")