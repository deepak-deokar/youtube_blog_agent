import ollama

def detect_sentiment(summary: str, model="phi4-mini") -> str:
    prompt = (
        "Analyze the overall emotional tone or sentiment of the following video summary.\n"
        "Pick one of the following labels: inspirational, critical, casual, analytical, humorous, sad, neutral.\n\n"
        f"{summary}\n\n"
        "Return only the label."
    )

    response = ollama.chat(model=model, messages=[
        {"role": "user", "content": prompt}
    ])
    
    return response["message"]["content"].strip().lower()