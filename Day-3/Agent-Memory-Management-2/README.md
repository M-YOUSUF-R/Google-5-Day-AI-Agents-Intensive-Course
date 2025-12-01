# Agent Memory Management-2

## What is Memory
Memory is a service that provides long-term knowledge storage for your agents. The key distinction:

```
Session = Short-term memory (single conversation)

Memory = Long-term knowledge (across multiple conversations)
```

Think of it in software engineering terms: Session is like application state (temporary), while Memory is like a database (persistent).

## Why Memory ?

| Capability |	What It Means |	Example |
|------------|----------------|---------|
|Cross-Conversation Recall|Access information from any past conversation|"What preferences has this user mentioned across all chats?"|
|Intelligent Extraction|LLM-powered consolidation extracts key facts|Stores "allergic to peanuts" instead of 50 raw messages|
|Semantic Search|Meaning-based retrieval, not just keyword matching|Query "preferred hue" matches "favorite color is blue"|
|Persistent Storage|Survives application restarts|Build knowledge that grows over time|
---
### Sometimes `load_memory` miss but `preload_memory` always check and fetch the data.
