___# youtube_blog_agent
# 🎬 YouTube-to-Blog Generator (Agentic AI Pipeline)

A multi-agent Generative AI application that transforms **YouTube videos into polished blog articles** using advanced LLM workflows.

✨ Built with:
- **LangGraph** (multi-agent orchestration)
- **Ollama** (LLM backend — e.g. `phi4-mini`, `phi4`, `mistral`, etc.)
- **Gradio** (user-friendly UI)
- **ROUGE-based evaluation**
- **Wikipedia RAG** for enrichment
- **Post-edit agent** for polished output

---

## 🚀 Features

✅ Extracts transcript from YouTube video  
✅ Hierarchical summarization → high-quality summary  
✅ Topic extraction  
✅ Dynamic RAG (Wikipedia) → enriches the blog  
✅ Sentiment detection  
✅ NER extraction (cleaned)  
✅ Blog generation → with **section headings**  
✅ Post-editing → improves flow, grammar  
✅ Condensed version → 1-pager blog  
✅ Gradio UI → with progress bar  
✅ Evaluation tab → ROUGE scores vs reference summary 🚀  
✅ Configurable via `config.yaml`

---

## 🖼️ App Architecture

```markdown
YouTube URL
    ↓
Transcript Extraction (YouTubeTranscriptAPI)
    ↓
Hierarchical Summarization (chunked)
    ↓
Topic Extraction
    ↓
 ┌───────────────┐
 │  Dynamic RAG  │ ← Skips if short video
 └───────────────┘
    ↓
Sentiment Detection
    ↓
NER Extraction
    ↓
Blog Generation (LLM)
    ↓
Post-Edit Agent (LLM)
    ↓
Condensed Blog (LLM)
    ↓
Gradio App (UI + Evaluation)

```

## ⚙️Installation
```bash
#Clone the repo
git clone https://github.com/deepak-deokar/youtube_blog_agent.git
cd youtube_blog_agent

# Recommended: create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install ROUGE scorer
pip install rouge-score

# (Optional) If using Ollama models:
# Make sure Ollama is running locally: https://ollama.com/download

# Start Gradio app
python gradio_app.py
```
---

## ✨Usage

    1️⃣ Paste a YouTube URL.
    2️⃣ Choose Blog Style (neutral, casual, professional, humorous).
    3️⃣ Click Generate Blog.
    4️⃣ View Full Blog or Condensed Blog.
    5️⃣ Optionally → paste YouTube description or manual reference → get ROUGE evaluation 🚀.

## 🚀 Key Technologies
	•	LangGraph (multi-agent orchestration)
	•	LangChain Core
	•	Ollama
	•	Gradio
	•	Wikipedia RAG
	•	ROUGE evaluation
	•	YAML config