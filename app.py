from workflows.blog_graph import create_blog_graph

def run_blog_agentic_flow(video_url: str):
    blog_graph = create_blog_graph()
    result = blog_graph.invoke({"video_url": video_url})
    return result["blog"]

if __name__ == "__main__":
    url = input("Enter YouTube video URL: ")
    blog = run_blog_agentic_flow(url)
    print("\n--- 📝 Generated Blog ---\n")
    print(blog)