# agents/blog_agent.py

import ollama

# IMPROVEMENT: Now blog sections have proper headings

def generate_blog(summary: str, topics: list[str], style: str = "neutral", sentiment: str = "neutral", entities=None, enriched_facts=None, model="phi4-mini") -> str:
    topic_sections = ""
    for topic in topics:
        fact = enriched_facts.get(topic, "")
        # IMPROVEMENT: Stronger prompt → add tone and fact
        prompt = (
            f"Write a blog section about '{topic}' with tone '{style}'. "
            f"Use this video summary and external fact if helpful.\n\n"
            f"Summary:\n{summary}\n\n"
            f"Fact:\n{fact}"
        )
        response = ollama.chat(model=model, messages=[
            {"role": "user", "content": prompt}
        ])
        # IMPROVEMENT: Add proper section heading
        section = f"## {topic}\n\n{response['message']['content']}\n"
        topic_sections += section

    # Final blog intro
    intro_prompt = (
        f"Write an engaging introduction for this blog with tone '{style}'. "
        f"Topics: {', '.join(topics)}\n\n"
        f"Summary:\n{summary}"
    )
    intro = ollama.chat(model=model, messages=[
        {"role": "user", "content": intro_prompt}
    ])["message"]["content"]

    # Final blog conclusion
    conclusion_prompt = (
        f"Write a short conclusion for a blog covering these topics with tone '{style}'. "
        f"Topics: {', '.join(topics)}"
    )
    conclusion = ollama.chat(model=model, messages=[
        {"role": "user", "content": conclusion_prompt}
    ])["message"]["content"]

    # Entity references
    if entities:
        entity_section = "### Referenced Entities:\n" + "\n".join(f"- {e}" for e in entities) + "\n\n"
    else:
        entity_section = ""

    # Assemble full blog
    full_blog = (
        f"# {generate_blog_title(summary, model)}\n\n"
        f"{intro}\n\n"
        f"{entity_section}"
        f"{topic_sections}\n"
        f"### Conclusion\n\n{conclusion}"
    )
    return full_blog

def generate_blog_title(summary: str, model="phi4-mini") -> str:
    prompt = (
        f"Based on this summary, generate a catchy blog title:\n\n{summary}"
    )
    response = ollama.chat(model=model, messages=[
        {"role": "user", "content": prompt}
    ])
    return response["message"]["content"].strip().strip('"')