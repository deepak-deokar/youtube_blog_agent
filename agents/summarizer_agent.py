import ollama

def summarize_text(text: str, model="phi4-mini") -> str:
    prompt = f"Summarize the following transcript:\n\n{text[:3000]}"
    response = ollama.chat(model=model, messages=[
        {"role": "user", "content": prompt}
    ])
    return response["message"]["content"]