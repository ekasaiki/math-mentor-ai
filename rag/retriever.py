# rag/retriever.py
import os

KB_PATH = "data/math_kb"

def retrieve_context(query: str, top_k: int = 3):
    """
    Simple keyword-based retrieval (EXAM SAFE)
    """
    results = []
    query_lower = query.lower()

    for file in os.listdir(KB_PATH):
        if not file.endswith(".md"):
            continue

        with open(os.path.join(KB_PATH, file), "r", encoding="utf-8") as f:
            content = f.read()

            # simple keyword match
            if any(word in content.lower() for word in query_lower.split()):
                results.append({
                    "source": file,
                    "content": content
                })

    return results[:top_k]