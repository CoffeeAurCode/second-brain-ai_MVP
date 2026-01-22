from memory_writer import store_interaction
from memory_retriever import retrieve_interactions
import time

# 1. Simulate a conversation 
conversations = [
    ("I need to fix a bug in the login API.", "debugging"),
    ("The server returns a 500 error on POST requests.", "debugging"),
    ("Remind me to buy milk later.", "personal")
]

print("--- Logging Conversation ---")
for text, intent in conversations:
    store_interaction(text, intent)

time.sleep(1)

# 2. User asks: "What was I working on?"
query = "login server error"
print(f"\nUser asks: '{query}'")

# 3. Retrieve context
memories = retrieve_interactions(query)

print("--- System Recall ---")
for mem in memories:
    print(f"Found: '{mem['text']}' (Intent: {mem['payload']['intent']})")