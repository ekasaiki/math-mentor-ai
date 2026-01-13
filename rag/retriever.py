import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

KB_PATH = "data/math_kb"

def load_documents():
    docs = []
    for file in os.listdir(KB_PATH):
        if file.endswith(".md"):
            with open(os.path.join(KB_PATH, file), "r", encoding="utf-8") as f:
                docs.append(f.read())
    return docs


def build_vectorstore():
    raw_docs = load_documents()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=50
    )

    documents = splitter.create_documents(raw_docs)

    # ✅ LOCAL EMBEDDINGS (NO API KEY)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(documents, embeddings)
    return vectorstore


def retrieve_context(vectorstore, query, k=3):
    return vectorstore.similarity_search(query, k=k)
