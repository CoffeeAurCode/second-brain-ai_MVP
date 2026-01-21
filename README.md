# second-brain-ai (qdrant-based)

this project is a minimal Second brain AI system using qdrant as the primary vector memory store


## How to Run

1. Start Qdrant locally:
   docker run -p 6333:6333 qdrant/qdrant

2. Install dependencies:
   pip install -r requirements.txt

3. Run the demo:
   python demo.py

The demo will store knowledge, retrieve relevant memories,
apply memory evolution, and retrieve again.



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

## Memory Evolution

Memory in the system is not static. Each memory item carries an importance
score that evolves over time.

- Frequently retrieved memories are reinforced
- Older memories gradually decay
- Low-importance memories are removed

This enables long-term memory management beyond a single prompt and
prevents uncontrolled memory growth.

Retrieved memories are reinforced by increasing their importance score,
creating a feedback loop where frequently used knowledge becomes more persistent.


## Societal Relevance

Modern students and knowledge workers suffer from fragmented information
spread across notes, documents, and conversations.

This project demonstrates a Second Brain system that:
- Retains important knowledge over time
- Forgets irrelevant information
- Reinforces frequently used concepts

Such systems can reduce cognitive overload, support long-term learning,
and improve knowledge reuse without relying on constant re-prompting.


## Limitations & Future Work

This system is intentionally minimal to prioritize correctness and clarity.
Future work could include multimodal memory, user-specific personalization,
and learned reinforcement policies instead of fixed rules.

## Multimodal Support (Design Consideration)

This MVP focuses on text-based semantic memory to prioritize correctness,
clarity, and robustness within the given time constraints.

However, the architecture is intentionally designed to be modality-agnostic.
Qdrant collections, payload schemas, and retrieval logic can directly support
additional modalities such as images, audio, code, or sensor data by storing
their corresponding embeddings alongside modality metadata.

For example:
- Images → CLIP embeddings
- Audio → Whisper or audio embedding models
- Code → Code-specific embedding models

No architectural changes are required to extend the system beyond text.
To add multimodal later, you would only add:
"modality": "image" | "audio" | "text"
and use a different embedding function.

Nothing else changes.


Interaction memory is currently stored to capture user intent and conversation traces.
It is not retrieved in the demo, as it primarily supports future context-aware
and personalized behaviors rather than factual recall.
