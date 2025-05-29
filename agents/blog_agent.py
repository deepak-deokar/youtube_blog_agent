import ollama

def generate_blog(summary: str, model="phi4-mini") -> str:
    prompt = f"""Write a blog post with an engaging title based on the following summary. 
    Format it with a title, introduction, body, and conclusion.

    Summary:
    {summary}
    """
    response = ollama.chat(model=model, messages=[
        {"role": "user", "content": prompt}
    ])
    return response["message"]["content"]