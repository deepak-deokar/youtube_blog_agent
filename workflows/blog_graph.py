# workflows/blog_graph.py

from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from typing import TypedDict

# Import agents
from agents.transcript_agent import extract_transcript
from agents.summarizer_agent import summarize_chunks
from agents.blog_agent import generate_blog
from agents.topic_agent import extract_topics
from agents.sentiment_agent import detect_sentiment
from agents.ner_agent import extract_named_entities
from agents.rag_agent import retrieve_facts
from agents.condense_agent import condense_blog
from agents.post_edit_agent import post_edit_blog  # IMPROVEMENT: Added post-edit agent

# Load config
import yaml

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

RAG_SKIP_THRESHOLD = config["rag_skip_threshold"]
MODEL_NAME = config["model_name"]

# State
class BlogState(TypedDict, total=False):
    video_url: str
    transcript: str
    summary: str
    topics: list[str]
    sentiment: str
    entities: list[str]
    blog: str
    style: str
    enriched_facts: dict
    condensed: str

# === Agent nodes ===

transcript_node = RunnableLambda(lambda x: {
    "transcript": extract_transcript(x["video_url"])
})

summary_node = RunnableLambda(lambda x: {
    "summary": summarize_chunks(x["transcript"], model=MODEL_NAME)
})

topic_node = RunnableLambda(lambda x: {
    "topics": extract_topics(x["summary"])
})

sentiment_node = RunnableLambda(lambda x: {
    "sentiment": detect_sentiment(x["summary"])
})

ner_node = RunnableLambda(lambda x: {
    "entities": extract_named_entities(x["summary"])
})

# === IMPROVEMENT: Dynamic RAG logic ===
def conditional_rag(x):
    if len(x["transcript"]) < RAG_SKIP_THRESHOLD:
        print(f"[RAG] Skipping RAG (transcript length {len(x['transcript'])})")
        return {"enriched_facts": {}}
    else:
        print(f"[RAG] Running RAG (transcript length {len(x['transcript'])})")
        return {"enriched_facts": retrieve_facts(x["topics"])}

rag_node = RunnableLambda(conditional_rag)

# === Generate blog ===
def safe_generate_blog(x):
    print("[DEBUG] Generating full blog...")
    return {
        "blog": generate_blog(
            x["summary"],
            x["topics"],
            x.get("style", "neutral"),
            x.get("sentiment", "neutral"),
            x.get("entities", []),
            x.get("enriched_facts", {}),
            model=MODEL_NAME
        )
    }

blog_node = RunnableLambda(safe_generate_blog)

# === IMPROVEMENT: Post-edit agent ===
post_edit_node = RunnableLambda(lambda x: {
    "blog": post_edit_blog(x["blog"], model=MODEL_NAME)
})

# === Condense blog ===
condense_node = RunnableLambda(lambda x: {
    "condensed": condense_blog(x["blog"], model_name=MODEL_NAME)
})

# === Build graph ===
def create_blog_graph():
    graph = StateGraph(BlogState)

    graph.add_node("extract_transcript", transcript_node)
    graph.add_node("summarize", summary_node)
    graph.add_node("extract_topics", topic_node)
    graph.add_node("retrieve_facts", rag_node)
    graph.add_node("detect_sentiment", sentiment_node)
    graph.add_node("extract_entities", ner_node)
    graph.add_node("generate_blog", blog_node)
    graph.add_node("post_edit_blog", post_edit_node)  # IMPROVEMENT: Post-edit node
    graph.add_node("condense_blog", condense_node)

    graph.set_entry_point("extract_transcript")

    graph.add_edge("extract_transcript", "summarize")
    graph.add_edge("summarize", "extract_topics")

    graph.add_edge("extract_topics", "retrieve_facts")
    graph.add_edge("extract_topics", "detect_sentiment")
    graph.add_edge("extract_topics", "extract_entities")

    graph.add_edge("retrieve_facts", "generate_blog")
    graph.add_edge("detect_sentiment", "generate_blog")
    graph.add_edge("extract_entities", "generate_blog")

    # IMPROVEMENT: Post-edit after blog generation
    graph.add_edge("generate_blog", "post_edit_blog")

    # Condense after post-edit
    graph.add_edge("post_edit_blog", "condense_blog")
    graph.add_edge("condense_blog", END)

    return graph.compile()