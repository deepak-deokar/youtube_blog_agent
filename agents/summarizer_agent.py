# agents/summarizer_agent.py

from agents.chunking_agent import chunk_text
import ollama

# IMPROVEMENT: Uses improved chunk_text() → paragraph-aware

def summarize_chunks(text: str, model="phi4-mini") -> str:
    chunks = chunk_text(text)
    summaries = []

    for i, chunk in enumerate(chunks):
        # IMPROVEMENT: Stronger prompt → more focused summary
        prompt = f"""
Summarize the following section of a YouTube transcript in clear and concise blog-friendly language (Part {i+1}):

Section:
{chunk}
"""
        response = ollama.chat(model=model, messages=[
            {"role": "user", "content": prompt}
        ])
        summary = response["message"]["content"]
        summaries.append(summary)

    # Merge all summaries
    full_summary_prompt = "Combine these partial summaries into a cohesive blog summary:\n\n" + "\n\n".join(summaries)
    final_response = ollama.chat(model=model, messages=[
        {"role": "user", "content": full_summary_prompt}
    ])
    return final_response["message"]["content"]