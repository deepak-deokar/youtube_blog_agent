# agents/chunking_agent.py

# IMPROVEMENT: Changed to paragraph-aware chunking → avoids cutting mid-sentence

def chunk_text(text: str, max_chunk_chars=2000) -> list:
    """Chunk text by paragraph boundaries (~max_chunk_chars per chunk)."""
    # IMPROVEMENT: Split by paragraphs (double newline)
    paragraphs = text.split("\n\n")
    chunks = []
    current_chunk = ""

    for para in paragraphs:
        if len(current_chunk) + len(para) < max_chunk_chars:
            current_chunk += para + "\n\n"
        else:
            # IMPROVEMENT: Add completed chunk
            chunks.append(current_chunk.strip())
            current_chunk = para + "\n\n"

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    print(f"[DEBUG] Created {len(chunks)} chunks.")
    return chunks