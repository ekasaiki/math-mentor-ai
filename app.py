import streamlit as st
from datetime import datetime

# ====== Agents ======
from agents.parser_agent import parse_problem
from agents.intent_router import route_intent
from agents.solver_agent import solve_problem
from agents.verifier_agent import verify_solution
from agents.explainer_agent import explain_solution

# ====== RAG ======
from rag.retriever import build_vectorstore, retrieve_context

# ====== Memory ======
from memory.memory_store import save_to_memory

# =============================
# Streamlit Config
# =============================
st.set_page_config(page_title="Math Mentor AI", layout="wide")
st.title("🧠 Math Mentor AI")
st.caption("Reliable Multimodal Math Mentor (RAG + Agents + HITL + Memory)")

# =============================
# Cache Vector Store
# =============================
@st.cache_resource
def load_vs():
    return build_vectorstore()

vectorstore = load_vs()

# =============================
# Session State (PREVENT VANISH)
# =============================
if "result" not in st.session_state:
    st.session_state.result = None

# =============================
# Input Mode
# =============================
input_mode = st.radio("Choose input type:", ["Text", "Image", "Audio"])

user_text = ""

if input_mode == "Text":
    user_text = st.text_area("✍️ Enter math problem", height=120)

elif input_mode == "Image":
    from multimodal.ocr import extract_text_from_image
    img = st.file_uploader("📷 Upload image", type=["jpg", "png"])
    if img:
        text, conf = extract_text_from_image(img)
        st.info(f"OCR Confidence: {conf}")
        user_text = st.text_area("Extracted Text", text)

elif input_mode == "Audio":
    from multimodal.asr import transcribe_audio
    audio = st.audio_input("🎤 Speak problem")
    if audio:
        text, conf = transcribe_audio(audio)
        st.info(f"ASR Confidence: {conf}")
        user_text = st.text_area("Transcript", text)

# =============================
# Solve Button
# =============================
if st.button("🚀 Solve Problem") and user_text.strip():

    st.session_state.result = {}

    # ===== Parser Agent =====
    parsed = parse_problem(user_text)
    st.subheader("🧠 Parser Agent")
    st.json(parsed)
    st.session_state.result["parsed"] = parsed

    # ===== Intent Router =====
    intent = route_intent(parsed)
    st.subheader("🧭 Intent Router Agent")
    st.success(intent)

    # ===== RAG Retriever =====
    docs = retrieve_context(vectorstore, parsed["problem_text"])
    st.subheader("📚 RAG Retriever")
    for i, d in enumerate(docs):
        st.info(f"Source {i+1}: {d}")

    # ===== Solver Agent =====
    solution = solve_problem(parsed, docs)
    st.subheader("🧮 Solver Agent")
    st.success(solution["answer"])
    st.code(solution["reasoning"])

    # ===== Verifier Agent =====
    verify = verify_solution(parsed, solution)
    st.subheader("🔍 Verifier Agent")
    st.json(verify)

    # ===== Explainer Agent =====
    explanation = explain_solution(parsed, solution)
    st.subheader("📖 Explainer Agent")
    st.write(explanation)

    # ===== Memory Save =====
    save_to_memory({
        "time": str(datetime.now()),
        "question": user_text,
        "parsed": parsed,
        "answer": solution["answer"]
    })

    st.session_state.result["final"] = solution["answer"]

# =============================
# Persist Final Answer
# =============================
if st.session_state.result:
    st.divider()
    st.subheader("✅ Final Answer (Persisted)")
    st.success(st.session_state.result.get("final", ""))