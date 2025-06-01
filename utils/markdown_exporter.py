import markdownify
import os

def export_to_markdown(blog_content: str, filename="blog_post.md") -> str:
    md_text = markdownify.markdownify(blog_content, heading_style="ATX")
    with open(filename, "w") as f:
        f.write(md_text)
    return os.path.abspath(filename)