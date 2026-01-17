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
