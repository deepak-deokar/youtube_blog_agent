import wikipedia

def retrieve_facts(topics: list[str], max_sentences: int = 3) -> dict:
    enriched = {}
    for topic in topics:
        try:
            summary = wikipedia.summary(topic, sentences=max_sentences)
            enriched[topic] = summary
        except Exception:
            enriched[topic] = "(No additional fact found)"
    return enriched