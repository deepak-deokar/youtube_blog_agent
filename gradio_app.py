import gradio as gr
from workflows.blog_graph import create_blog_graph
import os
import json

# Graph executor
blog_graph = create_blog_graph()

# Save blog history
def save_blog_to_history(url, style, blog):
    entry = {"url": url, "style": style, "blog": blog}
    if os.path.exists("blog_history.json"):
        with open("blog_history.json", "r") as f:
            data = json.load(f)
    else:
        data = []
    data.append(entry)
    with open("blog_history.json", "w") as f:
        json.dump(data, f, indent=2)

# Blog generator function
def generate_blog_from_youtube(video_url: str, style: str):
    try:
        result = blog_graph.invoke({"video_url": video_url, "style": style})
        blog = result["blog"]
        save_blog_to_history(video_url, style, blog)
        return blog
    except Exception as e:
        return f"Error: {e}"

# Download function
def download_blog(content):
    with open("blog_output.txt", "w") as f:
        f.write(content)
    return "blog_output.txt"

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# 🎬 YouTube to Blog Generator")

    with gr.Row():
        youtube_input = gr.Textbox(label="YouTube URL", placeholder="Paste YouTube link here...")

    with gr.Row():
        style_dropdown = gr.Dropdown(
            choices=["neutral", "casual", "professional", "humorous"],
            label="Choose Blog Style",
            value="neutral"
        )

    with gr.Row():
        generate_btn = gr.Button("Generate Blog")

    blog_output = gr.Markdown()

    download_btn = gr.Button("Download Blog")
    file_output = gr.File()

    generate_btn.click(fn=generate_blog_from_youtube, inputs=[youtube_input, style_dropdown], outputs=blog_output)
    download_btn.click(fn=download_blog, inputs=blog_output, outputs=file_output)

# Run the app
if __name__ == "__main__":
    demo.launch()