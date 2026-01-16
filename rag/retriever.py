import os

KB_PATH = "data/math_kb"

def build_vectorstore():
    documents = []

    for file in os.listdir(KB_PATH):
        if file.endswith(".md"):
            with open(os.path.join(KB_PATH, file), "r", encoding="utf-8") as f:
                documents.append({
                    "source": file,
                    "content": f.read().lower()
                })

    return documents


def retrieve_context(vectorstore, query, k=3):
    query = query.lower()
    matches = []

    for doc in vectorstore:
        score = sum(1 for word in query.split() if word in doc["content"])
        if score > 0:
            matches.append((score, doc))

    matches.sort(reverse=True, key=lambda x: x[0])
    return [m[1]["content"] for m in matches[:k]]