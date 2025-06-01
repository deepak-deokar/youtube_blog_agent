import ollama

def extract_topics(summary: str, model="phi4-mini") -> list:
    prompt = (
        "Given the following summary of a YouTube video, extract 3 to 5 high-level topics "
        "or themes that are discussed. Only return a plain list.\n\n"
        f"{summary}\n\n"
        "Return format:\n- Topic A\n- Topic B\n- Topic C"
    )

    response = ollama.chat(model=model, messages=[
        {"role": "user", "content": prompt}
    ])

    # Parse bullet list
    raw = response["message"]["content"]
    lines = [line.strip("- ").strip() for line in raw.strip().split("\n") if line.strip()]
    return [line for line in lines if line]  # ensure non-empty