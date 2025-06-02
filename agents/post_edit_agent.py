# agents/post_edit_agent.py

import ollama

# IMPROVEMENT: Post-edit agent → polishes blog for grammar, flow, readability

def post_edit_blog(blog_text: str, model="phi4-mini") -> str:
    prompt = f"""
You are an expert blog editor.

Please polish the following blog for grammar, style, flow, and readability.

Keep the meaning the same. Keep the headings and sections.

Make it sound natural, engaging, and easy to read.

BLOG:
{blog_text}
"""
    response = ollama.chat(model=model, messages=[
        {"role": "user", "content": prompt}
    ])
    edited_blog = response["message"]["content"]
    return edited_blog.strip()