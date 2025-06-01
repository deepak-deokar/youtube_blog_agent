def chunk_text(text: str, chunk_size: int = 1500, overlap: int = 100) -> list:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap  # slight overlap for context
    return chunks