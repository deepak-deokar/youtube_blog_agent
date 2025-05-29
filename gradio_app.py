import gradio as gr
from workflows.blog_graph import create_blog_graph

# Graph executor
blog_graph = create_blog_graph()

def generate_blog_from_youtube(video_url: str):
    try:
        result = blog_graph.invoke({"video_url": video_url})
        return result["blog"]
    except Exception as e:
        return f"Error: {e}"

# Define the Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# 🎬 YouTube to Blog Generator")
    with gr.Row():
        youtube_input = gr.Textbox(label="YouTube URL", placeholder="Paste YouTube link here...")
    with gr.Row():
        generate_btn = gr.Button("Generate Blog")
    blog_output = gr.Markdown()

    generate_btn.click(fn=generate_blog_from_youtube, inputs=youtube_input, outputs=blog_output)

# Run the app
if __name__ == "__main__":
    demo.launch()