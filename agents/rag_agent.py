# agents/rag_agent.py

import wikipedia
import os
import json

# IMPROVEMENT: Simple local cache → speeds up repeat runs

# Cache file path
CACHE_FILE = "rag_cache.json"

# Load cache if exists
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r") as f:
        rag_cache = json.load(f)
else:
    rag_cache = {}

def retrieve_facts(topics: list[str]) -> dict:
    global rag_cache
    facts = {}

    for topic in topics:
        if topic in rag_cache:
            print(f"[RAG] Using cached fact for {topic}")
            facts[topic] = rag_cache[topic]
            continue

        try:
            summary = wikipedia.summary(topic, sentences=3)
            facts[topic] = summary
            rag_cache[topic] = summary  # IMPROVEMENT: Save to cache
            print(f"[RAG] Retrieved fact for {topic}")
        except Exception as e:
            print(f"[RAG] Failed for {topic}: {e}")
            facts[topic] = "[No external fact available]"

    # Save updated cache
    with open(CACHE_FILE, "w") as f:
        json.dump(rag_cache, f, indent=2)

    return facts