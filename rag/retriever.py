import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

KB_PATH = "data/math_kb"

def load_documents():
    docs = []
    for file in os.listdir(KB_PATH):
        if file.endswith(".md"):
            with open(os.path.join(KB_PATH, file), "r", encoding="utf-8") as f:
                docs.append(f.read())
    return docs

def build_vectorstore():
    docs = load_documents()
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(docs)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))

    return {
        "index": index,
        "docs": docs,
        "model": model
    }

def retrieve_context(vectorstore, query, k=3):
    q_emb = vectorstore["model"].encode([query])
    _, I = vectorstore["index"].search(np.array(q_emb), k)
    return [vectorstore["docs"][i] for i in I[0]]
