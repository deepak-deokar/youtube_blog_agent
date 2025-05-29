from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from typing import TypedDict

from agents.transcript_agent import extract_transcript
from agents.summarizer_agent import summarize_text
from agents.blog_agent import generate_blog

# Define state keys
class BlogState(TypedDict):
    video_url: str
    transcript: str
    summary: str
    blog: str

# Define agent wrappers
transcript_node = RunnableLambda(lambda x: {"transcript": extract_transcript(x["video_url"])})
summary_node = RunnableLambda(lambda x: {"summary": summarize_text(x["transcript"])})
blog_node = RunnableLambda(lambda x: {"blog": generate_blog(x["summary"])})

# Create graph
def create_blog_graph():
    graph = StateGraph(BlogState)
    graph.add_node("extract_transcript", transcript_node)
    graph.add_node("summarize", summary_node)
    graph.add_node("generate_blog", blog_node)

    graph.set_entry_point("extract_transcript")
    graph.add_edge("extract_transcript", "summarize")
    graph.add_edge("summarize", "generate_blog")
    graph.add_edge("generate_blog", END)

    return graph.compile()