# second-brain-ai (qdrant-based)

this project is a minimal Second brain AI system using qdrant as the primary vector memory store


Status: Environment Setup complete (YAY!)


## Memory Architecture

The system uses Qdrant as the primary memory store.

Three typed memory collections are defined:
- knowledge_memory: long-term semantic knowledge(hard disk)
- context_memory: short-lived working context(RAM)
- interaction_memory: conversation traces and user intent(EQ)

All future retrieval and memory evolution operates exclusively on these collections.

## Embeddings

Text is converted into semantic vector representations using the
sentence-transformers model `all-MiniLM-L6-v2`.

These vectors capture semantic meaning and are used as the primary
signal for similarity search in Qdrant.

## Memory Writing
The system writes structured memories into Qdrant using semantic embeddings.
Each memory is stored with explicit metadata such as type, topic/intent,
importance, and creation time.

This enables controlled retrieval and future memory evolution.

## Design Decisions & Robustness
While Qdrant provides high-level client helpers for vector search, during development it was observed that certain helper methods (such as search / search_points) were not consistently available across client builds and environments.

To ensure maximum robustness, portability, and correctness, this system performs vector search using Qdrant’s official REST search endpoint
Using the REST API directly ensures that:

Qdrant remains the primary and authoritative vector search engine

Retrieval behavior is deterministic and reproducible

The system does not depend on SDK-specific abstractions that may vary by platform

Importantly, this does not change the architecture or capabilities of the system's semantic vector search, payload filtering, and memory retrieval are still performed entirely by Qdrant.

This design choice improves system reliability and reflects real-world engineering practices where stable lower-level interfaces are preferred when higher-level abstractions are inconsistent.
All memory retrieval is performed via semantic vector search with payload-based filtering, demonstrating memory recall as an active system capability rather than passive storage.