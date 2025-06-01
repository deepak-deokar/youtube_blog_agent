import gradio as gr
from workflows.blog_graph import create_blog_graph
from utils.markdown_exporter import export_to_markdown
import os
import json

# Graph executor
blog_graph = create_blog_graph()

# Save blog history
def save_blog_to_history(url, style, blog, condensed):
    entry = {"url": url, "style": style, "blog": blog, "condensed": condensed}
    if os.path.exists("blog_history.json"):
        with open("blog_history.json", "r") as f:
            data = json.load(f)
    else:
        data = []
    data.append(entry)
    with open("blog_history.json", "w") as f:
        json.dump(data, f, indent=2)

# Blog generator function — blocking version
def generate_blog_from_youtube(video_url: str, style: str):
    try:
        result = blog_graph.invoke({"video_url": video_url, "style": style})
        blog = result["blog"]
        condensed = result.get("condensed", "")
        save_blog_to_history(video_url, style, blog, condensed)
        return blog, condensed
    except Exception as e:
        return f"Error: {e}", ""

# Download function
def download_blog(content):
    with open("blog_output.txt", "w") as f:
        f.write(content)
    return "blog_output.txt"

# Markdown export function
def export_md(content):
    return export_to_markdown(content)

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

    # Tabbed view for Full / Condensed
    with gr.Tabs():
        with gr.TabItem("Full Blog"):
            blog_output = gr.Markdown(label="Full Blog")
        with gr.TabItem("Condensed Blog (1-Pager)"):
            condensed_output = gr.Markdown(label="Condensed Blog (1-Pager)")

    # Dropdown to choose version for export
    export_dropdown = gr.Dropdown(
        choices=["Full Blog", "Condensed Blog"],
        label="Choose version to export",
        value="Full Blog"
    )

    download_btn = gr.Button("Download as TXT")
    markdown_btn = gr.Button("Export as Markdown")
    file_output = gr.File()

    # Button logic → blocking version
    generate_btn.click(
        fn=generate_blog_from_youtube,
        inputs=[youtube_input, style_dropdown],
        outputs=[blog_output, condensed_output]
    )

    def download_selected(version, full, condensed):
        content = full if version == "Full Blog" else condensed
        return download_blog(content)

    def export_md_selected(version, full, condensed):
        content = full if version == "Full Blog" else condensed
        return export_md(content)

    download_btn.click(
        fn=download_selected,
        inputs=[export_dropdown, blog_output, condensed_output],
        outputs=file_output
    )

    markdown_btn.click(
        fn=export_md_selected,
        inputs=[export_dropdown, blog_output, condensed_output],
        outputs=file_output
    )

# Run the app
if __name__ == "__main__":
    demo.launch()