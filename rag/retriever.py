from sentence_transformers import SentenceTransformer, util
import os

model = SentenceTransformer("all-MiniLM-L6-v2")
KB_PATH = "data/math_kb"

def build_vectorstore():
    docs = []
    for file in os.listdir(KB_PATH):
        if file.endswith(".md"):
            with open(os.path.join(KB_PATH, file), "r", encoding="utf-8") as f:
                docs.append(f.read())

    embeddings = model.encode(docs, convert_to_tensor=True)
    return {"docs": docs, "embeddings": embeddings}

def retrieve_context(vectorstore, query, k=3):
    query_emb = model.encode(query, convert_to_tensor=True)
    scores = util.cos_sim(query_emb, vectorstore["embeddings"])[0]
    top_k = scores.topk(k).indices

    return [vectorstore["docs"][i] for i in top_k]
