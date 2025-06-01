import ollama

def extract_named_entities(summary: str, model="phi4-mini") -> list:
    prompt = (
        "From the following summary of a YouTube video, extract any named entities such as:\n"
        "- People\n- Organizations\n- Technologies\n- Locations\n- Events or Products\n\n"
        f"{summary}\n\n"
        "Return a bullet list of the named entities only."
    )

    response = ollama.chat(model=model, messages=[
        {"role": "user", "content": prompt}
    ])

    raw = response["message"]["content"]
    entities = [line.strip("-• ").strip() for line in raw.strip().split("\n") if line.strip()]
    return list(set(entities))  # remove duplicates