# agents/ner_agent.py

import ollama
import re

# IMPROVEMENT: Added post-filtering → removes junk entities

def extract_named_entities(summary: str, model="phi4-mini") -> list:
    prompt = f"""
Extract the important named entities (people, organizations, places, products) from the following text.
Return them as a comma-separated list:

Text:
{summary}
"""
    response = ollama.chat(model=model, messages=[
        {"role": "user", "content": prompt}
    ])
    raw_entities = response["message"]["content"]

    # IMPROVEMENT: Basic post-processing
    # Split by comma, strip spaces, remove duplicates
    entities = [e.strip() for e in raw_entities.split(",") if e.strip()]
    entities = list(set(entities))  # deduplicate

    # IMPROVEMENT: Filter out numeric-only entities and short junk
    filtered_entities = []
    for e in entities:
        if len(e) < 3:
            continue
        if re.match(r"^\d+$", e):
            continue
        filtered_entities.append(e)

    print(f"[DEBUG] Extracted entities: {filtered_entities}")
    return filtered_entities