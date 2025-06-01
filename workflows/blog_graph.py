from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from typing import TypedDict

from agents.transcript_agent import extract_transcript
from agents.summarizer_agent import summarize_chunks
from agents.blog_agent import generate_blog
from agents.topic_agent import extract_topics
from agents.sentiment_agent import detect_sentiment
from agents.ner_agent import extract_named_entities
from agents.rag_agent import retrieve_facts
from agents.condense_agent import condense_blog

# Define state keys
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

# === Agent wrappers ===

def safe_extract_transcript(x):
    transcript = extract_transcript(x["video_url"])
    if "[Error" in transcript:
        raise ValueError(transcript)
    print("[DEBUG] Transcript extracted.")
    return {"transcript": transcript}

transcript_node = RunnableLambda(safe_extract_transcript)

summary_node = RunnableLambda(lambda x: (
    print("[DEBUG] Summarizing transcript...") or {"summary": summarize_chunks(x["transcript"])}
))

topic_node = RunnableLambda(lambda x: (
    print("[DEBUG] Extracting topics...") or {"topics": extract_topics(x["summary"])}
))

sentiment_node = RunnableLambda(lambda x: (
    print("[DEBUG] Detecting sentiment...") or {"sentiment": detect_sentiment(x["summary"])}
))

ner_node = RunnableLambda(lambda x: (
    print("[DEBUG] Extracting named entities...") or {"entities": extract_named_entities(x["summary"])}
))

rag_node = RunnableLambda(lambda x: (
    print("[DEBUG] Retrieving facts...") or {"enriched_facts": retrieve_facts(x["topics"])}
))

condense_node = RunnableLambda(lambda x: (
    print("[DEBUG] Condense Blog...") or {"condensed": condense_blog(x["blog"], model_name="phi4-mini")}
))

def safe_generate_blog(x):
    try:
        print("[DEBUG] Generating blog...")
        return {
            "blog": generate_blog(
                x["summary"],
                x["topics"],
                x.get("style", "neutral"),
                x.get("sentiment", "neutral"),
                x.get("entities", []),
                x.get("enriched_facts", {})
            )
        }
    except Exception as e:
        print(f"[ERROR] Blog generation failed: {e}")
        return {"blog": f"[Error generating blog] {e}"}

blog_node = RunnableLambda(safe_generate_blog)

# === Create LangGraph ===
def create_blog_graph():
    graph = StateGraph(BlogState)

    graph.add_node("extract_transcript", transcript_node)
    graph.add_node("summarize", summary_node)
    graph.add_node("extract_topics", topic_node)
    graph.add_node("retrieve_facts", rag_node)
    graph.add_node("detect_sentiment", sentiment_node)
    graph.add_node("extract_entities", ner_node)
    graph.add_node("generate_blog", blog_node)
    graph.add_node("condense_blog", condense_node)

    graph.set_entry_point("extract_transcript")

    graph.add_edge("extract_transcript", "summarize")
    graph.add_edge("summarize", "extract_topics")

    # Parallel edges!
    graph.add_edge("extract_topics", "retrieve_facts")
    graph.add_edge("extract_topics", "detect_sentiment")
    graph.add_edge("extract_topics", "extract_entities")

    # All converge to generate_blog
    graph.add_edge("retrieve_facts", "generate_blog")
    graph.add_edge("detect_sentiment", "generate_blog")
    graph.add_edge("extract_entities", "generate_blog")

    graph.add_edge("generate_blog", "condense_blog")
    graph.add_edge("condense_blog", END)

    return graph.compile()