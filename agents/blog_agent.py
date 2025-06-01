import ollama

def generate_blog(summary: str, topics: list[str], style: str = "neutral", sentiment: str = "neutral", entities=None, enriched_facts=None, model="phi4-mini") -> str:
    topic_sections = ""
    for topic in topics:
        fact = enriched_facts.get(topic, "")
        prompt = (
            f"Write a short blog section about the topic '{topic}' based on the following summary.\n"
            f"Keep the tone {sentiment or style}.\n\n"
            f"Summary:\n{summary}\n\n"
            f"External Info:\n{fact}\n"
        )
        
        # Stream response
        response_stream = ollama.chat(model=model, messages=[
            {"role": "user", "content": prompt}
        ], stream=True)

        section_text = ""
        for chunk in response_stream:
            section_text += chunk['message']['content']
        
        section = f"## {topic}\n\n{section_text}\n"
        topic_sections += section

    # Final blog intro
    intro_prompt = (
        f"Write an engaging introduction for a blog with the following topics and tone: {style}.\n"
        f"Topics: {', '.join(topics)}\n"
        f"Summary:\n{summary}"
    )
    intro_stream = ollama.chat(model=model, messages=[{"role": "user", "content": intro_prompt}], stream=True)
    intro_text = ""
    for chunk in intro_stream:
        intro_text += chunk['message']['content']

    # Final blog conclusion
    conclusion_prompt = (
        f"Write a brief conclusion for a blog covering these topics with tone: {style}.\n"
        f"Topics: {', '.join(topics)}\n"
    )
    conclusion_stream = ollama.chat(model=model, messages=[{"role": "user", "content": conclusion_prompt}], stream=True)
    conclusion_text = ""
    for chunk in conclusion_stream:
        conclusion_text += chunk['message']['content']

    # Entity Section
    if entities:
        entity_section = "### Referenced in this video:\n" + "\n".join(f"- {e}" for e in entities) + "\n\n"
    else:
        entity_section = ""

    # Final Blog Assembly
    full_blog = (
        f"# {generate_blog_title(summary, model)}\n\n"
        f"{intro_text}\n\n"
        f"{entity_section}"
        f"{topic_sections}\n"
        f"### Conclusion\n\n{conclusion_text}"
    )
    return full_blog


def generate_blog_title(summary: str, model="phi4-mini") -> str:
    prompt = (
        f"Based on the following summary, generate a catchy blog post title.\n\n"
        f"{summary}"
    )
    
    response_stream = ollama.chat(model=model, messages=[
        {"role": "user", "content": prompt}
    ], stream=True)

    title_text = ""
    for chunk in response_stream:
        title_text += chunk['message']['content']

    return title_text.strip().strip('"')