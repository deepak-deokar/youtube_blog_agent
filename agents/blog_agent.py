import ollama

def generate_blog(summary: str, style: str = "neutral", model="phi4-mini") -> str:
    prompt = f"""Write a blog post with an engaging title based on the following summary. 
    Format it with a title, introduction, main content, and conclusion.

    Summary:
    {summary}
    """
    response = ollama.chat(model=model, messages=[
        {"role": "user", "content": prompt}
    ])
    return response["message"]["content"]