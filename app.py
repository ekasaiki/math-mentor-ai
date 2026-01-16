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
# Memory
# =============================
from memory.memory_store import save_to_memory, find_similar_by_topic

# =============================
# Multimodal
# =============================
from multimodal.ocr import extract_text_from_image
from multimodal.asr import transcribe_audio


# =============================
# Streamlit Config
# =============================
st.set_page_config(page_title="Math Mentor AI", layout="wide")
st.title("🧠 Math Mentor AI")
st.write("Multimodal AI Tutor for JEE-style Math Problems")

# =============================
# Cache Vector Store
# =============================
@st.cache_resource
def load_vectorstore():
    return build_vectorstore()

vectorstore = load_vectorstore()

# =============================
# HITL Panel
# =============================
def hitl_panel(reason: str):
    st.warning(f"🧑‍⚖️ HITL Triggered: {reason}")
    return st.radio(
        "Human Review Required:",
        ["Approve", "Edit and Re-run", "Reject"],
        key=f"hitl_{reason}"
    )

# =============================
# Input Mode
# =============================
input_mode = st.radio(
    "Choose input type:",
    ["Text", "Image", "Audio"]
)

st.divider()
user_text = ""

# =============================
# TEXT
# =============================
if input_mode == "Text":
    user_text = st.text_area("✍️ Type your math question", height=150)

# =============================
# IMAGE
# =============================
elif input_mode == "Image":
    image = st.file_uploader("📷 Upload image", type=["jpg", "jpeg", "png"])
    if image:
        extracted_text, confidence = extract_text_from_image(image)
        st.write(f"OCR Confidence: {confidence}")
        user_text = st.text_area("Extracted text", extracted_text)

# =============================
# AUDIO
# =============================
elif input_mode == "Audio":
    audio = st.audio_input("🎤 Record your math question")
    if audio:
        transcript, confidence = transcribe_audio(audio)
        st.write(f"ASR Confidence: {confidence}")
        user_text = st.text_area("Transcribed text", transcript)

# =============================
# Solve Button
# =============================
st.divider()
solve = st.button("🚀 Solve Problem")

# =============================
# MAIN PIPELINE
# =============================
if solve and user_text.strip():

    # -----------------------------
    # 1️⃣ Parser Agent
    # -----------------------------
    st.subheader("🧠 Parser Agent")
    parsed = parse_problem(user_text)
    st.json(parsed)

    if parsed.get("needs_clarification"):
        if hitl_panel("Parser ambiguity") != "Approve":
            st.stop()

    # -----------------------------
    # 2️⃣ Intent Router
    # -----------------------------
    st.subheader("🧭 Intent Router")
    route = route_intent(parsed)
    st.success(f"Routed to: {route}")

    # -----------------------------
    # 3️⃣ Memory Lookup
    # -----------------------------
    st.subheader("🧠 Memory Agent")
    past = find_similar_by_topic(parsed["topic"])
    if past:
        for p in past:
            st.info(p["final_answer"])
    else:
        st.info("No similar past problems found.")

    # -----------------------------
    # 4️⃣ Retriever (RAG)
    # -----------------------------
    st.subheader("📚 Retriever Agent")
    retrieved_docs = retrieve_context(vectorstore, parsed["problem_text"])

    if not retrieved_docs:
        st.error("No relevant documents retrieved.")
        st.stop()

    for i, doc in enumerate(retrieved_docs):
        st.markdown(f"*Document {i+1}*")
        st.code(doc)

    # -----------------------------
    # 5️⃣ SOLVER AGENT ✅ FIXED
    # -----------------------------
    solution = solve_problem(parsed, retrieved_docs)

    st.subheader("🧮 Solver Agent")
    st.success(solution["answer"])

    st.json({
        "used_formula": solution.get("used_formula", "Not available"),
        "method": solution.get("method", "Not specified")
    })

    # -----------------------------
    # 6️⃣ Verifier Agent
    # -----------------------------
    st.subheader("🔍 Verifier Agent")
    verification = verify_solution(parsed, solution)
    st.progress(verification.get("confidence", 0.5))

    if verification.get("needs_hitl"):
        if hitl_panel("Low verifier confidence") != "Approve":
            st.stop()

    # -----------------------------
    # 7️⃣ Explainer Agent
    # -----------------------------
    st.subheader("📖 Explainer Agent")
    explanation = explain_solution(parsed, solution)
    st.write(explanation)

    # -----------------------------
    # 8️⃣ Save to Memory
    # -----------------------------
    save_to_memory({
        "timestamp": str(datetime.now()),
        "input": user_text,
        "parsed": parsed,
        "answer": solution["answer"],
        "formula": solution.get("used_formula"),
        "confidence": verification.get("confidence")
    })

    # -----------------------------
    # 9️⃣ Feedback
    # -----------------------------
    st.subheader("🧠 Feedback")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("✅ Correct"):
            st.success("Feedback saved")

    with col2:
        if st.button("❌ Incorrect"):
            st.warning("Feedback saved")