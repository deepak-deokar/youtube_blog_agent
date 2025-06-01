from agents.chunking_agent import chunk_text
import ollama

def summarize_chunks(text: str, model="phi4-mini") -> str:
    chunks = chunk_text(text)
    summaries = []

    for i, chunk in enumerate(chunks):
        prompt = f"Summarize the following part of a transcript (Part {i+1}):\n\n{chunk}"
        response = ollama.chat(model=model, messages=[
            {"role": "user", "content": prompt}
        ])
        summary = response["message"]["content"]
        summaries.append(summary)

    # Merge all summaries into one
    full_summary_prompt = "Combine these partial summaries into a coherent summary:\n\n" + "\n\n".join(summaries)
    final_response = ollama.chat(model=model, messages=[
        {"role": "user", "content": full_summary_prompt}
    ])
    return final_response["message"]["content"]