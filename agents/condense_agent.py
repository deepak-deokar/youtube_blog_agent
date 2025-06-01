import ollama

def condense_blog(full_blog: str, model_name="phi4-mini") -> str:
    prompt = f"""
You are a professional content editor. 
Summarize this full blog into a 300-400 word professional article 
suitable for technical blogs and newsletters. Maintain conversational tone.
Add a 'Key Takeaways' section with 3 to 5 bullets.

BLOG:
{full_blog}
"""
    response = ollama.chat(model=model_name, messages=[
        {"role": "user", "content": prompt}]
    )

    condensed_text = response['message']['content'].strip()

    return condensed_text