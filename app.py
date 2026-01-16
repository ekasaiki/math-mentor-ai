import streamlit as st
from datetime import datetime

# =============================
# Agents
# =============================
from agents.parser_agent import parse_problem
from agents.intent_router import route_intent
from agents.solver_agent import solve_problem
from agents.verifier_agent import verify_solution
from agents.explainer_agent import explain_solution

# =============================
# RAG
# =============================
from rag.retriever import build_vectorstore, retrieve_context

# =============================
# Multimodal
# =============================
from multimodal.ocr import extract_text_from_image
from multimodal.asr import transcribe_audio

# =============================
# Memory
# =============================
from memory.memory_store import save_to_memory, find_similar_by_topic


# =============================
# Streamlit Config
# =============================
st.set_page_config(page_title="Math Mentor AI", layout="wide")
st.title("🧠 Math Mentor AI")
st.caption("Multimodal AI Tutor for JEE-style Math Problems")

# =============================
# Load Vector Store
# =============================
@st.cache_resource
def load_vectorstore():
    return build_vectorstore()

vectorstore = load_vectorstore()

# =============================
# HITL PANEL
# =============================
def hitl_panel(reason: str):
    st.warning(f"🧑‍⚖️ HITL Triggered: {reason}")
    return st.radio(
        "Human Review Required:",
        ["Approve", "Edit and Re-run", "Reject"],
        key=f"hitl_{reason}"
    )

# =============================
# INPUT MODE
# =============================
input_mode = st.radio("Choose input type:", ["Text", "Image", "Audio"])
st.divider()

user_text = ""

# =============================
# TEXT INPUT
# =============================
if input_mode == "Text":
    user_text = st.text_area("✍️ Enter math problem", height=150)

# =============================
# IMAGE INPUT (OCR)
# =============================
elif input_mode == "Image":
    image = st.file_uploader("📷 Upload math image", ["png", "jpg", "jpeg"])
    if image:
        extracted_text, confidence = extract_text_from_image(image)
        st.info(f"OCR confidence: {confidence}")
        user_text = st.text_area("Extracted text (editable)", extracted_text)

# =============================
# AUDIO INPUT (ASR)
# =============================
elif input_mode == "Audio":
    audio = st.audio_input("🎤 Record your question")
    if audio:
        transcript, confidence = transcribe_audio(audio)
        st.info(f"ASR confidence: {confidence}")
        user_text = st.text_area("Transcribed text (editable)", transcript)

# =============================
# SOLVE BUTTON
# =============================
st.divider()
solve = st.button("🚀 Solve Problem")

# =============================
# MAIN PIPELINE
# =============================
if solve and user_text.strip():

    # -------- Parser Agent --------
    st.subheader("🧠 Parser Agent")
    parsed = parse_problem(user_text)
    st.json(parsed)

    if parsed.get("needs_clarification"):
        if hitl_panel("Parser ambiguity") != "Approve":
            st.stop()

    # -------- Intent Router --------
    st.subheader("🧭 Intent Router")
    route = route_intent(parsed)
    st.success(route)

    # -------- Memory Lookup --------
    st.subheader("🧠 Memory Agent")
    past = find_similar_by_topic(parsed["topic"])
    if past:
        for p in past:
            st.info(p["final_answer"])
    else:
        st.caption("No similar past problems")

    # -------- RAG Retriever --------
    st.subheader("📚 RAG Retriever")
    retrieved_docs = retrieve_context(vectorstore, parsed["problem_text"])

    if not retrieved_docs:
        st.error("No relevant documents found")
        st.stop()

    for i, doc in enumerate(retrieved_docs):
        st.markdown(f"*Doc {i+1}*")
        st.code(doc, language="markdown")

    # -------- Solver Agent --------
    st.subheader("🧮 Solver Agent")
    solution = solve_problem(parsed, retrieved_docs)

    st.success(solution.get("answer", "No answer generated"))
    st.json({
        "used_formula": solution.get("used_formula", "Not found"),
        "method": solution.get("method", "Not found")
    })

    # -------- Verifier Agent --------
    st.subheader("✅ Verifier Agent")
    verification = verify_solution(parsed, solution)
    st.progress(verification.get("confidence", 0.5))

    if verification.get("needs_hitl"):
        if hitl_panel("Low confidence") != "Approve":
            st.stop()

    # -------- Explainer Agent --------
    st.subheader("📖 Explainer Agent")
    explanation = explain_solution(parsed, solution)
    st.write(explanation)

    # -------- Save to Memory --------
    save_to_memory({
        "timestamp": str(datetime.now()),
        "original_input": user_text,
        "parsed_problem": parsed,
        "retrieved_context": retrieved_docs,
        "final_answer": solution.get("answer"),
        "confidence": verification.get("confidence")
    })

    # -------- Feedback --------
    st.subheader("🧠 Feedback")
    c1, c2 = st.columns(2)

    with c1:
        if st.button("✅ Correct"):
            st.success("Saved as correct")

    with c2:
        if st.button("❌ Incorrect"):
            st.warning("Saved as incorrect")